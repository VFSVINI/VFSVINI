"""Gera os SVGs animados estaticos do perfil (crawl, divisor de sabres, citacoes).

Uso: python scripts/gen_static.py   (escreve em assets/)
SVG com SMIL/CSS roda dentro de <img> no GitHub, sem JavaScript.
"""
import random
import re
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

W, H = 900, 520
TOTAL = 132.0  # duracao do loop em segundos
YELLOW = "#FFE81F"
BLUE = "#4BD5EE"
FONT = "'Franklin Gothic Demi Cond','Franklin Gothic Medium','Arial Narrow','Helvetica Neue',Arial,sans-serif"

from fontkit import CEDILLA_DY, FONTS_DIR, GOTHIC, JEDI, glyph_defs, outline, outline_uses, text_path, text_width  # noqa: F401

def fmt(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def starfield(rng, n=150):
    parts = []
    for _ in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.choice([0.5, 0.7, 0.9, 1.2, 1.6])
        dur = rng.uniform(2.5, 7)
        lo = rng.choice([0.15, 0.3, 0.5])
        begin = rng.uniform(0, 5)
        color = rng.choice(["#fff", "#fff", "#cfe3ff", "#fff2c2"])
        parts.append(
            f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="{color}" opacity="{lo}">'
            f'<animate attributeName="opacity" values="{lo};1;{lo}" dur="{fmt(dur)}s" '
            f'begin="-{fmt(begin)}s" repeatCount="indefinite"/></circle>'
        )
    # estrelas cadentes
    for i in range(4):
        x, y = rng.uniform(120, 800), rng.uniform(20, 200)
        d = 6 + i * 4.5
        parts.append(
            f'<line x1="{fmt(x)}" y1="{fmt(y)}" x2="{fmt(x + 70)}" y2="{fmt(y + 24)}" '
            f'stroke="url(#shoot)" stroke-width="1.6" stroke-linecap="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;0.{40 + i * 5};0.{44 + i * 5};0.{50 + i * 5};1" '
            f'dur="{d}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="-90 -30;90 30" '
            f'keyTimes="0;1" dur="{d}s" repeatCount="indefinite"/></line>'
        )
    return "\n".join(parts)


CRAWL = [
    ("EPISODE IX", "head"),
    ("THE LEGACY STRIKES BACK", "title"),
    ("", ""),
    ("The galaxy of software is in", ""),
    ("turmoil. Empires of legacy code", ""),
    ("stretch across every system, and", ""),
    ("nobody remembers who built them,", ""),
    ("or why.", ""),
    ("", ""),
    ("Deep in the Outer Rim, a lone", ""),
    ("engineer receives a message: a", ""),
    ("payment service is failing, the", ""),
    ("pager is screaming, and it is, of", ""),
    ("course, a Friday afternoon.", ""),
    ("", ""),
    ("The Old Monolith looms over the", ""),
    ("repository like a Death Star.", ""),
    ("Every change risks a chain", ""),
    ("reaction. Its tests are few. Its", ""),
    ("documentation is a rumor passed", ""),
    ("between weary veterans.", ""),
    ("", ""),
    ("Yet hope survives. Rebel", ""),
    ("developers gather in the quiet", ""),
    ("hours, armed with unit tests,", ""),
    ("clean architecture, and a", ""),
    ("stubborn faith in refactoring.", ""),
    ("", ""),
    ("Their missions are never glorious.", ""),
    ("They hunt a bug that vanishes", ""),
    ("when observed. They bargain with", ""),
    ("a flaky test that fails only at", ""),
    ("midnight. They untangle a", ""),
    ("dependency older than the", ""),
    ("project itself.", ""),
    ("", ""),
    ("Some are tempted by the Dark", ""),
    ("Side: the quick hack, the copied", ""),
    ("snippet, the temporary fix that", ""),
    ("lives forever. It is faster. It", ""),
    ("is easier. And it always sends", ""),
    ("the bill later.", ""),
    ("", ""),
    ("But a Jedi engineer knows the", ""),
    ("way. Read before writing.", ""),
    ("Measure before optimizing. Test", ""),
    ("before shipping. Leave the code", ""),
    ("better than you found it.", ""),
    ("", ""),
    ("Across the galaxy, pipelines turn", ""),
    ("green, services scale, and a few", ""),
    ("brave builders ship what others", ""),
    ("called impossible, one pull", ""),
    ("request at a time.", ""),
    ("", ""),
    ("Now a new mission begins: build", ""),
    ("systems that survive contact with", ""),
    ("reality, teach others what was", ""),
    ("learned, and keep the lights of", ""),
    ("the galaxy running...", ""),
    ("", ""),
    ("MAY THE FORCE BE WITH YOU,", "end"),
    ("AND MAY YOUR BUILD STAY GREEN", "end"),
]

# --- parametros da perspectiva ---
HORIZON = 50.0          # y do ponto de fuga
BOTTOM = 540.0          # y logo abaixo da borda inferior
Z0 = 1.0                # profundidade de uma linha na borda inferior
K = (BOTTOM - HORIZON) * Z0
GAP = 0.075             # espacamento entre linhas em profundidade
SPEED = 0.068          # profundidade por segundo
T_START, T_CRAWL = 14.0, 112.0
SAMPLES = 120


def crawl_lines():
    out = []
    n_lines = len(CRAWL)
    for i, (text, kind) in enumerate(CRAWL):
        if not text:
            continue
        ys, ss, ops = [], [], []
        for k in range(SAMPLES + 1):
            t = T_CRAWL * k / SAMPLES
            z = Z0 - GAP * i + SPEED * t
            z = max(z, 0.45)
            y = HORIZON + K / z
            s = Z0 / z
            fade = max(0.0, min(1.0, (s - 0.17) / 0.14)) * min(1.0, (T_CRAWL - t) / 5.0)
            ys.append(y)
            ss.append(s)
            ops.append(fade)
        f0 = T_START / TOTAL
        f1 = (T_START + T_CRAWL) / TOTAL
        kt = [0.0] + [f0 + (f1 - f0) * k / SAMPLES for k in range(SAMPLES + 1)] + [1.0]
        ktxt = ";".join(f"{v:.4f}".rstrip("0").rstrip(".") for v in kt)
        tv = [ys[0]] + ys + [ys[-1]]
        sv = [ss[0]] + ss + [ss[-1]]
        ov = [0.0] + ops + [0.0]
        size = {"head": 40, "title": 48, "end": 40}.get(kind, 40)
        if kind in ("head", "title"):
            d = outline_uses(JEDI, text, 40 if kind == "head" else 44, 2, max_w=640)
        else:
            d = outline_uses(GOTHIC, text, 42, 1.2, max_w=640)
        trans = ";".join(f"450 {y:.1f}" for y in tv)
        scale = ";".join(f"{s:.3f} {s * 0.78:.3f}" for s in sv)
        opac = ";".join(f"{o:.2f}".rstrip("0").rstrip(".") or "0" for o in ov)
        out.append(
            f'<g fill="{YELLOW}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="{trans}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="scale" values="{scale}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite" additive="sum"/>'
            f'<animate attributeName="opacity" values="{opac}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite"/>'
            f"{d}</g>"
        )
    return "\n".join(out)


def logo():
    t0, t1 = 7.4, 14.2
    n = 50
    kt, sv, ov = [0.0], [1.0], [0.0]
    kt.append(t0 / TOTAL - 0.0001)
    sv.append(1.0)
    ov.append(0.0)
    for k in range(n + 1):
        u = k / n
        kt.append((t0 + (t1 - t0) * u) / TOTAL)
        s = 1.0 / (1.0 + 14 * u * u) if u > 0.08 else 1.0
        sv.append(s)
        ov.append(1.0 if u < 0.55 else max(0.0, 1 - (u - 0.55) / 0.45))
    kt.append(1.0)
    sv.append(sv[-1])
    ov.append(0.0)
    ktxt = ";".join(fmt(v) for v in kt)
    scale = ";".join(fmt(s) for s in sv)
    opac = ";".join(fmt(o) for o in ov)
    return (
        f'<g opacity="0" fill="{YELLOW}" stroke="{YELLOW}" stroke-linejoin="round">'
        f'<animateTransform attributeName="transform" type="translate" values="450 275;450 275" dur="{TOTAL}s" repeatCount="indefinite"/>'
        f'<animateTransform attributeName="transform" type="scale" values="{scale}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite" additive="sum"/>'
        f'<animate attributeName="opacity" values="{opac}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite"/>'
        f'<path transform="translate(0 -6)" stroke-width="2" d="{outline(JEDI, "VINÍCIUS", 120, 6, max_w=800)}"/>'
        f'<path transform="translate(0 112)" stroke-width="2" d="{outline(JEDI, "FRANÇA", 120, 6, max_w=800)}"/>'
        f'<path transform="translate(0 -112)" stroke-width="0.4" d="{outline(GOTHIC, "SOFTWARE DEVELOPER", 24, 10)}"/>'
        f"</g>"
    )


def intro():
    a, b, c, d = 0.6, 2.2, 5.0, 6.8
    kt = [0, a / TOTAL, b / TOTAL, c / TOTAL, d / TOTAL, 1]
    ktxt = ";".join(fmt(v) for v in kt)
    return (
        f'<g opacity="0" fill="{BLUE}">'
        f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite"/>'
        f'<path transform="translate(450 245)" d="{outline(GOTHIC, "A long time ago in a galaxy", 34, 1)}"/>'
        f'<path transform="translate(450 290)" d="{outline(GOTHIC, "far, far away....", 34, 1)}"/></g>'
    )


def build_crawl():
    rng = random.Random(77)
    lines = crawl_lines()
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A long time ago in a galaxy far, far away... Vinícius França, Software Developer.">
<title>Vinícius França — Software Developer</title>
<defs>
{glyph_defs()}
<linearGradient id="shoot" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="fadeTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="0.75" stop-color="#000" stop-opacity="0.85"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
<radialGradient id="nebula" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#1b2a6b" stop-opacity="0.55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="#000"/>
<ellipse cx="170" cy="400" rx="260" ry="150" fill="url(#nebula)"/>
<ellipse cx="760" cy="120" rx="240" ry="120" fill="url(#nebula)" opacity="0.6"/>
{starfield(rng)}
{intro()}
{logo()}
{lines}
<rect x="0" y="0" width="{W}" height="130" fill="url(#fadeTop)"/>
</svg>
"""
    (OUT / "crawl.svg").write_text(svg, encoding="utf-8")


def build_divider():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 44" width="900" height="44" role="img" aria-label="Lightsaber duel divider">
<defs>
<filter id="gb" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="4"/></filter>
<linearGradient id="hilt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9dde6"/><stop offset="0.5" stop-color="#7d8594"/><stop offset="1" stop-color="#3b414d"/></linearGradient>
<radialGradient id="spark"><stop offset="0" stop-color="#fff"/><stop offset="0.4" stop-color="#ffe81f"/><stop offset="1" stop-color="#ffe81f" stop-opacity="0"/></radialGradient>
</defs>
<g>
<rect x="410" y="19" width="0" height="6" rx="3" fill="#4bd5ee" filter="url(#gb)" opacity="0.95">
<animate attributeName="x" values="415;30;30;415" keyTimes="0;0.14;0.86;1" dur="7s" repeatCount="indefinite"/>
<animate attributeName="width" values="0;385;385;0" keyTimes="0;0.14;0.86;1" dur="7s" repeatCount="indefinite"/></rect>
<rect x="410" y="20.5" width="0" height="3" rx="1.5" fill="#7fe3ff">
<animate attributeName="x" values="415;30;30;415" keyTimes="0;0.14;0.86;1" dur="7s" repeatCount="indefinite"/>
<animate attributeName="width" values="0;385;385;0" keyTimes="0;0.14;0.86;1" dur="7s" repeatCount="indefinite"/></rect>
<rect x="485" y="19" width="0" height="6" rx="3" fill="#ff2a2a" filter="url(#gb)" opacity="0.95">
<animate attributeName="width" values="0;385;385;0" keyTimes="0;0.14;0.86;1" dur="7s" repeatCount="indefinite"/></rect>
<rect x="485" y="20.5" width="0" height="3" rx="1.5" fill="#ff9a9a">
<animate attributeName="width" values="0;385;385;0" keyTimes="0;0.14;0.86;1" dur="7s" repeatCount="indefinite"/></rect>
</g>
<g>
<rect x="395" y="16" width="30" height="12" rx="2" fill="url(#hilt)"/><rect x="402" y="14" width="3" height="16" fill="#2a2f39"/><rect x="412" y="14" width="3" height="16" fill="#2a2f39"/>
<rect x="475" y="16" width="30" height="12" rx="2" fill="url(#hilt)"/><rect x="485" y="14" width="3" height="16" fill="#2a2f39"/><rect x="495" y="14" width="3" height="16" fill="#2a2f39"/>
</g>
<circle cx="450" cy="22" r="14" fill="url(#spark)" opacity="0">
<animate attributeName="opacity" values="0;0;1;0.2;0.9;0;0" keyTimes="0;0.13;0.16;0.2;0.25;0.3;1" dur="7s" repeatCount="indefinite"/>
<animate attributeName="r" values="4;4;16;8;14;4;4" keyTimes="0;0.13;0.16;0.2;0.25;0.3;1" dur="7s" repeatCount="indefinite"/></circle>
</svg>
"""
    (OUT / "divider.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build_crawl()
    build_divider()
    for f in sorted(OUT.glob("*.svg")):
        print(f.name, f.stat().st_size // 1024, "KB")
