# Sketch 301 — A27: Misfit Gradient. Radial fit degraded by dosed center-offset.
# Satellites fixed; only the central blob moves. Four doses.
import math, random
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

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

SATS = [(200, 205, 30, 23), (455, 245, 34, 37), (440, 445, 28, 41), (185, 430, 36, 53)]
# satellite centroid ≈ (320, 331); the center blob (r=54, seed 11) moves off it:
CENTERS = {
    "a_perfect": (320, 331),   # dose 0
    "b_slight":  (356, 329),   # ~36 px
    "c_moderate": (392, 330),  # ~72 px
    "d_severe":  (428, 332),   # ~108 px — at the hull's edge, not pairing (>= 90 px to each satellite)
}

def render(name, c):
    im = ground(); d = ImageDraw.Draw(im)
    blob(d, c[0], c[1], 54, 11)
    for cx, cy, r, seed in SATS:
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, c in CENTERS.items():
        render(name, c)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(CENTERS):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
