"""Gera assets/duelo.svg: dois duelos de sabre cinematograficos e simultaneos.

Obi-Wan x Vader e Yoda x Imperador, 12 s em loop, fora de sincronia. Cada lutador tem posicao,
mortal, direcao do olhar (vira de frente ao trocar de lado) e braco do sabre animados. Nos choques
o ponto de contato e o ponto medio entre os dois ombros, e o codigo valida que as laminas alcancam
esse ponto. Efeitos: faiscas, onda de choque, raio anamorfico, flash, tremor, poeira, rastro dos
sabres, Raio da Forca e vinheta. Projeto de fa; personagens pertencem a Lucasfilm/Disney.
"""
import math
import random

from fontkit import GOTHIC, text_path
from gen_static import OUT, starfield
from texts import T

W, H = 900, 344
GROUND = 290
DUR = 12.0
YELLOW = "#FFE81F"


# ====================================================================== animacao
def _f(v, n=1):
    return f"{v:.{n}f}".rstrip("0").rstrip(".") or "0"


def _norm(frames):
    frames = sorted(frames, key=lambda f: f[0])
    if frames[0][0] > 0:
        frames.insert(0, (0.0,) + tuple(frames[0][1:]))
    if frames[-1][0] < DUR:
        frames.append((DUR,) + tuple(frames[-1][1:]))
    return frames


def _kt(frames):
    return ";".join(_f(min(max(t / DUR, 0.0), 1.0), 4) for t, *_ in frames)


def a_translate(frames):
    f = _norm(frames)
    vals = ";".join(f"{_f(x)} {_f(y)}" for _, x, y in f)
    return f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{_kt(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_rotate(frames, cx, cy):
    f = _norm(frames)
    vals = ";".join(f"{_f(a)} {cx} {cy}" for _, a in f)
    return f'<animateTransform attributeName="transform" type="rotate" values="{vals}" keyTimes="{_kt(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_scale(frames):
    f = _norm(frames)
    vals = ";".join(_f(v, 2) for _, v in f)
    return f'<animateTransform attributeName="transform" type="scale" values="{vals}" keyTimes="{_kt(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_opacity(frames):
    f = _norm(frames)
    vals = ";".join(_f(v, 2) for _, v in f)
    return f'<animate attributeName="opacity" values="{vals}" keyTimes="{_kt(f)}" dur="{DUR}s" repeatCount="indefinite"/>'


def a_facing(frames, sc, n):
    """Escala discreta: inverte o desenho quando o lutador vira de frente (frames [(t, +1|-1)])."""
    fr = sorted(frames)
    if fr[0][0] > 0:
        fr.insert(0, (0.0, fr[0][1]))
    vals = ";".join(f"{_f(sc * f * n, 3)} {_f(sc, 3)}" for _, f in fr)
    kts = ";".join(_f(min(t / DUR, 1.0), 4) for t, _ in fr)
    return f'<animateTransform attributeName="transform" type="scale" values="{vals}" keyTimes="{kts}" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete"/>'


def interp(frames, t):
    f = _norm(frames)
    for a, b in zip(f, f[1:]):
        if a[0] <= t <= b[0]:
            k = 0.0 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0])
            return tuple(a[i] + (b[i] - a[i]) * k for i in range(1, len(a)))
    return tuple(f[-1][1:])


def norm180(a):
    while a > 180:
        a -= 360
    while a <= -180:
        a += 360
    return a


# ====================================================================== lutador
class Fighter:
    def __init__(self, name, bx, sc, n, pivot, reach, cy, color, pos, face, flip, pivot2=None):
        self.name, self.bx, self.sc, self.n = name, bx, sc, n
        self.pv, self.r0, self.r1, self.cy, self.color = pivot, reach[0], reach[1], cy, color
        self.pos, self.face_f, self.flip = pos, sorted(face), flip
        self.pv2 = pivot2
        self.specs, self.specs2 = [], []   # (t, theta | ("C", ponto))
        self.theta, self.theta2 = [], []   # resolvidos
        self.alpha, self.alpha2 = [], []

    def x(self, t):
        return interp(self.pos, t)[0]

    def y(self, t):
        return interp(self.pos, t)[1]

    def f(self, t):
        cur = self.face_f[0][1]
        for ft, fv in self.face_f:
            if ft <= t + 1e-9:
                cur = fv
        return cur

    def pivot_w(self, t, which=1):
        p = self.pv if which == 1 else self.pv2
        return (self.x(t) + self.sc * self.f(t) * self.n * p[0], GROUND + self.y(t) + self.sc * p[1])

    def theta_to(self, t, c, which=1):
        px, py = self.pivot_w(t, which)
        phi = math.degrees(math.atan2(c[1] - py, c[0] - px))
        return phi if self.f(t) > 0 else norm180(180 - phi)

    def theta_at(self, t):
        return interp(self.theta, t)[0]

    def resolve(self):
        for which, specs, outt, outa in ((1, self.specs, "theta", "alpha"), (2, self.specs2, "theta2", "alpha2")):
            if not specs:
                continue
            frames = []
            for t, sp in sorted(specs, key=lambda s: s[0]):
                frames.append((t, self.theta_to(t, sp[1], which) if isinstance(sp, tuple) else sp))
            setattr(self, outt, frames)
            al = [a * self.n for _, a in frames]
            for i in range(1, len(al)):
                while al[i] - al[i - 1] > 180:
                    al[i] -= 360
                while al[i] - al[i - 1] < -180:
                    al[i] += 360
            setattr(self, outa, [(t, a) for (t, _), a in zip(frames, al)])

    def pos_off(self):
        return [(t, x - self.bx, y) for t, x, y in self.pos]

    def render(self, body):
        shadow = a_translate([(t, x - self.bx, 0) for t, x, y in self.pos])
        return f"""<g transform="translate({self.bx} {GROUND})">
<g>{shadow}<ellipse cx="0" cy="2" rx="{_f(self.sc * 52)}" ry="5" fill="#000" opacity="0.55"/></g>
<g>{a_translate(self.pos_off())}
<g>{a_rotate(self.flip, 0, self.cy)}
<g>{a_facing(self.face_f, self.sc, self.n)}
{body}
</g></g></g></g>"""


IMPACTS, RINGS, DUSTS, SWOOSH, SHOCK = [], [], [], [], []


def clash(t, a, b, big=1.0, dy=-4):
    pa, pb = a.pivot_w(t), b.pivot_w(t)
    c = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 + dy)
    for f, p in ((a, pa), (b, pb)):
        d = math.dist(p, c)
        lo, hi = f.r0 * f.sc, f.r1 * f.sc
        assert lo <= d <= hi, f"{f.name}: choque em t={t} fora de alcance ({d:.0f}, aceito {lo:.0f}..{hi:.0f})"
        f.specs.append((t, ("C", c)))
    IMPACTS.append((t, c, big))
    return c


# ====================================================================== desenho
def blade(x, y, w, length, color, core="#ffffff", direction=1):
    x0 = x if direction > 0 else x - length
    return (
        f'<rect x="{x0}" y="{y - w * 1.6}" width="{length}" height="{w * 3.2}" rx="{w * 1.6}" fill="{color}" filter="url(#bl)" opacity="0.9"/>'
        f'<rect x="{x0}" y="{y - w / 2}" width="{length}" height="{w}" rx="{w / 2}" fill="{core}" stroke="{color}" stroke-width="1.4"/>'
    )


def body_obi(arm):
    return f"""<path d="M-28 -150L-46 -4L46 -4L28 -150Z" fill="#5d4527"/>
<rect x="-17" y="-60" width="14" height="56" rx="4" fill="#2a1e12"/><rect x="3" y="-60" width="14" height="56" rx="4" fill="#2a1e12"/>
<rect x="-19" y="-14" width="17" height="12" rx="4" fill="#15100a"/><rect x="2" y="-14" width="17" height="12" rx="4" fill="#15100a"/>
<rect x="-24" y="-150" width="48" height="94" rx="12" fill="#c9ab78"/>
<rect x="-24" y="-92" width="48" height="9" fill="#4a3320"/><rect x="-6" y="-92" width="12" height="9" rx="2" fill="#c9a24a"/>
<rect x="-34" y="-146" width="12" height="52" rx="6" fill="#c9ab78"/><circle cx="-28" cy="-92" r="6" fill="#efc9a0"/>
<circle cx="0" cy="-168" r="17" fill="#efc9a0"/>
<path d="M-15 -164Q-17 -146 0 -142Q17 -146 15 -164Q8 -154 0 -154Q-8 -154 -15 -164Z" fill="#b9824a"/>
<path d="M-18 -170Q-18 -190 0 -190Q18 -190 18 -170Q10 -178 0 -177Q-10 -178 -18 -170Z" fill="#8a5a2b"/>
<circle cx="-6" cy="-168" r="1.8" fill="#2a1a0a"/><circle cx="6" cy="-168" r="1.8" fill="#2a1a0a"/>
<path d="M-4 -162Q0 -160 4 -162" stroke="#a5683e" fill="none" stroke-width="1.3" stroke-linecap="round"/>
<g>{a_rotate(arm, 24, -142)}
<rect x="24" y="-147" width="28" height="10" rx="5" fill="#c9ab78"/>
<circle cx="54" cy="-142" r="6" fill="#efc9a0"/>
<rect x="52" y="-145" width="16" height="6" rx="1.5" fill="#9aa3b2"/><rect x="58" y="-145" width="2" height="6" fill="#4a5160"/>
{blade(68, -142, 5.5, 88, "#5ab8ff", "#e6f4ff")}
</g>"""


def body_vader(arm):
    return f"""<path d="M-40 -144L-66 0L66 0L40 -144Z" fill="#0a0a10"><animate attributeName="d" values="M-40 -144L-66 0L66 0L40 -144Z;M-40 -144L-62 0L70 0L40 -144Z;M-40 -144L-66 0L66 0L40 -144Z" dur="3.8s" repeatCount="indefinite"/></path>
<rect x="-20" y="-40" width="17" height="40" rx="5" fill="#101018"/><rect x="3" y="-40" width="17" height="40" rx="5" fill="#101018"/>
<rect x="-36" y="-146" width="72" height="76" rx="12" fill="#15151c"/>
<rect x="-17" y="-126" width="34" height="26" rx="3" fill="#262633" stroke="#3a3a4a"/>
<circle cx="-9" cy="-118" r="3" fill="#ff3b3b"><animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/></circle>
<circle cx="0" cy="-118" r="3" fill="#4bd5ee"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.7s" repeatCount="indefinite"/></circle>
<circle cx="9" cy="-118" r="3" fill="#4cff4c"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
<rect x="-12" y="-110" width="24" height="4" rx="1" fill="#5a5a6e"/>
<rect x="-36" y="-76" width="72" height="10" fill="#2a2a35"/><rect x="-7" y="-75" width="14" height="8" rx="2" fill="#aeb6c4"/>
<rect x="39" y="-140" width="16" height="62" rx="8" fill="#101018"/>
<path d="M-27 -162C-33 -204 -15 -220 0 -220C15 -220 33 -204 27 -162L17 -148L-17 -148Z" fill="#0d0d13"/>
<path d="M-23 -168L-36 -144L36 -144L23 -168Z" fill="#12121a"/>
<ellipse cx="-8" cy="-206" rx="9" ry="14" fill="#fff" opacity="0.07"/>
<ellipse cx="-11" cy="-184" rx="8" ry="6" fill="#1b1b24" stroke="#3b3b4b" stroke-width="1.5" transform="rotate(12 -11 -184)"/>
<ellipse cx="11" cy="-184" rx="8" ry="6" fill="#1b1b24" stroke="#3b3b4b" stroke-width="1.5" transform="rotate(-12 11 -184)"/>
<path d="M-3.5 -176L0 -168L3.5 -176Z" fill="#2c2c38"/>
<rect x="-10" y="-164" width="20" height="12" rx="2" fill="#2c2c38"/>
<path d="M-6 -163V-153M-2 -163V-153M2 -163V-153M6 -163V-153" stroke="#555566" stroke-width="1.2"/>
<path d="M-20 -154L-24 -146M20 -154L24 -146" stroke="#333342" stroke-width="2"/>
<g>{a_rotate(arm, -44, -136)}
<rect x="-74" y="-141" width="30" height="10" rx="5" fill="#101018" stroke="#1c1c28"/>
<circle cx="-76" cy="-136" r="5.5" fill="#0c0c12" stroke="#1c1c28"/>
<rect x="-94" y="-139" width="16" height="6" rx="1.5" fill="#9aa3b2"/><rect x="-88" y="-139" width="2" height="6" fill="#4a5160"/>
{blade(-94, -136, 5.5, 100, "#ff2a2a", "#ffe3e3", direction=-1)}
</g>"""


def body_yoda(arm):
    skin, skin_d, robe, robe_d = "#9bc376", "#6f9a50", "#c8a96e", "#8b6b43"
    return f"""<ellipse cx="-9" cy="-3" rx="8" ry="4" fill="{skin}"/><ellipse cx="9" cy="-3" rx="8" ry="4" fill="{skin}"/>
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
<path d="M-5 -58Q0 -55.5 5 -58" stroke="{skin_d}" fill="none" stroke-width="1.4" stroke-linecap="round"/>
<g>{a_rotate(arm, 12, -46)}
<rect x="12" y="-50" width="26" height="8" rx="4" fill="{robe}"/>
<circle cx="40" cy="-46" r="4.5" fill="{skin}"/>
<rect x="36" y="-49" width="16" height="6" rx="1.5" fill="#9aa3b2"/><rect x="42" y="-49" width="2" height="6" fill="#4a5160"/>
{blade(52, -46, 5, 60, "#4cff4c", "#e6ffe6")}
</g>"""


def body_emperor(arm, arm2):
    robe, robe_d, pale = "#0f0f17", "#1d1d2b", "#c3be9c"
    return f"""<path d="M-30 -148C-56 -96 -74 -34 -78 -2L78 -2C74 -34 56 -96 30 -148Z" fill="{robe}"/>
<path d="M-10 -140C-14 -90 -18 -40 -20 -2M14 -140C18 -90 22 -40 26 -2M-40 -100C-46 -60 -54 -30 -58 -2" stroke="{robe_d}" stroke-width="3" fill="none"/>
<g>{a_rotate(arm, -24, -130)}
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
<path d="M-12 -135Q-5 -131.5 3 -136" stroke="#5a5540" fill="none" stroke-width="1.6" stroke-linecap="round"/>
<path d="M-14 -146L-9 -148M0 -146L5 -148M-10 -139L-14 -138M2 -139L6 -138" stroke="#8d8868" stroke-width="1"/>
<path d="M-14 -128L0 -112L14 -128Z" fill="#17171f"/>
<g>{a_rotate(arm2, -16, -124)}
<rect x="-46" y="-129" width="30" height="10" rx="5" fill="{robe}" stroke="{robe_d}"/>
<circle cx="-48" cy="-124" r="5.5" fill="{pale}"/>
<path d="M-52 -128L-58 -131M-53 -124L-60 -125M-52 -120L-58 -118" stroke="{pale}" stroke-width="2" stroke-linecap="round"/>
</g>"""


# ====================================================================== efeitos
def spark(c, t0, big=1.0):
    x, y = c
    rays = "".join(
        f'<line x1="0" y1="0" x2="{30 * math.cos(math.radians(a)):.1f}" y2="{30 * math.sin(math.radians(a)):.1f}" stroke="#fff6c2" stroke-width="2" stroke-linecap="round"/>'
        for a in range(0, 360, 40)
    )
    op = [(t0 - 0.06, 0), (t0, 1), (t0 + 0.34, 0)]
    sc = [(t0 - 0.06, 0.1), (t0, 1.5 * big), (t0 + 0.34, 0.4)]
    ring_op = [(t0 - 0.02, 0), (t0, 0.9), (t0 + 0.45, 0)]
    ring_sc = [(t0 - 0.02, 0.15), (t0 + 0.45, 1.5 * big + 0.6)]
    streak_op = [(t0 - 0.04, 0), (t0, 0.85 * min(big, 1.4)), (t0 + 0.3, 0)]
    return (
        f'<g transform="translate({_f(x)} {_f(y)})">'
        f'<g opacity="0">{a_opacity(streak_op)}<ellipse rx="{_f(70 * big + 40)}" ry="2.6" fill="url(#streak)"/></g>'
        f'<g opacity="0">{a_opacity(op)}<g>{a_scale(sc)}<circle r="20" fill="url(#spark)"/>{rays}</g></g>'
        f'<g opacity="0">{a_opacity(ring_op)}<g>{a_scale(ring_sc)}<circle r="32" fill="none" stroke="#fff6c2" stroke-width="2.5"/></g></g>'
        f"</g>"
    )


def dust(x, t0):
    op = [(t0 - 0.02, 0), (t0, 0.75), (t0 + 0.55, 0)]
    sc = [(t0 - 0.02, 0.3), (t0 + 0.55, 2.2)]
    drift_l = [(t0, 0, 0), (t0 + 0.55, -26, -6)]
    drift_r = [(t0, 0, 0), (t0 + 0.55, 26, -6)]
    return (
        f'<g transform="translate({_f(x)} {GROUND + 2})" opacity="0">{a_opacity(op)}'
        f'<g>{a_translate(drift_l)}<g>{a_scale(sc)}<ellipse rx="14" ry="4" fill="#cdbd9a"/></g></g>'
        f'<g>{a_translate(drift_r)}<g>{a_scale(sc)}<ellipse rx="14" ry="4" fill="#cdbd9a"/></g></g></g>'
    )


def swoosh(f, t, t_prev):
    """Rastro do sabre: arco em volta do ombro, da posicao de preparo ate o ponto do choque."""
    p = f.pivot_w(t)
    th0, th1 = f.theta_at(t_prev), f.theta_at(t)
    def world(th, tt):
        return th if f.f(tt) > 0 else 180 - th
    a0, a1 = world(th0, t_prev), world(th1, t)
    while a1 - a0 > 180:
        a1 -= 360
    while a1 - a0 < -180:
        a1 += 360
    r = f.sc * (f.r0 + f.r1) / 2 * 1.05
    pts = [(p[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / 9)), p[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / 9))) for k in range(10)]
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    op = [(t - 0.34, 0), (t - 0.12, 0.65), (t + 0.04, 0)]
    return f'<path d="{d}" fill="none" stroke="{f.color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0" filter="url(#bl)">{a_opacity(op)}</path>'


def shock(c, t0, color="#bfe8ff", r=130):
    x, y = c
    out = []
    for k, (dt, w) in enumerate(((0.0, 3.5), (0.14, 2.2), (0.28, 1.4))):
        op = [(t0 + dt - 0.02, 0), (t0 + dt, 0.9), (t0 + dt + 0.55, 0)]
        sc = [(t0 + dt - 0.02, 0.1), (t0 + dt + 0.55, 1.0)]
        out.append(f'<g opacity="0">{a_opacity(op)}<g>{a_scale(sc)}<circle r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/></g></g>')
    return f'<g transform="translate({_f(x)} {_f(y)})">{"".join(out)}</g>'


def bolt_points(p0, p1, rng, n=9, amp=9.0):
    pts = [p0]
    for i in range(1, n):
        t = i / n
        pts.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t + rng.uniform(-amp, amp)))
    pts.append(p1)
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def lightning(p0, targets, t0, t1, rng):
    parts = []
    for p1, w in targets:
        ds = [bolt_points(p0, p1, rng) for _ in range(4)]
        anim = f'<animate attributeName="d" values="{";".join(ds + [ds[0]])}" keyTimes="0;0.25;0.5;0.75;1" dur="0.24s" repeatCount="indefinite" calcMode="discrete"/>'
        parts.append(f'<path d="{ds[0]}" fill="none" stroke="#3fa8ff" stroke-width="{w * 3}" stroke-linejoin="round" opacity="0.55" filter="url(#bl)">{anim}</path>')
        parts.append(f'<path d="{ds[0]}" fill="none" stroke="#e6f9ff" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round">{anim}</path>')
    return f'<g opacity="0">{a_opacity([(t0 - 0.05, 0), (t0, 1), (t1, 1), (t1 + 0.05, 0)])}{"".join(parts)}</g>'


def flicker(c, t0, t1):
    frames, t, on = [(t0 - 0.05, 0)], t0, 1
    while t < t1:
        frames.append((t, 1 if on else 0.25))
        on ^= 1
        t += 0.09
    frames.append((t1, 0))
    return f'<g transform="translate({_f(c[0])} {_f(c[1])})"><g opacity="0">{a_opacity(frames)}<circle r="14" fill="url(#spark)"/></g></g>'


# ====================================================================== coreografia
def build_fighters():
    # ---------------- duelo A: Obi-Wan (azul) x Vader (vermelho)
    obi = Fighter(
        "Obi-Wan", 120, 1.0, +1, (24, -142), (44, 132), -90, "#5ab8ff",
        pos=[(0, 120, 0), (0.8, 120, 0), (1.2, 130, 0), (1.4, 130, 0), (1.65, 95, -75), (2.0, 60, 0), (2.5, 60, 0),
             (2.8, 130, -60), (3.1, 240, -72), (3.4, 330, -60), (3.75, 400, 0), (4.3, 400, 0), (5.0, 400, 0),
             (5.35, 415, -60), (5.7, 410, 0), (7.3, 410, 0), (7.6, 395, -45), (8.0, 300, -72), (8.35, 200, -55),
             (8.7, 120, 0), (9.4, 120, 0), (10.0, 150, 0), (10.4, 135, 0), (10.7, 150, -30), (11.0, 175, -70),
             (11.4, 140, -10), (11.7, 125, 0), (12.0, 120, 0)],
        face=[(0, 1), (3.35, -1), (8.1, 1)],
        flip=[(0, 0), (1.4, 0), (1.95, -360), (2.7, -360), (3.05, 0), (5.05, 0), (5.65, 360), (7.55, 360), (8.0, 0),
              (10.5, 0), (10.9, 360)],
    )
    vader = Fighter(
        "Vader", 330, 0.9, -1, (-44, -136), (50, 150), -90, "#ff4a4a",
        pos=[(0, 330, 0), (0.8, 330, 0), (1.2, 300, 0), (1.5, 300, 0), (2.0, 250, 0), (2.35, 230, 0), (3.0, 230, 0),
             (3.8, 232, 0), (4.3, 240, 0), (5.4, 240, 0), (5.9, 250, 0), (6.1, 255, -60), (6.5, 262, -70),
             (6.9, 285, 0), (7.4, 300, 0), (8.5, 320, 0), (9.0, 330, 0), (10.0, 320, 0), (10.4, 310, 0),
             (11.0, 330, 0), (12.0, 330, 0)],
        face=[(0, -1), (3.4, 1), (8.1, -1)],
        flip=[(0, 0), (5.9, 0), (6.3, 360)],
    )
    # ---------------- duelo B: Yoda (verde) x Imperador (vermelho)
    yoda = Fighter(
        "Yoda", 590, 1.0, +1, (12, -46), (40, 98), -45, "#4cff4c",
        pos=[(0, 590, 0), (0.75, 590, 0), (1.0, 610, -60), (1.2, 628, -85), (1.35, 635, -80), (1.65, 645, -25),
             (1.85, 655, 0), (2.8, 665, 0), (3.1, 690, 0), (4.7, 690, 0), (5.0, 720, 0), (5.5, 725, 0), (5.9, 715, 0),
             (6.2, 715, -40), (6.65, 700, -100), (7.05, 690, -85), (7.4, 690, 0), (8.0, 700, 0), (8.9, 690, 0),
             (9.0, 680, -10), (9.3, 640, -60), (9.65, 590, 0), (10.3, 605, 0), (10.6, 590, 0), (10.9, 600, -30),
             (11.1, 615, -60), (11.5, 595, 0), (12.0, 590, 0)],
        face=[(0, 1), (2.7, -1), (8.95, 1)],
        flip=[(0, 0), (0.85, 0), (1.25, 360), (6.25, 360), (6.95, -360), (9.0, -360), (9.55, -720)],
    )
    emp = Fighter(
        "Imperador", 770, 1.0, -1, (-24, -130), (44, 114), -85, "#ff4a4a",
        pos=[(0, 770, 0), (1.5, 770, 0), (1.75, 760, 0), (2.0, 700, -55), (2.35, 640, -72), (2.65, 590, -50),
             (2.95, 560, 0), (7.5, 560, 0), (7.8, 610, -55), (8.2, 700, -72), (8.6, 770, -45), (8.9, 785, 0),
             (9.3, 780, 0), (10.0, 770, 0), (10.3, 750, 0), (10.6, 765, 0), (11.1, 770, 0), (12.0, 770, 0)],
        face=[(0, -1), (2.55, 1), (8.7, -1)],
        flip=[(0, 0), (1.75, 0), (2.4, -360), (7.7, -360), (8.4, 0)],
        pivot2=(-16, -124),
    )
    return obi, vader, yoda, emp


def choreograph(obi, vader, yoda, emp, rng):
    # braços (theta: angulo relativo a frente, negativo = para cima)
    obi.specs += [(0, -40), (0.5, -85), (1.5, -40), (2.0, -75), (2.8, -30), (3.6, -10), (4.9, -40), (5.2, -70),
                  (5.7, -30), (6.2, -80), (6.9, -40), (7.3, -60), (7.9, -85), (9.0, -40), (10.6, -45), (11.5, -40), (12, -40)]
    vader.specs += [(0, -35), (0.6, -70), (1.5, -35), (1.9, -75), (2.8, -35), (3.6, -30), (4.8, -40), (5.0, -5),
                    (5.4, -35), (6.0, -80), (6.9, -35), (7.8, -35), (9.0, -35), (10.6, -40), (11.5, -35), (12, -35)]
    yoda.specs += [(0, -25), (0.7, -60), (1.7, -10), (2.4, -25), (3.0, -70), (3.5, -35), (3.7, -80), (3.95, -85),
                   (4.2, -75), (4.5, -82), (4.75, -78), (5.0, -40), (6.0, -60), (6.6, -85), (7.5, -25), (9.0, -25),
                   (9.9, -60), (10.6, -30), (10.9, -70), (11.5, -25), (12, -25)]
    emp.specs += [(0, 35), (0.9, 10), (1.7, 35), (2.5, 35), (2.9, 0), (3.5, 60), (4.9, 60), (5.5, 35), (6.5, 10),
                  (7.5, 35), (9.6, 35), (10.6, 35), (11.5, 35), (12, 35)]

    # choques do duelo A
    ca = [(1.2, 1.0), (2.35, 1.0), (4.3, 1.3), (6.5, 1.5), (9.4, 1.0), (10.2, 1.0), (11.0, 1.3)]
    for t, big in ca:
        clash(t, obi, vader, big)
    # choques do duelo B
    cb = [(1.35, 1.3), (3.1, 1.0), (7.05, 1.5), (10.3, 1.0), (11.1, 1.2)]
    for t, big in cb:
        clash(t, yoda, emp, big)

    # raio do Imperador (3.8 a 4.85): mao -> ponta do sabre do Yoda erguido
    t_l = 4.0
    yp = yoda.pivot_w(t_l)
    phi = math.radians(180 - (-80))  # Yoda olhando para a esquerda, sabre erguido
    tip = (yp[0] + 98 * math.cos(phi), yp[1] + 98 * math.sin(phi))
    th2 = emp.theta_to(t_l, tip, which=2)
    emp.specs2 += [(0, 90), (3.55, 90), (3.8, th2), (4.0, th2 + 3), (4.2, th2 - 3), (4.4, th2 + 3), (4.6, th2 - 2), (4.8, th2), (5.0, 90), (12, 90)]
    fp = emp.pivot_w(t_l, which=2)
    hand = (fp[0] + 32 * math.cos(math.atan2(tip[1] - fp[1], tip[0] - fp[0])), fp[1] + 32 * math.sin(math.atan2(tip[1] - fp[1], tip[0] - fp[0])))
    body_t = (yoda.x(t_l) - 6, GROUND - 52)
    bolts = lightning(hand, [(tip, 2.6), (body_t, 1.8)], 3.8, 4.85, rng)
    tip_flicker = flicker(tip, 3.8, 4.85)

    for f in (obi, vader, yoda, emp):
        f.resolve()

    # poeira nos pousos
    for x, t in [(1.85 * 0 + 655, 1.85), (560, 2.95), (400, 3.75), (410, 5.7), (285, 6.9), (120, 8.7), (785, 8.9),
                 (590, 9.65), (125, 11.7), (595, 11.5), (232, 3.8), (330, 9.0)]:
        DUSTS.append(dust(x, t))
    # rastros dos sabres antes de cada choque
    for t, _ in ca:
        SWOOSH.append(swoosh(obi, t, t - 0.4))
        SWOOSH.append(swoosh(vader, t, t - 0.4))
    for t, _ in cb:
        SWOOSH.append(swoosh(yoda, t, t - 0.4))
        SWOOSH.append(swoosh(emp, t, t - 0.4))
    # Forca de Vader em 5.0 empurra o Obi-Wan
    vp = vader.pivot_w(5.0)
    SHOCK.append(shock((vp[0] + 30, vp[1] + 4), 5.0))
    return bolts, tip_flicker


def shake_frames(extra):
    frames = [(0, 0, 0)]
    for t, big in extra:
        a = 3 * big
        frames += [(t - 0.02, 0, 0), (t, a, -a * 0.6), (t + 0.05, -a, a * 0.6), (t + 0.1, a * 0.6, -a * 0.3), (t + 0.16, 0, 0)]
    return sorted(frames, key=lambda f: f[0])


def flash_frames(events):
    frames = [(0, 0)]
    for t, v in events:
        frames += [(t - 0.04, 0), (t, v), (t + 0.14, 0)]
    return sorted(frames, key=lambda f: f[0])


def label(cx, text, color):
    return text_path(GOTHIC, text, 15, 3, cx, 322, color, "middle")


def build():
    rng = random.Random(21)
    names = T["duel_names"]
    IMPACTS.clear(), DUSTS.clear(), SWOOSH.clear(), SHOCK.clear()
    obi, vader, yoda, emp = build_fighters()
    bolts, tip_flicker = choreograph(obi, vader, yoda, emp, rng)

    bodies = [
        obi.render(body_obi(obi.alpha)),
        vader.render(body_vader(vader.alpha)),
        yoda.render(body_yoda(yoda.alpha)),
        emp.render(body_emperor(emp.alpha, emp.alpha2)),
    ]
    sparks = "".join(spark(c, t, big) for t, c, big in IMPACTS)
    big_hits = [(t, big) for t, c, big in IMPACTS if big >= 1.3] + [(5.0, 1.5), (3.8, 0.6)]
    flashes = [(t, 0.10 + 0.06 * big) for t, c, big in IMPACTS if big >= 1.3] + [(5.0, 0.2), (3.8, 0.1)]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{T["alt_duel"]}">
<title>{T["alt_duel"]}</title>
<defs>
<filter id="bl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.5"/></filter>
<radialGradient id="spark"><stop offset="0" stop-color="#fff"/><stop offset="0.4" stop-color="#ffe81f"/><stop offset="1" stop-color="#ffe81f" stop-opacity="0"/></radialGradient>
<linearGradient id="streak" x1="0" x2="1"><stop offset="0" stop-color="#9fd8ff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#9fd8ff" stop-opacity="0"/></linearGradient>
<linearGradient id="bgD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050c"/><stop offset="1" stop-color="#101a3a"/></linearGradient>
<linearGradient id="floorD" x1="0" x2="1"><stop offset="0" stop-color="#4bd5ee" stop-opacity="0"/><stop offset="0.5" stop-color="#ffe81f" stop-opacity="0.45"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></linearGradient>
<linearGradient id="shoot" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
<radialGradient id="glowL"><stop offset="0" stop-color="#4bd5ee" stop-opacity="0.22"/><stop offset="1" stop-color="#4bd5ee" stop-opacity="0"/></radialGradient>
<radialGradient id="glowR"><stop offset="0" stop-color="#ff2a2a" stop-opacity="0.22"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.6"/></radialGradient>
<clipPath id="cpD"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#cpD)">
<rect width="{W}" height="{H}" fill="url(#bgD)"/>
<g>{a_translate(shake_frames(big_hits))}
<ellipse cx="150" cy="262" rx="150" ry="85" fill="url(#glowL)"/><ellipse cx="320" cy="262" rx="150" ry="85" fill="url(#glowR)"/>
<ellipse cx="610" cy="262" rx="150" ry="85" fill="url(#glowL)"/><ellipse cx="770" cy="262" rx="150" ry="85" fill="url(#glowR)"/>
{starfield(rng, 90)}
<rect x="0" y="{GROUND + 1}" width="{W}" height="2" fill="url(#floorD)"/>
<line x1="470" y1="70" x2="470" y2="{GROUND}" stroke="#2a3a6b" stroke-opacity="0.4" stroke-dasharray="3 7"/>
{"".join(bodies)}
{"".join(SWOOSH)}
{"".join(DUSTS)}
{bolts}
{tip_flicker}
{"".join(SHOCK)}
{sparks}
{label(120, names["obi"], "#4BD5EE")}
{label(330, names["vader"], "#FF6B6B")}
{label(590, names["yoda"], "#8FE08A")}
{label(770, names["emp"], "#FF5A5A")}
</g>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<rect width="{W}" height="{H}" fill="#fff" opacity="0">{a_opacity(flash_frames(flashes))}</rect>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{YELLOW}" stroke-opacity="0.45"/>
</svg>
"""
    (OUT / "duelo.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build()
    print("duelo.svg", (OUT / "duelo.svg").stat().st_size // 1024, "KB")
