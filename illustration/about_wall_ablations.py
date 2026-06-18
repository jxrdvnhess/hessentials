"""
ABOUT wall — faculty ablations (2026-06-11). INSTRUMENT, NOT ASSET.

Five attacks ordered at page-contact review, run as real renders with
the real essay copy composited at the page's column geometry:

  Q1  remove the roller (and its pole)   — is the tool explanatory?
  Q2  remove the figure entirely         — what carries the idea?
  Q3  remove tray + can                  — is the floor evidence time
                                           or decoration?
  Q5a painted field reduced 20%          — is the balance correct or
  Q5b painted field increased 20%          merely familiar?

(Q4 is observational — recorded in the session report, not rendered.)

The whole working group (strips, roller, figure, floor evidence) moves
together under an edge-scale E so the figure always stands at his own
working edge.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
from about_figure import figure_strokes, render_strokes, PAPER, INK, SAMPLES
from about_scenes import s, scaled

W, H = 1920, 1280
FLOOR_Y, BASE_Y = 1150, 1122
K, DY = 0.353, 619
CLAY = np.array([216, 179, 160], float)


def _wavy(yy, base, amp, period, phase):
    return base + amp * np.sin(2 * np.pi * yy / period + phase)


def build(E=1.0, roller=True, figure=True, floor_ev=True, action=True,
          charm=False):
    """Render one variant. E scales the painted extent; the working
    group (figure, roller, floor evidence) tracks the edge.

    action=False is the final attack (Q6): everything kept, only the
    act removed — the man stands before the edge, arms down, the
    roller resting on its pole against the wall by the tray. The work
    is paused, not abandoned; the wet tools keep the causality."""
    cx = 1210 * E + 100
    rcx = 1152 * E
    # charm v4's grip sits at arm's length (figure-space (-146, 208));
    # the rig figure grips beside the head; best man reaches higher
    if charm == "best":
        fist = (cx - 62, 670)
    elif charm:
        fist = (cx - 51.5, 692)
    else:
        fist = (cx - 37.4, 668)

    S = []
    if figure:
        if charm == "best":
            from best_man import best_man
            S += scaled(best_man(0), K, cx, DY)
        elif charm == "v5":
            from charm_studies import presence_figure
            S += scaled(presence_figure(0), K, cx, DY)
        elif charm:
            from charm_studies import charm_figure
            S += scaled(charm_figure(0, head=1.08, weight=1.6, crane=0.6,
                                     observed=True), K, cx, DY)
        else:
            S += scaled(figure_strokes(0, left_arm="raised" if action else "down"),
                        K, cx, DY)
        if roller and action:
            S.append(s([(rcx, 386), ((rcx + fist[0]) / 2, 527),
                        fist, (fist[0] + 9, 700)], 1.5, swell=0.06, cs=True))
    if roller and not action:
        # the pole at rest — leaning on the wall beside the tray,
        # roller end up, still loaded
        px, py = cx + 62, 425                     # roller center, top
        bx = cx + 88                              # pole foot, by the tray
        S.append(s([(px - 47, py - 16), (px, py - 20), (px + 48, py - 17)],
                   1.7, swell=0.1))
        S.append(s([(px - 49, py), (px - 2, py - 4), (px + 46, py - 1)],
                   1.7, swell=0.1))
        S.append(s([(px - 47, py - 16), (px - 49, py)], 1.1, cs=True, ce=True))
        S.append(s([(px + 48, py - 17), (px + 46, py - 1)], 1.1, cs=True, ce=True))
        S.append(s([(px, py + 2), ((px + bx) / 2, 786), (bx, 1146)], 1.5,
                   swell=0.06, cs=True, ce=True))
    if roller and action:
        S.append(s([(rcx - 47, 366), (rcx, 362), (rcx + 48, 365)], 1.7, swell=0.1))
        S.append(s([(rcx - 49, 382), (rcx - 2, 378), (rcx + 46, 381)], 1.7, swell=0.1))
        S.append(s([(rcx - 47, 366), (rcx - 49, 382)], 1.1, cs=True, ce=True))
        S.append(s([(rcx + 48, 365), (rcx + 46, 381)], 1.1, cs=True, ce=True))
    S.append(s([(40, BASE_Y + 4), (700, BASE_Y), (1340, BASE_Y + 3),
                (1880, BASE_Y)], 0.9, lead=0.1, tail=0.1, swell=0.04))
    S.append(s([(28, FLOOR_Y + 2), (660, FLOOR_Y - 2), (1300, FLOOR_Y + 1),
                (1892, FLOOR_Y - 2)], 1.4, lead=0.06, tail=0.06, swell=0.06))
    if floor_ev:
        tx, cn = cx + 80, cx + 210
        S.append(s([(tx, 1128), (tx + 50, 1125), (tx + 100, 1126)], 1.5, swell=0.1))
        S.append(s([(tx, 1128), (tx + 7, 1148)], 1.1, cs=True))
        S.append(s([(tx + 100, 1126), (tx + 94, 1146)], 1.1, cs=True))
        S.append(s([(tx + 7, 1148), (tx + 52, 1150), (tx + 94, 1146)], 1.2, swell=0.08))
        S.append(s([(cn, 1090), (cn + 3, 1146)], 1.5, swell=0.1))
        S.append(s([(cn + 44, 1088), (cn + 46, 1144)], 1.5, swell=0.1))
        S.append(s([(cn, 1090), (cn + 22, 1084), (cn + 44, 1088)], 1.2, swell=0.08))
        S.append(s([(cn + 2, 1098), (cn + 43, 1096)], 0.8, swell=0.05))
        S.append(s([(cn + 5, 1147), (cn + 41, 1145)], 1.0, swell=0.06))
    ink = render_strokes(S, W, H)

    # ---- paint mask ----
    yy = np.arange(H, dtype=float)[:, None]
    xx = np.arange(W, dtype=float)[None, :]
    below = yy >= BASE_Y
    m = np.zeros((H, W))

    e0 = _wavy(yy, 870 * E, 4, 320, 0.8)
    m = np.maximum(m, np.where((xx < e0) & ~below, 0.85, 0))
    l1, r1 = _wavy(yy, 850 * E, 4, 260, 2.1), _wavy(yy, 1000 * E, 5, 290, 4.0)
    m = np.maximum(m, np.where((xx >= l1) & (xx < r1) & ~below, 0.78, 0))
    l2, r2 = _wavy(yy, 985 * E, 4, 270, 1.2), _wavy(yy, 1120 * E, 6, 300, 5.3)
    end2 = 950 + 55 * np.sin(np.pi * np.clip((xx - 985 * E) / (135 * E), 0, 1))
    in2 = (xx >= l2) & (xx < r2) & ~below
    a2 = np.where(yy < end2 - 24, 0.70,
                  np.where(yy < end2, 0.70 * (end2 - yy) / 24, 0.0))
    m = np.maximum(m, np.where(in2, a2, 0))
    l3, r3 = _wavy(yy, 1100 * E, 4, 250, 3.3), _wavy(yy, 1210 * E, 5, 330, 0.4)
    m = np.maximum(m, np.where((xx >= l3) & (xx < r3) & (yy < 366), 0.70, 0))

    for sx, ph in ((240, 5.1), (440, 0.7), (640, 2.2), (855, 4.1), (992, 3.0)):
        c = _wavy(yy, sx * E, 2.5, 230, ph)
        depth = 0.05 if sx * E < 700 * E else 0.09
        band = np.abs(xx - c) < 6
        m = np.where(band & (m > 0.2) & ~below, np.minimum(m + depth, 0.97), m)

    rng = np.random.default_rng(19)
    streak = rng.normal(0, 1, W)
    k = np.ones(31) / 31
    for _ in range(3):
        streak = np.convolve(streak, k, mode="same")
    streak /= np.abs(streak).max() + 1e-9
    amp = np.where(np.arange(W) < 700 * E, 0.03, 0.07)
    m *= 1 + amp[None, :] * streak[None, :]

    if roller and action:
        m[362:380, int(rcx - 47):int(rcx + 48)] = 1.0
    if roller and not action:
        m[409:424, int(cx + 15):int(cx + 110)] = 1.0   # resting roller, loaded
    if floor_ev:
        m[1132:1146, int(cx + 92):int(cx + 170)] = 1.0
        m[1086:1096, int(cx + 214):int(cx + 252)] = 1.0
    m = np.clip(m, 0, 1)

    out = np.ones((H, W, 3)) * PAPER
    out = out * (1 - m[..., None]) + CLAY * m[..., None]
    out = out * (1 - ink[..., None]) + INK * ink[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


PARAS = [
    "For as long as I can remember, the people in my life have asked me what I think.",
    "What to wear to the thing. How to set the table. Which flowers for the dinner. What pot to buy. What to cook when nothing in the fridge looks like dinner. Whether the apartment is worth it. Whether the wedding gift is too much or not enough.",
    "I don't think this is unusual. Most people have someone they call. I'm the person a lot of people call.",
    "It isn't trained or formal. I have an eye for what's right, and I trust it. The work is in the discernment — knowing what holds up and what doesn't, when something is technically fine but energetically off, what's the real version of a thing and what's the performance of one.",
    "My instinct is to refine. To look at something and see what's slightly off, then make the small adjustments that move it from fine to right.",
]


def with_text(img):
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 27)
    except OSError:
        f = ImageFont.load_default()
    x, y = 115, 384
    for p in PARAS:
        for line in textwrap.wrap(p, width=52):
            d.text((x, y), line, font=f, fill=(31, 29, 27))
            y += 44
        y += 22
    return img


if __name__ == "__main__":
    variants = {
        "q1_no_roller": dict(roller=False),
        "q2_no_figure": dict(figure=False, roller=False),
        "q3_no_floor": dict(floor_ev=False),
        "q5_minus20": dict(E=0.8),
        "q5_plus20": dict(E=1.2),
        "q6_pause": dict(action=False),
    }
    for name, kw in variants.items():
        img = with_text(build(**kw))
        img.save(os.path.join(SAMPLES, f"ablation_{name}.png"))
        print(name, "done")
