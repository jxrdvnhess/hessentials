# Sketch 301 — A1: twenty images that invite classification while resisting it.
# Each generator = one instability mechanism. Run: python3 generate.py
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (32, 29, 26)

def paper():
    base = np.full((H, W, 3), (244, 239, 229), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    img = np.clip(base + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(img, "RGB")

def canvas():
    im = paper()
    return im, ImageDraw.Draw(im)

def save(im, n):
    im.save(f"{OUT}/img{n:02d}.png")

def bez(p0, p1, p2, steps=60):
    return [(
        (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],
    ) for t in (i / steps for i in range(steps + 1))]

def thickline(d, pts, w):
    d.line(pts, fill=INK, width=w, joint="curve")

# 01 — one oval, two conflicting attachments (grown stem + manufactured string)
def img01():
    im, d = canvas()
    d.ellipse([225, 330, 415, 480], fill=INK)
    thickline(d, [(40, 80), (60, 92), (110, 98), (170, 96)], 14)  # bough
    thickline(d, bez((168, 96), (260, 150), (300, 336)), 7)       # curved stem
    d.line([(470, 0), (470, 300)], fill=INK, width=3)             # taut string
    d.line([(470, 300), (392, 352)], fill=INK, width=3)
    d.ellipse([464, 294, 478, 308], outline=INK, width=3)         # loop
    save(im, 1)

# 02 — figure/ground: two dark forms, gap shaped like a vessel
def img02():
    im, d = canvas()
    def profile(y):  # half-width of the gap at height y
        t = (y - 100) / 440
        if t < 0.35: return 95 - 60 * (t / 0.35) ** 1.4   # bowl
        if t < 0.8:  return 22 + 6 * math.sin(t * 9)      # stem
        return 22 + 90 * ((t - 0.8) / 0.2) ** 1.6         # foot
    L, R = [], []
    for y in range(100, 540, 4):
        p = profile(y)
        L.append((320 - p, y)); R.append((320 + p, y))
    left = [(110, 140), (150, 100)] + L + [(170, 560), (95, 545)]
    right = [(530, 140), (490, 100)] + [(x, y) for x, y in R] + [(470, 560), (545, 545)]
    d.polygon(left, fill=INK); d.polygon(right, fill=INK)
    save(im, 2)

# 03 — cracked cells, no scale cue
def img03():
    rng = np.random.default_rng(31)
    seeds = rng.uniform(0, W, (60, 2))
    yy, xx = np.mgrid[0:H, 0:W]
    pts = np.stack([xx.ravel(), yy.ravel()], 1).astype(np.float32)
    d2 = ((pts[:, None, :] - seeds[None, :, :]) ** 2).sum(-1)
    part = np.partition(d2, 1, axis=1)
    edge = (np.sqrt(part[:, 1]) - np.sqrt(part[:, 0])).reshape(H, W)
    idx = np.argmin(d2, axis=1).reshape(H, W)
    tint = 232 + (idx * 37 % 13) - 6
    img = np.stack([tint + 8, tint + 2, tint - 10], -1).astype(np.float32)
    img[edge < 1.6] = (60, 52, 44)
    img[(edge >= 1.6) & (edge < 3.2)] = (150, 138, 122)
    save(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)), 3)

# 04 — a confident handle on a nameless mass
def img04():
    im, d = canvas()
    for cx, cy, r in [(290, 390, 120), (380, 430, 90), (250, 460, 80), (350, 330, 70)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    ang = math.radians(-40)
    hx, hy = 392, 312
    ex, ey = hx + 190 * math.cos(ang), hy + 190 * math.sin(ang)
    d.line([(hx, hy), (ex, ey)], fill=INK, width=34)
    d.ellipse([ex - 17, ey - 17, ex + 17, ey + 17], fill=INK)
    nx, ny = -math.sin(ang), math.cos(ang)
    for t in (0.45, 0.58, 0.71, 0.84):
        px, py = hx + (ex - hx) * t, hy + (ey - hy) * t
        d.line([(px - nx * 19, py - ny * 19), (px + nx * 19, py + ny * 19)],
               fill=(244, 239, 229), width=4)
    save(im, 4)

# 05 — only the cast shadow; caster out of frame
def img05():
    im = paper()
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    body = [(640, 420), (560, 400), (470, 392), (380, 398), (300, 412),
            (240, 408), (200, 390), (150, 396), (120, 412), (160, 428),
            (220, 430), (270, 442), (200, 452), (160, 470), (230, 472),
            (320, 458), (420, 452), (520, 448), (640, 460)]
    d.polygon(body, fill=120)
    d.ellipse([60, 392, 130, 440], outline=120, width=16)  # loop in the shadow
    d.polygon([(330, 398), (300, 330), (318, 326), (352, 396)], fill=120)  # prong
    d.polygon([(420, 396), (412, 318), (430, 316), (446, 396)], fill=120)
    lay = lay.filter(ImageFilter.GaussianBlur(5))
    grey = Image.new("RGB", (W, H), (120, 112, 102))
    im.paste(grey, (0, 0), lay)
    save(im, 5)

# 06 — bilateral symmetry: organic curve, mechanical regularity
def img06():
    im, d = canvas()
    thickline(d, [(320, 90), (320, 540)], 16)
    for i in range(5):
        y = 150 + i * 80
        reach = 170 - i * 22
        for s in (-1, 1):
            pts = bez((320, y), (320 + s * reach * 0.9, y - 36), (320 + s * reach, y + 26))
            thickline(d, pts, 11 - i)
            tx, ty = pts[-1]
            r = 11 - i
            d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=INK)
    d.polygon([(304, 540), (336, 540), (320, 588)], fill=INK)
    save(im, 6)

# 07 — three relational marks (arc, ear, folded leg), rotated 90°
def img07():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    arc = bez((120, 380), (250, 180), (520, 360))
    d.line(arc, fill=INK + (255,), width=12, joint="curve")
    d.ellipse([150, 300, 215, 345], fill=INK + (255,))  # ear mass
    leg = [(360, 372), (300, 420), (430, 420), (470, 392)]
    d.line(leg, fill=INK + (255,), width=10, joint="curve")
    lay = lay.rotate(90, expand=False)
    im = paper(); im.paste(lay, (0, 0), lay)
    save(im, 7)

# 08 — regular dot field with one vortex of disorder
def img08():
    im, d = canvas()
    cx, cy = 360, 300
    for gy in range(40, 620, 26):
        for gx in range(40, 620, 26):
            dx, dy = gx - cx, gy - cy
            r = math.hypot(dx, dy)
            f = math.exp(-(r / 130) ** 2)
            a = math.atan2(dy, dx) + 2.4 * f
            rr = r * (1 - 0.35 * f)
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            s = 3.4 + 4.5 * f
            d.ellipse([x - s, y - s, x + s, y + s], fill=INK)
    save(im, 8)

# 09 — one silhouette built halfway between two objects
def img09():
    im, d = canvas()
    d.ellipse([200, 280, 460, 500], fill=INK)  # body
    neck = bez((230, 330), (130, 240), (150, 150))
    neck2 = bez((180, 165), (175, 250), (270, 310))
    d.polygon(neck + neck2[::-1] + [neck[0]], fill=INK)
    d.polygon([(150, 150), (118, 128), (152, 116), (180, 165)], fill=INK)  # tip
    d.ellipse([430, 290, 560, 410], outline=INK, width=22)  # loop
    d.polygon([(280, 495), (380, 495), (400, 545), (260, 545)], fill=INK)  # base
    save(im, 9)

# 10 — a page of writing in no script
def img10():
    im, d = canvas()
    rng = random.Random(10)
    def glyph(d, x, y, h):
        k = rng.randint(2, 4)
        w = 0
        for _ in range(k):
            s = rng.choice("vhad")
            if s == "v":
                d.line([(x + w, y - h), (x + w + rng.randint(-3, 3), y)], fill=INK, width=3)
                w += 8
            elif s == "h":
                yy = y - rng.choice((h, h // 2, 0))
                d.line([(x + w - 6, yy), (x + w + 8, yy)], fill=INK, width=3)
                w += 6
            elif s == "a":
                d.arc([x + w - 2, y - h, x + w + 16, y], rng.choice((0, 90, 180)),
                      rng.choice((270, 360)), fill=INK, width=3)
                w += 14
            else:
                d.ellipse([x + w + 2, y - h - 8, x + w + 7, y - h - 3], fill=INK)
                w += 4
        return max(w, 10)
    for line in range(5):
        y = 150 + line * 85
        x = 80
        while x < 520:
            for _ in range(rng.randint(2, 6)):
                if x > 540: break
                x += glyph(d, x, y, rng.choice((26, 30, 34))) + 5
            x += 26
    save(im, 10)

# 11 — handle says tool; head refuses to say which
def img11():
    im, d = canvas()
    d.rounded_rectangle([296, 300, 344, 560], 22, fill=INK)
    for yy in range(330, 545, 26):  # grain
        d.line([(305, yy), (335, yy + 12)], fill=(244, 239, 229), width=2)
    d.rectangle([288, 282, 352, 308], fill=(110, 100, 90))  # band
    d.ellipse([240, 110, 400, 296], fill=(150, 140, 128))   # head
    for i in range(9):  # mesh on upper half
        d.arc([240, 110 + i * 9, 400, 296 - i * 9], 180, 360, fill=(60, 54, 48), width=2)
    for i in range(7):
        x = 252 + i * 22
        d.line([(x, 132), (x, 200)], fill=(60, 54, 48), width=2)
    d.line([(240, 203), (400, 203)], fill=(60, 54, 48), width=4)
    save(im, 11)

# 12 — matte form, molded seam, hard star highlight, fuzzed edge
def img12():
    im = paper()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy, R = 320, 330, 170
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    sphere = r < R
    lam = np.clip(1 - r / R, 0, 1) ** 0.7
    arr = np.array(im, dtype=np.float32)
    shade = np.stack([120 + 90 * lam, 105 + 85 * lam, 88 + 78 * lam], -1)
    arr[sphere] = shade[sphere]
    im = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.arc([cx - R, cy - R * 0.55, cx + R, cy + R * 0.55], 10, 170, fill=(70, 62, 54), width=3)
    sx, sy = 255, 245  # star highlight
    for a, ln in [(0, 34), (90, 34), (45, 14), (135, 14)]:
        t = math.radians(a)
        d.line([(sx - ln * math.cos(t), sy - ln * math.sin(t)),
                (sx + ln * math.cos(t), sy + ln * math.sin(t))], fill=(252, 250, 244), width=5)
    rng = random.Random(12)
    for _ in range(260):  # fuzz
        a = rng.uniform(0, 6.283)
        x0, y0 = cx + R * math.cos(a), cy + R * math.sin(a)
        d.line([(x0, y0), (x0 + 9 * math.cos(a + rng.uniform(-.5, .5)),
                           y0 + 9 * math.sin(a + rng.uniform(-.5, .5)))], fill=(90, 80, 70), width=1)
    d.ellipse([cx - 130, cy + R - 6, cx + 130, cy + R + 38], fill=(205, 198, 186))
    save(im, 12)

# 13 — a framed luminous rectangle
def img13():
    im, d = canvas()
    f = 36
    d.rectangle([120, 90, 520, 550], fill=INK)
    for y in range(90 + f, 550 - f):
        t = (y - 126) / 388
        col = (int(250 - 60 * t), int(244 - 80 * t), int(228 - 95 * t))
        d.line([(120 + f, y), (520 - f, y)], fill=col)
    d.line([(120 + f, 395), (520 - f, 395)], fill=(170, 150, 128), width=2)
    d.ellipse([200, 170, 250, 220], fill=(252, 248, 236))
    for c in [(120, 90), (520, 90), (120, 550), (520, 550)]:  # mitres
        d.line([c, (c[0] + (f if c[0] == 120 else -f), c[1] + (f if c[1] == 90 else -f))],
               fill=(90, 82, 72), width=2)
    save(im, 13)

# 14 — thin verticals carrying masses
def img14():
    im, d = canvas()
    rng = random.Random(14)
    x = 60
    while x < 600:
        h = rng.randint(130, 210)
        base = 470 + rng.randint(-8, 8)
        d.ellipse([x - 16, base - 5, x + 16, base + 7], fill=(214, 206, 192))
        d.line([(x, base), (x + rng.randint(-6, 6), base - h)], fill=INK, width=3)
        tx, ty = x + rng.randint(-6, 6), base - h
        for _ in range(rng.randint(3, 6)):
            r = rng.randint(9, 18)
            ox, oy = rng.randint(-16, 16), rng.randint(-14, 8)
            d.ellipse([tx + ox - r, ty + oy - r, tx + ox + r, ty + oy + r], fill=INK)
        x += rng.randint(38, 52)
    save(im, 14)

# 15 — one heavy contour that never closes
def img15():
    im, d = canvas()
    pts = []
    pts += bez((150, 470), (130, 320), (250, 260), 40)   # rise
    pts += bez((250, 260), (340, 215), (420, 265), 40)   # hump
    pts += bez((420, 265), (470, 295), (475, 250), 30)   # dip up
    pts += bez((475, 250), (520, 215), (545, 265), 30)   # small round protrusion
    pts += bez((545, 265), (575, 330), (540, 420), 40)   # descend
    pts += bez((540, 420), (480, 480), (350, 478), 40)   # along bottom
    pts += bez((350, 478), (260, 478), (225, 455), 30)   # heel curve, then GAP
    thickline(d, pts, 13)
    save(im, 15)

# 16 — dark patches sharing one invisible straight-edged absence
def img16():
    lay = Image.new("RGB", (W, H), (244, 239, 229))
    d = ImageDraw.Draw(lay)
    rng = random.Random(16)
    for _ in range(11):
        cx, cy = rng.randint(80, 560), rng.randint(80, 560)
        blob = []
        for a in range(0, 360, 30):
            r = rng.randint(34, 78)
            blob.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
        d.polygon(blob, fill=INK)
    hole = [(250, 180), (420, 150), (500, 300), (430, 470), (270, 490), (180, 330)]
    d.polygon(hole, fill=(244, 239, 229))
    save(lay, 16)

# 17 — a tube shaded against itself
def img17():
    im, d = canvas()
    path = bez((110, 460), (240, 140), (380, 320), 50) + bez((380, 320), (480, 460), (560, 220), 50)
    n = len(path)
    for i in range(0, n - 1):
        x0, y0 = path[i]; x1, y1 = path[i + 1]
        ang = math.atan2(y1 - y0, x1 - x0)
        nx, ny = -math.sin(ang), math.cos(ang)
        for k in range(-28, 29, 2):
            t = abs(k) / 28
            tone = 70 + 150 * (1 - t) if i < n // 2 else 70 + 150 * t
            c = (int(tone), int(tone * 0.93), int(tone * 0.84))
            d.line([(x0 + nx * k, y0 + ny * k), (x1 + nx * k, y1 + ny * k)], fill=c, width=4)
    save(im, 17)

# 18 — boundary, nodes, connectors, ticks
def img18():
    im, d = canvas()
    rng = random.Random(18)
    pts = []
    for a in range(0, 360, 4):
        t = math.radians(a)
        r = 200 + 60 * math.sin(3 * t + 1) + 28 * math.sin(7 * t) + rng.uniform(-6, 6)
        pts.append((320 + r * math.cos(t), 320 + 0.85 * r * math.sin(t)))
    pts.append(pts[0])
    d.line(pts, fill=INK, width=3, joint="curve")
    for i in range(0, 90, 4):  # ticks on one stretch
        x, y = pts[i]; x2, y2 = pts[i + 1]
        nx, ny = -(y2 - y), (x2 - x)
        L = math.hypot(nx, ny) or 1
        d.line([(x, y), (x + 9 * nx / L, y + 9 * ny / L)], fill=INK, width=2)
    nodes = [(rng.randint(120, 520), rng.randint(120, 520)) for _ in range(12)]
    for i, (x, y) in enumerate(nodes):
        if i % 3 == 0:
            d.rectangle([x - 6, y - 6, x + 6, y + 6], fill=INK)
        else:
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=INK)
    for i in range(0, 10, 2):
        d.line([nodes[i], nodes[i + 1]], fill=(120, 110, 98), width=2)
    a, b = nodes[3], nodes[8]  # one dashed connector
    steps = 14
    for s in range(0, steps, 2):
        x0 = a[0] + (b[0] - a[0]) * s / steps; y0 = a[1] + (b[1] - a[1]) * s / steps
        x1 = a[0] + (b[0] - a[0]) * (s + 1) / steps; y1 = a[1] + (b[1] - a[1]) * (s + 1) / steps
        d.line([(x0, y0), (x1, y1)], fill=(120, 110, 98), width=2)
    save(im, 18)

# 19 — ridges without a horizon
def img19():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) / W
    warp = 0.25 * np.sin(3 * yy + 1.2) + 0.15 * np.sin(7 * xx * yy + 2)
    field = np.sin((xx * 6 + warp) * math.pi) * 0.5 + 0.5
    ridge = np.abs(field - 0.5) * 2
    gx = np.gradient(ridge, axis=1)
    light = np.clip(0.55 - gx * 9, 0, 1) ** 1.2
    arr = np.stack([90 + 140 * light, 82 + 132 * light, 70 + 120 * light], -1)
    save(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), 19)

# 20 — the presentation says LOOK; the object refuses to answer
def img20():
    im = Image.new("RGB", (W, H), (52, 47, 42))
    d = ImageDraw.Draw(im)
    for r in range(420, 80, -8):  # spotlight pool
        a = int(8 + 60 * (1 - r / 420))
        d.ellipse([320 - r, 430 - r * 0.42, 320 + r, 430 + r * 0.42],
                  fill=(52 + a, 47 + a, 42 + int(a * 0.9)))
    d.polygon([(230, 430), (410, 430), (400, 560), (240, 560)], fill=(168, 160, 148))  # plinth front
    d.polygon([(230, 430), (410, 430), (430, 405), (250, 405)], fill=(200, 192, 178))  # plinth top
    d.ellipse([285, 392, 385, 420], fill=(120, 112, 102))  # soft shadow
    for cx, cy, rx, ry in [(315, 380, 38, 26), (350, 368, 30, 22), (330, 352, 22, 18)]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(88, 78, 66))
    d.polygon([(352, 352), (390, 322), (398, 334), (362, 362)], fill=(88, 78, 66))  # protrusion
    d.ellipse([320, 358, 334, 368], fill=(140, 128, 112))  # sheen
    save(im, 20)

if __name__ == "__main__":
    for i in range(1, 21):
        globals()[f"img{i:02d}"]()
    print("done")
