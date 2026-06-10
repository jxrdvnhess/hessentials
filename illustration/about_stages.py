"""
Hessentials — ABOUT thesis sheet: discernment as a process, in three stages.

Not three styled rooms. The SAME shelf at three moments, where the meaning lives
entirely in the arrangement and in what changes between them (Sketch 201). The
objects are deliberately generic blocks — candidates — so nothing communicates
through itself; only through relationship: where things are, what was removed,
what remains, what is still being weighed.

  BEFORE  — full of possibilities; everything could stay; nothing judged yet
  DURING  — judgment happening now; pulled out, compared, removed, unresolved
  AFTER   — settled; only what earned its place remains, in calm space

Fast, loose, unfinished. Thesis, not production.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from linen import stroke_alpha

W, H = 1560, 640
CREAM = np.array([245, 239, 229], float)
INK = np.array([70, 64, 57], float)
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
rng = np.random.default_rng(5)
POLYS = []


def wob(pts, amp, k=7):
    m = len(pts)
    def sm(kk):
        kk = max(1, min(kk, m))
        return np.convolve(rng.normal(0, 1, m), np.ones(kk) / kk, mode="same")
    pts = pts.copy()
    pts[:, 0] += sm(k) * amp + sm(2) * amp * 0.4
    pts[:, 1] += sm(k) * amp + sm(2) * amp * 0.4
    return pts


def L(nodes, w=2.0, amp=1.0, closed=False, n=16):
    nn = [np.array(p, float) for p in nodes]
    if closed:
        nn = nn + [nn[0]]
    pts = np.vstack([np.linspace(nn[i], nn[i + 1], n) for i in range(len(nn) - 1)])
    POLYS.append(([tuple(p) for p in wob(pts, amp)], w))


def block(x, base, w=26, h=50, lean=0.0, flat=False):
    if flat:                                   # a thing taken down, set on the floor
        L([(x, base), (x + h, base - 5), (x + h, base - 21), (x, base - 16)], w=2.0, amp=0.9, closed=True)
    else:                                      # a thing standing on the shelf
        L([(x, base), (x + lean, base - h), (x + w + lean, base - h), (x + w, base)], w=2.0, amp=1.0, closed=True)


def shelf(ox):
    L([(ox + 30, 322), (ox + 410, 318)], w=2.2, amp=1.4)
    L([(ox + 30, 322), (ox + 30, 360)], w=1.5, amp=1.0)
    L([(ox + 410, 318), (ox + 410, 356)], w=1.5, amp=1.0)
    L([(ox + 30, 360), (ox + 410, 356)], w=1.5, amp=1.0)
    L([(ox - 10, 474), (ox + 452, 478)], w=2.0, amp=1.6)   # floor


def before(ox):
    shelf(ox)
    for i, x in enumerate([58, 102, 146, 190, 234, 278, 322, 366]):  # full, even — all could stay
        block(ox + x, 320, h=46 + (i % 3) * 7, lean=rng.normal(0, 0.8))


def during(ox):
    shelf(ox)
    for x in [58, 100, 142]:                       # a few still untouched at the left
        block(ox + x, 320, h=50, lean=rng.normal(0, 0.8))
    # a gap where one was removed (190–238 empty), and that one now on the floor
    block(ox + 196, 472, h=46, flat=True)
    # two pulled to the front and set side by side — being compared
    block(ox + 250, 332, h=44)
    block(ox + 280, 332, h=46)
    # one carried off to the far end, alone — set apart, still unresolved
    block(ox + 388, 320, h=54, lean=4)


def after(ox):
    shelf(ox)
    for x in [92, 214, 336]:                       # three, well spaced — what earned its place
        block(ox + x, 320, h=50, lean=rng.normal(0, 0.6))


def label(d, text, cx, y):
    try:
        f = ImageFont.truetype(FONT, 26)
    except Exception:
        f = ImageFont.load_default()
    spaced = "  ".join(text)
    w = d.textlength(spaced, font=f)
    d.text((cx - w / 2, y), spaced, font=f, fill=(120, 113, 103))


if __name__ == "__main__":
    before(10)
    during(530)
    after(1050)
    a = stroke_alpha(W, H, POLYS, width=2.0, jitterblur=0.6, supersample=3)
    img = np.ones((H, W, 3)) * CREAM
    img = img * (1 - a[..., None]) + INK * a[..., None]
    img += (np.asarray(Image.fromarray((rng.normal(0, 1, (H, W)) * 255).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 - 0.5)[..., None] * 6.0
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))
    d = ImageDraw.Draw(out)
    label(d, "BEFORE", 225, 556)
    label(d, "DURING", 745, 556)
    label(d, "AFTER", 1275, 556)
    out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "about", "about-stages.jpg"), quality=92)
    print("saved about-stages.jpg")
