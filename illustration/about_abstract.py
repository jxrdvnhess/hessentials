"""
Hessentials — ABOUT panel. The name as raw material, four directions.

Single glyphs from JORDAN HESS, blown past recognition and rendered as graphite
construction-line outlines, soft tonal masses, and erased ghosts, then composed
for tension and asymmetry. Four variants:

  arch      — drafting precision: thin contours, datums, projection + dimension
              lines, registration ticks. Almost no fill. An architect's sheet.
  twombly   — raw gesture: smeared contours, looping graphite scrawls, erasure.
  dissolved — enormous cropped fragments, vast negative space, near-abstraction.
  tonal     — overlapping soft masses (notan), one thin contour for tension.

Programmatic synthesis only. Warm graphite on warm cream.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "..", "public", "about")
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

W, H = 1200, 1600
CREAM = np.array([243, 239, 231], float)
GRAPHITE = np.array([72, 66, 60], float)
STONE = np.array([198, 190, 176], float)


def glyph_mask(ch, px=1500):
    font = ImageFont.truetype(FONT, px)
    tmp = Image.new("L", (int(px * 1.6), int(px * 1.8)), 0)
    ImageDraw.Draw(tmp).text((px * 0.3, px * 0.1), ch, font=font, fill=255)
    return tmp.crop(tmp.getbbox())


def placed(mask, scale, angle, cx, cy):
    m = mask.resize((max(1, int(mask.width * scale)), max(1, int(mask.height * scale))), Image.LANCZOS)
    m = m.rotate(angle, expand=True, resample=Image.BICUBIC)
    full = Image.new("L", (W, H), 0)
    full.paste(m, (int(cx - m.width / 2), int(cy - m.height / 2)))
    return full


def comp(canvas, alpha2d, color):
    a = np.clip(alpha2d, 0, 1)[..., None]
    return canvas * (1 - a) + color * a


def as_mass(full, alpha):
    return np.asarray(full, float) / 255.0 * alpha


def as_outline(full, thickness=7, alpha=0.85):
    if thickness % 2 == 0:
        thickness += 1
    eroded = full.filter(ImageFilter.MinFilter(thickness))
    b = np.asarray(full, float) / 255.0 - np.asarray(eroded, float) / 255.0
    return np.clip(b, 0, 1) * alpha


def as_ghost(full, blur=14, alpha=0.22):
    g = full.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(g, float) / 255.0 * alpha


def lines_layer(draw_fn):
    layer = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(layer))
    return layer


def tick(d, x, y, r=9, w=2):
    d.line([(x - r, y), (x + r, y)], fill=255, width=w)
    d.line([(x, y - r), (x, y + r)], fill=255, width=w)


def scribble(rng, n=240, x0=640, y0=760, spread=120, turns=6):
    ang = np.cumsum(rng.normal(0, 0.6, n)) + np.linspace(0, turns * np.pi, n)
    r = spread * (0.5 + 0.5 * np.sin(np.linspace(0, 3, n))) + np.cumsum(rng.normal(0, 1.2, n))
    xs = x0 + np.cos(ang) * r * 0.7 + rng.normal(0, 2, n).cumsum() * 0.2
    ys = y0 + np.sin(ang) * r + rng.normal(0, 2, n).cumsum() * 0.2
    return list(zip(xs, ys))


def compose(variant, seed=11):
    rng = np.random.default_rng(seed)
    canvas = np.ones((H, W, 3)) * CREAM

    if variant == "arch":
        canvas = comp(canvas, as_mass(placed(glyph_mask("D"), 0.85, -6, 175, 1210), 0.12), STONE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("S"), 1.05, 16, 840, 560), 5, 0.82), GRAPHITE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("A"), 0.62, 18, 360, 560), 5, 0.42), GRAPHITE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("R"), 0.5, -22, 660, 880), 5, 0.55), GRAPHITE)

        def draw(d):
            d.line([(250, 40), (250, 1240)], fill=255, width=1)            # vertical datum
            d.line([(110, 470), (1110, 470)], fill=255, width=1)           # horizontal datum
            d.line([(660, 880), (1180, 600)], fill=255, width=1)           # projection
            d.line([(180, 1330), (700, 1330)], fill=255, width=1)          # dimension line
            tick(d, 180, 1330); tick(d, 700, 1330)
            for p in [(250, 40), (1110, 470), (1180, 600), (660, 880)]:
                tick(d, *p)
        canvas = comp(canvas, np.asarray(lines_layer(draw), float) / 255.0 * 0.42, GRAPHITE)

    elif variant == "twombly":
        canvas = comp(canvas, as_mass(placed(glyph_mask("D"), 0.85, -6, 200, 1150), 0.18), STONE)
        canvas = comp(canvas, as_ghost(placed(glyph_mask("S"), 1.1, 18, 820, 560), 10, 0.30), GRAPHITE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("R"), 0.6, -26, 620, 840), 7, 0.48), GRAPHITE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("J"), 0.8, -4, 470, 1470), 7, 0.4), GRAPHITE)
        for (x0, y0, sp, tn, wd, al) in [(700, 700, 110, 7, 4, 0.5), (430, 980, 80, 5, 3, 0.42), (880, 470, 70, 6, 3, 0.4)]:
            gl = lines_layer(lambda d, pts=scribble(rng, x0=x0, y0=y0, spread=sp, turns=tn): d.line([(int(x), int(y)) for x, y in pts], fill=255, width=wd, joint="curve"))
            canvas = comp(canvas, np.asarray(gl.filter(ImageFilter.GaussianBlur(0.6)), float) / 255.0 * al, GRAPHITE)
        # a smear
        sm = lines_layer(lambda d: d.line([(560, 760), (900, 690)], fill=255, width=26))
        canvas = comp(canvas, np.asarray(sm.filter(ImageFilter.GaussianBlur(14)), float) / 255.0 * 0.16, GRAPHITE)

    elif variant == "dissolved":
        canvas = comp(canvas, as_mass(placed(glyph_mask("S"), 1.75, 20, 840, 980), 0.24), STONE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("O"), 1.95, 10, 240, 470), 9, 0.82), GRAPHITE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("J"), 1.0, -6, 540, 1500), 5, 0.4), GRAPHITE)

        def draw(d):
            d.line([(120, 360), (1140, 250)], fill=255, width=1)
            tick(d, 1140, 250)
        canvas = comp(canvas, np.asarray(lines_layer(draw), float) / 255.0 * 0.32, GRAPHITE)

    elif variant == "tonal":
        canvas = comp(canvas, as_mass(placed(glyph_mask("D"), 0.92, -6, 250, 1150), 0.22), STONE)
        canvas = comp(canvas, as_mass(placed(glyph_mask("A"), 0.72, 16, 540, 520), 0.16), STONE)
        canvas = comp(canvas, as_mass(placed(glyph_mask("S"), 0.95, 18, 880, 660), 0.15), STONE)
        canvas = comp(canvas, as_ghost(placed(glyph_mask("O"), 0.9, 8, 960, 1170), 12, 0.13), GRAPHITE)
        canvas = comp(canvas, as_outline(placed(glyph_mask("R"), 0.55, -24, 650, 870), 5, 0.42), GRAPHITE)

    canvas = canvas + rng.normal(0, 1.6, (H, W, 1))
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))


if __name__ == "__main__":
    for v in ("arch", "twombly", "dissolved", "tonal"):
        compose(v).save(os.path.join(OUTDIR, f"about-abstract-{v}.jpg"), quality=92)
        print("saved", v)
