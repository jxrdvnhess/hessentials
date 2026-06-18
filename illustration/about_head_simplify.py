"""
ABOUT — head silhouette simplification (2026-06-12, final figure adjustment).

The current hair reads as a specific cut (bob / pageboy / helmet): too wide
at the sides, a blunt nape edge, internal hair-direction strokes that read as
styling. The figure must read as anonymous "someone painting a wall," not a
haircut. HEAD ONLY — pose, scale, register, everything else frozen.

Renders into the refined wide scene (seated roller, flattened clay, resolved
hand) so the head is judged in context and at size. Head variants replace
strokes 0..5 of figure_strokes; the rest of the figure is byte-identical.

  current — the shipping head (reference)
  V1      — closer crop: narrower skull, gentle nape, small tucked ears
  V2      — cleanest skull: narrowest, faint nape, ears as ticks only

Output: samples/head_simplify_sheet.png
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import about_figure
import about_wall_page as m

ORIG = about_figure.figure_strokes


def _h(ctrl, w, swell=0.12, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=0.14, tail=0.2, swell=swell,
                smoothing=0.6, cap_start=cs, cap_end=ce)


def head_current(cx):
    return ORIG(cx, left_arm="raised")[0:6]


def head_v1(cx):
    # closer crop — bring the sides in (~±56), let the nape taper into the
    # neck, keep small tucked ears, drop the internal hair strokes.
    return [
        _h([(cx-54, 196), (cx-58, 146), (cx-44, 92), (cx-2, 66),
            (cx+40, 82), (cx+56, 144), (cx+52, 194)], 2.4, swell=0.16),   # skull
        _h([(cx-46, 191), (cx-16, 199), (cx+18, 198), (cx+48, 187)], 1.5,
           swell=0.08),                                                    # nape, gentle
        _h([(cx-58, 152), (cx-63, 168), (cx-54, 183)], 1.2, swell=0.1),    # left ear, small
        _h([(cx+56, 150), (cx+63, 166), (cx+54, 181)], 1.2, swell=0.1),    # right ear
    ]


def head_v2(cx):
    # cleanest skull — narrowest (~±50), faint nape, ears as ticks only.
    return [
        _h([(cx-49, 193), (cx-53, 142), (cx-39, 90), (cx-2, 68),
            (cx+37, 84), (cx+51, 140), (cx+47, 191)], 2.4, swell=0.15),    # skull
        _h([(cx-39, 189), (cx-12, 196), (cx+20, 195), (cx+44, 185)], 1.3,
           swell=0.06),                                                    # nape, faint
        _h([(cx-51, 156), (cx-57, 170)], 1.0, swell=0.06, cs=True, ce=True),  # ear tick
        _h([(cx+50, 156), (cx+56, 170)], 1.0, swell=0.06, cs=True, ce=True),  # ear tick
    ]


def make_variant(head_fn):
    def fn(cx, left_arm="raised"):
        return head_fn(cx) + ORIG(cx, left_arm=left_arm)[6:]
    return fn


def render(head_fn):
    about_figure.figure_strokes = make_variant(head_fn)
    m.figure_strokes = make_variant(head_fn)
    ink = m.render_strokes(m.ink_strokes(), m.W, m.H)
    mask = m.paint_mask()
    out = np.ones((m.H, m.W, 3)) * m.PAPER
    out = out * (1 - mask[..., None]) + m.CLAY * mask[..., None]
    out = out * (1 - ink[..., None]) + m.INK * ink[..., None]
    about_figure.figure_strokes = ORIG
    m.figure_strokes = ORIG
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def main():
    panels = [("current", head_current), ("V1 — closer crop", head_v1),
              ("V2 — cleanest skull", head_v2)]
    head_crop = (1255, 612, 1375, 720)   # the head, in the wide scene
    body_crop = (1230, 600, 1430, 1180)  # head + body at across-room size

    H_head = 360
    H_body = 360
    cols = []
    for _, fn in panels:
        img = render(fn)
        hc = img.crop(head_crop)
        hc = hc.resize((int(hc.width * H_head / hc.height), H_head), Image.LANCZOS)
        bc = img.crop(body_crop)
        bc = bc.resize((int(bc.width * H_body / bc.height), H_body), Image.LANCZOS)
        cols.append((hc, bc))

    gap = 26
    cw = max(c[0].width + gap + c[1].width for c in cols)
    sheet = Image.new("RGB", (gap + 3 * (cw + gap), H_head + 90),
                      tuple(int(v) for v in m.PAPER))
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
    except Exception:
        f = ImageFont.load_default()
    x = gap
    for i, (lab, _) in enumerate(panels):
        hc, bc = cols[i]
        sheet.paste(hc, (x, 70))
        sheet.paste(bc, (x + hc.width + gap, 70))
        d.text((x, 30), lab, fill=(31, 29, 27), font=f)
        x += cw + gap
    sheet.save("samples/head_simplify_sheet.png")
    print("done")


if __name__ == "__main__":
    main()
