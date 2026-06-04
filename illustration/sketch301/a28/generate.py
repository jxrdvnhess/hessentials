# Sketch 301 — A28: Sticky Claims. Pair-claim strength dosed; the fifth element fixed.
# A clean pairs / B weak pairs / C pairs-vs-arc ambiguous / D pair failure.
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

FIFTH = (320, 130, 34, 67)   # fixed in every image

CONFIGS = {
    # tight pairs, fifth far away
    "a_clean": [(170, 340, 38, 11), (236, 366, 32, 23),
                (420, 350, 40, 37), (489, 378, 30, 41)],
    # pairs loosened, still pairs
    "b_weak": [(152, 326, 38, 11), (262, 378, 32, 23),
               (402, 336, 40, 37), (514, 392, 30, 41)],
    # four on a shallow arc with near-even gaps: pairs vs arc, neither dominant
    "c_ambiguous": [(158, 362, 38, 11), (264, 398, 32, 23),
                    (390, 398, 40, 37), (496, 362, 30, 41)],
    # four spread evenly: pair reading barely supportable; 4+1 obvious
    "d_failure": [(140, 344, 38, 11), (260, 384, 32, 23),
                  (380, 384, 40, 37), (500, 344, 30, 41)],
}

def render(name, lower):
    im = ground(); d = ImageDraw.Draw(im)
    blob(d, *FIFTH)
    for cx, cy, r, seed in lower:
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    for name, lower in CONFIGS.items():
        render(name, lower)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(CONFIGS):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
