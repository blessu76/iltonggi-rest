#!/usr/bin/env python3
"""Making-of blog for iltonggi.ipe.rest: /blog/ list, /blog/<slug>/ posts, 11 languages, RSS. Stdlib only, Python 3.8+.

Imported by build_site.py (never run on its own; `python3 scripts/blog.py` just lints the queue + posts).

Layout of the sources (see README.md "블로그"):
    content/blog/ui.json                      UI strings, 11 languages
    content/blog/queue/<NNN>-<slug>/<lang>.md reviewed posts waiting for the daily publish (only publish_blog.py writes here; never built)
    content/blog/posts/<slug>/<lang>.md       published posts (built into the site)

A post = 11 markdown files (en ko ja zh es pt id ru vi fr de), same slug. en + ko are originals; the other nine carry
`translation_of: en|ko` and are shown with the AI-translation note. Front matter (all keys on one line, `key: value`):

    title, description, slug (= folder name), lang (= file name), date (KST day), [translation_of], [updated: ISO +09:00]
    published: ISO time with +09:00 offset (stamped by publish_blog.py; same in all 11 files, same KST day as `date`)

Body markdown subset: paragraphs, `## h2`, `### h3`, `- ` lists, `1. ` lists, `> ` quotes, `**bold**`, `*em*`,
`[text](/same-site/path)` links and `![alt](/assets/blog/file.webp)` images. Anything else is escaped text.
"""
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "content" / "blog"
LANGS = ["en", "ko", "ja", "zh", "es", "pt", "id", "ru", "vi", "fr", "de"]
ORIGINALS = ("en", "ko")
KST = dt.timezone(dt.timedelta(hours=9))
PER_PAGE = 10
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = set(LANGS) | {"feed", "page", "feed.xml"}
ISO_RE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?\+09:00$")

# Things that must never reach a public post (brief 2026-10-29). A safety net for the publish step — Dane's review is the real gate.
LINT = [
    (r"```|`", "code/backtick"),
    (r"https?://|www\.", "external URL (only /same-site links are allowed)"),
    (r"(?:/Users/|/home/|~/|[A-Za-z]:\\)", "local path"),
    (r"\b[\w-]+\.(?:py|dart|sh|plist|json|yaml|yml|swift|kt|gradle)\b", "file name"),
    (r"\b(?:sk|pk|ghp|gho|ghs|AKIA|AIza|xox[bp])[-_A-Za-z0-9]{12,}", "secret-looking token"),
    (r"(?i)\b(?:api[_ -]?key|secret|password|passwd|private[_ -]?key)\b", "secret word"),
    (r"[\w.+-]+@[\w-]+\.[\w.-]+", "e-mail address"),
    (r"[$€£¥₩]\s?\d|\d\s?(?:원|円|元|USD|KRW|JPY|EUR|dollars?|won)\b", "price"),
    (r"(?i)\b(?:\d{1,3}\.){3}\d{1,3}\b", "IP address"),
    (r"(?i)\b(?:worktree|harness|foundry(?:-f\d+)?|launchd|ipe-room)\b|워크트리|하네스", "internal tooling word"),
]


class BlogError(ValueError):
    pass


def esc(s):
    return html.escape(s, quote=True)


def lint(text):
    """-> [problem] found in a post file's text (front matter included)."""
    out = []
    for pat, why in LINT:
        m = re.search(pat, text)
        if m:
            out.append("%s: %r" % (why, m.group(0)[:40]))
    return out


# ---- parsing -----------------------------------------------------------------------------------------------------

def parse(text, where="?"):
    """-> (meta dict, body str). Raises BlogError."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise BlogError("%s: must start with ---" % where)
    head, sep, body = text[4:].partition("\n---")
    if not sep:
        raise BlogError("%s: front matter is not closed with ---" % where)
    meta = {}
    for line in head.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not m:
            raise BlogError("%s: bad front matter line %r" % (where, line))
        v = m.group(2).strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        meta[m.group(1)] = v
    return meta, body.lstrip("\n")


def check_post_files(d, slug, published=True):
    """Validate one post folder (11 files). -> {lang: (meta, body)}. Raises BlogError listing every problem."""
    errors, out = [], {}
    d = Path(d)
    for lang in LANGS:
        f = d / (lang + ".md")
        if not f.is_file():
            errors.append("%s: missing" % f.name)
            continue
        try:
            meta, body = parse(f.read_text(encoding="utf-8"), f.name)
        except BlogError as ex:
            errors.append(str(ex))
            continue
        out[lang] = (meta, body)
        w = f.name
        for k in ("title", "description", "slug", "lang", "date"):
            if not meta.get(k):
                errors.append("%s: no `%s:`" % (w, k))
        if meta.get("slug") != slug:
            errors.append("%s: slug %r != folder slug %r" % (w, meta.get("slug"), slug))
        if meta.get("lang") != lang:
            errors.append("%s: lang %r != file name" % (w, meta.get("lang")))
        if lang in ORIGINALS and meta.get("translation_of"):
            errors.append("%s: originals (en, ko) must not have translation_of" % w)
        if lang not in ORIGINALS and meta.get("translation_of") not in ORIGINALS:
            errors.append("%s: needs `translation_of: en` or `ko`" % w)
        if meta.get("date") and not re.match(r"^\d{4}-\d\d-\d\d$", meta["date"]):
            errors.append("%s: date must be YYYY-MM-DD" % w)
        if meta.get("updated") and not ISO_RE.match(meta["updated"]):
            errors.append("%s: updated must be ISO time with +09:00" % w)
        pub = meta.get("published", "")
        if published:
            if not ISO_RE.match(pub):
                errors.append("%s: `published:` must be ISO time with +09:00 (e.g. 2026-10-30T12:00:00+09:00)" % w)
            elif pub[:10] != meta.get("date"):
                errors.append("%s: `published` day != `date`" % w)
        elif pub:
            errors.append("%s: queued posts must not have `published:` (publish_blog.py stamps it)" % w)
        try:
            render_body(body)
        except BlogError as ex:
            errors.append("%s: %s" % (w, ex))
    if len(out) == len(LANGS):
        for k in ("published", "date"):
            if len({m.get(k) for m, _ in out.values()}) > 1:
                errors.append("`%s` differs between languages" % k)
    if errors:
        raise BlogError("; ".join(errors))
    return out


def load_posts(root=ROOT):
    """All published posts, newest first -> [{slug, no, published(datetime), files{lang:(meta,body)}}]."""
    base = Path(root) / "content" / "blog" / "posts"
    posts = []
    for d in sorted(p for p in base.glob("*") if p.is_dir()) if base.is_dir() else []:
        slug = d.name
        if not SLUG_RE.match(slug) or slug in RESERVED:
            raise BlogError("bad slug %r" % slug)
        files = check_post_files(d, slug)
        pub = dt.datetime.fromisoformat(files["en"][0]["published"])
        mods = [m.get("updated") or m["published"] for m, _ in files.values()]
        posts.append({"slug": slug, "published": pub, "files": files, "modified": max(dt.datetime.fromisoformat(x) for x in mods)})
    posts.sort(key=lambda p: (p["published"], p["slug"]))
    for i, p in enumerate(posts, 1):
        p["no"] = i  # No. N = publish order (oldest = 1), same in every language
    posts.reverse()
    return posts


# ---- markdown subset ---------------------------------------------------------------------------------------------

def inline(s):
    out = esc(s)

    def link(m):
        href = html.unescape(m.group(2))
        if not href.startswith("/") or href.startswith("//"):
            raise BlogError("link %r: only same-site /paths are allowed" % href)
        return '<a href="%s">%s</a>' % (esc(href), m.group(1))

    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", out)
    return out


def render_body(body):
    blocks, cur = [], []
    for line in body.split("\n") + [""]:
        if line.strip():
            cur.append(line.rstrip())
        elif cur:
            blocks.append(cur)
            cur = []
    out = []
    for b in blocks:
        first = b[0]
        if re.match(r"^#{2,3} ", first) and len(b) == 1:
            n = len(first.split(" ")[0])
            out.append("<h%d>%s</h%d>" % (n, inline(first[n + 1:]), n))
        elif all(re.match(r"^- ", x) for x in b):
            out.append("<ul>\n" + "\n".join("<li>%s</li>" % inline(x[2:]) for x in b) + "\n</ul>")
        elif all(re.match(r"^\d+\. ", x) for x in b):
            out.append("<ol>\n" + "\n".join("<li>%s</li>" % inline(re.sub(r"^\d+\. ", "", x)) for x in b) + "\n</ol>")
        elif all(x.startswith(">") for x in b):
            out.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(x[1:].strip() for x in b)))
        elif len(b) == 1 and re.match(r"^!\[[^\]]*\]\(/assets/blog/[A-Za-z0-9._-]+\)$", first):
            m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", first)
            out.append('<figure><img loading="lazy" src="%s" alt="%s"></figure>' % (esc(m.group(2)), esc(m.group(1))))
        elif first.startswith(("#", "!")) and not first.startswith("**"):
            raise BlogError("unsupported block %r (use ## / ### headings, /assets/blog/ images)" % first[:40])
        else:
            out.append("<p>%s</p>" % "<br>\n".join(inline(x) for x in b))
    return "\n".join(out)


# ---- pages -------------------------------------------------------------------------------------------------------

def org(bs):
    return {"@type": "Organization", "@id": "https://ipe.rest/#organization", "name": "ipe()", "url": "https://ipe.rest/",
            "logo": {"@type": "ImageObject", "url": bs.SITE + bs.asset("icon-512.png"), "width": 512, "height": 512}}


def warnings(meta, body, lang):
    """SEO guide v1 (P0-9, P1-3) soft limits -> [warning]; never blocks a publish."""
    cjk = lang in ("ja", "zh", "ko")
    n = len(re.sub(r"\s", "", body)) if cjk else len(re.findall(r"\w+", body))
    out = []
    if lang in ORIGINALS:
        floor = (800, 300) if cjk else (400, 300)  # target / minimum (CJK: characters; others: words)
        if n < (500 if cjk else floor[1]):
            out.append("%s: body %d %s is below the minimum (%s)" % (lang, n, "chars" if cjk else "words", "500 chars" if cjk else "300 words"))
    tl, dl = (40, 110) if cjk else (60, 160)
    if len(meta["title"]) > tl:
        out.append("%s: title %d chars > %d" % (lang, len(meta["title"]), tl))
    if len(meta["description"]) > dl:
        out.append("%s: description %d chars > %d" % (lang, len(meta["description"]), dl))
    return out


def ui_all():
    return json.loads((BLOG / "ui.json").read_text(encoding="utf-8"))


def list_path(n):
    return "/blog/" if n == 1 else "/blog/page/%d/" % n


def post_path(slug):
    return "/blog/%s/" % slug


def time_tag(iso):
    return '<time datetime="%s" data-ipe-time>%s KST</time>' % (iso, iso[:10] + " " + iso[11:16])


def localtime_script():
    return "<script>" + (ROOT / "scripts" / "ipe-localtime.js").read_text(encoding="utf-8").strip() + "</script>\n"


def build(bs, data, root=ROOT):
    """-> (files {relpath: text}, sitemap_extra [(page key, lastmod, changefreq, priority)]). `bs` = the build_site module."""
    UI = ui_all()
    posts = load_posts(root)
    pages = max(1, -(-len(posts) // PER_PAGE))
    files, extra = {}, []
    entries = [("en", True)] + [(l, False) for l in LANGS]

    def reg(key, path, lastmod, freq, prio):
        bs.PATH[key] = path
        extra.append((key, lastmod, freq, prio))

    def rel(lang, root_, path):
        return ("" if root_ else lang + "/") + path.strip("/") + "/index.html"

    for n in range(1, pages + 1):
        chunk_ = posts[(n - 1) * PER_PAGE:n * PER_PAGE]
        reg("blog:p%d" % n, list_path(n), max(p["modified"] for p in chunk_).date().isoformat() if chunk_ else None, None, None)
    for p in posts:
        reg("blog:" + p["slug"], post_path(p["slug"]), p["modified"].date().isoformat(), None, None)

    for lang, root_ in entries:
        t, ui = data[lang], UI[lang]
        pre = bs.prefix(lang, root_)
        for n in range(1, pages + 1):
            chunk = posts[(n - 1) * PER_PAGE:n * PER_PAGE]
            files[rel(lang, root_, list_path(n))] = list_page(bs, t, ui, lang, root_, pre, chunk, n, pages, bool(posts))
        for p in posts:
            files[rel(lang, root_, post_path(p["slug"]))] = post_page(bs, data, t, ui, lang, root_, pre, p, posts)
    if posts:
        files["blog/feed.xml"] = feed(posts)
    files["llms.txt"] = llms_txt(bs, data, UI, posts)
    return files, extra


def feed_link(ui, lang):
    return '<link rel="alternate" type="application/rss+xml" title="%s" href="/blog/feed.xml">\n' % esc(ui["title"])


def list_page(bs, t, ui, lang, root_, pre, chunk, n, pages, has_posts):
    key = "blog:p%d" % n
    title = "%s — %s" % (ui["nav"], t["name"]) if n == 1 else "%s · %s %d — %s" % (ui["nav"], ui["page"], n, t["name"])
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Blog", "name": ui["title"], "description": ui["lead"], "inLanguage": lang,
        "url": bs.url(lang, key, root_), "publisher": org(bs),
        "blogPost": [{"@type": "BlogPosting", "headline": p["files"][lang][0]["title"], "url": bs.url(lang, "blog:" + p["slug"], root_),
                      "datePublished": p["published"].isoformat(timespec="seconds"), "dateModified": p["modified"].isoformat(timespec="seconds")}
                     for p in chunk],
    }, ensure_ascii=False)
    extra = (feed_link(ui, lang) if has_posts else "") + '<script type="application/ld+json">%s</script>\n' % ld
    if n > 1:
        extra = '<link rel="prev" href="%s">\n' % bs.url(lang, "blog:p%d" % (n - 1), root_) + extra
    if n < pages:
        extra = '<link rel="next" href="%s">\n' % bs.url(lang, "blog:p%d" % (n + 1), root_) + extra
    cards = ""
    for p in chunk:
        m = p["files"][lang][0]
        cards += f'''      <article class="post-card">
        <p class="post-card__meta">No. {p['no']} · {time_tag(p['published'].isoformat(timespec='seconds'))}</p>
        <h2 class="post-card__title"><a href="{pre}{post_path(p['slug'])}">{esc(m['title'])}</a></h2>
        <p>{esc(m['description'])}</p>
      </article>
'''
    if not has_posts:
        cards = '      <p class="callout">%s</p>\n' % esc(ui["empty"])
    pager = ""
    if pages > 1:
        newer = '<a rel="prev" href="%s%s">← %s</a>' % (pre, list_path(n - 1), esc(ui["newer"])) if n > 1 else ""
        older = '<a rel="next" href="%s%s">%s →</a>' % (pre, list_path(n + 1), esc(ui["older"])) if n < pages else ""
        pager = '      <nav class="pager" aria-label="%s">%s<span class="pager__now">%d / %d</span>%s</nav>\n' % (
            esc(ui["page"]), newer, n, pages, older)
    out = bs.head(t, lang, key, root_, title, ui["lead"], extra) + bs.header(t, lang, root_)
    out += f'''<main id="content">
  <section class="doc">
    <div class="container doc__body">
      <p class="kicker">// blog</p>
      <h1>{esc(ui['title'])}</h1>
      <p class="lead">{esc(ui['lead'])}</p>
      <div class="post-list">
{cards}      </div>
{pager}      <div class="doc__links"><a href="{pre}/">← {esc(t['back_home'])}</a></div>
    </div>
  </section>
</main>
'''
    return out + (localtime_script() if chunk else "") + bs.footer(t, lang, key, root_) + "</body>\n</html>\n"


def post_page(bs, data, t, ui, lang, root_, pre, p, posts_all):
    key = "blog:" + p["slug"]
    meta, body = p["files"][lang]
    iso = p["published"].isoformat(timespec="seconds")
    modified = p["modified"].isoformat(timespec="seconds")
    can = bs.url(lang, key, root_)
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": meta["title"], "description": meta["description"],
        "datePublished": iso, "dateModified": modified, "inLanguage": lang, "url": can,
        "mainEntityOfPage": {"@type": "WebPage", "@id": can},
        "image": {"@type": "ImageObject", "url": bs.SITE + bs.asset("icon-512.png"), "width": 512, "height": 512},
        "author": {"@id": "https://ipe.rest/#organization"}, "publisher": org(bs),
    }, ensure_ascii=False)
    crumbs = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["name"], "item": bs.url(lang, "home", root_)},
        {"@type": "ListItem", "position": 2, "name": ui["nav"], "item": bs.url(lang, "blog:p1", root_)},
        {"@type": "ListItem", "position": 3, "name": meta["title"], "item": can}]}, ensure_ascii=False)
    extra = (feed_link(ui, lang)
             + '<meta property="article:published_time" content="%s">\n' % iso
             + '<meta property="article:modified_time" content="%s">\n' % modified
             + '<script type="application/ld+json">%s</script>\n' % ld
             + '<script type="application/ld+json">%s</script>\n' % crumbs)
    ai = ""
    if meta.get("translation_of"):
        o = meta["translation_of"]
        orig = bs.url(o, key, False)
        ai = '      <p class="meta ai-note">%s <a href="%s" hreflang="%s">%s</a></p>\n' % (
            esc(ui["ai_note"]), orig.replace(bs.SITE, ""), o, esc(ui["ai_orig"]))
    out = bs.head(t, lang, key, root_, "%s — %s" % (meta["title"], t["name"]), meta["description"], extra)
    out = out.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    out += bs.header(t, lang, root_)
    out += f'''<main id="content">
  <article class="doc">
    <div class="container doc__body post">
      <p class="kicker">// blog · No. {p['no']}</p>
      <h1>{esc(meta['title'])}</h1>
      <p class="meta">{time_tag(iso)}</p>
{ai}      <div class="post__body">
{render_body(body)}
      </div>
{more_links(p, posts_all, lang, pre, ui)}      <div class="doc__links"><a href="{pre}/blog/">← {esc(ui['back'])}</a></div>
    </div>
  </article>
</main>
'''
    return out + localtime_script() + bs.footer(t, lang, key, root_) + "</body>\n</html>\n"


def more_links(p, posts_all, lang, pre, ui):
    """Previous/next (by publish order) + up to 3 more recent posts of the same language (SEO guide P1-1)."""
    i = posts_all.index(p)  # newest first
    newer = posts_all[i - 1] if i > 0 else None
    older = posts_all[i + 1] if i + 1 < len(posts_all) else None

    def a(q):
        return '<a href="%s%s">%s</a>' % (pre, post_path(q["slug"]), esc(q["files"][lang][0]["title"]))
    pn = ""
    if older:
        pn += '<li>← %s: %s</li>' % (esc(ui["prev_post"]), a(older))
    if newer:
        pn += '<li>%s →: %s</li>' % (esc(ui["next_post"]), a(newer))
    out = '      <nav class="post-nav" aria-label="%s"><ul>%s</ul></nav>\n' % (esc(ui["related"]), pn) if pn else ""
    shown = {q["slug"] for q in (newer, older) if q} | {p["slug"]}
    rel = [q for q in posts_all if q["slug"] not in shown][:3]
    if rel:
        out += '      <section class="post-more"><h2>%s</h2><ul>%s</ul></section>\n' % (
            esc(ui["related"]), "".join("<li>%s</li>" % a(q) for q in rel))
    return out


def llms_txt(bs, data, UI, posts):
    en = data["en"]
    lines = ["# Iltonggi (一統記 · 일통기)", "",
             "> A Three Kingdoms strategy game for iOS by ipe Studio, in 11 languages. This site has the game page, release notes and a making-of blog (one short note a day).", "",
             "## Pages", "- [Home](%s/): what the game is" % bs.SITE,
             "- [Release notes](%s/releases/): what changed in each TestFlight build" % bs.SITE,
             "- [Support](%s/support/)" % bs.SITE, "- [Privacy](%s/privacy/)" % bs.SITE, "- [Terms](%s/terms/)" % bs.SITE, "",
             "## Blog (every post exists in %s)" % ", ".join(bs.LANGS), "- [Blog index](%s/blog/)" % bs.SITE]
    if posts:
        lines.append("- [RSS feed](%s/blog/feed.xml)" % bs.SITE)
        for q in posts:
            m = q["files"]["en"][0]
            lines.append("- [%s](%s/blog/%s/): %s" % (m["title"], bs.SITE, q["slug"], m["description"]))
    return "\n".join(lines) + "\n"


def feed(posts):
    site = "https://iltonggi.ipe.rest"
    items = ""
    for p in posts[:20]:
        m = p["files"]["en"][0]
        pub = p["published"].strftime("%a, %d %b %Y %H:%M:%S +0900")
        items += "  <item>\n    <title>%s</title>\n    <link>%s/blog/%s/</link>\n    <guid>%s/blog/%s/</guid>\n    <pubDate>%s</pubDate>\n    <description>%s</description>\n  </item>\n" % (
            esc(m["title"]), site, p["slug"], site, p["slug"], pub, esc(m["description"]))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n  <title>Making of Iltonggi</title>\n'
            '  <link>%s/blog/</link>\n  <description>How Iltonggi is being made — one short note a day.</description>\n'
            '  <language>en</language>\n%s</channel>\n</rss>\n' % (site, items))


def main(argv=None):
    """Lint (and structure-check) every queued and published post."""
    bad = 0
    for kind, published in (("queue", False), ("posts", True)):
        for d in sorted(p for p in (BLOG / kind).glob("*") if p.is_dir()):
            slug = re.sub(r"^\d+-", "", d.name) if kind == "queue" else d.name
            try:
                files = check_post_files(d, slug, published=published)
                for lang, (meta, body) in files.items():
                    for prob in lint((d / (lang + ".md")).read_text(encoding="utf-8")):
                        raise BlogError("%s.md: %s" % (lang, prob))
                print("ok  %s/%s" % (kind, d.name))
                for lang, (meta, body) in files.items():
                    for w in warnings(meta, body, lang):
                        print("  warn %s" % w)
            except BlogError as ex:
                bad += 1
                print("BAD %s/%s: %s" % (kind, d.name, ex))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
