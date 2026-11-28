"""Texto em contornos vetoriais: o GitHub nao carrega fontes dentro de SVG.

Fonte Star Wars (SF Distant Galaxy, freeware de uso pessoal) nao fica no repositorio:
localmente fica em fonts/, no CI e baixada a cada execucao. Se ela nao existir, cai para a
News Cycle (OFL, versionada), entao a geracao nunca quebra.
"""
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

# --- texto convertido em contornos vetoriais (GitHub nao carrega fontes em SVG) ---
FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"
GOTHIC = "NewsCycle-Bold.woff"  # corpo do texto (recriacao livre da News Gothic, OFL)
JEDI = "SFDistantGalaxy.ttf" if (FONTS_DIR / "SFDistantGalaxy.ttf").exists() else GOTHIC  # titulos e logo
CEDILLA_DY = 120               # deslocamento vertical da cedilha (unidades da fonte)
_FONTS = {}
FALLBACKS = {"“": '"', "”": '"', "’": "'", "—": "-", "–": "-", "×": "x", "·": "-", "→": ">"}


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
    if g is None and c in FALLBACKS:
        return cm.get(ord(FALLBACKS[c]))
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


GLYPH_DEFS = {}


def _register(name, g):
    gs = _font(name)[0]
    gid = "g" + re.sub(r"\W", "", name.split(".")[0][:3]) + re.sub(r"\W", "", g)
    if gid not in GLYPH_DEFS:
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.0f}")
        gs[g].draw(pen)
        GLYPH_DEFS[gid] = pen.getCommands()
    return gid, bool(GLYPH_DEFS[gid])


def outline_uses(name, text, size, spacing=0.0, max_w=None):
    """Como outline(), mas reutiliza cada glifo via <use> (arquivo bem menor)."""
    gs, cm, upm, hmtx = _font(name)
    if max_w:
        size = min(size, size * max_w / text_width(name, text, size, spacing))
    sc = size / upm
    x = -text_width(name, text, size, spacing) / 2
    parts = []
    for c in text:
        g = _glyph(cm, c)
        gid, ink = _register(name, g)
        if ink:
            parts.append(f'<use href="#{gid}" transform="translate({x:.1f} 0) scale({sc:.4f} {-sc:.4f})"/>')
        if c == "Ç":
            comma, k = cm[ord(",")], 0.62
            cid, _ = _register(name, comma)
            cx = x + (hmtx[g][0] - hmtx[comma][0] * k) * sc / 2
            parts.append(f'<use href="#{cid}" transform="translate({cx:.1f} {CEDILLA_DY * sc:.1f}) scale({sc * k:.4f} {-sc * k:.4f})"/>')
        x += hmtx[g][0] * sc + spacing
    return "".join(parts)


def glyph_defs():
    return "".join(f'<path id="{i}" d="{d}"/>' for i, d in GLYPH_DEFS.items())


def text_path(font, text, size, spacing, x, y, fill, anchor="start", max_w=None, extra=""):
    """Path de texto posicionado (anchor: start|middle|end), pronto para colar no SVG."""
    if max_w:
        size = min(size, size * max_w / text_width(font, text, size, spacing))
    w = text_width(font, text, size, spacing)
    cx = x + {"start": w / 2, "middle": 0.0, "end": -w / 2}[anchor]
    return f'<path transform="translate({cx:.1f} {y})" fill="{fill}" {extra} d="{outline(font, text, size, spacing)}"/>'
