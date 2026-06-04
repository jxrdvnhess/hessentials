# Sketch 301 — A26: The Phantom's Shape. Which organization creates the phantom?
# Five elements always: center+satellites / chain / two groups / ambiguous scatter.
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

CONFIGS = {
    # strong radial: one large center, four satellites at varied angles/distances
    "a_radial": [(320, 320, 54, 11), (200, 205, 30, 23), (455, 245, 34, 37),
                 (440, 445, 28, 41), (185, 430, 36, 53)],
    # chain: a curving directional progression, similar spacing, no straight row
    "b_chain": [(130, 465, 30, 11), (222, 392, 38, 23), (310, 345, 34, 37),
                (412, 302, 40, 41), (512, 228, 32, 53)],
    # two groups: 2 upper-left, 3 lower-right, clear separation
    "c_groups": [(180, 218, 40, 11), (252, 262, 30, 23), (424, 398, 44, 37),
                 (492, 356, 28, 41), (452, 470, 34, 53)],
    # ambiguous: near-uniform sizes, no center dominance, no alignments, no pairs
    "d_ambiguous": [(152, 228, 34, 11), (432, 162, 36, 23), (540, 392, 32, 37),
                    (212, 472, 38, 41), (368, 330, 31, 53)],
}

def render(name, elems):
    im = ground(); d = ImageDraw.Draw(im)
    for cx, cy, r, seed in elems:
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, elems in CONFIGS.items():
        render(name, elems)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(CONFIGS):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
