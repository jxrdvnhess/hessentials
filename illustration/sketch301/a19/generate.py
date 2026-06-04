# Sketch 301 — A19: Template Versus Instance. Basketball.
# A canonical pick-and-roll / B one anti-template step / C strong violation /
# D instance-only (pattern-free, legal). Violations carried by arrow geometry.
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

def arrow(d, pts, dashed=False, width=4):
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        if dashed:
            steps = max(2, int(math.hypot(x1 - x0, y1 - y0) / 12))
            for s in range(0, steps, 2):
                d.line([(x0 + (x1 - x0) * s / steps, y0 + (y1 - y0) * s / steps),
                        (x0 + (x1 - x0) * (s + 1) / steps, y0 + (y1 - y0) * (s + 1) / steps)],
                       fill=INK, width=width)
        else:
            d.line([(x0, y0), (x1, y1)], fill=INK, width=width)
    x0, y0 = pts[-2]; x1, y1 = pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1, y1),
               (x1 - 16 * math.cos(a - 0.45), y1 - 16 * math.sin(a - 0.45)),
               (x1 - 16 * math.cos(a + 0.45), y1 - 16 * math.sin(a + 0.45))], fill=INK)

def screen(d, x, y, ang):
    a = math.radians(ang)
    nx, ny = -math.sin(a), math.cos(a)
    d.line([(x - nx * 16, y - ny * 16), (x + nx * 16, y + ny * 16)], fill=INK, width=6)

def play_a():  # canonical pick-and-roll
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    O(d, 320, 470, "1", f, filled=True)
    O(d, 282, 410, "5", f)
    screen(d, 296, 438, 35)
    arrow(d, [(345, 458), (420, 400), (430, 300)])           # 1 drives off the screen
    arrow(d, [(272, 388), (300, 300), (315, 170)])           # 5 rolls to the rim
    arrow(d, [(432, 330), (340, 190)], dashed=True)          # pocket pass to the roller
    im.save(f"{OUT}/a_canonical.png")

def play_b():  # one anti-template step: the screener "rolls" AWAY from the basket
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    O(d, 320, 470, "1", f, filled=True)
    O(d, 282, 410, "5", f)
    screen(d, 296, 438, 35)
    arrow(d, [(345, 458), (420, 400), (430, 300)])           # 1 drives off the screen
    arrow(d, [(266, 420), (170, 480), (120, 520)])           # 5 departs to the deep corner, AWAY
    arrow(d, [(432, 330), (150, 500)], dashed=True)          # the pass follows the diagram
    im.save(f"{OUT}/b_violation.png")

def play_c():  # strong violation: refused screen, outward roll, backward pass
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    O(d, 320, 470, "1", f, filled=True)
    O(d, 282, 410, "5", f)
    O(d, 430, 520, "2", f)
    screen(d, 296, 438, 35)
    arrow(d, [(300, 482), (220, 520), (160, 540)])           # 1 drives AWAY from the screen
    arrow(d, [(290, 388), (420, 360), (520, 300)])           # 5 walks to the far wing, outward
    arrow(d, [(165, 528), (408, 512)], dashed=True)          # pass goes BACKWARD to 2
    im.save(f"{OUT}/c_strong.png")

def play_d():  # instance only: legal, coherent, pattern-free
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    O(d, 110, 530, "1", f, filled=True)                      # deep corner start
    O(d, 320, 250, "4", f)                                   # free-throw line
    O(d, 545, 200, "3", f)                                   # far short-corner area
    arrow(d, [(130, 512), (180, 430), (160, 350), (210, 300)])  # 1 zigzag dribble upcourt
    arrow(d, [(345, 245), (470, 230), (520, 215)], width=4)  # 4 drifts to the short corner
    arrow(d, [(222, 290), (520, 208)], dashed=True)          # pass corner-slot to short-corner
    arrow(d, [(545, 222), (470, 320), (380, 330)])           # 3 loops out to the wing
    im.save(f"{OUT}/d_instance.png")

if __name__ == "__main__":
    play_a(); play_b(); play_c(); play_d()
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_canonical", "b_violation", "c_strong", "d_instance"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
