"""Gera os SVGs animados estaticos do perfil (crawl, divisor de sabres, citacoes).

Uso: python scripts/gen_static.py   (escreve em assets/)
SVG com SMIL/CSS roda dentro de <img> no GitHub, sem JavaScript.
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

W, H = 900, 520
TOTAL = 62.0  # duracao do loop em segundos
YELLOW = "#FFE81F"
BLUE = "#4BD5EE"
FONT = "'Franklin Gothic Demi Cond','Franklin Gothic Medium','Arial Narrow','Helvetica Neue',Arial,sans-serif"

# --- texto convertido em contornos vetoriais (GitHub nao carrega fontes em SVG) ---
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"
JEDI = "SFDistantGalaxy.ttf"   # titulos e logo (fonte de fa, freeware, uso pessoal)
CEDILLA_DY = 120               # deslocamento vertical da cedilha (unidades da fonte)
GOTHIC = "NewsCycle-Bold.woff"  # corpo do crawl (recriacao livre da News Gothic, OFL)
_FONTS = {}


def _font(name):
    if name not in _FONTS:
        f = TTFont(FONTS_DIR / name)
        _FONTS[name] = (f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm, f["hmtx"])
    return _FONTS[name]


def _glyph(cm, c):
    """Glifo de c; o 'Ç' (ausente na SF Distant Galaxy) e composto de C + cedilha."""
    g = cm.get(ord(c))
    if g is None and c == "Ç":
        return cm[ord("C")]
    return g


def text_width(name, text, size, spacing=0.0):
    gs, cm, upm, hmtx = _font(name)
    sc = size / upm
    return sum(hmtx[_glyph(cm, c)][0] * sc + spacing for c in text) - spacing


def outline(name, text, size, spacing=0.0, max_w=None):
    """Devolve o 'd' do path, centralizado em x=0 com a linha de base em y=0."""
    gs, cm, upm, hmtx = _font(name)
    missing = [c for c in text if _glyph(cm, c) is None]
    if missing:
        raise SystemExit(f"{name} nao tem os glifos {missing} em '{text}'")
    if max_w:
        size = min(size, size * max_w / text_width(name, text, size, spacing))
    sc = size / upm
    x = -text_width(name, text, size, spacing) / 2
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    for c in text:
        g = _glyph(cm, c)
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, 0)))
        if c == "Ç":  # cedilha: virgula da propria fonte, menor, sob o C
            comma, k = cm[ord(",")], 0.62
            cx = x + (hmtx[g][0] - hmtx[comma][0] * k) * sc / 2
            gs[comma].draw(TransformPen(pen, (sc * k, 0, 0, -sc * k, cx, CEDILLA_DY * sc)))
        x += hmtx[g][0] * sc + spacing
    return pen.getCommands()


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
    ("EPISÓDIO VII", "head"),
    ("O ARQUITETO DESPERTA", "title"),
    ("", ""),
    ("Eram tempos sombrios para o", ""),
    ("software. Monólitos de código", ""),
    ("legado cobriam a galáxia, e os", ""),
    ("deploys aconteciam às sextas...", ""),
    ("", ""),
    ("Das sombras do CIn-UFPE, em", ""),
    ("Recife, surge VINÍCIUS FRANÇA,", ""),
    ("estudante de Sistemas de", ""),
    ("Informação e desenvolvedor", ""),
    ("Backend e Full Stack.", ""),
    ("", ""),
    ("Armado de Java, Spring, Go e", ""),
    ("Clean Architecture, ele forja", ""),
    ("sistemas escaláveis, testados", ""),
    ("e prontos para o combate.", ""),
    ("", ""),
    ("SUA MISSÃO: construir", "head"),
    ("plataformas de FinTech que", ""),
    ("unam dados, finanças e", ""),
    ("inteligência em toda a galáxia.", ""),
    ("", ""),
    ("Entre o Lado Luminoso do código", ""),
    ("limpo e o Lado Sombrio das", ""),
    ("gambiarras, ele escolheu o seu", ""),
    ("caminho. Que a Força (e os", ""),
    ("testes verdes) estejam com você...", "end"),
]

# --- parametros da perspectiva ---
HORIZON = 50.0          # y do ponto de fuga
BOTTOM = 540.0          # y logo abaixo da borda inferior
Z0 = 1.0                # profundidade de uma linha na borda inferior
K = (BOTTOM - HORIZON) * Z0
GAP = 0.075             # espacamento entre linhas em profundidade
SPEED = 0.15           # profundidade por segundo
T_START, T_CRAWL = 14.0, 47.0
SAMPLES = 110


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
            fade = max(0.0, min(1.0, (s - 0.17) / 0.14))
            ys.append(y)
            ss.append(s)
            ops.append(fade)
        f0 = T_START / TOTAL
        f1 = (T_START + T_CRAWL) / TOTAL
        kt = [0.0] + [f0 + (f1 - f0) * k / SAMPLES for k in range(SAMPLES + 1)] + [1.0]
        ktxt = ";".join(fmt(v) for v in kt)
        tv = [ys[0]] + ys + [ys[-1]]
        sv = [ss[0]] + ss + [ss[-1]]
        ov = [0.0] + ops + [0.0]
        size = {"head": 40, "title": 48, "end": 40}.get(kind, 40)
        if kind in ("head", "title"):
            d = outline(JEDI, text, 40 if kind == "head" else 44, 2, max_w=640)
        else:
            d = outline(GOTHIC, text, 42, 1.2, max_w=640)
        trans = ";".join(f"450 {fmt(y)}" for y in tv)
        scale = ";".join(f"{fmt(s)} {fmt(s * 0.78)}" for s in sv)
        opac = ";".join(fmt(o) for o in ov)
        out.append(
            f'<path d="{d}" fill="{YELLOW}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="{trans}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="scale" values="{scale}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite" additive="sum"/>'
            f'<animate attributeName="opacity" values="{opac}" keyTimes="{ktxt}" dur="{TOTAL}s" repeatCount="indefinite"/>'
            f"</path>"
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
        f'<path transform="translate(450 245)" d="{outline(GOTHIC, "Há muito tempo, numa galáxia", 34, 1)}"/>'
        f'<path transform="translate(450 290)" d="{outline(GOTHIC, "muito, muito distante....", 34, 1)}"/></g>'
    )


def build_crawl():
    rng = random.Random(77)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Há muito tempo, numa galáxia muito, muito distante... Vinícius França, Software Developer.">
<title>Vinícius França — Software Developer</title>
<defs>
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
{crawl_lines()}
<rect x="0" y="0" width="{W}" height="130" fill="url(#fadeTop)"/>
</svg>
"""
    (OUT / "crawl.svg").write_text(svg, encoding="utf-8")


def build_divider():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 44" width="900" height="44" role="img" aria-label="Duelo de sabres de luz">
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


QUOTES = [
    ("Faça, ou não faça. Tentativa não há.", "MESTRE YODA"),
    ("Medo é o caminho para o Lado Sombrio.", "MESTRE YODA"),
    ("Tenho um mau pressentimento sobre este deploy.", "TODO DEV, SEXTA 17h59"),
    ("Que a Força (e os testes verdes) estejam com você.", "VFSVINI"),
]


def build_quotes():
    per = 6.0
    total = per * len(QUOTES)
    items = []
    for i, (q, who) in enumerate(QUOTES):
        a = i * per / total
        b = (i * per + 0.8) / total
        c = (i * per + per - 0.9) / total
        d = (i * per + per - 0.1) / total
        kt = sorted({0.0, a, b, c, d, 1.0})
        vals = []
        for k in kt:
            if k < a - 1e-9 or k > d + 1e-9:
                vals.append("0")
            elif abs(k - a) < 1e-9 and a > 0:
                vals.append("0")
            elif abs(k - d) < 1e-9 and d < 1:
                vals.append("0")
            elif a - 1e-9 <= k <= d + 1e-9 and (abs(k - b) < 1e-9 or abs(k - c) < 1e-9):
                vals.append("1")
            else:
                vals.append("0")
        items.append(
            f'<g opacity="0"><animate attributeName="opacity" values="{";".join(vals)}" '
            f'keyTimes="{";".join(fmt(k) for k in kt)}" dur="{total}s" repeatCount="indefinite"/>'
            f'<text class="q" x="450" y="38" text-anchor="middle" font-size="22" font-style="italic">“{escape(q)}”</text>'
            f'<text class="a" x="450" y="64" text-anchor="middle" font-size="12" letter-spacing="4">— {escape(who)}</text></g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 80" width="900" height="80" role="img" aria-label="Citações da galáxia">
<style>
text{{font-family:{FONT}}}
.q{{fill:#7d8fc9}} .a{{fill:#b8860b}}
@media (prefers-color-scheme: dark){{.q{{fill:#aab8e8}} .a{{fill:#ffe81f}}}}
</style>
{"".join(items)}
</svg>
"""
    (OUT / "quotes.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build_crawl()
    build_divider()
    build_quotes()
    for f in sorted(OUT.glob("*.svg")):
        print(f.name, f.stat().st_size // 1024, "KB")
