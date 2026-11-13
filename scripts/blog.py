#!/usr/bin/env python3
"""Making-of blog for iltonggi.ipe.rest: /blog/ list, /blog/<slug>/ posts, 12 site languages (9 post languages), RSS. Stdlib only, Python 3.8+.

Imported by build_site.py (never run on its own; `python3 scripts/blog.py` just lints the queue + posts).

Layout of the sources (see README.md "블로그"):
    content/blog/ui.json                      UI strings, 9 languages (en ko ja es pt id vi fr de)
    content/blog/queue/<NNN>-<slug>/<lang>.md reviewed posts waiting for the daily publish (only publish_blog.py writes here; never built)
    content/blog/posts/<slug>/<lang>.md       published posts (built into the site)

A post = 9 markdown files (en ko ja es pt id vi fr de), same slug. en + ko are originals; the other seven carry
`translation_of: en|ko` and are shown with the AI-translation note. Front matter (all keys on one line, `key: value`):

    title, description, slug (= folder name), lang (= file name), date (KST day), [translation_of], [updated: ISO +09:00]
    published: ISO time with +09:00 offset (stamped by publish_blog.py; same in all 9 files, same KST day as `date`)

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
sys.path.insert(0, str(ROOT / "vendor"))
try:
    from ipe_web_kit import localtime as kit_localtime  # noqa: E402  web kit (private, installed from vendor/ipe_web_kit.lock by scripts/kit_lock.py): the company-wide ipe-localtime module
except ImportError:
    sys.exit("ipe_web_kit is not installed (private, not in this repo). Run: python3 scripts/kit_lock.py sync --kit <local ipe_web_kit clone>")
BLOG = ROOT / "content" / "blog"
LANGS = ["en", "ko", "ja", "es", "pt", "id", "vi", "fr", "de"]  # post languages; zh-Hant / th / tr show the English post (build_site.blog_code)
SITE_TAGS = ["en", "ko", "ja", "zh-Hant", "es", "pt-BR", "fr", "de", "id", "th", "vi", "tr"]
ORIGINALS = ("en", "ko")
KST = dt.timezone(dt.timedelta(hours=9))
PER_PAGE = 10
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = set(LANGS) | set(SITE_TAGS) | {"feed", "page", "feed.xml", "journal"}
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
    """Validate one post folder (9 files). -> {lang: (meta, body)}. Raises BlogError listing every problem."""
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


def og_image(bs):
    return {"@type": "ImageObject", "url": bs.SITE + bs.asset(OG_IMAGE["path"]), "width": OG_IMAGE["width"], "height": OG_IMAGE["height"]}


def about_game(bs, t, lang, root_):
    """The game a post is about, for `BlogPosting.about` (platform = what is really out: iOS, same as the home page)."""
    return {"@type": "VideoGame", "name": t["name"], "alternateName": ["Iltonggi", "일통기", "一統記"],
            "genre": ["Strategy", "Turn-based strategy", "Historical"], "gamePlatform": "iOS", "applicationCategory": "Game",
            "url": bs.url(lang, "home", root_), "publisher": {"@id": "https://ipe.rest/#organization"}}


def body_size(body, lang):
    """-> (count, unit): CJK = characters without whitespace, others = words (SEO guide v1 conversion: 400 words ~ 800 chars, 300 words ~ 500 chars)."""
    if lang in ("ja", "zh", "ko"):
        return len(re.sub(r"\s", "", body)), "chars"
    return len(re.findall(r"\w+", body)), "words"


MIN_BODY = {"words": (400, 300), "chars": (800, 500)}  # (warn below, error below) - originals only


def body_errors(meta, body, lang):
    """Hard limit (Davy 2026-10-29): an original (en/ko) body below the error floor blocks the publish."""
    if lang not in ORIGINALS:
        return []
    n, unit = body_size(body, lang)
    return ["%s: body %d %s is below the minimum (%d)" % (lang, n, unit, MIN_BODY[unit][1])] if n < MIN_BODY[unit][1] else []


def warnings(meta, body, lang):
    """SEO guide v1 (P0-9, P1-3) soft limits -> [warning]; never blocks a publish (body below the error floor is body_errors)."""
    cjk = lang in ("ja", "zh", "ko")
    out = []
    if lang in ORIGINALS:
        n, unit = body_size(body, lang)
        if MIN_BODY[unit][1] <= n < MIN_BODY[unit][0]:
            out.append("%s: body %d %s is below the target (%d)" % (lang, n, unit, MIN_BODY[unit][0]))
    tl, dl = (40, 110) if cjk else (60, 160)
    if len(meta["title"]) > tl:
        out.append("%s: title %d chars > %d" % (lang, len(meta["title"]), tl))
    if len(meta["description"]) > dl:
        out.append("%s: description %d chars > %d" % (lang, len(meta["description"]), dl))
    return out


FAQ_H2 = re.compile(r"(?i)\bfaq\b|자주\s*묻는|よくある質問|常见问题|常見問題|preguntas frecuentes|perguntas frequentes|pertanyaan|вопросы и ответы|часто задаваемые|câu hỏi thường gặp|questions fréquentes|häufige fragen|häufig gestellte")
OG_IMAGE = {"path": "og-share.jpg", "width": 1200, "height": 630}


def split_h2(body):
    """-> [(h2 title | None, [block lines])]: the body cut at `## ` headings (None = text before the first one)."""
    secs, cur = [[None, []]], None
    for line in body.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            secs.append([m.group(1), []])
        else:
            secs[-1][1].append(line)
    return [(t, ls) for t, ls in secs]


def first_paragraph(body):
    for blk in re.split(r"\n\s*\n", body.strip()):
        blk = blk.strip()
        if blk and not blk.startswith(("#", "!", "-", ">")) and not re.match(r"^\d+\. ", blk):
            return blk
    return ""


def faq_pairs(body):
    """-> [(question, answer)] from a FAQ section: an `## FAQ`-like h2 with `### question` headings followed by the answer paragraph(s)."""
    pairs = []
    for title, lines in split_h2(body):
        if not title or not FAQ_H2.search(title):
            continue
        q, ans = None, []
        for line in lines + ["### "]:
            m = re.match(r"^### (.*?)\s*$", line)
            if m:
                if q and " ".join(a for a in ans if a.strip()):
                    pairs.append((q, "\n".join(ans).strip()))
                q, ans = (m.group(1) or None), []
            elif q is not None:
                ans.append(line)
    return pairs


def plain(md):
    """Inline markdown -> plain text (for JSON-LD answers)."""
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    t = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", t)
    return re.sub(r"\s+", " ", re.sub(r"^[-\d.]+\s+|^> ?", "", t, flags=re.M)).strip()


def geo_warnings(body, lang):
    """GEO structure checks (soft): summary-style first paragraph, H2 sections, FAQ. Originals only."""
    if lang not in ORIGINALS:
        return []
    out = []
    fp = first_paragraph(body)
    cjk = lang in ("ja", "zh", "ko")
    lo, hi = (40, 400) if cjk else (60, 600)
    if not fp:
        out.append("%s: geo: no opening paragraph before the first heading" % lang)
    elif not lo <= len(fp) <= hi:
        out.append("%s: geo: opening paragraph is %d chars (a 1-3 sentence summary of %d-%d reads best for AI answers)" % (lang, len(fp), lo, hi))
    h2 = [t for t, _ in split_h2(body) if t]
    if len(h2) < 2:
        out.append("%s: geo: only %d `##` sections (use 2+ question-like or topic headings)" % (lang, len(h2)))
    if not faq_pairs(body):
        out.append("%s: geo: no FAQ section (`## FAQ` + `### question`) - optional, adds FAQPage JSON-LD" % lang)
    return out


def ui_all():
    return json.loads((BLOG / "ui.json").read_text(encoding="utf-8"))


def list_path(n):
    """The journal list (canonical). /journal/ is the one list address; the old /blog/ list pages stay as noindex copies whose canonical is the journal (legacy_list_path)."""
    return "/journal/" if n == 1 else "/journal/page/%d/" % n


def legacy_list_path(n):
    return "/blog/" if n == 1 else "/blog/page/%d/" % n


def post_path(slug):
    return "/blog/%s/" % slug


def time_tag(iso):
    return '<time datetime="%s" data-ipe-time>%s KST</time>' % (iso, iso[:10] + " " + iso[11:16])


def localtime_script():
    return "<script>" + kit_localtime.source().strip() + "</script>\n"


def build(bs, data, root=ROOT):
    """-> (files {relpath: text}, sitemap_extra [(page key, lastmod, changefreq, priority)]). `bs` = the build_site module."""
    UI = ui_all()
    posts = load_posts(root)
    pages = max(1, -(-len(posts) // PER_PAGE))
    files, extra = {}, []
    entries = [("en", True)] + [(l, False) for l in bs.LANGS]

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
        t, ui = data[lang], UI[bs.blog_code(lang)]
        pre = bs.prefix(lang, root_)
        for n in range(1, pages + 1):
            chunk = posts[(n - 1) * PER_PAGE:n * PER_PAGE]
            files[rel(lang, root_, list_path(n))] = list_page(bs, t, ui, lang, root_, pre, chunk, n, pages, bool(posts))
            files[rel(lang, root_, legacy_list_path(n))] = list_page(bs, t, ui, lang, root_, pre, chunk, n, pages, bool(posts), legacy=True)
        for p in posts:
            files[rel(lang, root_, post_path(p["slug"]))] = post_page(bs, data, t, ui, lang, root_, pre, p, posts)
    files["blog/feed.xml"] = feed(posts)
    files["blog/atom.xml"] = atom(posts)
    files["llms.txt"] = llms_txt(bs, data, UI, posts)
    return files, extra


def feed_link(ui, lang):
    return ('<link rel="alternate" type="application/rss+xml" title="%s (RSS)" href="/blog/feed.xml">\n'
            '<link rel="alternate" type="application/atom+xml" title="%s (Atom)" href="/blog/atom.xml">\n' % (esc(ui["title"]), esc(ui["title"])))


def list_page(bs, t, ui, lang, root_, pre, chunk, n, pages, has_posts, legacy=False):
    """legacy=True: the old /blog/ list address - same content, but canonical -> /journal/, noindex (one SEO page, no duplicate)."""
    key = "blog:p%d" % n
    title = "%s — %s" % (ui["nav"], t["name"]) if n == 1 else "%s · %s %d — %s" % (ui["nav"], ui["page"], n, t["name"])
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Blog", "name": ui["title"], "description": ui["lead"], "inLanguage": lang,
        "url": bs.url(lang, key, root_), "publisher": org(bs),
        "blogPost": [{"@type": "BlogPosting", "headline": p["files"][bs.blog_code(lang)][0]["title"], "url": bs.url(lang, "blog:" + p["slug"], root_),
                      "datePublished": p["published"].isoformat(timespec="seconds"), "dateModified": p["modified"].isoformat(timespec="seconds")}
                     for p in chunk],
    }, ensure_ascii=False)
    extra = feed_link(ui, lang) + '<script type="application/ld+json">%s</script>\n' % ld
    if n > 1:
        extra = '<link rel="prev" href="%s">\n' % bs.url(lang, "blog:p%d" % (n - 1), root_) + extra
    if n < pages:
        extra = '<link rel="next" href="%s">\n' % bs.url(lang, "blog:p%d" % (n + 1), root_) + extra
    cards = ""
    for p in chunk:
        m = p["files"][bs.blog_code(lang)][0]
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
        newer = '<a rel="prev" href="%s%s">%s %s</a>' % (pre, list_path(n - 1), bs.back_arrow(lang), esc(ui["newer"])) if n > 1 else ""
        older = '<a rel="next" href="%s%s">%s %s</a>' % (pre, list_path(n + 1), esc(ui["older"]), bs.next_arrow(lang)) if n < pages else ""
        pager = '      <nav class="pager" aria-label="%s">%s<span class="pager__now">%d / %d</span>%s</nav>\n' % (
            esc(ui["page"]), newer, n, pages, older)
    out = (bs.head(t, lang, key, root_, title, ui["lead"], extra, robots="noindex,follow") if legacy else bs.head(t, lang, key, root_, title, ui["lead"], extra)) + bs.header(t, lang, root_)
    out += f'''<main id="content">
  <section class="doc">
    <div class="container doc__body">
      <p class="kicker">// journal</p>
      <h1>{esc(ui['title'])}</h1>
      <p class="lead">{esc(ui['lead'])}</p>
      <div class="post-list">
{cards}      </div>
{pager}      <div class="doc__links"><a href="{pre}/">{bs.back_arrow(lang)} {esc(t['back_home'])}</a></div>
    </div>
  </section>
</main>
'''
    return out + (localtime_script() if chunk else "") + bs.footer(t, lang, key, root_) + "</body>\n</html>\n"


def post_page(bs, data, t, ui, lang, root_, pre, p, posts_all):
    key = "blog:" + p["slug"]
    meta, body = p["files"][bs.blog_code(lang)]
    iso = p["published"].isoformat(timespec="seconds")
    modified = p["modified"].isoformat(timespec="seconds")
    can = bs.url(lang, key, root_)
    content_lang = bs.blog_code(lang)
    n_words, _unit = body_size(body, content_lang)
    posting = {
        "@context": "https://schema.org", "@type": "BlogPosting", "@id": can + "#post", "headline": meta["title"], "description": meta["description"],
        "datePublished": iso, "dateModified": modified, "inLanguage": content_lang, "url": can,
        "mainEntityOfPage": {"@type": "WebPage", "@id": can},
        "image": [og_image(bs)], "author": {"@type": "Organization", "@id": "https://ipe.rest/#organization", "name": "ipe()", "url": "https://ipe.rest/"},
        "publisher": org(bs), "isPartOf": {"@type": "Blog", "name": ui["title"], "url": bs.url(lang, "blog:p1", root_)},
        "about": about_game(bs, t, lang, root_), "articleSection": ui["nav"], "wordCount": n_words,
    }
    ld = json.dumps(posting, ensure_ascii=False)
    faq = faq_pairs(body)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": content_lang, "mainEntityOfPage": {"@id": can},
                         "mainEntity": [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                                        for q, a in faq]}, ensure_ascii=False) if faq else ""
    crumbs = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": t["name"], "item": bs.url(lang, "home", root_)},
        {"@type": "ListItem", "position": 2, "name": ui["nav"], "item": bs.url(lang, "blog:p1", root_)},
        {"@type": "ListItem", "position": 3, "name": meta["title"], "item": can}]}, ensure_ascii=False)
    extra = (feed_link(ui, lang)
             + '<meta property="article:published_time" content="%s">\n' % iso
             + '<meta property="article:modified_time" content="%s">\n' % modified
             + '<script type="application/ld+json">%s</script>\n' % ld
             + '<script type="application/ld+json">%s</script>\n' % crumbs
             + ('<script type="application/ld+json">%s</script>\n' % faq_ld if faq_ld else ""))
    ai = ""
    if meta.get("translation_of"):
        o = meta["translation_of"]
        orig = bs.url(o, key, False)
        ai = '      <p class="meta ai-note">%s <a href="%s" hreflang="%s">%s</a></p>\n' % (
            esc(ui["ai_note"]), orig.replace(bs.SITE, ""), o, esc(ui["ai_orig"]))
    out = bs.head(t, lang, key, root_, "%s — %s" % (meta["title"], t["name"]), meta["description"], extra)
    out = out.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    out = re.sub(r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="%s">' % esc(meta["title"]), out, count=1)
    out = out.replace('<meta name="twitter:image" content=', '<meta name="twitter:image:alt" content="%s">\n<meta name="twitter:image" content=' % esc(meta["title"]), 1)
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
{more_links(bs, p, posts_all, lang, pre, ui)}      <div class="doc__links"><a href="{pre}{list_path(1)}">{bs.back_arrow(lang)} {esc(ui['back'])}</a></div>
    </div>
  </article>
</main>
'''
    return out + localtime_script() + bs.footer(t, lang, key, root_) + "</body>\n</html>\n"


def more_links(bs, p, posts_all, lang, pre, ui):
    """Previous/next (by publish order) + up to 3 more recent posts of the same language (SEO guide P1-1)."""
    i = posts_all.index(p)  # newest first
    newer = posts_all[i - 1] if i > 0 else None
    older = posts_all[i + 1] if i + 1 < len(posts_all) else None

    def a(q):
        return '<a href="%s%s">%s</a>' % (pre, post_path(q["slug"]), esc(q["files"][bs.blog_code(lang)][0]["title"]))
    pn = ""
    if older:
        pn += '<li>%s %s: %s</li>' % (bs.back_arrow(lang), esc(ui["prev_post"]), a(older))
    if newer:
        pn += '<li>%s %s: %s</li>' % (esc(ui["next_post"]), bs.next_arrow(lang), a(newer))
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
             "> A Three Kingdoms strategy game for iOS by ipe Studio, in %d languages. This site has the game page and a making-of blog (one short note a day)." % len(bs.LANGS), "",
             "## Pages", "- [Home](%s/): what the game is" % bs.SITE,
             "- [Support](%s/support/)" % bs.SITE, "- [Privacy](%s/privacy/)" % bs.SITE, "- [Terms](%s/terms/)" % bs.SITE, "",
             "## Journal (every post exists in %s)" % ", ".join(LANGS), "- [Journal index](%s/journal/)" % bs.SITE]
    lines.append("- [RSS feed](%s/blog/feed.xml)" % bs.SITE)
    lines.append("- [Atom feed](%s/blog/atom.xml)" % bs.SITE)
    if posts:
        for q in posts:
            m = q["files"]["en"][0]
            lines.append("- [%s](%s/blog/%s/): %s" % (m["title"], bs.SITE, q["slug"], m["description"]))
    return "\n".join(lines) + "\n"


def _last_modified(posts):
    return max(p["modified"] for p in posts) if posts else dt.datetime(2026, 10, 30, tzinfo=KST)


def feed(posts):
    site = "https://iltonggi.ipe.rest"
    items = ""
    for p in posts[:20]:
        m = p["files"]["en"][0]
        pub = p["published"].strftime("%a, %d %b %Y %H:%M:%S +0900")
        items += ("  <item>\n    <title>%s</title>\n    <link>%s/blog/%s/</link>\n    <guid isPermaLink=\"true\">%s/blog/%s/</guid>\n"
                  "    <pubDate>%s</pubDate>\n    <dc:creator>ipe Studio</dc:creator>\n    <description>%s</description>\n  </item>\n") % (
            esc(m["title"]), site, p["slug"], site, p["slug"], pub, esc(m["description"]))
    last = _last_modified(posts).strftime("%a, %d %b %Y %H:%M:%S +0900")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">\n<channel>\n  <title>Making of Iltonggi</title>\n'
            '  <link>%s/journal/</link>\n  <atom:link href="%s/blog/feed.xml" rel="self" type="application/rss+xml"/>\n'
            '  <description>How Iltonggi is being made — one short note a day.</description>\n'
            '  <language>en</language>\n  <lastBuildDate>%s</lastBuildDate>\n%s</channel>\n</rss>\n' % (site, site, last, items))


def atom(posts):
    site = "https://iltonggi.ipe.rest"
    entries = ""
    for p in posts[:20]:
        m = p["files"]["en"][0]
        entries += ('  <entry>\n    <title>%s</title>\n    <link href="%s/blog/%s/"/>\n    <id>%s/blog/%s/</id>\n'
                    '    <published>%s</published>\n    <updated>%s</updated>\n    <author><name>ipe Studio</name></author>\n    <summary>%s</summary>\n  </entry>\n') % (
            esc(m["title"]), site, p["slug"], site, p["slug"], p["published"].isoformat(timespec="seconds"),
            p["modified"].isoformat(timespec="seconds"), esc(m["description"]))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">\n  <title>Making of Iltonggi</title>\n'
            '  <link href="%s/journal/"/>\n  <link rel="self" type="application/atom+xml" href="%s/blog/atom.xml"/>\n  <id>%s/journal/</id>\n'
            '  <updated>%s</updated>\n  <subtitle>How Iltonggi is being made — one short note a day.</subtitle>\n%s</feed>\n' % (
                site, site, site, _last_modified(posts).isoformat(timespec="seconds"), entries))


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
                    for w in warnings(meta, body, lang) + geo_warnings(body, lang):
                        print("  warn %s" % w)
            except BlogError as ex:
                bad += 1
                print("BAD %s/%s: %s" % (kind, d.name, ex))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
