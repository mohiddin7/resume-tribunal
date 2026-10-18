"""Builds the website. Run from the repo root.

  python3 docs/build.py         drawings, blog pages, blog index, homepage, example run pages, feed.xml, sitemap.xml
  python3 docs/build.py media   also renders og.png, apple-touch-icon.png, a GIF of every blog figure
                                (for Medium and LinkedIn, which take GIFs but not SVGs) and the README's
                                How it works GIFs; needs Chrome, agent-browser and Pillow

Edit docs/blog/*.md, docs/art.py and the text in this file; never the generated HTML. Blog posts take
front matter (title, description, date, tags) and two shortcodes on their own line:
  [[figure:name|Caption]]   one of the drawings in art.FIGURES
  [[cta]]                   a box inviting the reader to try Resume Tribunal
  [[how]]                   the How it works player: waits for the reader at their steps, plays the AI steps itself
Example run pages come from examples/*/run.json (see examples/tools/README.md). docs/llms.txt is written by hand. The blog needs the markdown package (pip install markdown).
The site address is never typed in: set SITE_URL, or put a custom domain in docs/CNAME, or it is the
GitHub Pages address of the origin remote. Each build writes it into README.md, llms.txt and robots.txt.
"""
import datetime
import html
import json
import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import art  # noqa: E402

DOCS = pathlib.Path("docs")


def addresses():
    """The site and repository addresses, never hard-coded: SITE_URL if set, else the custom domain in
    docs/CNAME, else the GitHub Pages address of the origin remote."""
    remote = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout
    owner, repo = re.search(r"github\.com[:/]([^/]+)/(.+?)(?:\.git)?\s*$", remote).groups()
    pages = f"https://{owner.lower()}.github.io/{repo}/"
    cname = (DOCS / "CNAME").read_text().strip() if (DOCS / "CNAME").exists() else ""
    site = os.environ.get("SITE_URL") or (f"https://{cname}/" if cname else pages)
    return site.rstrip("/") + "/", f"https://github.com/{owner}/{repo}", pages


SITE, REPO, PAGES = addresses()
ZIP = f"{REPO}/releases/latest/download/resume-tribunal.zip"

# warmhop tracked links. links.json maps each landing place to its warmhop link; every placement adds
# ?ref=<where the link sits> plus UTM tags, so one link counts each spot apart. Until a key has its link, the plain
# address is used. Never for canonical, og:url, the sitemap, the feed, JSON-LD, llms.txt or resume-tribunal.md:
# search engines and AI apps need those direct.
LINKS = json.loads(pathlib.Path("links.json").read_text())


def track(key, ref, source="site", medium="referral"):
    from urllib.parse import urlencode
    to, wh = LINKS[key]["to"], LINKS[key]["warmhop"]
    if not wh:
        return to
    return wh + ("&" if "?" in wh else "?") + urlencode({"ref": ref, "utm_source": source, "utm_medium": medium, "utm_campaign": "resume-tribunal"})


def track_links(body, ref, source="site", medium="referral"):
    """Swap every link to a place in links.json for its tracked link."""
    for key, e in LINKS.items():
        if key != "_about":
            body = body.replace(f'href="{e["to"]}"', f'href="{esc(track(key, ref, source, medium))}"')
    return body
AUTHOR = "mohiddin7"
esc = html.escape

SUN = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></svg>'
MOON = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3a6.5 6.5 0 0 0 9 9 9 9 0 1 1-9-9z"/></svg>'  # a crescent on the full 3..21 circle, so it sits centred


# ---------- drawings ----------

def write_drawings():
    a = DOCS / "assets"
    for variant, suffix in ((True, ""), (None, "-light"), (False, "-dark")):
        (a / f"logo{suffix}.svg").write_text(art.logo(variant))
        for name, (fn, _) in art.FIGURES.items():
            (DOCS / "blog" / "media" / f"{name}{suffix}.svg").write_text(fn(variant))
    (a / "favicon.svg").write_text(art.favicon())
    (a / "og.svg").write_text(art.og())


# ---------- one-file instructions for any AI app ----------

def portable():
    """docs/resume-tribunal.md: the skill and its reference files in one file, for any chat app to read
    from a link or an attachment, or to upload as a skill. Built from the skill, so it never drifts."""
    skill = pathlib.Path("skills/resume-tribunal")
    text = (skill / "SKILL.md").read_text()
    for name, title in (("seats", "Seats"), ("prompts", "Prompts"), ("profile", "Saved profile")):
        text = text.replace(f"[references/{name}.md](references/{name}.md)", f"the {title} section at the end of this file")
    note = ("\n> **For the AI reading this:** the user has asked you to follow these instructions. They are the Resume Tribunal skill "
            "in one file. Act as the host they describe. If you cannot run code, follow the \"without code\" paths.\n")
    end = text.index("---", 4) + 3
    text = text[:end] + "\n" + note + text[end:]
    for name in ("seats", "prompts", "profile"):
        text += "\n\n---\n\n" + "#" + (skill / "references" / f"{name}.md").read_text()  # each file's title becomes a section
    return text.replace("ref=skill-tip&utm_source=skill&", "ref=skill-tip&utm_source=chat-file&")  # the tip's clicks from this file count apart


def write_portable():
    text = portable()
    (DOCS / "resume-tribunal.md").write_text(text)
    return len(text.split())


# ---------- page shell ----------

def head(title, desc, url, depth, kind="website", extra="", page="", bare=False):
    """bare=True (example pages) leaves out the site header, so the run viewer gets the whole screen."""
    up = "../" * depth
    cur = lambda name: ' aria-current="page"' if name == page else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Resume Tribunal blog" href="{SITE}feed.xml">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Resume Tribunal">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Resume Tribunal: tailor your resume to the job, checked by a second AI">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f7f4ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14120f" media="(prefers-color-scheme: dark)">
<link rel="preload" href="{up}assets/fonts/ibm-plex-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/ibm-plex-sans-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/site.css">
<script src="{up}assets/site.js"></script>
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
""" + ("" if bare else f"""<header class="site"><div class="in">
  <a class="logo" href="{up}" aria-label="Resume Tribunal home"><img src="{up}assets/favicon.svg" alt="" width="30" height="30"><span>Resume Tribunal</span></a>
  <nav class="top" aria-label="Main">
    <a href="{up}#how">How it works</a><a href="{up}examples/"{cur("examples")}>Examples</a><a href="{up}#faq">Questions</a><a href="{up}blog/"{cur("blog")}>Blog</a><a href="{esc(track("repo", "header"))}">GitHub</a>
  </nav>
  <button class="icon theme" type="button" aria-label="Switch to dark mode"><span class="moon">{MOON}</span><span class="sun">{SUN}</span></button>
  <a class="btn primary small" href="{up}#start">Get started</a>
</div></header>
""")


def foot(depth, bare=False):
    up = "../" * depth
    if bare:
        return "</body>\n</html>\n"
    return f"""<footer class="site"><div class="in">
  <div class="fbrand"><img src="{up}assets/favicon.svg" alt="" width="26" height="26"><strong>Resume Tribunal</strong><span>Free and open source. MIT license.</span></div>
  <nav aria-label="Footer"><a href="mailto:tribunal@warmhop.com">Support: tribunal@warmhop.com</a><a href="{up}#start">Get started</a><a href="{up}#faq">Questions</a><a href="{up}examples/">Examples</a><a href="{up}blog/">Blog</a><a href="{esc(track("repo", "footer"))}">GitHub</a></nav>
</div></footer>
</body>
</html>
"""


# ---------- blog ----------

def changed(*paths):
    """The day these files last changed: today while any has uncommitted edits, else the last commit's date."""
    if subprocess.run(["git", "status", "--porcelain", "--", *paths], capture_output=True, text=True).stdout.strip():
        return datetime.date.today().isoformat()
    return subprocess.run(["git", "log", "-1", "--format=%cs", "--", *paths], capture_output=True, text=True).stdout.strip()


def posts():
    import markdown  # only the blog needs it
    out = []
    for md in sorted((DOCS / "blog").glob("*.md")):
        front, body = md.read_text().split("---\n", 2)[1:]
        meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
        meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        words = len(re.sub(r"\[\[.*?\]\]", "", body).split())
        plain = re.sub(r"\[\[[^\]]*\]\]|[#*>|`_\[\]()-]", " ", body)
        plain = re.sub(r"https?://\S+", " ", plain)
        out.append(dict(slug=md.stem, md=body, words=words, modified=max(changed(str(md)), meta["date"]), minutes=max(1, round(words / 230)),
                        plain=" ".join(plain.lower().split()), **meta))
    for p in out:
        md = markdown.Markdown(extensions=["tables", "toc"])
        p["html"] = render_post_body(md.convert(p["md"]), p)
        p["toc"] = [(t["id"], html.unescape(t["name"])) for t in md.toc_tokens]
    return sorted(out, key=lambda p: p["date"], reverse=True)


def figure(name, caption):
    src = f"media/{name}"
    return (f'<figure class="fig"><img src="{src}.svg" data-light="{src}-light.svg" data-dark="{src}-dark.svg" '
            f'width="720" height="405" loading="lazy" alt="{esc(caption)}"><figcaption>{esc(caption)}</figcaption></figure>')


CTA = ('<aside class="cta-box"><img src="../assets/favicon.svg" alt="" width="40" height="40"><div>'
       '<strong>Try Resume Tribunal on your own resume.</strong><p>Free, no sign-up. Your AI writes it from your facts, a different AI checks it, and you approve each change.</p>'
       '<a class="btn primary" href="../#start">Get started in 2 minutes</a></div></aside>')


def render_post_body(body, p):
    body = re.sub(r"<p>\[\[figure:([\w-]+)\|(.+?)\]\]</p>", lambda m: figure(m.group(1), html.unescape(m.group(2))), body)
    body = body.replace("<p>[[cta]]</p>", CTA)
    body = body.replace("<p>[[how]]</p>", hiw(play=True) + '<p class="center meta hint">Your turn at steps 1 and 5. The AIs do the rest.</p>')
    body = body.replace("<p>[[tldr]]</p>", '<aside class="tldr"><strong>The short version</strong>').replace("<p>[[/tldr]]</p>", "</aside>")
    body = body.replace("<table>", '<div class="table"><table>').replace("</table>", "</table></div>")
    return re.sub(r"<tr>\s*<td>(.*?)</td>", r'<tr>\n<th scope="row">\1</th>', body)  # the first cell names the row


def tags(p, cls="tag"):
    return "".join(f'<span class="{cls}">{esc(t)}</span>' for t in p["tags"])


def share(slug, title):
    """Share buttons; each shares the post's own tracked link, so a click from LinkedIn or X counts apart."""
    from urllib.parse import quote
    key, t = f"post:{slug}", quote(title, safe="")
    u = lambda ref, src: quote(track(key, ref, src, "social"), safe="")
    return (f'<div class="share"><span>Share</span>'
            f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={u("share-linkedin", "linkedin")}" rel="noopener">LinkedIn</a>'
            f'<a href="https://twitter.com/intent/tweet?url={u("share-x", "x")}&amp;text={t}" rel="noopener">X</a>'
            f'<button type="button" class="copy" data-copy="{esc(track(key, "share-copy", "copy", "social"))}">Copy link</button></div>')


def build_blog(items):
    for p in items:
        url = f"{SITE}blog/{p['slug']}.html"
        day = datetime.date.fromisoformat(p["date"])
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"],
             "dateModified": p["modified"], "keywords": p["tags"], "wordCount": p["words"], "image": f"{SITE}assets/og.png",
             "author": {"@type": "Person", "name": AUTHOR, "url": "https://github.com/mohiddin7"},
             "publisher": {"@type": "Organization", "name": "Resume Tribunal", "logo": f"{SITE}assets/apple-touch-icon.png"},
             "mainEntityOfPage": url},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]}
        extra = (f'<meta property="article:published_time" content="{p["date"]}">\n'
                 + "".join(f'<meta property="article:tag" content="{esc(t)}">\n' for t in p["tags"])
                 + f'<script type="application/ld+json">{json.dumps(ld)}</script>\n')
        others = [o for o in items if o["slug"] != p["slug"]]
        related = "".join(f'<a class="card post" href="{o["slug"]}.html"><span class="tags">{tags(o)}</span><strong>{esc(o["title"])}</strong>'
                          f'<p>{esc(o["description"])}</p><span class="meta">{o["minutes"]} min read</span><span class="more" aria-hidden="true">Read the post →</span></a>' for o in others)
        page = (head(p["title"], p["description"], url, 1, "article", extra, page="blog")
                + f'''<div class="readbar" aria-hidden="true"><b></b></div>
<main id="main" class="post-wrap">
<div class="post-grid">
<nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>{"".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in p["toc"])}</ol></nav>
<div class="post-col">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <a href="./">Blog</a></nav>
<article class="post">
<header class="post-head"><div class="tags">{tags(p)}</div>
<h1>{esc(p["title"])}</h1><p class="lede">{esc(p["description"])}</p>
<div class="byline"><span class="avatar" aria-hidden="true">{AUTHOR[0].upper()}</span><span><strong>{AUTHOR}</strong><br><span class="meta">{day:%d %B %Y} · {p["minutes"]} min read</span></span>{share(p["slug"], p["title"])}</div></header>
<div class="prose">{track_links(p["html"], "blog-" + p["slug"])}</div>
{CTA}
<footer class="post-foot">{share(p["slug"], p["title"])}</footer>
</article>
</div>
</div>
{f'<section class="related"><h2>Keep reading</h2><div class="grid">{related}</div></section>' if related else ""}
</main>
''' + foot(1))
        (DOCS / "blog" / f"{p['slug']}.html").write_text(page)

    all_tags = sorted({t for p in items for t in p["tags"]})
    chips = '<button type="button" class="chip on" data-tag="">All</button>' + "".join(
        f'<button type="button" class="chip" data-tag="{esc(t)}">{esc(t)}</button>' for t in all_tags)
    cards = "\n".join(
        f'<article class="card post" data-tags="{esc("|".join(p["tags"]))}" '
        f'data-text="{esc((p["title"] + " " + p["description"] + " " + " ".join(p["tags"]) + " " + p["plain"]).lower())}">'
        f'<span class="tags">{"".join(f'<button type="button" class="tag" data-tag="{esc(t)}" aria-label="Show posts about {esc(t)}">{esc(t)}</button>' for t in p["tags"])}</span>'
        f'<a class="stretch" href="{p["slug"]}.html"><strong>{esc(p["title"])}</strong></a><span class="desc">{esc(p["description"])}</span>'
        f'<span class="meta">{datetime.date.fromisoformat(p["date"]):%d %b %Y} · {p["minutes"]} min read</span><span class="more" aria-hidden="true">Read the post →</span></article>'
        for p in items)
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Resume Tribunal blog", "url": f"{SITE}blog/",
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}blog/{p['slug']}.html", "datePublished": p["date"]} for p in items]}
    desc = "How to tailor your resume or CV to a job with ChatGPT, Claude or Gemini without inventing anything, and how AI resume tools compare."
    (DOCS / "blog" / "index.html").write_text(
        head("Blog: Tailoring Your Resume with AI | Resume Tribunal", desc, f"{SITE}blog/", 1, "website",
             f'<script type="application/ld+json">{json.dumps(ld)}</script>\n', page="blog")
        + f'''<main id="main" class="blog-wrap">
<header class="blog-head"><h1>Blog</h1></header>
<div class="blog-tools">
<label class="search"><span class="sr">Search posts</span><input type="search" id="q" placeholder="Search posts, e.g. ATS or ChatGPT" autocomplete="off" aria-describedby="count"></label>
<div class="chips" role="group" aria-label="Filter by topic">{chips}</div>
<p class="meta" id="count" aria-live="polite">{len(items)} posts</p>
</div>
<div class="grid posts" id="posts">
{cards}
</div>
<p class="empty" id="empty" hidden>No posts match that search.</p>
</main>
''' + foot(1))

    rss = "\n".join(f"<item><title>{esc(p['title'])}</title><link>{SITE}blog/{p['slug']}.html</link>"
                    f"<guid>{SITE}blog/{p['slug']}.html</guid>"
                    f"<pubDate>{datetime.date.fromisoformat(p['date']):%a, %d %b %Y} 00:00:00 +0000</pubDate>"
                    + "".join(f"<category>{esc(t)}</category>" for t in p["tags"])
                    + f"<description>{esc(p['description'])}</description></item>" for p in items)
    (DOCS / "feed.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Resume Tribunal blog</title>'
        f"<link>{SITE}blog/</link><description>{esc(desc)}</description>\n{rss}\n</channel></rss>\n")
    site = changed("docs/build.py", "docs/art.py", "docs/assets")
    runs = example_runs()
    urls = ([("", max(site, *(p["modified"] for p in items))), ("blog/", max(site, *(p["modified"] for p in items))),
             ("llms.txt", changed("docs/llms.txt")), ("resume-tribunal.md", changed("skills/resume-tribunal"))]
            + [(f"blog/{p['slug']}.html", max(site, p["modified"])) for p in items]
            + ([("examples/", max(site, changed("examples")))] + [(f"examples/{r['slug']}/", max(site, changed(f"examples/{r['slug']}"))) for r in runs] if runs else []))
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{day}</lastmod></url>\n" for u, day in urls) + "</urlset>\n")


# ---------- example runs ----------

EXAMPLES = pathlib.Path("examples")


def example_runs():
    """Every recorded example (examples/<slug>/run.json, written by examples/tools/export.py), council runs first."""
    runs = [json.loads(p.read_text()) for p in sorted(EXAMPLES.glob("*/run.json"))]
    return sorted(runs, key=lambda r: (r["mode"] != "Full council", r["title"]))


def json_script(id_, data):
    """Data for a page's script, safe inside <script>: '</' can never close the tag."""
    body = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/json" id="{id_}">{body}</script>'


VIEWER = """<main id="main" class="rv">
<div class="rv-app">
  <div class="rv-bar closed" id="rv-bar"><div class="in">
    <div class="rv-top">
      <a class="rv-home" href="../../" aria-label="Resume Tribunal home"><img src="../../assets/favicon.svg" alt="" width="26" height="26"></a>
      <a class="rv-back" href="../">All examples</a>
      <div class="rv-top-r">
        <label class="sr" for="example">Watch another example</label>
        <select id="example"></select>
        <button type="button" class="rv-ghost" id="details-toggle" aria-expanded="false" aria-controls="rv-details">Show details</button>
        <button class="icon theme" type="button" aria-label="Switch to dark mode"><span class="moon">{moon}</span><span class="sun">{sun}</span></button>
      </div>
    </div>
    <h1>{title}{note}</h1>
    <div class="rv-details" id="rv-details"><div class="rv-facts">{facts}</div></div>
  </div></div>
  <div class="rv-time" id="timeline" aria-label="Who worked when"><div>
    <div class="rv-ctrl">
      <button type="button" class="rv-play" id="play"><svg viewBox="0 0 16 16" aria-hidden="true" id="play-icon"><path d="M3 1.5v13l11-6.5z"/></svg><span id="play-label">Play the run</span></button>
      <span class="tl"><span id="clock"></span> / {length}</span>
      <input type="range" class="rv-scrub" id="scrub" min="0" step="1" aria-label="Time in the run">
      <button type="button" class="rv-ghost" id="lanes-toggle" aria-expanded="true">Hide timeline</button>
      <div class="rv-settings">
        <button type="button" class="rv-ghost" id="settings-btn" aria-expanded="false" aria-controls="settings">Settings</button>
        <div class="rv-pop" id="settings" hidden>
          <label class="rv-check"><input type="checkbox" id="autoplay" checked> Play the run when the page opens</label>
          <label class="rv-check"><input type="checkbox" id="follow" checked> Follow along: open the tab where each new message lands</label>
          <label class="rv-small">Speed <select id="speed"><option value="0.5">Slow</option><option value="1" selected>Normal</option><option value="2">Fast</option><option value="4">Fastest</option></select></label>
          <p class="rv-keys">Space bar plays and pauses. Arrow keys step through messages.</p>
        </div>
      </div>
    </div>
    <div class="rv-lanes-wrap"><div class="rv-lanes" id="lanes"></div></div>
  </div></div>
  <div class="rv-panes" id="panes" data-show="chat">
    <div class="rv-pane rv-pane-resume" role="region" aria-label="Resume">
      <div class="rv-pane-h">
        <h2>Resume</h2>
        <div class="seg mob-tabs" role="group" aria-label="Show"><button type="button" data-show="resume" aria-pressed="true">Resume</button><button type="button" data-show="chat" aria-pressed="false">Chat</button></div>
        <div class="seg" role="group" aria-label="Version"><button type="button" data-v="before" aria-pressed="false">Before</button><button type="button" data-v="after" aria-pressed="true">After</button></div>
        <label class="rv-check"><input type="checkbox" id="diff" checked> Show changes</label>
        <div class="seg zoom" role="group" aria-label="Page size"><button type="button" data-z="width" aria-pressed="false">Fit width</button><button type="button" data-z="page" aria-pressed="true">Whole page</button></div>
      </div>
      <div class="rv-scroll desk" id="resume-scroll">
        <div class="cutbar" id="cutbar" hidden></div>
        <div class="paper" id="paper"><div class="sheet" id="sheet"></div></div>
        <div class="key" id="key"></div>
      </div>
    </div>
    <button type="button" class="rv-divider" id="divider" role="separator" aria-orientation="vertical" aria-label="Resize the two panes" aria-valuemin="25" aria-valuemax="75" aria-valuenow="50"></button>
    <div class="rv-pane rv-pane-chat" role="region" aria-label="The run">
      <div class="rv-pane-h">
        <h2>The run</h2>
        <div class="seg mob-tabs" role="group" aria-label="Show"><button type="button" data-show="resume" aria-pressed="false">Resume</button><button type="button" data-show="chat" aria-pressed="true">Chat</button></div>
      </div>
      <div class="ctabs" role="tablist" aria-label="Conversations" id="ctabs"></div>
      <div class="rv-scroll" id="chat-scroll" role="tabpanel"><div class="feed" id="feed" aria-live="polite"></div></div>
    </div>
  </div>
</div>
</main>
"""


def build_examples():
    """docs/examples/: one page per recorded run, with its prompts and replies, and an index of them all."""
    runs = example_runs()
    out = DOCS / "examples"
    if out.exists():
        import shutil
        shutil.rmtree(out)
    if not runs:
        return []
    css = '<link rel="stylesheet" href="{up}assets/viewer.css">\n'
    listing = [{"slug": r["slug"], "title": r["title"], "mode": r["mode"]} for r in runs]
    for r in runs:
        page = out / r["slug"]
        (page / "files").mkdir(parents=True)
        for f in (EXAMPLES / r["slug"] / "files").glob("*"):
            (page / "files" / f.name).write_text(f.read_text())
        who = "a real, de-identified resume shared with consent" if r["facts"][0].startswith("Real resume") else "a fictional candidate"
        desc = f"Recorded Resume Tribunal run ({r['mode'].lower()}, {round(r['end'] / 60)} min) on {who}: every prompt, reply and resume change."
        url = f"{SITE}examples/{r['slug']}/"
        crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Example runs", "item": f"{SITE}examples/"},
            {"@type": "ListItem", "position": 3, "name": r["title"], "item": url}]}
        facts = "".join(f'<span class="rv-fact">{esc(f)}</span>' for f in r["facts"])
        (page / "index.html").write_text(
            head(f"{r['title']} | Resume Tribunal", desc, url, 2, "website",
                 css.format(up="../../") + f'<script type="application/ld+json">{json.dumps(crumbs)}</script>\n', page="examples", bare=True).replace("<body>", '<body class="wide bare">')
            + VIEWER.format(moon=MOON, sun=SUN, title=esc(r["title"]), facts=facts, note=(f' <span class="rv-info" tabindex="0" aria-label="How this run was recorded" aria-describedby="rv-tip">i<span class="rv-tip" role="tooltip" id="rv-tip">'
                      f'<b>How this run was recorded.</b> {esc(r["note"])}</span></span>') if r.get("note") else "", length=f"{r['end'] // 60:02d}:{r['end'] % 60:02d}")
            + json_script("run-data", r) + "\n" + json_script("examples-data", listing)
            + '\n<script src="../../assets/viewer.js"></script>\n' + foot(2, bare=True))
    cards = "\n".join(
        f'<a class="card post" href="{r["slug"]}/" target="_blank" rel="noopener" data-kind="{esc(r["mode"])}|{esc(r.get("reach", "Auto"))} mode">'
        f'<span class="tags"><span class="tag">{esc(r["mode"])}</span><span class="tag">{esc(r.get("reach", "Auto"))} mode</span></span>'
        f'<strong>{esc(r["title"])}</strong><span class="facts">{"".join(f"<span>{esc(f)}</span>" for f in r["facts"] if not f.startswith(("Auto mode:", "Manual mode:")))}</span>'
        f'<span class="more" aria-hidden="true">Watch the run →</span><span class="sr"> (opens in a new tab)</span></a>' for r in runs)
    kinds = ["Quick review", "Full council", "Auto mode", "Manual mode"]
    chips = '<button type="button" class="chip on" data-kind="" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" class="chip" data-kind="{k}" aria-pressed="false">{k}</button>' for k in kinds
        if any(k in (r["mode"], r.get("reach", "Auto") + " mode") for r in runs))
    desc = "Watch Resume Tribunal work on real and fictional resumes, message by message: what each AI was asked, what it answered, and how each line of the resume changed."
    (out / "index.html").write_text(
        head("Example runs | Resume Tribunal", desc, f"{SITE}examples/", 1, "website", css.format(up="../"), page="examples")
        + f'''<main id="main" class="blog-wrap ex-wrap">
<header class="ex-head"><h1>Example runs</h1><p class="meta">{esc(desc)} Each page plays back the run's recorded files.</p></header>
<div class="chips ex-chips" role="group" aria-label="Show">{chips}</div>
<div class="grid posts" id="ex-cards">
{cards}
</div>
</main>
<script>
document.querySelector(".ex-chips").addEventListener("click", function (e) {{
  var b = e.target.closest(".chip"); if (!b) return;
  document.querySelectorAll(".ex-chips .chip").forEach(function (c) {{ c.classList.toggle("on", c === b); c.setAttribute("aria-pressed", c === b); }});
  document.querySelectorAll("#ex-cards .card").forEach(function (c) {{ c.hidden = !!b.dataset.kind && c.dataset.kind.split("|").indexOf(b.dataset.kind) < 0; }});
}});
</script>
''' + foot(1))
    return [r["slug"] for r in runs]


# ---------- homepage ----------

FAQ = [
    ("Is Resume Tribunal actually free?",
     "Yes. Resume Tribunal costs nothing and there's no sign-up. It runs inside AI apps you may already use, like Claude and ChatGPT. Their free plans are enough for a quick review. The thorough version sends more messages, so it runs more smoothly on a paid plan."),
    ("I'm not a tech person. Can I still use Resume Tribunal?",
     "Yes. You paste one message into any AI chat app, like ChatGPT, Gemini or Claude, attach your resume, and answer a couple of questions. There are no commands to type."),
    ("Why can't I just ask ChatGPT to fix my resume?",
     "You can, and ChatGPT is fine for a quick tidy-up. The catch is that an AI checking its own writing tends to approve it, made-up numbers included. Resume Tribunal has a second AI, from a different company, check the draft without knowing who wrote it. A script then flags any number it can't find in what you said."),
    ("Will Resume Tribunal make stuff up on my resume?",
     "It is built not to. Every number, tool and job title has to come from you; a script flags any it cannot find in your words, and the second AI checks each line against them. If something is missing, Resume Tribunal asks you instead of guessing. You approve each changed line before you get the file."),
    ("Will my resume get past the ATS robots?",
     "Nobody can honestly promise that. ATS is the software employers use to collect applications, and most of it sorts candidates. It rarely rejects anyone on its own. Resume Tribunal keeps your layout simple enough for that software to read, and checks the PDF's text before you send it. After that, a person reads it."),
    ("Can a recruiter tell that AI wrote my resume?",
     "Resume Tribunal removes the usual giveaways, like long dashes and words such as \"spearheaded\", and keeps your own wording. It can't make the resume your unaided work, though. If an employer asks about AI use, be honest."),
    ("Who gets to see my resume?",
     "Not us. Resume Tribunal has no server. Before anything goes to a second AI, your name, email, phone number and links are swapped for stand-ins like <<NAME>>, and you're asked first. The AI apps you use see the rest under their own terms."),
    ("How long does Resume Tribunal take?",
     "About 2 minutes of your time for a quick review: you answer a few questions and approve the changes, and the AIs do the rest on their own. In the eight recorded example runs, a quick review took 6 to 37 minutes from start to finish, most under 15, and a full council 27 to 37. If you copy and paste between two apps yourself, add a few minutes."),
    ("What do I get at the end?",
     "Your finished resume as a PDF or Word file when your app can make files, and always as text you can paste into Word or Google Docs. You also get a list of what the job asks for that your resume doesn't show yet, plus the interview questions your resume is likely to prompt."),
    ("Does Resume Tribunal work with Word files, or on my phone?",
     "Word files are fine: attach your .docx as it is. Phones work too, but copying text between two apps is easier on a laptop."),
    ("Something went wrong. Who do I tell?",
     "Email tribunal@warmhop.com with what happened and which AI app you used. Leave your resume out unless we ask. You can also open an issue on GitHub."),
    ("What's warmhop™?",
     "A link tracker for resumes, made by the same person who made Resume Tribunal. If your resume has links, you'll see one optional tip about it at the end. You don't need it, and nothing is sent to it."),
]

HIW = [  # title, one short line
    ("Drop in the job and your resume", "Paste the link into any AI chat."),
    ("Your AI rewrites it for the job", "Using only your facts."),
    ("A second AI checks it like a hiring manager", "It looks for anything made up."),
    ("A script checks the details", "Layout, AI phrases, numbers."),
    ("You check the changes", "Say yes to the ones you want."),
    ("Ready to send", "With the questions you're likely to get."),
]
RC_HEAD = '<span class="rc-name"></span><span class="rc-sub"></span>'
SCENES = [
 # 1: the job link and the resume drop into a chat box
 '''<div class="sc sc1"><div class="chat"><span class="typed">Tailor my resume to this job</span><span class="send">↑</span></div>
  <div class="pill job"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>Job link</div>
  <div class="rc rc-in">''' + RC_HEAD + '''<i></i><i></i><i class="short"></i></div></div>''',
 # 2: AI 1 rewrites two lines, and slips in "4 hours"
 '''<div class="sc sc2"><div class="rc big"><span class="sctag t-blue">AI 1</span>''' + RC_HEAD + '''
  <p class="old">Helped improve on-time delivery</p>
  <p class="new n1">Helped raise on-time delivery from 81 to 93 percent</p>
  <p class="new n2">Cut report prep from 4 hours to 40 minutes</p></div>
  <span class="kw k1">Excel</span><span class="kw k2">Power Query</span><span class="kw k3">Carrier data</span></div>''',
 # 3: AI 2 reads blind, catches "4 hours", says it would shortlist
 '''<div class="sc sc3"><div class="rc big"><span class="sctag t-swap"><b>AI 1</b><b>Draft K</b></span>''' + RC_HEAD + '''
  <p>Helped raise on-time delivery from 81 to 93 percent</p>
  <p class="catch">Cut report prep from <span class="bad">4 hours</span><span class="fix">half a day</span> to 40 minutes</p>
  <span class="lens"></span></div>
  <span class="note">You said "half a day"</span><span class="verdict">Would shortlist: yes</span></div>''',
 # 4: a script ticks three checks
 '''<div class="sc sc4"><div class="rc">''' + RC_HEAD + '''<i></i><i></i><i class="short"></i><span class="scan"></span></div>
  <ul class="checks"><li class="c1"><b>✓</b>Screening software can read it</li><li class="c2"><b>✓</b>No AI-sounding phrases</li><li class="c3"><b>✓</b>Numbers match your words</li></ul></div>''',
 # 5: you approve two changes
 '''<div class="sc sc5"><div class="chg ch1"><p>"from 81 to 93 percent"</p><span class="ok">Approve</span></div>
  <div class="chg ch2"><p>"from half a day to 40 minutes"</p><span class="ok">Approve</span></div><span class="tap"></span></div>''',
 # 6: your resume lifts out of the pile, like the logo
 '''<div class="sc sc6"><div class="pile"><span class="p1"></span><span class="p2"></span><div class="rc lift">''' + RC_HEAD + '''<i></i><i></i><i class="short"></i></div></div>
  <span class="pill pdf">Resume.pdf</span><span class="pill qs">5 interview questions</span></div>''',
]


def hiw(play=False):
    """The How it works story player. play=True (the blog) waits for the reader at their two steps
    and runs the AI steps by itself; the homepage version plays straight through."""
    steps6 = "".join(f'<li role="presentation"><button role="tab" class="st" data-i="{n}" aria-selected="{"true" if n == 0 else "false"}">'
                     f'<span class="bar"><b></b></span><span class="stt">{esc(t)}</span><span class="sts">{esc(d)}</span></button></li>'
                     for n, (t, d) in enumerate(HIW))
    scenes = [sc.replace('class="sc ', f'data-t="{esc(HIW[n][0])}" data-d="{esc(HIW[n][1])}" class="sc ' + ("on " if n == 0 else ""), 1)
              for n, sc in enumerate(SCENES)]
    who = ""
    if play:  # the reader's turns: scene 1 (send the job and resume) and scene 5 (approve the changes)
        who = '<span class="who" aria-hidden="true"></span>'
        scenes[0] = scenes[0].replace('class="sc ', 'data-wait class="sc ', 1).replace(
            "</div></div>", '</div><button type="button" class="btn primary act">Paste the job and your resume</button></div>', 1)
        scenes[4] = scenes[4].replace('class="sc ', 'data-wait class="sc ', 1).replace(
            '<span class="ok">Approve</span>', '<button type="button" class="ok">Approve</button>')
        scenes[5] = scenes[5].rsplit("</div>", 1)[0] + '<button type="button" class="btn ghost act again">Watch again</button></div>'
        # A pretend pointer that shows where to click. It can't click anything; it loops until the reader does.
        scenes[-1] += ('\n<svg class="gcur" aria-hidden="true" viewBox="0 0 24 24" width="30" height="30">'
                       '<path d="M4 2l15 11.5-6.6 1 4 7.6-3 1.5-4-7.7L4 20z" fill="#fff" stroke="#14120f" stroke-width="1.6" stroke-linejoin="round"/></svg>')
    return f'''<div class="hiw{" play" if play else ""}" aria-roledescription="carousel" aria-label="How Resume Tribunal works">
    <ol class="steps6" role="tablist">{steps6}</ol>
    <div class="stage" tabindex="0" aria-live="polite">
      <button class="icon pause" type="button" aria-label="Pause" aria-pressed="false"><span class="ps">❚❚</span><span class="pl">▶</span></button>{who}
{chr(10).join(scenes)}
    </div>
    <p class="cap"><strong></strong><span></span></p>
  </div>'''


TITLE = "Free AI Resume Tailor for Any Job Description | Resume Tribunal"
DESC = "Not getting shortlisted? Tailor your resume or CV to the job in 2 minutes of your time with ChatGPT, Gemini or Claude. A second AI checks it. Free."


def thumb(p):
    """The post's first drawing, theme-aware like the figures in the post."""
    m = re.search(r'<img src="(media/[\w-]+)\.svg"', p["html"])
    if not m:
        return ""
    src = "blog/" + m.group(1)
    return f'<img class="thumb" src="{src}.svg" data-light="{src}-light.svg" data-dark="{src}-dark.svg" width="720" height="405" loading="lazy" alt="">'


FEATURED = "growth-analyst-pricing-council"  # a fictional candidate, three companies' AIs, auto mode


def showcase():
    """The homepage's examples section: one recorded run's "who worked when" chart, drawn from its run.json,
    with a playhead that sweeps across once when the section comes into view."""
    runs = {r["slug"]: r for r in example_runs()}
    r = runs.get(FEATURED)
    if not r:
        return ""
    pct = lambda t: f"{t / r['end'] * 100:.2f}%"
    rows = ["user", "host"] + [k for k in r["who"] if k not in ("user", "host")]
    steps = "".join(f'<span style="left:{pct(st["t"])}">{esc(st["name"])}</span>' for st in r["steps"])
    lanes = ""
    for k in rows:
        bars = "".join(f'<i style="left:{pct(a)};width:{pct(max(b - a, r["end"] / 300))};--d:{a / r["end"] * 4.4:.2f}s"{" class=w" if wait else ""}>{esc(label) if (b - a) / r["end"] * 480 >= len(label) * 6.8 + 12 else ""}</i>'
                       for who, a, b, label, wait, _ in r["lanes"] if who == k)
        lanes += f'<span class="ml-name">{esc(r["who"][k]["n"])}</span><span class="ml-track ml-{k}">{bars}</span>'
    facts = "".join(f"<span>{esc(f)}</span>" for f in r["facts"] if not f.startswith(("Auto mode:", "Manual mode:")))
    return f'''<section id="examples" class="split">
  <div class="sh">
    <h2>Watch three AIs work on one resume</h2>
    <p class="sub">Eight recorded runs on real and fictional resumes. You see every prompt each AI got, every reply, and the resume before and after.</p>
    <div class="cta"><a class="btn primary" href="examples/{r["slug"]}/" target="_blank" rel="noopener">Watch this run<span class="sr"> (opens in a new tab)</span></a><a class="btn ghost" href="examples/">See all eight</a></div>
  </div>
  <a class="card runcard" href="examples/{r["slug"]}/" target="_blank" rel="noopener">
    <strong>{esc(r["title"])}</strong>
    <span class="facts">{facts}</span>
    <span class="ml" aria-hidden="true"><span></span><span class="ml-steps">{steps}</span>{lanes}<span class="ml-head"></span></span>
    <span class="meta">Who worked when, from the run's own record. Each bar is a draft, a critique, a review or a wait for {esc(r["candidate"])}.</span><span class="sr"> (opens in a new tab)</span>
  </a>
</section>'''


def build_home(items):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": "Resume Tribunal", "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any", "url": SITE, "sameAs": REPO, "license": "https://opensource.org/licenses/MIT",
         "softwareVersion": "1.0.0", "image": f"{SITE}assets/og.png", "publisher": {"@type": "Organization", "name": "Resume Tribunal", "email": "tribunal@warmhop.com", "url": SITE}, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": "A free, open-source Agent Skill that tailors a resume or CV to a job using only the candidate's own facts. "
                        "A second AI from a different company checks every draft blind, a script flags numbers and names it cannot find in the "
                        "candidate's own words, and the candidate approves each change."},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    faq = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    blog = "\n".join(f'<a class="card post pic" href="blog/{p["slug"]}.html">{thumb(p)}<span class="tags">{tags(p)}</span><strong>{esc(p["title"])}</strong>'
                     f'<span class="desc">{esc(p["description"])}</span><span class="meta">{p["minutes"]} min read</span></a>' for p in items)
    agent_msg = "Install the Resume Tribunal skill (npx skills add mohiddin7/resume-tribunal), then tailor my resume to this job: [paste the job link]"
    chat_msg = f"Read {SITE}resume-tribunal.md and follow it to tailor my resume to this job: [paste the job link]"
    body = f"""<main id="main">
<section class="hero">
  <h1>Not getting shortlisted?<br><span class="accent">Fix your resume in <span class="nb">2 minutes</span> of your time.</span></h1>
  <p class="lede">Paste the job link into any AI chat. It tailors your resume from your own facts, then a second AI checks it.</p>
  <div class="cta"><a class="btn primary big" href="#start">Get started free</a><a class="btn ghost big" href="#proof">See what it caught</a></div>
  <ul class="trust"><li>No sign-up</li><li>Open source</li><li>Works with any AI app</li></ul>
</section>

<section id="how">
  <div class="sh">
    <h2>How it works</h2>
    <p class="sub">You paste the job and your resume, then check the changes. That takes about 2 minutes of your time, and the AIs do the rest.</p>
  </div>
  {hiw()}
  <p class="meta hint">Tap to skip. Hold to pause.</p>
  <p class="meta">In a full council, up to three AIs from different companies each write a draft and critique the others' drafts before they are merged.</p>
</section>

<section id="proof" class="split">
  <div class="sh">
    <h2>What the second AI caught</h2>
    <p class="sub">One role from a full run on a made-up candidate: the resume before and after, and what the review sent back.</p>
    <p class="meta"><a href="examples/">Watch eight recorded runs</a>, every message and prompt included.</p>
  </div>
  <div class="proof-body">
  <div class="ba">
    <div class="card"><span class="label">Before</span><ul><li>Helped improve on-time delivery</li><li>Utilized Excel for various reports</li></ul></div>
    <div class="card after"><span class="label">After</span><ul><li>Traced one carrier's late Dayton terminal loads to its Friday pickups in six months of Excel data; after the team moved them to another carrier, on-time delivery there went from 81% to 93% over about three months.</li>
      <li>Built the Monday late-delivery report in pivot tables and Power Query; it took half a day, now about 40 minutes.</li></ul></div>
  </div>
  <ul class="card caughtlist">
    <li><span class="was">"driving the rerouting decision"</span><span class="is">The candidate wrote "we moved those loads". Now: "after the team moved them".</span></li>
    <li><span class="was">"Carrier management"</span><span class="is">The posting's phrase. The candidate never said they manage carriers.</span></li>
    <li><span class="was">Dropping "simple" from "simple SQL queries"</span><span class="is">It's the candidate's own word, so it stays.</span></li>
  </ul>
  </div>
</section>

{showcase()}

<section id="start" class="split">
  <div class="sh">
    <h2>Pick where you use AI</h2>
    <p class="sub">Works with any AI app and any model. No account with us.</p>
    <div class="tabs" role="tablist" aria-label="Where you use AI">
      <button role="tab" aria-selected="true" aria-controls="t-chat" id="b-chat">AI chat app</button>
      <button role="tab" aria-selected="false" aria-controls="t-agent" id="b-agent">Coding agent</button>
      <button role="tab" aria-selected="false" aria-controls="t-other" id="b-other">Not sure</button>
    </div>
    <div class="note"><strong>The only manual part:</strong> if no second AI is connected, Resume Tribunal gives you one block of text to paste into a different AI app, and you paste the reply back.</div>
  </div>
  <div class="start-body">
  <div class="panels">
  <div class="panel" role="tabpanel" id="t-chat" aria-labelledby="b-chat">
    <p class="apps">ChatGPT, Gemini, Claude, Perplexity, Grok, Copilot, DeepSeek, Le Chat</p>
    <ol class="steps">
      <li>Open a new chat and attach your resume.</li>
      <li>Paste this message, with your job link at the end:
        <div class="copybox"><code>{esc(chat_msg).replace("/", "/<wbr>").replace(".md", "<wbr>.md")}</code><button type="button" class="copy" data-copy="{esc(chat_msg)}">Copy</button></div></li>
      <li>Answer a couple of questions. A quick review takes about 2 minutes of your time.</li>
    </ol>
    <p class="meta">If your app can't open links, <a href="resume-tribunal.md" download>download the instructions</a> and attach them too.</p>
  </div>
  <div class="panel" role="tabpanel" id="t-agent" aria-labelledby="b-agent" hidden>
    <p class="apps">Claude Code, Codex, Antigravity, Gemini CLI, Cursor, GitHub Copilot, Grok Build, OpenCode</p>
    <ol class="steps">
      <li>Send your agent this message. It asks your permission, installs Resume Tribunal, and starts:
        <div class="copybox"><code>{esc(agent_msg)}</code><button type="button" class="copy" data-copy="{esc(agent_msg)}">Copy</button></div></li>
      <li>Point it at your resume file when it asks.</li>
    </ol>
    <p class="meta">With two or more of these signed in on your computer, the second and third AIs run by themselves.</p>
  </div>
  <div class="panel" role="tabpanel" id="t-other" aria-labelledby="b-other" hidden>
    <p>Any AI that can read a file works, on a laptop or a phone.</p>
    <ol class="steps">
      <li><a class="btn primary small" href="resume-tribunal.md" download>Download the instructions</a></li>
      <li>In any AI chat, attach that file and your resume, then say <strong>"Follow this file to tailor my resume to this job:"</strong> and paste the job link.</li>
      <li>Answer a couple of questions. A quick review takes about 2 minutes of your time.</li>
    </ol>
  </div>
  </div>
  <details class="more"><summary>Save it as a skill, so you never paste the link again</summary>
      <p>Most apps now take skills. Download <a href="{esc(track("zip", "home-start"))}">resume-tribunal.zip</a> once and upload it:</p>
      <ul>
        <li><strong>Gemini:</strong> Settings, Skills, Upload (personal accounts, 18 and over).</li>
        <li><strong>Claude:</strong> Customize, Skills, +, Upload a skill. On Pro or Max you can skip the download: Customize, Plugins, Add marketplace, then <code>mohiddin7/resume-tribunal</code>.</li>
        <li><strong>ChatGPT, Grok, Perplexity:</strong> look for Skills in your settings. Which plans have it varies.</li>
      </ul>
      <p class="meta">Checked October 2026 against each app's help pages. Menus change.</p>
    </details>
  </div>
</section>

<section id="why">
  <div class="sh wide">
    <h2>Why a second AI checks the first</h2>
    <p class="sub">In the studies below, AIs went easy on their own work,<br class="desk"> and a checker from a different model family did better.</p>
  </div>
  <div class="grid three stats">
    <div class="card stat"><span class="big">50%+</span><p>more likely, in some tests, to pass a failed answer when an AI judges its own work.</p><a href="https://arxiv.org/abs/2604.06996">Study, 2026 (preprint)</a></div>
    <div class="card stat"><span class="big">37</span><p>models tested. A checker from a different model family beat self-checking.</p><a href="https://arxiv.org/abs/2512.02304">Study, 2026</a></div>
    <div class="card stat"><span class="big">2.5 to 5.4</span><p>false details per resume when AI rewrote resumes with no safeguards.</p><a href="https://arxiv.org/abs/2607.01457">Study, 2026 (preprint)</a></div>
  </div>
  <div class="split why-compare">
    <div class="table"><table>
      <tr><th></th><th>ChatGPT alone</th><th>Resume Tribunal</th></tr>
      <tr><th scope="row">Who checks it</th><td>The AI that wrote it</td><td><strong>A different company's AI, blind</strong></td></tr>
      <tr><th scope="row">Made-up numbers</th><td>Easy to miss</td><td><strong>Checked against your words</strong></td></tr>
      <tr><th scope="row">Your say</th><td>If you read closely</td><td><strong>You check each change</strong></td></tr>
      <tr><th scope="row">Your name and email</th><td>Sent as they are</td><td><strong>Hidden from the second AI</strong></td></tr>
    </table></div>
    <p class="meta limits"><strong>What the studies don't show.</strong> Those studies used maths, logic and test resumes, and no study shows several AIs write a better resume than one. See <a href="blog/resume-skills-compared.html">how six resume skills compare</a>, including where Resume Tribunal loses.</p>
  </div>
</section>

<section id="faq" class="split">
  <div class="sh">
    <h2>Things people ask</h2>
    <p class="sub">Not here? Email <a href="mailto:tribunal@warmhop.com">tribunal@warmhop.com</a> or open an issue on <a href="{esc(track("issues", "home-faq"))}">GitHub</a>.</p>
  </div>
  <div class="faq">{faq}</div>
</section>

<section id="blog">
  <div class="sh"><h2>Read more</h2><p class="sub">What I learned building Resume Tribunal, and how it compares with other AI resume tools.</p></div>
  <div class="grid two">{blog}</div>
</section>

<section class="final">
  <h2>Get a second opinion on your next application</h2>
  <p>Free and open source. You approve every change before you get the file.</p>
  <a class="btn primary big" href="#start">Get started free</a>
</section>
</main>
<a class="mcta btn primary" href="#start">Get started free</a>
"""
    extra = (f'<link rel="alternate" type="text/plain" href="llms.txt" title="Summary for AI assistants">\n'
             f'<script type="application/ld+json">{json.dumps(ld)}</script>\n')
    (DOCS / "index.html").write_text(head(TITLE, DESC, SITE, 0, "website", extra).replace("<body>", '<body class="home">') + body + foot(0))


# ---------- media (PNG and GIF) ----------

def media():
    """og.png, apple-touch-icon.png, one GIF per blog figure, and the homepage's How it works player as GIFs
    for the README, rendered in a real browser."""
    import glob
    import os
    import subprocess
    import tempfile
    from PIL import Image
    chrome = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome")))[-1]
    shot = lambda src, out, w, h: subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                                                  f"--window-size={w},{h}", f"--screenshot={out}", f"file://{src.resolve()}"],
                                                 capture_output=True)
    shot(DOCS / "assets" / "og.svg", DOCS / "assets" / "og.png", 1200, 630)
    with tempfile.TemporaryDirectory() as d:
        icon = pathlib.Path(d) / "icon.html"
        icon.write_text(f'<body style="margin:0"><img src="file://{(DOCS / "assets" / "favicon.svg").resolve()}" width="180" height="180" style="display:block"></body>')
        shot(icon, DOCS / "assets" / "apple-touch-icon.png", 180, 180)
        ab = lambda *args: subprocess.run(["agent-browser", *args], capture_output=True, text=True)
        for name, (_, cycle) in art.FIGURES.items():
            ab("open", f"file://{(DOCS / 'blog' / 'media' / f'{name}-light.svg').resolve()}")
            ab("set", "viewport", "720", "405")
            frames, step = [], 0.2
            for i in range(int(cycle / step)):
                t = int(i * step * 1000)
                ab("eval", f"document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {t}; }})")
                f = pathlib.Path(d) / f"{name}-{i:03}.png"
                ab("screenshot", str(f))
                frames.append(Image.open(f).convert("RGB").resize((720, 405)))
            frames[0].save(DOCS / "blog" / "media" / f"{name}.gif", save_all=True, append_images=frames[1:],
                           duration=int(step * 1000), loop=0, optimize=True)
            print("gif:", name, len(frames), "frames")
        # The README's How it works: the homepage player, frame by frame, in light and dark.
        ab("open", f"file://{(DOCS / 'index.html').resolve()}")
        ab("set", "viewport", "1040", "800")
        for theme in ("light", "dark"):
            js = (f'document.documentElement.dataset.theme = "{theme}"; document.documentElement.style.scrollBehavior = "auto";'
                  'document.querySelector(".hiw .pause").style.visibility = "hidden";'
                  'document.querySelector(".hiw").scrollIntoView({block: "center"});'
                  'var r = document.querySelector(".hiw").getBoundingClientRect(); JSON.stringify([r.left, r.top, r.right, r.bottom])')
            box = [round(v) for v in json.loads(json.loads(ab("eval", js).stdout.strip().splitlines()[-1]))]
            frames = []
            for n in range(len(HIW)):
                for i in range(22):  # 22 frames of 200 ms: the player's 4.4 s per step, stopping short of the step's end
                    click = f'document.querySelectorAll(".hiw .st")[{n}].click();' if i == 0 else ""
                    ab("eval", click + f"document.getAnimations().forEach(a => {{ a.pause(); a.currentTime = {i * 200}; }})")
                    f = pathlib.Path(d) / f"hiw-{theme}-{n}-{i:02}.png"
                    ab("screenshot", str(f))
                    frames.append(Image.open(f).convert("RGB").crop(box))
            frames[0].save(DOCS / "assets" / f"how-it-works-{theme}.gif", save_all=True, append_images=frames[1:],
                           duration=200, loop=0, optimize=True)
            print("gif: how-it-works", theme, len(frames), "frames")
        ab("close")


# ---------- cross-posts (LinkedIn articles, Medium) ----------

def syndicate(items):
    """research/syndication/<slug>/: each post as plain HTML to open in a browser, copy and paste into LinkedIn's
    article editor or Medium's, with GIF figures (neither takes SVG), no tables (neither has them), the player as
    a list, and tracked links tagged with the platform. Local only: research/ is not published."""
    import markdown
    import shutil
    out = pathlib.Path("research/syndication")
    for p in items:
        d = out / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        for name in re.findall(r"\[\[figure:([\w-]+)\|", p["md"]):
            shutil.copy(DOCS / "blog" / "media" / f"{name}.gif", d / f"{name}.gif")
        shutil.copy(DOCS / "assets" / "og.png", d / "cover.png")
        for site in ("linkedin", "medium"):
            ref = lambda where: f"{site}-{p['slug']}-{where}"
            body = markdown.markdown(p["md"], extensions=["tables"])
            body = re.sub(r"<p>\[\[figure:([\w-]+)\|(.+?)\]\]</p>",
                          lambda m: f'<figure><img src="{SITE}blog/media/{m.group(1)}.gif" alt="{m.group(2)}"><figcaption>{m.group(2)}</figcaption></figure>', body)
            body = body.replace("<p>[[tldr]]</p>", "<p><strong>The short version</strong></p>").replace("<p>[[/tldr]]</p>", "")
            body = body.replace("<p>[[how]]</p>", "<ol>" + "".join(f"<li><strong>{esc(t)}.</strong> {esc(d_)}</li>" for t, d_ in HIW) + "</ol>")
            body = body.replace("<p>[[cta]]</p>", f'<p><strong>Try Resume Tribunal on your own resume.</strong> Free, no sign-up. Your AI writes it from your facts, '
                                f'a different AI checks it, and you approve each change. <a href="{esc(track("site", ref("cta"), site, "article"))}">Get started</a>.</p>')
            body = re.sub(r'<table>(.*?)</table>', lambda m: table_as_list(m.group(1)), body, flags=re.S)
            body = body.replace('href="../#start"', f'href="{esc(track("site", ref("text"), site, "article"))}"')
            body = track_links(body, ref("text"), site, "article")
            orig = esc(track(f"post:{p['slug']}", ref("footer"), site, "article"))
            page = (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                    f'<title>{esc(p["title"])} ({site})</title><style>body{{font:18px/1.6 Georgia,serif;max-width:44rem;margin:2rem auto;padding:0 16px}}'
                    f'.how{{font:14px/1.5 system-ui,sans-serif;background:#f3e6e6;padding:12px 16px;border-radius:8px}}img{{max-width:100%}}</style></head><body>\n'
                    f'<p class="how">{"Paste into a new LinkedIn article (Write article). Title and cover go in their own fields: upload cover.png from this folder. Select from the line under the title to the end, copy, paste. If a figure does not come through, upload its GIF from this folder." if site == "linkedin" else "Best: Medium, Import a story, paste " + LINKS[f"post:{p['slug']}"]["to"] + ", which links back to the original for search engines. Or select from the title to the end, copy, paste into a new story."}</p>\n'
                    f'<article><h1>{esc(p["title"])}</h1>\n<p><em>{esc(p["description"])}</em></p>\n{body}\n'
                    f'<p><em>First published on <a href="{orig}">the Resume Tribunal blog</a>.</em></p></article>\n</body></html>\n')
            (d / f"{site}.html").write_text(page)
    return out


def table_as_list(rows):
    """A table as a list: one item per row, '<first cell>: header, value; ...'."""
    head = [html.unescape(re.sub("<.*?>", "", h)).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", rows, re.S)]
    items = []
    for tr in re.findall(r"<tr>(.*?)</tr>", rows, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if cells:
            rest = "; ".join(f"{esc(h)}: {c.strip()}" for h, c in zip(head[1:], cells[1:]))
            items.append(f"<li><strong>{cells[0].strip()}</strong>. {rest}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def point_hand_written_files_at_site():
    """README.md, llms.txt and robots.txt are written by hand: once docs/CNAME names a custom domain, swap the
    GitHub Pages address in them for it. A SITE_URL override, such as a local preview, leaves them alone."""
    if os.environ.get("SITE_URL") or SITE == PAGES:
        return
    for path in (pathlib.Path("README.md"), DOCS / "llms.txt", DOCS / "robots.txt"):
        text = path.read_text()
        if PAGES in text:
            path.write_text(text.replace(PAGES, SITE))


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:  # read-only: the published one-file skill must match the skill it is built from
        LINKS["_test"] = {"to": "https://example.com/", "warmhop": "https://warmhop.example/l?id=1"}
        assert track("_test", "here") == "https://warmhop.example/l?id=1&ref=here&utm_source=site&utm_medium=referral&utm_campaign=resume-tribunal"
        assert 'href="https://warmhop.example/l?id=1&amp;ref=x&amp;' in track_links('<a href="https://example.com/">', "x")
        same = (DOCS / "resume-tribunal.md").read_text() == portable()
        print("docs/resume-tribunal.md matches the skill" if same else "docs/resume-tribunal.md is stale: run python3 docs/build.py")
        sys.exit(0 if same else 1)
    (DOCS / "blog" / "media").mkdir(parents=True, exist_ok=True)
    write_drawings()
    print("portable file:", write_portable(), "words")
    point_hand_written_files_at_site()
    items = posts()
    build_blog(items)
    build_home(items)
    shown = build_examples()
    print("built: drawings, blog (" + ", ".join(p["slug"] for p in items) + "), homepage, examples (" + ", ".join(shown) + "), feed, sitemap")
    if sys.argv[1:] == ["syndicate"]:
        print("cross-posts:", syndicate(items))
    if sys.argv[1:] == ["media"]:
        media()
