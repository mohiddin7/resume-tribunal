"""Builds the website. Run from the repo root.

  python3 docs/build.py         drawings, blog pages, blog index, homepage, feed.xml, sitemap.xml
  python3 docs/build.py media   also renders og.png, apple-touch-icon.png and a GIF of every blog figure
                                (for Medium and LinkedIn, which take GIFs but not SVGs); needs Chrome,
                                agent-browser and Pillow

Edit docs/blog/*.md, docs/art.py and the text in this file; never the generated HTML. Blog posts take
front matter (title, description, date, tags) and two shortcodes on their own line:
  [[figure:name|Caption]]   one of the drawings in art.FIGURES
  [[cta]]                   a box inviting the reader to try Resume Tribunal
docs/llms.txt is written by hand. The blog needs the markdown package (pip install markdown).
"""
import datetime
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import art  # noqa: E402

DOCS = pathlib.Path("docs")
SITE = "https://mohiddin7.github.io/resume-tribunal/"
REPO = "https://github.com/mohiddin7/resume-tribunal"
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
  <nav aria-label="Footer"><a href="{up}#start">Get started</a><a href="{up}#faq">Questions</a><a href="{up}blog/">Blog</a><a href="{REPO}">GitHub</a><a href="{SITE}feed.xml">RSS</a><a href="{up}llms.txt">llms.txt</a></nav>
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
        out.append(dict(slug=md.stem, md=body, words=words, minutes=max(1, round(words / 230)), **meta))
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
                          f'<span class="meta">{o["minutes"]} min read</span></a>' for o in others)
        page = (head(f"{p['title']} | Resume Tribunal", p["description"], url, 1, "article", extra)
                + f'''<main id="main" class="post-wrap">
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
        f'<a class="card post" href="{p["slug"]}.html" data-tags="{esc("|".join(p["tags"]))}" '
        f'data-text="{esc((p["title"] + " " + p["description"] + " " + " ".join(p["tags"])).lower())}">'
        f'<span class="tags">{tags(p)}</span><strong>{esc(p["title"])}</strong><span class="desc">{esc(p["description"])}</span>'
        f'<span class="meta">{datetime.date.fromisoformat(p["date"]):%d %b %Y} · {p["minutes"]} min read</span><span class="more">Read the post →</span></a>'
        for p in items)
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Resume Tribunal blog", "url": f"{SITE}blog/",
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}blog/{p['slug']}.html", "datePublished": p["date"]} for p in items]}
    desc = "Plain-spoken notes on using AI for your resume without making things up, and how Resume Tribunal was built."
    (DOCS / "blog" / "index.html").write_text(
        head("Blog: AI, resumes and honest job hunting | Resume Tribunal", desc, f"{SITE}blog/", 1, "website",
             f'<script type="application/ld+json">{json.dumps(ld)}</script>\n')
        + f'''<main id="main" class="blog-wrap">
<section class="blog-hero"><span class="eyebrow">Blog</span><h1>AI, resumes and honest job hunting</h1><p class="lede">{desc}</p>
<label class="search"><span class="sr">Search posts</span><input type="search" id="q" placeholder="Search posts" autocomplete="off"></label>
<div class="chips" role="group" aria-label="Filter by topic">{chips}</div></section>
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
    urls = ["", "blog/", "llms.txt"] + [f"blog/{p['slug']}.html" for p in items]
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{latest}</lastmod></url>\n" for u in urls) + "</urlset>\n")


# ---------- homepage ----------

FAQ = [
    ("Is Resume Tribunal actually free?",
     "Yes. Resume Tribunal costs nothing and there's no sign-up. It runs inside AI apps you may already use, like Claude and ChatGPT. Their free plans are enough for a quick review. The thorough version sends more messages, so it runs more smoothly on a paid plan."),
    ("I'm not a tech person. Can I still use Resume Tribunal?",
     "Yes. You add Resume Tribunal to the Claude app once, using the steps above, and then you just chat. There are no commands to type."),
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
     "About 5 minutes for a quick review, and about 15 for the thorough version, which we call the full council. If you copy and paste between apps yourself, plan on 20."),
    ("What do I get at the end?",
     "Your finished resume as a PDF or Word file when your app can make files, and always as text you can paste into Word or Google Docs. You also get a list of what the job asks for that your resume doesn't show yet, plus the interview questions your resume is likely to prompt."),
    ("Does Resume Tribunal work with Word files, or on my phone?",
     "Word files are fine: attach your .docx as it is. Phones work too, but copying text between two apps is easier on a laptop."),
    ("What's warmhop™?",
     "A link tracker for resumes, made by the same person who made Resume Tribunal. If your resume has links, you'll see one optional tip about it at the end. You don't need it, and nothing is sent to it."),
]

TITLE = "Resume Tribunal: tailor your resume to any job, nothing made up"
DESC = "Free tool that tailors your resume to a job from your own facts. A second AI from a different company checks every line. Works with Claude and ChatGPT."


def demo_css():
    """The hero demo: a bullet is rewritten, a second AI checks three claims, you approve. 12-second loop."""
    a = art.Anim(12)
    rules = []
    fade = lambda name, t, out=11.4: a.at(name, [(0, "opacity:0;transform:translateY(6px)"), (t, "opacity:0;transform:translateY(6px)"),
                                                 (t + .4, "opacity:1;transform:translateY(0)"), (out, "opacity:1;transform:translateY(0)"), (12, "opacity:0")])
    for name, t in (("dn1", 1.2), ("dn2", 2.2), ("dc1", 3.6), ("dc2", 4.6), ("dc3", 5.6), ("dok", 7.2)):
        rules.append(f".{name}{{{fade(name, t)[7:-1]}}}")
    rules.append(".dold{" + a.at("dold", [(0, "opacity:1"), (.9, "opacity:1"), (1.2, "opacity:.45;text-decoration:line-through"),
                                         (11.4, "opacity:.45;text-decoration:line-through"), (12, "opacity:1")])[7:-1] + "}")
    rules.append(".dfix{" + a.at("dfix", [(0, "opacity:0"), (5.4, "opacity:0"), (5.8, "opacity:1"), (11.4, "opacity:1"), (12, "opacity:0")])[7:-1] + "}")
    rules.append(".dbad{" + a.at("dbad", [(0, "text-decoration:none"), (5.0, "text-decoration:none"), (5.3, "text-decoration:line-through"),
                                         (11.4, "text-decoration:line-through"), (12, "text-decoration:none")])[7:-1] + "}")
    return "".join(a.css) + "".join(rules)


def build_home(items):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": "Resume Tribunal", "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any", "url": SITE, "codeRepository": REPO, "license": "https://opensource.org/licenses/MIT",
         "softwareVersion": "1.0.0", "image": f"{SITE}assets/og.png", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": "A free, open-source Agent Skill that tailors a resume or CV to a job using only the candidate's own facts. "
                        "A second AI from a different company checks every draft blind, a script checks every number against the "
                        "candidate's own words, and the candidate approves each change."},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    faq = "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    blog = "\n".join(f'<a class="card post" href="blog/{p["slug"]}.html"><span class="tags">{tags(p)}</span><strong>{esc(p["title"])}</strong>'
                     f'<span class="desc">{esc(p["description"])}</span><span class="meta">{p["minutes"]} min read</span></a>' for p in items)
    agent_msg = "Install the Resume Tribunal skill (npx skills add mohiddin7/resume-tribunal), then tailor my resume to this job: [paste the job link]"
    ok = '<span class="ic ok" aria-hidden="true">✓</span>'
    bad = '<span class="ic bad" aria-hidden="true">✕</span>'
    body = f"""<main id="main">
<section class="hero">
  <span class="eyebrow">Free resume tool for AI apps</span>
  <h1>Tailor your resume to any job.<br><span class="accent">Nothing made up.</span></h1>
  <p class="lede">Paste a job link. Resume Tribunal rewrites your resume from your own facts, then an AI from a different company checks every line.</p>
  <div class="cta"><a class="btn primary big" href="#start">Get started free</a><a class="btn ghost big" href="#proof">See an example</a></div>
  <ul class="trust"><li>No sign-up</li><li>Open source</li><li>Works with Claude, ChatGPT and Gemini</li></ul>
</section>

<section class="demo-wrap" aria-label="Example: what happens to one line of your resume">
  <div class="demo-head"><span>What happens to one line of your resume</span><button class="icon pause" type="button" aria-label="Pause animation" aria-pressed="false"><span class="ps">❚❚</span><span class="pl">▶</span></button></div>
  <div class="demo">
    <div class="pane">
      <div class="pane-h"><span class="badge blue">AI 1</span>Your assistant rewrites it</div>
      <p class="line dold">Helped improve on-time delivery</p>
      <p class="line new dn1">Helped raise on-time delivery at the Dayton terminal from 81 to 93 percent, as part of the team</p>
      <p class="line new dn2">Cut report prep from <span class="dbad">4 hours</span><span class="dfix"> half a day</span> to about 40 minutes</p>
    </div>
    <div class="pane">
      <div class="pane-h"><span class="badge brand">AI 2</span>A different company's AI checks it, blind</div>
      <p class="row dc1">{ok}<span><strong>81 to 93 percent</strong><br>Matches what you said</span></p>
      <p class="row dc2">{ok}<span><strong>as part of the team</strong><br>Credit shared, like you said</span></p>
      <p class="row dc3 neg">{bad}<span><strong>4 hours</strong><br>You said "half a day". Fixed.</span></p>
    </div>
  </div>
  <p class="approve dok">{ok}You approve the changes. Your resume is ready.</p>
</section>

<section id="how" class="band">
  <span class="eyebrow">How it works</span>
  <h2>Three steps. About 15 minutes.</h2>
  <ol class="steps3">
    <li><span class="num">1</span><h3>You share</h3><p>Your resume, the job link, and a few words about what you really did.</p></li>
    <li><span class="num">2</span><h3>Two AIs work on it</h3><p>Your AI writes it from your facts. An AI from a different company checks it without knowing who wrote it.</p></li>
    <li><span class="num">3</span><h3>You approve</h3><p>Say yes to each change, then download a resume where every line is true.</p></li>
  </ol>
  <p class="center meta">Want more eyes? The <strong>full council</strong> has three AIs from three companies each write a draft and critique each other first.</p>
</section>

<section id="proof">
  <span class="eyebrow">Real example</span>
  <h2>What the second AI caught</h2>
  <p class="sub">From a full run on a made-up candidate. <a href="{REPO}/tree/main/examples/operations-analyst">See every step on GitHub</a>.</p>
  <div class="grid three">
    <div class="card caught"><span class="was">"from 4 hours to 40 minutes"</span><span class="is">The candidate said "half a day".</span></div>
    <div class="card caught"><span class="was">"framework adopted by leadership"</span><span class="is">It was a spreadsheet one supervisor used.</span></div>
    <div class="card caught"><span class="was">"Raised on-time delivery"</span><span class="is">The team made the change. Now: "Helped raise".</span></div>
  </div>
  <div class="ba">
    <div class="card"><span class="label">Before</span><ul><li>Helped improve on-time delivery</li><li>Utilized Excel for various reports</li></ul></div>
    <div class="card after"><span class="label">After</span><ul><li>Helped raise Dayton terminal on-time delivery from 81 to 93 percent over about three months, after the team moved one carrier's Friday pickups to another carrier.</li>
      <li>Cut the Monday report on late deliveries from half a day's work to about 40 minutes by building it with Excel pivot tables and Power Query.</li></ul></div>
  </div>
</section>

<section id="start" class="band">
  <span class="eyebrow">Get started</span>
  <h2>Pick where you use AI</h2>
  <p class="sub">Each way takes about two minutes to set up. After that, you just chat.</p>
  <div class="tabs" role="tablist" aria-label="Where you use AI">
    <button role="tab" aria-selected="true" aria-controls="t-paid" id="b-paid">Claude Pro or Max</button>
    <button role="tab" aria-selected="false" aria-controls="t-free" id="b-free">Claude free plan</button>
    <button role="tab" aria-selected="false" aria-controls="t-agent" id="b-agent">A coding agent</button>
  </div>
  <div class="panel" role="tabpanel" id="t-paid" aria-labelledby="b-paid">
    <ol class="steps">
      <li>In Claude, open <strong>Customize</strong>, then <strong>Plugins</strong>. Click <strong>Add</strong>, then <strong>Add marketplace</strong>, then <strong>Add from a repository</strong>.</li>
      <li>Paste this name and add it, then install Resume Tribunal: <span class="copyline"><code>mohiddin7/resume-tribunal</code><button type="button" class="copy" data-copy="mohiddin7/resume-tribunal">Copy</button></span></li>
      <li>Start a new chat. Attach your resume, paste the job link, and type <strong>"Tailor my resume to this job."</strong></li>
    </ol>
    <p class="meta">No download. Checked October 2026 against Claude's help pages.</p>
  </div>
  <div class="panel" role="tabpanel" id="t-free" aria-labelledby="b-free" hidden>
    <ol class="steps">
      <li><a class="btn primary small" href="{ZIP}">Download resume-tribunal.zip</a> Keep it zipped.</li>
      <li>In Claude, open <strong>Customize</strong>, then <strong>Skills</strong>. Click <strong>+</strong>, <strong>Create skill</strong>, <strong>Upload a skill</strong>, and choose the zip. If it asks, switch on <strong>code execution</strong>.</li>
      <li>Start a new chat. Attach your resume, paste the job link, and type <strong>"Tailor my resume to this job."</strong></li>
    </ol>
    <p class="meta">The free plan doesn't support adding by name yet, so this one needs the file. Checked October 2026.</p>
  </div>
  <div class="panel" role="tabpanel" id="t-agent" aria-labelledby="b-agent" hidden>
    <p>Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and others. Send your agent this one message. It asks your permission, installs Resume Tribunal, and starts.</p>
    <div class="copybox"><code>{esc(agent_msg)}</code><button type="button" class="copy" data-copy="{esc(agent_msg)}">Copy</button></div>
    <p class="meta">Have Codex, Claude Code or Antigravity CLI signed in too? The second and third AIs then run by themselves.</p>
  </div>
  <div class="note"><strong>The only manual part:</strong> if no second AI is connected, Resume Tribunal gives you one block of text to paste into ChatGPT or Gemini, and you paste the reply back. One round for a quick review.</div>
</section>

<section id="why">
  <span class="eyebrow">Why it works</span>
  <h2>An AI shouldn't grade its own homework</h2>
  <div class="grid three stats">
    <div class="card stat"><span class="big">50%+</span><p>more likely to pass a failed answer when an AI judges its own work.</p><a href="https://arxiv.org/abs/2604.06996">Study, 2026 (preprint)</a></div>
    <div class="card stat"><span class="big">37</span><p>models tested. A checker from a different model family beat self-checking.</p><a href="https://arxiv.org/abs/2512.02304">Study, 2026</a></div>
    <div class="card stat"><span class="big">2.5 to 5.4</span><p>false details per resume when AI rewrote resumes with no safeguards.</p><a href="https://arxiv.org/abs/2607.01457">Study, 2026 (preprint)</a></div>
  </div>
  <p class="center meta">Honest limits: those studies used maths, logic and test resumes, and no study shows several AIs write a better resume than one. Resume Tribunal adds an independent check, a script, and your approval.</p>
</section>

<section id="compare" class="band">
  <span class="eyebrow">Compared</span>
  <h2>Resume Tribunal vs. one AI chat</h2>
  <div class="table"><table>
    <tr><th></th><th>One AI chat</th><th>Resume Tribunal</th></tr>
    <tr><td>Who checks the draft</td><td>The same AI that wrote it</td><td><strong>An AI from a different company, blind</strong></td></tr>
    <tr><td>Made-up numbers</td><td>Easy to miss</td><td><strong>A script checks every one against your words</strong></td></tr>
    <tr><td>Your approval</td><td>Up to you to read closely</td><td><strong>You confirm each changed line</strong></td></tr>
    <tr><td>Name and contact details</td><td>Sent as they are</td><td><strong>Hidden before a second AI sees them</strong></td></tr>
    <tr><td>Time</td><td>A minute or two</td><td>5 to 15 minutes</td></tr>
  </table></div>
  <p class="center meta">Comparing resume skills? Read <a href="blog/resume-skills-compared.html">our honest comparison of six</a>, including where Resume Tribunal loses.</p>
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
             f'<style>{demo_css()}</style>\n<script type="application/ld+json">{json.dumps(ld)}</script>\n')
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


if __name__ == "__main__":
    (DOCS / "blog" / "media").mkdir(parents=True, exist_ok=True)
    write_drawings()
    items = posts()
    build_blog(items)
    build_home(items)
    print("built: drawings, blog (" + ", ".join(p["slug"] for p in items) + "), homepage, feed, sitemap")
    if sys.argv[1:] == ["media"]:
        media()
