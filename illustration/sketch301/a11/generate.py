# Sketch 301 — A11: Resisting Presence. The clock only.
# A control / B absence (7 removed) / C smudge in the 7 slot / D wrong-but-legible "13".
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def ground():
    base = np.full((H, W, 3), (240, 234, 222), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.4, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def slot_xy(n, cx=320, cy=320, R=240):
    a = math.radians(n * 30 - 90)
    return cx + (R - 52) * math.cos(a), cy + (R - 52) * math.sin(a)

def clock(seven="normal"):
    im = ground(); d = ImageDraw.Draw(im)
    cx, cy, R = 320, 320, 240
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=INK, width=8)
    f = ImageFont.truetype(FONT, 44)
    for n in range(1, 13):
        x, y = slot_xy(n)
        if n == 7:
            if seven == "normal":
                d.text((x, y), "7", font=f, fill=INK, anchor="mm")
            elif seven == "absent":
                pass
            elif seven == "wrong":
                d.text((x, y), "13", font=f, fill=INK, anchor="mm")
            elif seven == "smudge":
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ds = ImageDraw.Draw(lay)
                rng = random.Random(11)
                blob = []
                for a in range(0, 360, 24):
                    r = rng.randint(14, 26)
                    blob.append((x + r * math.cos(math.radians(a)) * 1.2,
                                 y + r * math.sin(math.radians(a))))
                ds.polygon(blob, fill=INK + (235,))
                ds.line([(x - 30, y + 6), (x + 34, y - 4)], fill=INK + (120,), width=9)  # drag
                ds.line([(x - 22, y + 14), (x + 26, y + 10)], fill=INK + (70,), width=6)
                lay = lay.filter(ImageFilter.GaussianBlur(1.6))
                im.paste(lay, (0, 0), lay)
                d = ImageDraw.Draw(im)
        else:
            d.text((x, y), str(n), font=f, fill=INK, anchor="mm")
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        d.line([(cx + (R - 14) * math.cos(a), cy + (R - 14) * math.sin(a)),
                (cx + (R - 28) * math.cos(a), cy + (R - 28) * math.sin(a))], fill=INK, width=5)
    ah = math.radians(10 * 30 - 90 + 15)
    d.line([(cx, cy), (cx + 110 * math.cos(ah), cy + 110 * math.sin(ah))], fill=INK, width=12)
    am = math.radians(6 * 30 - 90)
    d.line([(cx, cy), (cx + 170 * math.cos(am), cy + 170 * math.sin(am))], fill=INK, width=8)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=INK)
    return im

if __name__ == "__main__":
    clock("normal").save(f"{OUT}/a_control.png")
    clock("absent").save(f"{OUT}/b_absence.png")
    clock("smudge").save(f"{OUT}/c_smudge.png")
    clock("wrong").save(f"{OUT}/d_wrong.png")
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_control", "b_absence", "c_smudge", "d_wrong"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
