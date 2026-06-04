# Sketch 301 — A14: System Abandonment. Domain: cartographic documents.
# A control map / B locally damaged / C structurally re-platformed (star-chart grammar)
# / D boundary case (system-shaped, recruitment-hostile).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
SEA = (216, 211, 199)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def ground():
    base = np.full((H, W, 3), (226, 219, 207), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.5, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

SHEET = (70, 60, 570, 580)

def sheet_base():
    im = ground(); d = ImageDraw.Draw(im)
    d.rectangle([SHEET[0] + 6, SHEET[1] + 8, SHEET[2] + 6, SHEET[3] + 8], fill=(196, 188, 174))
    d.rectangle(SHEET, fill=(248, 244, 234), outline=(160, 152, 138), width=2)
    return im, d

def coast(d, sea_right=True):
    pts = [(SHEET[0], 150)]
    rng = random.Random(3)
    x, y = SHEET[0], 150
    while x < SHEET[2]:
        x += rng.randint(28, 50)
        y += rng.randint(-30, 42)
        y = max(SHEET[1] + 60, min(SHEET[3] - 220, y))
        pts.append((min(x, SHEET[2]), y))
    d.line(pts, fill=INK, width=3, joint="curve")
    # water texture below the coast
    rng2 = random.Random(5)
    for _ in range(60):
        wx = rng2.randint(SHEET[0] + 12, SHEET[2] - 24)
        wy = rng2.randint(150, SHEET[3] - 30)
        below = False
        for i in range(len(pts) - 1):
            if pts[i][0] <= wx <= pts[i + 1][0]:
                t = (wx - pts[i][0]) / max(1, pts[i + 1][0] - pts[i][0])
                cy = pts[i][1] + t * (pts[i + 1][1] - pts[i][1])
                below = wy > cy + 14
                break
        if below:
            d.line([(wx, wy), (wx + 14, wy)], fill=(170, 162, 148), width=2)
    return pts

def town(d, x, y, name, f, label_dy=-22):
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=INK)
    d.text((x, y + label_dy), name, font=f, fill=INK, anchor="mm")

def legend(d, f, rows, x0=None, y0=None):
    x0 = x0 or SHEET[0] + 22
    y0 = y0 or SHEET[3] - 130
    d.rectangle([x0, y0, x0 + 170, y0 + 104], outline=INK, width=2, fill=(250, 247, 240))
    for i, (sym, label) in enumerate(rows):
        yy = y0 + 22 + i * 28
        sym(d, x0 + 24, yy)
        d.text((x0 + 48, yy), label, font=f, fill=INK, anchor="lm")

def sym_road(d, x, y): d.line([(x - 14, y), (x + 14, y)], fill=INK, width=4)
def sym_town(d, x, y): d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=INK)
def sym_marsh(d, x, y):
    for k in (-8, 0, 8):
        d.line([(x + k - 4, y + 3), (x + k + 4, y + 3)], fill=INK, width=2)
        d.line([(x + k, y + 3), (x + k, y - 5)], fill=INK, width=2)
def sym_tree(d, x, y):
    d.polygon([(x, y - 9), (x - 7, y + 4), (x + 7, y + 4)], fill=INK)
    d.line([(x, y + 4), (x, y + 9)], fill=INK, width=2)

def scalebar(d, f, labels=("0", "1", "2 km"), x0=None, y0=None):
    x0 = x0 or SHEET[2] - 200
    y0 = y0 or SHEET[3] - 44
    d.line([(x0, y0), (x0 + 140, y0)], fill=INK, width=3)
    for i, lab in enumerate(labels):
        xx = x0 + i * 70
        d.line([(xx, y0 - 6), (xx, y0 + 6)], fill=INK, width=3)
        d.text((xx, y0 + 18), lab, font=f, fill=INK, anchor="mm")

def north(d, f, label="N", x=None, y=None):
    x = x or SHEET[2] - 60; y = y or SHEET[1] + 70
    d.line([(x, y + 26), (x, y - 18)], fill=INK, width=3)
    d.polygon([(x, y - 30), (x - 9, y - 10), (x + 9, y - 10)], fill=INK)
    d.text((x, y + 42), label, font=f, fill=INK, anchor="mm")

def map_a():
    im, d = sheet_base()
    f = ImageFont.truetype(FONT, 17)
    coast(d)
    t1, t2, t3 = (170, 230), (370, 130), (470, 250)
    d.line([t1, t2], fill=INK, width=4); d.line([t2, t3], fill=INK, width=4)
    d.line([t1, (300, 330), t3], fill=(120, 112, 100), width=3, joint="curve")
    town(d, *t1, "HALFORD", f); town(d, *t2, "CRAY", f); town(d, *t3, "WICK FERRY", f)
    for tx, ty in [(120, 120), (150, 95), (185, 115), (220, 90)]:
        sym_tree(d, tx, ty)
    legend(d, f, [(sym_road, "ROAD"), (sym_town, "TOWN"), (sym_marsh, "MARSH")])
    for mx, my in [(420, 480), (470, 500), (380, 510)]:
        sym_marsh(d, mx, my)
    scalebar(d, f); north(d, f)
    im.save(f"{OUT}/a_control.png")

def map_b():
    im, d = sheet_base()
    f = ImageFont.truetype(FONT, 17)
    pts = coast(d)
    t1, t2, t3 = (170, 230), (370, 130), (470, 250)
    d.line([t1, t2], fill=INK, width=4); d.line([t2, t3], fill=INK, width=4)
    d.line([(470, 250), (500, 420)], fill=INK, width=4)  # road runs into open water, ends
    town(d, *t1, "HALFORD", f); town(d, *t2, "CRAY", f); town(d, *t3, "WICK FERRY", f)
    town(d, 250, 470, "GORSE HILL", f)                   # a town in the sea
    for tx, ty in [(120, 120), (150, 95), (185, 115), (220, 90)]:
        sym_tree(d, tx, ty)
    legend(d, f, [(sym_road, "TOWN"), (sym_town, "MARSH"), (sym_marsh, "ROAD")])  # keys shuffled
    scalebar(d, f, labels=("0", "3", "1 km"))            # out of order
    north(d, f, label="S")                                # arrow up, labeled S
    im.save(f"{OUT}/b_damaged.png")

def glyphword(d, x, y, rng, n=None):
    n = n or rng.randint(3, 6)
    for i in range(n):
        h = rng.randint(8, 15)
        d.line([(x, y), (x + rng.randint(-2, 3), y - h)], fill=INK, width=2)
        if rng.random() < 0.45:
            d.line([(x - 3, y - h // 2), (x + 4, y - h // 2)], fill=INK, width=1)
        if rng.random() < 0.2:
            d.ellipse([x + 1, y - h - 4, x + 4, y - h - 1], fill=INK)
        x += rng.randint(7, 11)
    return x

def map_c():
    im, d = sheet_base()
    f = ImageFont.truetype(FONT, 15)
    rng = random.Random(14)
    d.arc([SHEET[0] - 180, SHEET[1] - 180, SHEET[2] + 180, SHEET[3] + 180], 20, 160,
          fill=INK, width=3)  # planisphere-like border arc
    stars = []
    for _ in range(26):
        sx, sy = rng.randint(SHEET[0] + 40, SHEET[2] - 40), rng.randint(SHEET[1] + 50, SHEET[3] - 160)
        r = rng.choice([2, 2, 3, 3, 4, 5, 6])
        stars.append((sx, sy, r))
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=INK)
    for chain_n in range(3):  # constellation polylines among the bigger dots
        big = [s for s in stars if s[2] >= 3]
        rng.shuffle(big)
        chain = big[:rng.randint(4, 5)]
        d.line([(s[0], s[1]) for s in chain], fill=(120, 112, 100), width=2, joint="curve")
        cx, cy = chain[0][0], chain[0][1]
        glyphword(d, cx + 8, cy - 8, rng, n=4)
    # magnitude legend: dot sizes
    x0, y0 = SHEET[0] + 22, SHEET[3] - 110
    d.rectangle([x0, y0, x0 + 200, y0 + 84], outline=INK, width=2, fill=(250, 247, 240))
    for i, r in enumerate([6, 5, 4, 3, 2]):
        d.ellipse([x0 + 22 + i * 34 - r, y0 + 30 - r, x0 + 22 + i * 34 + r, y0 + 30 + r], fill=INK)
    glyphword(d, x0 + 16, y0 + 70, rng, n=7)
    north(d, f, label="")  # arrow with no label
    im.save(f"{OUT}/c_replaced.png")

def map_d():
    im, d = sheet_base()
    f = ImageFont.truetype(FONT, 15)
    rng = random.Random(41)
    # self-crossing "coastline"
    pts = []
    for a in range(0, 720, 24):
        t = math.radians(a)
        rr = 120 + 60 * math.sin(2.7 * t) + rng.randint(-12, 12)
        pts.append((320 + rr * math.cos(t * 0.7), 280 + rr * math.sin(t * 0.83)))
    d.line(pts, fill=INK, width=3, joint="curve")
    # "contours" that intersect each other
    for k in range(3):
        cpts = []
        for a in range(0, 360, 20):
            t = math.radians(a)
            rr = 60 + k * 28 + 22 * math.sin((3 + k) * t + k)
            cpts.append((300 + rr * math.cos(t), 300 + rr * math.sin(t)))
        cpts.append(cpts[0])
        d.line(cpts, fill=(140, 132, 118), width=2, joint="curve")
    # a line that changes style mid-stroke
    seg = [(140, 480), (240, 430), (350, 460), (460, 420)]
    d.line(seg[:2], fill=INK, width=4)
    x0, y0 = seg[1]; x1, y1 = seg[2]
    for s in range(0, 10, 2):
        d.line([(x0 + (x1 - x0) * s / 10, y0 + (y1 - y0) * s / 10),
                (x0 + (x1 - x0) * (s + 1) / 10, y0 + (y1 - y0) * (s + 1) / 10)], fill=INK, width=4)
    for s in range(0, 12, 3):
        xx = seg[2][0] + (seg[3][0] - seg[2][0]) * s / 12
        yy = seg[2][1] + (seg[3][1] - seg[2][1]) * s / 12
        d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill=INK)
    # labels with leaders pointing at nothing
    for lx, ly, ex, ey in [(150, 130, 210, 180), (470, 140, 420, 200), (500, 360, 450, 330)]:
        glyphword(d, lx, ly, rng)
        d.line([(lx + 18, ly + 4), (ex, ey)], fill=(140, 132, 118), width=1)
    # legend keyed to symbols that appear nowhere
    x0, y0 = SHEET[0] + 22, SHEET[3] - 130
    d.rectangle([x0, y0, x0 + 170, y0 + 104], outline=INK, width=2, fill=(250, 247, 240))
    for i in range(3):
        yy = y0 + 22 + i * 28
        if i == 0:
            d.polygon([(x0 + 24, yy - 7), (x0 + 17, yy + 6), (x0 + 31, yy + 6)], outline=INK)
        elif i == 1:
            d.line([(x0 + 16, yy), (x0 + 32, yy)], fill=INK, width=2)
            d.line([(x0 + 24, yy - 8), (x0 + 24, yy + 8)], fill=INK, width=2)
        else:
            d.ellipse([x0 + 18, yy - 6, x0 + 30, yy + 6], outline=INK, width=2)
        glyphword(d, x0 + 44, yy + 7, rng, n=4)
    # non-monotonic scale bar with glyph units
    x0, y0 = SHEET[2] - 200, SHEET[3] - 44
    d.line([(x0, y0), (x0 + 140, y0)], fill=INK, width=3)
    for i, xx in enumerate([x0, x0 + 40, x0 + 65, x0 + 140]):
        d.line([(xx, y0 - 6), (xx, y0 + 6)], fill=INK, width=3)
    glyphword(d, x0 + 4, y0 + 24, rng, n=3)
    glyphword(d, x0 + 84, y0 + 24, rng, n=2)
    # five-armed uneven compass rose, two arms same glyph
    cx, cy = SHEET[2] - 70, SHEET[1] + 80
    for a in [0, 80, 150, 220, 305]:
        t = math.radians(a - 90)
        d.line([(cx, cy), (cx + 34 * math.cos(t), cy + 34 * math.sin(t))], fill=INK, width=3)
        d.polygon([(cx + 42 * math.cos(t), cy + 42 * math.sin(t)),
                   (cx + 30 * math.cos(t) - 6 * math.sin(t), cy + 30 * math.sin(t) + 6 * math.cos(t)),
                   (cx + 30 * math.cos(t) + 6 * math.sin(t), cy + 30 * math.sin(t) - 6 * math.cos(t))],
                  fill=INK)
    glyphword(d, cx - 30, cy - 48, rng, n=2)
    glyphword(d, cx + 18, cy + 58, rng, n=2)
    im.save(f"{OUT}/d_boundary.png")

if __name__ == "__main__":
    map_a(); map_b(); map_c(); map_d()
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_control", "b_damaged", "c_replaced", "d_boundary"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
