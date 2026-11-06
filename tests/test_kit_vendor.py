"""Web kit (vendor/ipe_web_kit) — the copy is untouched, pinned to a tag, and wired into indexnow + the blog's local-time script."""
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import blog  # noqa: E402  (puts vendor/ on sys.path)
import indexnow  # noqa: E402
from ipe_web_kit import __version__ as KIT_VERSION, localtime  # noqa: E402

LOCALTIME_SHA256 = "57326449ddf5050eabadd1394d69eb2b0f61c88f084ec83ee4aff6fcad0f74b8"  # ipe-localtime v2 (ipe-rest c466827)


class KitVendor(unittest.TestCase):
    def test_vendor_copy_is_unmodified(self):
        r = subprocess.run([sys.executable, str(ROOT / "vendor" / "ipe_web_kit" / "vendor.py"), "verify", str(ROOT)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_pinned_tag(self):
        stamp = (ROOT / "vendor" / "ipe_web_kit" / "KIT_VERSION").read_text(encoding="utf-8").split()
        self.assertEqual(stamp[0], "v" + KIT_VERSION)
        self.assertRegex(stamp[1], r"^[0-9a-f]{40}$")

    def test_imports_come_from_vendor(self):
        vendor = str((ROOT / "vendor").resolve())
        self.assertTrue(str(Path(localtime.__file__).resolve()).startswith(vendor))
        self.assertEqual(indexnow.find_key.__module__, "ipe_web_kit.indexnow")

    def test_localtime_is_the_company_module(self):
        raw = (ROOT / "vendor" / "ipe_web_kit" / "assets" / "ipe-localtime.js").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), LOCALTIME_SHA256)
        self.assertEqual(blog.localtime_script(), "<script>" + raw.decode("utf-8").strip() + "</script>\n")

    def test_deploy_does_not_publish_vendor(self):
        deploy = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
        self.assertIn("--exclude='/vendor'", deploy)


if __name__ == "__main__":
    unittest.main()
