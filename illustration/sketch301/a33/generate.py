# Sketch 301 — A33: Positive Control. A second occupancy-bearing object: the traffic
# light (constitutively 3 lights). A 3 / B 4 surplus / C 2 deficit / D salient violation.
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
LIGHT = (224, 218, 204)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def housing(d, top, bottom, cx=320, half=66):
    d.rounded_rectangle([cx - half, top, cx + half, bottom], 34, fill=INK)
    # short post
    d.rectangle([cx - 12, bottom - 4, cx + 12, bottom + 60], fill=INK)

def light(d, cx, cy, r=42, fill=LIGHT):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(60, 54, 48), width=2)

def render_lights(name, n, salient_extra=False):
    im = ground(); d = ImageDraw.Draw(im)
    cx = 320
    pad = 30
    r = 42
    gap = 22
    top = 120
    bottom = top + 2 * pad + n * 2 * r + (n - 1) * gap if not salient_extra else None
    if salient_extra:
        # housing holds 3; the 4th light is large and protrudes outside, lower-right
        n_in = 3
        bottom = top + 2 * pad + n_in * 2 * r + (n_in - 1) * gap
        housing(d, top, bottom)
        y = top + pad + r
        for i in range(n_in):
            light(d, cx, y); y += 2 * r + gap
        # salient extra: big, bright, outside the housing
        light(d, cx + 150, bottom - 70, r=64, fill=(236, 230, 216))
    else:
        housing(d, top, bottom)
        y = top + pad + r
        for i in range(n):
            light(d, cx, y); y += 2 * r + gap
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render_lights("a_three", 3)
    render_lights("b_four", 4)
    render_lights("c_two", 2)
    render_lights("d_salient", 3, salient_extra=True)
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_three", "b_four", "c_two", "d_salient"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
