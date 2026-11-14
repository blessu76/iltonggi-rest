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
PREFIXED = set(bs.LANGS) | {bs.LEGACY_PT}  # language folders + the legacy /pt/ redirect stubs

HARNESS = r"""
const vm = require('vm');
const {code, search, hash, stored, legacy, languages, throwStorage, pathname, ua} = JSON.parse(process.env.LANG_CASE);
const out = {replaced: null, saved: null, history: null};
const sandbox = {
  location: {search, hash, pathname, replace: (u) => { out.replaced = u; }},
  localStorage: {
    getItem: (k) => { if (throwStorage) throw new Error('blocked'); return k === 'ipe_lang' ? stored : legacy; },
    setItem: (k, v) => { if (throwStorage) throw new Error('blocked'); out.saved = out.saved || {}; out.saved[k] = v; },
  },
  navigator: {languages, language: languages && languages[0], userAgent: ua},
  history: {replaceState: (a, b, u) => { out.history = u; }},
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox);
console.log(JSON.stringify(out));
"""


def page_code(rel):
    page = bs.build()[rel]
    return re.search(r"<script>(\(function\(\)\{function ltNorm.*?)</script>", page, re.S).group(1)


def both(lang):
    return {"ipe_lang": lang, "iltonggi-lang": lang}


def run_root(search="", hash="", stored=None, languages=("en-US",), throw=False, rel="index.html", pathname="/", code=None, ua="", legacy=None):
    code = code or page_code(rel)
    arg = json.dumps({"code": code, "search": search, "hash": hash, "stored": stored, "legacy": legacy, "pathname": pathname,
                      "languages": list(languages), "throwStorage": throw, "ua": ua})
    r = subprocess.run([NODE, "-e", HARNESS], capture_output=True, text=True, check=True, env={**os.environ, "LANG_CASE": arg})
    return json.loads(r.stdout)


@unittest.skipUnless(NODE, "node not installed")
class RootLang(unittest.TestCase):
    def test_lang_param_goes_to_the_language_and_is_saved(self):
        r = run_root(search="?lang=ko")
        self.assertEqual(r["replaced"], "/ko/")
        self.assertEqual(r["saved"], both("ko"))

    def test_lang_param_beats_saved_and_browser(self):
        r = run_root(search="?lang=ja", stored="de", languages=["ko-KR"])
        self.assertEqual(r["replaced"], "/ja/")
        self.assertEqual(r["saved"], both("ja"))

    def test_lang_param_regional_code_is_normalised(self):
        self.assertEqual(run_root(search="?lang=zh-TW")["replaced"], "/zh-Hant/")
        self.assertEqual(run_root(search="?lang=KO_kr")["replaced"], "/ko/")

    def test_legacy_indonesian_code_in_means_id(self):
        r = run_root(search="?lang=in")
        self.assertEqual(r["replaced"], "/id/")
        self.assertEqual(r["saved"], both("id"))
        self.assertEqual(run_root(search="?lang=in-ID")["replaced"], "/id/")
        self.assertEqual(run_root(languages=["in-ID", "en"])["replaced"], "/id/")
        self.assertEqual(run_root(stored="in")["replaced"], "/id/")
        self.assertIsNone(run_root(search="?lang=inx")["replaced"])  # only the exact legacy code, not a prefix

    def test_lang_en_stays_on_root_saves_and_drops_the_query(self):
        r = run_root(search="?lang=en", stored="ko", languages=["ko-KR"])
        self.assertIsNone(r["replaced"])
        self.assertEqual(r["saved"], both("en"))
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
        r = run_root(search="?lang=xx", languages=["he-IL"])
        self.assertIsNone(r["replaced"])

    def test_saved_choice_beats_browser(self):
        r = run_root(stored="de", languages=["ko-KR"])
        self.assertEqual(r["replaced"], "/de/")
        self.assertIsNone(r["saved"])

    def test_ipe_lang_beats_the_older_key(self):
        r = run_root(stored="ko", legacy="de", languages=["ja-JP"])
        self.assertEqual(r["replaced"], "/ko/")
        self.assertIsNone(run_root(stored="en", legacy="de", languages=["ja-JP"])["replaced"])

    def test_older_key_is_used_when_ipe_lang_is_missing(self):
        self.assertEqual(run_root(legacy="de", languages=["ko-KR"])["replaced"], "/de/")

    def test_saved_english_beats_browser_korean(self):
        r = run_root(stored="en", languages=["ko-KR"])
        self.assertIsNone(r["replaced"])

    def test_invalid_saved_value_is_ignored(self):
        self.assertEqual(run_root(stored="tlh", languages=["ko"])["replaced"], "/ko/")

    def test_browser_language_in_order_first_supported_wins(self):
        self.assertEqual(run_root(languages=["ko-KR", "en-US"])["replaced"], "/ko/")
        self.assertEqual(run_root(languages=["th", "vi-VN", "ko"])["replaced"], "/th/")
        self.assertEqual(run_root(languages=["zh-Hant-TW"])["replaced"], "/zh-Hant/")
        self.assertEqual(run_root(languages=["zh-HK"])["replaced"], "/zh-Hant/")
        self.assertEqual(run_root(languages=["pt-BR"])["replaced"], "/pt-BR/")
        self.assertEqual(run_root(languages=["pt-PT"])["replaced"], "/pt-BR/")
        self.assertEqual(run_root(languages=["tr-TR"])["replaced"], "/tr/")
        # simplified Chinese and the retired languages (ar, hi, ru) are not on the site: they stay on English
        self.assertIsNone(run_root(languages=["zh-CN"])["replaced"])
        self.assertIsNone(run_root(languages=["zh"])["replaced"])  # bare zh is not Traditional (kit parity)
        self.assertIsNone(run_root(languages=["ar-EG", "en"])["replaced"])
        self.assertEqual(run_root(languages=["hi-IN", "th"])["replaced"], "/th/")
        self.assertEqual(run_root(stored="ar", languages=["ko"])["replaced"], "/ko/")
        self.assertIsNone(run_root(search="?lang=hi")["replaced"])
        self.assertIsNone(run_root(search="?lang=ru")["replaced"])

    def test_browser_english_or_unsupported_stays_on_english_root(self):
        self.assertIsNone(run_root(languages=["en-GB", "ko"])["replaced"])
        self.assertIsNone(run_root(languages=["he-IL", "ar"])["replaced"])
        self.assertIsNone(run_root(languages=[])["replaced"])

    def test_blocked_storage_does_not_break_the_redirect(self):
        r = run_root(search="?lang=ko", throw=True)
        self.assertEqual(r["replaced"], "/ko/")
        self.assertEqual(run_root(languages=["ja"], throw=True)["replaced"], "/ja/")

    def test_crawlers_are_never_redirected(self):
        for ua in ("Googlebot/2.1 (+http://www.google.com/bot.html)", "Mozilla/5.0 (compatible; bingbot/2.0)",
                   "Mozilla/5.0 (compatible; YandexBot/3.0)", "Slurp", "Lighthouse", "Mozilla/5.0 Crawler/1.0"):
            with self.subTest(ua):
                r = run_root(search="?lang=ko", stored="de", languages=["ko-KR"], ua=ua)
                self.assertIsNone(r["replaced"])
                self.assertIsNone(r["saved"])
        self.assertEqual(run_root(languages=["ko-KR"], ua="Mozilla/5.0 (iPhone; CPU iPhone OS 18_0)")["replaced"], "/ko/")


class Built(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = bs.build()

    def test_only_pages_without_a_language_prefix_carry_the_script(self):
        """every prefix-less page except 404.html has it; no /xx/ page (en included) and not the 404 page"""
        for rel, text in self.files.items():
            if not rel.endswith(".html"):
                continue
            with self.subTest(rel):
                prefixed = rel.split("/")[0] in PREFIXED
                self.assertEqual("function ltResolve" in text, not prefixed and rel != "404.html")

    def test_root_script_is_in_head_and_hint_ui_is_gone(self):
        page = self.files["index.html"]
        head = page.split("</head>")[0]
        self.assertIn("function ltResolve", head)
        self.assertNotIn("langHint", page)
        self.assertNotIn("iltonggi_hint_off", page)
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertNotIn("lang-hint", css)

    def test_every_page_has_one_header_language_menu_that_remembers_the_choice(self):
        for rel, text in self.files.items():
            if rel.endswith(".html") and rel.split("/")[0] != bs.LEGACY_PT:  # /pt/ stubs only redirect
                with self.subTest(rel):
                    self.assertEqual(text.count('<select class="lang-select"'), 1)
                    self.assertLess(text.index('<select class="lang-select"'), text.index("</header>"))
                    self.assertIn('["ipe_lang", "iltonggi-lang"].forEach', text)

    def test_header_menu_lists_twelve_languages_and_selects_the_page_language(self):
        for rel, text in self.files.items():
            top = rel.split("/")[0]
            if not rel.endswith(".html") or top == bs.LEGACY_PT:
                continue
            page_lang = top if top in bs.LANGS else "en"
            with self.subTest(rel):
                sel = re.search(r'<select class="lang-select".*?</select>', text, re.S).group(0)
                opts = re.findall(r'<option value="([^"]*)" lang="([^"]+)"( selected)?>', sel)
                self.assertEqual([o[1] for o in opts], bs.LANGS)
                self.assertEqual([o[1] for o in opts if o[2]], [page_lang])

    def test_header_nav_has_no_terms_and_footer_keeps_legal_links(self):
        for rel, text in self.files.items():
            if not rel.endswith(".html") or rel.split("/")[0] == bs.LEGACY_PT:
                continue
            with self.subTest(rel):
                nav = re.search(r'<nav class="nav".*?</nav>', text, re.S).group(0)
                self.assertNotIn("/terms/", nav)
                foot = re.search(r'<nav class="footer-links".*?</nav>', text, re.S).group(0)
                self.assertIn("/terms/", foot)
                self.assertIn("/privacy/", foot)
                self.assertNotIn("foot-langs", text)

    def test_404_menu_only_goes_home(self):
        self.assertIn("data-home", re.search(r'<select class="lang-select"[^>]*>', self.files["404.html"]).group(0))

    def test_seo_tags_untouched(self):
        page = self.files["index.html"]
        self.assertIn('<link rel="canonical" href="https://iltonggi.ipe.rest/">', page)
        self.assertEqual(page.count('<link rel="alternate" hreflang="'), 13)


def prefixless_pages():
    return sorted(r for r in bs.build() if r.endswith(".html") and r != "404.html" and r.split("/")[0] not in PREFIXED)


def url_of(rel):
    return "/" if rel == "index.html" else "/" + rel[: -len("index.html")]


class EveryPage(unittest.TestCase):
    """the rule is on /privacy/ /terms/ /support/ /blog/... too, not only on /"""

    @classmethod
    def setUpClass(cls):
        cls.files = bs.build()
        cls.pages = prefixless_pages()

    def test_the_pages_are_the_expected_ones(self):
        urls = [url_of(r) for r in self.pages]
        for want in ("/", "/privacy/", "/terms/", "/support/", "/blog/"):
            self.assertIn(want, urls)
        self.assertTrue(any(u.startswith("/blog/") and u != "/blog/" for u in urls), "a blog post")

    def test_each_page_lists_exactly_the_languages_that_have_it(self):
        for rel in self.pages:
            with self.subTest(rel):
                m = re.search(r"var SUP=(\[[^\]]*\]),AV=(\[[^\]]*\])", self.files[rel])
                self.assertEqual(json.loads(m.group(1)), bs.LANGS)
                have = [l for l in bs.LANGS if l != "en" and "%s/%s" % (l, rel) in self.files]
                self.assertEqual(json.loads(m.group(2)), have)
                self.assertTrue(have)

    def test_script_is_in_head_once_with_the_saved_key(self):
        for rel in self.pages:
            with self.subTest(rel):
                text = self.files[rel]
                self.assertEqual(text.count("function ltResolve"), 1)
                self.assertIn("function ltResolve", text.split("</head>")[0])
                self.assertIn('KEYS=["ipe_lang", "iltonggi-lang"]', text)

    def test_language_pages_and_404_do_not_have_it(self):
        for rel, text in self.files.items():
            if rel.endswith(".html") and (rel.split("/")[0] in PREFIXED or rel == "404.html"):
                with self.subTest(rel):
                    self.assertNotIn("ltResolve", text)

    def test_no_marker_left_over(self):
        for rel, text in self.files.items():
            self.assertNotIn(bs.LANG_MARK.strip(), text, rel)

    def test_a_language_without_the_page_is_left_alone(self):
        """AV is built per page: drop one language's copy of a page from the build and only that page loses the language"""
        raw = bs.build()
        # swap the marker on a small copy of the build in which /ja/support/ is missing
        marked = {"support/index.html": "<head>" + bs.LANG_MARK + "</head>", "privacy/index.html": "<head>" + bs.LANG_MARK + "</head>"}
        marked.update({r: "x" for r in raw if r.split("/")[0] in bs.LANGS and r.endswith("index.html") and r != "ja/support/index.html"})
        out = bs.add_lang_script(marked)
        self.assertNotIn('"ja"', re.search(r"AV=(\[[^\]]*\])", out["support/index.html"]).group(1))
        self.assertIn('"ja"', re.search(r"AV=(\[[^\]]*\])", out["privacy/index.html"]).group(1))


@unittest.skipUnless(NODE, "node not installed")


class TwelveLanguages(unittest.TestCase):
    """the site has exactly 12 languages in a fixed order (ipe_web_kit languages): symmetric hreflang, a folder per tag"""

    ORDER = ["en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr"]

    @classmethod
    def setUpClass(cls):
        cls.files = bs.build()

    def test_twelve_languages_in_order(self):
        self.assertEqual(bs.LANGS, self.ORDER)

    def test_retired_languages_do_not_exist(self):
        for l in ("ar", "hi", "ru", "zh"):
            self.assertNotIn(l, bs.LANGS)
            self.assertFalse([r for r in self.files if r.startswith(l + "/")], l)
            self.assertFalse((ROOT / "content" / (l + ".json")).exists(), l)

    def test_no_release_notes_anywhere(self):
        for rel, text in self.files.items():
            self.assertNotIn("releases", rel)
            if rel.endswith((".html", ".xml", ".txt")):
                with self.subTest(rel):
                    self.assertNotIn("/releases/", text)
                    self.assertNotIn("/release-notes/", text)
        self.assertFalse((ROOT / "content" / "releases.json").exists())

    def test_pages_exist_for_every_page(self):
        for rel in prefixless_pages():
            for l in bs.LANGS:
                if l != "en":
                    with self.subTest(rel=rel, lang=l):
                        self.assertIn("%s/%s" % (l, rel), self.files)

    def test_direction_and_lang_on_html(self):
        for rel, text in self.files.items():
            top = rel.split("/")[0]
            if rel.endswith(".html") and top in bs.LANGS:
                with self.subTest(rel):
                    self.assertIn('<html lang="%s" dir="ltr">' % top, text)

    def test_hreflang_is_symmetric(self):
        for rel in prefixless_pages():
            sibs = {}
            for l in bs.LANGS:
                key = rel if l == "en" else "%s/%s" % (l, rel)
                if key in self.files:
                    sibs[l] = set(re.findall(r'<link rel="alternate" hreflang="([^"]+)"', self.files[key]))
            with self.subTest(rel):
                self.assertEqual(len(set(map(frozenset, sibs.values()))), 1)
                self.assertEqual(next(iter(sibs.values())), set(bs.LANGS) | {"x-default"})
                self.assertEqual(set(sibs), set(bs.LANGS))

    def test_old_pt_addresses_redirect_to_pt_br(self):
        stub = self.files["pt/privacy/index.html"]
        self.assertIn('url=https://iltonggi.ipe.rest/pt-BR/privacy/', stub)
        self.assertIn("noindex", stub)
        self.assertNotIn("ltResolve", stub)
        self.assertNotIn("/pt/", self.files["sitemap.xml"])

    def test_css_has_no_rtl_or_retired_language_rules(self):
        css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        self.assertNotIn("html:lang(ar)", css)
        self.assertNotIn("html:lang(hi)", css)

    def test_content_files_match_english_keys(self):
        en = json.loads((ROOT / "content" / "en.json").read_text(encoding="utf-8"))
        for tag in bs.LANGS:
            d = json.loads((ROOT / "content" / (tag + ".json")).read_text(encoding="utf-8"))
            with self.subTest(tag):
                self.assertEqual(set(d), set(en))
                self.assertEqual(set(d["privacy"]), set(en["privacy"]))
                self.assertEqual(len(d["privacy"]["sections"]), len(en["privacy"]["sections"]))
                self.assertIn("{gaoptout}", "".join(d["privacy"]["sections"][2]["p"]))


class InnerPageBehaviour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = bs.build()
        cls.post = next(r for r in cls.files if r.startswith("blog/") and r.endswith("/index.html") and r != "blog/index.html")
        cls.post_url = url_of(cls.post)

    def code(self, rel):
        return re.search(r"<script>(\(function\(\)\{function ltNorm.*?)</script>", self.files[rel], re.S).group(1)

    def test_inner_pages_move_to_the_same_page_in_the_language(self):
        for rel in ("privacy/index.html", "terms/index.html", "support/index.html", "blog/index.html", self.post):
            with self.subTest(rel):
                r = run_root(languages=["ko-KR", "en"], rel=rel, pathname=url_of(rel), code=self.code(rel))
                self.assertEqual(r["replaced"], "/ko" + url_of(rel))

    def test_query_and_hash_survive_and_lang_param_is_dropped(self):
        r = run_root(search="?utm=x&lang=fr&app=1", hash="#faq", rel="support/index.html", pathname="/support/", code=self.code("support/index.html"))
        self.assertEqual(r["replaced"], "/fr/support/?utm=x&app=1#faq")
        self.assertEqual(r["saved"], both("fr"))
        r = run_root(search="?utm=x", hash="#faq", stored="de", rel="support/index.html", pathname="/support/", code=self.code("support/index.html"))
        self.assertEqual(r["replaced"], "/de/support/?utm=x#faq")

    def test_english_unsupported_and_saved_english_stay(self):
        code = self.code("terms/index.html")
        for kw in (dict(languages=["en-US"]), dict(languages=["he", "ar"]), dict(stored="en", languages=["ko"]), dict(languages=[])):
            with self.subTest(kw):
                self.assertIsNone(run_root(rel="terms/index.html", pathname="/terms/", code=code, **kw)["replaced"])
        r = run_root(search="?lang=en&app=1", hash="#x", rel="terms/index.html", pathname="/terms/", code=code)
        self.assertIsNone(r["replaced"])
        self.assertEqual(r["history"], "/terms/?app=1#x")

    def test_a_language_without_the_counterpart_stays(self):
        code = self.code("blog/index.html").replace('AV=["ko", ', "AV=[", 1)  # this page has no /ko/ copy
        self.assertNotIn('"ko"', re.search(r"AV=(\[[^\]]*\])", code).group(1))
        r = run_root(languages=["ko-KR", "ja"], rel="blog/index.html", pathname="/blog/", code=code)
        self.assertIsNone(r["replaced"])  # the first supported language decides: ko, which this page lacks; no fallback to ja
        r = run_root(search="?lang=ko", rel="blog/index.html", pathname="/blog/", code=code)
        self.assertIsNone(r["replaced"])
        self.assertEqual(r["saved"], both("ko"))
        self.assertEqual(r["history"], "/blog/")
        self.assertEqual(run_root(languages=["ja"], rel="blog/index.html", pathname="/blog/", code=code)["replaced"], "/ja/blog/")

    def test_a_language_path_never_moves_again(self):
        code = self.code("privacy/index.html")
        for pathname in ("/ko/privacy/", "/en/privacy/", "/ja/"):
            with self.subTest(pathname):
                self.assertIsNone(run_root(languages=["de"], stored="fr", search="?lang=ja", rel="privacy/index.html", pathname=pathname, code=code)["replaced"])

    def test_blocked_storage_still_moves(self):
        r = run_root(search="?lang=ko", throw=True, rel="privacy/index.html", pathname="/privacy/", code=self.code("privacy/index.html"))
        self.assertEqual(r["replaced"], "/ko/privacy/")


if __name__ == "__main__":
    unittest.main()
