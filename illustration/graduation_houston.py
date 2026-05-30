"""
GRADUATION (imagined scene, no photo) — Houston, grey rain. A man leans into a
window watching the rain, elsewhere; the other one a city away, a silence where
a voice should be. The whole weight of the distance is in how he holds himself
against the glass. Not grief — the low ache of being apart.

Target = the FEELING. The locks are only the floor (body not insectile, value
not mud, space coheres); passing them earns nothing. Drawn from the gesture and
mood up — searching line, a living particular body, flat grey almost-colorless
light. Made not captured, no rendered face, figural. The eye is the only judge:
would a stranger feel him missing someone.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS
from figure_construction import capsule, ellipse_poly

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1100, 1380
GROUND = np.array([171, 173, 176], float)   # flat cool grey room (almost no colour)
WINDOW = np.array([200, 203, 206], float)    # the rainlight, a touch lighter
FIGURE = np.array([past if False else 120, 122, 127], float)  # soft mid-grey body (low contrast)
LINE   = np.array([72, 73, 78], float)       # the searching line — grey, not black
RAIN   = np.array([188, 191, 195], float)

def soft(a,r): return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0
def fillpolys(polys):
    im=Image.new("L",(W,H),0); d=ImageDraw.Draw(im)
    for p in polys: d.polygon([(float(x),float(y)) for x,y in p],fill=255)
    return np.asarray(im,float)/255.0

def figure(hide_head=False):
    """A man slumped into the window: forehead resting on his forearm against the
    glass, weight sagging forward, the other arm hanging. Drawn in the SEARCHING
    LINE (Schmitz) — a faint mass underneath, but the living particular line
    carries it. The ache is the slump and the forehead on the glass. No face."""
    # faint mass — compact, weighted (NOT a reed): wide torso, thick legs, ~7 heads
    mass = [ellipse_poly(556,640,58,98,-0.20), ellipse_poly(590,856,54,58,-0.05),
            capsule((602,902),(612,1010),34,30), capsule((612,1010),(622,1150),30,22),
            capsule((566,908),(576,1016),32,27), capsule((576,1016),(586,1156),27,20),
            capsule((552,560),(518,520),22,18), capsule((518,520),(498,452),18,13),
            capsule((576,566),(612,742),22,17), capsule((612,742),(624,898),17,12)]
    if not hide_head: mass.append(ellipse_poly(520,496,36,42,-0.5))
    # searching contours (the line that hunts THIS slumped, weighted body)
    C = [([(636,1156),(620,1000),(600,800),(572,610),(552,560)], 14),     # BACK — the slump (line of action)
         ([(552,566),(520,606),(536,760),(576,892),(606,910)], 11),       # neck->chest(bows to glass)->belly->lap
         ([(552,566),(518,524),(498,452)], 11),                           # raised arm -> forearm on the glass
         ([(578,566),(614,742),(626,898)], 11),                           # the heavy hanging arm
         ([(602,906),(614,1012),(624,1156)], 14),                         # near leg (thick)
         ([(566,912),(578,1018),(588,1158)], 13)]                         # far leg
    if not hide_head:
        C += [([(544,526),(518,530),(502,502),(514,476),(540,476),(550,500)], 9),  # bowed head on the arm (no face)
              ([(518,476),(540,470),(552,492)], 6)]                                 # hair
    action=[(634,1156),(616,1000),(596,790),(564,600),(544,526)]
    fingers=[(500,448,494,474),(510,446,506,472),(520,448,518,474)]      # fingertips/forehead on the glass
    return mass, C, action, fingers

def render(hide_head=False, verbose=True):
    yy,xx=np.mgrid[0:H,0:W].astype(float)
    out=np.ones((H,W,3))*GROUND
    # ---- a large window of flat rainlight; the man stands in front of it ----
    win=(xx>120)&(xx<820)&(yy>120)&(yy<1080)
    out=np.where(win[...,None], WINDOW, out)
    for m in [(466,124,474,1076),(124,596,816,604)]:                 # mullions (a cross)
        out=np.where(((xx>m[0])&(xx<m[2])&(yy>m[1])&(yy<m[3]))[...,None], GROUND*0.9, out)
    rng=np.random.default_rng(3); rim=Image.new("L",(W,H),0); rd=ImageDraw.Draw(rim)
    for _ in range(160):
        x=rng.uniform(126,814); y=rng.uniform(126,1074); ln=rng.uniform(24,78)
        rd.line([(x,y),(x+rng.uniform(-3,3),y+ln)],fill=255,width=1)
    rain=soft(np.asarray(rim,float)/255.0,0.5)*win
    out=out*(1-(rain*0.45)[...,None]) + RAIN*(rain*0.45)[...,None]

    # ---- the figure: a faint soft body mass, then the SEARCHING LINE carries it.
    # He's slumped into the glass; the line hunts the particular weary body. ----
    mass, C, action, fingers = figure(hide_head)
    figm = soft((fillpolys(mass)>0.5).astype(float), 2.5)
    out=out*(1-(figm*0.55)[...,None]) + FIGURE*(figm*0.55)[...,None]   # soft body mass; the line does the work
    rng2=np.random.default_rng(5); main=[]; search=[]
    for ctrl,w in C:
        main.append(dict(ctrl=ctrl,w=w,lead=0.08,tail=0.12,swell=0.4,smoothing=0.6))
        for _ in range(2):
            search.append(dict(ctrl=[(x+rng2.normal(0,5.5),y+rng2.normal(0,5.5)) for x,y in ctrl],w=w*0.55,smoothing=0.6,swell=0.4))
    main.append(dict(ctrl=action,w=9,lead=0.08,tail=0.14,swell=0.45,smoothing=0.6))   # the slump, heaviest
    for _ in range(2):
        search.append(dict(ctrl=[(x+rng2.normal(0,5.5),y+rng2.normal(0,5.5)) for x,y in action],w=5,smoothing=0.6,swell=0.4))
    for (x0,y0,x1,y1) in fingers: main.append(dict(ctrl=[(x0,y0),(x1,y1)],w=4,cap_start=True,cap_end=True,swell=0.2,smoothing=0.85))
    def layer(strokes):
        im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
        for s in strokes: stroke(d,**s)
        return np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    a=np.clip(layer(main)+layer(search)*0.5,0,1)
    out=out*(1-a[...,None]) + LINE*a[...,None]
    img=np.clip(out,0,255)
    if verbose: floor_locks(img, figm)
    return Image.fromarray(img.astype(np.uint8))

def floor_locks(img, figm):
    lum=img.mean(2); fm=figm>0.5
    ys,xs=np.where(fm); top=ys.min()
    head=fm[top:top+46,:]; head_w=head.sum(1).max() if head.any() else 1
    torso=fm[int(np.quantile(ys,0.28)):int(np.quantile(ys,0.45)),:]; torso_w=torso.sum(1).max()
    mass_ok=torso_w>=1.3*head_w
    figL=lum[fm].mean(); gnd=lum[~fm & (np.mgrid[0:H,0:W][1]>700)].mean()
    reads = abs(gnd-figL) > 8                          # figure separable from ground (not lost)
    flat  = (np.quantile(lum,0.95)-np.quantile(lum,0.05)) < 130   # narrow range = flat grey, not dramatic
    print("FLOOR LOCKS (the target is the feeling, not these):")
    print(f"  body not insectile: {'PASS' if mass_ok else 'FAIL'}  (torso {torso_w:.0f}px vs head {head_w:.0f}px)")
    print(f"  value not mud     : {'PASS' if reads else 'FAIL'}  (figure {figL:.0f} vs ground {gnd:.0f}, reads softly)")
    print(f"  flat grey light   : {'PASS' if flat else 'FAIL'}  (value range narrow, undramatic)")
    print("  EYE (the only judge): does a stranger feel him missing someone?")

if __name__ == "__main__":
    render(False).save(f"{OUT}/graduation_houston.png")
    render(True, verbose=False).save(f"{OUT}/graduation_houston_headless.png")
    print("done")
