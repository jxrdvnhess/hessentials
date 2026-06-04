# Sketch 301 — A9: the completion machinery, studied directly.
# Scissors base. Three deletions x two edge characters (clean termination vs torn break).
import math
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)

def ground():
    base = np.full((H, W, 3), (240, 234, 222), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.4, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def torn(d, x, y, ang_deg, w=14):
    """A torn break at (x,y), oriented along ang_deg: jagged notch + splinters."""
    a = math.radians(ang_deg)
    nx, ny = -math.sin(a), math.cos(a)
    # jagged zigzag cap
    pts = []
    for i, off in enumerate([-w, -w * 0.4, -w * 0.1, w * 0.3, w * 0.7, w]):
        jag = (8 if i % 2 == 0 else -5)
        pts.append((x + nx * off + math.cos(a) * jag, y + ny * off + math.sin(a) * jag))
    d.polygon(pts + [(x + nx * w - math.cos(a) * 10, y + ny * w - math.sin(a) * 10),
                     (x - nx * w - math.cos(a) * 10, y - ny * w - math.sin(a) * 10)], fill=INK)
    # splinters just beyond the break
    for off, ln in [(-w * 0.5, 14), (w * 0.2, 18), (w * 0.8, 10)]:
        sx, sy = x + nx * off + math.cos(a) * 6, y + ny * off + math.sin(a) * 6
        d.polygon([(sx, sy), (sx + math.cos(a) * ln + nx * 2, sy + math.sin(a) * ln + ny * 2),
                   (sx + math.cos(a) * ln * 0.6 - nx * 3, sy + math.sin(a) * ln * 0.6 - ny * 3)],
                  fill=INK)

def base(d, blades=True, loops_n=2, shaft_end=470):
    """Scissors: loops at left, shafts to pivot at (330,320), blades right."""
    ends = []
    for k, s in enumerate((-1, 1)):
        if k >= loops_n:
            continue
        ly = 320 + s * 44
        d.ellipse([110, ly - 40, 190, ly + 40], outline=INK, width=10)
        d.line([(186, ly), (330, 320 + s * 4)], fill=INK, width=13)
    px, py = 330, 320
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=INK)
    if blades:
        d.polygon([(px, py - 6), (shaft_end + 50, 292), (shaft_end + 58, 301), (px, py + 4)], fill=INK)
        d.polygon([(px, py + 6), (shaft_end + 46, 350), (shaft_end + 38, 358), (px, py - 4)], fill=INK)
    return px, py

# D1 — blades deleted
def d1a():  # clean: shafts simply end at the pivot, rounded
    im = ground(); d = ImageDraw.Draw(im)
    base(d, blades=False)
    d.ellipse([322, 312, 338, 328], fill=INK)  # neat rounded terminus
    im.save(f"{OUT}/d1a_blades_gone_clean.png")

def d1b():  # torn: blades broken off just past the pivot
    im = ground(); d = ImageDraw.Draw(im)
    px, py = base(d, blades=False)
    d.polygon([(px, py - 6), (368, 306), (372, 312), (px, py + 4)], fill=INK)  # blade stumps
    d.polygon([(px, py + 6), (366, 332), (362, 338), (px, py - 4)], fill=INK)
    torn(d, 372, 310, 0, w=8)
    torn(d, 366, 336, 8, w=8)
    im.save(f"{OUT}/d1b_blades_gone_torn.png")

# D2 — one loop deleted
def d2a():  # clean absence: lower loop simply not there; its shaft ends in a cap
    im = ground(); d = ImageDraw.Draw(im)
    base(d, blades=True, loops_n=1)
    d.line([(250, 348), (330, 324)], fill=INK, width=13)  # the loopless shaft, present
    d.ellipse([243, 341, 259, 357], fill=INK)             # smooth cap where loop would join
    im.save(f"{OUT}/d2a_loop_gone_clean.png")

def d2b():  # torn absence: stub + splinters where the loop was
    im = ground(); d = ImageDraw.Draw(im)
    base(d, blades=True, loops_n=1)
    d.line([(250, 348), (330, 324)], fill=INK, width=13)
    torn(d, 250, 348, 200, w=9)
    im.save(f"{OUT}/d2b_loop_gone_torn.png")

# D3 — the middle deleted: loops left, blade tips right, nothing between
def d3a():  # clean: both fragments taper smoothly into the gap
    im = ground(); d = ImageDraw.Draw(im)
    for s in (-1, 1):
        ly = 320 + s * 44
        d.ellipse([110, ly - 40, 190, ly + 40], outline=INK, width=10)
        d.polygon([(186, ly - 7), (262, 320 + s * 24 - 2), (262, 320 + s * 24 + 2),
                   (186, ly + 7)], fill=INK)              # shaft tapering to nothing
    d.polygon([(450, 305), (528, 292), (536, 301), (458, 311)], fill=INK)  # blade tips
    d.polygon([(452, 337), (524, 350), (516, 358), (446, 343)], fill=INK)
    im.save(f"{OUT}/d3a_middle_gone_clean.png")

def d3b():  # torn: both sides break raggedly at the gap
    im = ground(); d = ImageDraw.Draw(im)
    for s in (-1, 1):
        ly = 320 + s * 44
        d.ellipse([110, ly - 40, 190, ly + 40], outline=INK, width=10)
        d.line([(186, ly), (268, 320 + s * 22)], fill=INK, width=13)
        torn(d, 268, 320 + s * 22, s * 14, w=8)
    d.polygon([(452, 303), (528, 292), (536, 301), (460, 312)], fill=INK)
    d.polygon([(450, 338), (524, 350), (516, 358), (444, 345)], fill=INK)
    torn(d, 455, 307, 188, w=7)
    torn(d, 450, 341, 172, w=7)
    im.save(f"{OUT}/d3b_middle_gone_torn.png")

if __name__ == "__main__":
    d1a(); d1b(); d2a(); d2b(); d3a(); d3b()
    sheet = Image.new("RGB", (3 * 330, 2 * 330), (255, 255, 255))
    names = ["d1a_blades_gone_clean", "d1b_blades_gone_torn", "d2a_loop_gone_clean",
             "d2b_loop_gone_torn", "d3a_middle_gone_clean", "d3b_middle_gone_torn"]
    for k, n in enumerate(names):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)),
                    ((k % 3) * 330 + 5, (k // 3) * 330 + 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
