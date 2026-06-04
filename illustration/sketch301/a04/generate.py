# Sketch 301 — A4: one key, three intents.
# A: identify as fast as possible. B: correctly but as late as possible.
# C: never settles — ambiguity through representation, form undistorted.
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (32, 29, 26)
PAPER = (244, 239, 229)

def paper():
    base = np.full((H, W, 3), PAPER, dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

TEETH = [(0, 26), (18, 26), (18, 12), (34, 12), (34, 26), (52, 26), (52, 6),
         (66, 6), (66, 26), (84, 26), (84, 16), (98, 16), (98, 0)]  # serration profile

# A — the instant key: canonical orientation, silhouette, naming feature loud
def key_a():
    im = paper(); d = ImageDraw.Draw(im)
    cy = 320
    d.ellipse([80, cy - 75, 230, cy + 75], fill=INK)            # bow
    d.ellipse([125, cy - 32, 189, cy + 32], fill=PAPER)         # hole
    d.rectangle([220, cy - 22, 545, cy + 22], fill=INK)         # shaft
    base = 545
    pts = [(base - 98 + x, cy + 22 + y * 1.6) for x, y in TEETH]  # teeth, down, near tip
    d.polygon([(base - 98, cy + 22)] + pts + [(base, cy + 22)], fill=INK)
    d.polygon([(545, cy - 22), (560, cy - 14), (560, cy + 14), (545, cy + 22)], fill=INK)
    im.save(f"{OUT}/key_a.png")

# B — the late key: vertical, bow-dominant, low contrast, naming feature last in reading order
def key_b():
    im = paper()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    TONE = (172, 163, 150, 255)       # low contrast against paper
    DEEP = (148, 139, 127, 255)
    cx = 320
    # large bow first in reading order (top), as an abstract ring
    d.ellipse([cx - 150, 60, cx + 150, 360], fill=TONE)
    d.ellipse([cx - 86, 124, cx + 86, 296], fill=PAPER + (255,))
    d.ellipse([cx - 150, 60, cx + 150, 360], outline=DEEP, width=3)
    d.ellipse([cx - 86, 124, cx + 86, 296], outline=DEEP, width=3)
    # shaft descends
    d.polygon([(cx - 26, 352), (cx + 26, 352), (cx + 20, 560), (cx - 20, 560)], fill=TONE)
    # accurate serration, small, low, same tone — present, last
    pts = [(cx - 20 + x * 0.62, 560 - y * 1.05) for x, y in TEETH]
    d.polygon([(cx - 20, 560)] + pts + [(cx + 20, 560), (cx + 20, 520), (cx - 20, 520)], fill=TONE)
    d.line([(p[0], p[1]) for p in pts], fill=DEEP, width=2, joint="curve")
    # soft interior shading on the bow (slow texture)
    sh = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(sh)
    ds.ellipse([cx - 150, 60, cx + 30, 300], fill=44)
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    dark = Image.new("RGBA", (W, H), (120, 112, 100, 255))
    lay.paste(dark, (0, 0), Image.composite(sh, Image.new("L", (W, H), 0),
                                            lay.split()[3]))
    im.paste(lay, (0, 0), lay)
    im.save(f"{OUT}/key_b.png")

# C — the unsettled key: exact key form; each region in a different representational mode
def key_c():
    im = paper(); d = ImageDraw.Draw(im)
    rng = random.Random(4)
    cx = 320
    # bow: organic mode — soft tonal disc, fuzzed edge, faint section hatching
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt((xx - cx) ** 2 + (yy - 210) ** 2)
    arr = np.array(im, dtype=np.float32)
    m = r < 145
    lam = np.clip(1 - r / 145, 0, 1) ** 0.8
    arr[m] = np.stack([150 + 70 * lam, 138 + 64 * lam, 120 + 58 * lam], -1)[m]
    im = Image.fromarray(arr.astype(np.uint8)); d = ImageDraw.Draw(im)
    d.ellipse([cx - 62, 152, cx + 62, 268], fill=PAPER)   # the hole, kept (form intact)
    for _ in range(220):                                   # fuzz on the bow edge
        a = rng.uniform(0, 6.283)
        x0, y0 = cx + 145 * math.cos(a), 210 + 145 * math.sin(a)
        d.line([(x0, y0), (x0 + 8 * math.cos(a), y0 + 8 * math.sin(a))],
               fill=(110, 98, 86), width=1)
    for i in range(-4, 5):                                 # faint section hatching
        y = 210 + i * 26
        if abs(i) * 26 < 140:
            half = math.sqrt(145 ** 2 - (y - 210) ** 2)
            d.line([(cx - half + 6, y), (cx + half - 6, y)], fill=(125, 113, 99), width=1)
    # shaft: machine mode — hard cylinder, crisp specular band
    d.polygon([(cx - 24, 348), (cx + 24, 348), (cx + 19, 552), (cx - 19, 552)],
              fill=(96, 88, 78))
    d.polygon([(cx - 12, 349), (cx - 5, 349), (cx - 7, 552), (cx - 13, 552)],
              fill=(190, 182, 168))
    # teeth: diagram mode — thin dashed outline only, unfilled, accurate profile
    pts = [(cx - 19 + x * 0.62, 552 + (26 - y) * 1.05) for x, y in TEETH]
    seq = [(cx - 19, 552)] + pts + [(cx + 19, 552)]
    for i in range(len(seq) - 1):
        x0, y0 = seq[i]; x1, y1 = seq[i + 1]
        steps = max(2, int(math.hypot(x1 - x0, y1 - y0) / 7))
        for s in range(0, steps, 2):
            d.line([(x0 + (x1 - x0) * s / steps, y0 + (y1 - y0) * s / steps),
                    (x0 + (x1 - x0) * (s + 1) / steps, y0 + (y1 - y0) * (s + 1) / steps)],
                   fill=(70, 62, 54), width=2)
    # one diagram leader line, unlabeled but lettered
    d.line([(cx + 138, 150), (cx + 215, 110)], fill=(70, 62, 54), width=2)
    d.ellipse([cx + 134, 146, cx + 142, 154], fill=(70, 62, 54))
    d.text((cx + 220, 100), "a.", fill=(70, 62, 54))
    im.save(f"{OUT}/key_c.png")

if __name__ == "__main__":
    key_a(); key_b(); key_c(); print("done")
