# Sketch 301 — A2: three new images for the fixed-image / varied-question grid.
import math
import numpy as np
from PIL import Image, ImageDraw

W = H = 640
OUT = __file__.rsplit("/", 1)[0]
INK = (32, 29, 26)

def paper():
    base = np.full((H, W, 3), (244, 239, 229), dtype=np.float32)
    noise = np.random.default_rng(7).normal(0, 2.2, (H, W, 1))
    return Image.fromarray(np.clip(base + noise, 0, 255).astype(np.uint8), "RGB")

def bez(p0, p1, p2, steps=50):
    return [(
        (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1],
    ) for t in (i / steps for i in range(steps + 1))]

# control — an unmistakable cup
def cup():
    im = paper(); d = ImageDraw.Draw(im)
    body = [(220, 220), (420, 220), (400, 470), (240, 470)]
    d.polygon(body, fill=(225, 218, 206), outline=INK)
    d.polygon(body, outline=INK)
    for poly in [body]:
        d.line(poly + [poly[0]], fill=INK, width=6, joint="curve")
    d.ellipse([220, 200, 420, 240], fill=(210, 202, 190), outline=INK, width=6)
    d.ellipse([240, 208, 400, 232], fill=(180, 170, 158))
    d.arc([390, 270, 510, 410], -80, 95, fill=INK, width=16)
    d.ellipse([255, 455, 385, 482], fill=(214, 206, 192))  # ground shadow hint
    d.polygon([(240, 470), (400, 470), (396, 478), (244, 478)], fill=INK)
    im.save(f"{OUT}/cup.png")

# a scene — two figures, one extended hand, one turned away
def scene():
    im = paper(); d = ImageDraw.Draw(im)
    d.line([(60, 500), (580, 500)], fill=INK, width=3)
    # figure 1 (left), leaning toward the other, arm extended, small object in hand
    d.ellipse([170, 150, 222, 202], fill=INK)                       # head
    d.polygon([(176, 205), (226, 210), (250, 330), (190, 340)], fill=INK)  # torso leaning right
    d.line([(225, 240), (320, 270)], fill=INK, width=14)            # extended arm
    d.ellipse([316, 258, 344, 286], fill=INK)                       # held object
    d.line([(200, 335), (185, 500)], fill=INK, width=14)
    d.line([(225, 335), (235, 500)], fill=INK, width=14)
    # figure 2 (right), turned away, head bowed
    d.ellipse([432, 175, 482, 225], fill=INK)                       # bowed head, lower
    d.polygon([(420, 230), (470, 222), (462, 345), (414, 345)], fill=INK)  # upright torso, away
    d.line([(424, 250), (410, 350)], fill=INK, width=12)            # arm down
    d.line([(462, 248), (470, 350)], fill=INK, width=12)
    d.line([(428, 345), (424, 500)], fill=INK, width=14)
    d.line([(456, 345), (462, 500)], fill=INK, width=14)
    im.save(f"{OUT}/scene.png")

# a sign — full prohibition grammar around an invented pictogram
def sign():
    im = paper(); d = ImageDraw.Draw(im)
    RED = (178, 44, 38)
    d.ellipse([120, 120, 520, 520], fill=(250, 247, 240), outline=RED, width=34)
    # invented pictogram: spiral over a bar
    cx, cy = 320, 300
    pts = []
    for i in range(260):
        t = i / 30
        r = 6 + 9.5 * t
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    d.line(pts, fill=INK, width=12, joint="curve")
    d.line([(230, 420), (410, 420)], fill=INK, width=16)
    # diagonal slash
    a = math.radians(45)
    r0, r1 = 183, 183
    d.line([(320 - r0 * math.cos(a), 320 - r0 * math.sin(a)),
            (320 + r1 * math.cos(a), 320 + r1 * math.sin(a))], fill=RED, width=34)
    im.save(f"{OUT}/sign.png")

if __name__ == "__main__":
    cup(); scene(); sign(); print("done")
