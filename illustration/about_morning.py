"""
Hessentials — ABOUT, the morning room. Two readings, lighter.

From the owned interior hacienda-03-morning.jpg (coffee at the table, the day not
started). Rendered as a made graphite drawing on cream, airier than the first
pass — lights opened to bare cream, fewer strokes, the room left to breathe.

  about-morning-figure.jpg  — the moment, with the person in it
  about-morning-empty.jpg   — the moment just after: the cup and the light, no one

The empty version inpaints the figure out of the source first (Telea), so the
table, the doorway and the morning light remain and the room becomes a place the
viewer inhabits. Programmatic synthesis only.
"""
import os
import numpy as np
from PIL import Image
from about_backdrop import scratch_on_cream

import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "public", "home", "hacienda-03-morning.jpg")
OUTDIR = os.path.join(HERE, "..", "public", "about")

PARAMS = dict(
    seed=4, n_strokes=82000, ss=2, gamma=1.5, edge_gain=1.35, follow=0.9,
    floor_cut=0.30, hi_protect=0.62, hi_strength=0.9, glow=0.6, sat=5.4,
)


def long_size(path, long=1600):
    aw, ah = Image.open(path).size
    return (long, round(long * ah / aw)) if aw >= ah else (round(long * aw / ah), long)


def empty_the_room():
    im = cv2.imread(SRC)
    h, w = im.shape[:2]
    sx, sy = w / 768.0, h / 512.0   # mask authored in 768x512 space, scaled
    mask = np.zeros((h, w), np.uint8)
    pts = np.array([[110, 140], [300, 135], [362, 300], [384, 430], [300, 512], [108, 512]], np.float32)
    pts = (pts * [sx, sy]).astype(np.int32)
    cv2.fillPoly(mask, [pts], 255)
    mask = cv2.dilate(mask, np.ones((11, 11), np.uint8), iterations=2)
    empty = cv2.inpaint(im, mask, 10, cv2.INPAINT_TELEA)
    out = os.path.join(OUTDIR, "_morning-empty-src.jpg")
    cv2.imwrite(out, empty)
    return out


if __name__ == "__main__":
    empty_src = empty_the_room()
    for src, out in [(SRC, "about-morning-figure.jpg"), (empty_src, "about-morning-empty.jpg")]:
        W, H = long_size(src)
        scratch_on_cream(src, W, H, **PARAMS).save(os.path.join(OUTDIR, out), quality=92)
        print("saved", out, f"{W}x{H}")
