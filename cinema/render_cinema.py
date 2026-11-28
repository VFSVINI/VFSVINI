"""Renderiza o filme 3D: Chrome headless desenha cada quadro (Three.js), o Python recebe os quadros,
aplica pos-processamento (bloom, vinheta, grading, fades) e monta um WebP animado.

Uso: python cinema/render_cinema.py --fps 15 --t0 0 --t1 16 --out assets/duelo3d.webp [--quality 70]
Requer Google Chrome instalado e Pillow. Nao baixa nada.
"""
import argparse
import http.server
import math
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


class Receiver(http.server.SimpleHTTPRequestHandler):
    frames_dir = None
    done = threading.Event()
    count = 0

    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(HERE), **k)

    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        if self.path.startswith("/frame/"):
            idx = int(self.path.rsplit("/", 1)[1])
            (Receiver.frames_dir / f"f{idx:05d}.jpg").write_bytes(body)
            Receiver.count = max(Receiver.count, idx + 1)
        elif self.path == "/done":
            Receiver.done.set()
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


def vignette_mask(w, h, strength=0.55):
    mask = Image.new("L", (w, h))
    px = mask.load()
    cx, cy = w / 2, h / 2
    maxd = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            d = math.hypot((x - cx) / cx, (y - cy) / cy) / math.sqrt(2)
            px[x, y] = int(255 * (1 - strength * max(0.0, d - 0.35) ** 1.6 * 2.2))
    return mask


def post(img, vig, fade):
    bright = img.point(lambda v: 0 if v < 175 else min(255, int((v - 175) * 3.2)))
    b1 = bright.filter(ImageFilter.GaussianBlur(5))
    b2 = bright.filter(ImageFilter.GaussianBlur(16))
    glow = ImageChops.add(b1.point(lambda v: int(v * 0.8)), b2.point(lambda v: int(v * 1.1)))
    out = ImageChops.screen(img, glow)
    out = ImageEnhance.Contrast(out).enhance(1.08)
    out = ImageEnhance.Color(out).enhance(1.12)
    out = ImageChops.multiply(out, Image.merge("RGB", (vig, vig, vig)))
    if fade < 1.0:
        out = ImageEnhance.Brightness(out).enhance(max(0.0, fade))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--t0", type=float, default=0.0)
    ap.add_argument("--t1", type=float, default=16.0)
    ap.add_argument("--out", default=str(HERE.parent / "assets" / "duelo3d.webp"))
    ap.add_argument("--quality", type=int, default=70)
    ap.add_argument("--port", type=int, default=8766)
    ap.add_argument("--workdir", default=str(HERE.parent / ".cinema_frames"))
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--skip-render", action="store_true", help="reaproveita os quadros ja renderizados")
    a = ap.parse_args()

    work = Path(a.workdir)
    n = round((a.t1 - a.t0) * a.fps)
    if not a.skip_render:
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        Receiver.frames_dir = work
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), Receiver)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        chrome = next((c for c in CHROME_CANDIDATES if Path(c).exists()), None)
        if not chrome:
            sys.exit("Chrome/Edge nao encontrado")
        url = f"http://127.0.0.1:{a.port}/render.html?batch=1&fps={a.fps}&t0={a.t0}&t1={a.t1}&host=http://127.0.0.1:{a.port}"
        prof = work / "chrome-profile"
        t_start = time.time()
        proc = subprocess.Popen(
            [chrome, "--headless=new", "--no-sandbox", "--enable-unsafe-swiftshader", "--use-angle=swiftshader",
             "--ignore-gpu-blocklist", "--hide-scrollbars", "--window-size=900,344", f"--user-data-dir={prof}", url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        last = 0
        while not Receiver.done.wait(2.0):
            if Receiver.count != last and Receiver.count % 30 == 0:
                last = Receiver.count
                el = time.time() - t_start
                print(f"  {Receiver.count}/{n} quadros ({el:.0f}s, {el / max(1, Receiver.count):.2f}s/quadro)", flush=True)
            if proc.poll() is not None and not Receiver.done.is_set():
                sys.exit("Chrome encerrou antes de terminar")
        proc.terminate()
        srv.shutdown()
        print(f"render: {Receiver.count} quadros em {time.time() - t_start:.0f}s")

    files = sorted(work.glob("f*.jpg"))
    first = Image.open(files[0]).convert("RGB")
    vig = vignette_mask(*first.size)
    frames = []
    total = len(files)
    for i, f in enumerate(files):
        t = i / a.fps
        fade = min(1.0, t / 0.7, (total / a.fps - t) / 0.9)
        frames.append(post(Image.open(f).convert("RGB"), vig, fade))
    t_enc = time.time()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=int(1000 / a.fps), loop=0,
                   quality=a.quality, method=4, minimize_size=False)
    size = out.stat().st_size / 1e6
    print(f"webp: {out.name} {size:.2f} MB para {total / a.fps:.1f}s ({total} quadros, {size / (total / a.fps):.2f} MB/s) em {time.time() - t_enc:.0f}s")
    if not a.keep and not a.skip_render:
        pass
    return size


if __name__ == "__main__":
    main()
