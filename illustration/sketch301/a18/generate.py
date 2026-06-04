# Sketch 301 — A18: Execution Meets Conflict. Basketball plays; sequence tags make
# order objective. A clean / B one in-run conflict / C specialist HORNS / D dense.
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

def court():
    im = ground(); d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 580, 560], outline=INK, width=4)
    d.line([(250, 60), (250, 250)], fill=INK, width=3)
    d.line([(390, 60), (390, 250)], fill=INK, width=3)
    d.line([(250, 250), (390, 250)], fill=INK, width=3)
    d.arc([250, 180, 390, 320], 0, 180, fill=INK, width=3)
    d.arc([90, -160, 550, 460], 12, 168, fill=INK, width=3)
    d.line([(280, 86), (360, 86)], fill=INK, width=4)
    d.ellipse([305, 90, 335, 120], outline=INK, width=3)
    return im, d

def O(d, x, y, label, f, filled=False):
    if filled:
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=INK)
        d.text((x, y), label, font=f, fill=(246, 242, 232), anchor="mm")
    else:
        d.ellipse([x - 20, y - 20, x + 20, y + 20], outline=INK, width=4,
                  fill=(246, 242, 232))
        d.text((x, y), label, font=f, fill=INK, anchor="mm")

def Xd(d, x, y):
    d.line([(x - 13, y - 13), (x + 13, y + 13)], fill=INK, width=5)
    d.line([(x - 13, y + 13), (x + 13, y - 13)], fill=INK, width=5)

def arrow(d, pts, dashed=False, width=4, color=INK):
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        if dashed:
            steps = max(2, int(math.hypot(x1 - x0, y1 - y0) / 12))
            for s in range(0, steps, 2):
                d.line([(x0 + (x1 - x0) * s / steps, y0 + (y1 - y0) * s / steps),
                        (x0 + (x1 - x0) * (s + 1) / steps, y0 + (y1 - y0) * (s + 1) / steps)],
                       fill=color, width=width)
        else:
            d.line([(x0, y0), (x1, y1)], fill=color, width=width)
    x0, y0 = pts[-2]; x1, y1 = pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1, y1),
               (x1 - 16 * math.cos(a - 0.45), y1 - 16 * math.sin(a - 0.45)),
               (x1 - 16 * math.cos(a + 0.45), y1 - 16 * math.sin(a + 0.45))], fill=INK)

def screen(d, x, y, ang):
    a = math.radians(ang)
    nx, ny = -math.sin(a), math.cos(a)
    d.line([(x - nx * 16, y - ny * 16), (x + nx * 16, y + ny * 16)], fill=INK, width=6)

def tag(d, x, y, label, f):
    d.ellipse([x - 12, y - 12, x + 12, y + 12], outline=INK, width=2,
              fill=(246, 242, 232))
    d.text((x, y), label, font=f, fill=INK, anchor="mm")

def play_a():
    im, d = court()
    f = ImageFont.truetype(FONT, 22); ft = ImageFont.truetype(FONT, 16)
    O(d, 320, 480, "1", f, filled=True)
    O(d, 500, 350, "2", f)
    O(d, 270, 200, "5", f)
    arrow(d, [(345, 470), (480, 363)], dashed=True)            # (1) pass to 2
    tag(d, 420, 432, "1", ft)
    arrow(d, [(320, 455), (300, 280), (315, 150)])             # (2) 1 cuts off 5
    screen(d, 295, 265, 70)
    tag(d, 282, 350, "2", ft)
    arrow(d, [(488, 332), (350, 160)], dashed=True)            # (3) return pass
    tag(d, 430, 240, "3", ft)
    im.save(f"{OUT}/a_control.png")

def play_b():
    im, d = court()
    f = ImageFont.truetype(FONT, 22); ft = ImageFont.truetype(FONT, 16)
    O(d, 320, 480, "1", f, filled=True)
    O(d, 500, 350, "2", f)
    O(d, 270, 200, "5", f)
    arrow(d, [(500, 372), (510, 480)])                         # (1) 2 cuts wing->corner
    tag(d, 528, 425, "1", ft)
    arrow(d, [(345, 470), (480, 360)], dashed=True)            # (2) pass to the spot 2 LEFT
    tag(d, 408, 400, "2", ft)
    arrow(d, [(290, 215), (320, 300)], width=3)                # 5 drifts (no tag needed)
    im.save(f"{OUT}/b_conflict.png")

def play_c():
    im, d = court()
    f = ImageFont.truetype(FONT, 22); ft = ImageFont.truetype(FONT, 16)
    fs = ImageFont.truetype(FONT, 17)
    d.text((320, 38), "HORNS FLARE", font=fs, fill=INK, anchor="mm")
    O(d, 320, 480, "1", f, filled=True)
    O(d, 265, 235, "4", f); O(d, 375, 235, "5", f)
    O(d, 120, 470, "2", f); O(d, 520, 470, "3", f)
    Xd(d, 320, 430); Xd(d, 280, 280); Xd(d, 380, 285)
    arrow(d, [(335, 458), (282, 258)], dashed=True)            # (1) pass to 4
    tag(d, 322, 372, "1", ft)
    arrow(d, [(300, 470), (180, 420), (150, 350)])             # (2) 1 flares off 5
    screen(d, 230, 442, 25)
    tag(d, 205, 470, "2", ft)
    arrow(d, [(252, 222), (160, 330)], dashed=True)            # (3) 4 passes to 1
    tag(d, 196, 268, "3", ft)
    arrow(d, [(358, 296), (336, 416)], width=3, color=(120, 112, 100))  # switch
    im.save(f"{OUT}/c_specialist.png")

def play_d():
    im, d = court()
    f = ImageFont.truetype(FONT, 22); ft = ImageFont.truetype(FONT, 16)
    O(d, 320, 480, "1", f, filled=True)
    O(d, 520, 440, "3", f)
    O(d, 150, 300, "2", f)
    O(d, 430, 200, "4", f)
    # (1a) 2 cuts to mid-lane spot
    arrow(d, [(172, 312), (290, 330), (330, 290)])
    tag(d, 238, 348, "1", ft)
    # (1b) 4 cuts to the SAME spot, tagged 1 as well
    arrow(d, [(415, 222), (360, 270), (335, 288)])
    tag(d, 396, 262, "1", ft)
    # (2) pass to 3's ORIGINAL corner — after 3 has left at (1)? 3 leaves at (3)!:
    # make it: 3 cuts away at (1) too? Keep per design: pass (2) to corner spot
    arrow(d, [(508, 420), (430, 330), (390, 250)])             # 3 cuts up at (3)?? tag:
    tag(d, 452, 372, "1", ft)                                  # third simultaneous "1"
    arrow(d, [(345, 472), (505, 452)], dashed=True)            # (2) pass to vacated corner
    tag(d, 428, 478, "2", ft)
    # (4) screen supporting the cut that happened at (1)
    screen(d, 300, 320, 60)
    tag(d, 286, 296, "4", ft)
    im.save(f"{OUT}/d_dense.png")

if __name__ == "__main__":
    play_a(); play_b(); play_c(); play_d()
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_control", "b_conflict", "c_specialist", "d_dense"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
