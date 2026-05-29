"""
STAGE 2 — gesture & line of action.  (Rebuilt after the legibility correction.)

The fundamental, corrected: a gesture is the clearest possible read of ONE
motion in the fewest marks. It is built on a SINGLE dominant line of action —
the strongest directional curve, found by squinting and laid down first —
with everything else subordinate to it. Not a bundle of equal flowing lines
(that swing into looseness lost the pose); one curve that carries the thrust.

Procedure: `action` is one heavy stroke. `secondary` is a few light, thin marks
that never compete. The head is a small mark, omittable.

THE GATE (encoded, run automatically — this is how we stop grading kindly):
  1. three-word name: can the pose be named at a glance — "slumped, weary,
     forward" — and would someone else name it the same?
  2. head-covered read: hide the head; the same named attitude must still hold.
  A pose passes only if both are yes. Legible beats pretty. Loose is allowed;
  ambiguous is not. Reps until first-look legibility is reliable, not lucky.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from line_figure import stroke, SS, INK
from linen import linen_ground

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
CW, CH = 440, 580

def ellipse_poly(cx, cy, a, b, ang, n=26):
    t = np.linspace(0, 2*np.pi, n)
    x, y = a*np.cos(t), b*np.sin(t)
    ca, sa = np.cos(ang), np.sin(ang)
    X = cx + x*ca - y*sa; Y = cy + x*sa + y*ca
    return list(zip(X.tolist(), Y.tolist()))

# Each pose: ONE action line (the thrust) + a few subordinate marks + a head.
GESTURES = [
    dict(name="slumped · weary · forward",
         action=[(250,452),(286,344),(268,236),(196,250)],          # hips up rounded back, head falls forward
         secondary=[[(252,456),(326,486)], [(326,486),(330,520)],   # thigh, shin
                    [(262,262),(286,372)]],                          # arm hanging
         head=(190,250,24,28,0.45)),
    dict(name="reaching · up · open",
         action=[(224,470),(238,344),(250,256),(312,150),(348,108)], # base up through body to raised hand
         secondary=[[(224,470),(214,520)], [(250,268),(226,372)]],   # leg, lower arm
         head=(224,242,22,26,0.0)),
    dict(name="reclined · loose · gazing-up",
         action=[(372,476),(298,448),(232,436),(200,360),(216,300)], # extended feet -> reclined torso -> head tipped back
         secondary=[[(206,366),(170,446),(160,508)],                 # propping arm behind
                    [(236,388),(296,428)]],                          # near arm rest
         head=(214,294,24,26,-0.30)),
    dict(name="curled · inward · small",
         action=[(232,300),(296,332),(286,424),(208,402),(214,486)], # head down, round back, knees up, shins down
         secondary=[[(252,360),(214,408)]],                          # arm hugging knees
         head=(224,300,22,24,0.35)),
    dict(name="striding · forward · driven",
         action=[(150,500),(232,360),(300,182)],                     # trailing foot up through leaning body to head
         secondary=[[(262,360),(330,486)], [(268,300),(228,360)], [(268,300),(338,332)]],  # front leg, two arms
         head=(304,180,22,26,-0.1)),
    dict(name="standing · weight-shift · easy",
         action=[(232,176),(252,300),(238,372),(244,500)],           # gentle S through a relaxed standing figure
         secondary=[[(244,372),(292,498)], [(238,300),(206,392)], [(252,300),(286,388)]],  # relaxed leg, two arms
         head=(232,170,22,26,0.0)),
]

def render_gesture(pose, headless=False, seed=0, label=True):
    main = Image.new("L", (CW*SS, CH*SS), 0); d = ImageDraw.Draw(main)
    stroke(d, ctrl=[(60,CH-72),(CW-60,CH-72)], w=2.2, cap_start=True, cap_end=True, swell=0, smoothing=0.95)  # floor
    for sec in pose["secondary"]:
        stroke(d, ctrl=sec, w=5.5, lead=0.16, tail=0.22, swell=0.3, smoothing=0.7)   # subordinate, thin
    stroke(d, ctrl=pose["action"], w=14, lead=0.07, tail=0.14, swell=0.45, smoothing=0.7)  # the dominant action line
    if not headless:
        cx,cy,a,b,ang = pose["head"]
        stroke(d, ctrl=ellipse_poly(cx,cy,a,b,ang), w=5, smoothing=0.9, swell=0.18)
    a_img = np.asarray(main.resize((CW,CH), Image.LANCZOS), float)/255.0
    linen = linen_ground(CW, CH, seed=seed, tone=0.25)
    out = linen*(1-a_img[...,None]) + INK*a_img[...,None]
    im = Image.fromarray(np.clip(out,0,255).astype(np.uint8))
    if label:
        dd = ImageDraw.Draw(im); f = ImageFont.truetype(SERIF, 21)
        txt = pose["name"] + ("   (head hidden)" if headless else "")
        dd.text((22, CH-38), txt, font=f, fill=(64,58,52))
    return im

def tile(images, cols):
    rows = (len(images)+cols-1)//cols; pad = 12
    w, h = images[0].size
    sheet = Image.new("RGB", (w*cols+pad*(cols+1), h*rows+pad*(rows+1)), (236,230,220))
    for i, im in enumerate(images):
        r, c = divmod(i, cols)
        sheet.paste(im, (pad+c*(w+pad), pad+r*(h+pad)))
    return sheet

if __name__ == "__main__":
    reps = [render_gesture(p, seed=i+1) for i,p in enumerate(GESTURES)]
    tile(reps, 3).save(f"{OUT}/stage2_reps.png")
    # the gate: head-covered read for the same poses
    hid = [render_gesture(p, headless=True, seed=i+1) for i,p in enumerate(GESTURES)]
    tile(hid, 3).save(f"{OUT}/stage2_reps_headless.png")
    print("done")
