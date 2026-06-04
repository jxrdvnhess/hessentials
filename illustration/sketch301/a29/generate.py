# Sketch 301 — A29: Absorbability. The fifth member dosed from embedded to dominant.
# Constant: upper pair + lower pair. Variable: the fifth's position (and, at D, size).
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

CONST = [(180, 218, 40, 11), (252, 262, 30, 23),     # upper pair
         (410, 390, 44, 37), (474, 468, 34, 41)]     # lower pair
FIFTHS = {
    "a_embedded": (478, 366, 28, 53),   # nested against the lower group (~60 px)
    "b_released": (516, 330, 28, 53),   # intermediate (~115 px)
    "c_salient":  (552, 282, 28, 53),   # clearly separate (~175 px)
    "d_dominant": (540, 290, 56, 53),   # separate AND the largest member
}

def render(name, fifth):
    im = ground(); d = ImageDraw.Draw(im)
    for cx, cy, r, seed in CONST:
        blob(d, cx, cy, r, seed)
    blob(d, *fifth)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, fifth in FIFTHS.items():
        render(name, fifth)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(FIFTHS):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
