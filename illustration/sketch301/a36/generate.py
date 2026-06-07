# Sketch 301 — A36: Reversal. Recruited identity vs default identity.
# An ambiguous-flag target note placed in sixteenth / eighth / mixed contexts.
# Does context flip the target's reported flag-count?
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def flag(d, sx, y0, scale=1.0, w=7):
    pts = [(sx, y0)]
    for t in range(1, 9):
        tt = t / 8
        pts.append((sx + 44 * scale * tt, y0 + 8 + 54 * scale * tt - 22 * scale * tt * tt))
    d.line(pts, fill=INK, width=w, joint="curve")

def note(d, hx, hy, kind, stem_h=170):
    # kind: 0=quarter,1=eighth,2=sixteenth,'amb'=one full + one partial flag
    d.ellipse([hx - 28, hy - 20, hx + 28, hy + 20], fill=INK)
    sx = hx + 38
    sy_top = hy - stem_h
    d.line([(sx, hy - 5), (sx, sy_top)], fill=INK, width=6)
    if kind == 0:
        pass
    elif kind == 1:
        flag(d, sx, sy_top)
    elif kind == 2:
        flag(d, sx, sy_top); flag(d, sx, sy_top + 28)
    elif kind == "amb":
        flag(d, sx, sy_top)                       # one full flag
        flag(d, sx, sy_top + 28, scale=0.46, w=4) # one short/faint partial flag

def render(name, layout):
    # layout: list of (kind) left-to-right; target marked by 'amb'
    im = ground(); d = ImageDraw.Draw(im)
    n = len(layout)
    xs = [int(W * (i + 1) / (n + 1)) for i in range(n)]
    hy = 380
    for x, kind in zip(xs, layout):
        note(d, x, hy, kind)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render("a_alone", ["amb"])
    render("b_sixteenth_ctx", [2, 2, "amb", 2])
    render("c_eighth_ctx", [1, 1, "amb", 1])
    render("d_mixed_ctx", [0, 1, 2, "amb"])
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_alone", "b_sixteenth_ctx", "c_eighth_ctx", "d_mixed_ctx"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
