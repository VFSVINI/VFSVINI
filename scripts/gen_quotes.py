"""Gera quotes.svg: carrossel com as frases originais em ordem embaralhada.

A ordem muda a cada 12h (semente = data + metade do dia), entao quem abre o perfil
em momentos diferentes ve frases diferentes primeiro.
Uso: python scripts/gen_quotes.py [pasta_saida]
"""
import hashlib
import random
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from quotes_data import quotes

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
OUT.mkdir(parents=True, exist_ok=True)

PER = 7.0      # segundos por frase
WRAP = 62      # caracteres por linha
W, H = 900, 104
FONT = "'Franklin Gothic Medium','Arial Narrow','Segoe UI',Arial,sans-serif"


def fmt(v):
    return f"{v:.5f}".rstrip("0").rstrip(".") or "0"


def build():
    now = datetime.now(timezone.utc)
    seed = int(hashlib.sha256(f"{now:%Y-%m-%d}-{now.hour // 12}".encode()).hexdigest(), 16)
    items = quotes()
    random.Random(seed).shuffle(items)
    total = PER * len(items)
    groups = []
    for i, (text, who) in enumerate(items):
        t0 = i * PER
        pts = [(0, 0), (t0, 0), (t0 + 0.7, 1), (t0 + PER - 0.8, 1), (t0 + PER - 0.05, 0), (total, 0)]
        # primeira e ultima frases encostam nas bordas do ciclo
        kt, vals = [], []
        for t, v in pts:
            k = min(max(t / total, 0.0), 1.0)
            if kt and k < kt[-1]:
                k = kt[-1]
            kt.append(k)
            vals.append(v)
        lines = textwrap.wrap(text, WRAP)
        if len(lines) == 1:
            ys, ya = [48], 82
        else:
            ys, ya = [36, 62], 90
        tspans = "".join(
            f'<text class="q" x="450" y="{y}" text-anchor="middle" font-size="21" font-style="italic">'
            f'{"“" if n == 0 else ""}{escape(line)}{"”" if n == len(lines) - 1 else ""}</text>'
            for n, (line, y) in enumerate(zip(lines, ys))
        )
        groups.append(
            f'<g opacity="0"><animate attributeName="opacity" values="{";".join(str(v) for v in vals)}" '
            f'keyTimes="{";".join(fmt(k) for k in kt)}" dur="{total:g}s" repeatCount="indefinite"/>'
            f'{tspans}<text class="a" x="450" y="{ya}" text-anchor="middle" font-size="12" letter-spacing="4">— {escape(who)}</text></g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Original maxims in the voice of Star Wars characters">
<style>
text{{font-family:{FONT}}}
.q{{fill:#4a5a8f}} .a{{fill:#a07400}}
@media (prefers-color-scheme: dark){{.q{{fill:#b6c3ee}} .a{{fill:#ffe81f}}}}
</style>
{"".join(groups)}
</svg>
"""
    (OUT / "quotes.svg").write_text(svg, encoding="utf-8")
    print(f"quotes.svg: {len(items)} frases, {len(svg) // 1024} KB, ciclo de {total / 60:.0f} min")


if __name__ == "__main__":
    build()
