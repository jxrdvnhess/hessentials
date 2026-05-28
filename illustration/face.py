"""
Hessentials — construction-based face illustrator (v2).

Lesson from the sources (Simonetti face method + illustration fundamentals):
a face reads as ALIVE and EMOTIONAL when a loose hand wanders over CORRECT
structure — not random wander, and not vector-clean symmetry. So:

  1) build a proportioned armature  (sphere implied; three equal thirds
     hairline-brow-nosebase-chin; eyes one-eye-width apart, five across)
  2) POSE it with emotion controls   (gaze, brow obliqueness, lids, mouth, tilt)
  3) draw a single living line over it (low tremor + slow drift, slight
     overshoot, variable weight) on woven linen.

Construction underneath, life on top. This is the illustrator's path and it
resolves the rubric: structure is allowed; mechanical symmetry is the failure.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
from linen import linen_ground, ink_on_linen, stroke_alpha, short_hatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(OUT, exist_ok=True)
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

# ----------------------------------------------------------------- curve helpers
def catmull(ctrl, n=22):
    """Smooth polyline through control pts (Catmull-Rom)."""
    p = np.array(ctrl, float)
    if len(p) < 3:
        return p
    p = np.vstack([p[0], p, p[-1]])
    out = []
    for i in range(1, len(p)-2):
        p0, p1, p2, p3 = p[i-1], p[i], p[i+1], p[i+2]
        t = np.linspace(0, 1, n)[:, None]
        out.append(0.5*((2*p1) + (-p0+p2)*t +
                   (2*p0-5*p1+4*p2-p3)*t**2 + (-p0+3*p1-3*p2+p3)*t**3))
    return np.vstack(out)

def living(pts, rng, jit=0.5, drift=1.8, overshoot=0.0):
    """Offset a smooth polyline along its normals with slow drift (proportion
    wander) + cumulative hand tremor (detrended). Optional overshoot at the end."""
    pts = np.array(pts, float)
    n = len(pts)
    d = np.gradient(pts, axis=0)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6)
    t = np.linspace(0, 1, n)
    lf = (np.sin(t*np.pi*rng.uniform(0.6, 1.5)+rng.uniform(0, 6))*rng.uniform(0.5, 1.0)
          + np.sin(t*np.pi*rng.uniform(1.4, 2.6)+rng.uniform(0, 6))*rng.uniform(0.2, 0.4))
    hf = np.cumsum(rng.normal(0, jit, n)); hf -= np.linspace(hf[0], hf[-1], n)
    off = (lf*drift + hf*0.55)[:, None] * nrm
    out = pts + off
    if overshoot:
        ext = out[-1] + (out[-1]-out[-2]) * np.arange(1, int(overshoot*12)+1)[:, None]
        out = np.vstack([out, ext])
    return out

# ----------------------------------------------------------------- the face
def face(emotion, seed=0, tilt=-4, turn=0.10):
    """Return list of (polyline, width) in local units (face center origin,
    head height 1). emotion: dict of pose params 0..1 / -1..1."""
    rng = np.random.default_rng(seed)
    e = emotion
    gaze   = e.get("gaze_down", 0.5)      # 0 level, 1 fully down
    lid    = e.get("lid_open", 0.7)       # 1 wide, 0 closed
    browin = e.get("brow_inner", 0.4)     # inner-brow raise (sadness oblique)
    browht = e.get("brow_height", 0.0)    # overall brow raise
    mcurve = e.get("mouth_curve", -0.1)   # -down .. +up
    mopen  = e.get("mouth_open", 0.10)
    lips   = e.get("lip_full", 1.0)

    # vertical landmarks (y down). thirds hairline->brow->nosebase->chin
    hair, brow, nbase, chin = -0.50, -0.17, 0.16, 0.50
    eye_y = brow + (nbase-brow)*0.34
    third = (chin-hair)/3
    # widths
    fw = 0.62                              # face width at cheekbone
    ew = fw/5.0                            # one eye width
    polys = []
    # add() now stores the CLEAN smooth armature + a life factor + width.
    # The living-line wobble is applied later in render(), in pixel space.
    def add(ctrl, w, n=22, life=1.0, ov=0.0):
        polys.append((catmull(ctrl, n), w, life, ov))

    # ---- jaw / cheek outline (soft, slightly open at top = hair implied) ----
    L = -fw/2; R = fw/2
    add([(L*0.95, brow-0.02), (L, eye_y+0.04), (L*0.92, nbase+0.02),
         (L*0.55, chin*0.86), (0.0, chin), (R*0.55, chin*0.86),
         (R*0.92, nbase+0.02), (R, eye_y+0.04), (R*0.95, brow-0.02)],
        w=2.2, n=26, life=1.3)

    # ---- brows (emotion: inner raise + arch) ----
    bi = browin*0.075                      # inner end lifts (sadness oblique)
    by = brow - browht*0.05
    jl, jr = rng.normal(0, 0.010), rng.normal(0, 0.010)   # brows don't agree
    # inner ends high + outer ends low = the classic melancholy oblique
    add([(-ew*0.28, by-bi+jl), (-ew*0.85, by-0.040+jl), (-ew*1.55, by+0.005+jl)],
        w=2.1, n=14, life=0.8)
    add([( ew*0.28, by-bi+jr), ( ew*0.85, by-0.040+jr), ( ew*1.55, by+0.005+jr)],
        w=2.1, n=14, life=0.8)
    for p, ww in short_hatch((-ew*0.95, by-0.03), ew*0.9, 6, 0.15, rng, length=0.022):
        polys.append((np.array(p, float), ww, 0.0, 0.0))
    for p, ww in short_hatch(( ew*0.95, by-0.03), ew*0.9, 6, -0.15, rng, length=0.022):
        polys.append((np.array(p, float), ww, 0.0, 0.0))

    # ---- eyes (expressive; misregistered for life) ----
    # per-eye misregistration: the two eyes don't perfectly agree (the alive
    # tell), but they sit on a real eye-line (the structure).
    mis = [(rng.normal(0, 0.012), rng.normal(0, 0.010), rng.uniform(0.93, 1.07))
           for _ in range(2)]
    def eye(cx, m):
        dx, dy, sc = m
        cx += dx; ey = eye_y + dy; w_ = ew*0.58*sc
        if lid < 0.22:
            # CLOSED / serene — a calm downward lash crease, a few lashes
            add([(cx-w_, ey-0.002), (cx-w_*0.2, ey+0.020), (cx+w_*0.5, ey+0.018),
                 (cx+w_, ey-0.004)], w=2.1, n=16, life=0.5)
            for k in range(3):
                f = (k-1)*0.4
                add([(cx+f*w_, ey+0.016), (cx+f*w_-0.004, ey+0.034)], w=1.3, n=4, life=0.3)
            return
        op = (0.024 + lid*0.040)
        up = ey - op*(1-gaze*0.55)          # upper lid lowers with downcast gaze
        lo = ey + op*0.62
        # upper lid — heavier (illustration convention), arcs lower when downcast
        add([(cx-w_, ey+0.003), (cx-w_*0.25, up), (cx+w_*0.35, up*0.999+0.001),
             (cx+w_, ey+0.004)], w=2.5, n=16, life=0.5)
        add([(cx-w_, ey+0.003), (cx-w_*0.10, lo), (cx+w_*0.40, lo),
             (cx+w_, ey+0.004)], w=1.4, n=16, life=0.45)
        # iris — sits low for downcast, tucked under the upper lid
        ir_y = ey + gaze*op*0.7 - 0.004
        add([(cx-w_*0.30, ir_y-0.004), (cx-w_*0.32, ir_y+0.010),
             (cx, ir_y+0.014), (cx+w_*0.32, ir_y+0.010), (cx+w_*0.30, ir_y-0.004)],
            w=1.6, n=12, life=0.3)
    eye(-ew*1.0, mis[0]); eye(ew*1.0, mis[1])

    # ---- nose (minimal: bridge shadow + nostril hook) ----
    add([(-ew*0.10, brow+0.02), (-ew*0.16, eye_y+0.05),
         (-ew*0.20, nbase-0.02), (-ew*0.02, nbase+0.01)], w=1.8, n=16, life=0.8)
    add([(-ew*0.02, nbase+0.01), (ew*0.10, nbase+0.02), (ew*0.16, nbase-0.02)],
        w=1.6, n=8, life=0.5)

    # ---- lips (cupid + lower; curvature = emotion) ----
    my = nbase + (chin-nbase)*0.46
    lw = ew*1.05*lips
    corner_dy = -mcurve*0.045               # corners up smile / down sad
    add([(-lw, my+corner_dy), (-lw*0.4, my-0.018), (0, my-0.006*lips),
         (lw*0.4, my-0.018), (lw, my+corner_dy)], w=2.0, n=18, life=0.6)
    add([(-lw, my+corner_dy), (-lw*0.4, my+0.018+mopen),
         (0, my+0.030*lips+mopen), (lw*0.4, my+0.018+mopen), (lw, my+corner_dy)],
        w=1.7, n=18, life=0.6)

    # ---- pose: tilt + slight turn ----
    th = np.deg2rad(tilt); ct, st = np.cos(th), np.sin(th)
    out = []
    for pl, w, life, ov in polys:
        p = np.array(pl, float)
        p[:, 0] *= (1 - turn*0.5)
        p[:, 0] += turn*0.18*(p[:, 1])
        x = p[:, 0]*ct - p[:, 1]*st
        y = p[:, 0]*st + p[:, 1]*ct
        out.append((np.stack([x, y], 1), w, life, ov))
    return out

def render(emotion, w=1500, h=1100, seed=0, scale=0.46, pos=(0.52, 0.48),
           tilt=-4, turn=0.10, tone=0.0):
    rng = np.random.default_rng(seed*3+1)
    polys = face(emotion, seed, tilt, turn)
    Hh = h*scale
    cx, cy = w*pos[0], h*pos[1]
    px = []
    for pl, ww, life, ov in polys:
        pts = np.stack([cx + pl[:, 0]*Hh, cy + pl[:, 1]*Hh], 1)
        if life > 0:
            # living-line wobble in PIXEL space (tuned scale): slow drift +
            # detrended tremor, proportional to head size.
            drift = life * (Hh/520.0) * 4.0
            jit   = life * 0.55
            pts = living(pts, rng, jit=jit, drift=drift, overshoot=ov)
        width = max(1.6, ww*(Hh/520.0))
        px.append(([(float(x), float(y)) for x, y in pts], width))
    a = stroke_alpha(w, h, px, width=1.0, jitterblur=0.6)
    linen = linen_ground(w, h, seed=seed*7+5, tone=tone)
    out = ink_on_linen(linen, np.clip(a*0.92, 0, 1))
    return Image.fromarray(out.astype(np.uint8))

# emotion presets — translating LANGUAGE into pose
EMOTIONS = {
    # pushed so each reads at a glance: gaze/lid carry repose, brow_inner the
    # sadness oblique, mouth the warmth.
    "melancholy": dict(gaze_down=1.0, lid_open=0.40, brow_inner=1.0,
                       brow_height=-0.2, mouth_curve=-0.35, mouth_open=0.0, lip_full=1.0),
    "serene":     dict(gaze_down=1.0, lid_open=0.10, brow_inner=0.30,
                       brow_height=0.05, mouth_curve=0.10, mouth_open=0.0, lip_full=1.05),
    "tender":     dict(gaze_down=0.40, lid_open=0.75, brow_inner=0.55,
                       brow_height=0.10, mouth_curve=0.45, mouth_open=0.03, lip_full=1.15),
    "pensive":    dict(gaze_down=0.55, lid_open=0.65, brow_inner=0.85,
                       brow_height=-0.10, mouth_curve=-0.12, mouth_open=0.05, lip_full=0.95),
}

if __name__ == "__main__":
    # 1) emotion strip (same construction seed, square crops)
    strip_imgs = []
    for name, em in EMOTIONS.items():
        im = render(em, w=620, h=720, seed=9, scale=0.62, pos=(0.5, 0.46),
                    tilt=-3, turn=0.08)
        d = ImageDraw.Draw(im); f = ImageFont.truetype(SERIF, 30)
        d.text((26, 660), name, font=f, fill=(40, 37, 34))
        im.save(f"{OUT}/emo_{name}.png"); strip_imgs.append(im)
    sp = 14; cw, ch = 620, 720
    strip = Image.new("RGB", (cw*4+sp*5, ch+sp*2), (236, 230, 220))
    for i, im in enumerate(strip_imgs):
        strip.paste(im, (sp+i*(cw+sp), sp))
    strip.save(f"{OUT}/emotion_strip.png")

    # 2) refined close candidate (melancholy/repose) at panel size + poem line
    im = render(EMOTIONS["melancholy"], w=1500, h=1100, seed=14,
                scale=0.50, pos=(0.60, 0.50), tilt=-5, turn=0.12)
    d = ImageDraw.Draw(im); f = ImageFont.truetype(SERIF, 60)
    ink = (31, 29, 27); x, y = int(1500*0.085), int(1100*0.36)
    d.text((x, y), "This is what stayed.", font=f, fill=ink)
    tb = d.textbbox((x, y), "This is what stayed.", font=f)
    d.line([(x, tb[3]+22), (x+80, tb[3]+22)], fill=ink, width=2)
    im.save(f"{OUT}/CLOSE_melancholy.png")
    print("done:", sorted(os.listdir(OUT)))
