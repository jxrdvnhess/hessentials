# Sketch 301 — A25: The Census. Is counting derived from elements or organization?
# 5-scatter (replication) / 6-scatter / 5-row / 6-row. Counts must volunteer.
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

# A: the A21/A22 scatter, exactly (third exposure of the replication cell)
SCATTER5 = [(300, 330, 52, 11), (438, 252, 38, 23), (172, 318, 30, 37),
            (392, 432, 44, 41), (174, 416, 26, 53)]
# B: same character, one more element, still unorganized
SCATTER6 = SCATTER5 + [(480, 510, 34, 67)]

def scatter(name, elems):
    im = ground(); d = ImageDraw.Draw(im)
    for cx, cy, r, seed in elems:
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

def row(name, n):
    im = ground(); d = ImageDraw.Draw(im)
    xs = [int(320 - (n - 1) * 45 + i * 90) for i in range(n)]
    seeds = [11, 23, 37, 41, 53, 67]
    for x, seed in zip(xs, seeds[:n]):
        blob(d, x, 320, 36, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    scatter("a_scatter5", SCATTER5)
    scatter("b_scatter6", SCATTER6)
    row("c_row5", 5)
    row("d_row6", 6)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_scatter5", "b_scatter6", "c_row5", "d_row6"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
