# Sketch 301 — A21: Recruitment Threshold. Pure accumulation, one form family.
# Five steps; each step adds one element; earlier elements never move.
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
    pts = []
    n = 14
    radii = [r * rng.uniform(0.78, 1.18) for _ in range(n)]
    # smooth radii once to keep edges soft, not spiky
    radii = [(radii[i - 1] + radii[i] + radii[(i + 1) % n]) / 3 for i in range(n)]
    for i in range(n):
        a = 2 * math.pi * i / n
        pts.append((cx + radii[i] * math.cos(a), cy + radii[i] * math.sin(a)))
    d.polygon(pts, fill=INK)

# fixed placements; chosen once, never moved; no rows, no face-triads
ELEMENTS = [
    (300, 330, 52, 11),   # 1
    (438, 252, 38, 23),   # 2
    (172, 318, 30, 37),   # 3
    (392, 432, 44, 41),   # 4
    (174, 416, 26, 53),   # 5
]

def step(n):
    im = ground(); d = ImageDraw.Draw(im)
    for cx, cy, r, seed in ELEMENTS[:n]:
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/step{n}.png")

if __name__ == "__main__":
    for n in range(1, 6):
        step(n)
    s = Image.new("RGB", (5 * 264, 264), (255, 255, 255))
    for k in range(1, 6):
        s.paste(Image.open(f"{OUT}/step{k}.png").resize((254, 254)), ((k - 1) * 264 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
