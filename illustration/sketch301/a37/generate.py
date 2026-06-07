# Sketch 301 — A37: Name capture. Can a strong uniform context flip the NAME
# (not just the count)? Plus a beamed-sixteenth positive control.
import numpy as np
from PIL import Image, ImageDraw

W, H = 760, 460
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def flag(d, sx, y0, scale=1.0, w=6):
    pts = [(sx, y0)]
    for t in range(1, 9):
        tt = t / 8
        pts.append((sx + 34 * scale * tt, y0 + 6 + 42 * scale * tt - 18 * scale * tt * tt))
    d.line(pts, fill=INK, width=w, joint="curve")

def note(d, hx, hy, kind, stem_h=140):
    d.ellipse([hx - 22, hy - 15, hx + 22, hy + 15], fill=INK)
    sx = hx + 30
    sy = hy - stem_h
    d.line([(sx, hy - 4), (sx, sy)], fill=INK, width=5)
    if kind == 1:
        flag(d, sx, sy)
    elif kind == 2:
        flag(d, sx, sy); flag(d, sx, sy + 22)
    elif kind == "amb":
        flag(d, sx, sy); flag(d, sx, sy + 22, scale=0.45, w=3)
    return sx, sy

def render_row(name, layout):
    im = ground(); d = ImageDraw.Draw(im)
    n = len(layout)
    xs = [int(W * (i + 1) / (n + 1)) for i in range(n)]
    for x, k in zip(xs, layout):
        note(d, x, 300, k)
    im.save(f"{OUT}/{name}.png")

def render_beamed(name, n_beams, n=4):
    im = ground(); d = ImageDraw.Draw(im)
    xs = [int(W * (i + 1) / (n + 1)) for i in range(n)]
    sy = 300 - 150
    for x in xs:
        d.ellipse([x - 22, 285, x + 22, 315], fill=INK)
        sx = x + 30
        d.line([(sx, 296), (sx, sy)], fill=INK, width=5)
    # horizontal beams across the stem tops
    x0 = xs[0] + 30; x1 = xs[-1] + 30
    for b in range(n_beams):
        yy = sy + b * 20
        d.rectangle([x0, yy, x1, yy + 9], fill=INK)
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render_row("a_alone", ["amb"])
    render_row("b_sixteenth_strong", [2, 2, 2, "amb", 2, 2, 2])
    render_row("c_eighth_strong", [1, 1, 1, "amb", 1, 1, 1])
    render_beamed("d_beamed_sixteenth", 2)   # positive control: beamed = sixteenth
    s = Image.new("RGB", (4 * 330, int(330 * H / W)), (255, 255, 255))
    for k, name in enumerate(["a_alone", "b_sixteenth_strong", "c_eighth_strong", "d_beamed_sixteenth"]):
        im = Image.open(f"{OUT}/{name}.png").resize((320, int(320 * H / W)))
        s.paste(im, (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
