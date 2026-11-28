"""Frases em portugues: vem do Compendio Galactico Definitivo (PDF do dono do perfil).

Arquivo de dados: quotes_pt.txt, uma frase por linha no formato  texto<TAB>autor.
Fica de fora a secao de falas classicas da dublagem (dialogo dos filmes, protegido).
Para acrescentar frases, basta adicionar linhas ao arquivo.
"""
from pathlib import Path

DATA = Path(__file__).resolve().parent / "quotes_pt.txt"


def quotes():
    out = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        text, who = line.split("\t", 1)
        out.append((text.strip(), who.strip().upper()))
    return out


if __name__ == "__main__":
    qs = quotes()
    print(len(qs), "frases;", "autores:", len({w for _, w in qs}), "maior:", max(len(t) for t, _ in qs), "caracteres")
