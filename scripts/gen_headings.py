"""Gera os banners de titulo, a nota de XP e o rodape (todos em fonte Star Wars, contornos)."""
from xml.sax.saxutils import escape

from fontkit import GOTHIC, JEDI, text_path, text_width
from gen_static import OUT
from texts import T

W = 900
YELLOW, CYAN = "#FFE81F", "#4BD5EE"

HEADINGS = [(slug, T[f"h_{slug}"]) for slug in ("transmission", "duel", "arsenal", "dossier", "missions", "snake")]

DEFS = f"""<defs>
<linearGradient id="hb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#05070f"/><stop offset="1" stop-color="#0d1530"/></linearGradient>
<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<filter id="hg" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


def heading(slug, title):
    h = 64
    size = 28
    max_w = W - 120
    txt = text_path(JEDI, title, size, 4, 54, 42, YELLOW, max_w=max_w, extra='filter="url(#hg)"')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
{DEFS}
<rect width="{W}" height="{h}" rx="12" fill="url(#hb)"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="12" fill="none" stroke="{YELLOW}" stroke-opacity="0.35"/>
<path d="M30 20l9 5.2v10.4L30 40.8l-9-5.2V25.2z" fill="none" stroke="{CYAN}" stroke-width="1.6"><animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></path>
<circle cx="30" cy="30.4" r="2.6" fill="{CYAN}"/>
{txt}
<rect x="18" y="54" width="0" height="2.4" rx="1.2" fill="url(#hl)"><animate attributeName="width" from="0" to="{W - 36}" dur="1.4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/></rect>
<circle cx="{W - 26}" cy="30" r="3" fill="#ff5a5a"><animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/></circle>
</svg>
"""
    (OUT / f"h-{slug}.svg").write_text(svg, encoding="utf-8")


def footer():
    h = 96
    title = text_path(JEDI, T["footer_title"], 26, 5, W / 2, 60, YELLOW, "middle", max_w=W - 80, extra='filter="url(#hg)"')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{T["alt_footer"]}">
<rect width="{W}" height="{h}" rx="12" fill="url(#hb)"/>{DEFS}
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="12" fill="none" stroke="{YELLOW}" stroke-opacity="0.35"/>
{title}
</svg>
"""
    (OUT / "footer.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    for slug, title in HEADINGS:
        heading(slug, title)
    footer()
    print("ok:", ", ".join(f"h-{s}" for s, _ in HEADINGS), "footer")
