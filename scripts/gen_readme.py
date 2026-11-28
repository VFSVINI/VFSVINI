"""Gera o README.md a partir de texts.py (idioma pela variavel PROFILE_LANG)."""
from pathlib import Path

from texts import T

RAW = "https://raw.githubusercontent.com/VFSVINI/VFSVINI/output"


def heading(slug):
    return f'<h2 align="center"><img src="assets/h-{slug}.svg" alt="{T["h_" + slug].title()}" width="100%"/></h2>'


DIV = '<div align="center">\n<img src="assets/divider.svg" alt="" width="100%"/>\n</div>'


def build():
    readme = f"""<div align="center">

<img src="assets/crawl.svg" alt="{T["alt_crawl"]}" width="100%"/>

<br/>

<a href="https://github.com/VFSVINI?tab=followers"><img alt="{T["alt_followers"]}" src="{RAW}/badge-followers.svg"/></a>
<a href="https://github.com/VFSVINI?tab=repositories"><img alt="{T["alt_squadron"]}" src="{RAW}/badge-squadron.svg"/></a>
<a href="https://github.com/VFSVINI/meridian-wealth"><img alt="{T["alt_mission"]}" src="{RAW}/badge-mission.svg"/></a>

<img src="assets/divider.svg" alt="" width="100%"/>

</div>

{heading("transmission")}

<p align="center">
  <img src="assets/transmission.svg" alt="{T["alt_transmission"]}" width="100%"/>
</p>

{DIV}

{heading("duel")}

<p align="center">
  <img src="assets/duelo.svg" alt="{T["alt_duel"]}" width="100%"/>
</p>

{DIV}

{heading("film")}

<p align="center">
  <a href="https://github.com/VFSVINI/VFSVINI/blob/main/assets/duelo3d.webp"><img src="assets/duelo3d-poster.jpg" alt="{T["alt_film"]}" width="100%"/></a>
</p>

{DIV}

{heading("arsenal")}

<p align="center">
  <img src="assets/arsenal.svg" alt="{T["alt_arsenal"]}" width="100%"/>
</p>

{DIV}

{heading("dossier")}

<p align="center">
  <img alt="{T["alt_rank"]}" src="{RAW}/rank.svg" width="49%"/>
  <img alt="{T["alt_galaxy"]}" src="{RAW}/galaxy.svg" width="49%"/>
</p>

<p align="center">
  <img alt="{T["alt_ladder"]}" src="{RAW}/ladder.svg" width="100%"/>
</p>

{DIV}

{heading("missions")}

<p align="center">
  <a href="https://github.com/VFSVINI/meridian-wealth"><img alt="meridian-wealth" src="{RAW}/mission-1.svg" width="49%"/></a>
  <a href="https://github.com/VFSVINI/FleetTrack-Realtime"><img alt="FleetTrack-Realtime" src="{RAW}/mission-2.svg" width="49%"/></a>
  <a href="https://github.com/VFSVINI/Vortex-Engine"><img alt="Vortex-Engine" src="{RAW}/mission-3.svg" width="49%"/></a>
  <a href="https://github.com/VFSVINI/heloc-streamlit"><img alt="heloc-streamlit" src="{RAW}/mission-4.svg" width="49%"/></a>
</p>

{DIV}

{heading("snake")}

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{RAW}/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="{RAW}/github-snake.svg" />
  <img alt="{T["alt_snake"]}" src="{RAW}/github-snake-dark.svg" />
</picture>
</p>

<div align="center">

<img src="assets/divider.svg" alt="" width="100%"/>

<img src="{RAW}/quotes.svg" alt="{T["alt_quotes"]}" width="100%"/>

<br/><br/>

<img src="assets/footer.svg" alt="{T["alt_footer"]}" width="100%"/>

</div>
"""
    Path(__file__).resolve().parent.parent.joinpath("README.md").write_text(readme, encoding="utf-8")
    print("README.md gerado")


if __name__ == "__main__":
    build()
