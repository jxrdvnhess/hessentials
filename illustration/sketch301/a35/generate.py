# Sketch 301 — A35: Separation. Isolate enforcement vs perceptual merging.
# Eighth-note family; vary ONLY flag separation. A 1-flag / B 2-close / C 2-far / D detached.
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def flag(d, sx, y0, scale=1.0, w=8):
    pts = [(sx, y0)]
    for t in range(1, 9):
        tt = t / 8
        pts.append((sx + 52 * scale * tt, y0 + 10 + 64 * scale * tt - 26 * scale * tt * tt))
    d.line(pts, fill=INK, width=w, joint="curve")

def base_note(d, hx=285, hy=380, stem_h=230):
    d.ellipse([hx - 34, hy - 24, hx + 34, hy + 24], fill=INK)
    sx = hx + 46
    sy_top = hy - stem_h
    d.line([(sx, hy - 6), (sx, sy_top)], fill=INK, width=7)
    return sx, sy_top

def render(name, mode):
    im = ground(); d = ImageDraw.Draw(im)
    sx, sy_top = base_note(d)
    if mode == "one":
        flag(d, sx, sy_top)
    elif mode == "close":          # A34 replication: ~34 px apart
        flag(d, sx, sy_top)
        flag(d, sx, sy_top + 34)
    elif mode == "far":            # widely separated, unmergeable: ~95 px apart
        flag(d, sx, sy_top)
        flag(d, sx, sy_top + 95)
    elif mode == "detached":       # 1 attached + 1 detached but plausibly belonging
        flag(d, sx, sy_top)
        flag(d, sx + 30, sy_top + 18)   # offset off the stem, still near the note's top
    im.save(f"{OUT}/{name}.png")

if __name__ == "__main__":
    render("a_one", "one")
    render("b_close", "close")
    render("c_far", "far")
    render("d_detached", "detached")
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, name in enumerate(["a_one", "b_close", "c_far", "d_detached"]):
        s.paste(Image.open(f"{OUT}/{name}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
