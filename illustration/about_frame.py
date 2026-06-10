"""
ABOUT — the frame. Jordan's frame direction, 2026-06-10.

The back-facing figure, arms raised, adjusting a large rectangular
frame on the wall. The frame is intentionally slightly crooked (+0.8
degrees, right side settling). He stands in front of its right portion,
both arms up: one hand on the top-right corner, the other steadying
the top edge. The act is unfinished — he is still deciding. The frame
is empty: on the page, the About essay lives inside it and scrolls
there. Figure, wall, frame, text. Nothing else.

The frame's lines break where his body and arms pass in front of them
— occlusion drawn honestly, no crossings.

Success test: cover the text area and the drawing alone should read
"someone carefully deciding what belongs."

Outputs:
  samples/about_frame_paper.png      — proof on plaster cream
  ../public/about/the-man-frame.png  — RGBA transparent for web

Frame interior (unrotated, for the page's text container), canvas
1180 x 1240:  x 116..690, y 440..1130  ->  left 9.83%, top 35.48%,
width 48.64%, height 55.65%; CSS rotate(0.8deg), same center, to match.
"""
import os
import math
from about_figure import figure_strokes, render_strokes, save_paper, save_web, SAMPLES, WEB

W, H = 1180, 1240
FCX, FLOOR, SCALE = 850, 1228, 0.505   # figure slightly right of center
LOCAL_FLOOR = 1504                     # the figure source's floor line
WSCALE = 0.74                          # line-weight compensation at this scale

# Frame geometry (unrotated), rotated +0.8 deg about its own center.
# The figure stands wholly CLEAR of the opening — the essay lives in
# there; no ink may cross it.
FX0, FY0, FX1, FY1 = 96, 420, 710, 1150
ANG = math.radians(0.8)
FCXC, FCYC = (FX0 + FX1) / 2, (FY0 + FY1) / 2


def rot(x, y):
    """+0.8 deg clockwise about the frame center — the crooked hang."""
    dx, dy = x - FCXC, y - FCYC
    return (FCXC + dx * math.cos(ANG) - dy * math.sin(ANG),
            FCYC + dx * math.sin(ANG) + dy * math.cos(ANG))


def s(ctrl, w, lead=0.14, tail=0.2, swell=0.14, sm=0.6, cs=False, ce=False):
    return dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                smoothing=sm, cap_start=cs, cap_end=ce)


def rs(ctrl, w, **kw):
    return s([rot(x, y) for x, y in ctrl], w, **kw)


def scaled_figure(cx, floor, k):
    """Figure strokes scaled by k, feet kept on `floor`. The hanging
    arms, hands, and the hair-direction strokes (which read as a cap at
    this scale) are removed."""
    S = figure_strokes(cx)
    del S[21:23]      # hanging hands
    del S[11:17]      # hanging sleeves + cuffs
    del S[2:4]        # hair direction strokes
    for st in S:
        st["ctrl"] = [(cx + (x - cx) * k, floor - (LOCAL_FLOOR - y) * k)
                      for x, y in st["ctrl"]]
        st["w"] = st["w"] * WSCALE
    return S


def build():
    S = scaled_figure(FCX, FLOOR, SCALE)
    # Figure landmarks at this scale: head y 499..571 (x 763..837),
    # shoulders (724, 623) and (876, 623), torso left seam x ~ 738,
    # left leg outer x ~ 741..757 low, feet on 1228.

    # ---- THE FRAME — outer + inner moulding, hand waver. He stands
    # beside it; only the corner hand interrupts a line.
    S.append(rs([(FX0, 420), (340, 417), (660, 416)], 2.2))                # top, to the hand
    S.append(rs([(FX0, 420), (94, 780), (FX0, FY1)], 2.2))                 # left edge
    S.append(rs([(FX0, FY1), (340, 1155), (FX1, FY1)], 2.2))               # bottom
    S.append(rs([(710, 432), (712, 780), (710, 1146)], 2.2))               # right edge, below the hand
    S.append(rs([(116, 440), (340, 438), (660, 438)], 1.2))                # inner top
    S.append(rs([(116, 440), (114, 780), (116, 1130)], 1.2))               # inner left
    S.append(rs([(116, 1130), (340, 1127), (690, 1128)], 1.2))             # inner bottom
    S.append(rs([(690, 452), (692, 780), (690, 1126)], 1.2))               # inner right

    # ---- RAISED ARMS — his left hand on the corner, still aligning it;
    # his right arc[s] over his head, open, not yet settled. The act is
    # unfinished.
    # left arm to the corner (clear of the frame opening throughout)
    S.append(s([(774, 623), (744, 540), (726, 470), (719, 438)], 2.0, swell=0.16))
    S.append(s([(792, 626), (762, 556), (744, 494), (734, 452)], 1.5,
               lead=0.22, swell=0.12))
    # hand wrapping the corner
    S.append(s([(711, 430), (706, 412), (717, 403), (729, 409)], 1.3, swell=0.08))
    S.append(s([(719, 405), (725, 417)], 0.9, cs=True, ce=True))
    # right arm, arced over the head, hand open near the corner
    S.append(s([(926, 623), (916, 520), (880, 452), (818, 430)], 2.0, swell=0.16))
    S.append(s([(920, 640), (908, 544), (884, 478), (838, 452)], 1.5,
               lead=0.22, swell=0.12))
    # open hand, hovering — not touching
    S.append(s([(814, 426), (802, 421), (794, 429), (801, 440)], 1.3, swell=0.08))
    S.append(s([(806, 424), (812, 436)], 0.9, cs=True, ce=True))

    return S


if __name__ == "__main__":
    fa = render_strokes(build(), W, H)
    save_paper(fa, os.path.join(SAMPLES, "about_frame_paper.png"))
    save_web(fa, os.path.join(WEB, "the-man-frame.png"))
    print("done")
