"""GA4: one snippet per generated page (every page type, incl. blog), and the privacy / FAQ text that must match it."""
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
        # the legacy /pt/ stubs only redirect to /pt-BR/ (no GA, no content)
        cls.pages = {k: v for k, v in cls.files.items() if k.endswith(".html") and k.split("/")[0] != bs.LEGACY_PT}
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
        for rel in ("index.html", "ko/index.html", "privacy/index.html", "terms/index.html", "support/index.html",
                    "th/privacy/index.html", "de/privacy/index.html", "404.html", "blog/index.html"):
            self.assertIn(rel, self.pages)
        self.assertTrue([k for k in self.pages if re.match(r"blog/[^/]+/index\.html$", k) and "page/" not in k])
        self.assertTrue([k for k in self.pages if re.match(r"ja/blog/[^/]+/index\.html$", k)])

    def test_committed_pages_have_the_snippet(self):
        for rel in self.pages:
            with self.subTest(rel):
                self.assertEqual((ROOT / rel).read_text(encoding="utf-8").count(GA_ID), 1)

    def test_no_other_tracker_and_none_in_assets(self):
        for rel, text in self.pages.items():
            self.assertNotIn("doubleclick", text, rel)
        self.assertNotIn(GA_ID, (ROOT / "assets" / "site.css").read_text(encoding="utf-8"))

    def test_skipped_in_the_app_web_view(self):
        # the app collects nothing: pages opened inside it (?app=1) must not load Google Analytics
        self.assertIn("if(/[?&]app=1(&|$)/.test(location.search))return;", bs.GA_SNIPPET)
        self.assertLess(bs.GA_SNIPPET.index("location.search"), bs.GA_SNIPPET.index("googletagmanager"))

    def test_privacy_has_a_web_only_ga_section_and_keeps_the_app_statement(self):
        for lang in LANGS:
            path = "privacy/index.html" if lang == "en" else "%s/privacy/index.html" % lang
            text = self.pages[path]
            main = text[text.index("<main"):text.index("</main>")]
            with self.subTest(lang):
                self.assertIn("Google Analytics", main)
                self.assertIn("_ga", main)
                self.assertIn(bs.GA_OPTOUT, main)
                self.assertEqual(len(re.findall(r"<h2[ >]", main)), 9)
                self.assertIn("iltonggi.ipe.rest", main.split("<h2>")[3])  # section 3 = website only
                self.assertIn("2026", main.split('class="meta"')[1][:120])
            sec1 = self.data[lang]["privacy"]["sections"][0]["p"]
            self.assertEqual(len(sec1), 2)  # app collects nothing: both original app sentences stay

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
            path = "privacy/index.html" if lang == "en" else "%s/privacy/index.html" % lang
            main = self.pages[path]
            main = main[main.index("<main"):main.index("</main>")]
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
        for rel in ("privacy/index.html", "support/index.html", "ko/privacy/index.html", "ko/support/index.html"):
            self.assertIsNone(stale.search(self.pages[rel]), rel)

    def test_support_faq_mentions_google_analytics(self):
        for lang in LANGS:
            with self.subTest(lang):
                self.assertIn("Google Analytics", self.data[lang]["support"]["faq"][2][1])


if __name__ == "__main__":
    unittest.main()
