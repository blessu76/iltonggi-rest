import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import blog  # noqa: E402
import build_site as bs  # noqa: E402
import publish_blog as pb  # noqa: E402


def write_post(base, folder, slug, published=None, bad=None):
    d = Path(base) / folder
    d.mkdir(parents=True, exist_ok=True)
    for l in blog.LANGS:
        tr = "" if l in blog.ORIGINALS else "translation_of: en\n"
        pub = "published: %s\n" % published if published else ""
        body = "Hello **world** and [home](/).\n\n## Part\n\n- a\n- b\n"
        if bad and l == "de":
            body += "\n" + bad + "\n"
        (d / (l + ".md")).write_text(
            "---\ntitle: T %s\ndescription: D %s\ndate: 2026-10-29\nslug: %s\nlang: %s\n%s%s---\n\n%s" % (l, l, slug, l, tr, pub, body),
            encoding="utf-8")
    return d


class Blog(unittest.TestCase):
    def test_committed_content_ok(self):
        self.assertEqual(blog.main(), 0)

    def test_ui_complete(self):
        ui = blog.ui_all()
        self.assertEqual(sorted(ui), sorted(blog.LANGS))
        for l in blog.LANGS:
            self.assertEqual(sorted(ui[l]), sorted(ui["en"]), l)
            self.assertTrue(all(ui[l].values()), l)

    def test_markdown_subset(self):
        h = blog.render_body("## H\n\ntext <script> **b** *i*\n\n- x\n- y\n\n1. a\n2. b\n\n> q\n\n![alt](/assets/blog/a.webp)")
        self.assertIn("<h2>H</h2>", h)
        self.assertIn("&lt;script&gt;", h)
        self.assertIn("<strong>b</strong>", h)
        self.assertIn("<ol>", h)
        self.assertIn('src="/assets/blog/a.webp"', h)
        for bad in ("[x](https://example.com)", "[x](//evil.com)", "# H1", "![a](https://x/y.png)"):
            with self.assertRaises(blog.BlogError):
                blog.render_body(bad)

    def test_warnings(self):
        m = {"title": "x" * 70, "description": "y" * 170}
        w = blog.warnings(m, "short body", "en")
        self.assertEqual(len(w), 3)
        self.assertEqual(blog.warnings({"title": "t", "description": "d"}, "word " * 400, "en"), [])

    def test_indexnow_today(self):
        import indexnow
        tmp = Path(tempfile.mkdtemp())
        try:
            (tmp / "sitemap.xml").write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://a/x/</loc><lastmod>2026-10-30</lastmod></url><url><loc>https://a/y/</loc><lastmod>2026-10-29</lastmod></url><url><loc>https://a/</loc></url></urlset>')
            self.assertEqual(indexnow.sitemap_urls_modified(tmp / "sitemap.xml", "2026-10-30"), ["https://a/x/"])
        finally:
            shutil.rmtree(tmp)

    def test_lint(self):
        for bad in ("`code`", "see https://x.com", "/Users/a/b", "run build_site.py", "key sk-abcdefghijklmnop", "a@b.com", "$4.99", "9,900원", "foundry-f018"):
            self.assertTrue(blog.lint(bad), bad)
        self.assertFalse(blog.lint("A calm story about a mountain pass."))

    def test_publish_flow(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            q = tmp / "content" / "blog" / "queue"
            write_post(q, "002-second", "second")
            write_post(q, "001-first", "first")
            args = ["--root", str(tmp), "--no-git"]
            self.assertEqual(pb.main(args + ["--dry-run", "--at", "2026-10-30T12:00:00+09:00"]), 0)
            self.assertTrue((q / "001-first").exists())
            self.assertEqual(pb.main(args + ["--at", "2026-10-30T12:00:00+09:00"]), 0)
            posts = tmp / "content" / "blog" / "posts"
            self.assertFalse((q / "001-first").exists())
            for l in blog.LANGS:
                m, _ = blog.parse((posts / "first" / (l + ".md")).read_text(encoding="utf-8"))
                self.assertEqual((m["date"], m["published"]), ("2026-10-30", "2026-10-30T12:00:00+09:00"))
            self.assertEqual(len(blog.load_posts(tmp)), 1)
            # same KST day -> skipped; next day -> second
            self.assertEqual(pb.main(args + ["--at", "2026-10-30T15:00:00+09:00"]), 0)
            self.assertTrue((q / "002-second").exists())
            self.assertEqual(pb.main(args + ["--at", "2026-10-31T12:00:00+09:00"]), 0)
            got = blog.load_posts(tmp)
            self.assertEqual([(p["slug"], p["no"]) for p in got], [("second", 2), ("first", 1)])
            self.assertEqual(pb.main(args + ["--at", "2026-11-01T12:00:00+09:00"]), 0)  # empty queue
        finally:
            shutil.rmtree(tmp)

    def test_publish_refuses_bad(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            q = tmp / "content" / "blog" / "queue"
            write_post(q, "001-leaky", "leaky", bad="see /Users/me/x")
            self.assertEqual(pb.main(["--root", str(tmp), "--no-git"]), 1)
            self.assertTrue((q / "001-leaky").exists())
            shutil.rmtree(q / "001-leaky")
            d = write_post(q, "001-short", "short")
            (d / "ja.md").unlink()
            self.assertEqual(pb.main(["--root", str(tmp), "--no-git"]), 1)
        finally:
            shutil.rmtree(tmp)

    def test_build_pages(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for i in range(12):
                write_post(tmp / "content" / "blog" / "posts", "p%02d" % i, "p%02d" % i, published="2026-10-%02dT12:00:00+09:00" % (i + 1))
                for l in blog.LANGS:  # date must match published day
                    f = tmp / "content" / "blog" / "posts" / ("p%02d" % i) / (l + ".md")
                    f.write_text(f.read_text(encoding="utf-8").replace("date: 2026-10-29", "date: 2026-10-%02d" % (i + 1)), encoding="utf-8")
            files, extra = blog.build(bs, bs.load(), tmp)
            self.assertIn("blog/index.html", files)
            self.assertIn("blog/page/2/index.html", files)
            self.assertIn("ko/blog/p11/index.html", files)
            self.assertIn("blog/feed.xml", files)
            page = files["ja/blog/p00/index.html"]
            self.assertEqual(page.count('<link rel="alternate" hreflang="'), 11 + 1)  # 11 langs + x-default
            self.assertIn('"@type": "BlogPosting"', page)
            self.assertIn('"inLanguage": "ja"', page)
            self.assertIn("datePublished\": \"2026-10-01T12:00:00+09:00", page)
            self.assertIn('rel="canonical" href="https://iltonggi.ipe.rest/ja/blog/p00/"', page)
            self.assertIn("No. 1", page)
            self.assertIn("No. 12", files["blog/index.html"])
            self.assertIn('"@id": "https://ipe.rest/#organization"', page)
            self.assertIn('"@type": "BreadcrumbList"', page)
            self.assertIn('"@type": "ImageObject"', page)
            self.assertIn("post-nav", page)
            self.assertIn("post-more", files["ja/blog/p05/index.html"])
            self.assertIn("blog/p11/", files["llms.txt"])
            sm = bs.sitemap(extra)
            self.assertIn("<lastmod>2026-10-01</lastmod>", sm)
            self.assertNotIn("<priority>0.7</priority>", sm.split("/blog/")[1])
            p2 = files["blog/page/2/index.html"]
            self.assertIn("No. 2 ", p2)
            self.assertNotIn("No. 12 ", p2)
            self.assertIn('rel="prev"', p2)
        finally:
            bs.PATH.clear()
            bs.PATH.update({"home": "/", "privacy": "/privacy/", "terms": "/terms/", "support": "/support/", "releases": "/releases/"})
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
