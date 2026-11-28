"""Gera assets/arsenal.svg: painel holografico com as ferramentas da stack.

Icones: Simple Icons (CC0, https://simpleicons.org) embutidos como paths em scripts/icons/.
Uso: python scripts/gen_arsenal.py
"""
import math
import re
from pathlib import Path

from texts import T
from gen_static import GOTHIC, JEDI, OUT, outline

ICONS = Path(__file__).resolve().parent / "icons"

BLUE, YELLOW, RED = "#4BD5EE", "#FFE81F", "#FF5A5A"
# (titulo da faixa, cor, [(arquivo, nome exibido)])
BANDS = [
    (T["arsenal_bands"][0], BLUE, [("java", "Java"), ("springboot", "Spring Boot"), ("go", "Go"), ("python", "Python")]),
    (T["arsenal_bands"][1], YELLOW, [("javascript", "JavaScript"), ("html5", "HTML5"), ("css3", "CSS3"),
                          ("threedotjs", "Three.js"), ("apacheecharts", "ECharts"), ("leaflet", "Leaflet")]),
    (T["arsenal_bands"][2], RED, [("postgresql", "PostgreSQL"), ("timescale", "TimescaleDB"), ("redis", "Redis"),
                           ("rabbitmq", "RabbitMQ"), ("docker", "Docker"), ("githubactions", "GitHub Actions"),
                           ("prometheus", "Prometheus")]),
]

W = 900
ROW_H = 112
TOP = 20
H = TOP + ROW_H * len(BANDS) + 18
LABEL_W = 170
SLOT = 96
R = 33  # raio do hexagono


def icon_paths(slug):
    """Devolve (paths, lado do viewBox); descarta cores proprias para pintar tudo igual."""
    svg = (ICONS / f"{slug}.svg").read_text(encoding="utf-8")
    side = float(re.search(r'viewBox="0 0 ([\d.]+) ', svg).group(1))
    return "".join(f'<path d="{d}"/>' for d in re.findall(r'<path[^>]*? d="([^"]+)"', svg)), side


def hexagon(r):
    pts = [(r * math.cos(math.radians(60 * i - 90)), r * math.sin(math.radians(60 * i - 90))) for i in range(6)]
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def tile(cx, cy, slug, name, color, idx):
    dur = 4 + (idx % 5) * 0.6
    begin = -(idx * 0.45)
    return f"""<g transform="translate({cx} {cy})">
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
<path d="{hexagon(R + 6)}" fill="{color}" opacity="0.10" filter="url(#soft)"><animate attributeName="opacity" values="0.06;0.2;0.06" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>
<path d="{hexagon(R)}" fill="#0a1226" stroke="{color}" stroke-width="1.6" stroke-opacity="0.85"/>
<path d="{hexagon(R - 6)}" fill="none" stroke="{color}" stroke-width="0.6" stroke-opacity="0.35"/>
<g transform="translate(-14 -14) scale({28 / icon_paths(slug)[1]:.4f})" fill="#EAF2FF">{icon_paths(slug)[0]}</g>
</g>
<path transform="translate(0 {R + 22})" fill="#AAB8E8" d="{outline(GOTHIC, name, 12.5, 1.2, max_w=SLOT - 8)}"/>
</g>"""


def build():
    rows = []
    n = 0
    for b, (title, color, items) in enumerate(BANDS):
        y0 = TOP + b * ROW_H
        cy = y0 + 46
        rows.append(f'<path transform="translate(28 {cy + 5})" fill="{color}" d="{outline(JEDI, title, 20, 2).replace("M", "M", 1)}"/>')
        # outline() centraliza em x=0: reposiciona alinhado a esquerda
        rows[-1] = rows[-1].replace(f'translate(28 {cy + 5})', f'translate({28 + _w(title) / 2} {cy + 5})')
        rows.append(f'<line x1="{LABEL_W - 8}" y1="{y0 + 8}" x2="{LABEL_W - 8}" y2="{y0 + ROW_H - 14}" stroke="{color}" stroke-opacity="0.35"/>')
        if b:
            rows.append(f'<line x1="24" y1="{y0 - 2}" x2="{W - 24}" y2="{y0 - 2}" stroke="#2a3a6b" stroke-opacity="0.6" stroke-dasharray="3 6"/>')
        avail = W - LABEL_W - 24
        start = LABEL_W + 24 + SLOT / 2 + (avail - len(items) * SLOT) / 2
        for i, (slug, name) in enumerate(items):
            rows.append(tile(start + i * SLOT, cy, slug, name, color, n))
            n += 1
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{T["alt_arsenal"]}">
<title>{T["h_arsenal"]}</title>
<defs>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="bgA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#05070f"/><stop offset="1" stop-color="#0d1530"/></linearGradient>
<linearGradient id="scanA" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.5" stop-color="{BLUE}" stop-opacity="0.12"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<clipPath id="cpA"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#cpA)">
<rect width="{W}" height="{H}" fill="url(#bgA)"/>
<rect x="-160" width="160" height="{H}" fill="url(#scanA)"><animate attributeName="x" values="-160;{W}" dur="7s" repeatCount="indefinite"/></rect>
{"".join(rows)}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{YELLOW}" stroke-opacity="0.45"/>
</svg>
"""
    (OUT / "arsenal.svg").write_text(svg, encoding="utf-8")


def _w(title):
    from gen_static import text_width
    return text_width(JEDI, title, 20, 2)


if __name__ == "__main__":
    build()
    print("arsenal.svg", (OUT / "arsenal.svg").stat().st_size // 1024, "KB")
