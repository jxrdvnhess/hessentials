# Sketch 301 — A34: Numeric Identity. A non-pip count-defined object: the flagged
# musical note (flag count = name; eighth=1 flag, sixteenth=2). Tests whether a
# count violation is DELETED (die-style enforcement) or RE-IDENTIFIED (renamed).
import math
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def note(d, hx, hy, n_flags, stem_h=210, stem_x_off=46):
    # filled, slightly rotated notehead
    d.ellipse([hx - 34, hy - 24, hx + 34, hy + 24], fill=INK)
    # stem up the right side
    sx = hx + stem_x_off
    sy_top = hy - stem_h
    d.line([(sx, hy - 6), (sx, sy_top)], fill=INK, width=7)
    # flags off the top-right
    for i in range(n_flags):
        y0 = sy_top + i * 34
        pts = [(sx, y0)]
        for t in range(1, 9):
            tt = t / 8
            pts.append((sx + 52 * tt, y0 + 10 + 64 * tt - 26 * tt * tt))
        d.line(pts, fill=INK, width=8, joint="curve")
    return sx, sy_top

def render(name, n_flags, salient_extra=False):
    im = ground(); d = ImageDraw.Draw(im)
    sx, sy_top = note(d, 285, 380, n_flags if not salient_extra else 1)
    if salient_extra:
        # a big detached flag floating to the right, not on the stem
        x0, y0 = 470, 250
        pts = [(x0, y0)]
        for t in range(1, 9):
            tt = t / 8
            pts.append((x0 + 78 * tt, y0 + 14 + 96 * tt - 38 * tt * tt))
        d.line(pts, fill=INK, width=11, joint="curve")
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render("a_eighth", 1)       # eighth note (1 flag) — control
    render("b_two", 2)          # two flags (sixteenth) — "surplus"
    render("c_zero", 0)         # no flag (quarter note) — "deficit"
    render("d_salient", 1, salient_extra=True)  # eighth + detached extra flag
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_eighth", "b_two", "c_zero", "d_salient"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
