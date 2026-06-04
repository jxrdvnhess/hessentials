# Sketch 301 — A24: Configuration Rescue. Can the failed unequal ring be saved?
# A baseline (A23 replication) / B + faint contour / C density (9 blobs) / D both.
import math, random
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
FAINT = (203, 195, 181)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def blob(d, cx, cy, r, seed):
    rng = random.Random(seed)
    n = 14
    radii = [r * rng.uniform(0.82, 1.14) for _ in range(n)]
    radii = [(radii[i - 1] + radii[i] + radii[(i + 1) % n]) / 3 for i in range(n)]
    pts = [(cx + radii[i] * math.cos(2 * math.pi * i / n),
            cy + radii[i] * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d.polygon(pts, fill=INK)

R = 175
CX, CY = 320, 320

def ring_pts(n):
    return [(CX + R * math.cos(math.radians(a - 90)),
             CY + R * math.sin(math.radians(a - 90)))
            for a in [i * 360 / n for i in range(n)]]

SIZES5 = [58, 22, 44, 16, 50]
SEEDS5 = [11, 23, 37, 41, 53]
SIZES9 = [58, 22, 44, 16, 50, 30, 54, 20, 40]
SEEDS9 = [11, 23, 37, 41, 53, 61, 73, 83, 97]

def contour(d):
    d.ellipse([CX - R, CY - R, CX + R, CY + R], outline=FAINT, width=3)

def render(name, n, with_contour):
    im = ground(); d = ImageDraw.Draw(im)
    if with_contour:
        contour(d)
    sizes = SIZES5 if n == 5 else SIZES9
    seeds = SEEDS5 if n == 5 else SEEDS9
    for (cx, cy), r, seed in zip(ring_pts(n), sizes, seeds):
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render("a_baseline", 5, False)
    render("b_contour", 5, True)
    render("c_density", 9, False)
    render("d_combined", 9, True)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_baseline", "b_contour", "c_density", "d_combined"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
