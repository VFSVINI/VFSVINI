"""Gera assets/elenco.svg: R2-D2, C-3PO, Darth Vader, Han Solo e Chewbacca animados em vetor.

Uso: python scripts/gen_characters.py   (precisa de fonts/NewsCycle-Bold.woff)
Projeto de fa; personagens e marcas pertencem a Lucasfilm/Disney.
"""
import random
from pathlib import Path

from texts import T
from gen_static import GOTHIC, OUT, outline, starfield

W, H = 900, 310
GROUND = 252


def label(cx, text, color="#8ea3d6"):
    return f'<path transform="translate({cx} 288)" fill="{color}" d="{outline(GOTHIC, text, 15, 3)}"/>'


def shadow(cx, rx):
    return f'<ellipse cx="{cx}" cy="{GROUND + 2}" rx="{rx}" ry="5" fill="#000" opacity="0.55"/>'


def r2d2(cx):
    return f"""<g>
{shadow(cx, 34)}
<animateTransform attributeName="transform" type="rotate" values="-2.5 {cx} {GROUND};2.5 {cx} {GROUND};-2.5 {cx} {GROUND}" dur="3.4s" repeatCount="indefinite"/>
<rect x="{cx - 38}" y="198" width="11" height="50" rx="4" fill="#cdd6e2"/><rect x="{cx + 27}" y="198" width="11" height="50" rx="4" fill="#cdd6e2"/>
<rect x="{cx - 42}" y="240" width="19" height="12" rx="4" fill="#b7c2d1"/><rect x="{cx + 23}" y="240" width="19" height="12" rx="4" fill="#b7c2d1"/>
<rect x="{cx - 27}" y="160" width="54" height="84" rx="8" fill="#e8eef6"/>
<rect x="{cx - 27}" y="202" width="54" height="9" fill="#2f6fd6"/><rect x="{cx - 20}" y="222" width="40" height="14" rx="3" fill="#2f6fd6"/>
<rect x="{cx - 8}" y="180" width="16" height="12" rx="2" fill="#aab6c6"/>
<path d="M{cx - 27} 160A27 27 0 0 1 {cx + 27} 160Z" fill="#e8eef6"/>
<path d="M{cx - 27} 160A27 27 0 0 1 {cx - 9} 135.500 L{cx - 9} 160Z" fill="#2f6fd6" opacity="0.9"/>
<circle cx="{cx + 5}" cy="147" r="7.500" fill="#14161c" stroke="#aab6c6" stroke-width="1.500"/>
<circle cx="{cx + 5}" cy="147" r="3.600" fill="#ff3b3b"><animate attributeName="fill" values="#ff3b3b;#ff3b3b;#4bd5ee;#4bd5ee;#ff3b3b" keyTimes="0;.45;.5;.9;1" dur="4s" repeatCount="indefinite"/></circle>
<line x1="{cx + 14}" y1="136" x2="{cx + 22}" y2="118" stroke="#aab6c6" stroke-width="2"/>
<circle cx="{cx + 22}" cy="117" r="2.500" fill="#ffe81f"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>
</g>
{label(cx, "R2-D2")}"""


def c3po(cx):
    return f"""<g>
{shadow(cx, 34)}
<rect x="{cx - 22}" y="196" width="16" height="52" rx="6" fill="#e8b923"/><rect x="{cx + 6}" y="196" width="16" height="52" rx="6" fill="#e8b923"/>
<rect x="{cx - 24}" y="240" width="20" height="12" rx="4" fill="#b8860b"/><rect x="{cx + 4}" y="240" width="20" height="12" rx="4" fill="#b8860b"/>
<rect x="{cx - 31}" y="118" width="62" height="84" rx="16" fill="#f0c431"/>
<rect x="{cx - 31}" y="168" width="62" height="10" fill="#c99a14"/>
<circle cx="{cx}" cy="140" r="10" fill="#d4a017"/><circle cx="{cx}" cy="140" r="5" fill="#8a6a00"/>
<rect x="{cx - 46}" y="124" width="13" height="64" rx="6" fill="#e8b923"/>
<g><animateTransform attributeName="transform" type="rotate" values="0 {cx + 39} 128;-150 {cx + 39} 128;-125 {cx + 39} 128;-150 {cx + 39} 128;0 {cx + 39} 128" keyTimes="0;.18;.3;.42;.8" dur="5s" repeatCount="indefinite"/>
<rect x="{cx + 32}" y="124" width="13" height="64" rx="6" fill="#e8b923"/><circle cx="{cx + 38.500}" cy="192" r="7" fill="#f0c431"/></g>
<rect x="{cx - 21}" y="68" width="42" height="56" rx="18" fill="#f0c431"/>
<circle cx="{cx - 9}" cy="92" r="9" fill="#14110a"/><circle cx="{cx + 9}" cy="92" r="9" fill="#14110a"/>
<circle cx="{cx - 9}" cy="92" r="6.500" fill="#fff6b0"><animate attributeName="opacity" values="1;1;0.35;1;1" keyTimes="0;.7;.74;.78;1" dur="4s" repeatCount="indefinite"/></circle>
<circle cx="{cx + 9}" cy="92" r="6.500" fill="#fff6b0"><animate attributeName="opacity" values="1;1;0.35;1;1" keyTimes="0;.7;.74;.78;1" dur="4s" repeatCount="indefinite"/></circle>
<rect x="{cx - 8}" y="108" width="16" height="4" rx="2" fill="#8a6a00"/>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -1.500;0 0" dur="2.600s" repeatCount="indefinite"/>
</g>
{label(cx, "C-3PO")}"""


def vader(cx):
    s = cx + 47  # x do sabre
    return f"""<g>
{shadow(cx, 52)}
<rect x="{s - 3.500 - 9}" y="40" width="25" height="146" rx="12" fill="#ff2a2a" filter="url(#blur)" opacity="0.9"><animate attributeName="opacity" values="0.9;0.55;0.95;0.7;0.9" dur="0.9s" repeatCount="indefinite"/></rect>
<path d="M{cx - 40} 108L{cx - 66} {GROUND}L{cx + 66} {GROUND}L{cx + 40} 108Z" fill="#0a0a10"><animate attributeName="d" values="M{cx - 40} 108L{cx - 66} {GROUND}L{cx + 66} {GROUND}L{cx + 40} 108Z;M{cx - 40} 108L{cx - 62} {GROUND}L{cx + 70} {GROUND}L{cx + 40} 108Z;M{cx - 40} 108L{cx - 66} {GROUND}L{cx + 66} {GROUND}L{cx + 40} 108Z" dur="3.800s" repeatCount="indefinite"/></path>
<rect x="{cx - 20}" y="212" width="17" height="40" rx="5" fill="#101018"/><rect x="{cx + 3}" y="212" width="17" height="40" rx="5" fill="#101018"/>
<g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -1.800;0 0" dur="3s" repeatCount="indefinite"/>
<rect x="{s - 3.500}" y="40" width="7" height="140" rx="3.500" fill="#ffe3e3" stroke="#ff2a2a" stroke-width="1.500"/>
<rect x="{s - 5}" y="166" width="10" height="30" rx="2" fill="#9aa3b2"/><rect x="{s - 5}" y="176" width="10" height="3" fill="#4a5160"/><rect x="{s - 5}" y="184" width="10" height="3" fill="#4a5160"/>
<rect x="{cx - 36}" y="106" width="72" height="76" rx="12" fill="#15151c"/>
<rect x="{cx - 17}" y="126" width="34" height="26" rx="3" fill="#262633" stroke="#3a3a4a"/>
<circle cx="{cx - 9}" cy="134" r="3" fill="#ff3b3b"><animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/></circle>
<circle cx="{cx}" cy="134" r="3" fill="#4bd5ee"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.7s" repeatCount="indefinite"/></circle>
<circle cx="{cx + 9}" cy="134" r="3" fill="#4cff4c"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
<rect x="{cx - 12}" y="142" width="24" height="4" rx="1" fill="#5a5a6e"/>
<rect x="{cx - 36}" y="176" width="72" height="10" fill="#2a2a35"/><rect x="{cx - 7}" y="177" width="14" height="8" rx="2" fill="#aeb6c4"/>
<rect x="{cx - 56}" y="112" width="16" height="66" rx="8" fill="#101018"/><rect x="{s - 8}" y="112" width="16" height="62" rx="8" fill="#101018"/>
<path d="M{cx - 27} 90C{cx - 33} 48 {cx - 15} 32 {cx} 32C{cx + 15} 32 {cx + 33} 48 {cx + 27} 90L{cx + 17} 104L{cx - 17} 104Z" fill="#0d0d13"/>
<path d="M{cx - 23} 84L{cx - 36} 108L{cx + 36} 108L{cx + 23} 84Z" fill="#12121a"/>
<ellipse cx="{cx - 8}" cy="46" rx="9" ry="14" fill="#fff" opacity="0.07"/>
<ellipse cx="{cx - 11}" cy="68" rx="8" ry="6" fill="#1b1b24" stroke="#3b3b4b" stroke-width="1.500" transform="rotate(12 {cx - 11} 68)"/>
<ellipse cx="{cx + 11}" cy="68" rx="8" ry="6" fill="#1b1b24" stroke="#3b3b4b" stroke-width="1.500" transform="rotate(-12 {cx + 11} 68)"/>
<path d="M{cx - 3.500} 76L{cx} 84L{cx + 3.500} 76Z" fill="#2c2c38"/>
<rect x="{cx - 10}" y="88" width="20" height="12" rx="2" fill="#2c2c38"/>
<path d="M{cx - 6} 89V99M{cx - 2} 89V99M{cx + 2} 89V99M{cx + 6} 89V99" stroke="#555566" stroke-width="1.200"/>
<path d="M{cx - 20} 98L{cx - 24} 106M{cx + 20} 98L{cx + 24} 106" stroke="#333342" stroke-width="2"/>
</g>
</g>
{label(cx, "DARTH VADER", "#ff6b6b")}"""


def han(cx):
    bolt_x = cx - 92
    return f"""<g>
{shadow(cx, 32)}
<rect x="{cx - 22}" y="188" width="19" height="52" rx="4" fill="#1d2a44"/><rect x="{cx + 3}" y="188" width="19" height="52" rx="4" fill="#1d2a44"/>
<rect x="{cx - 22}" y="188" width="3.500" height="52" fill="#c0392b"/><rect x="{cx + 18.500}" y="188" width="3.500" height="52" fill="#c0392b"/>
<rect x="{cx - 25}" y="236" width="22" height="16" rx="4" fill="#15151a"/><rect x="{cx + 3}" y="236" width="22" height="16" rx="4" fill="#15151a"/>
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -1.200;0 0" dur="2.200s" repeatCount="indefinite"/>
<rect x="{cx - 25}" y="118" width="50" height="74" rx="9" fill="#f2f2f2"/>
<rect x="{cx - 25}" y="118" width="17" height="74" rx="6" fill="#17171c"/><rect x="{cx + 8}" y="118" width="17" height="74" rx="6" fill="#17171c"/>
<rect x="{cx - 26}" y="178" width="52" height="9" fill="#5a3a1a"/><rect x="{cx - 7}" y="179" width="12" height="7" rx="1" fill="#c9a24a"/>
<rect x="{cx + 25}" y="124" width="14" height="58" rx="7" fill="#f2f2f2"/><circle cx="{cx + 32}" cy="184" r="6" fill="#f0c9a0"/>
<rect x="{cx - 62}" y="124" width="40" height="13" rx="6" fill="#f2f2f2"/><circle cx="{cx - 64}" cy="130" r="6.500" fill="#f0c9a0"/>
<rect x="{cx - 94}" y="124" width="32" height="10" rx="3" fill="#3a3f4b"/><rect x="{cx - 70}" y="130" width="9" height="16" rx="2" fill="#2a2d36"/><rect x="{cx - 96}" y="126" width="6" height="6" fill="#1b1d24"/>
<circle cx="{cx}" cy="95" r="20" fill="#f0c9a0"/>
<path d="M{cx - 21} 92C{cx - 22} 68 {cx + 22} 68 {cx + 21} 92C{cx + 14} 80 {cx - 14} 80 {cx - 21} 92Z" fill="#4a3320"/>
<circle cx="{cx - 8}" cy="97" r="2.200" fill="#222"/><circle cx="{cx + 8}" cy="97" r="2.200" fill="#222"/>
<path d="M{cx - 7} 108Q{cx} 113 {cx + 8} 106" fill="none" stroke="#9a5a3a" stroke-width="2" stroke-linecap="round"/>
</g>
<g><rect x="{bolt_x}" y="127" width="22" height="5" rx="2.500" fill="#ff3030" filter="url(#blur)" opacity="0"/>
<rect x="{bolt_x}" y="127.500" width="20" height="4" rx="2" fill="#fff0f0" opacity="0">
<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.03;.14;.15;1" dur="3.600s" repeatCount="indefinite"/>
<animateTransform attributeName="transform" type="translate" values="0 0;-6 0;-36 0;-36 0" keyTimes="0;.03;.14;1" dur="3.600s" repeatCount="indefinite"/></rect>
<circle cx="{cx - 128}" cy="130" r="10" fill="#ffe81f" filter="url(#blur)" opacity="0">
<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.13;.15;.25;1" dur="3.600s" repeatCount="indefinite"/></circle></g>
</g>
{label(cx, "HAN SOLO", "#ffd27a")}"""


def chewie(cx):
    fur, dark = "#7a4a22", "#4a2b12"
    return f"""<g>
{shadow(cx, 44)}
<rect x="{cx - 32}" y="204" width="24" height="48" rx="9" fill="{fur}"/><rect x="{cx + 8}" y="204" width="24" height="48" rx="9" fill="{fur}"/>
<rect x="{cx - 36}" y="242" width="30" height="10" rx="5" fill="{dark}"/><rect x="{cx + 6}" y="242" width="30" height="10" rx="5" fill="{dark}"/>
<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -1.500;0 0" dur="2.800s" repeatCount="indefinite"/>
<rect x="{cx - 38}" y="96" width="76" height="118" rx="30" fill="{fur}"/>
<rect x="{cx - 58}" y="104" width="22" height="84" rx="11" fill="{fur}"/>
<g><animateTransform attributeName="transform" type="rotate" values="0 {cx + 44} 110;-22 {cx + 44} 110;0 {cx + 44} 110" dur="2.800s" repeatCount="indefinite"/>
<rect x="{cx + 36}" y="104" width="22" height="84" rx="11" fill="{fur}"/><circle cx="{cx + 47}" cy="190" r="10" fill="{dark}"/></g>
<path d="M{cx - 32} 108L{cx + 34} 188" stroke="#3a2410" stroke-width="11" stroke-linecap="round"/>
<path d="M{cx - 28} 111L{cx + 30} 184" stroke="#c9a24a" stroke-width="2.500" stroke-dasharray="4 5"/>
<path d="M{cx - 30} 150Q{cx - 18} 154 {cx - 8} 148M{cx + 8} 170Q{cx + 20} 176 {cx + 30} 168M{cx - 20} 190Q{cx - 8} 195 {cx + 4} 189" stroke="{dark}" stroke-width="2" fill="none" opacity="0.7"/>
<rect x="{cx - 26}" y="52" width="52" height="62" rx="24" fill="{fur}"/>
<path d="M{cx - 26} 70L{cx - 32} 56L{cx - 18} 62L{cx - 12} 48L{cx - 4} 60L{cx + 6} 46L{cx + 12} 60L{cx + 24} 50L{cx + 22} 66Z" fill="{dark}"/>
<ellipse cx="{cx}" cy="94" rx="16" ry="19" fill="#c9a27a"/>
<circle cx="{cx - 8}" cy="82" r="3.500" fill="#101820"/><circle cx="{cx + 8}" cy="82" r="3.500" fill="#101820"/>
<circle cx="{cx - 8.600}" cy="81" r="1.200" fill="#fff"/><circle cx="{cx + 7.400}" cy="81" r="1.200" fill="#fff"/>
<ellipse cx="{cx}" cy="91" rx="5" ry="3.500" fill="#1a1008"/>
<ellipse cx="{cx}" cy="103" rx="7" ry="2" fill="#3a1410"><animate attributeName="ry" values="2;2;7;2;2" keyTimes="0;.55;.62;.72;1" dur="4s" repeatCount="indefinite"/></ellipse>
</g>
</g>
{label(cx, "CHEWBACCA", "#d9a066")}"""


def build():
    rng = random.Random(5)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{T["alt_cast"]}">
<title>Elenco: R2-D2, C-3PO, Darth Vader, Han Solo e Chewbacca</title>
<defs>
<filter id="blur" x="-100%" y="-30%" width="300%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="bgE" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050c"/><stop offset="1" stop-color="#101a3a"/></linearGradient>
<linearGradient id="floor" x1="0" x2="1"><stop offset="0" stop-color="#4bd5ee" stop-opacity="0"/><stop offset="0.5" stop-color="#ffe81f" stop-opacity="0.55"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></linearGradient>
<linearGradient id="shoot" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<clipPath id="cp"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#cp)">
<rect width="{W}" height="{H}" fill="url(#bgE)"/>
{starfield(rng, 70)}
<rect x="0" y="{GROUND + 1}" width="{W}" height="2" fill="url(#floor)"/>
{r2d2(100)}
{c3po(250)}
{vader(440)}
{han(630)}
{chewie(790)}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="#FFE81F" stroke-opacity="0.45"/>
</svg>
"""
    (OUT / "elenco.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build()
    print("elenco.svg", (OUT / "elenco.svg").stat().st_size // 1024, "KB")
