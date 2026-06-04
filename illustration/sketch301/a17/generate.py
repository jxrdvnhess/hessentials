# Sketch 301 — A17: Runnable Systems. Domain: basketball play diagrams (X-and-O).
# A control give-and-go / B locally damaged / C specialist set play / D boundary.
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
    d.rectangle([60, 60, 580, 560], outline=INK, width=4)            # half court
    d.line([(250, 60), (250, 250)], fill=INK, width=3)               # key
    d.line([(390, 60), (390, 250)], fill=INK, width=3)
    d.line([(250, 250), (390, 250)], fill=INK, width=3)
    d.arc([250, 180, 390, 320], 0, 180, fill=INK, width=3)           # FT circle
    d.arc([90, -160, 550, 460], 12, 168, fill=INK, width=3)          # 3pt arc
    d.line([(280, 86), (360, 86)], fill=INK, width=4)                # backboard
    d.ellipse([305, 90, 335, 120], outline=INK, width=3)             # hoop
    return im, d

def O(d, x, y, label, f, filled=False):
    if filled:
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=INK)
        d.text((x, y), label, font=f, fill=(246, 242, 232), anchor="mm")
    else:
        d.ellipse([x - 20, y - 20, x + 20, y + 20], outline=INK, width=4,
                  fill=(246, 242, 232))
        d.text((x, y), label, font=f, fill=INK, anchor="mm")

def Xd(d, x, y, f):
    d.line([(x - 13, y - 13), (x + 13, y + 13)], fill=INK, width=5)
    d.line([(x - 13, y + 13), (x + 13, y - 13)], fill=INK, width=5)

def arrow(d, pts, dashed=False, width=4, head=True, color=INK):
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
    if head:
        x0, y0 = pts[-2]; x1, y1 = pts[-1]
        a = math.atan2(y1 - y0, x1 - x0)
        d.polygon([(x1, y1),
                   (x1 - 16 * math.cos(a - 0.45), y1 - 16 * math.sin(a - 0.45)),
                   (x1 - 16 * math.cos(a + 0.45), y1 - 16 * math.sin(a + 0.45))], fill=color)

def screen(d, x, y, ang):
    a = math.radians(ang)
    nx, ny = -math.sin(a), math.cos(a)
    d.line([(x - nx * 16, y - ny * 16), (x + nx * 16, y + ny * 16)], fill=INK, width=6)

def play_a():
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    O(d, 320, 480, "1", f, filled=True)        # ball handler
    O(d, 500, 350, "2", f)
    O(d, 150, 350, "3", f)
    O(d, 270, 200, "5", f)
    arrow(d, [(345, 470), (480, 365)], dashed=True)              # pass to 2
    arrow(d, [(320, 455), (300, 280), (315, 150)])               # 1 cuts to rim
    screen(d, 295, 265, 70)                                       # screen by 5
    arrow(d, [(270, 222), (288, 258)], width=3, head=False)
    im.save(f"{OUT}/a_control.png")

def play_b():
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    O(d, 320, 480, "1", f, filled=True)
    O(d, 500, 350, "1", f)                                        # duplicate 1
    O(d, 150, 350, "6", f)                                        # an O6
    O(d, 270, 200, "5", f)
    arrow(d, [(345, 470), (480, 365)], dashed=True)
    arrow(d, [(320, 455), (300, 280), (315, 150)])
    screen(d, 295, 265, 70)
    arrow(d, [(150, 328), (110, 150), (40, 100)])                 # cut exits the court
    im.save(f"{OUT}/b_damaged.png")

def play_c():
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    fs = ImageFont.truetype(FONT, 17)
    d.text((320, 38), "SLOB — BOX", font=fs, fill=INK, anchor="mm")
    O(d, 320, 540, "1", f, filled=True)                           # inbounder
    O(d, 270, 300, "2", f); O(d, 370, 300, "3", f)
    O(d, 270, 170, "4", f); O(d, 370, 170, "5", f)
    Xd(d, 300, 250, f); Xd(d, 345, 235, f); Xd(d, 320, 150, f)
    arrow(d, [(282, 285), (250, 230), (255, 195)])                # 2 backscreens for 4
    screen(d, 258, 200, 20)
    arrow(d, [(370, 278), (372, 230)], width=3)                   # 3 down to wing? cut
    arrow(d, [(270, 148), (320, 110)])                            # 4 dives to rim
    arrow(d, [(340, 525), (380, 330)], dashed=True)               # inbound pass to 3
    for label, (lx, ly) in [("1", (262, 250)), ("2", (385, 255)), ("3", (300, 122))]:
        d.ellipse([lx - 11, ly - 11, lx + 11, ly + 11], outline=INK, width=2)
        d.text((lx, ly), label, font=fs, fill=INK, anchor="mm")
    arrow(d, [(312, 244), (330, 240)], width=3, head=True, color=(120, 112, 100))  # switch
    im.save(f"{OUT}/c_specialist.png")

def play_d():
    im, d = court(); f = ImageFont.truetype(FONT, 22)
    fs = ImageFont.truetype(FONT, 17)
    O(d, 320, 480, "1", f, filled=True)
    O(d, 500, 350, "2", f)
    O(d, 150, 350, "3", f)
    O(d, 270, 200, "4", f)
    O(d, 430, 200, "5", f)
    # two passes converge on the same empty spot
    arrow(d, [(345, 470), (420, 300)], dashed=True)
    arrow(d, [(480, 340), (425, 305)], dashed=True)
    # 3 and 4 both cut to that same spot, crossing
    arrow(d, [(170, 335), (300, 280), (415, 300)])
    arrow(d, [(285, 215), (350, 330), (418, 308)])
    # 5's cut loops back on itself
    arrow(d, [(430, 222), (470, 280), (430, 320), (400, 270), (435, 235)])
    # screen set on a teammate (bar across 3's own path start)
    screen(d, 200, 325, 110)
    # sequence tags out of order
    for label, (lx, ly) in [("3", (350, 440)), ("1", (455, 320)), ("2", (250, 300))]:
        d.ellipse([lx - 11, ly - 11, lx + 11, ly + 11], outline=INK, width=2)
        d.text((lx, ly), label, font=fs, fill=INK, anchor="mm")
    im.save(f"{OUT}/d_boundary.png")

if __name__ == "__main__":
    play_a(); play_b(); play_c(); play_d()
    s = Image.new("RGB", (4 * 330, 330), (255, 255, 255))
    for k, n in enumerate(["a_control", "b_damaged", "c_specialist", "d_boundary"]):
        s.paste(Image.open(f"{OUT}/{n}.png").resize((320, 320)), (k * 330 + 5, 5))
    s.save(f"{OUT}/_contact.png")
    print("done")
