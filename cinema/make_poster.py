"""Gera o poster do filme (assets/duelo3d-poster.jpg): um quadro do filme com botao de play e texto.

Uso: python cinema/make_poster.py [--frame-seconds 14]
O README mostra este poster leve; ao clicar, abre o WebP animado (assets/duelo3d.webp).
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from texts import T  # noqa: E402

FONTS = ROOT / "fonts"
YELLOW = (255, 232, 31)


def font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.truetype(str(FONTS / "NewsCycle-Bold.woff"), size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame-seconds", type=float, default=14.0)
    ap.add_argument("--fps", type=int, default=12)
    a = ap.parse_args()

    movie = Image.open(ROOT / "assets" / "duelo3d.webp")
    movie.seek(min(movie.n_frames - 1, int(a.frame_seconds * a.fps)))
    img = ImageEnhance.Brightness(movie.convert("RGB")).enhance(0.62)
    w, h = img.size
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    cx, cy, r = w // 2, h // 2 - 22, 46
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(5, 8, 20, 190), outline=YELLOW + (255,), width=4)
    d.polygon([(cx - 14, cy - 24), (cx - 14, cy + 24), (cx + 26, cy)], fill=YELLOW + (255,))
    title = T["poster_title"]
    sub = T["poster_sub"]
    ft = font(FONTS / "SFDistantGalaxy.ttf", 30)
    fs = font(FONTS / "NewsCycle-Bold.woff", 17)
    tw = d.textlength(title, font=ft)
    d.text(((w - tw) / 2, cy + r + 16), title, font=ft, fill=YELLOW + (255,))
    sw = d.textlength(sub, font=fs)
    d.text(((w - sw) / 2, cy + r + 58), sub, font=fs, fill=(207, 216, 255, 255))
    out = Image.alpha_composite(img.convert("RGBA"), over).convert("RGB")
    dest = ROOT / "assets" / "duelo3d-poster.jpg"
    out.save(dest, quality=88, optimize=True)
    print(f"{dest.name}: {dest.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
