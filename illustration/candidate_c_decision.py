"""
501-13 Candidate C — THE DECISION. INSTRUMENT, NOT ASSET.

Why is the wall unfinished? Because the color was still being chosen —
and choosing well takes time. No figure. Three brushed test swatches
on the bare side (clay / sage / limewash — the brand's actual color
studies), the clay field advancing across the wall as the verdict
being acted on. Tools where the worker left them.

Swatches are brushed by hand, not rolled: horizontal stroke texture,
wavy edges. The limewash swatch nearly disappears against the wall —
that is true, so it stays true here.
"""
import os
import numpy as np
from PIL import Image
from about_figure import PAPER, INK, SAMPLES, render_strokes
from about_wall_ablations import build, with_text, _wavy, W, H, BASE_Y, FLOOR_Y, K, DY, CLAY
from about_scenes import s

SAGE = np.array([185, 187, 164], float)
LIME = np.array([246, 241, 231], float)

SWATCHES = (
    (CLAY, 1430, 1545, 570, 742, 0.1),
    (SAGE, 1570, 1685, 578, 748, 2.3),
    (LIME, 1710, 1825, 566, 738, 4.4),
)


def swatch_mask(x0, x1, y0, y1, phase):
    """One hand-brushed test patch: wavy bounds, horizontal strokes."""
    yy = np.arange(H, dtype=float)[:, None]
    xx = np.arange(W, dtype=float)[None, :]
    l = _wavy(yy, x0, 4, 90, phase)
    r = _wavy(yy, x1, 4, 110, phase + 1.7)
    t = x0 + (x1 - x0) * 0  # noqa: placeholder for readability
    top = y0 + 5 * np.sin(2 * np.pi * xx / 70 + phase)
    bot = y1 + 5 * np.sin(2 * np.pi * xx / 85 + phase + 2.1)
    m = ((xx >= l) & (xx < r) & (yy >= top) & (yy < bot)).astype(float) * 0.8
    # horizontal brush variation (hand strokes, not roller pulls)
    rng = np.random.default_rng(int(phase * 100) + 7)
    rows = rng.normal(0, 1, H)
    k = np.ones(9) / 9
    for _ in range(2):
        rows = np.convolve(rows, k, mode="same")
    rows /= np.abs(rows).max() + 1e-9
    m *= 1 + 0.12 * rows[:, None]
    return np.clip(m, 0, 1)


if __name__ == "__main__":
    # base: wall mid-advance, no figure, tools at rest (pause geometry)
    base = build(figure=False, action=False)
    out = np.asarray(base, float)

    for color, x0, x1, y0, y1, ph in SWATCHES:
        m = swatch_mask(x0, x1, y0, y1, ph)[..., None]
        out = out * (1 - m) + color * m

    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    img.save(os.path.join(SAMPLES, "candidate_c_decision_proof.png"))
    with_text(img.copy()).save(os.path.join(SAMPLES, "candidate_c_decision_page.png"))
    print("done")
