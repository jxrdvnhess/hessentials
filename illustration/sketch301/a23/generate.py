# Sketch 301 — A23: Perceived Configuration. Does arrangement survive size distortion?
# Ring/row × equal/unequal sizes. Same blob family, five elements, nothing else.
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

SEEDS = [11, 23, 37, 41, 53]
EQUAL = [40] * 5
UNEQUAL = [58, 22, 44, 16, 50]   # more aggressive than A22

RING = [(320 + 175 * math.cos(math.radians(a - 90)),
         320 + 175 * math.sin(math.radians(a - 90))) for a in range(0, 360, 72)]
ROW = [(120 + i * 100, 320) for i in range(5)]

def render(name, pts, sizes):
    im = ground(); d = ImageDraw.Draw(im)
    for (cx, cy), r, seed in zip(pts, sizes, SEEDS):
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render("a_ring_equal", RING, EQUAL)
    render("b_ring_unequal", RING, UNEQUAL)
    render("c_row_equal", ROW, EQUAL)
    render("d_row_unequal", ROW, UNEQUAL)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_ring_equal", "b_ring_unequal", "c_row_equal", "d_row_unequal"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
