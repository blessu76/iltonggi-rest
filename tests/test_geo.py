"""GEO checks for the journal: JSON-LD on every generated page, sitemap/feeds XML, llms.txt, robots.txt, FAQ + structure lint."""
import json
import re
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import blog  # noqa: E402
import build_site as bs  # noqa: E402

LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "a": "http://www.w3.org/2005/Atom"}
FAQ_BODY = "Intro line.\n\n## FAQ\n\n### What is it?\n\nA **game**. See [home](/).\n\n### Is it free?\n\nYes.\n\n## Other\n\ntext\n"


def ld_blocks(html_text):
    return [json.loads(m) for m in LD.findall(html_text)]


class JsonLd(unittest.TestCase):
    def test_every_generated_page_parses(self):
        files = bs.build()
        n = 0
        for path, text in files.items():
            if path.endswith(".html"):
                for m in LD.findall(text):
                    json.loads(m)  # raises on a parse error
                    n += 1
        self.assertGreater(n, 100)

    def test_committed_pages_parse(self):
        """The pages on disk are what goes live."""
        for f in list(ROOT.glob("blog/**/index.html")) + list(ROOT.glob("*/blog/**/index.html")):
            for m in LD.findall(f.read_text(encoding="utf-8")):
                json.loads(m)

    def test_post_has_geo_fields(self):
        posts = blog.load_posts(ROOT)
        self.assertTrue(posts)
        for p in posts:
            for lang in ["en"] + bs.LANGS:
                path = "blog/%s/index.html" % p["slug"] if lang == "en" else "%s/blog/%s/index.html" % (lang, p["slug"])
                h = (ROOT / path).read_text(encoding="utf-8")
                post = [b for b in ld_blocks(h) if b["@type"] == "BlogPosting"]
                self.assertEqual(len(post), 1, path)
                b = post[0]
                for k in ("headline", "author", "datePublished", "dateModified", "inLanguage", "image", "mainEntityOfPage", "about"):
                    self.assertTrue(b.get(k), "%s: %s" % (path, k))
                self.assertEqual(b["about"]["@type"], "VideoGame")
                self.assertEqual(b["about"]["gamePlatform"], "iOS")
                self.assertIn("og-share.jpg", b["image"][0]["url"])
                self.assertEqual(len(re.findall(r'<link rel="alternate" hreflang="', h)), 13, path)
                self.assertIn('hreflang="x-default"', h, path)
                for tag in ('og:title', 'og:description', 'og:image:alt', 'twitter:card', 'twitter:title', 'twitter:image:alt'):
                    self.assertIn(tag, h, "%s: %s" % (path, tag))
                self.assertIn('rel="canonical"', h)
                self.assertIn('type="application/atom+xml"', h)


class Faq(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual(blog.faq_pairs(FAQ_BODY), [("What is it?", "A **game**. See [home](/)."), ("Is it free?", "Yes.")])
        self.assertEqual(blog.faq_pairs("## Plain\n\n### Not a question\n\ntext"), [])
        self.assertEqual(len(blog.faq_pairs("## 자주 묻는 질문\n\n### 무료인가요?\n\n네.")), 1)
        self.assertEqual(blog.plain("A **game**. See [home](/)."), "A game. See home.")

    def test_post_with_faq_emits_faqpage(self):
        post = {"slug": "x", "no": 1, "published": blog.dt.datetime(2026, 11, 1, 12, tzinfo=blog.KST), "modified": blog.dt.datetime(2026, 11, 1, 12, tzinfo=blog.KST)}
        meta = {"title": "T", "description": "D", "slug": "x", "lang": "en", "date": "2026-11-01"}
        post["files"] = {l: (dict(meta, lang=l), FAQ_BODY) for l in blog.LANGS}
        data = bs.load()
        bs.PATH["blog:x"] = "/blog/x/"
        bs.PATH["blog:p1"] = "/journal/"
        ui = blog.ui_all()["en"]
        h = blog.post_page(bs, data, data["en"], ui, "en", True, "", post, [post])
        faq = [b for b in ld_blocks(h) if b["@type"] == "FAQPage"]
        self.assertEqual(len(faq), 1)
        self.assertEqual(len(faq[0]["mainEntity"]), 2)
        self.assertEqual(faq[0]["mainEntity"][0]["acceptedAnswer"]["text"], "A game. See home.")

    def test_geo_warnings(self):
        w = blog.geo_warnings("## Only\n\ntext", "en")
        self.assertTrue(any("opening paragraph" in x for x in w))
        self.assertTrue(any("`##` sections" in x for x in w))
        self.assertTrue(any("FAQ" in x for x in w))
        good = "A clear two sentence summary that tells the reader what this post is about. It names the game.\n\n## A\n\nx\n\n## B\n\ny\n"
        self.assertEqual([x for x in blog.geo_warnings(good, "en") if "FAQ" not in x], [])
        self.assertEqual(blog.geo_warnings("x", "de"), [])  # translations are not checked


class SiteFiles(unittest.TestCase):
    def test_sitemap_has_every_post_and_lastmod(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        locs = {u.find("s:loc", NS).text: u.find("s:lastmod", NS) for u in root.findall("s:url", NS)}
        self.assertIn(bs.SITE + "/journal/", locs)
        for p in blog.load_posts(ROOT):
            for lang in ["en"] + bs.LANGS:
                u = "%s/blog/%s/" % (bs.SITE, p["slug"]) if lang == "en" else "%s/%s/blog/%s/" % (bs.SITE, lang, p["slug"])
                self.assertIn(u, locs)
                self.assertIsNotNone(locs[u], u)
                self.assertEqual(locs[u].text, p["modified"].date().isoformat())

    def test_feeds_valid_and_list_posts(self):
        slugs = {p["slug"] for p in blog.load_posts(ROOT)}
        rss = ET.parse(ROOT / "blog" / "feed.xml").getroot()
        links = {i.find("link").text for i in rss.iter("item")}
        self.assertTrue(all("%s/blog/%s/" % (bs.SITE, s) in links for s in list(slugs)[:20]) or len(slugs) > 20)
        self.assertIsNotNone(rss.find("channel/lastBuildDate"))
        atom = ET.parse(ROOT / "blog" / "atom.xml").getroot()
        self.assertEqual(len(atom.findall("a:entry", NS)), len(rss.findall("channel/item")))
        self.assertIsNotNone(atom.find("a:updated", NS))

    def test_llms_txt(self):
        t = (ROOT / "llms.txt").read_text(encoding="utf-8")
        for need in ("/journal/", "/blog/feed.xml", "/blog/atom.xml"):
            self.assertIn(bs.SITE + need, t)
        for p in blog.load_posts(ROOT):
            self.assertIn("%s/blog/%s/" % (bs.SITE, p["slug"]), t)

    def test_robots_lets_ai_crawlers_in(self):
        t = (ROOT / "robots.txt").read_text(encoding="utf-8")
        groups = {}
        cur = []
        for line in t.splitlines():
            line = line.split("#")[0].strip()
            if line.lower().startswith("user-agent:"):
                cur.append(line.split(":", 1)[1].strip())
            elif line.lower().startswith(("allow:", "disallow:")) and cur:
                for a in cur:
                    groups.setdefault(a, []).append(line)
            elif not line:
                cur = []
        for bot in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"):
            rules = groups.get(bot) or groups.get("*")
            self.assertIn("Allow: /", rules, bot)
            self.assertNotIn("Disallow: /", rules, bot)
        self.assertIn("Sitemap: %s/sitemap.xml" % bs.SITE, t)


if __name__ == "__main__":
    unittest.main()
