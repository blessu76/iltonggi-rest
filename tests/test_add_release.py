import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import add_release as ar  # noqa: E402

NOTES = "at: 2026-10-29 10:13\n\n## ko\n- 하나\n- 둘\n\n## en\n- one\n- two\n"


class AddRelease(unittest.TestCase):
    def test_norm_build(self):
        self.assertEqual(ar.norm_build("25"), "1.0.0+25")
        self.assertEqual(ar.norm_build("1.0.0+26"), "1.0.0+26")
        with self.assertRaises(ValueError):
            ar.norm_build("abc")

    def test_parse_notes(self):
        self.assertEqual(ar.parse_notes(NOTES), ("2026-10-29 10:13", ["하나", "둘"], ["one", "two"]))

    def test_parse_notes_default_at_and_errors(self):
        at, _, _ = ar.parse_notes("## ko\n- a\n## en\n- b\n")
        self.assertRegex(at, r"^\d{4}-\d\d-\d\d \d\d:\d\d$")
        for bad in ("## ko\n- a\n", "## fr\n- a\n", "## ko\n- a\n## en\nstray\n"):
            with self.assertRaises(ValueError):
                ar.parse_notes(bad)

    def test_upsert_adds_sorted_then_replaces(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "releases.json"
            p.write_text(json.dumps({"entries": [
                {"build": "1.0.0+2", "at": "x", "ko": ["a"], "en": ["a"]},
                {"build": "1.0.0+24", "at": "x", "state": "uploading", "ko": ["a"], "en": ["a"]}]}), encoding="utf-8")
            self.assertFalse(ar.upsert(p, "1.0.0+25", "t", ["k"], ["e"]))
            self.assertEqual([e["build"] for e in json.loads(p.read_text())["entries"]],
                             ["1.0.0+25", "1.0.0+24", "1.0.0+2"])
            self.assertTrue(ar.upsert(p, "1.0.0+24", "t2", ["k"], ["e"]))
            es = json.loads(p.read_text())["entries"]
            self.assertEqual(len(es), 3)
            self.assertNotIn("state", es[1])
            self.assertEqual(es[1]["at"], "t2")

    def test_replace_shots(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as d:
            shots, assets = Path(d) / "s", Path(d) / "a"
            shots.mkdir(); assets.mkdir()
            Image.new("RGB", (1334, 750), (200, 30, 30)).save(shots / "map.png")
            Image.new("RGB", (2000, 400), (30, 30, 200)).save(shots / "march.jpg")
            self.assertEqual(ar.replace_shots(shots, assets), ["shot-map", "shot-march"])
            for n in ("shot-map", "shot-march"):
                self.assertEqual(Image.open(assets / (n + ".webp")).size, (1200, 554))
                self.assertEqual(Image.open(assets / (n + "-600.webp")).size, (600, 277))
            self.assertEqual(ar.replace_shots(Path(d) / "empty", assets), [])


if __name__ == "__main__":
    unittest.main()
