"""Builds the site's generated files. Run from the repo root: python3 docs/build.py

docs/assets/how-it-works*.svg  animated flow; plain, -light and -dark (the plain one follows the viewer)
docs/assets/favicon.svg        adaptive mark
docs/assets/og.svg             social card; render it to og.png at 1200x630 in any browser after edits
docs/blog/<slug>.html          from docs/blog/<slug>.md (front matter: title, description, date)
docs/blog/index.html, docs/feed.xml, docs/sitemap.xml

The blog needs the markdown package (pip install markdown). Everything else is standard library.
"""
import datetime
import html
import pathlib
import re

OUT = pathlib.Path("docs/assets")
LIGHT = dict(bg="#f7f4ef", surf="#fffdf9", ink="#221e19", muted="#5f574d", line="#ddd5c8",
             brand="#a8515c", onbrand="#ffffff", blue="#35619a", green="#2f6c36", purple="#685497")
DARK = dict(bg="#14120f", surf="#221e19", ink="#f3ede4", muted="#b5ab9e", line="#3a332b",
            brand="#d67a84", onbrand="#14120f", blue="#4e88d3", green="#479650", purple="#9177cf")
FONT = 'system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif'


def tokens(t):
    return ";".join(f"--{k}:{v}" for k, v in t.items())


def theme_css(adaptive):
    """True follows the viewer's setting, False is always dark, None is always light."""
    if adaptive is None:
        return f"svg{{{tokens(LIGHT)}}}"
    if adaptive:
        return f"svg{{{tokens(LIGHT)}}}@media (prefers-color-scheme:dark){{svg{{{tokens(DARK)}}}}}"
    return f"svg{{{tokens(DARK)}}}"


STEPS = [  # tag, accent var, title, body lines
    ("YOU", "green", "You give three things",
     ["Your resume, the job posting, and a few sentences in your own words."]),
    ("AI 1 · YOUR ASSISTANT", "blue", "It writes a draft for the job",
     ["Only your facts. A missing number becomes a question, never a guess."]),
    ("AI 2 · FROM A DIFFERENT COMPANY", "brand", "A second AI checks it blind",
     ["It is not told who wrote the draft, so no AI grades its own work."]),
    ("AUTOMATIC CHECK", "purple", "A script tests every line",
     ["Flags AI writing habits, layout problems, and numbers you never gave."]),
    ("YOU", "green", "You approve every changed line",
     ["Is it true? Could you explain it in an interview?"]),
    ("RESULT", "brand", "A resume you can defend",
     ["Readable by screening software, honest about what you lack,",
      "with the interview questions to expect."]),
]
STEP_S, HOLD_S = 1.7, 2.8
CYCLE = STEP_S * len(STEPS) + HOLD_S


def pct(t):
    return f"{100 * t / CYCLE:.2f}%"


def how_it_works(adaptive):
    W, X, BW, GAP, y = 680, 40, 600, 34, 78
    end = STEP_S * len(STEPS) + HOLD_S * .75  # everything stays lit until here, then fades and loops
    kf = []
    for i in range(len(STEPS)):
        a = i * STEP_S
        kf.append(f"@keyframes lit{i}{{0%,{pct(a)}{{opacity:0}}{pct(a + .25)},{pct(end)}{{opacity:1}}{pct(end + .5)},100%{{opacity:0}}}}")
        b, c = a + STEP_S * .5, a + STEP_S * .95
        kf.append(f"@keyframes go{i}{{0%,{pct(b)}{{opacity:0;transform:translateY(0)}}{pct(b + .1)}{{opacity:1;transform:translateY(0)}}"
                  f"{pct(c)}{{opacity:1;transform:translateY({GAP - 12}px)}}{pct(c + .1)},100%{{opacity:0;transform:translateY({GAP - 12}px)}}}}")
    a = 2 * STEP_S
    for name, dx in (("swapK", 368), ("swapR", -368)):
        kf.append(f"@keyframes {name}{{0%,{pct(a + .35)}{{transform:translateX(0)}}{pct(a + 1.15)},{pct(end)}{{transform:translateX({dx}px)}}"
                  f"{pct(end + .6)},100%{{transform:translateX(0)}}}}")
    anim = lambda name: f"animation:{name} {CYCLE:.1f}s ease-in-out infinite"
    css = [theme_css(adaptive), f"text{{font-family:{FONT}}}",
           ".h{font-size:22px;font-weight:700;fill:var(--ink)}.sub{font-size:13px;fill:var(--muted)}",
           ".tag{font-size:12px;font-weight:700;letter-spacing:.08em}.title{font-size:19px;font-weight:700;fill:var(--ink)}",
           ".body{font-size:15px;fill:var(--muted)}.card{fill:var(--surf);stroke:var(--line);stroke-width:1.5}",
           ".chip{fill:var(--bg);stroke:var(--line)}.chipt{font-size:12px;font-weight:700;fill:var(--ink)}",
           ".lit,.dot{opacity:0}", *kf,
           "@media (prefers-reduced-motion:reduce){.lit,.dot,.mv{animation:none!important}.lit{opacity:1}}"]
    parts = []
    for i, (tag, acc, title, body) in enumerate(STEPS):
        h = 70 + 22 * len(body) + (62 if i == 2 else 0)
        parts.append(f'<rect class="card" x="{X}" y="{y}" width="{BW}" height="{h}" rx="12"/>')
        # the lit layer: accent border and a faint tint
        parts.append(f'<rect class="lit" style="{anim(f'lit{i}')}" x="{X}" y="{y}" width="{BW}" height="{h}" rx="12" '
                     f'fill="var(--{acc})" fill-opacity=".07" stroke="var(--{acc})" stroke-width="2.5"/>')
        parts.append(f'<rect x="{X}" y="{y + 14}" width="5" height="{h - 28}" rx="2.5" fill="var(--{acc})"/>')
        parts.append(f'<text x="{X + 24}" y="{y + 27}" class="tag" fill="var(--{acc})">{tag}</text>')
        parts.append(f'<text x="{X + 24}" y="{y + 52}" class="title">{title}</text>')
        for j, line in enumerate(body):
            parts.append(f'<text x="{X + 24}" y="{y + 76 + 22 * j}" class="body">{line}</text>')
        if i == 2:  # three anonymous drafts trade places: labels are shuffled before review
            cy = y + 98
            for k, (label, name) in enumerate([("Draft K", "swapK"), ("Draft M", ""), ("Draft R", "swapR")]):
                cx = X + 24 + k * 184
                mv = f' class="mv" style="{anim(name)}"' if name else ""
                parts.append(f'<g{mv}><rect class="chip" x="{cx}" y="{cy}" width="168" height="26" rx="13"/>'
                             f'<text x="{cx + 84}" y="{cy + 17}" text-anchor="middle" class="chipt">{label}</text></g>')
            parts.append(f'<text x="{X + 24}" y="{cy + 44}" class="sub">Full council: three AIs draft, then critique each other under shuffled labels.</text>')
        y += h
        if i < len(STEPS) - 1:
            cx = W // 2
            parts.append(f'<path d="M{cx} {y + 6} V{y + GAP - 8}" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>')
            parts.append(f'<path d="M{cx - 6} {y + GAP - 14} l6 7 l6 -7" fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
            parts.append(f'<circle class="dot" style="{anim(f'go{i}')}" cx="{cx}" cy="{y + 6}" r="5" fill="var(--{STEPS[i + 1][1]})"/>')
            y += GAP
    H = y + 34
    desc = ("You give your resume, the job posting and a few sentences in your own words. Your assistant writes a draft "
            "from your facts only. An AI from a different company checks it without being told who wrote it; in full council "
            "three AIs draft and critique each other under shuffled labels. A script flags AI writing habits, layout problems "
            "and numbers you never gave. You approve every changed line. You get a resume you can defend.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">'
            f'<title id="t">How Resume Tribunal works</title><desc id="d">{desc}</desc>'
            f'<style>{"".join(css)}</style>'
            f'<rect width="{W}" height="{H}" rx="16" fill="var(--bg)"/>'
            f'<text x="{X}" y="44" class="h">How Resume Tribunal works</text>'
            f'<text x="{X}" y="64" class="sub">Each step lights up in turn. A quick review takes about 5 minutes, a full council about 15.</text>'
            + "".join(parts) + "</svg>\n")


def favicon():
    # three seats in a ring; the filled one is the reviewer that did not write the draft
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><style>{theme_css(True)}</style>'
            '<rect width="32" height="32" rx="8" fill="var(--brand)"/>'
            '<circle cx="16" cy="9" r="4" fill="var(--onbrand)"/>'
            '<circle cx="9" cy="21.5" r="4" fill="none" stroke="var(--onbrand)" stroke-width="2.2"/>'
            '<circle cx="23" cy="21.5" r="4" fill="none" stroke="var(--onbrand)" stroke-width="2.2"/></svg>\n')


def og():
    t = LIGHT
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<style>text{{font-family:{FONT}}}</style>
<rect width="1200" height="630" fill="{t['bg']}"/>
<rect x="0" y="0" width="16" height="630" fill="{t['brand']}"/>
<g transform="translate(80 92)"><rect width="56" height="56" rx="14" fill="{t['brand']}"/>
<circle cx="28" cy="16" r="7" fill="#fff"/><circle cx="16" cy="38" r="7" fill="none" stroke="#fff" stroke-width="3.6"/>
<circle cx="40" cy="38" r="7" fill="none" stroke="#fff" stroke-width="3.6"/></g>
<text x="156" y="134" font-size="40" font-weight="700" fill="{t['ink']}">Resume Tribunal</text>
<text x="80" y="250" font-size="60" font-weight="800" fill="{t['ink']}">Tailor your resume to a job,</text>
<text x="80" y="326" font-size="60" font-weight="800" fill="{t['brand']}">with a second AI checking the first.</text>
<text x="80" y="410" font-size="28" fill="{t['muted']}">Built only from your own facts. Reviewed blind by an AI from a different</text>
<text x="80" y="450" font-size="28" fill="{t['muted']}">company. Readable by screening software. Free and open source.</text>
<rect x="80" y="510" width="460" height="56" rx="12" fill="{t['surf']}" stroke="{t['line']}" stroke-width="2"/>
<text x="104" y="546" font-size="24" font-family="ui-monospace,Menlo,Consolas,monospace" fill="{t['ink']}">npx skills add mohiddin7/resume-tribunal</text>
</svg>
'''



SITE = "https://mohiddin7.github.io/resume-tribunal/"
REPO = "https://github.com/mohiddin7/resume-tribunal"
AUTHOR = "mohiddin7"


def head(title, desc, url, depth, kind="website", extra=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Resume Tribunal blog" href="{SITE}feed.xml">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Resume Tribunal">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#a8515c">
<link rel="stylesheet" href="{up}assets/site.css">
<script src="{up}assets/site.js"></script>
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="in">
  <a class="logo" href="{up}"><img src="{up}assets/favicon.svg" alt="" width="28" height="28">Resume Tribunal</a>
  <nav class="top" aria-label="Main">
    <a href="{up}#how">How it works</a><a href="{up}#start">Start here</a><a href="{up}#faq">Questions</a>
    <a href="{up}blog/">Blog</a><a href="{REPO}">GitHub</a>
    <button class="theme" type="button">Dark mode</button>
  </nav>
</div></header>
"""


def foot(depth):
    up = "../" * depth
    return f"""<footer class="site"><div class="in">
  <span>Resume Tribunal is free and open source, MIT license.</span>
  <a href="{REPO}">Source code</a><a href="{up}blog/">Blog</a><a href="{SITE}feed.xml">RSS</a><a href="{up}llms.txt">llms.txt</a>
</div></footer>
</body>
</html>
"""


def posts():
    import markdown  # only the blog needs it
    out = []
    for md in sorted(pathlib.Path("docs/blog").glob("*.md")):
        front, body = md.read_text().split("---\n", 2)[1:]
        meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
        words = len(body.split())
        out.append(dict(slug=md.stem, body=markdown.markdown(body, extensions=["tables"]), words=words,
                        minutes=max(1, round(words / 230)), **meta))
    return sorted(out, key=lambda p: p["date"], reverse=True)


def build_blog():
    items = posts()
    for p in items:
        url = f"{SITE}blog/{p['slug']}.html"
        day = datetime.date.fromisoformat(p["date"])
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
              "description": p["description"], "datePublished": p["date"], "dateModified": p["date"],
              "author": {"@type": "Person", "name": AUTHOR, "url": "https://github.com/mohiddin7"},
              "image": f"{SITE}assets/og.png", "mainEntityOfPage": url, "wordCount": p["words"]}
        import json
        extra = (f'<meta property="article:published_time" content="{p["date"]}">\n'
                 f'<script type="application/ld+json">{json.dumps(ld)}</script>\n')
        page = (head(f"{p['title']} | Resume Tribunal", p["description"], url, 1, "article", extra)
                + f'<main id="main"><article>\n<p class="meta"><a href="./">Blog</a> · {day:%d %B %Y} · {p["minutes"]} min read</p>\n'
                + f"<h1>{html.escape(p['title'])}</h1>\n<p class=\"lede\">{html.escape(p['description'])}</p>\n"
                + p["body"]
                + f'\n<div class="card"><strong>Try Resume Tribunal.</strong> It is free and open source. '
                  f'<a href="../#start">Start here</a> if you have never used a terminal, or see the <a href="{REPO}">code on GitHub</a>.</div>\n'
                + "</article></main>\n" + foot(1))
        pathlib.Path(f"docs/blog/{p['slug']}.html").write_text(page)
    lis = "\n".join(f'<li><a href="{p["slug"]}.html">{html.escape(p["title"])}</a>'
                    f'<p class="meta">{datetime.date.fromisoformat(p["date"]):%d %B %Y} · {p["minutes"]} min read</p>'
                    f'<p>{html.escape(p["description"])}</p></li>' for p in items)
    pathlib.Path("docs/blog/index.html").write_text(
        head("Blog | Resume Tribunal", "Notes on building Resume Tribunal and on using AI for resumes honestly.", f"{SITE}blog/", 1)
        + f'<main id="main"><h1>Blog</h1><p class="lede">How Resume Tribunal was made, and what we have learned about AI and resumes.</p>\n<ul class="posts">\n{lis}\n</ul></main>\n'
        + foot(1))
    rss = "\n".join(f"<item><title>{html.escape(p['title'])}</title><link>{SITE}blog/{p['slug']}.html</link>"
                    f"<guid>{SITE}blog/{p['slug']}.html</guid>"
                    f"<pubDate>{datetime.date.fromisoformat(p['date']):%a, %d %b %Y} 00:00:00 +0000</pubDate>"
                    f"<description>{html.escape(p['description'])}</description></item>" for p in items)
    pathlib.Path("docs/feed.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Resume Tribunal blog</title>'
        f"<link>{SITE}blog/</link><description>Notes on building Resume Tribunal and on using AI for resumes honestly.</description>\n{rss}\n</channel></rss>\n")
    today = max(p["date"] for p in items)
    urls = ["", "blog/", "llms.txt"] + [f"blog/{p['slug']}.html" for p in items]
    pathlib.Path("docs/sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    return [p["slug"] for p in items]

FAQ = [
    ("Do I need to know how to code?",
     "No. If you use the Claude app, you upload the skill once and then chat as usual. The steps are under Start here. The terminal route is quicker, but you can skip it."),
    ("Is it free?",
     "The skill is. It runs on the AI apps you already use, and free plans work. Free plans have daily limits, and a long run can reach them, so the thorough version goes more smoothly on a paid plan."),
    ("Why not just ask ChatGPT to fix my resume?",
     "You can, and for a quick tidy-up that's fine. The trouble starts when the same AI writes your resume and then tells you it's good. It tends to like its own work, and it will happily turn \"half a day\" into \"4 hours\". A second AI from another company catches more of that, and a script checks every number against what you actually said."),
    ("Will it make things up?",
     "It's designed not to, and it checks. Every number, tool and job title has to come from you. If something's missing, it asks. Before you get the final file, you say yes or no to each changed line, and anything you don't confirm comes out."),
    ("Will this get me past the ATS?",
     "No one can promise that. ATS is the software many employers use to collect and sort applications. This skill avoids the things known to confuse it: columns, tables, text in headers, images, hidden text. Then it checks that the PDF's text reads back correctly. In the end a person usually reads your resume, and it's written for them."),
    ("Can recruiters tell an AI helped?",
     "Maybe. It removes the habits people spot most, like long dashes and words such as \"spearheaded\". It won't make the resume your unaided work, though. If an employer asks about AI use, tell the truth."),
    ("Is my resume safe?",
     "This project never sees it. Your name, email, phone number and links are swapped for stand-in text such as <<NAME>> before anything goes to a second AI, and you're asked before anything is sent. The AI companies you use do see the text, under their own terms, so leave out anything confidential."),
    ("How long does it take?",
     "About 5 minutes for a quick review when the other AI runs by itself, and about 15 for a full council. If you're copying and pasting by hand, allow 20 minutes or so."),
    ("What's a \"full council\"?",
     "Three AIs from three companies each write a draft. Then they point out problems in each other's drafts without knowing who wrote which. The best parts are merged and checked again. It uses about five times as much AI time as a quick review."),
    ("What's warmhop™?",
     "A resume link tracker made by the same person who made this skill. If your resume has links, you'll see one optional tip about it at the end. You don't need it, and nothing is sent to it."),
]
TITLE = "Resume Tribunal: tailor your resume to a job, checked by a second AI"
DESC = "Free tool that tailors your resume to a job using only your facts, then has an AI from another company check it blind. Works with Claude and ChatGPT."


def build_home(items):
    import json
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": "Resume Tribunal", "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any", "url": SITE, "codeRepository": REPO, "license": "https://opensource.org/licenses/MIT",
         "softwareVersion": "1.0.0", "image": f"{SITE}assets/og.png", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": "An open-source Agent Skill that tailors a resume or CV to a job description using only the candidate's own facts. "
                        "An AI assistant from a different company reviews every draft blind, a script checks every number against the "
                        "candidate's own words, and the candidate approves each changed line."},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
    faq = "\n".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in FAQ)
    blog = "\n".join(f'<li><a href="blog/{p["slug"]}.html">{html.escape(p["title"])}</a><p class="meta">{p["minutes"]} min read</p></li>' for p in items)
    body = f"""<main id="main" class="wide">
<h1>Tailor your resume to a job, <span class="accent">with a second AI checking the first.</span></h1>
<p class="lede">Resume Tribunal is a free add-on for AI assistants such as Claude, ChatGPT and Gemini. It rewrites your resume for one job using only facts you gave it. Then an AI from a different company checks the draft without being told who wrote it, so nothing gets exaggerated and no AI grades its own work.</p>
<p>New to this? You'll run it in the free Claude app, and use ChatGPT or Gemini for the second check.</p>
<div class="cta"><a class="btn primary" href="#start">New to this? Start here</a><a class="btn ghost" href="#install">I'm a developer</a></div>
<p class="meta">Free and open source. No sign-up. Your resume never comes to us.</p>

<h2>Before and after</h2>
<p>One job from the <a href="{REPO}/tree/main/examples/operations-analyst">worked example</a>, a made-up operations coordinator applying for an analyst role.</p>
<div class="ba">
  <div class="card"><h3>Before</h3><ul><li>Helped improve on-time delivery</li><li>Utilized Excel for various reports</li></ul></div>
  <div class="card after"><h3>After</h3><ul>
    <li>Helped raise Dayton terminal on-time delivery from 81 to 93 percent over about three months, after the team moved one carrier's Friday pickups to another carrier.</li>
    <li>Cut the Monday report on late deliveries for the operations manager from half a day's work to about 40 minutes by building it with Excel pivot tables and Power Query.</li></ul></div>
</div>
<p class="note">A reviewing AI suggested "from 4 hours to 40 minutes". The candidate had said "half a day", so that is what the resume says.</p>

<h2 id="how">How it works</h2>
<div class="flow"><img src="assets/how-it-works.svg" data-light="assets/how-it-works-light.svg" data-dark="assets/how-it-works-dark.svg" width="620" height="918" alt="How Resume Tribunal works. You give your resume, the job posting and a few sentences in your own words. Your assistant writes a draft from your facts only. An AI from a different company checks it without being told who wrote it. A script flags AI writing habits, layout problems and numbers you never gave. You approve every changed line. You get a resume you can defend."></div>
<p><strong>Quick review</strong> is one writer and one checker. <strong>Full council</strong> has three AIs from three companies each write a draft and critique each other under shuffled labels, and the best parts are merged before the check. Why three? It is the smallest group where two can outvote one that is wrong, the same reason aircraft flight computers vote two out of three.</p>
<p>The second AI can be reached two ways. If you have other AI tools installed on a computer, it runs by itself. If not, you get one block of text to paste into another AI app, such as ChatGPT or Gemini, and you paste the reply back.</p>

<h2 id="start">Start here: no coding needed</h2>
<p>You need the Claude app, which is free. Get it at <a href="https://claude.ai">claude.ai</a> or from your phone's app store. Skills need one setting called "code execution" switched on; it's an on/off switch in the app's settings. (Checked October 2026.)</p>
<ol class="steps">
  <li><a href="https://github.com/mohiddin7/resume-tribunal/releases/latest/download/resume-tribunal.zip">Download resume-tribunal.zip</a>. Keep it zipped.</li>
  <li>In the Claude app, open Customize, then Skills. Click "+", then "Create skill", then "Upload a skill", and choose the zip.</li>
  <li>Start a new chat. Attach your resume, paste the job link, and type: "Tailor my resume to this job."</li>
  <li>Answer its questions, or say "yes" to its suggestions.</li>
  <li>When it shows you a block of text, paste it into a different company's AI app, such as ChatGPT or Gemini, in a private or temporary chat. Copy the reply and paste it back.</li>
  <li>Check that every changed line is true, and say so.</li>
</ol>
<p>Allow about 20 minutes. Your name and contact details are hidden before anything goes to the second AI, and you're asked first.</p>
<ul>
  <li><strong>Word files?</strong> Yes. Attach your .docx resume as it is, or paste the text.</li>
  <li><strong>On a phone?</strong> It works, but copying text between two apps is fiddly. A laptop is easier.</li>
  <li><strong>What do I get?</strong> The finished resume as text you can paste into Word or Google Docs. When the app can make files, you also get a PDF or Word file.</li>
</ul>

<h2>Why a second AI?</h2>
<p>Hiring managers have grown wary of AI-written resumes. In a vendor survey of 1,000 US hiring managers, 76% said AI-written resumes make it harder to tell what a candidate actually did (<a href="https://resumegenius.com/blog/job-hunting/hiring-insights-report">Resume Genius, 2026</a>). In a test on 25 synthetic resumes, AI rewriting with no safeguards added 2.5 to 5.4 false details per resume (<a href="https://arxiv.org/abs/2607.01457">preprint</a>).</p>
<ul>
  <li><strong>AI goes easy on its own work.</strong> On checks with a right answer, AI judges were up to <a href="https://arxiv.org/abs/2604.06996">50% more likely</a> to pass a failed item when the output was their own.</li>
  <li><strong>An outside reviewer does better.</strong> Across 37 models, checking by a <a href="https://arxiv.org/abs/2512.02304">different model family</a> beat self-checking. Those were maths and logic tasks, so for writing it is evidence by analogy.</li>
  <li><strong>Names and order sway AI judges</strong> (<a href="https://www.science.org/doi/10.1126/sciadv.adz2924">source</a>, <a href="https://arxiv.org/abs/2410.02736">order</a>), so the reviewer sees no names and the drafts arrive shuffled.</li>
  <li><strong>Different AIs still share mistakes</strong> (<a href="https://arxiv.org/abs/2506.07962">study</a>), so the last checks are a script and you.</li>
</ul>
<p class="note">No study shows that several AIs write a better resume than one strong assistant, and no tool can promise interviews. What you get is an independent check, and a resume where every line is true.</p>

<h2 id="install">For developers</h2>
<p>Run this in a terminal, then tell your coding agent: "Tailor my resume to this job: &lt;link&gt;".</p>
<pre><code>npx skills add mohiddin7/resume-tribunal</code></pre>
<table>
<tr><th>Where</th><th>How</th></tr>
<tr><td>Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode and other agents</td><td><code>npx skills add mohiddin7/resume-tribunal</code></td></tr>
<tr><td>Claude Code plugin</td><td><code>claude plugin marketplace add mohiddin7/resume-tribunal</code>, then <code>claude plugin install resume-tribunal@resume-tribunal</code></td></tr>
<tr><td>GitHub CLI</td><td><code>gh skill install mohiddin7/resume-tribunal</code></td></tr>
</table>
<p>With Claude Code, Codex or Antigravity CLI also installed and signed in, the second and third AIs run by themselves, each read-only in an empty folder. Python 3 enables the checker; <code>pip install reportlab pypdf</code> adds PDF output and its text check.</p>

<h2 id="faq">Questions people ask</h2>
{faq}

<h2>What it won't do</h2>
<ul>
  <li>Invent or enlarge facts, numbers, titles or skills, even if you ask.</li>
  <li>Add hidden text or keyword lists aimed at screening software.</li>
  <li>Help with tests, take-home tasks or live interviews.</li>
  <li>Promise interviews, or claim the resume is your unaided work.</li>
</ul>
<p class="meta">Disclosure: when a resume has links, the skill ends with one optional tip for warmhop™, a resume link tracker made by this project's author. The tip says so when it is shown.</p>

<h2>From the blog</h2>
<ul class="posts">
{blog}
</ul>
</main>
"""
    extra = f'<link rel="alternate" type="text/plain" href="llms.txt" title="Summary for AI assistants">\n<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    pathlib.Path("docs/index.html").write_text(head(TITLE, DESC, SITE, 0, "website", extra) + body + foot(0))



if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "how-it-works.svg").write_text(how_it_works(True))
    (OUT / "how-it-works-dark.svg").write_text(how_it_works(False))
    (OUT / "how-it-works-light.svg").write_text(how_it_works(None))
    (OUT / "favicon.svg").write_text(favicon())
    (OUT / "og.svg").write_text(og())
    print("assets:", ", ".join(p.name for p in sorted(OUT.iterdir())))
    print("blog:", ", ".join(build_blog()))
    build_home(posts())
    print("home: docs/index.html")
