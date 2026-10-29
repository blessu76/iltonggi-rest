#!/usr/bin/env python3
"""Post-deploy smoke test for the blog (SEO guide D2): the newest post, all 11 languages, on the live site. Never fails the deploy.

    python3 scripts/check_blog_live.py            # newest post in sitemap.xml (by lastmod)
    python3 scripts/check_blog_live.py SLUG

Per URL: HTTP 200, canonical == URL, exactly one <h1>, BlogPosting JSON-LD parses with datePublished/dateModified/inLanguage,
11 hreflang + x-default, URL listed in the live sitemap. Retries for a few minutes (Pages may still be publishing). Exit 1 on any miss.
"""
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://iltonggi.ipe.rest"
LANGS = ["en", "ko", "ja", "zh", "es", "pt", "id", "ru", "vi", "fr", "de"]
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def get(url):
    req = urllib.request.Request(url + ("&" if "?" in url else "?") + "_=%d" % time.time(), headers={"User-Agent": "iltonggi-check"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read().decode("utf-8", "replace")


def newest_slug():
    best = None
    for u in ET.parse(ROOT / "sitemap.xml").iter(NS + "url"):
        loc, lm = u.find(NS + "loc").text, u.find(NS + "lastmod")
        m = re.match(re.escape(SITE) + r"/blog/([a-z0-9-]+)/$", loc)
        if m and m.group(1) != "page" and lm is not None and (best is None or lm.text > best[0]):
            best = (lm.text, m.group(1))
    return best[1] if best else None


def check(slug, sitemap_text):
    bad = []
    for l in LANGS:
        url = "%s/%s/blog/%s/" % (SITE, l, slug)
        try:
            st, h = get(url)
        except Exception as ex:  # noqa: BLE001
            bad.append("%s: %s" % (url, ex))
            continue
        if st != 200:
            bad.append("%s: HTTP %d" % (url, st))
            continue
        if '<link rel="canonical" href="%s">' % url not in h:
            bad.append("%s: canonical mismatch" % url)
        if len(re.findall(r"<h1[ >]", h)) != 1:
            bad.append("%s: h1 count != 1" % url)
        if len(re.findall(r'<link rel="alternate" hreflang="', h)) != 12:
            bad.append("%s: hreflang count != 12" % url)
        if "<loc>%s</loc>" % url not in sitemap_text:
            bad.append("%s: not in live sitemap" % url)
        ok = False
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, flags=re.S):
            try:
                j = json.loads(m.group(1))
            except ValueError:
                bad.append("%s: JSON-LD does not parse" % url)
                continue
            if j.get("@type") == "BlogPosting":
                ok = all(j.get(k) for k in ("datePublished", "dateModified", "inLanguage", "headline"))
        if not ok:
            bad.append("%s: BlogPosting JSON-LD incomplete" % url)
    return bad


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    slug = argv[0] if argv else newest_slug()
    if not slug:
        print("check_blog_live: no blog post in sitemap.xml - nothing to check")
        return 0
    bad = []
    for attempt in range(6):
        try:
            bad = check(slug, get(SITE + "/sitemap.xml")[1])
        except Exception as ex:  # noqa: BLE001
            bad = ["sitemap: %s" % ex]
        if not bad:
            break
        time.sleep(30)
    if bad:
        print("check_blog_live: %s FAILED\n  " % slug + "\n  ".join(bad))
        return 1
    print("check_blog_live: %s ok - 11 languages 200, canonical/h1/hreflang/JSON-LD/sitemap fine" % slug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
