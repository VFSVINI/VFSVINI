"""Camada de dados dos cards: consulta a API GraphQL do GitHub e calcula XP e patente.

Os SVGs sao montados em gen_cards.py.
"""
import json
import math
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from texts import T

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


# Escada de poder, do mais fraco ao mais poderoso, intercalando os dois lados da Forca.
# (xp minimo, patente, personagem, lado)
RANKS = [
    (0, "PADAWAN", "AHSOKA TANO", "light"),
    (900, "JEDI KNIGHT", "OBI-WAN KENOBI", "light"),
    (1800, "SITH APPRENTICE", "DARTH MAUL", "dark"),
    (3200, "JEDI MASTER", "LUKE SKYWALKER", "light"),
    (5500, "SITH COUNT", "DARTH TYRANUS", "dark"),
    (8000, "COUNCIL MASTER", "MACE WINDU", "light"),
    (11000, "SITH LORD", "DARTH VADER", "dark"),
    (15000, "SITH EMPEROR", "DARTH SIDIOUS", "dark"),
    (22000, "GRAND MASTER", "YODA", "light"),
]


RANKS = [(m, T["ranks"][i], c, s) for i, (m, _, c, s) in enumerate(RANKS)]


def xp_of(d):
    """XP = commits + 5*PRs + 3*issues + 2*reviews + 10*estrelas + 2*repositorios.

    Atualizado a cada 12h pelo workflow. A formula nao aparece no perfil de proposito.
    """
    return d["commits"] + 5 * d["prs"] + 3 * d["issues"] + 2 * d["reviews"] + 10 * d["stars"] + 2 * d["repos"]


def rank_of(xp):
    """Devolve (indice, patente, xp da proxima, patente da proxima, progresso 0..1)."""
    idx = max(i for i, r in enumerate(RANKS) if xp >= r[0])
    cur_min, name = RANKS[idx][0], RANKS[idx][1]
    if idx + 1 < len(RANKS):
        nxt_min, nxt_name = RANKS[idx + 1][0], RANKS[idx + 1][1]
    else:
        nxt_min, nxt_name = cur_min, name
    prog = 1.0 if nxt_min == cur_min else (xp - cur_min) / (nxt_min - cur_min)
    return idx, name, nxt_min, nxt_name, prog
