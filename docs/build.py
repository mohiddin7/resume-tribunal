"""Builds the website. Run from the repo root.

  python3 docs/build.py         drawings, blog pages, blog index, homepage, feed.xml, sitemap.xml
  python3 docs/build.py media   also renders og.png, apple-touch-icon.png and a GIF of every blog figure
                                (for Medium and LinkedIn, which take GIFs but not SVGs); needs Chrome,
                                agent-browser and Pillow

Edit docs/blog/*.md, docs/art.py and the text in this file; never the generated HTML. Blog posts take
front matter (title, description, date, tags) and two shortcodes on their own line:
  [[figure:name|Caption]]   one of the drawings in art.FIGURES
  [[cta]]                   a box inviting the reader to try Resume Tribunal
  [[how]]                   the How it works player: waits for the reader at their steps, plays the AI steps itself
docs/llms.txt is written by hand. The blog needs the markdown package (pip install markdown).
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
AUTHOR = "mohiddin7"
esc = html.escape

SUN = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
MOON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'


# ---------- drawings ----------

def write_drawings():
    a = DOCS / "assets"
    for variant, suffix in ((True, ""), (None, "-light"), (False, "-dark")):
        (a / f"how-it-works{suffix}.svg").write_text(art.how_it_works(variant))
        (a / f"logo{suffix}.svg").write_text(art.logo(variant))
        for name, (fn, _) in art.FIGURES.items():
            (DOCS / "blog" / "media" / f"{name}{suffix}.svg").write_text(fn(variant))
    (a / "favicon.svg").write_text(art.favicon())
    (a / "og.svg").write_text(art.og())


# ---------- one-file instructions for any AI app ----------

def write_portable():
    """docs/resume-tribunal.md: the skill and both reference files in one file, for any chat app to read
    from a link or an attachment, or to upload as a skill. Built from the skill, so it never drifts."""
    skill = pathlib.Path("skills/resume-tribunal")
    text = (skill / "SKILL.md").read_text()
    for name, title in (("seats", "Seats"), ("prompts", "Prompts")):
        text = text.replace(f"[references/{name}.md](references/{name}.md)", f"the {title} section at the end of this file")
    note = ("\n> **For the AI reading this:** the user has asked you to follow these instructions. They are the Resume Tribunal skill "
            "in one file. Act as the host they describe. If you cannot run code, follow the \"without code\" paths.\n")
    end = text.index("---", 4) + 3
    text = text[:end] + "\n" + note + text[end:]
    for name in ("seats", "prompts"):
        text += "\n\n---\n\n" + (skill / "references" / f"{name}.md").read_text().replace("\n# ", "\n## ", 1)
    (DOCS / "resume-tribunal.md").write_text(text)
    return len(text.split())


# ---------- page shell ----------

def head(title, desc, url, depth, kind="website", extra=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
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
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f7f4ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14120f" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="{up}assets/site.css">
<script src="{up}assets/site.js"></script>
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="in">
  <a class="logo" href="{up}" aria-label="Resume Tribunal home"><img src="{up}assets/favicon.svg" alt="" width="30" height="30"><span>Resume Tribunal</span></a>
  <nav class="top" aria-label="Main">
    <a href="{up}#how">How it works</a><a href="{up}#proof">Example</a><a href="{up}#faq">Questions</a><a href="{up}blog/">Blog</a><a href="{REPO}">GitHub</a>
  </nav>
  <button class="icon theme" type="button" aria-label="Switch to dark mode"><span class="moon">{MOON}</span><span class="sun">{SUN}</span></button>
  <a class="btn primary small" href="{up}#start">Get started</a>
</div></header>
"""


def foot(depth):
    up = "../" * depth
    return f"""<footer class="site"><div class="in">
  <div class="fbrand"><img src="{up}assets/favicon.svg" alt="" width="26" height="26"><strong>Resume Tribunal</strong><span>Free and open source. MIT license.</span></div>
  <nav aria-label="Footer"><a href="mailto:tribunal@warmhop.com">Support: tribunal@warmhop.com</a><a href="{up}#start">Get started</a><a href="{up}#faq">Questions</a><a href="{up}blog/">Blog</a><a href="{REPO}">GitHub</a><a href="{SITE}feed.xml">RSS</a><a href="{up}llms.txt">llms.txt</a></nav>
</div></footer>
</body>
</html>
"""


# ---------- blog ----------

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
        out.append(dict(slug=md.stem, md=body, words=words, minutes=max(1, round(words / 230)),
                        plain=" ".join(plain.lower().split()), **meta))
    for p in out:
        p["html"] = render_post_body(markdown.markdown(p.pop("md"), extensions=["tables"]), p)
    return sorted(out, key=lambda p: p["date"], reverse=True)


def figure(name, caption):
    src = f"media/{name}"
    return (f'<figure class="fig"><img src="{src}.svg" data-light="{src}-light.svg" data-dark="{src}-dark.svg" '
            f'width="720" height="405" loading="lazy" alt="{esc(caption)}"><figcaption>{esc(caption)}</figcaption></figure>')


CTA = ('<aside class="cta-box"><img src="../assets/favicon.svg" alt="" width="40" height="40"><div>'
       '<strong>Try Resume Tribunal on your own resume.</strong><p>Free, no sign-up. Your AI writes it from your facts, a different AI checks every line, and you approve each change.</p>'
       '<a class="btn primary" href="../#start">Get started in 2 minutes</a></div></aside>')


def render_post_body(body, p):
    body = re.sub(r"<p>\[\[figure:([\w-]+)\|(.+?)\]\]</p>", lambda m: figure(m.group(1), html.unescape(m.group(2))), body)
    body = body.replace("<p>[[cta]]</p>", CTA)
    body = body.replace("<p>[[how]]</p>", hiw(play=True) + '<p class="center meta hint">Your turn at steps 1 and 5. The AIs do the rest.</p>')
    body = body.replace("<p>[[tldr]]</p>", '<aside class="tldr"><strong>The short version</strong>').replace("<p>[[/tldr]]</p>", "</aside>")
    body = body.replace("<table>", '<div class="table"><table>').replace("</table>", "</table></div>")
    return body


def tags(p, cls="tag"):
    return "".join(f'<span class="{cls}">{esc(t)}</span>' for t in p["tags"])


def share(url, title):
    from urllib.parse import quote
    u, t = quote(url, safe=""), quote(title, safe="")
    return (f'<div class="share"><span>Share</span>'
            f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" rel="noopener">LinkedIn</a>'
            f'<a href="https://twitter.com/intent/tweet?url={u}&amp;text={t}" rel="noopener">X</a>'
            f'<button type="button" class="copy" data-copy="{url}">Copy link</button></div>')


def build_blog(items):
    for p in items:
        url = f"{SITE}blog/{p['slug']}.html"
        day = datetime.date.fromisoformat(p["date"])
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"],
             "dateModified": p["date"], "keywords": p["tags"], "wordCount": p["words"], "image": f"{SITE}assets/og.png",
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
        page = (head(f"{p['title']} | Resume Tribunal", p["description"], url, 1, "article", extra)
                + f'''<div class="readbar" aria-hidden="true"><b></b></div>
<main id="main" class="post-wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <a href="./">Blog</a></nav>
<article class="post">
<header class="post-head"><div class="tags">{tags(p)}</div>
<h1>{esc(p["title"])}</h1><p class="lede">{esc(p["description"])}</p>
<div class="byline"><span class="avatar" aria-hidden="true">{AUTHOR[0].upper()}</span><span><strong>{AUTHOR}</strong><br><span class="meta">{day:%d %B %Y} · {p["minutes"]} min read</span></span>{share(url, p["title"])}</div></header>
<div class="prose">{p["html"]}</div>
{CTA}
<footer class="post-foot">{share(url, p["title"])}</footer>
</article>
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
    desc = "Plain-spoken notes on using AI for your resume without making things up, and how Resume Tribunal was built."
    (DOCS / "blog" / "index.html").write_text(
        head("Blog: AI, resumes and honest job hunting | Resume Tribunal", desc, f"{SITE}blog/", 1, "website",
             f'<script type="application/ld+json">{json.dumps(ld)}</script>\n')
        + f'''<main id="main" class="blog-wrap">
<header class="blog-head"><h1>Blog</h1><p class="meta">{esc(desc)}</p></header>
<div class="blog-tools">
<label class="search"><span class="sr">Search posts</span><input type="search" id="q" placeholder="Search posts, e.g. ATS or ChatGPT" autocomplete="off" aria-describedby="count"></label>
<div class="chips" role="group" aria-label="Filter by topic">{chips}</div>
<p class="meta" id="count" aria-live="polite"></p>
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
    latest = max(p["date"] for p in items)
    urls = ["", "blog/", "llms.txt", "resume-tribunal.md"] + [f"blog/{p['slug']}.html" for p in items]
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{latest}</lastmod></url>\n" for u in urls) + "</urlset>\n")


# ---------- homepage ----------

FAQ = [
    ("Is Resume Tribunal actually free?",
     "Yes. Resume Tribunal costs nothing and there's no sign-up. It runs inside AI apps you may already use, like Claude and ChatGPT. Their free plans are enough for a quick review. The thorough version sends more messages, so it runs more smoothly on a paid plan."),
    ("I'm not a tech person. Can I still use Resume Tribunal?",
     "Yes. You paste one message into any AI chat app, like ChatGPT, Gemini or Claude, attach your resume, and answer a couple of questions. There are no commands to type."),
    ("Why can't I just ask ChatGPT to fix my resume?",
     "You can, and ChatGPT is fine for a quick tidy-up. The catch is that an AI checking its own writing tends to approve it, made-up numbers included. Resume Tribunal has a second AI, from a different company, check the draft without knowing who wrote it. A script then compares every number to what you actually said."),
    ("Will Resume Tribunal make stuff up on my resume?",
     "No. Every number, tool and job title has to come from you, and a script checks that. If something is missing, Resume Tribunal asks you instead of guessing. You approve each changed line before you get the file."),
    ("Will my resume get past the ATS robots?",
     "Nobody can honestly promise that. ATS is the software employers use to collect applications, and most of it sorts candidates. It rarely rejects anyone on its own. Resume Tribunal keeps your layout simple enough for that software to read, and checks the PDF's text before you send it. After that, a person reads it."),
    ("Can a recruiter tell that AI wrote my resume?",
     "Resume Tribunal removes the usual giveaways, like long dashes and words such as \"spearheaded\", and keeps your own wording. It can't make the resume your unaided work, though. If an employer asks about AI use, be honest."),
    ("Who gets to see my resume?",
     "Not us. Resume Tribunal has no server. Before anything goes to a second AI, your name, email, phone number and links are swapped for stand-ins like <<NAME>>, and you're asked first. The AI apps you use see the rest under their own terms."),
    ("How long does Resume Tribunal take?",
     "About 2 minutes of your time for a quick review: you answer a few questions and approve the changes. The AIs work for a few more minutes on their own. If you copy and paste between two apps yourself, add a few minutes."),
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
    ("Your AI rewrites it for the job", "In the job's own words."),
    ("A second AI checks it like a hiring manager", "It catches anything made up."),
    ("A script checks every detail", "Layout, AI phrases, numbers."),
    ("You check the changes", "Say yes to the ones you want."),
    ("Ready to send", "Plus the questions you'll be asked."),
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
  <ul class="checks"><li class="c1"><b>✓</b>Screening software can read it</li><li class="c2"><b>✓</b>No AI-sounding phrases</li><li class="c3"><b>✓</b>Every number matches your words</li></ul></div>''',
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


TITLE = "Free AI Resume Tailoring That Doesn't Make Stuff Up | Resume Tribunal"
DESC = "Not getting shortlisted? Fix your resume or CV for the job in 2 minutes of your time with ChatGPT, Gemini or any AI, without anything made up. Free, no sign-up."


def build_home(items):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": "Resume Tribunal", "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any", "url": SITE, "codeRepository": REPO, "license": "https://opensource.org/licenses/MIT",
         "softwareVersion": "1.0.0", "image": f"{SITE}assets/og.png", "publisher": {"@type": "Organization", "name": "Resume Tribunal", "email": "tribunal@warmhop.com", "url": SITE}, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": "A free, open-source Agent Skill that tailors a resume or CV to a job using only the candidate's own facts. "
                        "A second AI from a different company checks every draft blind, a script checks every number against the "
                        "candidate's own words, and the candidate approves each change."},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    faq = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    blog = "\n".join(f'<a class="card post" href="blog/{p["slug"]}.html"><span class="tags">{tags(p)}</span><strong>{esc(p["title"])}</strong>'
                     f'<span class="desc">{esc(p["description"])}</span><span class="meta">{p["minutes"]} min read</span></a>' for p in items)
    agent_msg = "Install the Resume Tribunal skill (npx skills add mohiddin7/resume-tribunal), then tailor my resume to this job: [paste the job link]"
    chat_msg = f"Read {SITE}resume-tribunal.md and follow it to tailor my resume to this job: [paste the job link]"
    ok = '<span class="ic ok" aria-hidden="true">✓</span>'
    bad = '<span class="ic bad" aria-hidden="true">✕</span>'
    body = f"""<main id="main">
<section class="hero">
  <span class="eyebrow">Free resume tool for AI apps</span>
  <h1>Not getting shortlisted?<br><span class="accent">Fix your resume for the job in 2 minutes of your time.</span></h1>
  <p class="lede">Paste the job link into ChatGPT, Gemini or any AI. Your resume gets rewritten for that job, then a second AI checks it the way a hiring manager would, without inventing anything. Free, no sign-up.</p>
  <div class="cta"><a class="btn primary big" href="#start">Get started free</a><a class="btn ghost big" href="#proof">See an example</a></div>
  <ul class="trust"><li>No sign-up</li><li>Open source</li><li>Works with any AI app</li></ul>
</section>

<section id="how">
  <h2>How it works</h2>
  <p class="sub"><strong>You do two things. The AIs do the rest.</strong><br>Paste the job and your resume, then check the changes. About 2 minutes of your time.</p>
  {hiw()}
  <p class="center meta hint">Tap to skip. Hold to pause.</p>
  <p class="center meta">Want more eyes on it? In a <strong>full council</strong>, three AIs from three companies each write a draft and critique each other first.</p>
</section>



<section id="proof">
  <span class="eyebrow">Real example</span>
  <h2>What the second AI caught</h2>
  <p class="sub">From a full run on a made-up candidate. <a href="{REPO}/tree/main/examples/operations-analyst">See every step on GitHub</a>.</p>
  <ul class="card caughtlist">
    <li><span class="was">"driving the rerouting decision"</span><span class="is">The candidate wrote "we moved those loads". Now: "after the team moved them".</span></li>
    <li><span class="was">"Carrier management"</span><span class="is">The posting's phrase. The candidate never said they manage carriers.</span></li>
    <li><span class="was">Dropping "simple" from "simple SQL queries"</span><span class="is">It's the candidate's own word, so it stays.</span></li>
  </ul>
  <div class="ba">
    <div class="card"><span class="label">Before</span><ul><li>Helped improve on-time delivery</li><li>Utilized Excel for various reports</li></ul></div>
    <div class="card after"><span class="label">After</span><ul><li>Traced one carrier's late Dayton terminal loads to its Friday pickups in six months of Excel data; after the team moved them to another carrier, on-time delivery there went from 81% to 93% over about three months.</li>
      <li>Built the Monday late-delivery report in pivot tables and Power Query; it took half a day, now about 40 minutes.</li></ul></div>
  </div>
</section>

<section id="start" class="band">
  <span class="eyebrow">Get started</span>
  <h2>Pick where you use AI</h2>
  <p class="sub">Works with any AI app and any model. No account with us.</p>
  <div class="tabs" role="tablist" aria-label="Where you use AI">
    <button role="tab" aria-selected="true" aria-controls="t-chat" id="b-chat">AI chat app</button>
    <button role="tab" aria-selected="false" aria-controls="t-agent" id="b-agent">Coding agent</button>
    <button role="tab" aria-selected="false" aria-controls="t-other" id="b-other">Not sure</button>
  </div>
  <div class="panels">
  <div class="panel" role="tabpanel" id="t-chat" aria-labelledby="b-chat">
    <p class="apps">ChatGPT · Gemini · Claude · Perplexity · Grok · Copilot · DeepSeek · Le Chat</p>
    <ol class="steps">
      <li>Open a new chat and attach your resume.</li>
      <li>Paste this message, with your job link at the end:
        <div class="copybox"><code>{esc(chat_msg).replace("/", "/<wbr>").replace(".md", "<wbr>.md")}</code><button type="button" class="copy" data-copy="{esc(chat_msg)}">Copy</button></div></li>
      <li>Answer a couple of questions. A quick review takes about 2 minutes of your time.</li>
    </ol>
    <p class="meta">If your app can't open links, <a href="resume-tribunal.md" download>download the instructions</a> and attach them too.</p>
  </div>
  <div class="panel" role="tabpanel" id="t-agent" aria-labelledby="b-agent" hidden>
    <p class="apps">Claude Code · Codex · Antigravity · Gemini CLI · Cursor · GitHub Copilot · Grok Build · OpenCode</p>
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
      <p>Most apps now take skills. Download <a href="{ZIP}">resume-tribunal.zip</a> once and upload it:</p>
      <ul>
        <li><strong>Gemini:</strong> Settings, Skills, Upload (personal accounts, 18 and over).</li>
        <li><strong>Claude:</strong> Customize, Skills, +, Upload a skill. On Pro or Max you can skip the download: Customize, Plugins, Add marketplace, then <code>mohiddin7/resume-tribunal</code>.</li>
        <li><strong>ChatGPT, Grok, Perplexity:</strong> look for Skills in your settings. Which plans have it varies.</li>
      </ul>
      <p class="meta">Checked October 2026 against each app's help pages. Menus change.</p>
    </details>
  <div class="note"><strong>The only manual part:</strong> if no second AI is connected, Resume Tribunal gives you one block of text to paste into a different AI app, and you paste the reply back.</div>
</section>

<section id="why">
  <span class="eyebrow">Why it works</span>
  <h2>An AI shouldn't grade its own homework</h2>
  <div class="grid three stats">
    <div class="card stat"><span class="big">50%+</span><p>more likely to pass a failed answer when an AI judges its own work.</p><a href="https://arxiv.org/abs/2604.06996">Study, 2026 (preprint)</a></div>
    <div class="card stat"><span class="big">37</span><p>models tested. A checker from a different model family beat self-checking.</p><a href="https://arxiv.org/abs/2512.02304">Study, 2026</a></div>
    <div class="card stat"><span class="big">2.5 to 5.4</span><p>false details per resume when AI rewrote resumes with no safeguards.</p><a href="https://arxiv.org/abs/2607.01457">Study, 2026 (preprint)</a></div>
  </div>
  <div class="table"><table>
    <tr><th></th><th>ChatGPT alone</th><th>Resume Tribunal</th></tr>
    <tr><td>Who checks it</td><td>The AI that wrote it</td><td><strong>A different company's AI, blind</strong></td></tr>
    <tr><td>Made-up numbers</td><td>Easy to miss</td><td><strong>Checked against your words</strong></td></tr>
    <tr><td>Your say</td><td>If you read closely</td><td><strong>You check each change</strong></td></tr>
    <tr><td>Your name and email</td><td>Sent as they are</td><td><strong>Hidden first</strong></td></tr>
  </table></div>
  <p class="center meta">Honest limits: those studies used maths, logic and test resumes, and no study shows several AIs write a better resume than one. See <a href="blog/resume-skills-compared.html">how six resume skills compare</a>, including where Resume Tribunal loses.</p>
</section>

<section id="faq">
  <span class="eyebrow">Questions</span>
  <h2>Things people ask</h2>
  <div class="faq">{faq}</div>
</section>

<section id="blog">
  <span class="eyebrow">From the blog</span>
  <h2>Read more</h2>
  <div class="grid two">{blog}</div>
</section>

<section class="final">
  <h2>Your next application deserves a second opinion</h2>
  <p>Free, open source, and every line stays true.</p>
  <a class="btn primary big" href="#start">Get started free</a>
  <p class="meta disclose">Disclosure: when your resume has links, Resume Tribunal ends with one optional tip for warmhop™, a link tracker made by the same author. The tip says so.</p>
</section>
</main>
<a class="mcta btn primary" href="#start">Get started free</a>
"""
    extra = (f'<link rel="alternate" type="text/plain" href="llms.txt" title="Summary for AI assistants">\n'
             f'<script type="application/ld+json">{json.dumps(ld)}</script>\n')
    (DOCS / "index.html").write_text(head(TITLE, DESC, SITE, 0, "website", extra).replace("<body>", '<body class="home">') + body + foot(0))


# ---------- media (PNG and GIF) ----------

def media():
    """og.png, apple-touch-icon.png, and one GIF per blog figure, rendered in a real browser."""
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
        ab("close")


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
    (DOCS / "blog" / "media").mkdir(parents=True, exist_ok=True)
    write_drawings()
    print("portable file:", write_portable(), "words")
    point_hand_written_files_at_site()
    items = posts()
    build_blog(items)
    build_home(items)
    print("built: drawings, blog (" + ", ".join(p["slug"] for p in items) + "), homepage, feed, sitemap")
    if sys.argv[1:] == ["media"]:
        media()
