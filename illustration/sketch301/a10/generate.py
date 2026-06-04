# Sketch 301 — A10: the search for inventory.
# Three structures that declare their own contents, each minus one member, each with control.
# Series: a clock face missing its 7. Lattice: a shelf row with one empty slot.
# Symmetry: a moth missing one wing.
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def ground():
    base = np.full((H, W, 3), (240, 234, 222), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.4, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

# --- series: clock ---
def clock(missing=None):
    im = ground(); d = ImageDraw.Draw(im)
    cx, cy, R = 320, 320, 240
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=INK, width=8)
    f = ImageFont.truetype(FONT, 44)
    for n in range(1, 13):
        if n == missing:
            continue
        a = math.radians(n * 30 - 90)
        x, y = cx + (R - 52) * math.cos(a), cy + (R - 52) * math.sin(a)
        d.text((x, y), str(n), font=f, fill=INK, anchor="mm")
    for n in range(1, 13):  # minute ticks at hours
        a = math.radians(n * 30 - 90)
        d.line([(cx + (R - 14) * math.cos(a), cy + (R - 14) * math.sin(a)),
                (cx + (R - 28) * math.cos(a), cy + (R - 28) * math.sin(a))], fill=INK, width=5)
    ah = math.radians(10 * 30 - 90 + 15)  # ~10:30 hour hand
    d.line([(cx, cy), (cx + 110 * math.cos(ah), cy + 110 * math.sin(ah))], fill=INK, width=12)
    am = math.radians(6 * 30 - 90)        # minute hand at 6
    d.line([(cx, cy), (cx + 170 * math.cos(am), cy + 170 * math.sin(am))], fill=INK, width=8)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=INK)
    return im

# --- lattice: shelf row ---
def bottle(d, x, base_y):
    d.polygon([(x - 26, base_y), (x - 26, base_y - 80), (x - 10, base_y - 104),
               (x - 10, base_y - 132), (x + 10, base_y - 132), (x + 10, base_y - 104),
               (x + 26, base_y - 80), (x + 26, base_y)], fill=INK)
    d.rectangle([x - 12, base_y - 146, x + 12, base_y - 132], fill=INK)

def shelf(gap_slot=None, n=None):
    im = ground(); d = ImageDraw.Draw(im)
    d.line([(60, 420), (580, 420)], fill=(150, 140, 124), width=6)
    if gap_slot:  # six slots, one empty
        xs = [95 + i * 90 for i in range(6)]
        for i, x in enumerate(xs, 1):
            if i != gap_slot:
                bottle(d, x, 418)
    else:         # five bottles, evenly spaced, no gap
        xs = [110 + i * 105 for i in range(5)]
        for x in xs:
            bottle(d, x, 418)
    return im

# --- symmetry: moth ---
def wing(d, cx, cy, side):
    s = 1 if side == "r" else -1
    d.polygon([(cx + s * 16, cy - 60), (cx + s * 170, cy - 130), (cx + s * 205, cy - 70),
               (cx + s * 150, cy - 10), (cx + s * 16, cy - 10)], fill=INK)   # forewing
    d.polygon([(cx + s * 16, cy), (cx + s * 140, cy + 30), (cx + s * 120, cy + 95),
               (cx + s * 30, cy + 60), (cx + s * 16, cy + 10)], fill=INK)    # hindwing
    d.ellipse([cx + s * 60 - 14, cy - 92, cx + s * 60 + 14, cy - 64], fill=(240, 234, 222))  # spot

def moth(wings="lr"):
    im = ground(); d = ImageDraw.Draw(im)
    cx, cy = 320, 330
    if "l" in wings: wing(d, cx, cy, "l")
    if "r" in wings: wing(d, cx, cy, "r")
    d.ellipse([cx - 16, cy - 70, cx + 16, cy + 80], fill=INK)  # body
    for s in (-1, 1):  # antennae
        pts = [(cx + s * 6, cy - 68)]
        for t in range(1, 11):
            pts.append((cx + s * (6 + t * 7), cy - 68 - t * 9 + (t * t) * 0.35))
        d.line(pts, fill=INK, width=4)
    return im

if __name__ == "__main__":
    clock(missing=7).save(f"{OUT}/s1_clock_no7.png")
    clock().save(f"{OUT}/s1c_clock_full.png")
    shelf(gap_slot=4).save(f"{OUT}/s2_shelf_gap.png")
    shelf().save(f"{OUT}/s2c_shelf_full.png")
    moth(wings="l").save(f"{OUT}/s3_moth_onewing.png")
    moth().save(f"{OUT}/s3c_moth_full.png")
    names = ["s1_clock_no7", "s1c_clock_full", "s2_shelf_gap",
             "s2c_shelf_full", "s3_moth_onewing", "s3c_moth_full"]
    sheet = Image.new("RGB", (3 * 440, 2 * 440), (255, 255, 255))
    for k, n in enumerate(names):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((430, 430)),
                    ((k % 3) * 440 + 5, (k // 3) * 440 + 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
