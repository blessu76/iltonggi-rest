#!/usr/bin/env python3
"""Build iltonggi.ipe.rest: 11 languages x (home, privacy, terms, support) + 404 + sitemap.

    python3 scripts/build_site.py          # write pages (generated files are never hand-edited)
    python3 scripts/build_site.py --check  # fail if the committed pages differ from a fresh build

Sources: content/<lang>.json (all copy), content/template-notes none; CSS in assets/site.css.
Layout follows still.ipe.rest: root (/) = English = x-default, plus /<lang>/ for every language
(en included, own canonical); hreflang + x-default on every page; language links in the footer;
a root-only hint that suggests (never redirects) the browser language. Stdlib only, Python 3.8+.
"""
import hashlib
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://iltonggi.ipe.rest"
MAIL = "ipe.haven@gmail.com"
LANGS = ["en", "ko", "ja", "zh", "es", "pt", "id", "ru", "vi", "fr", "de"]
OG = {"en": "en_US", "ko": "ko_KR", "ja": "ja_JP", "zh": "zh_CN", "es": "es_ES", "pt": "pt_BR",
      "id": "id_ID", "ru": "ru_RU", "vi": "vi_VN", "fr": "fr_FR", "de": "de_DE"}
NATIVE = {"en": "English", "ko": "한국어", "ja": "日本語", "zh": "中文", "es": "Español", "pt": "Português",
          "id": "Bahasa Indonesia", "ru": "Русский", "vi": "Tiếng Việt", "fr": "Français", "de": "Deutsch"}
PAGES = ["home", "privacy", "terms", "support"]
PATH = {"home": "/", "privacy": "/privacy/", "terms": "/terms/", "support": "/support/"}
FONT = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
        "&family=JetBrains+Mono:wght@400;500&family=Lora:wght@400;500;600&display=swap")
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
    """strings may carry {mail} / {privacy} / {support}; everything else is escaped."""
    out = esc(s)
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
<html lang="{lang}" dir="ltr">
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
<meta property="og:image" content="{SITE}{asset('icon-512.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT}">
<link rel="stylesheet" href="{asset('site.css')}">
{extra}</head>
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
      <a href="{p}/support/">{esc(t['nav_support'])}</a>
    </nav>
  </div>
  <nav class="foot-langs container" aria-label="{esc(t['lang_aria'])}">{langs}</nav>
</footer>
'''


HINT = '''<div class="lang-hint" id="langHint" hidden></div>
<script>
(function () {
  var NAMES = %s, CLOSE = %s;
  var hint = document.getElementById('langHint'); if (!hint) return;
  try { if (sessionStorage.getItem('iltonggi_hint_off') === '1') return; } catch (e) {}
  var pick = null;
  try { var list = navigator.languages || [navigator.language || '']; for (var i = 0; i < list.length && !pick; i++) { var c = String(list[i]).toLowerCase().split('-')[0]; if (NAMES[c]) pick = c; } } catch (e) {}
  if (!pick || pick === 'en') return;
  var a = document.createElement('a'); a.href = '/' + pick + '/'; a.hreflang = pick; a.lang = pick; a.textContent = NAMES[pick] + ' \\u2192';
  var b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', CLOSE); b.textContent = '\\u00d7';
  b.addEventListener('click', function () { hint.hidden = true; try { sessionStorage.setItem('iltonggi_hint_off', '1'); } catch (e) {} });
  hint.appendChild(a); hint.appendChild(b); hint.hidden = false;
})();
</script>
'''


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
    if root:
        out += HINT % (json.dumps(NATIVE, ensure_ascii=False), json.dumps(t["hint_close"], ensure_ascii=False))
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
        meta = '      <p class="meta">%s</p>\n' % esc(t["meta_line"])
    # [[privacy]] placeholder is raw-escaped by esc(); restore it
    body = body.replace("[[privacy]]", '<a href="%s/privacy/">%s</a>' % (p, esc(t["privacy_link"])))
    out = head(t, lang, page, root, "%s — %s" % (d["title"], t["name"]), d["desc"]) + header(t, lang, root)
    out += f'''<main id="content">
  <section class="doc">
    <div class="container doc__body">
      <p class="kicker">// {page}</p>
      <h1>{esc(d['title'])}</h1>
{meta}{body}
      <div class="doc__links"><a href="{p}/">← {esc(t['back_home'])}</a></div>
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


def sitemap():
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
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def build():
    data = load()
    files = {}
    for page in PAGES:
        builder = home if page == "home" else (lambda t, l, r, pg=page: doc(t, l, pg, r))
        files[("index.html" if page == "home" else PATH[page].strip("/") + "/index.html")] = builder(data["en"], "en", True)
        for l in LANGS:
            files["%s/%s" % (l, "index.html" if page == "home" else PATH[page].strip("/") + "/index.html")] = builder(data[l], l, False)
    files["404.html"] = not_found(data)
    files["sitemap.xml"] = sitemap()
    return files


def main():
    files = build()
    if "--check" in sys.argv:
        stale = [f for f, s in files.items() if not (ROOT / f).exists() or (ROOT / f).read_text(encoding="utf-8") != s]
        if stale:
            print("stale (run scripts/build_site.py):", *stale, sep="\n  ")
            return 1
        print("ok: %d files up to date" % len(files))
        return 0
    for f, s in files.items():
        (ROOT / f).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / f).write_text(s, encoding="utf-8")
    print("wrote %d files" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
