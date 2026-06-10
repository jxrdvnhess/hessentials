"""
Hessentials — ABOUT left panel. The name as tonal wallpaper.

The letters of JORDAN HESS, oversized, overlapping, bled off every edge and
laid down in warm-neutral tones at low opacity so the overlaps build the
value. Reads as abstract first, the name second — disguised, not announced.
Geometric face (Poppins Bold). Programmatic synthesis only.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "about", "about-name.jpg")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

NAME = "JORDANHESS"
BG = (242, 238, 230)        # warm cream / greige, a touch warmer than the page
# warm-neutral palette — greige, sand, pale stone. Strictly warm (R>G>B), no
# cool/green drift; the overlaps stay in the same family.
TONES = [
    (206, 196, 180), (219, 210, 193), (228, 220, 203), (197, 187, 170),
    (213, 204, 187), (223, 214, 196), (202, 192, 175), (216, 207, 189),
]


def compose(w=1200, h=1600, seed=6):
    rng = np.random.default_rng(seed)
    base = Image.new("RGBA", (w, h), BG + (255,))

    cols, step_x, step_y = 3, 432, 430
    x0, y0 = -96, -150
    order = rng.permutation(len(NAME))  # stack order varies so overlaps differ

    for k in order:
        ch = NAME[k]
        c, r = k % cols, k // cols
        size = int(610 + rng.integers(-40, 60))
        font = ImageFont.truetype(FONT, size)
        x = x0 + c * step_x + int(rng.integers(-26, 26))
        y = y0 + r * step_y + int(rng.integers(-22, 22))
        tone = TONES[k % len(TONES)]
        outline = (k % 3 == 1)  # roughly every third letter is implied, not filled

        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        if outline:
            a = int(255 * rng.uniform(0.42, 0.55))
            d.text((x, y), ch, font=font, fill=(0, 0, 0, 0),
                   stroke_width=max(3, size // 84), stroke_fill=tone + (a,))
        else:
            # a few letters anchor darker for depth; the rest stay soft
            a = int(255 * (rng.uniform(0.30, 0.42) if k % 4 == 0 else rng.uniform(0.20, 0.30)))
            d.text((x, y), ch, font=font, fill=tone + (a,))
        base = Image.alpha_composite(base, layer)

    img = np.asarray(base.convert("RGB"), float)

    # gentle top-light tonal drift + the barest grain, then a hair of blur so
    # the overlaps read as panes of tone rather than hard vector edges
    yy = np.linspace(0, 1, h)[:, None, None]
    img = img + (0.5 - yy) * 6.0
    img += rng.normal(0, 1.6, (h, w, 1))
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    return out


if __name__ == "__main__":
    compose().save(OUT, quality=92)
    print("saved", OUT)
