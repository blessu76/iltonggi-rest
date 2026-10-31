"""Root language handoff: ?lang=xx > saved choice > browser language > English.

The inline script of the built root page is run in node with a fake location/localStorage/navigator (skipped if node is missing);
the pure resolver (scripts/lang_resolve.js) is exercised the same way."""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_site as bs  # noqa: E402

NODE = shutil.which("node")

HARNESS = r"""
const vm = require('vm');
const {code, search, hash, stored, languages, throwStorage} = JSON.parse(process.env.LANG_CASE);
const out = {replaced: null, saved: null, history: null};
const sandbox = {
  location: {search, hash, pathname: '/', replace: (u) => { out.replaced = u; }},
  localStorage: {
    getItem: (k) => { if (throwStorage) throw new Error('blocked'); return stored; },
    setItem: (k, v) => { if (throwStorage) throw new Error('blocked'); out.saved = [k, v]; },
  },
  navigator: {languages, language: languages && languages[0]},
  history: {replaceState: (a, b, u) => { out.history = u; }},
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox);
console.log(JSON.stringify(out));
"""


def run_root(search="", hash="", stored=None, languages=("en-US",), throw=False):
    page = bs.build()["index.html"]
    code = re.search(r"<script>(\(function\(\)\{function ltNorm.*?)</script>", page, re.S).group(1)
    arg = json.dumps({"code": code, "search": search, "hash": hash, "stored": stored,
                      "languages": list(languages), "throwStorage": throw})
    r = subprocess.run([NODE, "-e", HARNESS], capture_output=True, text=True, check=True, env={**os.environ, "LANG_CASE": arg})
    return json.loads(r.stdout)


@unittest.skipUnless(NODE, "node not installed")
class RootLang(unittest.TestCase):
    def test_lang_param_goes_to_the_language_and_is_saved(self):
        r = run_root(search="?lang=ko")
        self.assertEqual(r["replaced"], "/ko/")
        self.assertEqual(r["saved"], ["iltonggi-lang", "ko"])

    def test_lang_param_beats_saved_and_browser(self):
        r = run_root(search="?lang=ja", stored="de", languages=["ko-KR"])
        self.assertEqual(r["replaced"], "/ja/")
        self.assertEqual(r["saved"], ["iltonggi-lang", "ja"])

    def test_lang_param_regional_code_is_normalised(self):
        self.assertEqual(run_root(search="?lang=zh-TW")["replaced"], "/zh/")
        self.assertEqual(run_root(search="?lang=KO_kr")["replaced"], "/ko/")

    def test_lang_en_stays_on_root_saves_and_drops_the_query(self):
        r = run_root(search="?lang=en", stored="ko", languages=["ko-KR"])
        self.assertIsNone(r["replaced"])
        self.assertEqual(r["saved"], ["iltonggi-lang", "en"])
        self.assertEqual(r["history"], "/")

    def test_other_query_and_hash_survive(self):
        r = run_root(search="?utm=x&lang=fr&app=1", hash="#shots")
        self.assertEqual(r["replaced"], "/fr/?utm=x&app=1#shots")
        r = run_root(search="?lang=en&app=1", hash="#shots")
        self.assertEqual(r["history"], "/?app=1#shots")

    def test_unsupported_lang_param_is_ignored_and_falls_through(self):
        r = run_root(search="?lang=xx", stored="de")
        self.assertEqual(r["replaced"], "/de/")
        self.assertIsNone(r["saved"])
        r = run_root(search="?lang=xx", languages=["ja-JP"])
        self.assertEqual(r["replaced"], "/ja/")
        r = run_root(search="?lang=xx", languages=["th-TH"])
        self.assertIsNone(r["replaced"])

    def test_saved_choice_beats_browser(self):
        r = run_root(stored="de", languages=["ko-KR"])
        self.assertEqual(r["replaced"], "/de/")
        self.assertIsNone(r["saved"])

    def test_saved_english_beats_browser_korean(self):
        r = run_root(stored="en", languages=["ko-KR"])
        self.assertIsNone(r["replaced"])

    def test_invalid_saved_value_is_ignored(self):
        self.assertEqual(run_root(stored="tlh", languages=["ko"])["replaced"], "/ko/")

    def test_browser_language_in_order_first_supported_wins(self):
        self.assertEqual(run_root(languages=["ko-KR", "en-US"])["replaced"], "/ko/")
        self.assertEqual(run_root(languages=["th", "vi-VN", "ko"])["replaced"], "/vi/")
        self.assertEqual(run_root(languages=["zh-Hant-TW"])["replaced"], "/zh/")
        self.assertEqual(run_root(languages=["zh-CN"])["replaced"], "/zh/")
        self.assertEqual(run_root(languages=["pt-BR"])["replaced"], "/pt/")

    def test_browser_english_or_unsupported_stays_on_english_root(self):
        self.assertIsNone(run_root(languages=["en-GB", "ko"])["replaced"])
        self.assertIsNone(run_root(languages=["th-TH", "ar"])["replaced"])
        self.assertIsNone(run_root(languages=[])["replaced"])

    def test_blocked_storage_does_not_break_the_redirect(self):
        r = run_root(search="?lang=ko", throw=True)
        self.assertEqual(r["replaced"], "/ko/")
        self.assertEqual(run_root(languages=["ja"], throw=True)["replaced"], "/ja/")


class Built(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = bs.build()

    def test_only_the_root_home_redirects(self):
        for rel, text in self.files.items():
            if not rel.endswith(".html"):
                continue
            with self.subTest(rel):
                self.assertEqual("function ltResolve" in text, rel == "index.html")

    def test_root_script_is_in_head_and_hint_ui_is_gone(self):
        page = self.files["index.html"]
        head = page.split("</head>")[0]
        self.assertIn("function ltResolve", head)
        self.assertNotIn("langHint", page)
        self.assertNotIn("iltonggi_hint_off", page)
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertNotIn("lang-hint", css)

    def test_every_page_with_the_language_menu_remembers_the_choice(self):
        for rel, text in self.files.items():
            if rel.endswith(".html"):
                with self.subTest(rel):
                    self.assertEqual(text.count(".foot-langs a[hreflang]"), 1)
                    self.assertIn("localStorage.setItem(\"iltonggi-lang\"", text)

    def test_seo_tags_untouched(self):
        page = self.files["index.html"]
        self.assertIn('<link rel="canonical" href="https://iltonggi.ipe.rest/">', page)
        self.assertEqual(page.count('<link rel="alternate" hreflang="'), 12)


if __name__ == "__main__":
    unittest.main()
