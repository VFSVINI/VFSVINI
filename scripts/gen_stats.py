"""Gera os cards gamificados (Ficha do Jedi e Sistema de Linguagens) a partir da API do GitHub.

Uso: GITHUB_TOKEN=... GITHUB_USER=VFSVINI python scripts/gen_stats.py [pasta_saida]
Sem JavaScript: tudo e SMIL/CSS dentro de SVG, que o GitHub renderiza via <img>.
"""
import json
import math
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USER = os.environ.get("GITHUB_USER", "VFSVINI")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
OUT.mkdir(parents=True, exist_ok=True)

FONT = "'Franklin Gothic Medium','Arial Narrow','Segoe UI',Arial,sans-serif"
YELLOW, BLUE, GREEN = "#FFE81F", "#4BD5EE", "#4CFF4C"


def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


BASE = """
query($u:String!){ user(login:$u){
  name createdAt
  followers{totalCount}
  pullRequests{totalCount}
  issues{totalCount}
  repositories(ownerAffiliations:OWNER,isFork:false,first:100){
    totalCount
    nodes{ stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}} }
  }
}}"""

YEAR = """
query($u:String!,$f:DateTime!,$t:DateTime!){ user(login:$u){
  contributionsCollection(from:$f,to:$t){
    totalCommitContributions totalPullRequestReviewContributions
  }
}}"""


def collect():
    u = gql(BASE, u=USER)["user"]
    created = datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    commits = reviews = 0
    y = created.year
    while y <= now.year:
        f = max(created, datetime(y, 1, 1, tzinfo=timezone.utc))
        t = min(now, datetime(y, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
        c = gql(YEAR, u=USER, f=f.isoformat(), t=t.isoformat())["user"]["contributionsCollection"]
        commits += c["totalCommitContributions"]
        reviews += c["totalPullRequestReviewContributions"]
        y += 1
    repos = u["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]
            cur = langs.setdefault(n["name"], {"size": 0, "color": n["color"] or "#8b949e"})
            cur["size"] += e["size"]
    return {
        "name": u["name"] or USER,
        "commits": commits,
        "prs": u["pullRequests"]["totalCount"],
        "issues": u["issues"]["totalCount"],
        "reviews": reviews,
        "stars": stars,
        "repos": u["repositories"]["totalCount"],
        "followers": u["followers"]["totalCount"],
        "langs": sorted(langs.items(), key=lambda kv: -kv[1]["size"]),
    }


# (xp minimo, patente)
RANKS = [
    (0, "YOUNGLING"),
    (300, "PADAWAN"),
    (900, "JEDI KNIGHT"),
    (2000, "JEDI MASTER"),
    (4500, "COUNCIL MASTER"),
    (9000, "GRAND MASTER"),
]


def xp_of(d):
    return d["commits"] + 5 * d["prs"] + 3 * d["issues"] + 2 * d["reviews"] + 10 * d["stars"] + 2 * d["repos"]


def rank_of(xp):
    idx = max(i for i, (m, _) in enumerate(RANKS) if xp >= m)
    cur_min, name = RANKS[idx]
    if idx + 1 < len(RANKS):
        nxt_min = RANKS[idx + 1][0]
        nxt_name = RANKS[idx + 1][1]
    else:
        nxt_min, nxt_name = cur_min, name
    prog = 1.0 if nxt_min == cur_min else (xp - cur_min) / (nxt_min - cur_min)
    return idx, name, nxt_min, nxt_name, prog


def frame(w, h, title, inner, uid):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
<linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b18"/><stop offset="1" stop-color="#0d1530"/></linearGradient>
<linearGradient id="saber{uid}" x1="0" x2="1"><stop offset="0" stop-color="#1fb81f"/><stop offset="1" stop-color="#9dff9d"/></linearGradient>
<linearGradient id="scan{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.5" stop-color="{BLUE}" stop-opacity="0.13"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<radialGradient id="sun{uid}"><stop offset="0" stop-color="#fff7b0"/><stop offset="0.5" stop-color="{YELLOW}"/><stop offset="1" stop-color="#ff9d00" stop-opacity="0"/></radialGradient>
<filter id="glow{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="clip{uid}"><rect width="{w}" height="{h}" rx="12"/></clipPath>
</defs>
<style>text{{font-family:{FONT}}}.lbl{{fill:#8ea3d6;font-size:13px;letter-spacing:1.5px}}.val{{fill:#fff;font-size:15px;font-weight:700}}.ttl{{fill:{YELLOW};font-size:14px;letter-spacing:3px;font-weight:700}}</style>
<g clip-path="url(#clip{uid})">
<rect width="{w}" height="{h}" fill="url(#bg{uid})"/>
<rect y="-60" width="{w}" height="60" fill="url(#scan{uid})"><animate attributeName="y" values="-60;{h}" dur="5s" repeatCount="indefinite"/></rect>
{inner}
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="none" stroke="{YELLOW}" stroke-opacity="0.55"/>
<path d="M10 28V10h18M{w - 28} 10h18v18M{w - 10} {h - 28}v18h-18M28 {h - 10}H10v-18" fill="none" stroke="{YELLOW}" stroke-width="2"/>
</svg>
"""


def card_rank(d):
    xp = xp_of(d)
    idx, name, nxt_min, nxt_name, prog = rank_of(xp)
    level = int(math.sqrt(xp / 10)) + 1
    w, h = 495, 232
    rows = [
        ("COMMITS", d["commits"], BLUE),
        ("PULL REQUESTS", d["prs"], GREEN),
        ("ISSUES", d["issues"], YELLOW),
        ("CODE REVIEWS", d["reviews"], "#c58cff"),
        ("STARS", d["stars"], "#ffb347"),
        ("MISSIONS (REPOS)", d["repos"], "#ff6b6b"),
    ]
    inner = [f'<text class="ttl" x="26" y="36">JEDI DOSSIER</text>',
             f'<text x="{w - 24}" y="36" text-anchor="end" fill="#6b7aa8" font-size="12" letter-spacing="2">{escape(d["name"].upper())}</text>']
    for i, (lab, val, col) in enumerate(rows):
        y = 70 + i * 22
        inner.append(
            f'<circle cx="32" cy="{y - 4}" r="3.5" fill="{col}" filter="url(#glowrank)"/>'
            f'<text class="lbl" x="46" y="{y}">{lab}</text>'
            f'<text class="val" x="262" y="{y}" text-anchor="end">{val:,}</text>'.replace(",", ".")
        )
    cx, cy, r = 386, 112, 46
    circ = 2 * math.pi * r
    off = circ * (1 - prog)
    inner.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1b2745" stroke-width="8"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="8" stroke-linecap="round" '
        f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {cx} {cy})" filter="url(#glowrank)">'
        f'<animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="{off:.1f}" dur="2.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/></circle>'
        f'<text x="{cx}" y="{cy - 8}" text-anchor="middle" fill="#8ea3d6" font-size="12" letter-spacing="3">LEVEL</text>'
        f'<text x="{cx}" y="{cy + 26}" text-anchor="middle" fill="#fff" font-size="40" font-weight="700">{level}</text>'
        f'<text x="{cx}" y="{cy + 72}" text-anchor="middle" fill="{YELLOW}" font-size="14" font-weight="700" letter-spacing="2">{name}</text>'
    )
    bw = w - 52
    fill_w = bw * prog
    if nxt_min == RANKS[idx][0]:
        label = f"XP {xp:,} · MAX LEVEL".replace(",", ".")
    else:
        label = f"XP {xp:,} / {nxt_min:,} → {nxt_name}".replace(",", ".")
    inner.append(
        f'<text x="26" y="199" fill="#8ea3d6" font-size="12" letter-spacing="1.5">{escape(label)}</text>'
        f'<rect x="26" y="206" width="{bw}" height="9" rx="4.5" fill="#1b2745"/>'
        f'<rect x="26" y="206" width="0" height="9" rx="4.5" fill="url(#saberrank)" filter="url(#glowrank)">'
        f'<animate attributeName="width" from="0" to="{fill_w:.1f}" dur="2.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/></rect>'
    )
    (OUT / "rank.svg").write_text(frame(w, h, f"Jedi dossier: {name}, level {level}, {xp} XP", "\n".join(inner), "rank"), encoding="utf-8")


def card_galaxy(d):
    langs = d["langs"][:6]
    total = sum(v["size"] for _, v in d["langs"]) or 1
    w, h = 495, 232
    cx, cy = 128, 124
    inner = [f'<text class="ttl" x="26" y="36">LANGUAGE SYSTEM</text>']
    inner.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="url(#sungalaxy)"><animate attributeName="r" values="30;36;30" dur="4s" repeatCount="indefinite"/></circle>'
                 f'<circle cx="{cx}" cy="{cy}" r="11" fill="#fff7b0"/>')
    biggest = max((v["size"] for _, v in langs), default=1)
    for i, (name, v) in enumerate(langs):
        orbit = 42 + i * 14
        share = v["size"] / total
        pr = 4.5 + 8 * (v["size"] / biggest) ** 0.5
        start = (i * 67) % 360
        dur = 9 + i * 5.5
        inner.append(
            f'<circle cx="{cx}" cy="{cy}" r="{orbit}" fill="none" stroke="#2a3a6b" stroke-width="1" stroke-dasharray="2 4"/>'
            f'<g><animateTransform attributeName="transform" type="rotate" from="{start} {cx} {cy}" to="{start + 360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<circle cx="{cx + orbit}" cy="{cy}" r="{pr:.1f}" fill="{v["color"]}" filter="url(#glowgalaxy)"><title>{escape(name)} {share * 100:.1f}%</title></circle></g>'
        )
    for i, (name, v) in enumerate(langs):
        y = 72 + i * 25
        share = v["size"] / total
        inner.append(
            f'<circle cx="290" cy="{y - 4}" r="5" fill="{v["color"]}"/>'
            f'<text class="lbl" x="304" y="{y}" style="font-size:14px">{escape(name.upper())}</text>'
            f'<text class="val" x="{w - 26}" y="{y}" text-anchor="end">{share * 100:.1f}%</text>'
            f'<rect x="290" y="{y + 6}" width="{w - 316}" height="2.5" rx="1.2" fill="#1b2745"/>'
            f'<rect x="290" y="{y + 6}" width="0" height="2.5" rx="1.2" fill="{v["color"]}"><animate attributeName="width" from="0" to="{(w - 316) * share:.1f}" dur="2s" fill="freeze"/></rect>'
        )
    (OUT / "galaxy.svg").write_text(frame(w, h, "Solar system of most used languages", "\n".join(inner), "galaxy"), encoding="utf-8")


if __name__ == "__main__":
    data = collect()
    print({k: v for k, v in data.items() if k != "langs"}, "langs:", [(n, v["size"]) for n, v in data["langs"][:6]])
    print("xp:", xp_of(data), rank_of(xp_of(data))[:4])
    card_rank(data)
    card_galaxy(data)
