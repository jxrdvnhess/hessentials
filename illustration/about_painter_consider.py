"""
ABOUT — the painter, micro-variants toward CONSIDERATION (2026-06-12).

Decision phase closed: painter stands. Finishing question: is the figure
correct? The steelman killed the *active / mid-stroke* reading (it reverts
him to a captured instant and forfeits the present-tense win). What survives
is CONSIDERATION — a man paused to look at the wall, the editor's pause. Not
motion.

Three micro-variants. FIGURE ONLY. The wall, clay field, pole, roller, floor,
baseboard are byte-for-byte identical to scene_d — only the figure strokes
change, and the raised arm/fist stay locked to the pole so nothing else moves.

  A — HEAD TILT   the head cocks slightly toward the wall, considering it.
  B — HAND TO HIP the free arm bends, hand rests at the hip (appraising).
  C — WEIGHT      he settles onto one leg, the other eased (a paused stance).

Outputs:
  samples/painter_consider_sheet.png    — current + A/B/C, full + figure crop
"""
import os
import math
import copy
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from about_figure import figure_strokes, render_strokes, PAPER, INK, SAMPLES
from about_scenes import scaled, s, W, H
from scene_d_color import paint_mask

CLAY = np.array([216, 179, 160], float)
FIELD_ALPHA = 0.85
K, DX, DY = 0.415, 680, 756


def _rotate(pts, pivot, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    px, py = pivot
    out = []
    for (x, y) in pts:
        dx, dy = x - px, y - py
        out.append((px + dx * ca - dy * sa, py + dx * sa + dy * ca))
    return out


def base_figure():
    return figure_strokes(0, left_arm="raised")


def variant(move):
    """Return the unscaled figure stroke list with one consideration move.
    Indices are stable because left_arm='raised' is fixed.
      head cluster   = 0..5   (skull, nape, hair x2, ears x2)
      free right arm = 15,16,17 (sleeves, cuff) + 23 (hand)
      free leg/foot  = right leg 24,26 + right shoe 32,33 + break 29
    """
    S = copy.deepcopy(base_figure())

    if move == "head":
        # cock the head toward the wall (his left), about the neck base.
        pivot = (-2, 208)
        for i in range(0, 6):
            S[i]["ctrl"] = _rotate(S[i]["ctrl"], pivot, -7.0)

    elif move == "hip":
        # bend the free (right) arm so the hand rests at the hip; elbow
        # eases out. A held, static appraising stance — not motion.
        S[15]["ctrl"] = [(148, 316), (180, 404), (192, 536), (158, 648),
                         (126, 708)]                      # upper arm + forearm, outer
        S[16]["ctrl"] = [(124, 370), (150, 470), (168, 566), (142, 648),
                         (130, 702)]                      # inner
        S[17]["ctrl"] = [(126, 706), (140, 700)]          # wrist tuck
        S[23]["ctrl"] = [(126, 706), (116, 724), (124, 742), (146, 742),
                         (150, 722), (138, 704)]          # hand on hip

    elif move == "weight":
        # settle onto the left leg; ease the right (free) leg — knee a touch
        # forward, hip a hair higher, foot relaxed. Contrapposto whisper.
        S[24]["ctrl"] = [(118, 754), (120, 902), (128, 1066), (124, 1238),
                         (118, 1388), (116, 1446)]        # right outer, knee out
        S[26]["ctrl"] = [(14, 794), (30, 956), (44, 1122), (50, 1294),
                         (52, 1446)]                      # right inner
        S[32]["ctrl"] = [(116, 1448), (122, 1472), (112, 1484), (62, 1486),
                         (54, 1474), (56, 1448)]          # right shoe, eased forward
        S[33]["ctrl"] = [(120, 1472), (58, 1476)]         # heel seam
        S[29]["ctrl"] = [(116, 1442), (60, 1446)]         # break

    return S


def scene(move):
    """scene_d, with the figure replaced by a consideration variant.
    Props copied verbatim from about_scenes.scene_d."""
    fig = base_figure() if move == "current" else variant(move)
    S = scaled(fig, K, DX, DY)
    # pole
    S.append(s([(630, 150), (633, 480), (636, 814), (643, 846)], 1.6,
               swell=0.06, cs=True))
    # roller
    S.append(s([(575, 128), (630, 124), (685, 127)], 1.8, swell=0.1))
    S.append(s([(573, 146), (628, 142), (683, 145)], 1.8, swell=0.1))
    S.append(s([(575, 128), (573, 146)], 1.2, cs=True, ce=True))
    S.append(s([(685, 127), (683, 145)], 1.2, cs=True, ce=True))
    # floor
    S.append(s([(48, 1354), (380, 1350), (720, 1353), (1004, 1350)], 0.9,
               lead=0.12, tail=0.12, swell=0.04))
    S.append(s([(36, 1384), (360, 1379), (700, 1382), (1012, 1378)], 1.5,
               lead=0.08, tail=0.08, swell=0.06))
    return S


def composite(move, mask):
    ink = render_strokes(scene(move), W, H)
    out = np.ones((H, W, 3)) * PAPER
    field = mask * FIELD_ALPHA
    out = out * (1 - field[..., None]) + CLAY * field[..., None]
    out = out * (1 - ink[..., None]) + INK * ink[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def main():
    mask = paint_mask()
    panels = {m: composite(m, mask) for m in ("current", "head", "hip", "weight")}

    # figure crop region (scaled figure ~ x600-760, y780-1380); pad it
    crop = (548, 720, 812, 1420)
    labels = [("current", "CURRENT"), ("head", "A — HEAD TILT"),
              ("hip", "B — HAND TO HIP"), ("weight", "C — WEIGHT")]

    full_h = 760
    crops = []
    fulls = []
    for key, _ in labels:
        p = panels[key]
        fulls.append(p.resize((int(W * full_h / H), full_h), Image.LANCZOS))
        c = p.crop(crop)
        cw = int(c.width * full_h / c.height)
        crops.append(c.resize((cw, full_h), Image.LANCZOS))

    gap = 28
    fw = fulls[0].width
    cw = crops[0].width
    col = fw + gap + cw
    sheet_w = gap + 4 * (col + gap)
    sheet_h = full_h + 130
    sheet = Image.new("RGB", (sheet_w, sheet_h), tuple(int(v) for v in PAPER))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
    except Exception:
        font = ImageFont.load_default()

    x = gap
    for i, (key, lab) in enumerate(labels):
        sheet.paste(fulls[i], (x, 90))
        sheet.paste(crops[i], (x + fw + gap, 90))
        d.text((x, 40), lab, fill=(31, 29, 27), font=font)
        x += col + gap

    out_path = os.path.join(SAMPLES, "painter_consider_sheet.png")
    sheet.save(out_path)
    print("done:", out_path)


if __name__ == "__main__":
    main()
