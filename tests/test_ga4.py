"""GA4 coverage, exclusions, and the app disclosures retained with legal redirects."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_site as bs  # noqa: E402

GA_ID = "G-XG4BH800J0"
LANGS = bs.LANGS


class Ga4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = bs.build()
        cls.html = {k: v for k, v in cls.files.items() if k.endswith(".html")}
        cls.excluded = {k for k in cls.html if k == "404.html" or k.startswith("pt/")
                        or Path(k).parent.name in ("privacy", "terms")}
        cls.pages = {k: v for k, v in cls.html.items() if k not in cls.excluded}
        cls.data = bs.DATA

    def test_constant_is_the_ipe_rest_property(self):
        self.assertEqual(bs.GA_MEASUREMENT_ID, GA_ID)

    def test_every_generated_page_has_the_snippet_once(self):
        self.assertGreater(len(self.pages), 60)
        for rel, text in self.pages.items():
            with self.subTest(rel):
                self.assertEqual(text.count(GA_ID), 1)
                self.assertEqual(text.count("googletagmanager.com/gtag/js"), 1)
                self.assertEqual(text.count("window.gtag('config',GA_ID)"), 1)
                self.assertLess(text.index(GA_ID), text.index("</head>"))

    def test_page_types_are_covered(self):
        for rel in ("index.html", "ko/index.html", "support/index.html", "th/support/index.html",
                    "blog/index.html", "blog/page/2/index.html", "journal/index.html"):
            self.assertIn(rel, self.pages)
        self.assertTrue([k for k in self.pages if re.match(r"blog/[^/]+/index\.html$", k) and "page/" not in k])
        self.assertTrue([k for k in self.pages if re.match(r"ja/blog/[^/]+/index\.html$", k)])

    def test_committed_pages_have_the_snippet(self):
        for rel in self.pages:
            with self.subTest(rel):
                self.assertEqual((ROOT / rel).read_text(encoding="utf-8").count(GA_ID), 1)

    def test_404_and_redirects_omit_the_tag(self):
        for rel in self.excluded:
            with self.subTest(rel):
                for text in (self.html[rel], (ROOT / rel).read_text(encoding="utf-8")):
                    self.assertNotIn(GA_ID, text)
                    self.assertNotIn("googletagmanager", text)

    def test_local_and_file_guard_precedes_the_loader(self):
        loader = bs.GA_SNIPPET.index("googletagmanager")
        for guard in ("location.protocol==='file:'", "h==='localhost'", "h==='127.0.0.1'",
                      "h==='0.0.0.0'", "h==='::1'", "h==='[::1]'"):
            self.assertIn(guard, bs.GA_SNIPPET[:loader])

    def test_no_other_tracker_and_none_in_assets(self):
        for rel, text in self.pages.items():
            self.assertNotIn("doubleclick", text, rel)
        self.assertNotIn(GA_ID, (ROOT / "assets" / "site.css").read_text(encoding="utf-8"))

    def test_skipped_in_the_app_web_view(self):
        # the app collects nothing: pages opened inside it (?app=1) must not load Google Analytics
        self.assertIn("if(/[?&]app=1(&|$)/.test(location.search))return;", bs.GA_SNIPPET)
        self.assertLess(bs.GA_SNIPPET.index("location.search"), bs.GA_SNIPPET.index("googletagmanager"))

    def test_legal_routes_link_to_the_central_documents_and_stay_off_sitemap(self):
        for prefix in [""] + LANGS + ["pt"]:
            for doc in ("privacy", "terms"):
                with self.subTest(prefix=prefix, doc=doc):
                    path = (prefix + "/" if prefix else "") + doc + "/"
                    dest = "https://ipe.rest" + ("/ko" if prefix == "ko" else "") + "/legal/" + doc + "/"
                    rel = path + "index.html"
                    text = self.html[rel]
                    self.assertIn(rel, self.excluded)
                    self.assertIn('name="robots" content="noindex,follow"', text)
                    self.assertIn('rel="canonical" href="%s"' % dest, text)
                    self.assertIn('http-equiv="refresh" content="0; url=%s"' % dest, text)
                    self.assertIn('<a href="%s">' % dest, text)
                    self.assertNotIn('rel="alternate"', text)
                    self.assertNotIn(bs.SITE + "/" + path, self.files["sitemap.xml"])

    def test_footer_links_directly_to_central_documents(self):
        for rel, text in self.pages.items():
            with self.subTest(rel):
                footer = text.split("<footer", 1)[1]
                for doc in ("privacy", "terms"):
                    path = "/ko/legal/" if rel.startswith("ko/") else "/legal/"
                    self.assertIn('href="https://ipe.rest%s%s/"' % (path, doc), footer)

    def test_app_weather_disclosures_are_retained_on_support(self):
        for prefix in [""] + LANGS:
            with self.subTest(prefix):
                t = self.data[prefix or "en"]
                support = self.pages[(prefix + "/" if prefix else "") + "support/index.html"]
                self.assertIn('id="app-privacy"', support)
                self.assertIn('id="app-terms"', support)
                for text in (t["privacy"]["sections"][1]["p"] + [t["privacy"]["sections"][3]["p"][1]]
                             + t["terms"]["sections"][2]["p"] + t["terms"]["sections"][3]["p"]):
                    self.assertIn(bs.esc(text), support)

    NICKNAME = {
        "ko": "게임 안에서 정한 닉네임과 기록은 기기에만 저장되며 회사로 전송·수집하지 않습니다.",
        "en": "Any nickname you choose in the game and your game records are stored only on your device and are not sent to or collected by us.",
        "ja": "ゲーム内で設定したニックネームや記録は端末内にのみ保存され、当社に送信・収集されることはありません。",
        "zh-Hant": "你在遊戲中設定的暱稱與遊戲紀錄僅儲存在你的裝置上,不會傳送給我們,我們也不會蒐集。",
        "es": "El apodo que elijas en el juego y tus registros de partida se guardan únicamente en tu dispositivo; no los enviamos ni los recopilamos.",
        "pt-BR": "O apelido que você definir no jogo e os seus registros de partida ficam armazenados apenas no seu dispositivo; nós não os recebemos nem os coletamos.",
        "id": "Nama panggilan yang Anda tetapkan di dalam game dan catatan permainan Anda hanya disimpan di perangkat Anda; kami tidak menerima maupun mengumpulkannya.",
        "vi": "Biệt danh bạn đặt trong trò chơi và các bản ghi của bạn chỉ được lưu trên thiết bị của bạn; chúng tôi không nhận hay thu thập chúng.",
        "fr": "Le pseudo que vous choisissez dans le jeu et vos données de partie sont stockés uniquement sur votre appareil ; nous ne les recevons ni ne les collectons.",
        "de": "Der Spitzname, den Sie im Spiel festlegen, und Ihre Spielstände werden nur auf Ihrem Gerät gespeichert; wir erhalten oder erfassen sie nicht.",
        "th": "ชื่อเล่นที่คุณตั้งในเกมและบันทึกการเล่นจะถูกเก็บไว้ในอุปกรณ์ของคุณเท่านั้น ไม่ถูกส่งหรือเก็บโดยเรา",
        "tr": "Oyunda seçtiğiniz takma ad ve oyun kayıtlarınız yalnızca cihazınızda saklanır; bize gönderilmez ve tarafımızca toplanmaz.",
    }

    def test_privacy_says_the_nickname_stays_on_the_device(self):
        # 12 languages: section 1 carries the nickname/records-stay-on-device sentence; no Game Center / Play Games wording
        import html
        for lang in LANGS:
            path = "support/index.html" if lang == "en" else "%s/support/index.html" % lang
            main = self.pages[path].split('<details id="app-privacy">')[1].split("</details>")[0]
            with self.subTest(lang):
                self.assertIn(self.NICKNAME[lang], self.data[lang]["privacy"]["sections"][0]["p"][0])
                self.assertIn(html.escape(self.NICKNAME[lang], quote=False), main.replace("&#x27;", "'").replace("&#39;", "'"))
                self.assertNotRegex(main, r"(?i)game ?center|play ?games|play 게임즈")
                self.assertIn("2026", self.data[lang]["privacy_meta_line"])
        self.assertEqual(self.NICKNAME["en"], "Any nickname you choose in the game and your game records are stored only on your device and are not sent to or collected by us.")
        self.assertEqual(self.NICKNAME["ko"], "게임 안에서 정한 닉네임과 기록은 기기에만 저장되며 회사로 전송·수집하지 않습니다.")

    def test_app_statements_unchanged(self):
        en = self.data["en"]["privacy"]["sections"][0]["p"]
        self.assertIn("does not collect or send to any server any personal information", en[0])
        self.assertEqual(en[1], "The App contains no advertising, analytics or tracking SDKs.")

    def test_privacy_effective_date_is_separate_from_terms(self):
        for lang in LANGS:
            t = self.data[lang]
            with self.subTest(lang):
                self.assertNotEqual(t["privacy_meta_line"], t["meta_line"])
        self.assertIn("November 1, 2026", self.data["en"]["privacy_meta_line"])
        self.assertIn("October 28, 2026", self.data["en"]["meta_line"])

    def test_no_stale_no_analytics_claims_about_the_website(self):
        stale = re.compile(r"uses no cookies|no analytics or advertising tags|neither the app nor the website|"
                           r"쿠키를 사용하지 않|분석 도구나 광고 태그를 넣지|앱과 웹사이트 모두 개인정보를 수집하지", re.I)
        for rel in ("support/index.html", "ko/support/index.html"):
            self.assertIsNone(stale.search(self.pages[rel]), rel)

    def test_support_faq_mentions_google_analytics(self):
        for lang in LANGS:
            with self.subTest(lang):
                self.assertIn("Google Analytics", self.data[lang]["support"]["faq"][2][1])


if __name__ == "__main__":
    unittest.main()
