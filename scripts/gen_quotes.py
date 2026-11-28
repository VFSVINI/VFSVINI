"""Gera quotes.svg: carrossel de frases originais em contornos (fonte do filme + News Cycle).

Sorteia SHOWN das frases a cada execucao (semente = data + metade do dia), entao quem abre o
perfil em momentos diferentes ve frases diferentes. Nao precisa de token do GitHub.
Uso: python scripts/gen_quotes.py [pasta_saida]
"""
import hashlib
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from fontkit import GOTHIC, JEDI, glyph_defs, outline_uses, text_width
from quotes_data import quotes

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
OUT.mkdir(parents=True, exist_ok=True)

PER = 7.0     # segundos por frase
SHOWN = 60    # frases por ciclo (cada letra vira um desenho; mais frases = arquivo mais pesado)
W, H = 900, 124
YELLOW = "#FFE81F"


def fmt(v):
    return f"{v:.5f}".rstrip("0").rstrip(".") or "0"


def wrap(text, max_w, size=22, spacing=0.6):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if text_width(GOTHIC, trial, size, spacing) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def build():
    now = datetime.now(timezone.utc)
    seed = int(hashlib.sha256(f"{now:%Y-%m-%d}-{now.hour // 12}".encode()).hexdigest(), 16)
    items = quotes()
    random.Random(seed).shuffle(items)
    items = items[:SHOWN]
    total = PER * len(items)
    groups = []
    for i, (text, who) in enumerate(items):
        t0 = i * PER
        pts = [(0, 0), (t0, 0), (t0 + 0.7, 1), (t0 + PER - 0.8, 1), (t0 + PER - 0.05, 0), (total, 0)]
        kt, vals = [], []
        for t, v in pts:
            k = min(max(t / total, 0.0), 1.0)
            if kt and k < kt[-1]:
                k = kt[-1]
            kt.append(k)
            vals.append(v)
        lines = wrap("\u201c" + text + "\u201d", 800)
        ys, ya = ([58], 98) if len(lines) == 1 else ([46, 74], 106)
        body = "".join(
            f'<g transform="translate(450 {y})" fill="#B6C3EE">{outline_uses(GOTHIC, line, 22, 0.6)}</g>'
            for line, y in zip(lines, ys)
        )
        who_use = f'<g transform="translate(450 {ya})" fill="{YELLOW}">{outline_uses(JEDI, who, 12, 4)}</g>'
        groups.append(
            f'<g opacity="0"><animate attributeName="opacity" values="{";".join(str(v) for v in vals)}" '
            f'keyTimes="{";".join(fmt(k) for k in kt)}" dur="{total:g}s" repeatCount="indefinite"/>{body}{who_use}</g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Original maxims in the voice of Star Wars characters">
<defs>
{glyph_defs()}
<linearGradient id="qb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#05070f"/><stop offset="1" stop-color="#0d1530"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="12" fill="url(#qb)"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{YELLOW}" stroke-opacity="0.35"/>
{"".join(groups)}
</svg>
"""
    (OUT / "quotes.svg").write_text(svg, encoding="utf-8")
    print(f"quotes.svg: {len(items)} de {len(quotes())} frases, {len(svg) // 1024} KB, ciclo de {total / 60:.0f} min")


if __name__ == "__main__":
    build()
