"""
ABOUT — the still figure. THE MAN seen from behind, clothed, standing.

For the /about right column: present while the text runs. No mirror, no
motion, no face — the back of a man in a plain shirt and trousers,
weight settled on the right leg. Economical made line (the Matisse/
Schmitz target): few marks, each committed, no tone, no construction
showing. Asymmetry is deliberate — left and right are placed by hand,
never mirrored.

Outputs:
  samples/about_figure_paper.png  — on plaster cream, for judging
  ../public/about/the-man-about.png — RGBA transparent, ink #1f1d1b, for web
"""
import os
import numpy as np
from PIL import Image, ImageDraw
from line_figure import stroke, SS

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(HERE, "samples")
WEB = os.path.normpath(os.path.join(HERE, "..", "public", "about"))
os.makedirs(SAMPLES, exist_ok=True)
os.makedirs(WEB, exist_ok=True)

W, H = 560, 1560
CX = 280
PAPER = np.array([241, 237, 229], float)
INK = np.array([31, 29, 27], float)  # #1f1d1b

# Figure bounds at cx: x in [cx-188, cx+188], y in [60, 1504].
FIG_TOP, FIG_BOTTOM = 60, 1504


def figure_strokes(cx, left_arm="down"):
    """THE MAN's stroke list, placed at horizontal center `cx`.
    Reused by about_scenes.py to stand him inside an environment.

    left_arm: "down" (canonical, default) or "raised" — reaching up-left,
    mid-task (scene D, the painter). The canonical figure is untouched
    when the default is used."""
    S = []
    def a(ctrl, w, lead=0.14, tail=0.2, swell=0.22, sm=0.6, cs=False, ce=False):
        S.append(dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                      smoothing=sm, cap_start=cs, cap_end=ce))

    # ---- HEAD, back view — one hair mass, nape line, ears tucked ----
    a([(cx-64, 200), (cx-72, 142), (cx-48, 80), (cx+4, 60), (cx+54, 78),
       (cx+74, 144), (cx+65, 198)], 2.4, swell=0.18)                   # skull/hair contour
    a([(cx-52, 184), (cx-20, 192), (cx+16, 192), (cx+54, 182)], 1.9,
      swell=0.1)                                                        # hair edge at the nape
    a([(cx-22, 88), (cx-30, 128), (cx-32, 168)], 0.9, swell=0.08)      # hair direction
    a([(cx+16, 84), (cx+22, 126), (cx+20, 166)], 0.9, swell=0.08)      # hair direction
    a([(cx-72, 156), (cx-81, 174), (cx-70, 190)], 1.4, swell=0.1)      # left ear
    a([(cx+74, 154), (cx+84, 172), (cx+72, 188)], 1.4, swell=0.1)      # right ear

    # ---- NECK into TRAPEZIUS (weight right: left shoulder rides higher) ----
    a([(cx-26, 202), (cx-27, 224), (cx-29, 244)], 1.8)
    a([(cx+27, 202), (cx+29, 224), (cx+31, 246)], 1.8)
    a([(cx-29, 244), (cx-88, 274), (cx-150, 306)], 2.6, swell=0.16)    # left trap/shoulder
    a([(cx+31, 246), (cx+88, 282), (cx+148, 316)], 2.6, swell=0.16)    # right trap/shoulder

    # ---- SHIRT — collar from behind bows up; sleeves; V-taper; tilted hem ----
    a([(cx-34, 240), (cx-2, 232), (cx+35, 242)], 1.4)                  # collar band (back arc)
    if left_arm == "down":
        # left arm (hangs close)
        a([(cx-150, 306), (cx-172, 346), (cx-180, 432), (cx-172, 524),
           (cx-161, 618), (cx-153, 696), (cx-149, 742)], 2.8, swell=0.2)   # outer sleeve
        a([(cx-124, 362), (cx-136, 454), (cx-141, 548), (cx-144, 648),
           (cx-146, 734)], 2.0, lead=0.22, swell=0.16)                      # inner sleeve
        a([(cx-166, 736), (cx-149, 741)], 1.1, cs=True, ce=True)           # cuff
    else:
        # left arm raised — reaching up-left to the work, mid-task.
        # A soft elbow bend; the two sleeve lines stay clearly apart so
        # the arm keeps its width all the way to the wrist.
        a([(cx-150, 306), (cx-202, 276), (cx-244, 240), (cx-270, 218)],
          2.8, swell=0.2)                                                   # outer sleeve
        a([(cx-124, 362), (cx-174, 326), (cx-222, 288), (cx-246, 262)],
          2.0, lead=0.22, swell=0.16)                                       # inner sleeve
        a([(cx-272, 220), (cx-250, 258)], 1.1, cs=True, ce=True)            # cuff
        # the shirt pulls with the reach — one diagonal fold
        a([(cx-118, 470), (cx-136, 398), (cx-146, 356)], 0.9, lead=0.25,
          tail=0.3, swell=0.08)
    # right arm (carries a few degrees away from the body)
    a([(cx+148, 316), (cx+175, 356), (cx+187, 442), (cx+184, 534),
       (cx+177, 630), (cx+169, 704), (cx+165, 748)], 2.8, swell=0.2)
    a([(cx+124, 370), (cx+141, 462), (cx+149, 556), (cx+153, 656),
       (cx+156, 740)], 2.0, lead=0.22, swell=0.16)
    a([(cx+158, 742), (cx+175, 747)], 1.1, cs=True, ce=True)
    # torso side seams — male V-taper: hem narrower than the chest
    a([(cx-122, 366), (cx-116, 480), (cx-110, 580), (cx-112, 680),
       (cx-116, 766)], 2.2, swell=0.18)
    a([(cx+122, 372), (cx+118, 486), (cx+112, 586), (cx+114, 684),
       (cx+118, 754)], 2.2, swell=0.18)
    a([(cx-116, 766), (cx-44, 772), (cx+38, 766), (cx+118, 754)], 1.8,
      swell=0.12)                                                       # hem, right hip high
    a([(cx+10, 316), (cx+4, 404), (cx+8, 482)], 0.9, lead=0.3, tail=0.34,
      swell=0.08)                                                       # one quiet back fold

    # ---- HANDS — compact, blunt-bottomed, no taper to a point ----
    if left_arm == "down":
        a([(cx-149, 742), (cx-155, 770), (cx-152, 796), (cx-143, 806),
           (cx-134, 800), (cx-132, 778)], 1.6, swell=0.1)
    else:
        # raised hand — a compact fist around the handle, real mass
        a([(cx-270, 218), (cx-290, 210), (cx-298, 192), (cx-290, 174),
           (cx-272, 172), (cx-262, 186)], 1.7, swell=0.1)
        a([(cx-288, 198), (cx-272, 194)], 0.9, swell=0.06)                  # knuckle line
    a([(cx+165, 748), (cx+171, 778), (cx+167, 804), (cx+157, 813),
       (cx+148, 806), (cx+147, 784)], 1.6, swell=0.1)

    # ---- TROUSERS — right leg plumb under the hip; left settles inward ----
    # right (weight) outer: near-vertical drop
    a([(cx+118, 754), (cx+118, 900), (cx+113, 1070), (cx+109, 1240),
       (cx+106, 1390), (cx+105, 1448)], 2.6, swell=0.16)
    # left (free) outer: angles in, soft knee break
    a([(cx-116, 766), (cx-114, 900), (cx-105, 1060), (cx-106, 1100),
       (cx-97, 1240), (cx-88, 1380), (cx-85, 1452)], 2.6, swell=0.18)
    # inner lines from under the hem
    a([(cx+14, 794), (cx+27, 956), (cx+37, 1124), (cx+43, 1296),
       (cx+46, 1448)], 2.2, lead=0.18, swell=0.16)
    a([(cx-6, 794), (cx-16, 950), (cx-24, 1110), (cx-28, 1170),
       (cx-25, 1300), (cx-22, 1452)], 2.2, lead=0.18, swell=0.16)
    # trouser break
    a([(cx-86, 1446), (cx-24, 1452)], 1.1, cs=True, ce=True)
    a([(cx+104, 1444), (cx+48, 1448)], 1.1, cs=True, ce=True)

    # ---- SHOES from behind — heels, low and flat; free heel drifts out ----
    a([(cx-88, 1452), (cx-96, 1478), (cx-86, 1490), (cx-32, 1492),
       (cx-22, 1480), (cx-23, 1454)], 1.8, swell=0.1)
    a([(cx-90, 1478), (cx-26, 1482)], 0.9, cs=True, ce=True)           # heel seam
    a([(cx+104, 1450), (cx+110, 1476), (cx+100, 1488), (cx+50, 1490),
       (cx+42, 1478), (cx+44, 1450)], 1.8, swell=0.1)
    a([(cx+108, 1476), (cx+46, 1480)], 0.9, cs=True, ce=True)

    return S


def render_strokes(S, w_img, h_img):
    """Stroke list -> alpha array in [0,1] at (h_img, w_img)."""
    im = Image.new("L", (w_img*SS, h_img*SS), 0)
    d = ImageDraw.Draw(im)
    for s in S:
        stroke(d, **s)
    return np.asarray(im.resize((w_img, h_img), Image.LANCZOS), float) / 255.0


def save_paper(fa, path, paper=PAPER, ink=INK):
    h_img, w_img = fa.shape
    out = np.ones((h_img, w_img, 3)) * paper
    out = out * (1 - fa[..., None]) + ink * fa[..., None]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(path)


def save_web(fa, path, ink=INK):
    h_img, w_img = fa.shape
    rgba = np.zeros((h_img, w_img, 4), np.uint8)
    rgba[..., 0:3] = ink.astype(np.uint8)
    rgba[..., 3] = (fa * 255).astype(np.uint8)
    Image.fromarray(rgba).save(path)


if __name__ == "__main__":
    fa = render_strokes(figure_strokes(CX), W, H)
    save_paper(fa, os.path.join(SAMPLES, "about_figure_paper.png"))
    save_web(fa, os.path.join(WEB, "the-man-about.png"))
    print("done")
