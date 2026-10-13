"""Drawings for the site and README: logo, the how-it-works flow, and the animated blog figures.

Every drawing is an SVG with colour tokens. variant=True follows the viewer's light or dark setting,
False is always dark, None is always light (used for GIF exports and GitHub's theme switch).
Animations use one shared cycle per drawing, with keyframes at absolute times, and stop for viewers
who ask for reduced motion.
"""
LIGHT = dict(bg="#f7f4ef", surf="#fffdf9", ink="#221e19", muted="#5f574d", line="#ddd5c8", brand="#a8515c",
             onbrand="#ffffff", blue="#35619a", green="#2f6c36", purple="#685497", danger="#a14126", tint="#f3e6e6")
DARK = dict(bg="#14120f", surf="#221e19", ink="#f3ede4", muted="#b5ab9e", line="#3a332b", brand="#d67a84",
            onbrand="#14120f", blue="#4e88d3", green="#479650", purple="#9177cf", danger="#db6141", tint="#3a2326")
FONT = 'system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif'


def theme(variant):
    tok = lambda t: ";".join(f"--{k}:{v}" for k, v in t.items())
    if variant is None:
        return f"svg{{{tok(LIGHT)}}}"
    if variant is False:
        return f"svg{{{tok(DARK)}}}"
    return f"svg{{{tok(LIGHT)}}}@media (prefers-color-scheme:dark){{svg{{{tok(DARK)}}}}}"


class Anim:
    """Collects keyframes on one cycle. at(name, [(seconds, css), ...]) returns a style attribute."""

    def __init__(self, cycle):
        self.cycle, self.css = cycle, []

    def at(self, name, frames, extra=""):
        stops = "".join(f"{min(100, 100 * t / self.cycle):.2f}%{{{css}}}" for t, css in frames)
        self.css.append(f"@keyframes {name}{{{stops}}}")
        return f'style="{extra}animation:{name} {self.cycle}s linear infinite"'

    def style(self):
        return "".join(self.css) + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def svg(w, h, variant, title, desc, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>'
            f"<style>{theme(variant)}text{{font-family:{FONT}}}{css}</style>"
            f'<rect width="{w}" height="{h}" rx="18" fill="var(--bg)"/>{body}</svg>\n')


# The mark: a fanned pile of resumes, with yours lifted out of it and on top. Standing out, picked.
def mark(x=0, y=0, s=1.0, tile=True):
    # The tile is always clay rose with white cards, in light and dark alike, like an app icon.
    c, t = ("#ffffff", "#a8515c") if tile else ("var(--brand)", "var(--bg)")
    cards = (f'<rect x="5" y="9" width="14" height="18" rx="2.6" fill="{c}" opacity=".3" transform="rotate(-14 12 18)"/>'
             f'<rect x="7" y="9" width="14" height="18" rx="2.6" fill="{c}" opacity=".55" transform="rotate(-6 14 18)"/>'
             f'<rect x="13" y="3.5" width="15" height="20" rx="2.6" fill="{c}" stroke="{t}" stroke-width="1.6"/>'
             f'<path d="M16.5 9h8M16.5 12.5h8M16.5 16h5" stroke="{t}" stroke-width="1.8" stroke-linecap="round"/>')
    g = f'<g transform="translate({x} {y}) scale({s})">'
    if tile:
        return g + f'<rect width="32" height="32" rx="8" fill="#a8515c"/><g transform="translate(3.5 4.5) scale(.75)">{cards}</g></g>'
    return g + cards + "</g>"


def favicon():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><style>{theme(True)}</style>'
            f"{mark()}</svg>\n")


def logo(variant):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 236 40" width="236" height="40" role="img" aria-label="Resume Tribunal">'
            f"<style>{theme(variant)}text{{font-family:{FONT}}}</style>{mark(0, 4)}"
            '<text x="42" y="27" font-size="20" font-weight="800" letter-spacing="-.4" fill="var(--ink)">Resume Tribunal</text></svg>\n')


def og():
    t = LIGHT
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<style>{theme(None)}text{{font-family:{FONT}}}</style>
<rect width="1200" height="630" fill="{t['bg']}"/>
{mark(80, 72, 1.9)}<text x="158" y="118" font-size="36" font-weight="800" fill="{t['ink']}">Resume Tribunal</text>
<text x="80" y="250" font-size="64" font-weight="800" letter-spacing="-2" fill="{t['ink']}">Not getting shortlisted?</text>
<text x="80" y="330" font-size="58" font-weight="800" letter-spacing="-2" fill="{t['brand']}">Fix your resume for the job</text>
<text x="80" y="398" font-size="58" font-weight="800" letter-spacing="-2" fill="{t['brand']}">in 5 minutes.</text>
<text x="80" y="462" font-size="28" fill="{t['muted']}">Works with ChatGPT, Gemini or any AI. Nothing made up. Free, no sign-up.</text>
<rect x="80" y="510" width="330" height="60" rx="30" fill="{t['brand']}"/>
<text x="245" y="549" text-anchor="middle" font-size="26" font-weight="700" fill="#fff">Free and open source</text>
</svg>
'''


# The six steps, shared by the README drawing and the website (tag, colour, title, line).
STEPS = [
    ("YOU", "green", "Share the job and your resume", "Paste the job link, attach your resume, and add a few words about what you really did."),
    ("AI 1 · YOUR AI", "blue", "It rewrites your resume for this job", "Uses the job's own words for the skills you really have, so you read like a match."),
    ("AI 2 · A DIFFERENT COMPANY", "brand", "A second AI reads it like the hiring manager", "Would they shortlist you? What's missing? It isn't told who wrote the draft."),
    ("AUTOMATIC CHECK", "purple", "A script checks the details", "A layout screening software can read, no AI-sounding phrases, no numbers you never gave."),
    ("YOU", "green", "You approve the changes", "Say yes to each one. Nothing goes in that you couldn't explain in an interview."),
    ("RESULT", "brand", "Your resume, ready to send", "Plus what the job asks for that you don't show yet, and the questions to expect."),
]
STEP_S, HOLD_S = 1.6, 2.4


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def how_it_works(variant):
    """README drawing: six cards light up one after another, a dot runs down each arrow, then it loops."""
    cycle = STEP_S * len(STEPS) + HOLD_S
    a, W, X, BW, GAP, y, out = Anim(round(cycle, 1)), 680, 40, 600, 30, 84, []
    end = STEP_S * len(STEPS) + HOLD_S * .7
    for i, (tag, col, title, line) in enumerate(STEPS):
        body = wrap(line, 66)
        h = 66 + 22 * len(body) + (46 if i == 2 else 0)
        t0 = i * STEP_S
        lit = a.at(f"l{i}", [(0, "opacity:0"), (t0, "opacity:0"), (t0 + .3, "opacity:1"), (end, "opacity:1"), (end + .5, "opacity:0"), (cycle, "opacity:0")])
        out.append(f'<rect x="{X}" y="{y}" width="{BW}" height="{h}" rx="14" fill="var(--surf)" stroke="var(--line)" stroke-width="1.5"/>'
                   f'<rect {lit} x="{X}" y="{y}" width="{BW}" height="{h}" rx="14" fill="var(--{col})" fill-opacity=".07" stroke="var(--{col})" stroke-width="2.5"/>'
                   f'<rect x="{X}" y="{y + 14}" width="5" height="{h - 28}" rx="2.5" fill="var(--{col})"/>'
                   f'<text x="{X + 24}" y="{y + 26}" font-size="12" font-weight="700" letter-spacing="1.2" fill="var(--{col})">{tag}</text>'
                   f'<text x="{X + 24}" y="{y + 50}" font-size="19" font-weight="800" fill="var(--ink)">{title}</text>'
                   + "".join(f'<text x="{X + 24}" y="{y + 73 + 22 * k}" font-size="15" fill="var(--muted)">{l}</text>' for k, l in enumerate(body)))
        if i == 2:
            cy, chips = y + 66 + 22 * len(body) + 2, ""
            for k, (label, dx) in enumerate([("Draft K", 368), ("Draft M", 0), ("Draft R", -368)]):
                mv = a.at(f"sw{k}", [(0, "transform:translateX(0)"), (t0 + .4, "transform:translateX(0)"), (t0 + 1.2, f"transform:translateX({dx}px)"),
                                     (end, f"transform:translateX({dx}px)"), (end + .6, "transform:translateX(0)"), (cycle, "transform:translateX(0)")]) if dx else ""
                cx = X + 24 + k * 184
                chips += (f'<g {mv}><rect x="{cx}" y="{cy}" width="168" height="26" rx="13" fill="var(--bg)" stroke="var(--line)"/>'
                          f'<text x="{cx + 84}" y="{cy + 17}" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">{label}</text></g>')
            out.append(chips)
        y += h
        if i < len(STEPS) - 1:
            dot = a.at(f"d{i}", [(0, "opacity:0;transform:translateY(0)"), (t0 + .8, "opacity:0;transform:translateY(0)"), (t0 + .9, "opacity:1;transform:translateY(0)"),
                                 (t0 + 1.5, f"opacity:1;transform:translateY({GAP - 12}px)"), (t0 + 1.6, f"opacity:0;transform:translateY({GAP - 12}px)"), (cycle, "opacity:0")])
            out.append(f'<path d="M{W / 2} {y + 5}V{y + GAP - 7}" stroke="var(--line)" stroke-width="2" stroke-linecap="round"/>'
                       f'<path d="M{W / 2 - 6} {y + GAP - 13}l6 7 6-7" fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                       f'<circle {dot} cx="{W / 2}" cy="{y + 6}" r="5" fill="var(--{STEPS[i + 1][1]})"/>')
            y += GAP
    H = y + 30
    head = (f'<text x="{X}" y="44" font-size="23" font-weight="800" fill="var(--ink)">How Resume Tribunal works</text>'
            f'<text x="{X}" y="66" font-size="14" fill="var(--muted)">About 5 minutes. Each step lights up in turn.</text>')
    desc = " ".join(f"Step {n}: {t}. {l}" for n, (_, _, t, l) in enumerate(STEPS, 1))
    return svg(W, H, variant, "How Resume Tribunal works", desc, head + "".join(out), a.style())


# Blog figures, 720 x 405 (16:9, the shape Medium and LinkedIn show best).
def fig_rejected(variant):
    a = Anim(9)
    strike = a.at("s", [(0, "stroke-dashoffset:470"), (1.6, "stroke-dashoffset:470"), (2.4, "stroke-dashoffset:0"), (8.4, "stroke-dashoffset:0"), (9, "stroke-dashoffset:470")])
    stamp = a.at("p", [(0, "opacity:0"), (2.5, "opacity:0;transform:scale(1.3)"), (2.8, "opacity:1;transform:scale(1)"), (8.4, "opacity:1"), (9, "opacity:0")], "transform-origin:602px 114px;")
    said = a.at("w", [(0, "opacity:0"), (3.4, "opacity:0"), (3.9, "opacity:1"), (8.4, "opacity:1"), (9, "opacity:0")])
    kept = a.at("k", [(0, "opacity:0"), (4.8, "opacity:0;transform:translateY(8px)"), (5.4, "opacity:1;transform:translateY(0)"), (8.4, "opacity:1"), (9, "opacity:0")])
    body = f'''<text x="40" y="52" font-size="15" font-weight="700" letter-spacing="1.5" fill="var(--muted)">A REVIEWING AI SUGGESTED</text>
<rect x="40" y="72" width="640" height="84" rx="14" fill="var(--surf)" stroke="var(--line)" stroke-width="1.5"/>
<text x="64" y="122" font-size="20" fill="var(--ink)">Cut report prep from 4 hours to 40 minutes</text>
<path {strike} d="M60 115 h420" stroke="var(--danger)" stroke-width="3.5" stroke-dasharray="470" stroke-linecap="round"/>
<g {stamp}><rect x="546" y="96" width="112" height="36" rx="18" fill="var(--danger)"/>
<text x="602" y="120" text-anchor="middle" font-size="16" font-weight="800" fill="#fff">Rejected</text></g>
<g {said}><text x="40" y="206" font-size="19" fill="var(--muted)">The candidate actually said: <tspan font-weight="700" fill="var(--ink)">"half a day"</tspan></text></g>
<g {kept}><rect x="40" y="236" width="640" height="84" rx="14" fill="var(--surf)" stroke="var(--green)" stroke-width="2.5"/>
<text x="64" y="285" font-size="20" fill="var(--ink)">Cut report prep from half a day to about 40 minutes</text>
<circle cx="646" cy="278" r="16" fill="var(--green)"/><path d="M638 278l6 6 10-11" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>
<text x="40" y="368" font-size="15" fill="var(--muted)">Resume Tribunal: the candidate's own words decide. From the worked example.</text>'''
    return svg(720, 405, variant, "A made-up number, rejected",
               'A reviewing AI suggested "cut report prep from 4 hours to 40 minutes". It is crossed out and marked rejected, because the '
               'candidate had said "half a day". The kept line reads "cut report prep from half a day to about 40 minutes".', body, a.style())


def fig_self_preference(variant):
    a = Anim(8)
    grow = lambda n, t: a.at(n, [(0, "transform:scaleX(0)"), (t, "transform:scaleX(0)"), (t + 1.2, "transform:scaleX(1)"), (7.4, "transform:scaleX(1)"), (8, "transform:scaleX(0)")], "transform-origin:40px 0;")
    label = a.at("lb", [(0, "opacity:0"), (3.2, "opacity:0"), (3.7, "opacity:1"), (7.4, "opacity:1"), (8, "opacity:0")])
    body = f'''<text x="40" y="56" font-size="26" font-weight="800" fill="var(--ink)">How often an AI judge passes a failed answer</text>
<text x="40" y="86" font-size="16" fill="var(--muted)">Same mistakes, judged by the AI that made them or by another AI</text>
<text x="40" y="150" font-size="17" font-weight="700" fill="var(--ink)">Another AI's answer</text>
<rect x="40" y="164" width="640" height="42" rx="10" fill="var(--surf)" stroke="var(--line)"/>
<rect {grow("g1", .4)} x="40" y="164" width="300" height="42" rx="10" fill="var(--muted)"/>
<text x="40" y="256" font-size="17" font-weight="700" fill="var(--ink)">Its own answer</text>
<rect x="40" y="270" width="640" height="42" rx="10" fill="var(--surf)" stroke="var(--line)"/>
<rect {grow("g2", 1.6)} x="40" y="270" width="456" height="42" rx="10" fill="var(--brand)"/>
<g {label}><text x="680" y="256" text-anchor="end" font-size="18" font-weight="800" fill="var(--brand)">up to 50%+ more</text></g>
<text x="40" y="364" font-size="14" fill="var(--muted)">Illustration. Source: Pombal, Rei and Martins, 2026 (preprint).</text>'''
    return svg(720, 405, variant, "AI judges go easy on their own mistakes",
               "Two bars. An AI judge checking another AI's answers passes some failed answers. Checking its own answers, it passes "
               "up to 50 percent more of them.", body, a.style())


def fig_manual_vs_skill(variant):
    a, cards = Anim(10), []
    for i in range(16):
        x, y, t = 52 + (i % 4) * 66, 116 + (i // 4) * 50, .2 + i * .18
        st = a.at(f"c{i}", [(0, "opacity:0"), (t, "opacity:0"), (t + .15, "opacity:1"), (9.4, "opacity:1"), (10, "opacity:0")])
        cards.append(f'<rect {st} x="{x}" y="{y}" width="56" height="40" rx="7" fill="var(--surf)" stroke="var(--line)"/>'
                     f'<path {st} d="M{x + 9} {y + 14}h38M{x + 9} {y + 24}h26" stroke="var(--muted)" stroke-width="3" stroke-linecap="round"/>')
    bubble = a.at("b", [(0, "opacity:0"), (3.6, "opacity:0;transform:translateY(10px)"), (4.2, "opacity:1;transform:translateY(0)"), (9.4, "opacity:1"), (10, "opacity:0")])
    done = a.at("dn", [(0, "opacity:0"), (5.2, "opacity:0"), (5.8, "opacity:1"), (9.4, "opacity:1"), (10, "opacity:0")])
    body = f'''<text x="40" y="60" font-size="15" font-weight="700" letter-spacing="1.5" fill="var(--muted)">BY HAND</text>
{"".join(cards)}
<text x="40" y="350" font-size="16" font-weight="700" fill="var(--ink)">16 prompts · 3 tabs · hours</text>
<path d="M352 70v290" stroke="var(--line)" stroke-width="2"/>
<text x="392" y="60" font-size="15" font-weight="700" letter-spacing="1.5" fill="var(--brand)">WITH RESUME TRIBUNAL</text>
<g {bubble}><rect x="392" y="130" width="296" height="60" rx="20" fill="var(--brand)"/>
<text x="410" y="166" font-size="17" font-weight="700" fill="var(--onbrand)">Tailor my resume to this job</text></g>
<g {done}><rect x="392" y="214" width="250" height="52" rx="16" fill="var(--surf)" stroke="var(--line)"/>
<circle cx="420" cy="240" r="12" fill="var(--green)"/><path d="M414 240l4 4 8-8" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
<text x="442" y="247" font-size="17" fill="var(--ink)">Drafted, checked, ready</text></g>
<text x="392" y="350" font-size="16" font-weight="700" fill="var(--ink)">1 message · about 5 minutes</text>'''
    return svg(720, 405, variant, "By hand versus with Resume Tribunal",
               "Left, sixteen prompt cards appear one by one: 16 prompts, 3 chat tabs, hours. Right, one message, tailor my resume "
               "to this job, and a note: drafted, checked, ready. One message, about 5 minutes.", body, a.style())


def fig_blind_check(variant):
    a = Anim(9)
    move = a.at("mv", [(0, "transform:translateX(0)"), (1.2, "transform:translateX(0)"), (2.6, "transform:translateX(342px)"), (8.4, "transform:translateX(342px)"), (9, "transform:translateX(0)")])
    tag = a.at("tg", [(0, "opacity:1"), (1.1, "opacity:1"), (1.5, "opacity:0"), (8.6, "opacity:0"), (9, "opacity:1")])
    anon = a.at("an", [(0, "opacity:0"), (2.6, "opacity:0"), (3.0, "opacity:1"), (8.4, "opacity:1"), (9, "opacity:0")])
    q = a.at("q", [(0, "opacity:0"), (3.4, "opacity:0"), (3.9, "opacity:1"), (8.4, "opacity:1"), (9, "opacity:0")])
    ok = a.at("ok", [(0, "opacity:0"), (5.0, "opacity:0"), (5.5, "opacity:1"), (8.4, "opacity:1"), (9, "opacity:0")])
    body = f'''<rect x="40" y="70" width="250" height="250" rx="18" fill="var(--surf)" stroke="var(--blue)" stroke-width="2"/>
<text x="64" y="106" font-size="15" font-weight="700" letter-spacing="1.5" fill="var(--blue)">AI 1 · WRITES</text>
<rect x="430" y="70" width="250" height="250" rx="18" fill="var(--surf)" stroke="var(--brand)" stroke-width="2"/>
<text x="454" y="106" font-size="15" font-weight="700" letter-spacing="1.5" fill="var(--brand)">AI 2 · CHECKS</text>
<text x="165" y="300" text-anchor="middle" font-size="14" fill="var(--muted)">writes the draft</text>
<text x="454" y="128" font-size="14" fill="var(--muted)">from a different company</text>
<g {move}><rect x="96" y="150" width="128" height="150" rx="10" fill="var(--bg)" stroke="var(--line)"/>
<path d="M114 182h92M114 204h92M114 226h70M114 248h84" stroke="var(--muted)" stroke-width="5" stroke-linecap="round"/>
<g {tag}><rect x="104" y="270" width="112" height="22" rx="11" fill="var(--blue)"/><text x="160" y="286" text-anchor="middle" font-size="12" font-weight="700" fill="var(--onbrand)">written by AI 1</text></g>
<g {anon}><rect x="116" y="270" width="88" height="22" rx="11" fill="var(--muted)"/><text x="160" y="286" text-anchor="middle" font-size="12" font-weight="700" fill="var(--bg)">Draft K</text></g></g>
<g {q}><text x="555" y="352" text-anchor="middle" font-size="17" fill="var(--ink)">Who wrote this? <tspan font-weight="800">It isn't told.</tspan></text></g>
<g {ok}><rect x="40" y="338" width="250" height="34" rx="17" fill="var(--tint)"/><text x="165" y="361" text-anchor="middle" font-size="15" font-weight="700" fill="var(--brand)">No AI grades its own work</text></g>
<text x="40" y="44" font-size="22" font-weight="800" fill="var(--ink)">The check that makes the difference</text>'''
    return svg(720, 405, variant, "A blind check by a different AI",
               "A draft written by AI 1 moves to AI 2, from a different company. On the way its label changes from written by AI 1 "
               "to Draft K, so the checker is not told who wrote it. No AI grades its own work.", body, a.style())


def fig_ats_myth(variant):
    a = Anim(8)
    stamp = a.at("st", [(0, "opacity:0"), (1.8, "opacity:0;transform:rotate(-8deg) scale(1.6)"), (2.2, "opacity:1;transform:rotate(-8deg) scale(1)"), (7.4, "opacity:1;transform:rotate(-8deg) scale(1)"), (8, "opacity:0")], "transform-origin:550px 200px;")
    fact = a.at("f", [(0, "opacity:0"), (3.0, "opacity:0"), (3.5, "opacity:1"), (7.4, "opacity:1"), (8, "opacity:0")])
    body = f'''<text x="40" y="60" font-size="15" font-weight="700" letter-spacing="1.5" fill="var(--muted)">YOU'VE PROBABLY READ THIS</text>
<text x="40" y="128" font-size="34" font-weight="800" fill="var(--ink)">"75% of resumes are rejected</text>
<text x="40" y="172" font-size="34" font-weight="800" fill="var(--ink)">by ATS before a human</text>
<text x="40" y="216" font-size="34" font-weight="800" fill="var(--ink)">sees them"</text>
<g {stamp}><rect x="440" y="168" width="220" height="64" rx="10" fill="var(--bg)" stroke="var(--danger)" stroke-width="5"/>
<text x="550" y="211" text-anchor="middle" font-size="28" font-weight="900" letter-spacing="2" fill="var(--danger)">NO SOURCE</text></g>
<g {fact}><text x="40" y="286" font-size="20" fill="var(--ink)">The figure traces back to a vendor that closed in 2013.</text>
<text x="40" y="316" font-size="20" fill="var(--ink)">Most resumes are turned down by people, not software.</text></g>
<text x="40" y="364" font-size="14" fill="var(--muted)">Sources: HRTact (2020); Greenhouse Talent Matching FAQ.</text>'''
    return svg(720, 405, variant, "The 75 percent ATS myth",
               'A quote, "75% of resumes are rejected by ATS before a human sees them", is stamped NO SOURCE. The figure traces back '
               "to a vendor that closed in 2013. Most resumes are turned down by people, not software.", body, a.style())


FIGURES = {"rejected-claims": (fig_rejected, 9), "self-preference": (fig_self_preference, 8),
           "manual-vs-skill": (fig_manual_vs_skill, 10), "blind-check": (fig_blind_check, 9), "ats-myth": (fig_ats_myth, 8)}
