"""
STAGE 5 — composition & master copies. FIRST copy: Hammershoi.

Reconstruct the BONES, never trace: the big shapes, the muted value structure,
the placement in the frame, the figure seen from behind — rebuilt in our own
marks on linen. Recognisable as Hammershoi's structure; plainly our hand.

Why Hammershoi first: his quiet interior is the exact composition lesson the
Merida interiors need — a single dark figure-note off-centre in a pale still
room, a door, and vast ACTIVE emptiness carrying the solitude.

COMPOSITION LOCK (teeth, like every gate now):
  C1 about     — name what the image is about in a few words (a decision, not a
                 figure-on-a-ground). Evidence: the figure is deliberately
                 OFF-centre, the frame is a choice.
  C2 neg-space — name what the empty space is DOING. Evidence: the figure is
                 small (emptiness dominates) and the openness is asymmetric
                 toward what she faces (the distance / the door), not leftover.
(Plus the three guards banked in value_light.py, and the eye as final word.)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from line_figure import stroke, SS, INK
from linen import linen_ground
from construction import Camera

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
W, H = 1100, 1300
WARM = np.array([108, 86, 72], float)     # quiet muted shadow (Hammershoi grey-warm)
DRESS = np.array([60, 48, 46], float)     # the dark note

ABOUT = "a held stillness — a woman alone, the distance between her and the door"

def soft(a, r):
    return np.asarray(Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)),float)/255.0

def poly_mask(pts):
    im=Image.new("L",(W,H),0); ImageDraw.Draw(im).polygon([(float(x),float(y)) for x,y in pts],fill=255)
    return np.asarray(im,float)/255.0

def render():
    cam = Camera(W, H, eye_level=0.50, vpx=0.50, f=900, cam_h=1.5)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    linen = linen_ground(W, H, seed=6, tone=0.2)               # pale, cool-quiet linen
    Zb = 8.0

    # ---- the figure: a STANDING WOMAN seen from behind — tall, narrow, columnar
    # (stage 3 stays true at small size), with shoulders + a nape so the
    # from-behind read is unmistakable. Off-centre left, facing the door. ----
    Xf, Zf = -1.5, 3.3     # closer so the columnar figure is present (still dwarfed by the tall room)
    feet = cam.project(Xf, 0.0, Zf); head = cam.project(Xf, 1.66, Zf)
    fh = feet[1]-head[1]; fx = feet[0]
    sh_y = head[1] + 0.185*fh                                   # shoulders sit below the head (room for the nape)
    # columnar dress: real width (a dress, not pencil-thin), slight waist + hem flare
    dress = poly_mask([(fx-0.115*fh, sh_y),(fx+0.115*fh, sh_y),
                       (fx+0.082*fh, head[1]+0.55*fh),
                       (fx+0.125*fh, feet[1]),(fx-0.125*fh, feet[1]),
                       (fx-0.082*fh, head[1]+0.55*fh)])
    neck = poly_mask([(fx-0.026*fh, head[1]+0.115*fh),(fx+0.026*fh, head[1]+0.115*fh),
                      (fx+0.034*fh, sh_y),(fx-0.034*fh, sh_y)])  # the nape
    headball = soft(((xx-fx)**2/(0.05*fh)**2 + (yy-(head[1]+0.06*fh))**2/(0.062*fh)**2 < 1).astype(float),1)
    bun = soft(((xx-fx)**2/(0.028*fh)**2 + (yy-(head[1]+0.02*fh))**2/(0.024*fh)**2 < 1).astype(float),1)
    fig = np.clip(dress + neck + headball + bun, 0, 1)
    fig = soft((fig>0.5).astype(float), 1.5)

    # ---- value, QUIET: pale room = light (linen left alone); a soft window pool
    # low-left (the off-frame window); soft muted shadow gathering upper-right ----
    pool = soft(np.clip(1 - np.hypot((xx-330)/420,(yy-980)/360),0,1), 60)   # light on the floor, left
    shadow = np.clip(0.5*(xx/W) + 0.35*(yy/H) - 0.42, 0, 1)                 # muted gather upper/right
    shadow = soft(shadow, 70) * 0.5
    out = linen.copy()
    out = out*(1-shadow[...,None]) + WARM*shadow[...,None]
    out = np.clip(out + (pool*0.5)[...,None]*np.array([10,8,4.]), 0, 255)   # faint warm light pool

    # ---- the figure as the single dark note (dress dark; a soft lit left edge) ----
    litedge = np.clip((fx - xx)/(0.16*fh), 0, 1)               # window from the left: left edge lighter
    figval = 0.86 - 0.22*litedge                               # mostly dark, a touch lighter on the lit side
    k = (fig*figval)[...,None]
    out = out*(1-k) + DRESS*k

    # ---- a few committed lines: the door (off-centre right), floor seam, figure contour
    def ink(strokes):
        im=Image.new("L",(W*SS,H*SS),0); d=ImageDraw.Draw(im)
        for s in strokes: stroke(d, **s)
        return np.asarray(im.resize((W,H),Image.LANCZOS),float)/255.0
    d_tl=cam.project(0.9,2.45,Zb); d_bl=cam.project(0.9,0,Zb)
    d_tr=cam.project(2.5,2.45,Zb); d_br=cam.project(2.5,0,Zb)
    seamL=cam.project(-6,0,Zb); seamR=cam.project(6,0,Zb)
    lines = [
        dict(ctrl=[d_bl,d_tl], w=4, cap_start=True, swell=0.25, smoothing=0.8),     # door left jamb
        dict(ctrl=[d_tl,d_tr], w=4, swell=0.25, smoothing=0.8),                     # door head
        dict(ctrl=[d_tr,d_br], w=4, cap_end=True, swell=0.25, smoothing=0.8),       # door right jamb
        dict(ctrl=[seamL,seamR], w=3.5, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85),  # floor/wall seam
    ]
    edge=(fig>0.45).astype(float); edge=np.clip(edge-soft(edge,1.4),0,1)
    a=np.clip(soft(edge,0.5)*0.7 + ink(lines), 0, 1)
    out = out*(1-a[...,None]) + INK*a[...,None]

    door_cx = cam.project(1.7, 0.0, Zb)[0]
    composition_checks(fig, fx, door_cx)
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

def composition_checks(fig, fx, door_cx):
    figm = fig > 0.5
    area = figm.mean()
    off = abs(fx - W/2) / W
    C1 = off > 0.08                                   # frame is a decision (off-centre)
    # C2 measures the ACTIVE void: the lookspace toward what she faces (the door)
    # must be a deliberate large gap, clearly bigger than the breathing room
    # behind her — and the figure present-but-dwarfed (not a lost speck).
    gap_to_door = abs(door_cx - fx)
    gap_behind  = fx                                   # to the left frame edge
    present = 0.02 < area < 0.11
    lookspace = gap_to_door > 1.5*gap_behind
    C2 = present and lookspace
    # stage 3 doesn't switch off at small size: the note must read as a STANDING
    # person — columnar (much taller than wide), not a squat cone.
    ys, xs = np.where(figm); aspect = (ys.max()-ys.min())/max(1,(xs.max()-xs.min()))
    C3 = aspect > 3.0
    print(f'  about      : "{ABOUT}"')
    print(f"  C1 off-centre  : {'PASS' if C1 else 'FAIL'}  (figure {100*off:.0f}% off frame-centre)")
    print(f"  C2 neg-space   : {'PASS' if C2 else 'FAIL'}  (figure {100*area:.1f}% of frame; "
          f"lookspace to door {gap_to_door:.0f}px vs {gap_behind:.0f}px behind)")
    print(f"  C3 reads-person: {'PASS' if C3 else 'FAIL'}  (columnar aspect h/w {aspect:.1f}, need > 3 — not a cone)")
    return C1 and C2 and C3

ABOUT_M = "a figure reclining at ease — languid, arm behind the head"

def render_matisse(hide_head=False):
    """Matisse, for ECONOMY: a whole living, specific figure in a handful of
    decisive lines — reclining, languid, one arm cradling the head, one knee
    raised. Reconstruct the bones (the long line of action, the few flowing
    contours), our hand, on linen. Every gate still holds; fewer lines, same
    truths. The dominant line of action is the back; the rest is subordinate."""
    Wm, Hm = 1300, 860
    S = []
    # 1) LINE OF ACTION — the long top contour: shoulder -> waist -> hip -> thigh
    S.append(dict(ctrl=[(414,432),(474,456),(566,486),(664,476),(744,456),(856,512),(940,560)],
                  w=10, lead=0.06, tail=0.14, swell=0.5, smoothing=0.72))
    # 2) front/underside: breast -> belly -> hip underside -> thigh underside
    S.append(dict(ctrl=[(420,456),(452,488),(470,504),(566,544),(664,560),(746,558)],
                  w=7, lead=0.12, tail=0.2, swell=0.4, smoothing=0.72))
    # 3) raised arm cradling the head (frames it)
    S.append(dict(ctrl=[(420,430),(378,360),(320,316),(284,346),(300,398)],
                  w=7.5, lead=0.12, tail=0.2, swell=0.4, smoothing=0.72))
    # 4) raised knee — bent leg: thigh up to the knee, shin down to the foot
    S.append(dict(ctrl=[(744,544),(800,468),(842,440)], w=8, lead=0.14, tail=0.18, swell=0.35, smoothing=0.72))
    S.append(dict(ctrl=[(842,440),(872,512),(886,584)], w=7, lead=0.10, tail=0.16, swell=0.35, cap_end=True, smoothing=0.72))
    # 5) far leg extended, foot
    S.append(dict(ctrl=[(742,560),(862,602),(982,614)], w=7.5, lead=0.14, swell=0.35, smoothing=0.72))
    S.append(dict(ctrl=[(982,612),(1012,606),(986,626)], w=6, cap_start=True, cap_end=True, swell=0.2, smoothing=0.85))
    if not hide_head:
        # 6) head resting back (no features) + hair
        S.append(dict(ctrl=[(322,388),(330,348),(362,342),(376,372),(356,394)], w=7, lead=0.12, tail=0.24, swell=0.35, smoothing=0.72))
        S.append(dict(ctrl=[(330,348),(356,336),(376,356)], w=5, lead=0.22, tail=0.3, swell=0.5, smoothing=0.7))
    # ground the figure reclines on (faint)
    ground=[dict(ctrl=[(150,686),(1180,682)], w=3, cap_start=True, cap_end=True, swell=0.2, smoothing=0.9)]

    im=Image.new("L",(Wm*SS,Hm*SS),0); d=ImageDraw.Draw(im)
    for s in ground+S: stroke(d, **s)
    a=np.asarray(im.resize((Wm,Hm),Image.LANCZOS),float)/255.0
    rng=np.random.default_rng(7); grain=rng.normal(0,1,(Hm,Wm))
    grain=np.asarray(Image.fromarray(((grain-grain.min())/(np.ptp(grain)+1e-6)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)),float)/255.0
    a=np.clip(a*(0.9+0.2*grain),0,1)
    linen=linen_ground(Wm,Hm,seed=6,tone=0.3)
    out=linen*(1-a[...,None]) + INK*a[...,None]
    print(f'  about        : "{ABOUT_M}"   (economy: {len(S)} figure strokes)')
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

ABOUT_S = "a person seated and gathered forward — weary, withdrawn"

def render_schmitz(hide_head=False):
    """Boris Schmitz, the SEARCHING line — the opposite pole from Matisse. The
    line hunts, doubles back, finds the particular truth of THIS body, not a
    graceful general one. Built on a believable seated figure; each contour is
    found through a few searching passes. Watch the mirror trap: the search must
    RESOLVE into the figure, not collapse into scribble-mud. Reconstruct the
    bones, our hand, on linen, never traced. No rendered face."""
    Ws, Hs = 1000, 1200
    rng = np.random.default_rng(5)
    # seated figure leaning forward, head bowed. The torso now has real volume:
    # BACK (left, the line of action) and FRONT (right, chest/belly bowing OUT)
    # enclose a believable mass — the search hunts the body, not just the spine.
    back  = [(478,762),(456,600),(428,432),(418,304),(432,256)]      # left edge / spine
    front = [(470,292),(540,442),(528,624),(498,706)]                # right edge: chest bows out -> belly -> lap
    head_w = 84
    contours = [
        (back, 13),
        (front, 10),
        ([(420,300),(472,288)], 7),                                  # shoulder line (joins back->front)
        ([(498,710),(664,734),(750,744)], 13),                       # near thigh (thick)
        ([(750,744),(762,922),(780,1090)], 11),                      # near shin
        ([(482,724),(642,754),(728,766)], 11),                       # far thigh
        ([(728,766),(740,942),(758,1096)], 10),                      # far shin
        ([(470,300),(540,520),(732,732)], 11),                       # near arm to knee
        ([(452,308),(520,538),(716,752)], 10),                       # far arm
        ([(478,768),(578,782),(498,774)], 8),                        # seat
    ]
    if not hide_head:
        contours += [([(456,256),(438,212),(472,196),(506,214),(498,260),(468,272)], 10),  # bowed head
                      ([(438,212),(468,196),(504,210)], 6)]                                  # hair
    main, search = [], []
    for ctrl, w in contours:
        main.append(dict(ctrl=ctrl, w=w, lead=0.08, tail=0.12, swell=0.4, smoothing=0.58))
        for _ in range(3):
            g = [(x+rng.normal(0,9), y+rng.normal(0,9)) for x,y in ctrl]
            search.append(dict(ctrl=g, w=w*0.5, lead=0.1, tail=0.16, swell=0.4, smoothing=0.58))
        if len(ctrl) >= 3:
            jx,jy = ctrl[-1]
            search.append(dict(ctrl=[(jx-12,jy-9),(jx+13,jy+10)], w=max(3,w*0.4), cap_start=True, cap_end=True, swell=0.2, smoothing=0.8))
    def layer(strokes):
        im=Image.new("L",(Ws*SS,Hs*SS),0); d=ImageDraw.Draw(im)
        for s in strokes: stroke(d, **s)
        return np.asarray(im.resize((Ws,Hs),Image.LANCZOS),float)/255.0
    a = np.clip(layer(main) + layer(search)*0.5, 0, 1)
    linen = linen_ground(Ws,Hs,seed=6,tone=0.3)
    out = linen*(1-a[...,None]) + INK*a[...,None]

    # NOT-MUD lock: a line drawing stays open
    cover = (a > 0.25).mean(); not_mud = cover < 0.10
    # BELIEVABLE-MASS lock (teeth for the gate that had no number): the torso the
    # contours ENCLOSE must be a real body, not a reed — measure its width vs the
    # head. Build the torso polygon (back + reversed front) and measure mid-chest.
    tp = Image.new("L",(Ws,Hs),0); ImageDraw.Draw(tp).polygon([(float(x),float(y)) for x,y in back+front[::-1]],fill=255)
    tm = np.asarray(tp,float)/255.0
    band = tm[420:470,:]
    chest_w = (band.sum(1).max())
    mass_ok = chest_w >= 0.9*head_w
    print(f'  about         : "{ABOUT_S}"')
    print(f"  not-mud       : {'PASS' if not_mud else 'FAIL'}  (ink {100*cover:.1f}%, need < 10%)")
    print(f"  believable-mass: {'PASS' if mass_ok else 'FAIL'}  (torso chest width {chest_w:.0f}px vs head {head_w}px — need >= {0.9*head_w:.0f}, not a reed)")
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))

if __name__ == "__main__":
    render().save(f"{OUT}/stage5_hammershoi.png")
    print("matisse:")
    render_matisse(False).save(f"{OUT}/stage5_matisse.png")
    render_matisse(True ).save(f"{OUT}/stage5_matisse_headless.png")
    print("schmitz:")
    render_schmitz(False).save(f"{OUT}/stage5_schmitz.png")
    render_schmitz(True ).save(f"{OUT}/stage5_schmitz_headless.png")
    print("done")
