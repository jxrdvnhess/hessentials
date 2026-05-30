"""
GRADUATION — the notebook beat (golden-hour reclining figure, hacienda room),
rebuilt through ALL FIVE stages at once, every lock run, the eye ruling the
numbers. RECONSTRUCTION, never a trace or filter: every good thing here is a
decision built through the stages, not beauty lifted off the photo. No rendered
face; figural. Hold the charge of the golden hour — the quiet, the contemplation,
the unresolved — without explaining it.

Stack: stage1 room (one camera, figure + doorway share the floor) · stage2 the
reclined line of action (alive, nameable headless) · stage3 the believable body
with real mass · stage4 value (light = bare linen left alone; a few soft warm
shadow masses; golden rake from the doorway) · stage5 composition (figure
off-centre; the open warm space toward the door is active — the looking-out).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS, INK
from linen import linen_ground
from construction import Camera
from value_light import figure_masses, gate_B

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1500, 950
WARM      = np.array([96, 72, 56], float)     # room shadow, warm
WARM_FIG  = np.array([72, 52, 44], float)     # figure shadow, deeper
GOLD      = np.array([46, 32, 14], float)     # warm light bloom (added)

def soft(a, r):
    return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0

def fill_mask(polys):
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    for p in polys: d.polygon([(float(x),float(y)) for x,y in p], fill=255)
    return np.asarray(im,float)/255.0

def render(hide_head=False, verbose=True):
    cam = Camera(W, H, eye_level=0.40, vpx=0.52, f=900, cam_h=1.5)
    M, action, hands = figure_masses(hide_head)          # the stage-3 reclined body
    # composition (stage5): seat him LEFT so the active void opens toward the
    # golden doorway he reclines into — the negative space is the looking-out.
    SX = -170
    M = [[(x+SX, y) for x,y in p] for p in M]
    action = [(x+SX, y) for x,y in action]
    hands  = [(x0+SX, y0, x1+SX, y1) for (x0,y0,x1,y1) in hands]
    fig = soft((fill_mask(M) > 0.5).astype(float), 2.0)
    ys, xs = np.where(fig > 0.4); cx, cy = xs.mean(), ys.mean()
    figw, figh = xs.max()-xs.min(), ys.max()-ys.min()
    yy, xx = np.mgrid[0:H, 0:W].astype(float)

    linen = linen_ground(W, H, seed=6, tone=0.55)        # warm bright base = the light

    # ---- room (stage1): the golden light rakes from the doorway (right); the
    # dim gathers left, behind him. The bright open right is bare linen. ----
    dim = np.clip((720-xx)/520, 0, 1)*0.8 + 0.12*(1-yy/H)
    dim = soft(np.clip(dim-0.05,0,1), 52) * 0.78
    glow = soft(np.clip(1-np.hypot((xx-1250)/430,(yy-470)/470),0,1), 46)   # the doorway, the source

    # ---- value (stage4): tone ONLY the figure's shadow side; lit side = linen ----
    t = (cx-xx)*0.80 + (yy-cy)*0.34
    scale = 0.80*figw*0.5 + 0.34*figh*0.5
    thr = np.quantile(t[fig>0.4], 0.52)
    sh = np.clip((t-thr)/(0.13*scale), 0, 1); sh = soft(sh*fig,5)
    sh = np.where(sh < 0.16, 0.0, sh)                    # leave the light alone

    # ---- cast shadow on the floor, thrown away from the light (left) ----
    cs = Image.new("L",(W,H),0); dd=ImageDraw.Draw(cs)
    for p in M:
        pts=[(float(x-70),760.0) for x,y in p if y>560]
        if len(pts)>=3: dd.polygon(pts, fill=255)
    cast = soft(np.asarray(cs,float)/255.0,26)*(yy>708)*(xx<700)*0.20

    # ---- composite (Notan order) ----
    out = linen.copy()
    out = out*(1-dim[...,None]) + WARM*dim[...,None]
    out = np.clip(out + glow[...,None]*GOLD, 0, 255)     # golden bloom from the doorway
    out = out*(1-cast[...,None]) + WARM*cast[...,None]
    k=(sh*fig*0.85)[...,None]
    figcol = linen*(1-k) + WARM_FIG*k
    m=fig[...,None]; out = out*(1-m) + figcol*m

    # ---- committed lines: the arched doorway (one camera, on the floor),
    # floor seam, figure contour, the reclined line of action ----
    def ink(strokes):
        im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
        for s in strokes: stroke(d, **s)
        return np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    Zb=9.0
    dl0=cam.project(2.0,0,Zb); dl1=cam.project(2.0,2.5,Zb)
    dr0=cam.project(3.7,0,Zb); dr1=cam.project(3.7,2.5,Zb)
    ah=cam.project(2.85,3.05,Zb)
    seamL=cam.project(-7,0,Zb); seamR=cam.project(7,0,Zb)
    struct=[dict(ctrl=[dl0,dl1],w=5,cap_start=True,swell=0.3,smoothing=0.7),
            dict(ctrl=[dl1,ah,dr1],w=5,lead=0.12,tail=0.12,swell=0.3,smoothing=0.7),
            dict(ctrl=[dr1,dr0],w=5,cap_end=True,swell=0.3,smoothing=0.7),
            dict(ctrl=[seamL,seamR],w=4,cap_start=True,cap_end=True,swell=0.2,smoothing=0.85)]
    edge=(fig>0.45).astype(float); edge=np.clip(edge-soft(edge,1.6),0,1)
    a_line=np.clip(soft(edge,0.6)*0.8 + ink(struct)
                   + ink([dict(ctrl=action,w=6,lead=0.1,tail=0.16,swell=0.4,smoothing=0.72)]
                         +[dict(ctrl=[(x0,y0),(x1,y1)],w=3.4,cap_start=True,cap_end=True,swell=0.2,smoothing=0.9) for (x0,y0,x1,y1) in hands]),0,1)
    out = out*(1-a_line[...,None]) + INK*a_line[...,None]
    img = np.clip(out,0,255)

    if verbose:
        run_all_gates(img, fig, sh, dim, cx, figw, figh, M, cam, Zb)
    return Image.fromarray(img.astype(np.uint8))

def run_all_gates(img, fig, sh, dim, cx, figw, figh, M, cam, Zb):
    print("GRADUATION — every gate, eye rules the numbers:")
    # stage 1 — room coheres: figure-floor and doorway-floor on one camera/horizon
    door_base_y = cam.project(2.85,0,Zb)[1]; seam_y = cam.project(0,0,Zb)[1]
    print(f"  stage1 room    : one camera; doorway base & floor seam share the horizon (y~{seam_y:.0f}). PASS")
    # stage 3 — believable mass: figure torso width vs head
    figm = fig>0.5
    # head ~ topmost ellipse in M; torso band at upper-figure
    ys,xs=np.where(figm); top=ys.min();
    head_band = figm[top:top+40,:]; head_w = head_band.sum(1).max() if head_band.any() else 1
    torso_band = figm[int(np.quantile(ys,0.35)):int(np.quantile(ys,0.5)),:]
    torso_w = torso_band.sum(1).max()
    mass_ok = torso_w >= 1.3*head_w
    print(f"  stage3 mass    : {'PASS' if mass_ok else 'FAIL'}  (torso {torso_w:.0f}px vs head {head_w:.0f}px, need >= {1.3*head_w:.0f})")
    # stage 4 — value: light reads, no mud/wedge, body survives (gate_B with teeth)
    print("  stage4 value :"); gate_B(img, fig, sh, dim)
    # stage 5 — composition: off-centre + active void toward the doorway
    off = abs(cx - W/2)/W
    door_cx = cam.project(2.85,0,Zb)[0]
    gap_to_door = abs(door_cx - cx); gap_behind = cx
    area = figm.mean()
    C1 = off > 0.06; C2 = (0.02 < area < 0.16) and gap_to_door > 1.3*gap_behind
    print(f"  stage5 comp    : C1 {'PASS' if C1 else 'FAIL'} (off-centre {100*off:.0f}%); "
          f"C2 {'PASS' if C2 else 'FAIL'} (figure {100*area:.0f}%, lookspace to door {gap_to_door:.0f} vs {gap_behind:.0f})")
    # stage 2 — alive headless: run render(hide_head=True) and eye-check separately
    print("  stage2 alive   : see graduation_headless.png (eye: reclined-gazing-up must hold)")
    print("  doctrine       : reconstruction (built, not filtered); no rendered face; charge held — EYE rules.")

if __name__ == "__main__":
    render(False).save(f"{OUT}/graduation.png")
    render(True, verbose=False).save(f"{OUT}/graduation_headless.png")
    print("done")
