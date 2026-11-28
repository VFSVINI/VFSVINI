"""Gera assets/transmission.svg: cartao holografico 'Incoming Transmission' com os dados do perfil."""
from gen_static import GOTHIC, JEDI, OUT, outline, text_width

W, H = 900, 280
CYAN, YELLOW = "#4BD5EE", "#FFE81F"
X0, XV = 292, 452  # coluna dos rotulos e dos valores
DIM = 'opacity="0.75"'

ROWS = [
    ("NAME", "Vinícius França"),
    ("ORDER", "Information Systems @ CIn-UFPE"),
    ("CLASS", "Backend & Full Stack Developer"),
    ("FOCUS", "Clean Architecture · Scalable Systems · FinTech"),
    ("MISSION", "Turn data into decisions, one clean commit at a time"),
    ("BASE", "Recife, Brazil"),
]


def left(font, text, size, spacing, x, y, fill, extra="", max_w=None):
    if max_w:
        size = min(size, size * max_w / text_width(font, text, size, spacing))
    w = text_width(font, text, size, spacing)
    return f'<path transform="translate({x + w / 2:.1f} {y})" fill="{fill}" {extra} d="{outline(font, text, size, spacing)}"/>'


def hologram(cx, cy, r):
    meridians = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none" stroke="{CYAN}" stroke-width="1.2" opacity="0.8">'
        f'<animate attributeName="rx" values="{r};0;{r}" dur="6s" begin="{-i * 1.5}s" repeatCount="indefinite"/></ellipse>'
        for i in range(4)
    )
    parallels = "".join(
        f'<ellipse cx="{cx}" cy="{cy + dy}" rx="{(r * r - dy * dy) ** 0.5:.1f}" ry="{(r * r - dy * dy) ** 0.5 * 0.18:.1f}" fill="none" stroke="{CYAN}" stroke-width="1" opacity="0.65"/>'
        for dy in (-r * 0.66, -r * 0.33, 0, r * 0.33, r * 0.66)
    )
    return f"""<g filter="url(#holoGlow)">
<polygon points="{cx - 46},{cy + r + 46} {cx + 46},{cy + r + 46} {cx + r * 0.8},{cy + r - 4} {cx - r * 0.8},{cy + r - 4}" fill="url(#beam)"/>
<ellipse cx="{cx}" cy="{cy + r + 50}" rx="58" ry="11" fill="#0a1a30" stroke="{CYAN}" stroke-width="1.5"/>
<ellipse cx="{cx}" cy="{cy + r + 50}" rx="38" ry="6" fill="none" stroke="{CYAN}" stroke-width="1" opacity="0.7"><animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/></ellipse>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CYAN}" fill-opacity="0.06" stroke="{CYAN}" stroke-width="1.6"/>
{meridians}{parallels}
<animate attributeName="opacity" values="1;0.88;1;0.95;0.82;1" keyTimes="0;0.2;0.4;0.6;0.65;1" dur="3.4s" repeatCount="indefinite"/>
</g>"""


def build():
    clips, rows = [], []
    for i, (label, value) in enumerate(ROWS):
        y = 100 + i * 29
        begin = 0.7 + i * 0.9
        clips.append(
            f'<clipPath id="r{i}"><rect x="{X0 - 4}" y="{y - 24}" width="0" height="32">'
            f'<animate attributeName="width" from="0" to="{W - X0}" dur="0.8s" begin="{begin}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.3 0 0.2 1"/></rect></clipPath>'
        )
        rows.append(
            f'<g clip-path="url(#r{i})">'
            f'{left(GOTHIC, label, 14, 2.5, X0, y - 2, CYAN, DIM)}'
            f'{left(GOTHIC, value, 20, 0.6, XV, y, "#EAF2FF", max_w=W - 32 - XV)}</g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Incoming transmission: Vinícius França, Information Systems at CIn-UFPE, Backend and Full Stack Developer, Recife, Brazil">
<title>Incoming transmission</title>
<defs>
<linearGradient id="bgT" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#04070f"/><stop offset="1" stop-color="#0a1830"/></linearGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.45"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<pattern id="scanT" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="{CYAN}" opacity="0.07"/></pattern>
<filter id="holoGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="cpT"><rect width="{W}" height="{H}" rx="14"/></clipPath>
{"".join(clips)}
</defs>
<g clip-path="url(#cpT)">
<rect width="{W}" height="{H}" fill="url(#bgT)"/>
<rect width="{W}" height="{H}" fill="url(#scanT)"/>
<rect y="-40" width="{W}" height="40" fill="{CYAN}" opacity="0.07"><animate attributeName="y" values="-40;{H}" dur="4.5s" repeatCount="indefinite"/></rect>
{hologram(150, 118, 62)}
{left(JEDI, "INCOMING TRANSMISSION", 15, 3, X0, 50, YELLOW)}
<circle cx="{W - 40}" cy="44" r="4" fill="#ff5a5a"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>
{left(GOTHIC, "SIGNAL STRONG", 12, 3, W - 168, 49, "#8ea3d6")}
<line x1="{X0}" y1="64" x2="{W - 30}" y2="64" stroke="{CYAN}" stroke-opacity="0.35"/>
{"".join(rows)}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{CYAN}" stroke-opacity="0.5"/>
</svg>
"""
    (OUT / "transmission.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build()
    print("transmission.svg", (OUT / "transmission.svg").stat().st_size // 1024, "KB")
