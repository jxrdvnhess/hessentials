# Sketch 301 — A8: can an image promise IDENTITY?
# One tool family (paired loop handles). The discriminating head withheld three ways.
# C: full view. T1: drawer occlusion. T2: foreshortening. T3: draped cloth.
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (240, 234, 222), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.4, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def loops(d, cx, cy, ang_deg, spread=34, r=40, w=9):
    """Two loop handles + shaft stubs, pointing along ang_deg."""
    a = math.radians(ang_deg)
    nx, ny = -math.sin(a), math.cos(a)
    pts = []
    for s in (-1, 1):
        lx, ly = cx + s * nx * spread, cy + s * ny * spread
        d.ellipse([lx - r, ly - r, lx + r, ly + r], outline=INK, width=w)
        sx, sy = lx + math.cos(a) * r * 0.9, ly + math.sin(a) * r * 0.9
        ex, ey = cx + math.cos(a) * (r + 95), cy + math.sin(a) * (r + 95) + s * 6
        d.line([(sx, sy), (ex, ey)], fill=INK, width=w + 3)
        pts.append((ex, ey))
    return pts  # where the shafts end (the pivot region)

# C — the whole tool, plainly: scissors
def ctrl():
    im = ground(); d = ImageDraw.Draw(im)
    ends = loops(d, 190, 320, 0)
    px, py = 330, 320
    for ex, ey in ends:
        d.line([(ex, ey), (px, py)], fill=INK, width=11)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=INK)  # pivot
    d.polygon([(px, py - 5), (520, 290), (528, 300), (px, py + 4)], fill=INK)  # blade 1
    d.polygon([(px, py + 5), (516, 352), (508, 360), (px, py - 4)], fill=INK)  # blade 2
    d.ellipse([200, 390, 520, 412], fill=(214, 206, 192))
    im.save(f"{OUT}/t0_control.png")

# T1 — drawer: handles rise out of a part-open drawer; the head is inside
def drawer():
    im = ground(); d = ImageDraw.Draw(im)
    d.rectangle([80, 330, 560, 560], fill=(196, 182, 160))          # drawer front
    d.rectangle([80, 330, 560, 344], fill=(160, 146, 126))          # top edge of front
    d.rectangle([80, 296, 560, 330], fill=(58, 50, 44))             # the open gap
    d.rectangle([60, 286, 580, 300], fill=(205, 192, 172))          # carcass rail above
    d.ellipse([300, 430, 340, 470], fill=(150, 136, 118))           # knob
    # handles + shaft stubs emerging from the gap, head down inside
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    loops(dl, 320, 210, 90, spread=44, r=42, w=9)                   # pointing down into gap
    im.paste(lay, (0, 0), lay)
    im.save(f"{OUT}/t1_drawer.png")

# T2 — foreshortening: loops near, the head pointing away, reduced to a sliver
def foreshort():
    im = ground(); d = ImageDraw.Draw(im)
    # big near loops
    for s, (lx, ly, rr) in enumerate([(180, 260, 62), (210, 380, 62)]):
        d.ellipse([lx - rr, ly - rr, lx + rr, ly + rr], outline=INK, width=13)
    # shafts converging hard to a far point (perspective)
    d.line([(238, 282), (470, 316)], fill=INK, width=12)
    d.line([(266, 364), (470, 326)], fill=INK, width=12)
    # the entire head: a tiny foreshortened sliver at the far end
    d.polygon([(470, 313), (498, 318), (497, 324), (470, 329)], fill=INK)
    d.line([(498, 318), (504, 320)], fill=INK, width=2)
    d.ellipse([160, 440, 480, 462], fill=(214, 206, 192))
    im.save(f"{OUT}/t2_foreshort.png")

# T3 — the cloth: handles visible; everything past the shafts under a draped cloth
def cloth():
    im = ground(); d = ImageDraw.Draw(im)
    d.line([(60, 430), (580, 430)], fill=(190, 182, 168), width=3)
    ends = loops(d, 170, 330, -4)
    # cloth mound covering the head region
    mound = [(320, 430), (330, 360), (370, 322), (430, 306), (490, 318),
             (530, 352), (548, 396), (552, 430)]
    d.polygon(mound, fill=(225, 219, 207), outline=(186, 178, 164))
    for x0, y0, x1, y1 in [(360, 430, 392, 330), (420, 430, 430, 310),
                           (470, 430, 498, 326), (510, 430, 532, 360)]:
        d.line([(x0, y0), (x1, y1)], fill=(200, 192, 178), width=3)
    d.ellipse([330, 432, 560, 452], fill=(212, 204, 190))
    im.save(f"{OUT}/t3_cloth.png")

if __name__ == "__main__":
    ctrl(); drawer(); foreshort(); cloth()
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["t0_control", "t1_drawer", "t2_foreshort", "t3_cloth"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
