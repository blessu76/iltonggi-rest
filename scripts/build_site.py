#!/usr/bin/env python3
"""Build iltonggi.ipe.rest: 12 languages x (home, privacy, terms, support, journal) + 404 + sitemap.

    python3 scripts/build_site.py          # write pages (generated files are never hand-edited)
    python3 scripts/build_site.py --check  # fail if the committed pages differ from a fresh build

Sources: content/<tag>.json (all copy), CSS in assets/site.css. The language list, order and names come from ipe_web_kit.languages (vendor/, locked).
Layout follows still.ipe.rest: root (/) = English = x-default, plus /<tag>/ for every language
(en included, own canonical); hreflang + x-default on every page; language links in the footer;
every page that opens without a language prefix picks the language itself (?lang= > saved choice > browser language > English, see scripts/lang_resolve.js). Stdlib only, Python 3.8+.
"""
import hashlib
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "vendor"))
import blog  # noqa: E402
from ipe_web_kit import languages  # noqa: E402

SITE = "https://iltonggi.ipe.rest"
MAIL = "ipe.haven@gmail.com"
LANGS = list(languages.SUPPORTED)  # en ko ja zh-Hant es pt-BR fr de id th vi tr — the folder under / is the tag itself
NATIVE = languages.NAMES
OG = {"en": "en_US", "ko": "ko_KR", "ja": "ja_JP", "zh-Hant": "zh_TW", "es": "es_ES", "pt-BR": "pt_BR",
      "fr": "fr_FR", "de": "de_DE", "id": "id_ID", "th": "th_TH", "vi": "vi_VN", "tr": "tr_TR"}
LEGACY_PT = "pt"  # old /pt/ addresses (before pt-BR) keep working as redirect stubs
RTL = set()  # none of the 12 languages is right-to-left; the helpers stay so a future one only needs an entry here


def direction(lang):
    return "rtl" if lang in RTL else "ltr"


def back_arrow(lang):
    """Glyph for 'back / newer / previous' (points to the start of the line): <- in LTR, -> in RTL."""
    return "→" if lang in RTL else "←"


def next_arrow(lang):
    """Glyph for 'forward / older / next' (points to the end of the line): -> in LTR, <- in RTL."""
    return "←" if lang in RTL else "→"


def blog_code(tag):
    """The blog posts and blog UI strings exist for the 9 older languages (pt = pt-BR); zh-Hant, th and tr show the English post."""
    c = languages.legacy_code(tag)
    return c if c in blog.LANGS else "en"


PAGES = ["home", "privacy", "terms", "support"]
PATH = {"home": "/", "privacy": "/privacy/", "terms": "/terms/", "support": "/support/"}
FONT = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
        "&family=JetBrains+Mono:wght@400;500&family=Lora:wght@400;500;600&display=swap")
# GA4 (same property as ipe.rest; a subdomain, so no cross-domain setup). Inserted once by head(), which every page type
# (home, privacy, terms, support, 404, blog list/post) goes through. The privacy policy (section 3), the support FAQ and
# privacy_meta_line say so -> change them together with this. Skipped in the in-app web view (?app=1): the app collects nothing.
GA_MEASUREMENT_ID = "G-XG4BH800J0"
GA_SNIPPET = (
    "<script>(function(){if(/[?&]app=1(&|$)/.test(location.search))return;var GA_ID='%s';"
    "var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID;document.head.appendChild(s);"
    "window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments)};"
    "window.gtag('js',new Date());window.gtag('config',GA_ID);"
    "function track(e){if(e.type==='auxclick'&&e.button!==1)return;"
    "var a=e.target.closest&&e.target.closest('a[href^=\"http\"]');if(!a)return;"
    "var h=a.hostname;if(h==='ipe.rest'||/\\.ipe\\.rest$/.test(h))return;"
    "window.gtag('event','outbound_click',{link_url:a.href,link_domain:h,transport_type:'beacon'})}"
    "document.addEventListener('click',track);document.addEventListener('auxclick',track)})();</script>\n") % GA_MEASUREMENT_ID
GA_OPTOUT = "https://tools.google.com/dlpage/gaoptout"
IMG = {"icon": "icon-512.png", "map": "shot-map-600.webp", "march": "shot-march-600.webp"}


def esc(s):
    return html.escape(s, quote=True)


def asset(name):
    """/assets/<name>?v=<8 hex of the file bytes> — cache busting that changes only when the file does."""
    v = hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]
    return "/assets/%s?v=%s" % (name, v)


def load():
    return {l: json.loads((ROOT / "content" / (l + ".json")).read_text(encoding="utf-8")) for l in LANGS}


def rich(s):
    """strings may carry {mail} / {gaoptout} / {privacy} / {support}; everything else is escaped."""
    out = esc(s)
    out = out.replace("{gaoptout}", '<a href="%s" rel="noopener">tools.google.com/dlpage/gaoptout</a>' % GA_OPTOUT)
    out = out.replace("{mail}", '<a href="mailto:%s">%s</a>' % (MAIL, MAIL))
    return out


def prefix(lang, root):
    return "" if root else "/" + lang


def url(lang, page, root):
    return SITE + prefix(lang, root) + PATH[page]


def head(t, lang, page, root, title, desc, extra="", robots="index,follow", canonical=None, alt=True):
    can = canonical or url(lang, page, root)
    alts = ""
    if alt:
        alts = "".join('<link rel="alternate" hreflang="%s" href="%s">\n' % (l, url(l, page, False)) for l in LANGS)
        alts += '<link rel="alternate" hreflang="x-default" href="%s">\n' % url("en", page, True)
    return f'''<!doctype html>
<html lang="{lang}" dir="{direction(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#24312b">
<link rel="canonical" href="{can}">
{alts}<link rel="icon" type="image/png" sizes="32x32" href="{asset('favicon-32.png')}">
<link rel="icon" type="image/png" sizes="192x192" href="{asset('favicon-192.png')}">
<link rel="apple-touch-icon" href="{asset('apple-touch-icon.png')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(t['name'])}">
<meta property="og:locale" content="{OG[lang]}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{can}">
<meta property="og:image" content="{SITE}{asset('og-share.jpg')}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Iltonggi app icon and in-game map of a Three Kingdoms land-grab strategy game">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{asset('og-share.jpg')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT}">
<link rel="stylesheet" href="{asset('site.css')}">
{LANG_MARK if root and canonical is None else ""}{extra}{GA_SNIPPET}</head>
<body>
'''


def header(t, lang, root):
    p = prefix(lang, root)
    return f'''<a class="skip-link" href="#content">{esc(t['skip'])}</a>
<header class="site-header">
  <div class="site-header__inner container">
    <a class="brand" href="{p}/" aria-label="{esc(t['home_aria'])}">
      <span class="seal" aria-hidden="true"></span>
      <span class="brand__text">
        <span class="brand__name">{esc(t['name'])}</span>
        <span class="brand__sub">ipe studio</span>
      </span>
    </a>
    <nav class="nav" aria-label="{esc(t['nav_aria'])}">
      <a href="{p}{blog.list_path(1)}">{esc(blog.ui_all()[blog_code(lang)]['nav'])}</a>
      <a href="{p}/support/">{esc(t['nav_support'])}</a>
    </nav>
  </div>
</header>

'''


def footer(t, lang, page, root):
    p = prefix(lang, root)
    langs = "".join(
        '<a href="%s"%s hreflang="%s" lang="%s">%s</a>' % (
            (PATH[page] if root and l == "en" else "/" + l + PATH[page]),
            ' aria-current="true"' if l == lang else "", l, l, NATIVE[l])
        for l in LANGS)
    return f'''
<footer class="site-footer">
  <div class="site-footer__inner container">
    <div>
      <p class="h3">ipe Studio</p>
      <p class="site-footer__meta"><span>iltonggi.ipe.rest</span><span>{MAIL}</span></p>
      <p class="site-footer__credit">Weather data: <a href="https://www.met.no/en" rel="noopener">MET Norway</a> (<a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener">CC BY 4.0</a>)</p>
    </div>
    <nav class="footer-links" aria-label="{esc(t['legal_aria'])}">
      <a href="{p}/privacy/">{esc(t['privacy_link'])}</a>
      <a href="{p}/terms/">{esc(t['terms_link'])}</a>
      <a href="{p}{blog.list_path(1)}">{esc(blog.ui_all()[blog_code(lang)]['nav'])}</a>
      <a href="{p}/support/">{esc(t['nav_support'])}</a>
    </nav>
  </div>
  <nav class="foot-langs container" aria-label="{esc(t['lang_aria'])}">{langs}</nav>
</footer>
{FOOT_LANG_SCRIPT % json.dumps(LANG_KEY)}'''


LANG_KEY = "iltonggi-lang"
LANG_JS = (ROOT / "scripts" / "lang_resolve.js").read_text(encoding="utf-8").split("*/", 1)[1].strip()
# Every page that opens WITHOUT a language prefix (/, /privacy/, /terms/, /support/, /blog/..., not 404.html): inline in <head>, runs
# before first paint. Saves the language on ?lang=xx, then leaves for the same page under /xx/ (replace, so Back works) -- but only when that
# language really has this page (AV, filled in per page by add_lang_script() from the files of the build). English, an unsupported language
# or a language without this page stays where it is (the query is dropped). Path, other query params and #hash are kept. Pages under a
# language prefix never carry it (and it returns at once on one): no loop.
LANG_MARK = "<!--LANG-REDIRECT-->\n"  # head() puts it on a prefix-less page; build() swaps it for the script
PAGE_LANG_SCRIPT = (
    "<script>(function(){" + LANG_JS + "\n"
    "var SUP=%s,AV=%s,KEY=%s,st=null,pm=/^\\/([A-Za-z]{2,3}(?:-[A-Za-z]{2,4})?)\\//.exec(location.pathname);\n"
    "if(pm&&SUP.indexOf(pm[1])>=0)return;\n"
    "try{st=localStorage.getItem(KEY)}catch(e){}\n"
    "var r=ltResolve({search:location.search,stored:st,languages:navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language],supported:SUP});\n"
    "if(r.from==='url'){try{localStorage.setItem(KEY,r.lang)}catch(e){}}\n"
    "var q=ltStrip(location.search);\n"
    "if(r.lang!=='en'&&AV.indexOf(r.lang)>=0){location.replace('/'+r.lang+location.pathname+q+location.hash)}\n"
    "else if(/[?&]lang=/.test(location.search)&&history.replaceState){history.replaceState(null,'',location.pathname+q+location.hash)}\n"
    "})();</script>\n")


def add_lang_script(files):
    """Swap LANG_MARK in every prefix-less page for the language script with the languages that have THAT page (looked up in the build)."""
    for rel, text in files.items():
        if LANG_MARK not in text:
            continue
        have = [l for l in LANGS if l != "en" and "%s/%s" % (l, rel) in files]
        files[rel] = text.replace(LANG_MARK, PAGE_LANG_SCRIPT % (json.dumps(LANGS), json.dumps(have), json.dumps(LANG_KEY)), 1)
    return files


# Every page: choosing a language in the footer menu remembers it.
FOOT_LANG_SCRIPT = (
    "<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.foot-langs a[hreflang]');"
    "if(a)try{localStorage.setItem(%s,a.getAttribute('hreflang'))}catch(x){}});</script>\n")


def home(t, lang, root):
    p = prefix(lang, root)
    feats = "".join(
        '''        <article class="feature-card">
          <span class="feature-card__tag">0%d</span>
          <h3 class="feature-card__title">%s</h3>
          <p class="feature-card__text">%s</p>%s
        </article>
''' % (i + 1, esc(f[0]), esc(f[1]), '''
          <div class="nations" aria-hidden="true">
            <span style="background:var(--color-goguryeo)"></span>
            <span style="background:var(--color-baekje)"></span>
            <span style="background:var(--color-silla)"></span>
            <span style="background:var(--color-gaya)"></span>
          </div>''' if i == 2 else "")
        for i, f in enumerate(t["features"]))
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "VideoGame", "name": t["name"], "alternateName": ["Iltonggi", "일통기", "一統記"],
        "description": t["ld_desc"], "url": url(lang, "home", root), "image": SITE + asset("icon-512.png"),
        "inLanguage": lang, "gamePlatform": "iOS", "publisher": {"@type": "Organization", "name": "ipe Studio", "url": "https://ipe.rest/"},
    }, ensure_ascii=False)
    extra = '<script type="application/ld+json">%s</script>\n' % ld
    out = head(t, lang, "home", root, t["home_title"], t["desc"], extra) + header(t, lang, root)
    out += f'''<main id="content">
  <section class="hero section">
    <div class="hero__grid container-wide">
      <div class="hero__copy">
        <p class="kicker">{esc(t['kicker'])}</p>
        <span class="hero__badge"><span aria-hidden="true">●</span> {esc(t['badge'])}</span>
        <h1 class="h1 hero__title">{esc(t['name'])}<small>{esc(t['name_sub'])}</small></h1>
        <p class="lead hero__intro">{esc(t['intro'])}</p>
        <div class="hero__actions">
          <span class="btn btn--store" role="button" aria-disabled="true">App Store <small>{esc(t['soon'])}</small></span>
          <a class="btn btn--secondary" href="#shots">{esc(t['see_shots'])}</a>
        </div>
      </div>
      <div class="hero__media hanji" aria-hidden="true">
        <span class="ink-wash"></span>
        <div class="icon"><img src="{asset(IMG['icon'])}" alt="" width="512" height="512"></div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="features-title">
    <div class="container">
      <p class="kicker">// features</p>
      <h2 class="h2" id="features-title">{esc(t['feat_title'])}</h2>
      <div class="feature-grid">
{feats}      </div>
    </div>
  </section>

  <section class="section" id="shots" aria-labelledby="shots-title">
    <div class="container">
      <p class="kicker">// screenshots</p>
      <h2 class="h2" id="shots-title">{esc(t['shots_title'])}</h2>
      <div class="shots">
        <figure class="shot">
          <div class="shot__frame"><img loading="lazy" src="{asset(IMG['map'])}" alt="{esc(t['shot_alts'][0])}" width="600" height="277"></div>
          <figcaption>// screen 01</figcaption>
        </figure>
        <figure class="shot">
          <div class="shot__frame"><img loading="lazy" src="{asset(IMG['march'])}" alt="{esc(t['shot_alts'][1])}" width="600" height="277"></div>
          <figcaption>// screen 02</figcaption>
        </figure>
      </div>
    </div>
  </section>
</main>
'''
    return out + footer(t, lang, "home", root) + "</body>\n</html>\n"


def body_blocks(items):
    """paragraph strings; a leading '- ' makes consecutive items a list."""
    out, ul = [], []
    for s in items:
        if s.startswith("- "):
            ul.append("<li>%s</li>" % rich(s[2:]))
            continue
        if ul:
            out.append("      <ul>\n        " + "\n        ".join(ul) + "\n      </ul>")
            ul = []
        out.append("      <p>%s</p>" % rich(s))
    if ul:
        out.append("      <ul>\n        " + "\n        ".join(ul) + "\n      </ul>")
    return "\n".join(out)


def doc(t, lang, page, root):
    d = t[page]
    p = prefix(lang, root)
    if page == "support":
        body = "      <p class=\"lead\">%s</p>\n      <p class=\"callout\"><strong>%s</strong> · %s<br>%s</p>\n" % (
            esc(d["lead"]), esc(d["callout_label"]), rich("{mail}"), esc(d["callout_note"]))
        body += "\n      <h2>%s</h2>\n      <ul>\n%s\n      </ul>\n" % (
            esc(d["tips_h"]), "\n".join("        <li>%s</li>" % esc(x) for x in d["tips"]))
        body += "\n      <h2>%s</h2>\n" % esc(d["faq_h"])
        for q, a in d["faq"]:
            body += '      <h3 class="h3 faq-q">%s</h3>\n      <p>%s</p>\n' % (esc(q), rich(a).replace("{privacy}", ""))
        body = body.replace("[[privacy]]", '<a href="%s/privacy/">%s</a>' % (p, esc(t["privacy_link"])))
        meta = ""
    else:
        body = ""
        if d.get("callout"):
            body += '      <p class="callout"><strong>%s</strong> %s</p>\n' % (esc(d["callout_label"]), esc(d["callout"]))
        for s in d["sections"]:
            body += "\n      <h2>%s</h2>\n%s\n" % (esc(s["h"]), body_blocks(s["p"]))
        meta = '      <p class="meta">%s</p>\n' % esc(t["privacy_meta_line"] if page == "privacy" else t["meta_line"])
    # [[privacy]] placeholder is raw-escaped by esc(); restore it
    body = body.replace("[[privacy]]", '<a href="%s/privacy/">%s</a>' % (p, esc(t["privacy_link"])))
    out = head(t, lang, page, root, "%s — %s" % (d["title"], t["name"]), d["desc"]) + header(t, lang, root)
    out += f'''<main id="content">
  <section class="doc">
    <div class="container doc__body">
      <p class="kicker">// {page}</p>
      <h1>{esc(d['title'])}</h1>
{meta}{body}
      <div class="doc__links"><a href="{p}/">{back_arrow(lang)} {esc(t['back_home'])}</a></div>
    </div>
  </section>
</main>
'''
    return out + footer(t, lang, page, root) + "</body>\n</html>\n"


def not_found(data):
    t = data["en"]
    items = "".join(
        '      <li lang="%s"><span class="msg">%s</span> <a href="%s/">%s</a> · <a href="%s/support/">%s</a></li>\n' % (
            l, esc(data[l]["nf"]["title"]), "/" + l if l != "en" else "", esc(data[l]["back_home"]),
            "/" + l if l != "en" else "", esc(data[l]["nav_support"]))
        for l in LANGS)
    out = head(t, "en", "home", True, t["nf"]["title"] + " — " + t["name"], t["nf"]["desc"],
               robots="noindex, follow", canonical=SITE + "/404.html", alt=False) + header(t, "en", True)
    out += f'''<main id="content">
  <section class="doc">
    <div class="container doc__body">
      <p class="kicker">// 404</p>
      <h1>{esc(t['nf']['title'])}</h1>
      <p>{esc(t['nf']['text'])}</p>
      <ul class="nf-list">
{items}      </ul>
    </div>
  </section>
</main>
'''
    return out + footer(t, "en", "home", True).replace('<nav class="foot-langs', '<nav hidden class="foot-langs', 1) + "</body>\n</html>\n"


def redirect_page(target):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
<title>Português (Brasil) — ipe Studio</title>
</head>
<body><p><a href="{target}">{target}</a></p></body>
</html>
'''


def pt_redirects(blog_extra):
    """Old /pt/ addresses -> the same path under /pt-BR/ (links already out there keep working)."""
    keys = [PATH[p] for p in PAGES] + [PATH[k] for k, *_ in blog_extra]
    keys += [blog.legacy_list_path(n) for n in range(1, 1 + sum(1 for k, *_ in blog_extra if k.startswith("blog:p") and k[6:].isdigit()))]
    return {LEGACY_PT + path.rstrip("/") + "/index.html": redirect_page(SITE + "/pt-BR" + path) for path in keys}


def sitemap(extra=()):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    entries = [("en", True)] + [(l, False) for l in LANGS]
    for page in PAGES:
        for l, root in entries:
            out.append("  <url>\n    <loc>%s</loc>" % url(l, page, root))
            for l2 in LANGS:
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l2, url(l2, page, False)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url("en", page, True))
            out.append("    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>" % ("1.0" if page == "home" and root else "0.6"))
    for key, lastmod, freq, prio in extra:
        for l, root in entries:
            out.append("  <url>\n    <loc>%s</loc>" % url(l, key, root))
            for l2 in LANGS:
                out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l2, url(l2, key, False)))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % url("en", key, True))
            if lastmod:
                out.append("    <lastmod>%s</lastmod>" % lastmod)
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


DATA = {}


def build():
    data = load()
    DATA.clear()
    DATA.update(data)
    files = {}
    for page in PAGES:
        builder = home if page == "home" else (lambda t, l, r, pg=page: doc(t, l, pg, r))
        files[("index.html" if page == "home" else PATH[page].strip("/") + "/index.html")] = builder(data["en"], "en", True)
        for l in LANGS:
            files["%s/%s" % (l, "index.html" if page == "home" else PATH[page].strip("/") + "/index.html")] = builder(data[l], l, False)
    files["404.html"] = not_found(data)
    blog_files, blog_extra = blog.build(sys.modules[__name__], data, ROOT)
    files.update(blog_files)
    files.update(pt_redirects(blog_extra))
    files["sitemap.xml"] = sitemap(blog_extra)
    return add_lang_script(files)


def orphans(files):
    """Generated blog files on disk that the build no longer produces (e.g. a removed/renamed post)."""
    found = []
    for sec in ("blog", "journal"):
        found += [f for f in (ROOT / sec).rglob("*") if f.is_file()] if (ROOT / sec).is_dir() else []
        for l in LANGS + [LEGACY_PT]:
            if (ROOT / l / sec).is_dir():
                found += [f for f in (ROOT / l / sec).rglob("*") if f.is_file()]
    return sorted(str(f.relative_to(ROOT)) for f in found if str(f.relative_to(ROOT)) not in files)


def main():
    files = build()
    if "--check" in sys.argv:
        stale = [f for f, s in files.items() if not (ROOT / f).exists() or (ROOT / f).read_text(encoding="utf-8") != s]
        stale += ["%s (orphan, no longer generated)" % f for f in orphans(files)]
        if stale:
            print("stale (run scripts/build_site.py):", *stale, sep="\n  ")
            return 1
        print("ok: %d files up to date" % len(files))
        return 0
    for f in orphans(files):
        (ROOT / f).unlink()
        print("removed orphan", f)
    for f, s in files.items():
        (ROOT / f).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / f).write_text(s, encoding="utf-8")
    print("wrote %d files" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
