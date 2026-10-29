#!/usr/bin/env python3
"""Publish the next queued blog post (daily 12:00 KST, run by launchd on the Mac mini — see scripts/launchd/README.md).

    python3 scripts/publish_blog.py                 # next post in content/blog/queue/ -> posts/, build, test, commit, push main
    python3 scripts/publish_blog.py --dry-run       # validate + say what would happen; writes nothing
    python3 scripts/publish_blog.py --no-push       # everything except the push (commit stays local)
    python3 scripts/publish_blog.py --slug my-slug  # a specific queued post instead of the first one
    python3 scripts/publish_blog.py --force         # allow a 2nd post on the same KST day

The queue is `content/blog/queue/<NNN>-<slug>/{en,ko,ja,zh,es,pt,id,ru,vi,fr,de}.md` (NNN = order; this script is the only writer of
posts/, humans only add reviewed folders to the queue). Nothing is published unless all 11 files pass the structure check + the safety lint
(scripts/blog.py). One post per KST day: if a post was already published today the script exits 0 without doing anything.
Any failure after files moved rolls the working tree back (it must be clean when the script starts) and exits 1.
"""
import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blog  # noqa: E402

ROOT = blog.ROOT
KST = blog.KST


def queue_dirs(root):
    q = Path(root) / "content" / "blog" / "queue"
    return sorted(p for p in q.glob("*") if p.is_dir()) if q.is_dir() else []


def queue_slug(d):
    m = re.match(r"^(\d+)-(.+)$", d.name)
    if not m:
        raise blog.BlogError("queue folder %r must be named <NNN>-<slug> (e.g. 001-first-post)" % d.name)
    return m.group(2)


def published_today(root, today):
    base = Path(root) / "content" / "blog" / "posts"
    for f in base.glob("*/en.md"):
        meta, _ = blog.parse(f.read_text(encoding="utf-8"), str(f))
        if meta.get("published", "")[:10] == today:
            return f.parent.name
    return None


def validate(d, slug, root):
    if not blog.SLUG_RE.match(slug) or slug in blog.RESERVED:
        raise blog.BlogError("bad slug %r (kebab-case English, not a language code/feed/page)" % slug)
    if (Path(root) / "content" / "blog" / "posts" / slug).exists():
        raise blog.BlogError("slug %r is already published" % slug)
    files = blog.check_post_files(d, slug, published=False)
    problems = []
    for lang in blog.LANGS:
        for prob in blog.lint((d / (lang + ".md")).read_text(encoding="utf-8")):
            problems.append("%s.md: %s" % (lang, prob))
    if problems:
        raise blog.BlogError("safety lint: " + "; ".join(problems))
    return files


def stamp(text, when):
    head, sep, rest = text.replace("\r\n", "\n")[4:].partition("\n---")
    head = re.sub(r"^(published|date):.*\n?", "", head, flags=re.M).rstrip("\n")
    head += "\ndate: %s\npublished: %s" % (when.date().isoformat(), when.isoformat(timespec="seconds"))
    return "---\n" + head + "\n---" + rest


def run(cmd, root, check=True):
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=str(root), check=check)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--no-git", action="store_true", help="skip git entirely (tests)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--at", help="ISO time with +09:00 (tests); default now")
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args(argv)
    root = Path(a.root)
    now = dt.datetime.fromisoformat(a.at) if a.at else dt.datetime.now(KST)
    when = now.astimezone(KST).replace(second=0, microsecond=0)
    today = when.date().isoformat()

    queue = queue_dirs(root)
    if a.slug:
        queue = [d for d in queue if queue_slug(d) == a.slug]
    if not queue:
        print("publish_blog: queue is empty - nothing to publish (%s)" % today)
        return 0
    dup = published_today(root, today)
    if dup and not a.force:
        print("publish_blog: %s was already published today (%s) - skipping" % (dup, today))
        return 0
    d = queue[0]
    try:
        slug = queue_slug(d)
        validate(d, slug, root)
    except blog.BlogError as ex:
        print("publish_blog: %s is not publishable: %s" % (d.name, ex), file=sys.stderr)
        return 1
    if a.dry_run:
        print("publish_blog: DRY RUN - would publish %s (%s) at %s" % (d.name, slug, when.isoformat()))
        return 0

    git = not a.no_git
    if git:
        if subprocess.run(["git", "status", "--porcelain"], cwd=str(root), capture_output=True, text=True).stdout.strip():
            print("publish_blog: working tree is not clean - refusing", file=sys.stderr)
            return 1
        run(["git", "pull", "--ff-only", "--quiet"], root)
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, check=True).stdout.strip()
        if not d.is_dir():  # the pull removed it (another run published it first)
            return 0
    dest = root / "content" / "blog" / "posts" / slug
    try:
        shutil.move(str(d), str(dest))
        for lang in blog.LANGS:
            f = dest / (lang + ".md")
            f.write_text(stamp(f.read_text(encoding="utf-8"), when), encoding="utf-8")
        if (root / "scripts" / "build_site.py").is_file():
            run([sys.executable, "scripts/build_site.py"], root)
            run([sys.executable, "scripts/build_site.py", "--check"], root)
            run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], root)
        if git:
            run(["git", "add", "-A"], root)
            stat = subprocess.run(["git", "diff", "--cached", "--name-status"], cwd=str(root), capture_output=True, text=True).stdout
            if re.search(r"^D\s+(?!content/blog/queue/)", stat, flags=re.M):
                raise RuntimeError("unexpected deleted files outside the queue:\n" + stat)
            run(["git", "commit", "-q", "-m", "blog: %s (%s)" % (slug, when.date().isoformat())], root)
            if not a.no_push:
                run(["git", "pull", "--rebase", "--quiet"], root)
                run(["git", "push", "--quiet", "origin", "HEAD:main"], root)
    except Exception as ex:  # noqa: BLE001 - roll back everything, then report
        print("publish_blog: FAILED (%s) - rolling back" % ex, file=sys.stderr)
        if git:
            run(["git", "reset", "--hard", "-q", base], root, check=False)
            run(["git", "clean", "-fdq"], root, check=False)
        elif dest.exists() and not d.exists():
            shutil.move(str(dest), str(d))
        return 1
    print("publish_blog: published %s at %s%s" % (slug, when.isoformat(), "" if git and not a.no_push else " (not pushed)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
