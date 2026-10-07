#!/usr/bin/env python3
"""Generates the animated SVGs used by README.md. Run: python3 scripts/build_assets.py

Palette is taken from siddharth.wiki. SVGs are self-contained (system fonts only)
and animate with CSS/SMIL, which GitHub renders inside <img>.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

BG, SURFACE, RULE = "#0a0f15", "#12171f", "#282e35"
FG, MUTED, ACCENT, ACCENT_SOFT = "#f0eee8", "#959ba5", "#dd8f66", "#a44b25"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "'SF Mono', 'Martian Mono', ui-monospace, Menlo, Consolas, monospace"
SANS = "'Instrument Sans', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def write(name, svg):
    (OUT / name).write_text(svg, encoding="utf-8")
    print("wrote", name, len(svg), "bytes")


# --------------------------------------------------------------------- header
def header():
    roles = [
        "backend engineer",
        "building AI systems on AWS",
        "founder, DevToolie",
        "MS CS @ Arizona State",
    ]
    n, dur = len(roles), 3.2
    role_svg = ""
    for i, r in enumerate(roles):
        delay = i * dur
        role_svg += (
            f'<text class="role" x="80" y="232" style="animation-delay:{delay}s">'
            f'<tspan fill="{ACCENT}">&gt; </tspan>{escape(r)}<tspan class="cur" fill="{ACCENT}">_</tspan></text>'
        )
    total = n * dur
    # grid dots
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1" fill="{RULE}"/>'
        for x in range(40, 1200, 40)
        for y in range(40, 360, 40)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-label="Siddharth Mehta, backend engineer">
<defs>
  <radialGradient id="g1" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{ACCENT}" stop-opacity=".55"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#5b7fa6" stop-opacity=".35"/><stop offset="1" stop-color="#5b7fa6" stop-opacity="0"/></radialGradient>
  <linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>
  <clipPath id="c"><rect width="1200" height="360" rx="20"/></clipPath>
</defs>
<style>
  .name{{font:italic 400 84px {SERIF};fill:{FG};letter-spacing:-2px}}
  .eyebrow{{font:500 13px {MONO};fill:{MUTED};letter-spacing:3px}}
  .role{{font:500 22px {MONO};fill:{FG};opacity:0;animation:role {total}s infinite}}
  .cur{{animation:blink 1s steps(1) infinite}}
  .orb1{{animation:d1 14s ease-in-out infinite alternate}}
  .orb2{{animation:d2 18s ease-in-out infinite alternate}}
  .rise{{animation:rise 1.1s cubic-bezier(.2,.7,.2,1) both}}
  .rise2{{animation:rise 1.1s .15s cubic-bezier(.2,.7,.2,1) both}}
  .draw{{stroke-dasharray:420;stroke-dashoffset:420;animation:draw 1.6s .5s ease-out forwards}}
  @keyframes role{{0%{{opacity:0;transform:translateY(10px)}}2%{{opacity:1;transform:none}}{100/n-3:.2f}%{{opacity:1;transform:none}}{100/n:.2f}%{{opacity:0;transform:translateY(-10px)}}100%{{opacity:0}}}}
  @keyframes blink{{50%{{opacity:0}}}}
  @keyframes d1{{to{{transform:translate(120px,40px)}}}}
  @keyframes d2{{to{{transform:translate(-140px,-30px)}}}}
  @keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  {REDUCE}
</style>
<g clip-path="url(#c)">
  <rect width="1200" height="360" fill="{BG}"/>
  <g opacity=".7">{dots}</g>
  <circle class="orb1" cx="900" cy="80" r="260" fill="url(#g1)"/>
  <circle class="orb2" cx="1050" cy="300" r="240" fill="url(#g2)"/>
  <rect x=".5" y=".5" width="1199" height="359" rx="20" fill="none" stroke="{RULE}"/>
  <text class="eyebrow rise" x="80" y="84">PORTFOLIO &#183; GITHUB / MYSELFSIDDHARTH</text>
  <text class="name rise2" x="76" y="172">Siddharth Mehta</text>
  <path class="draw" d="M80 194 H500" stroke="url(#line)" stroke-width="2"/>
  {role_svg}
  <g font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="2">
    <text x="1120" y="318" text-anchor="end">TEMPE, AZ &#183; USA</text>
  </g>
</g>
</svg>"""


# ---------------------------------------------------------------- section bar
def divider(name, label):
    w = 1200
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="64" viewBox="0 0 {w} 64" role="img" aria-label="{escape(label)}">
<style>
  .t{{font:500 13px {MONO};fill:{ACCENT};letter-spacing:4px}}
  .l{{stroke-dasharray:{w};stroke-dashoffset:{w};animation:s 1.6s ease-out forwards}}
  .p{{animation:p 2.4s ease-in-out infinite}}
  @keyframes s{{to{{stroke-dashoffset:0}}}}
  @keyframes p{{50%{{opacity:.25}}}}
  {REDUCE}
</style>
<circle class="p" cx="8" cy="32" r="4" fill="{ACCENT}"/>
<text class="t" x="26" y="37">{escape(label.upper())}</text>
<line class="l" x1="{26 + len(label)*13 + 24}" y1="32" x2="{w}" y2="32" stroke="{RULE}" stroke-width="1"/>
</svg>"""


# ------------------------------------------------------------ numbers strip
def numbers():
    items = [
        ("10,000+", "students served by the\nTutorBot RAG platform"),
        ("4.0", "GPA in the MS in CS\nat Arizona State"),
        ("4x", "hackathon winner,\nlatest: VillageHacks '26"),
        ("vscode", "fixes contributed to\nmicrosoft/vscode"),
    ]
    w, h, gap = 282, 150, 24
    total = 4 * w + 3 * gap
    body = ""
    for i, (big, small) in enumerate(items):
        x = i * (w + gap)
        lines = "".join(
            f'<text x="24" y="{104 + j*20}" class="s">{escape(l)}</text>' for j, l in enumerate(small.split("\n"))
        )
        body += f"""<g class="card" style="animation-delay:{i*.12}s" transform="translate({x},0)">
  <rect width="{w}" height="{h}" rx="16" fill="{SURFACE}" stroke="{RULE}"/>
  <rect x="24" y="24" width="28" height="3" rx="1.5" fill="{ACCENT}"/>
  <text x="24" y="76" class="b">{escape(big)}</text>
  {lines}
</g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{h}" viewBox="0 0 {total} {h}" role="img" aria-label="Highlights">
<style>
  .b{{font:italic 400 38px {SERIF};fill:{FG};letter-spacing:-1px}}
  .s{{font:400 13px {SANS};fill:{MUTED}}}
  .card{{opacity:0;animation:in .8s cubic-bezier(.2,.7,.2,1) forwards}}
  @keyframes in{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1}}}}
  {REDUCE}
</style>
{body}
</svg>"""


# ------------------------------------------------------------ project cards
def project(name, title, kind, desc, tags, stars, accent=ACCENT, badge=None):
    w, h = 588, 214
    # wrap description at ~62 chars
    words, lines, cur = desc.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > 64:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    d = "".join(f'<text x="28" y="{108 + i*22}" class="d">{escape(l)}</text>' for i, l in enumerate(lines[:3]))
    tx, tag_svg = 28, ""
    for t in tags:
        tw = len(t) * 7.4 + 22
        tag_svg += (
            f'<rect x="{tx}" y="168" width="{tw:.0f}" height="26" rx="13" fill="none" stroke="{RULE}"/>'
            f'<text x="{tx + tw/2:.0f}" y="185" text-anchor="middle" class="tg">{escape(t)}</text>'
        )
        tx += tw + 8
    badge_svg = ""
    if badge:
        bw = len(badge) * 7.2 + 24
        badge_svg = (
            f'<rect x="{w - 28 - bw:.0f}" y="24" width="{bw:.0f}" height="26" rx="13" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".5"/>'
            f'<text x="{w - 28 - bw/2:.0f}" y="41" text-anchor="middle" class="bd">{escape(badge)}</text>'
        )
    star = f'<text x="{w-28}" y="{h-20}" text-anchor="end" class="st">&#9733; {stars}</text>' if stars else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}: {escape(desc)}">
<defs>
  <radialGradient id="glow" cx="100%" cy="0%" r="90%"><stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <clipPath id="cl"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<style>
  .k{{font:500 11px {MONO};fill:{accent};letter-spacing:3px}}
  .h{{font:italic 400 30px {SERIF};fill:{FG};letter-spacing:-.5px}}
  .d{{font:400 14.5px {SANS};fill:{MUTED}}}
  .tg{{font:500 11px {MONO};fill:{FG}}}
  .bd{{font:600 11px {MONO};fill:{accent};letter-spacing:1px}}
  .st{{font:500 12px {MONO};fill:{MUTED}}}
  .sweep{{animation:sw 7s ease-in-out infinite}}
  @keyframes sw{{0%,60%{{transform:translateX(-120px)}}100%{{transform:translateX({w+120}px)}}}}
  {REDUCE}
</style>
<g clip-path="url(#cl)">
  <rect width="{w}" height="{h}" fill="{SURFACE}"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect class="sweep" x="0" y="0" width="60" height="{h}" fill="{FG}" opacity=".035" transform="skewX(-20)"/>
  <text x="28" y="40" class="k">{escape(kind.upper())}</text>
  <text x="28" y="76" class="h">{escape(title)}</text>
  {d}
  {tag_svg}
  {badge_svg}
  {star}
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{RULE}"/>
</svg>"""


# ------------------------------------------------------------------- stack
def stack():
    rows = [
        ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "SQL", "Solidity"]),
        ("BACKEND & CLOUD", ["AWS", "Node.js", "Express", "Django", "Flask", "PostgreSQL", "Docker", "Kubernetes", "Terraform"]),
        ("AI / ML", ["RAG", "LLM agents", "PyTorch", "XGBoost", "LSTM / GRU", "NetworkX"]),
        ("DATA & INFRA", ["Neo4j", "Kafka", "Stripe", "GitHub Actions", "MapLibre"]),
    ]
    w, rh = 1200, 76
    h = rh * len(rows) + 8
    out = ""
    for ri, (label, items) in enumerate(rows):
        y = ri * rh
        out += f'<text x="0" y="{y+28}" class="lb">{escape(label)}</text>'
        x = 0
        for ci, it in enumerate(items):
            tw = len(it) * 8.6 + 34
            delay = (ri * 0.15 + ci * 0.06)
            out += (
                f'<g class="chip" style="animation-delay:{delay:.2f}s" transform="translate({x:.0f},{y+38})">'
                f'<rect width="{tw:.0f}" height="30" rx="15" fill="{SURFACE}" stroke="{RULE}"/>'
                f'<circle cx="16" cy="15" r="3" fill="{ACCENT}"/>'
                f'<text x="28" y="20" class="ch">{escape(it)}</text></g>'
            )
            x += tw + 10
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tech stack">
<style>
  .lb{{font:500 11px {MONO};fill:{MUTED};letter-spacing:3px}}
  .ch{{font:500 13px {MONO};fill:{FG}}}
  .chip{{opacity:0;animation:in .6s cubic-bezier(.2,.7,.2,1) forwards}}
  @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1}}}}
  {REDUCE}
</style>
{out}
</svg>"""


# ------------------------------------------------------------------ footer
def footer():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="140" viewBox="0 0 1200 140" role="img" aria-label="Let's build something">
<defs>
  <linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset=".5" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>
  <clipPath id="c"><rect width="1200" height="140" rx="20"/></clipPath>
</defs>
<style>
  .f{{font:italic 400 40px {SERIF};fill:{FG};letter-spacing:-1px}}
  .s{{font:500 12px {MONO};fill:{MUTED};letter-spacing:3px}}
  .w1{{animation:w 9s linear infinite}}
  .w2{{animation:w 14s linear infinite reverse}}
  @keyframes w{{to{{transform:translateX(-600px)}}}}
  {REDUCE}
</style>
<g clip-path="url(#c)">
  <rect width="1200" height="140" fill="{BG}"/>
  <g opacity=".5"><path class="w1" d="M0 122 q150 -30 300 0 t300 0 t300 0 t300 0 t300 0 t300 0" fill="none" stroke="url(#a)" stroke-width="2"/></g>
  <g opacity=".3"><path class="w2" d="M0 128 q150 24 300 0 t300 0 t300 0 t300 0 t300 0 t300 0" fill="none" stroke="{ACCENT_SOFT}" stroke-width="1.5"/></g>
  <text class="s" x="600" y="48" text-anchor="middle">THANKS FOR STOPPING BY</text>
  <text class="f" x="600" y="92" text-anchor="middle">Let's build something good.</text>
  <rect x=".5" y=".5" width="1199" height="139" rx="20" fill="none" stroke="{RULE}"/>
</g>
</svg>"""


if __name__ == "__main__":
    write("header.svg", header())
    write("footer.svg", footer())
    write("numbers.svg", numbers())
    write("stack.svg", stack())
    for nm, lab in [("about", "About"), ("highlights", "Highlights"), ("work", "Selected work"),
                    ("stack-title", "Toolbox"), ("research", "Research"), ("connect", "Connect")]:
        write(f"h-{nm}.svg", divider(nm, lab))
    write("p-flecto.svg", project("flecto", "Flecto", "DevOps · npm · GitHub Action",
        "Reads your Terraform plan and Kubernetes changes and posts a plain-English risk summary on every pull request, blocking the dangerous ones.",
        ["JavaScript", "Terraform", "Kubernetes"], 7, badge="ON NPM"))
    write("p-paragent.svg", project("paragent", "Paragent", "AI agents · DevToolie",
        "A stateful execution layer for browser agents. Record an agent once, then replay it with no model in the loop.",
        ["TypeScript", "Browser agents", "Replay"], 6, accent="#7fa7d6", badge="DEVTOOLIE"))
    write("p-griefos.svg", project("griefos", "GriefOS", "AI · Healthcare",
        "A therapy agent built on a recall memory architecture, tracking how themes and confidence evolve across a session.",
        ["TypeScript", "Claude", "Memory"], 3, accent="#b9a3e3", badge="HACKATHON WINNER"))
    write("p-sonic.svg", project("sonic", "Sonic Cartography", "Data viz · Full stack",
        "Interactive globe that maps your Spotify artists to the real-world cities they came from, colored by genre and clustered as you zoom.",
        ["Python", "Flask", "MapLibre"], 9, accent="#6fcf97", badge="LIVE DEMO"))
