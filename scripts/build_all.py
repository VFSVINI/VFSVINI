"""Regenera tudo que e estatico (assets/ e README.md) no idioma de PROFILE_LANG.

Uso local (precisa de fonts/SFDistantGalaxy.ttf e fonts/NewsCycle-Bold.woff):
    PROFILE_LANG=pt python scripts/build_all.py
Os cards dinamicos (ficha, escada, linguagens, selos, missoes, frases e cobrinha) sao gerados
pelo workflow na branch output; para trocar o idioma deles, mude DEFAULT_LANG em texts.py.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["gen_static.py", "gen_characters.py", "gen_arsenal.py", "gen_transmission.py", "gen_headings.py", "gen_readme.py"]

if __name__ == "__main__":
    for step in STEPS:
        print(f"== {step}")
        subprocess.run([sys.executable, str(HERE / step)], check=True)
