# Sketch 301 — A22 (per A21 review recommendation): arrangement at fixed count.
# The same five blobs, four configurations: scatter / row / ring / cluster+outlier.
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
    radii = [r * rng.uniform(0.78, 1.18) for _ in range(n)]
    radii = [(radii[i - 1] + radii[i] + radii[(i + 1) % n]) / 3 for i in range(n)]
    pts = [(cx + radii[i] * math.cos(2 * math.pi * i / n),
            cy + radii[i] * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d.polygon(pts, fill=INK)

# the same five elements as A21 (size, seed), repositioned per configuration
SIZES = [(52, 11), (38, 23), (30, 37), (44, 41), (26, 53)]

CONFIGS = {
    "a_scatter": [(300, 330), (438, 252), (172, 318), (392, 432), (174, 416)],  # = A21 step 5
    "b_row":     [(120, 320), (220, 320), (320, 320), (420, 320), (520, 320)],
    "c_ring":    [(320, 170), (463, 274), (408, 442), (232, 442), (177, 274)],
    "d_outlier": [(238, 286), (336, 258), (276, 372), (372, 350), (530, 478)],
}

def render(name, pts):
    im = ground(); d = ImageDraw.Draw(im)
    for (cx, cy), (r, seed) in zip(pts, SIZES):
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, pts in CONFIGS.items():
        render(name, pts)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(CONFIGS):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
