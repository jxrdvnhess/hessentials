# Sketch 301 — A12: Breaking the Recital.
# A: control 1-12. B: nine evenly spaced numerals (coherent, wrong count, no gaps).
# C: three numerals substituted with wrong numbers. D: three substituted with foreign glyphs.
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

def clock(labels, n_positions):
    im = ground(); d = ImageDraw.Draw(im)
    cx, cy, R = 320, 320, 240
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=INK, width=8)
    f = ImageFont.truetype(FONT, 44)
    step = 360 / n_positions
    for i in range(n_positions):
        a = math.radians((i + 1) * step - 90)
        x, y = cx + (R - 52) * math.cos(a), cy + (R - 52) * math.sin(a)
        d.text((x, y), labels[i], font=f, fill=INK, anchor="mm")
        d.line([(cx + (R - 14) * math.cos(a), cy + (R - 14) * math.sin(a)),
                (cx + (R - 28) * math.cos(a), cy + (R - 28) * math.sin(a))], fill=INK, width=5)
    ah = math.radians(10 * (360 / 12) - 90 + 15)
    d.line([(cx, cy), (cx + 110 * math.cos(ah), cy + 110 * math.sin(ah))], fill=INK, width=12)
    am = math.radians(6 * (360 / 12) - 90)
    d.line([(cx, cy), (cx + 170 * math.cos(am), cy + 170 * math.sin(am))], fill=INK, width=8)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=INK)
    return im

if __name__ == "__main__":
    clock([str(n) for n in range(1, 13)], 12).save(f"{OUT}/a_control.png")
    clock([str(n) for n in range(1, 10)], 9).save(f"{OUT}/b_nine.png")
    labels_c = [str(n) for n in range(1, 13)]
    for pos, wrong in [(2, "13"), (5, "17"), (9, "21")]:
        labels_c[pos - 1] = wrong
    clock(labels_c, 12).save(f"{OUT}/c_wrongnums.png")
    labels_d = [str(n) for n in range(1, 13)]
    for pos, glyph in [(2, "Ж"), (5, "Ω"), (9, "Ѱ")]:  # Ж Ω Ѱ
        labels_d[pos - 1] = glyph
    clock(labels_d, 12).save(f"{OUT}/d_foreign.png")
    sheet = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_control", "b_nine", "c_wrongnums", "d_foreign"]):
        sheet.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    sheet.save(f"{OUT}/_contact.png")
    print("done")
