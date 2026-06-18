"""
ABOUT — scene D color pass (2026-06-11).

Jordan approved the rescaled painter and asked for paint color. This is
the first color in the illustration language, so it ships as three
quiet candidates, one flat field each — no gradients, no rendering,
just the wall holding a color the way limewash holds one.

The painted region is everything left of the drawn wet edge, ceiling
to baseboard. The roller carries the same color at full strength (it
is the one place the color is "wet"). A whisper of per-column
variation keeps the field from reading as a vector fill — paint, not
pixel.

Candidates:
  limewash — #f6f1e7  the page's own register, one shade fresher;
             "he is painting the page"
  clay     — #d8b3a0  the hacienda register, warm, melancholy
  sage     — #b9bba4  cooler, gardenish, the most New Yorker of the
             three

Outputs:
  samples/about_scene_d_<name>_paper.png  — one per candidate
  samples/about_scene_d_colors_sheet.png  — side-by-side contact sheet
  ../public/about/the-man-scene-d-<name>.png — flattened web JPEG-style
             PNG on paper (the color field is part of the artwork, so
             the web asset is opaque, not RGBA-over-page)
"""
import os
import numpy as np
from PIL import Image, ImageFilter
from about_figure import render_strokes, PAPER, INK, SAMPLES, WEB
from about_scenes import scene_d, W, H

BASEBOARD_Y = 1350

# Roller cylinder bounds (must match scene_d).
ROLLER_X0, ROLLER_X1 = 575, 685
ROLLER_Y0, ROLLER_Y1 = 127, 143

CANDIDATES = {
    "limewash": (246, 241, 231),
    "clay":     (216, 179, 160),
    "sage":     (185, 187, 164),
}

FIELD_ALPHA = 0.85   # the dried field
ROLLER_ALPHA = 1.0   # the wet load

# Jordan's pick, 2026-06-11: clay. The first color in the illustration
# language. The canonical web asset carries it.
CANONICAL = "clay"


def _wavy(yy, base, amp, period, phase):
    """A vertical boundary that breathes — never ruled."""
    return base + amp * np.sin(2 * np.pi * yy / period + phase)


def paint_mask():
    """(H, W) alpha mask of the painted field + loaded roller.

    Halfway through the wall. The field is built from overlapping
    vertical roller strips, left to right, the way the wall is
    actually being painted:

      settled field — the strips done earlier, evened out, fullest
      strip 1       — full height, one coat, a shade lighter
      strip 2       — bottom unfinished; he lifted early, will return
      strip 3       — the current strip, only begun: ceiling down to
                      the roller, which is still on the wall

    The boundary is never a line; it is wherever the last stroke
    stopped."""
    yy = np.arange(H, dtype=float)[:, None]
    xx = np.arange(W, dtype=float)[None, :]
    below_base = yy >= BASEBOARD_Y

    m = np.zeros((H, W))

    # settled field — everything left of ~415
    e0 = _wavy(yy, 415, 4, 300, 0.8)
    m = np.maximum(m, np.where((xx < e0) & ~below_base, 0.85, 0))

    # strip 1 — full height, one coat. Value kept close to the settled
    # field: a matte wall, not light-and-shadow folds.
    l1 = _wavy(yy, 395, 4, 250, 2.1)
    r1 = _wavy(yy, 505, 5, 280, 4.0)
    m = np.maximum(m, np.where((xx >= l1) & (xx < r1) & ~below_base, 0.82, 0))

    # strip 2 — bottom unfinished, rounded lift, a tight fade (a lift
    # mark, not an airbrush)
    l2 = _wavy(yy, 495, 4, 260, 1.2)
    r2 = _wavy(yy, 605, 6, 300, 5.3)
    end2 = 1255 + 55 * np.sin(np.pi * np.clip((xx - 495) / 110, 0, 1))
    in2 = (xx >= l2) & (xx < r2) & ~below_base
    a2 = np.where(yy < end2 - 24, 0.80,
                  np.where(yy < end2, 0.80 * (end2 - yy) / 24, 0.0))
    m = np.maximum(m, np.where(in2, a2, 0))

    # strip 3 — the current strip: ceiling down to the roller
    l3 = _wavy(yy, 575, 4, 240, 3.3)
    r3 = _wavy(yy, 685, 6, 320, 0.4)
    m = np.maximum(m, np.where((xx >= l3) & (xx < r3) & (yy < ROLLER_Y0 + 4),
                               0.70, 0))

    # pass seams — now a whisper: just enough to say two pulls met here,
    # never a fold crease. Thin and shallow.
    for sx, ph in ((228, 5.1), (310, 0.7), (398, 2.2), (500, 4.1)):
        c = _wavy(yy, sx, 2.5, 230, ph)
        band = np.abs(xx - c) < 5
        m = np.where(band & (m > 0.2) & ~below_base,
                     np.minimum(m + 0.03, 0.97), m)

    # roller-pass texture — much quieter vertical streak; the field reads
    # matte, with only the faintest directional memory of the roller.
    rng = np.random.default_rng(19)
    streak = rng.normal(0, 1, W)
    k = np.ones(31) / 31
    for _ in range(3):
        streak = np.convolve(streak, k, mode="same")
    streak /= np.abs(streak).max() + 1e-9
    amp = np.where(np.arange(W) < 410, 0.016, 0.03)
    m *= 1 + amp[None, :] * streak[None, :]

    # low-frequency, NON-directional mottle — limewash applied by hand.
    # Replaces the curtain read with gentle 2-D unevenness that carries no
    # vertical grain, so the field says "painted", not "cloth".
    g = rng.normal(0, 1, (H, W))
    g = np.asarray(
        Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-9) * 255).astype(np.uint8))
        .filter(ImageFilter.GaussianBlur(22)), float) / 255.0
    g = (g - g.mean()) / (g.std() + 1e-9)
    m = m * (1 + 0.013 * np.clip(g, -2.2, 2.2))

    # the roller itself, loaded
    m[ROLLER_Y0:ROLLER_Y1, ROLLER_X0:ROLLER_X1] = ROLLER_ALPHA
    return np.clip(m, 0, 1)


def render(name, rgb, ink_alpha, mask):
    tint = np.array(rgb, float)
    out = np.ones((H, W, 3)) * PAPER
    out = out * (1 - mask[..., None]) + tint * mask[..., None]
    out = out * (1 - ink_alpha[..., None]) + INK * ink_alpha[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    img.save(os.path.join(SAMPLES, f"about_scene_d_{name}_paper.png"))
    if name == CANONICAL:
        img.save(os.path.join(WEB, "the-man-scene-d.png"))
    return img


if __name__ == "__main__":
    ink = render_strokes(scene_d(), W, H)
    mask = paint_mask()
    panels = [render(n, c, ink, mask) for n, c in CANDIDATES.items()]

    # contact sheet
    gap = 24
    th = 760
    thumbs = [p.resize((int(W * th / H), th), Image.LANCZOS) for p in panels]
    tw = thumbs[0].width
    sheet = Image.new("RGB", (tw * 3 + gap * 4, th + gap * 2),
                      tuple(int(v) for v in PAPER))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (gap + i * (tw + gap), gap))
    sheet.save(os.path.join(SAMPLES, "about_scene_d_colors_sheet.png"))
    print("done:", ", ".join(CANDIDATES))
