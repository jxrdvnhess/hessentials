"""
Step 1 — the single economical figure. Confident MADE line, not traced, not
scratch, not timid. Few marks, each committed. Charcoal-like: tapered ends,
pressure-varying weight, an occasional faint searching second pass.

For this proving exercise: monochrome line on bare ground. (The finished work
comes home to warm linen — see render_on_linen flag.)

The figure has an attitude, not a pose: seated, turned away, head looking back
over the shoulder — #12's charge from a single body. No rendered face.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
os.makedirs(OUT, exist_ok=True)
SS = 3
INK = np.array([26, 23, 27], float)

def catmull(ctrl, n=48):
    p = np.array(ctrl, float)
    if len(p) < 3:
        return p
    p = np.vstack([p[0], p, p[-1]])
    out = []
    for i in range(1, len(p)-2):
        p0,p1,p2,p3 = p[i-1],p[i],p[i+1],p[i+2]
        t = np.linspace(0,1,n)[:,None]
        out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t**2+(-p0+3*p1-3*p2+p3)*t**3))
    return np.vstack(out)

def smootherstep(x):
    x = np.clip(x,0,1); return x*x*x*(x*(x*6-15)+10)

def stroke(draw, ctrl, w, lead=0.10, tail=0.16, swell=0.35, swell_k=1.3,
           phase=0.0, cap_start=False, cap_end=False, smoothing=0.5):
    """Stamp a tapered, pressure-varying ribbon along a centerline.
    cap_start/cap_end: end at full weight (a confident crop).
    smoothing: 1.0 = fully spline-fitted (graceful); lower = stay closer to the
    committed control points (direct, un-sanded). Trust the first mark."""
    P = catmull(ctrl, n=46)
    cp = np.array(ctrl, float)
    if len(cp) >= 2 and smoothing < 0.999:
        d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(cp,axis=0),axis=1))]
        if d[-1] > 0:
            tt = np.linspace(0, d[-1], len(P))
            lin = np.stack([np.interp(tt,d,cp[:,0]), np.interp(tt,d,cp[:,1])],1)
            P = smoothing*P + (1-smoothing)*lin   # blend toward the direct gesture
    # resample to ~1px spacing along the WHOLE length so strokes of any length
    # stay solid. (Short fingers were stamping only endpoints -> two dots; long
    # thin lines were stamping too sparsely -> a dotted/stippled line. Both fixed
    # by spacing the stamps by length, not by a fixed point count.)
    dd = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P,axis=0),axis=1))]
    if dd[-1] > 0:
        npts = int(min(6000, max(len(P), dd[-1]/1.1)))
        tt = np.linspace(0, dd[-1], npts)
        P = np.stack([np.interp(tt,dd,P[:,0]), np.interp(tt,dd,P[:,1])], 1)
    N = len(P)
    for i,(x,y) in enumerate(P):
        t = i/(N-1)
        up = 1.0 if cap_start else smootherstep(np.clip(t/lead,0,1))
        dn = 1.0 if cap_end   else smootherstep(np.clip((1-t)/tail,0,1))
        env = min(up, dn)
        pressure = 1 + swell*np.sin(t*np.pi*swell_k + phase)
        r = max(0.9*SS if (cap_start and t<0.02) or (cap_end and t>0.98) else 0.5,
                0.5*w*env*pressure*SS)
        draw.ellipse([x*SS-r, y*SS-r, x*SS+r, y*SS+r], fill=255)

def render(strokes, ghosts, w_img, h_img, render_on_linen=False, seed=0):
    main = Image.new("L",(w_img*SS,h_img*SS),0); md=ImageDraw.Draw(main)
    gho  = Image.new("L",(w_img*SS,h_img*SS),0); gd=ImageDraw.Draw(gho)
    for s in strokes: stroke(md, **s)
    for s in ghosts:  stroke(gd, **s)
    a_main = np.asarray(main.resize((w_img,h_img),Image.LANCZOS),float)/255.0
    a_gho  = np.asarray(gho.resize((w_img,h_img),Image.LANCZOS),float)/255.0
    alpha = np.clip(np.maximum(a_main, a_gho*0.34), 0, 1)
    # a whisper of charcoal grain so the line is "made", not vector-flat
    rng = np.random.default_rng(seed)
    grain = rng.normal(0,1,(h_img,w_img))
    grain = np.asarray(Image.fromarray(((grain-grain.min())/(np.ptp(grain)+1e-6)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)),float)/255.0
    alpha = np.clip(alpha*(0.85+0.30*grain), 0, 1)
    if render_on_linen:
        from linen import linen_ground
        ground = linen_ground(w_img,h_img,seed=seed,tone=0.3)
    else:
        ground = np.full((h_img,w_img,3), np.array([245,241,234.]))   # bare warm ground
    out = ground*(1-alpha[...,None]) + INK*alpha[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

# ---------------------------------------------------------------- the figure
W,H = 1150, 1200

def figure_seated():
    """Sitting curled on the ground: knees drawn up, an arm around them, the back
    a true line of action, the head resting on that curve. Real weight, real
    lower half — a posture that carries feeling on its own. Tender and a little
    awkward, not elegant. Ends crop with confidence; no fade, no shadow."""
    S = []
    # 1) LINE OF ACTION — the back, seat up to the neck (the gesture's spine)
    S.append(dict(ctrl=[(548,1004),(566,884),(548,762),(506,672),(490,628)], w=11,
                  tail=0.18, swell=0.42, cap_start=True))
    # 2) neck into the back of the skull, over the crown
    S.append(dict(ctrl=[(490,628),(508,560),(494,496),(452,472),(430,500)], w=8,
                  lead=0.10, tail=0.20, swell=0.35))
    # 3) forehead -> cheek -> jaw, back to the neck (open face, nothing inside)
    S.append(dict(ctrl=[(430,500),(424,548),(442,588),(478,602),(498,628)], w=6.5,
                  lead=0.16, tail=0.28, swell=0.3, phase=0.6))
    # 4) hair knot — a couple of confident loops at the crown
    S.append(dict(ctrl=[(452,472),(486,464),(508,488),(504,520)], w=6,
                  lead=0.2, tail=0.3, swell=0.5, phase=1.0))
    # 5) the closed eye — one mark
    S.append(dict(ctrl=[(434,548),(448,544),(460,549)], w=3.8, lead=0.3, tail=0.3, swell=0.2))
    # 6) front of the body — chest curving down toward the knee
    S.append(dict(ctrl=[(482,640),(506,776),(484,884)], w=8,
                  lead=0.16, tail=0.26, swell=0.35, phase=1.0))
    # 7) the bent leg as ONE clean contour — front of thigh up to the knee peak,
    #    then down the shin to the foot, cropped firmly at the ground
    S.append(dict(ctrl=[(484,886),(410,838),(398,930),(432,1010)], w=8.5,
                  lead=0.16, swell=0.4, cap_end=True))
    # 8) the arm wrapping the knee — shoulder down to the hand resting at the knee
    S.append(dict(ctrl=[(498,666),(452,784),(414,846),(392,842)], w=7.5,
                  lead=0.16, tail=0.36, swell=0.35, phase=2.0))
    # 9) seat / ground contact — a short flat tick of weight (no bell, no skirt)
    S.append(dict(ctrl=[(552,1012),(508,1018),(470,1012)], w=7,
                  swell=0.15, cap_start=True, cap_end=True))
    return S, []

def figure_embrace():
    """A tight, overlapping embrace (cf. #3, #6, #9). A is the near figure, back
    to us, head turned to rest toward B. B is behind A's right shoulder, head
    nestled over it and tilted down. B's arm drapes OVER A's shoulder and the
    hand hangs down A's back, fingers resting — full weight, the charge. The
    bodies OVERLAP (no gap to cross), B mostly occluded by A. Cropped at the
    chest. Smooth weighted arm; the line stays committed elsewhere."""
    S = []
    sm = 0.5      # bodies/heads: committed, un-sanded
    aw = 0.82     # arm: a limb flows, so smoother
    # ===== A — near figure, back to us, leaning RIGHT into B (the fold) =====
    S.append(dict(ctrl=[(498,470),(512,406),(488,360),(446,362),(430,410),(438,460)], w=8, lead=0.10, tail=0.20, swell=0.35, smoothing=sm))  # back of A's head
    S.append(dict(ctrl=[(446,362),(486,356),(512,380)], w=5.5, lead=0.22, tail=0.3, swell=0.5, phase=1.0, smoothing=sm))             # A hair
    S.append(dict(ctrl=[(444,500),(500,494),(556,516)], w=8, lead=0.16, tail=0.18, swell=0.3, smoothing=sm))                         # A shoulders (back)
    S.append(dict(ctrl=[(444,506),(454,612),(478,704)], w=10, lead=0.12, swell=0.42, cap_end=True, smoothing=sm))                    # A left side — slight inward lean, cropped short (less body)
    S.append(dict(ctrl=[(560,520),(582,612),(596,704)], w=10, lead=0.14, swell=0.42, cap_end=True, smoothing=sm))                    # A right side, cropped short
    # ===== B — behind A's right shoulder, leaning LEFT over A (the fold) =====
    S.append(dict(ctrl=[(648,402),(670,350),(654,312),(612,316),(600,358)], w=8, lead=0.10, tail=0.20, swell=0.35, smoothing=sm))    # B crown/back of head
    S.append(dict(ctrl=[(600,358),(600,398),(622,426),(650,418)], w=6, lead=0.16, tail=0.30, swell=0.3, phase=0.7, smoothing=sm))    # B face/jaw, tilted down toward A (open)
    S.append(dict(ctrl=[(610,380),(624,376),(636,381)], w=3.6, lead=0.3, tail=0.3, swell=0.2))                                       # B closed eye
    S.append(dict(ctrl=[(612,316),(648,312),(672,340)], w=5, lead=0.22, tail=0.3, swell=0.5, phase=1.2, smoothing=sm))               # B hair
    S.append(dict(ctrl=[(700,540),(712,628),(700,712)], w=9.5, lead=0.14, swell=0.4, cap_end=True, smoothing=sm))                    # B right side peeking past A, cropped short
    # ===== the wrap + hand as ONE continuous gesture =====
    # arc OVER A's shoulder (apex above the shoulder line), down the back, and
    # ARRIVE into the hand — tail barely tapers so the arm becomes the wrist,
    # not a line ending near a separate hand.
    S.append(dict(ctrl=[(650,506),(596,476),(556,458),(540,498),(516,574),(502,636),(498,668)],
                  w=9.5, lead=0.10, tail=0.06, swell=0.5, swell_k=0.9, smoothing=aw))   # arm -> wrist
    # fingers fan from exactly where the arm arrives (welded), full weight
    S.append(dict(ctrl=[(492,668),(478,704)], w=4.4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))  # finger
    S.append(dict(ctrl=[(500,670),(492,710)], w=4.4, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))  # finger
    S.append(dict(ctrl=[(510,668),(508,708)], w=4.2, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))  # finger
    S.append(dict(ctrl=[(520,664),(528,702)], w=4.0, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9))  # finger
    return S, []

if __name__ == "__main__":
    E,_ = figure_embrace()
    render(E,[],W,H,render_on_linen=False,seed=11).save(f"{OUT}/embrace_bare.png")
    render(E,[],W,H,render_on_linen=True, seed=11).save(f"{OUT}/embrace_linen.png")
    print("done")
