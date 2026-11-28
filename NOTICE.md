# Avisos e documentação (não aparece no perfil)

Este repositório é o README do perfil. Os detalhes abaixo ficam aqui, fora do visual.

## Projeto de fã
Projeto de fã de Star Wars, sem vínculo com a Lucasfilm/Disney. Os personagens pertencem aos
seus donos. As frases do carrossel são **originais**, escritas no estilo da saga, e não são falas
dos filmes.

## Créditos
- Letras (convertidas em contorno vetorial): **SF Distant Galaxy** (ShyFonts, freeware, uso pessoal;
  nunca versionada, o workflow baixa a cada execução) e **News Cycle** (OFL, em `fonts/`).
- Ícones do Arsenal: **Simple Icons** (CC0) e **Devicon** (MIT, ícone do Java).

## Como o XP e as patentes funcionam
`XP = commits + 5 × pull requests + 3 × issues + 2 × revisões + 10 × estrelas + 2 × repositórios`
(`scripts/gen_stats.py`, função `xp_of`). A escada, do mais fraco ao mais poderoso, intercala os dois lados da Força: Grogu, Ahsoka Tano,
Obi-Wan Kenobi, Darth Maul, Luke Skywalker, Mace Windu, Darth Tyranus (Conde Dooku), Darth Vader,
Darth Sidious e, no topo, Yoda. Os cortes de XP estão em `RANKS`.

## Como gerar
- Estático (`assets/` e `README.md`): `PROFILE_LANG=pt python scripts/build_all.py`
  (precisa de `fonts/SFDistantGalaxy.ttf` e `pip install fonttools`).
- Dinâmico (ficha, escada, linguagens, selos, missões, frases e cobrinha): workflow
  `.github/workflows/snake.yml`, a cada 12 horas, publicado na branch `output`.
- Idioma: `scripts/texts.py` tem `pt` e `en`; troque `DEFAULT_LANG` (e `PROFILE_LANG` no workflow).
