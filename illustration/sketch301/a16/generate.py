# Sketch 301 — A16: Execution. Domain: wordless assembly instructions (a stool).
# A control / B locally damaged / C expert exploded view / D boundary (hard to run).
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (38, 34, 30)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def ground():
    base = np.full((H, W, 3), (246, 242, 232), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def panel(d, box, num, f):
    d.rectangle(box, outline=INK, width=3)
    d.ellipse([box[0] + 8, box[1] + 8, box[0] + 40, box[1] + 40], outline=INK, width=3)
    d.text((box[0] + 24, box[1] + 24), str(num), font=f, fill=INK, anchor="mm")

def top_piece(d, x, y, w=120, h=26):
    d.rounded_rectangle([x, y, x + w, y + h], 10, fill=(210, 202, 188), outline=INK, width=3)

def leg(d, x, y, L=70, vert=True):
    if vert:
        d.rounded_rectangle([x, y, x + 16, y + L], 7, fill=(190, 180, 164), outline=INK, width=3)
    else:
        d.rounded_rectangle([x, y, x + L, y + 16], 7, fill=(190, 180, 164), outline=INK, width=3)

def screw(d, x, y):
    d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=INK, width=3)
    d.line([(x - 3, y - 3), (x + 3, y + 3)], fill=INK, width=2)
    d.line([(x, y + 5), (x, y + 18)], fill=INK, width=3)
    for k in range(3):
        d.line([(x - 3, y + 8 + k * 4), (x + 3, y + 8 + k * 4)], fill=INK, width=1)

def allen(d, x, y):
    d.line([(x, y), (x, y + 30)], fill=INK, width=5)
    d.line([(x, y + 30), (x + 18, y + 30)], fill=INK, width=5)

def arrow(d, x0, y0, x1, y1):
    d.line([(x0, y0), (x1, y1)], fill=INK, width=4)
    a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1, y1),
               (x1 - 14 * math.cos(a - 0.45), y1 - 14 * math.sin(a - 0.45)),
               (x1 - 14 * math.cos(a + 0.45), y1 - 14 * math.sin(a + 0.45))], fill=INK)

def count(d, x, y, n, f):
    d.text((x, y), f"{n}×", font=f, fill=INK, anchor="lm")

def sheet(steps, screws_n=4, legs_n=4, reversed_arrow=False, extra=False):
    im = ground(); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 24)
    boxes = [(60, 60, 580, 240), (60, 260, 320, 560), (330, 260, 580, 560)]
    for box, num in zip(boxes, steps[:3]):
        panel(d, box, num, f)
    # P1 inventory
    top_piece(d, 90, 120)
    for i in range(legs_n):
        leg(d, 250 + i * 30, 100, L=90)
    count(d, 250 + legs_n * 30 + 10, 145, legs_n, f)
    for i in range(4):
        screw(d, 420 + i * 26, 120)
    count(d, 420 + 4 * 26 + 8, 130, screws_n, f)
    allen(d, 540, 105)
    # P2 attach
    top_piece(d, 95, 480, w=170)
    d.ellipse([120, 484, 134, 494], outline=INK, width=2)  # corner hole
    leg(d, 119, 330, L=110)
    if reversed_arrow:
        arrow(d, 127, 452, 127, 360)
    else:
        arrow(d, 127, 452, 127, 478)
    screw(d, 200, 350); allen(d, 240, 345)
    # P3 done
    top_piece(d, 380, 330, w=150)
    for k in (0, 1):
        leg(d, 398 + k * 100, 356, L=130)
        leg(d, 420 + k * 70, 350, L=120)
    d.line([(480, 530), (500, 550), (540, 500)], fill=INK, width=6, joint="curve")
    if extra:
        pass
    return im, d, f

def sheet_a():
    im, d, f = sheet([1, 2, 3])
    im.save(f"{OUT}/a_control.png")

def sheet_b():
    im, d, f = sheet([1, 3, 2], screws_n=5, reversed_arrow=True)
    im.save(f"{OUT}/b_damaged.png")

def sheet_c():
    im = ground(); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 22)
    fs = ImageFont.truetype(FONT, 17)
    # exploded isometric-ish view
    top = [(220, 150), (470, 120), (540, 170), (290, 200)]
    d.polygon(top, fill=(210, 202, 188), outline=INK)
    d.polygon([(290, 200), (540, 170), (540, 192), (290, 222)], fill=(180, 170, 154),
              outline=INK)
    d.text((205, 130), "A", font=f, fill=INK, anchor="mm")
    holes = [(300, 196), (380, 186), (450, 176), (520, 168)]
    for i, (hx, hy) in enumerate(holes):
        d.ellipse([hx - 6, hy - 3, hx + 6, hy + 3], outline=INK, width=2)
        # dashed axis down to leg
        for s in range(6):
            d.line([(hx, hy + 30 + s * 28), (hx, hy + 42 + s * 28)], fill=(120, 112, 100), width=2)
        leg(d, hx - 8, hy + 200, L=100)
        d.text((hx - 26, hy + 250), f"B{i+1}", font=fs, fill=INK, anchor="mm")
        screw(d, hx, hy + 60)
    d.text((560, 250), "S  M6×40", font=fs, fill=INK, anchor="mm")
    d.text((585, 272), "4×", font=fs, fill=INK, anchor="mm")
    # detail inset: zoom circle of joint
    d.ellipse([60, 380, 220, 540], outline=INK, width=3)
    d.line([(200, 400), (300, 230)], fill=INK, width=2)
    top_piece(d, 85, 430, w=110, h=20)
    screw(d, 140, 398)
    leg(d, 132, 455, L=70)
    d.text((140, 560), "DETAIL  1:2", font=fs, fill=INK, anchor="mm")
    im.save(f"{OUT}/c_specialist.png")

def sheet_d():
    im = ground(); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 24)
    boxes = [(60, 60, 350, 300), (360, 60, 580, 300), (60, 310, 350, 560), (360, 310, 580, 560)]
    for box, num in zip(boxes, [1, 2, 3, 2]):       # two panels both numbered 2
        panel(d, box, num, f)
    # P1 inventory: 3 legs, 5 screws, a bracket never used
    top_piece(d, 90, 130, w=110)
    for i in range(3):
        leg(d, 230 + i * 26, 110, L=80)
    count(d, 230 + 3 * 26 + 6, 150, 3, f)
    for i in range(5):
        screw(d, 95 + i * 24, 230)
    count(d, 95 + 5 * 24 + 6, 240, 5, f)
    d.polygon([(310, 230), (336, 230), (336, 256), (323, 256), (323, 243), (310, 243)],
              outline=INK, width=3)                 # the bracket X
    # P2: two opposing arrows at the same hole
    top_piece(d, 390, 200, w=150)
    leg(d, 420, 100, L=80)
    arrow(d, 428, 186, 428, 198)
    arrow(d, 448, 198, 448, 120)
    screw(d, 520, 120)
    # P3: assembled with 4 legs (one never in inventory) + bracket floating
    top_piece(d, 95, 370, w=150)
    for k in range(4):
        leg(d, 105 + k * 34, 396, L=120)
    d.polygon([(280, 430), (306, 430), (306, 456), (293, 456), (293, 443), (280, 443)],
              outline=INK, width=3)
    for s in range(5):
        d.line([(270 - s * 14, 440), (264 - s * 14, 440)], fill=(120, 112, 100), width=2)
    # P4 ("2" again): the stool upside-down with legs being removed?? arrows outward
    top_piece(d, 395, 480, w=150)
    for k in (0, 1):
        leg(d, 420 + k * 80, 360, L=100)
        arrow(d, 428 + k * 80, 470, 428 + k * 80, 380)
    im.save(f"{OUT}/d_boundary.png")

if __name__ == "__main__":
    sheet_a(); sheet_b(); sheet_c(); sheet_d()
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_control", "b_damaged", "c_specialist", "d_boundary"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
