# Sketch 301 — A13: System Replacement. Playing cards only.
# A: 7 of clubs (control). B: 15 of clubs (rank overflow). C: 7 of crescents
# (foreign suit). D: an arcana-shaped card (Roman numeral XXI, central emblem, banner).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 640, 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def ground():
    base = np.full((H, W, 3), (226, 219, 207), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.5, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

CARD = (170, 90, 470, 550)  # card rect

def card_base():
    im = ground(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([CARD[0] + 6, CARD[1] + 8, CARD[2] + 6, CARD[3] + 8], 22,
                        fill=(196, 188, 174))  # shadow
    d.rounded_rectangle(CARD, 22, fill=(250, 247, 240), outline=(160, 152, 138), width=2)
    return im, d

def club(d, x, y, s):
    for ox, oy in [(0, -s * 0.55), (-s * 0.52, 0.18 * s), (s * 0.52, 0.18 * s)]:
        d.ellipse([x + ox - s * 0.42, y + oy - s * 0.42, x + ox + s * 0.42, y + oy + s * 0.42],
                  fill=INK)
    d.polygon([(x - s * 0.16, y + s * 0.1), (x + s * 0.16, y + s * 0.1),
               (x + s * 0.3, y + s * 0.95), (x - s * 0.3, y + s * 0.95)], fill=INK)

def crescent(d, x, y, s):
    d.ellipse([x - s * 0.7, y - s * 0.7, x + s * 0.7, y + s * 0.7], fill=INK)
    d.ellipse([x - s * 0.7 + s * 0.45, y - s * 0.7 - s * 0.12,
               x + s * 0.7 + s * 0.45, y + s * 0.7 - s * 0.12], fill=(250, 247, 240))

def index(d, text, pip, s=22):
    f = ImageFont.truetype(FONT, 40)
    d.text((CARD[0] + 34, CARD[1] + 38), text, font=f, fill=INK, anchor="mm")
    pip(d, CARD[0] + 34, CARD[1] + 84, s)
    d.text((CARD[2] - 34, CARD[3] - 38), text, font=f, fill=INK, anchor="mm")
    pip(d, CARD[2] - 34, CARD[3] - 84, s)

def pip_layout(n):
    cx = (CARD[0] + CARD[2]) / 2
    xs = [cx - 75, cx, cx + 75]
    if n == 7:
        return [(xs[0], 180), (xs[2], 180), (cx, 240), (xs[0], 320),
                (xs[2], 320), (xs[0], 460), (xs[2], 460)]
    if n == 15:
        pts = []
        for r in range(5):
            for c in range(3):
                pts.append((xs[c], 160 + r * 80))
        return pts
    return []

def card_a():
    im, d = card_base()
    index(d, "7", club)
    for x, y in pip_layout(7):
        club(d, x, y, 26)
    im.save(f"{OUT}/a_seven_clubs.png")

def card_b():
    im, d = card_base()
    index(d, "15", club)
    for x, y in pip_layout(15):
        club(d, x, y, 21)
    im.save(f"{OUT}/b_fifteen_clubs.png")

def card_c():
    im, d = card_base()
    index(d, "7", crescent)
    for x, y in pip_layout(7):
        crescent(d, x, y, 26)
    im.save(f"{OUT}/c_seven_crescents.png")

def card_d():
    im, d = card_base()
    f = ImageFont.truetype(FONT, 40)
    d.text((CARD[0] + 44, CARD[1] + 38), "XXI", font=f, fill=INK, anchor="mm")
    d.text((CARD[2] - 44, CARD[3] - 38), "XXI", font=f, fill=INK, anchor="mm")
    d.rounded_rectangle([CARD[0] + 28, CARD[1] + 70, CARD[2] - 28, CARD[3] - 110], 10,
                        outline=INK, width=3)
    cx, cy = (CARD[0] + CARD[2]) / 2, 290
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=INK)
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(250, 247, 240))
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=INK)
    for a in range(0, 360, 30):  # rays
        t = math.radians(a)
        d.line([(cx + 78 * math.cos(t), cy + 78 * math.sin(t)),
                (cx + 102 * math.cos(t), cy + 102 * math.sin(t))], fill=INK, width=5)
    d.rectangle([CARD[0] + 52, 440, CARD[2] - 52, 478], outline=INK, width=3)  # banner
    rng = random.Random(13)  # asemic banner glyphs
    x = CARD[0] + 66
    while x < CARD[2] - 70:
        h = rng.randint(10, 18)
        d.line([(x, 470), (x + rng.randint(-2, 3), 470 - h)], fill=INK, width=2)
        if rng.random() < 0.4:
            d.line([(x - 3, 462), (x + 5, 462)], fill=INK, width=2)
        x += rng.randint(8, 13)
    im.save(f"{OUT}/d_arcana.png")

if __name__ == "__main__":
    card_a(); card_b(); card_c(); card_d()
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_seven_clubs", "b_fifteen_clubs", "c_seven_crescents", "d_arcana"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
