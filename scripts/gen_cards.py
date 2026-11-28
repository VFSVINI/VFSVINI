"""Gera os cards dinamicos (ficha do Jedi, linguagens, selos, missoes) com texto em contornos.

Uso: GITHUB_TOKEN=... GITHUB_USER=VFSVINI python scripts/gen_cards.py [pasta_saida]
Sem JavaScript: SMIL/CSS dentro de SVG, que o GitHub renderiza via <img>.
"""
import math
from xml.sax.saxutils import escape

import gen_stats as gs
from fontkit import GOTHIC, JEDI, text_path, text_width

OUT = gs.OUT
YELLOW, BLUE, GREEN, RED = "#FFE81F", "#4BD5EE", "#4CFF4C", "#FF5A5A"
MISSIONS = ["meridian-wealth", "FleetTrack-Realtime", "Vortex-Engine", "heloc-streamlit"]


def frame(w, h, title, inner, uid):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
<linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b18"/><stop offset="1" stop-color="#0d1530"/></linearGradient>
<linearGradient id="saber{uid}" x1="0" x2="1"><stop offset="0" stop-color="#1fb81f"/><stop offset="1" stop-color="#9dff9d"/></linearGradient>
<linearGradient id="sith{uid}" x1="0" x2="1"><stop offset="0" stop-color="#b80f0f"/><stop offset="1" stop-color="#ff7a7a"/></linearGradient>
<linearGradient id="scan{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.5" stop-color="{BLUE}" stop-opacity="0.13"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<radialGradient id="sun{uid}"><stop offset="0" stop-color="#fff7b0"/><stop offset="0.5" stop-color="{YELLOW}"/><stop offset="1" stop-color="#ff9d00" stop-opacity="0"/></radialGradient>
<filter id="glow{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="clip{uid}"><rect width="{w}" height="{h}" rx="12"/></clipPath>
</defs>
<g clip-path="url(#clip{uid})">
<rect width="{w}" height="{h}" fill="url(#bg{uid})"/>
<rect y="-60" width="{w}" height="60" fill="url(#scan{uid})"><animate attributeName="y" values="-60;{h}" dur="5s" repeatCount="indefinite"/></rect>
{inner}
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="none" stroke="{YELLOW}" stroke-opacity="0.55"/>
<path d="M10 28V10h18M{w - 28} 10h18v18M{w - 10} {h - 28}v18h-18M28 {h - 10}H10v-18" fill="none" stroke="{YELLOW}" stroke-width="2"/>
</svg>
"""


def num(n):
    return f"{n:,}".replace(",", ".")


def card_rank(d):
    xp = gs.xp_of(d)
    idx, name, nxt_min, nxt_name, prog = gs.rank_of(xp)
    _, _, char, side = gs.RANKS[idx]
    nxt_char = gs.RANKS[min(idx + 1, len(gs.RANKS) - 1)][2]
    accent = BLUE if side == "light" else RED
    bar = "saberrank" if side == "light" else "sithrank"
    level = int(math.sqrt(xp / 10)) + 1
    w, h = 495, 232
    rows = [
        ("COMMITS", d["commits"], BLUE),
        ("PULL REQUESTS", d["prs"], GREEN),
        ("ISSUES", d["issues"], YELLOW),
        ("CODE REVIEWS", d["reviews"], "#c58cff"),
        ("STARS", d["stars"], "#ffb347"),
        ("MISSIONS (REPOS)", d["repos"], RED),
    ]
    inner = [
        text_path(JEDI, "JEDI DOSSIER", 15, 3, 26, 36, YELLOW),
        text_path(GOTHIC, d["name"].upper(), 12, 2, w - 24, 36, "#6b7aa8", "end"),
    ]
    for i, (lab, val, col) in enumerate(rows):
        y = 70 + i * 22
        inner.append(f'<circle cx="32" cy="{y - 4}" r="3.5" fill="{col}" filter="url(#glowrank)"/>')
        inner.append(text_path(GOTHIC, lab, 13, 1.5, 46, y, "#8ea3d6"))
        inner.append(text_path(GOTHIC, num(val), 16, 0.5, 262, y, "#ffffff", "end"))
    cx, cy, r = 386, 100, 44
    circ = 2 * math.pi * r
    off = circ * (1 - prog)
    inner.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1b2745" stroke-width="8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" stroke-width="8" stroke-linecap="round" '
        f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {cx} {cy})" filter="url(#glowrank)">'
        f'<animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="{off:.1f}" dur="2.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/></circle>'
    )
    inner.append(text_path(GOTHIC, "LEVEL", 12, 3, cx, cy - 10, "#8ea3d6", "middle"))
    inner.append(text_path(JEDI, str(level), 36, 2, cx, cy + 26, "#ffffff", "middle"))
    inner.append(text_path(JEDI, name, 13, 2, cx, cy + 66, YELLOW, "middle", max_w=170))
    inner.append(text_path(GOTHIC, char, 13, 2.2, cx, cy + 84, accent, "middle", max_w=170))
    bw = w - 52
    if nxt_min != gs.RANKS[idx][0]:
        label = f"XP {num(xp)} / {num(nxt_min)}   NEXT: {nxt_char}"
    else:
        label = f"XP {num(xp)}   MAX LEVEL"
    inner.append(text_path(GOTHIC, label, 12, 1.5, 26, 199, "#8ea3d6", max_w=330))
    inner.append(
        f'<rect x="26" y="206" width="{bw}" height="9" rx="4.5" fill="#1b2745"/>'
        f'<rect x="26" y="206" width="0" height="9" rx="4.5" fill="url(#{bar})" filter="url(#glowrank)">'
        f'<animate attributeName="width" from="0" to="{bw * prog:.1f}" dur="2.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/></rect>'
    )
    title = f"Jedi dossier: {char}, {name}, level {level}, {xp} XP"
    (OUT / "rank.svg").write_text(frame(w, h, title, "\n".join(inner), "rank"), encoding="utf-8")


def ladder(d):
    """Escada de patentes: do mais fraco ao mais poderoso, com a posicao atual destacada."""
    xp = gs.xp_of(d)
    cur = gs.rank_of(xp)[0]
    n = len(gs.RANKS)
    w, h = 900, 176
    step = (w - 80) / (n - 1)
    y0 = 78
    xs = [40 + i * step for i in range(n)]
    inner = [
        text_path(JEDI, "RANK LADDER", 15, 3, 26, 36, YELLOW),
        text_path(GOTHIC, "FROM THE WEAKEST TO THE MOST POWERFUL", 11, 3, w - 24, 36, "#6b7aa8", "end"),
        f'<line x1="{xs[0]}" y1="{y0}" x2="{xs[-1]}" y2="{y0}" stroke="#1b2745" stroke-width="4" stroke-linecap="round"/>',
        f'<line x1="{xs[0]}" y1="{y0}" x2="{xs[cur]}" y2="{y0}" stroke="url(#saberladder)" stroke-width="4" stroke-linecap="round" filter="url(#glowladder)"/>',
    ]
    for i, (mn, title, char, side) in enumerate(gs.RANKS):
        x = xs[i]
        col = BLUE if side == "light" else RED
        reached = i <= cur
        fill = col if reached else "#0b1226"
        flt = ' filter="url(#glowladder)"' if reached else ""
        pulse = '<animate attributeName="r" values="10;14;10" dur="2s" repeatCount="indefinite"/>' if i == cur else ""
        inner.append(
            f'<circle cx="{x:.1f}" cy="{y0}" r="{11 if i == cur else 8}" fill="{fill}" stroke="{col}" stroke-width="2" '
            f'opacity="{1 if reached else 0.55}"{flt}>{pulse}</circle>'
        )
        inner.append(text_path(GOTHIC, num(mn), 10, 1.2, x, y0 - 22, "#8ea3d6" if reached else "#4a5a8f", "middle"))
        inner.append(text_path(GOTHIC, char, 11.5, 1, x, y0 + 36, "#ffffff" if reached else "#5a6a9f", "middle", max_w=step - 8))
        inner.append(text_path(GOTHIC, title, 9.5, 1.3, x, y0 + 52, col if reached else "#4a5a8f", "middle", max_w=step - 6))
        if i == cur:
            inner.append(f'<path d="M{x:.1f} {y0 + 62}l-5 8h10z" fill="{YELLOW}"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></path>')
            inner.append(text_path(JEDI, "YOU ARE HERE", 10, 2, x, y0 + 90, YELLOW, "middle"))
    label = f"Rank ladder: current rank {gs.RANKS[cur][1]}, {gs.RANKS[cur][2]}"
    (OUT / "ladder.svg").write_text(frame(w, h, label, "\n".join(inner), "ladder"), encoding="utf-8")


def card_galaxy(d):
    langs = d["langs"][:6]
    total = sum(v["size"] for _, v in d["langs"]) or 1
    w, h = 495, 232
    cx, cy = 128, 124
    inner = [text_path(JEDI, "LANGUAGE SYSTEM", 15, 3, 26, 36, YELLOW)]
    inner.append(
        f'<circle cx="{cx}" cy="{cy}" r="34" fill="url(#sungalaxy)"><animate attributeName="r" values="30;36;30" dur="4s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="11" fill="#fff7b0"/>'
    )
    biggest = max((v["size"] for _, v in langs), default=1)
    for i, (name, v) in enumerate(langs):
        orbit = 42 + i * 14
        pr = 4.5 + 8 * (v["size"] / biggest) ** 0.5
        start = (i * 67) % 360
        dur = 9 + i * 5.5
        inner.append(
            f'<circle cx="{cx}" cy="{cy}" r="{orbit}" fill="none" stroke="#2a3a6b" stroke-width="1" stroke-dasharray="2 4"/>'
            f'<g><animateTransform attributeName="transform" type="rotate" from="{start} {cx} {cy}" to="{start + 360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<circle cx="{cx + orbit}" cy="{cy}" r="{pr:.1f}" fill="{v["color"]}" filter="url(#glowgalaxy)"/></g>'
        )
    for i, (name, v) in enumerate(langs):
        y = 72 + i * 25
        share = v["size"] / total
        inner.append(f'<circle cx="290" cy="{y - 4}" r="5" fill="{v["color"]}"/>')
        inner.append(text_path(GOTHIC, name.upper(), 14, 1.2, 304, y, "#8ea3d6", max_w=110))
        inner.append(text_path(GOTHIC, f"{share * 100:.1f}%", 15, 0.5, w - 26, y, "#ffffff", "end"))
        inner.append(
            f'<rect x="290" y="{y + 6}" width="{w - 316}" height="2.5" rx="1.2" fill="#1b2745"/>'
            f'<rect x="290" y="{y + 6}" width="0" height="2.5" rx="1.2" fill="{v["color"]}"><animate attributeName="width" from="0" to="{(w - 316) * share:.1f}" dur="2s" fill="freeze"/></rect>'
        )
    (OUT / "galaxy.svg").write_text(frame(w, h, "Solar system of the most used languages", "\n".join(inner), "galaxy"), encoding="utf-8")


def pill(slug, label, value, color, aria):
    pad, gap = 16, 14
    lw = text_width(GOTHIC, label, 13, 2.2)
    vw = text_width(JEDI, value, 13, 2)
    w = pad + lw + gap + gap + vw + pad
    h = 38
    split = pad + lw + gap
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" viewBox="0 0 {w:.0f} {h}" role="img" aria-label="{escape(aria)}">
<title>{escape(aria)}</title>
<defs><clipPath id="c{slug}"><rect width="{w:.0f}" height="{h}" rx="6"/></clipPath></defs>
<g clip-path="url(#c{slug})">
<rect width="{w:.0f}" height="{h}" fill="#060a14"/>
<rect x="{split}" width="{w - split:.0f}" height="{h}" fill="{color}"/>
{text_path(GOTHIC, label, 13, 2.2, pad, 24, "#cfd8ff")}
{text_path(JEDI, value, 13, 2, split + gap, 24, "#05070f")}
</g>
<rect x="0.5" y="0.5" width="{w - 1:.0f}" height="{h - 1}" rx="6" fill="none" stroke="{color}" stroke-opacity="0.7"/>
</svg>
"""
    (OUT / f"badge-{slug}.svg").write_text(svg, encoding="utf-8")


def badges(d):
    pill("followers", "ALLIES OF THE REBELLION", str(d["followers"]), YELLOW, f"{d['followers']} followers")
    pill("squadron", "SQUADRON", "CIN-UFPE", BLUE, "Squadron: CIn-UFPE")
    pill("mission", "CURRENT MISSION", "MERIDIAN-WEALTH", RED, "Current mission: meridian-wealth")


def wrap(text, font, size, spacing, max_w, max_lines=2):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if text_width(font, trial, size, spacing) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" .,;") + "..."
    return lines


REPO_Q = "query($o:String!,$n:String!){repository(owner:$o,name:$n){name description primaryLanguage{name color} stargazerCount}}"


def missions():
    for i, name in enumerate(MISSIONS):
        r = gs.gql(REPO_Q, o=gs.USER, n=name)["repository"]
        desc = r["description"] or "No briefing yet. A mission still hiding in the shadows."
        lang = r["primaryLanguage"] or {"name": "Unknown", "color": "#8b949e"}
        w, h = 440, 132
        inner = [text_path(JEDI, r["name"].upper(), 17, 2, 26, 44, YELLOW, max_w=w - 52)]
        for n, line in enumerate(wrap(desc, GOTHIC, 14, 0.6, w - 52)):
            inner.append(text_path(GOTHIC, line, 14, 0.6, 26, 72 + n * 20, "#cfd8ff"))
        inner.append(f'<circle cx="32" cy="114" r="5" fill="{lang["color"]}"/>')
        inner.append(text_path(GOTHIC, lang["name"].upper(), 12, 1.5, 44, 118, "#8ea3d6"))
        star = "M0 -6L1.8 -1.9 6.2 -1.7 2.8 1.1 3.9 5.4 0 3 -3.9 5.4 -2.8 1.1 -6.2 -1.7 -1.8 -1.9Z"
        inner.append(f'<path transform="translate({w - 74} 113)" d="{star}" fill="#ffb347"/>')
        inner.append(text_path(GOTHIC, str(r["stargazerCount"]), 13, 0.5, w - 60, 118, "#ffffff"))
        (OUT / f"mission-{i + 1}.svg").write_text(frame(w, h, f"Mission: {r['name']}", "\n".join(inner), f"m{i}"), encoding="utf-8")


if __name__ == "__main__":
    data = gs.collect()
    xp = gs.xp_of(data)
    print("xp:", xp, gs.rank_of(xp)[:4])
    card_rank(data)
    ladder(data)
    card_galaxy(data)
    badges(data)
    missions()
    print("cards:", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))
