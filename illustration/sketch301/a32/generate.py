# Sketch 301 — A32: Transfer. Does a recruited schema enforce its OWN roster?
# Polygon-vertex schemas (triangle=3, hexagon=6), each with surplus/deficit.
import math, random
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
CX, CY = 320, 322

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def blob(d, cx, cy, r, seed):
    rng = random.Random(seed)
    n = 14
    radii = [r * rng.uniform(0.86, 1.10) for _ in range(n)]
    radii = [(radii[i - 1] + radii[i] + radii[(i + 1) % n]) / 3 for i in range(n)]
    pts = [(cx + radii[i] * math.cos(2 * math.pi * i / n),
            cy + radii[i] * math.sin(2 * math.pi * i / n)) for i in range(n)]
    d.polygon(pts, fill=INK)

def poly(nv, R, rot=-90):
    return [(CX + R * math.cos(math.radians(rot + i * 360 / nv)),
             CY + R * math.sin(math.radians(rot + i * 360 / nv))) for i in range(nv)]

SEEDS = [11, 23, 37, 41, 53, 67, 73, 83]

def render(name, pts, sizes=None):
    im = ground(); d = ImageDraw.Draw(im)
    sizes = sizes or [34] * len(pts)
    for (cx, cy), r, seed in zip(pts, sizes, SEEDS):
        blob(d, cx, cy, r, seed)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    # A: triangle (3 verts) + 1 surplus near the centroid  → 4 elements
    tri = poly(3, 200)
    render("a_tri_surplus", tri + [(CX, CY + 18)])
    # B: triangle layout, only 2 of 3 vertices filled  → 2 elements (deficit)
    render("b_tri_deficit", [tri[0], tri[1]])
    # C: hexagon (6 verts) with one vertex MISSING  → 5 elements (deficit)
    hexv = poly(6, 205)
    render("c_hex_deficit", hexv[:5])
    # D: hexagon (6 verts) + 1 surplus at center  → 7 elements (surplus)
    render("d_hex_surplus", hexv + [(CX, CY)])
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_tri_surplus", "b_tri_deficit", "c_hex_deficit", "d_hex_surplus"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
