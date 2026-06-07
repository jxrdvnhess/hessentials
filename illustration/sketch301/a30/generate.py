# Sketch 301 — A30: Schema Protection. Does inviting a schema repair the +1 field?
# Same five blob identities throughout; only the arrangement's schema-ability varies.
# A baseline diagonal clusters (the +1 producer) / B weak / C strong quincunx /
# D competing (quincunx vs 2+2+1).
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

# fixed identities (size, seed) carried across all four images
IDS = [(40, 11), (30, 23), (44, 37), (34, 41), (30, 53)]

POS = {
    # A: the A29 diagonal two-cluster +1 field
    "a_baseline": [(180, 218), (252, 262), (410, 390), (474, 468), (516, 330)],
    # B: weak — a center emerges but corners are uneven/asymmetric, schema only faint
    "b_weak":     [(178, 224), (452, 268), (336, 360), (236, 470), (502, 432)],
    # C: clean quincunx — die-five, seats all five, known to count right
    "c_strong":   [(195, 195), (470, 195), (332, 332), (195, 470), (470, 470)],
    # D: competing — reads as quincunx OR as two pairs + center (2+2+1)
    "d_competing": [(205, 250), (300, 250), (332, 332), (205, 415), (300, 415)],
}
# D competing: two vertical pairs flanking a center — reads as quincunx OR 2+2+1
POS["d_competing"] = [(210, 210), (210, 320), (332, 332), (455, 210), (455, 320)]

def render(name, pos):
    im = ground(); d = ImageDraw.Draw(im)
    for (cx, cy), (r, seed) in zip(pos, IDS):
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, pos in POS.items():
        render(name, pos)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_baseline", "b_weak", "c_strong", "d_competing"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
