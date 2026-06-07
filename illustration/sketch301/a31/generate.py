# Sketch 301 — A31: Five-slot schema over six elements. The risky prediction:
# a die-five quincunx + a sixth dot. Does the schema delete the extra to keep roster 5?
# Sixth dosed from interior-near-center to far-outside, to pit roster-match (delete
# regardless) against salience/field (a salient sixth survives).
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

# the fixed quincunx (die-five), identical in every image
QUINCUNX = [(195, 195, 40, 11), (470, 195, 30, 23), (332, 332, 44, 37),
            (195, 470, 34, 41), (470, 470, 30, 53)]
# the sixth dot, dosed from interior (near center, absorbable) to far-outside (salient).
# kept OFF the die grid lines so it can't complete a die-six.
SIXTHS = {
    "a_interior":  (278, 278, 26, 67),   # tucked between center and TL corner
    "b_midway":    (332, 235, 26, 67),    # interior, above center (inside the square)
    "c_edge":      (332, 560, 28, 67),    # just below the die, outside the square
    "d_far":       (575, 332, 30, 67),    # far right, clearly detached outlier
}

def render(name, sixth):
    im = ground(); d = ImageDraw.Draw(im)
    for cx, cy, r, seed in QUINCUNX:
        blob(d, cx, cy, r, seed)
    blob(d, *sixth)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, sixth in SIXTHS.items():
        render(name, sixth)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_interior", "b_midway", "c_edge", "d_far"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
