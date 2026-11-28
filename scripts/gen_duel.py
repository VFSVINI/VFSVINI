"""Gera assets/duelo.svg: Mestre Yoda x Imperador Palpatine, com Obi-Wan e Luke de guarda.

A coreografia dura DUR segundos e repete: salto e choque de sabres, Raio da Forca bloqueado
com o sabre, segundo salto com mortal e novo choque. Os angulos dos bracos nos choques sao
calculados para as laminas se encontrarem no ponto do choque.
Projeto de fa; personagens pertencem a Lucasfilm/Disney.
"""
import math
import random

from fontkit import GOTHIC, text_path
from gen_static import OUT, starfield
from texts import T

W, H = 900, 344
GROUND = 290
DUR = 7.0
YELLOW = "#FFE81F"


# ---------------------------------------------------------------- animacao
def _fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") or "0"


def _norm(frames):
    frames = sorted(frames, key=lambda f: f[0])
    if frames[0][0] > 0:
        frames.insert(0, (0.0,) + tuple(frames[0][1:]))
    if frames[-1][0] < DUR:
        frames.append((DUR,) + tuple(frames[-1][1:]))
    return frames


def _keytimes(frames):
    out = []
    for t, *_ in frames:
        v = min(max(t / DUR, 0.0), 1.0)
        out.append(f"{v:.4f}".rstrip("0").rstrip(".") or "0")
    return ";".join(out)


def a_translate(frames):
    f = _norm(frames)
    vals = ";".join(f"{_fmt(x)} {_fmt(y)}" for _, x, y in f)
    return f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{_keytimes(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_rotate(frames, cx, cy):
    f = _norm(frames)
    vals = ";".join(f"{_fmt(a)} {cx} {cy}" for _, a in f)
    return f'<animateTransform attributeName="transform" type="rotate" values="{vals}" keyTimes="{_keytimes(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_scale(frames):
    f = _norm(frames)
    vals = ";".join(f"{v:.2f}" for _, v in f)
    return f'<animateTransform attributeName="transform" type="scale" values="{vals}" keyTimes="{_keytimes(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_opacity(frames):
    f = _norm(frames)
    vals = ";".join(f"{v:.2f}".rstrip("0").rstrip(".") or "0" for _, v in f)
    return f'<animate attributeName="opacity" values="{vals}" keyTimes="{_keytimes(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


# ---------------------------------------------------------------- sabres e efeitos
def blade(x, y, w, length, color, core="#ffffff", horizontal=True, direction=1):
    """Lamina com brilho. horizontal: cresce no eixo x (direction +1 direita, -1 esquerda)."""
    if horizontal:
        x0 = x if direction > 0 else x - length
        glow = f'<rect x="{x0}" y="{y - w * 1.6}" width="{length}" height="{w * 3.2}" rx="{w * 1.6}" fill="{color}" filter="url(#bl)" opacity="0.9"/>'
        body = f'<rect x="{x0}" y="{y - w / 2}" width="{length}" height="{w}" rx="{w / 2}" fill="{core}" stroke="{color}" stroke-width="1.4"/>'
    else:
        glow = f'<rect x="{x - w * 1.6}" y="{y - length}" width="{w * 3.2}" height="{length}" rx="{w * 1.6}" fill="{color}" filter="url(#bl)" opacity="0.9"/>'
        body = f'<rect x="{x - w / 2}" y="{y - length}" width="{w}" height="{length}" rx="{w / 2}" fill="{core}" stroke="{color}" stroke-width="1.4"/>'
    return glow + body


def spark(x, y, t0, big=1.0):
    rays = "".join(
        f'<line x1="0" y1="0" x2="{30 * math.cos(math.radians(a)):.1f}" y2="{30 * math.sin(math.radians(a)):.1f}" stroke="#fff6c2" stroke-width="2" stroke-linecap="round"/>'
        for a in range(0, 360, 40)
    )
    op = [(t0 - 0.06, 0), (t0, 1), (t0 + 0.32, 0)]
    sc = [(t0 - 0.06, 0.1), (t0, 1.5 * big), (t0 + 0.32, 0.4)]
    return (
        f'<g transform="translate({_fmt(x)} {_fmt(y)})"><g opacity="0">{a_opacity(op)}<g>{a_scale(sc)}'
        f'<circle r="20" fill="url(#spark)"/>{rays}</g></g></g>'
    )


def flicker_spark(x, y, t0, t1):
    frames, t, on = [(t0 - 0.05, 0)], t0, 1
    while t < t1:
        frames.append((t, 1 if on else 0.25))
        on ^= 1
        t += 0.09
    frames.append((t1, 0))
    return (
        f'<g transform="translate({_fmt(x)} {_fmt(y)})"><g opacity="0">{a_opacity(frames)}'
        f'<circle r="14" fill="url(#spark)"/></g></g>'
    )


def bolt_points(p0, p1, rng, n=9, amp=9.0):
    pts = [p0]
    for i in range(1, n):
        t = i / n
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t + rng.uniform(-amp, amp)
        pts.append((x, y))
    pts.append(p1)
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def lightning(p0, targets, t0, t1, rng):
    parts = []
    for p1, width in targets:
        ds = [bolt_points(p0, p1, rng) for _ in range(4)]
        values = ";".join(ds + [ds[0]])
        kt = "0;0.25;0.5;0.75;1"
        anim = f'<animate attributeName="d" values="{values}" keyTimes="{kt}" dur="0.24s" repeatCount="indefinite" calcMode="discrete"/>'
        parts.append(f'<path d="{ds[0]}" fill="none" stroke="#3fa8ff" stroke-width="{width * 3}" stroke-linejoin="round" opacity="0.55" filter="url(#bl)">{anim}</path>')
        parts.append(f'<path d="{ds[0]}" fill="none" stroke="#e6f9ff" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round">{anim}</path>')
    op = [(t0 - 0.05, 0), (t0, 1), (t1, 1), (t1 + 0.05, 0)]
    return f'<g opacity="0">{a_opacity(op)}{"".join(parts)}</g>'


# ---------------------------------------------------------------- personagens
def yoda(clash1, clash2):
    """Yoda de frente para a direita. Origem nos pes."""
    base = (390, GROUND)
    pivot = (12, -46)
    off1, off2 = (35, -55), (40, -90)
    th1 = math.degrees(math.atan2(clash1[1] - (base[1] + off1[1] + pivot[1]), clash1[0] - (base[0] + off1[0] + pivot[0])))
    th2 = math.degrees(math.atan2(clash2[1] - (base[1] + off2[1] + pivot[1]), clash2[0] - (base[0] + off2[0] + pivot[0])))
    jump = [
        (0, 0, 0), (0.9, 0, 0), (1.1, 15, -40), (1.3, 28, -54), (1.45, *off1), (1.6, 30, -50),
        (1.9, 15, -25), (2.2, 10, 0), (4.4, 10, 0), (4.55, 20, -45), (4.75, 36, -88), (4.9, *off2),
        (5.1, 30, -85), (5.4, 15, -40), (5.7, 5, 0), (6.2, 0, 0),
    ]
    flip = [(0, 0), (4.5, 0), (4.8, 360)]
    arm = [
        (0, -25), (0.8, -55), (1.0, -40), (1.45, th1), (1.7, -10), (2.2, -25), (2.6, -30), (2.85, -75),
        (3.1, -82), (3.3, -70), (3.5, -80), (3.7, -72), (3.9, -78), (4.2, -60), (4.4, -60), (4.9, th2),
        (5.2, -10), (5.9, -25),
    ]
    skin, skin_d, robe, robe_d = "#9bc376", "#6f9a50", "#c8a96e", "#8b6b43"
    svg = f"""<g transform="translate({base[0]} {base[1]})">
<ellipse cx="0" cy="2" rx="30" ry="5" fill="#000" opacity="0.55"/>
<g>{a_translate(jump)}
<g>{a_rotate(flip, 0, -45)}
<ellipse cx="-9" cy="-3" rx="8" ry="4" fill="{skin}"/><ellipse cx="9" cy="-3" rx="8" ry="4" fill="{skin}"/>
<path d="M-17 -50Q-24 -18 -22 -4L22 -4Q24 -18 17 -50Z" fill="{robe}"/>
<path d="M-17 -50Q0 -42 17 -50L19 -38Q0 -30 -19 -38Z" fill="{robe_d}"/>
<rect x="-18" y="-24" width="36" height="5" fill="#7a5a35"/>
<rect x="-27" y="-48" width="9" height="22" rx="4" fill="{robe}"/>
<path d="M-12 -70L-46 -84L-14 -56Z" fill="{skin}" stroke="{skin_d}"/><path d="M12 -70L46 -84L14 -56Z" fill="{skin}" stroke="{skin_d}"/>
<path d="M-14 -68L-36 -78L-15 -60Z" fill="{skin_d}" opacity="0.5"/><path d="M14 -68L36 -78L15 -60Z" fill="{skin_d}" opacity="0.5"/>
<ellipse cx="0" cy="-66" rx="15" ry="13" fill="{skin}"/>
<path d="M-6 -78Q-2 -92 2 -78M0 -78Q6 -90 9 -77M-9 -76Q-12 -86 -5 -78" stroke="#f0f0e8" fill="none" stroke-width="1.6" stroke-linecap="round"/>
<ellipse cx="-6" cy="-67" rx="3.4" ry="2.8" fill="#f4f1e0"/><ellipse cx="6" cy="-67" rx="3.4" ry="2.8" fill="#f4f1e0"/>
<circle cx="-5.2" cy="-67" r="1.6" fill="#5b3b12"/><circle cx="6.8" cy="-67" r="1.6" fill="#5b3b12"/>
<path d="M-11 -72Q-6 -76 -2 -72M2 -72Q6 -76 11 -72M-8 -76Q0 -79 8 -76" stroke="{skin_d}" fill="none" stroke-width="1.2"/>
<path d="M-5 -58Q0 -55.500 5 -58" stroke="{skin_d}" fill="none" stroke-width="1.4" stroke-linecap="round"/>
<g>{a_rotate(arm, pivot[0], pivot[1])}
<rect x="12" y="-50" width="26" height="8" rx="4" fill="{robe}"/>
<circle cx="40" cy="-46" r="4.5" fill="{skin}"/>
<rect x="36" y="-49" width="16" height="6" rx="1.5" fill="#9aa3b2"/><rect x="42" y="-49" width="2" height="6" fill="#4a5160"/>
{blade(52, -46, 5, 60, "#4cff4c", "#e6ffe6")}
</g>
</g></g></g>"""
    return svg


def emperor(clash1, clash2, rng):
    base = (560, GROUND)
    sp = (-24, -130)  # ombro do braco do sabre
    fp = (-16, -124)  # ombro do braco do raio
    off = [
        (0, 0, 0), (1.45, 0, 0), (1.55, 10, 0), (2.0, 0, 0), (2.7, 0, 0), (3.0, -12, 0), (4.05, -12, 0),
        (4.35, 0, 0), (4.9, 0, 0), (5.0, 12, -2), (5.6, 0, 0),
    ]

    def rot_to(target, pivot, eo=(0, 0)):
        px, py = base[0] + eo[0] + pivot[0], base[1] + eo[1] + pivot[1]
        ang = math.degrees(math.atan2(target[1] - py, target[0] - px))
        return ang - 180 if ang > 0 else ang + 180  # direcao local do braco e 180 graus

    r1 = rot_to(clash1, sp)
    r2 = rot_to(clash2, sp)
    saber = [
        (0, -40), (1.0, -45), (1.35, -34), (1.45, r1), (1.7, -45), (2.5, -45), (2.8, -75), (4.1, -75),
        (4.4, -45), (4.8, -34), (4.9, r2), (5.2, -45), (7.0, -40),
    ]
    # alvo do raio: ponta do sabre do Yoda erguido (10, 0 de deslocamento, braco a -75 graus)
    ytip = (390 + 10 + 12 + 98 * math.cos(math.radians(-75)), GROUND - 46 + 98 * math.sin(math.radians(-75)))
    fpw = (base[0] - 12 + fp[0], base[1] + fp[1])
    phi = math.degrees(math.atan2(ytip[1] - fpw[1], ytip[0] - fpw[0]))
    zap = phi - 180 + 360 if phi - 180 < -180 else phi - 180
    front = [(0, -90), (2.6, -90), (2.85, zap), (3.1, zap + 3), (3.3, zap - 3), (3.5, zap + 3), (3.7, zap - 2), (3.9, zap + 2), (4.0, zap), (4.25, -90)]
    hand = (fpw[0] + 32 * math.cos(math.radians(phi)), fpw[1] + 32 * math.sin(math.radians(phi)))
    body_target = (404, GROUND - 52)
    bolts = lightning(hand, [(ytip, 2.6), (body_target, 1.8)], 2.9, 3.95, rng)
    robe, robe_d, pale = "#0f0f17", "#1d1d2b", "#c3be9c"
    svg = f"""<g transform="translate({base[0]} {base[1]})">
<ellipse cx="0" cy="2" rx="66" ry="6" fill="#000" opacity="0.6"/>
<g>{a_translate(off)}
<path d="M-30 -148C-56 -96 -74 -34 -78 -2L78 -2C74 -34 56 -96 30 -148Z" fill="{robe}"/>
<path d="M-10 -140C-14 -90 -18 -40 -20 -2M14 -140C18 -90 22 -40 26 -2M-40 -100C-46 -60 -54 -30 -58 -2" stroke="{robe_d}" stroke-width="3" fill="none"/>
<g>{a_rotate(saber, sp[0], sp[1])}
<rect x="-50" y="-135" width="26" height="10" rx="5" fill="{robe}" stroke="{robe_d}"/>
<circle cx="-52" cy="-130" r="5" fill="{pale}"/>
<rect x="-68" y="-133" width="16" height="6" rx="1.5" fill="#7d8594"/><rect x="-62" y="-133" width="2" height="6" fill="#2a2f39"/>
{blade(-68, -130, 5, 70, "#ff2a2a", "#ffe3e3", direction=-1)}
</g>
<path d="M-30 -132C-40 -176 -12 -194 0 -194C12 -194 40 -176 30 -132Z" fill="#0a0a10"/>
<ellipse cx="-4" cy="-150" rx="15" ry="19" fill="{pale}"/>
<path d="M-23 -156C-21 -178 13 -180 15 -156C7 -165 -15 -165 -23 -156Z" fill="#0a0a10"/>
<path d="M-25 -150C-35 -140 -33 -126 -29 -120L-20 -128Z" fill="#0a0a10"/><path d="M17 -150C27 -140 25 -126 21 -120L12 -128Z" fill="#0a0a10"/>
<ellipse cx="-11" cy="-153" rx="3" ry="1.7" fill="#ffd23f"/><ellipse cx="3" cy="-153" rx="3" ry="1.7" fill="#ffd23f"/>
<path d="M-5 -150L-8 -141L-4 -141" stroke="#8d8868" fill="none" stroke-width="1.2"/>
<path d="M-12 -135Q-5 -131.500 3 -136" stroke="#5a5540" fill="none" stroke-width="1.6" stroke-linecap="round"/>
<path d="M-14 -146L-9 -148M0 -146L5 -148M-10 -139L-14 -138M2 -139L6 -138" stroke="#8d8868" stroke-width="1"/>
<path d="M-14 -128L0 -112L14 -128Z" fill="#17171f"/>
<g>{a_rotate(front, fp[0], fp[1])}
<rect x="-46" y="-129" width="30" height="10" rx="5" fill="{robe}" stroke="{robe_d}"/>
<circle cx="-48" cy="-124" r="5.5" fill="{pale}"/>
<path d="M-52 -128L-58 -131M-53 -124L-60 -125M-52 -120L-58 -118" stroke="{pale}" stroke-width="2" stroke-linecap="round"/>
</g>
</g></g>
{bolts}"""
    return svg


def jedi(cx, mirror, cloak, tunic, belt, hair, beard, saber_color, core, name_color):
    """Obi-Wan / Luke de guarda: respiracao e brilho do sabre."""
    sx = -1 if mirror else 1
    beard_svg = (
        f'<path d="M-15 -164Q-17 -146 0 -142Q17 -146 15 -164Q8 -154 0 -154Q-8 -154 -15 -164Z" fill="{beard}"/>' if beard else ""
    )
    return f"""<g transform="translate({cx} {GROUND}) scale({sx} 1)">
<ellipse cx="0" cy="2" rx="36" ry="5" fill="#000" opacity="0.55"/>
<g>{a_translate([(0, 0, 0), (1.5, 0, -1.6), (3.0, 0, 0), (4.5, 0, -1.6), (6.0, 0, 0), (7.0, 0, 0)])}
<path d="M-28 -150L-46 -4L46 -4L28 -150Z" fill="{cloak}"/>
<rect x="-17" y="-60" width="14" height="56" rx="4" fill="#2a1e12"/><rect x="3" y="-60" width="14" height="56" rx="4" fill="#2a1e12"/>
<rect x="-19" y="-14" width="17" height="12" rx="4" fill="#15100a"/><rect x="2" y="-14" width="17" height="12" rx="4" fill="#15100a"/>
<rect x="-24" y="-150" width="48" height="94" rx="12" fill="{tunic}"/>
<rect x="-24" y="-92" width="48" height="9" fill="{belt}"/><rect x="-6" y="-92" width="12" height="9" rx="2" fill="#c9a24a"/>
<rect x="-34" y="-146" width="12" height="52" rx="6" fill="{tunic}"/><circle cx="-28" cy="-92" r="6" fill="#efc9a0"/>
<rect x="22" y="-146" width="12" height="50" rx="6" fill="{tunic}"/><circle cx="28" cy="-94" r="6" fill="#efc9a0"/>
<rect x="24" y="-110" width="8" height="26" rx="2" fill="#9aa3b2"/><rect x="24" y="-100" width="8" height="3" fill="#4a5160"/><rect x="24" y="-93" width="8" height="3" fill="#4a5160"/>
{blade(28, -110, 5.5, 84, saber_color, core, horizontal=False)}
<circle cx="0" cy="-168" r="17" fill="#efc9a0"/>
{beard_svg}
<path d="M-18 -170Q-18 -190 0 -190Q18 -190 18 -170Q10 -178 0 -177Q-10 -178 -18 -170Z" fill="{hair}"/>
<circle cx="-6" cy="-168" r="1.8" fill="#2a1a0a"/><circle cx="6" cy="-168" r="1.8" fill="#2a1a0a"/>
<path d="M-4 -162Q0 -160 4 -162" stroke="#a5683e" fill="none" stroke-width="1.3" stroke-linecap="round"/>
</g></g>"""


def label(cx, text, color):
    return text_path(GOTHIC, text, 15, 3, cx, 322, color, "middle")


def build():
    rng = random.Random(21)
    names = T["duel_names"]
    clash1, clash2 = (488, 190), (486, 158)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{T["alt_duel"]}">
<title>{T["alt_duel"]}</title>
<defs>
<filter id="bl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.5"/></filter>
<radialGradient id="spark"><stop offset="0" stop-color="#fff"/><stop offset="0.4" stop-color="#ffe81f"/><stop offset="1" stop-color="#ffe81f" stop-opacity="0"/></radialGradient>
<linearGradient id="bgD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050c"/><stop offset="1" stop-color="#101a3a"/></linearGradient>
<linearGradient id="floorD" x1="0" x2="1"><stop offset="0" stop-color="#4bd5ee" stop-opacity="0"/><stop offset="0.35" stop-color="#4bd5ee" stop-opacity="0.7"/><stop offset="0.65" stop-color="#ff2a2a" stop-opacity="0.7"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></linearGradient>
<linearGradient id="shoot" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<radialGradient id="glowL"><stop offset="0" stop-color="#4bd5ee" stop-opacity="0.22"/><stop offset="1" stop-color="#4bd5ee" stop-opacity="0"/></radialGradient>
<radialGradient id="glowR"><stop offset="0" stop-color="#ff2a2a" stop-opacity="0.22"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></radialGradient>
<clipPath id="cpD"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#cpD)">
<rect width="{W}" height="{H}" fill="url(#bgD)"/>
<ellipse cx="300" cy="260" rx="260" ry="90" fill="url(#glowL)"/><ellipse cx="620" cy="260" rx="260" ry="90" fill="url(#glowR)"/>
{starfield(rng, 90)}
<rect x="0" y="{GROUND + 1}" width="{W}" height="2" fill="url(#floorD)"/>
{jedi(110, False, "#5d4527", "#c9ab78", "#4a3320", "#8a5a2b", "#b9824a", "#5ab8ff", "#e6f4ff", "#4bd5ee")}
{jedi(790, True, "#101018", "#1b1b23", "#3a3a46", "#d6b06a", None, "#4cff4c", "#e6ffe6", "#4cff4c")}
{yoda(clash1, clash2)}
{emperor(clash1, clash2, rng)}
{spark(*clash1, 1.45)}
{spark(*clash2, 4.9, 1.2)}
{flicker_spark(390 + 10 + 12 + 98 * math.cos(math.radians(-75)), GROUND - 46 + 98 * math.sin(math.radians(-75)), 2.9, 3.95)}
{label(110, names["obi"], "#4BD5EE")}
{label(345, names["yoda"], "#8FE08A")}
{label(582, names["emp"], "#FF5A5A")}
{label(790, names["luke"], "#4CFF4C")}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{YELLOW}" stroke-opacity="0.45"/>
</svg>
"""
    (OUT / "duelo.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build()
    print("duelo.svg", (OUT / "duelo.svg").stat().st_size // 1024, "KB")
