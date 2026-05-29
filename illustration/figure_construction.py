"""
STAGE 3 — figure construction. The reclined-gazing-up gesture built into a
believable body as proportioned Loomis masses.

THE BELIEVABLE GATE (its own test, so it can't be graded around — the lesson:
a list of true small fixes is not a believable whole). Run ALL THREE before
calling a body believable:
  1. proportion in heads — ~7-8 heads, limbs in proportion, not stretched/thin.
  2. name the masses — point to a ribcage, a PELVIS, a thigh as distinct volumes.
  3. squint test — squint at the silhouette; say "human" or "insect" out loud.
The previous pass failed all three (too long/thin, no pelvis, insectile). Build
the body from real masses with real thickness so it survives them.

THE ALIVE GATE (kept from stage 2): hide the head; the reclined attitude must
still hold. Believable AND alive, both, or it isn't a pass.
"""
import os
import numpy as np
from line_figure import render

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1200, 1000
HEAD = 100.0   # one head-height; the unit the whole figure is proportioned in

def ellipse_poly(cx, cy, a, b, ang, n=30):
    t = np.linspace(0, 2*np.pi, n)
    x, y = a*np.cos(t), b*np.sin(t)
    ca, sa = np.cos(ang), np.sin(ang)
    return list(zip((cx+x*ca-y*sa).tolist(), (cy+x*sa+y*ca).tolist()))

def capsule(p0, p1, r0, r1, n=10):
    """Outline of a tapered limb (a stadium): radius r0 at p0, r1 at p1."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1-p0; ang = np.arctan2(d[1], d[0]); L = float(np.hypot(*d))
    local = [(0, r0), (L, r1)]
    local += [(L+r1*np.cos(a), r1*np.sin(a)) for a in np.linspace(np.pi/2, -np.pi/2, n)]  # far cap
    local += [(0, -r0)]
    local += [(r0*np.cos(a), r0*np.sin(a)) for a in np.linspace(-np.pi/2, -3*np.pi/2, n)] # near cap
    ca, sa = np.cos(ang), np.sin(ang)
    return [ (p0[0]+x*ca-y*sa, p0[1]+x*sa+y*ca) for (x, y) in local ]

def reclined_body(hide_head=False):
    """Reclined, propped back on the left arm, legs extended right, head tipped
    back gazing up. Masses sized in head-units (HEAD=100): ribcage ~1.6H,
    pelvis ~1H, thigh ~2H, etc., with real thickness so it reads human."""
    S = []
    OUT_W = 5     # mass outline weight
    def mass(pts, w=OUT_W):  S.append(dict(ctrl=pts+[pts[0]], w=w, smoothing=0.62, swell=0.12))
    def limb(p0,p1,r0,r1,w=OUT_W): S.append(dict(ctrl=capsule(p0,p1,r0,r1), w=w, smoothing=0.6, swell=0.12))

    # --- joints (reclined diagonal; facing left, legs extend right) ---
    head_c=(360,298)
    shoulder=(414,392); waist=(508,548); crotch=(572,632)
    hip_n=(578,616); hip_f=(560,634)
    knee_n=(764,654); ankle_n=(902,708)
    knee_f=(736,694); ankle_f=(866,746)
    elbowP=(366,506); wristP=(322,642)            # propping arm (weight-bearing)
    elbowN=(492,540); handN=(616,628)             # near arm rests on the lap/thigh

    # --- torso masses (the missing pelvis is now a real mass) ---
    mass(ellipse_poly((shoulder[0]+waist[0])/2+6,(shoulder[1]+waist[1])/2,80,56,
                      np.arctan2(waist[1]-shoulder[1],waist[0]-shoulder[0])), w=6)   # RIBCAGE egg ~1.6H
    mass(ellipse_poly((waist[0]+crotch[0])/2,(waist[1]+crotch[1])/2,52,48,
                      np.arctan2(crotch[1]-waist[1],crotch[0]-waist[0])), w=6)        # PELVIS ~1H (real)
    # --- legs: thick weighted tubes (thigh ~2H, real thickness) ---
    limb(hip_n,knee_n,30,24); limb(knee_n,ankle_n,23,16)        # near leg
    limb((ankle_n[0],ankle_n[1]),(ankle_n[0]+34,ankle_n[1]+6),15,7)   # near foot
    limb(hip_f,knee_f,28,22); limb(knee_f,ankle_f,21,15)        # far leg (behind/lower)
    limb((ankle_f[0],ankle_f[1]),(ankle_f[0]+32,ankle_f[1]+6),14,7)   # far foot
    # --- propping arm: thick enough to bear the recline ---
    limb(shoulder,elbowP,24,20); limb(elbowP,wristP,20,15)
    for i,dx in enumerate((-10,0,10,20)):                       # planted hand, fingers
        S.append(dict(ctrl=[(wristP[0]+dx-6,wristP[1]+8),(wristP[0]+dx-10,wristP[1]+34)],
                      w=4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))
    # --- near arm resting forward on the thigh ---
    limb((426,406),elbowN,21,16); limb(elbowN,handN,16,11)
    # --- head + neck (tipped back, gazing up; no face) ---
    if not hide_head:
        limb(shoulder,(388,352),18,16)                          # neck
        mass(ellipse_poly(head_c[0],head_c[1],42,50,-0.18), w=6) # head
        S.append(dict(ctrl=[(340,266),(372,262),(392,286)], w=4.5, lead=0.2, tail=0.3, swell=0.5, smoothing=0.7))  # hair
    # --- the line of action drawn through the back (keeps it alive) ---
    S.append(dict(ctrl=[(404,372),(452,470),(520,560),(576,628)], w=7, lead=0.1, tail=0.16, swell=0.4, smoothing=0.72))
    return S, []

if __name__ == "__main__":
    S,_ = reclined_body(False)
    render(S, [], W, H, render_on_linen=True,  seed=4).save(f"{OUT}/stage3_body_linen.png")
    render(S, [], W, H, render_on_linen=False, seed=4).save(f"{OUT}/stage3_body_bare.png")
    Sh,_ = reclined_body(True)
    render(Sh, [], W, H, render_on_linen=False, seed=4).save(f"{OUT}/stage3_body_headless.png")
    print("done")
