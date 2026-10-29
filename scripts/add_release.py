#!/usr/bin/env python3
"""Add (or replace) a release-notes entry and optionally swap the home-page screenshots.

usage: add_release.sh <build> <notes.md> [shots_dir]

<build>     "25" or "1.0.0+25"
<notes.md>  optional first line `at: 2026-10-29 10:13` (KST; default = $RELEASE_AT, else now in KST), then
            `## ko` and `## en` sections, one `- ` bullet per line. Without any `##` section the whole file is
            the Korean text (the app's `<n>.ko.md`); English then comes from a sibling `<n>.en.md` if present,
            else the page shows the Korean text for English too.
[shots_dir] optional; `map.*` and/or `march.*` replace the two home screenshots; if neither exists, the first
            two images (by file name) become map and march. Cropped to 1200x554, saved as
            assets/shot-<name>.webp and -600.webp.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOTS = {"map": "shot-map", "march": "shot-march"}
EXTS = ("png", "jpg", "jpeg", "webp")
W, H = 1200, 554


def norm_build(b):
    b = b.strip()
    if re.fullmatch(r"\d+", b):
        return "1.0.0+" + b
    if re.fullmatch(r"\d+\.\d+\.\d+\+\d+", b):
        return b
    raise ValueError("build must be N or 1.0.0+N, got %r" % b)


def parse_notes(text, sibling_en=None):
    if not re.search(r"^## ", text, re.M):  # plain bullets = Korean only
        text = "## ko\n" + text + ("\n## en\n" + sibling_en if sibling_en else "")
    at, lang, out = None, None, {"ko": [], "en": []}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = re.match(r"at:\s*(.+)$", line)
        if m and lang is None:
            at = m.group(1).strip()
        elif line.startswith("## "):
            lang = line[3:].strip().lower()
            if lang not in out:
                raise ValueError("unknown section %r (only ko, en)" % lang)
        elif line.startswith("- ") and lang:
            out[lang].append(line[2:].strip())
        else:
            raise ValueError("unexpected line: %r" % raw)
    if not out["ko"]:
        raise ValueError("section 'ko' is empty")
    if not out["en"]:
        out["en"] = list(out["ko"])
    if at is None:
        at = os.environ.get("RELEASE_AT") or (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")
    return at, out["ko"], out["en"]


def upsert(path, build, at, ko, en):
    data = json.loads(path.read_text(encoding="utf-8"))
    entry = {"build": build, "at": at, "ko": ko, "en": en}
    entries = [e for e in data["entries"] if e["build"] != build]
    replaced = len(entries) != len(data["entries"])
    data["entries"] = [entry] + entries
    data["entries"].sort(key=lambda e: -int(e["build"].split("+")[1]))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return replaced


def replace_shots(shots_dir, assets_dir):
    from PIL import Image
    done = []
    files = sorted(p for p in Path(shots_dir).glob("*") if p.suffix.lower().lstrip(".") in EXTS) if Path(shots_dir).is_dir() else []
    named = {k: next((p for p in files if p.stem == k), None) for k in SHOTS}
    if not any(named.values()):
        named = dict(zip(SHOTS, files[:2]))
    for key, name in SHOTS.items():
        src = named.get(key)
        if not src:
            continue
        im = Image.open(src).convert("RGB")
        w, h = im.size
        ch = round(w * H / W)
        if ch > h:  # too wide for the frame: crop the sides instead
            cw = round(h * W / H)
            im = im.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h))
        else:
            im = im.crop((0, h - ch, w, h))
        im.resize((W, H), Image.LANCZOS).save(Path(assets_dir) / (name + ".webp"), quality=82)
        im.resize((W // 2, H // 2), Image.LANCZOS).save(Path(assets_dir) / (name + "-600.webp"), quality=82)
        done.append(name)
    return done


def main(argv):
    if len(argv) not in (3, 4):
        sys.exit(__doc__)
    build = norm_build(argv[1])
    md = Path(argv[2])
    en_md = md.with_name(md.name.replace(".ko.md", ".en.md")) if ".ko.md" in md.name else None
    sibling = en_md.read_text(encoding="utf-8") if en_md and en_md.is_file() else None
    at, ko, en = parse_notes(md.read_text(encoding="utf-8"), sibling)
    replaced = upsert(ROOT / "content" / "releases.json", build, at, ko, en)
    print("%s %s (%s)" % ("replaced" if replaced else "added", build, at))
    if len(argv) == 4:
        print("screenshots:", ", ".join(replace_shots(argv[3], ROOT / "assets")) or "none found")
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build_site.py")])
    print("next: python3 -m unittest discover -s tests, then commit and push to main")


if __name__ == "__main__":
    main(sys.argv)
