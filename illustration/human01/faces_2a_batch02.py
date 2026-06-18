"""
HUMAN STUDIES VOL. 1 — ASSIGNMENT 2A, batch 02 (f211–f212).
Production under the carrier question: draw the observation in the
carrier where the information actually lived.

f211  Entry 5 retranslated — the kiss WITH the kisser. The audit
      ruled f206 Category C: a two-body observation cut to one body.
      This is the same observation given both bodies. Not a redraw
      of f206 (which stands as audited); a new translation.
f212  Entry 31 — the lean-back power stroke (bed-making). The
      information lived in torso and cycle; the carrier is posture.
      First full-figure drawing of the assignment.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import render               # noqa: E402
from heads_batch01 import s, tilt            # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def f211_kiss_with_kisser():
    """Entry 5, both bodies. Jordan in profile from the left, lips at
    Greg's cheek; Greg chin up under the hat, eyes closed, pressed
    scrunch smile. The chin is offered TO someone now."""
    S = []
    # ---- GREG, right of center, head tipped back-right ~8deg
    # hat brim low, owning the forehead
    S += [s([(352,262),(412,238),(492,234),(552,254),(572,278)], 3.4)]
    S += [s([(366,238),(424,206),(500,202),(552,228)], 2.6)]            # crown
    S += [s([(352,262),(360,280)], 2.0)]
    S += [s([(572,278),(562,296)], 2.0)]
    # face sides; jaw underside showing (chin up)
    S += [s([(366,284),(362,344),(372,398),(390,448),(418,488),(452,504)], 2.8)]
    S += [s([(560,288),(564,348),(556,400),(540,448),(514,490),(458,506)], 3.0)]
    S += [s([(424,494),(444,506),(472,506),(492,494)], 2.4)]            # chin shelf
    S += [s([(430,516),(460,526),(488,514)], 2.0)]                      # underside plane
    # closed eyes high on the lifted face; squeeze ticks
    S += [s([(398,318),(420,326),(442,320)], 2.6)]
    S += [s([(404,332),(420,338),(436,333)], 1.3)]
    S += [s([(478,318),(500,326),(522,320)], 2.6)]
    S += [s([(484,332),(500,338),(516,333)], 1.3)]
    # brows easy
    S += [s([(394,298),(420,292),(444,297)], 2.5)]
    S += [s([(476,296),(502,290),(526,296)], 2.5)]
    # nose from below + scrunch smile, cheek balls high
    S += [s([(462,330),(458,376)], 1.7)]
    S += [s([(442,386),(460,394),(482,384)], 2.1)]
    S += [s([(424,428),(448,436),(466,438),(486,434),(506,424)], 2.6)]
    S += [s([(434,444),(464,450),(496,440)], 1.9)]
    S += [s([(408,396),(422,420)], 1.3)]                                # cheek ball L
    S += [s([(516,392),(502,416)], 1.3)]                                # cheek ball R
    # neck stretched, collar
    S += [s([(428,508),(424,570)], 2.4)]
    S += [s([(490,508),(496,568)], 2.4)]
    S += [s([(398,584),(462,604),(526,580)], 2.6)]
    S += [s([(404,600),(462,618),(520,596)], 1.4)]                      # shirt placket
    # ---- JORDAN, left, true profile leaning in; lips at Greg's cheek
    # profile skull: back of head left, face right toward Greg
    S += [s([(148,300),(150,228),(192,176),(252,160),(304,178)], 3.0)]  # crown
    S += [s([(304,178),(330,210),(338,246)], 2.6)]                      # forehead
    S += [s([(160,196),(206,170),(258,162)], 2.2)]                      # quiff swept back
    S += [s([(154,250),(170,196),(214,168),(266,160),(300,172)], 2.8)]  # hair mass silhouette
    S += [s([(168,234),(196,196),(240,178)], 1.6)]                      # interior sweep, one only
    S += [s([(148,300),(146,356),(158,408)], 2.8)]                      # back of skull→nape
    # profile features: brow ridge, closed eye, nose, kissing lips
    S += [s([(338,246),(330,272),(336,286)], 2.5)]                      # brow ridge
    S += [s([(310,288),(330,284)], 2.0)]                                # closed eye lash line
    S += [s([(314,296),(328,293)], 1.2)]                                # lid fold
    S += [s([(336,286),(352,322),(356,338)], 2.5)]                      # the nose, committed
    # lips pursed, MEETING Greg's cheek line — contact at (366,360)
    S += [s([(356,338),(366,352),(362,362)], 2.3)]                      # upper lip to contact
    S += [s([(348,368),(360,366)], 1.8)]                                # lower lip pursed
    S += [s([(344,380),(356,392),(372,406)], 2.2)]                      # chin tucked
    # jaw to ear; ear mid-skull
    S += [s([(372,406),(330,430),(268,430)], 2.6)]
    S += [s([(238,300),(254,288),(262,310),(248,326),(236,316)], 2.0)]  # ear
    # neck and shoulder driving the lean; arm reaching behind Greg
    S += [s([(268,430),(254,470),(240,510)], 2.6)]                      # throat line
    S += [s([(158,408),(170,460),(192,506)], 2.8)]                      # nape into trapezius
    S += [s([(140,540),(196,512),(252,508)], 3.0)]                      # shoulder mass
    S += [s([(252,508),(330,520),(396,548)], 2.8)]                      # arm crossing low to Greg
    S += [s([(150,566),(208,544),(262,540)], 2.0)]                      # blazer lapel hint
    S = tilt(S, 0.0)
    return S, [s([(150,330),(570,330)], 1.0)]


def f212_power_stroke():
    """Entry 31. Kneeling on the mattress, torso in the lean-back
    power stroke, arms straight to the duvet mass, head bowed under
    the cap through the whole pull. The face carries nothing; the
    body carries all of it."""
    S = []
    # mattress line + bed base
    S += [s([(60,620),(340,612),(640,618)], 3.0)]
    S += [s([(70,660),(350,652),(630,658)], 2.2)]
    S += [s([(96,620),(98,660)], 1.8)]
    S += [s([(600,618),(602,656)], 1.8)]
    # duvet mass, left: three soft billows, the pulled edge taut
    S += [s([(70,560),(130,510),(210,520),(258,556)], 3.0)]
    S += [s([(86,600),(150,560),(228,572)], 2.4)]
    S += [s([(120,614),(190,596),(252,600)], 2.0)]
    S += [s([(258,556),(300,520),(330,492)], 2.6)]                      # taut edge to the grip
    S += [s([(228,572),(282,536),(326,502)], 2.2)]                      # second taut line — fabric wedge
    S += [s([(252,600),(296,562),(330,520)], 1.6)]                      # slack fold trailing the pull
    # ---- the figure, side view facing left, kneeling, LEANING BACK
    # head bowed, cap
    S += [s([(394,318),(386,276),(410,248),(450,242),(478,262)], 2.8)]  # skull bowed fwd
    S += [s([(376,300),(408,282),(446,276)], 2.6)]                      # cap brim down-left
    S += [s([(390,258),(430,240),(466,246)], 2.2)]                      # cap crown
    S += [s([(478,262),(484,294),(476,318)], 2.4)]                      # back of head→nape
    # face hint only: jaw line under brim, nothing else
    S += [s([(394,318),(412,336),(438,342)], 2.2)]
    # torso: the lean-back arc — spine curves BACK of the pelvis
    S += [s([(476,318),(500,360),(516,412),(520,464)], 3.2)]            # spine, leaning back
    S += [s([(438,342),(452,376),(454,414)], 2.6)]                      # chest line
    # arms: straight, taut, both reaching down-left to the grip
    S += [s([(452,360),(396,420),(338,478),(330,492)], 2.9)]            # near arm to grip
    S += [s([(474,348),(420,404),(360,462)], 2.3)]                      # far arm, parallel
    S += [s([(322,486),(338,502),(352,490)], 2.0)]                      # the grip: two curves
    # pelvis sitting toward heels; thighs; shins flat on mattress
    S += [s([(520,464),(512,506),(488,536)], 3.0)]                      # pelvis→hip
    S += [s([(454,414),(470,470),(462,520)], 2.4)]                      # front of hip/thigh
    S += [s([(488,536),(444,572),(412,596)], 2.9)]                      # thigh down to knee
    S += [s([(412,596),(470,606),(540,608)], 2.9)]                      # shin flat on bed
    S += [s([(540,608),(566,596),(572,580)], 2.4)]                      # foot, toes tucked
    # far leg hint
    S += [s([(498,548),(462,582),(444,600)], 1.8)]
    # tank top edges
    S += [s([(444,352),(468,348)], 1.6)]
    S += [s([(456,430),(500,438)], 1.8)]                                # hem at the lean
    S = tilt(S, 0.0)
    return S, [s([(330,492),(520,464)], 1.0)]


SEQ = [("f211", f211_kiss_with_kisser),
       ("f212", f212_power_stroke)]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = []
    for name, fn in SEQ:
        Sx, G = fn()
        im = render(Sx, G, W, H, seed=hash(name) % 999)
        im.save(os.path.join(OUT, f"{name}.png"))
        imgs.append((name, im))
        print("wrote", name)
    sheet = Image.new("RGB", (2 * W // 2 + 20, H // 2), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(imgs):
        x = i * (W // 2 + 20)
        sheet.paste(im.resize((W // 2, H // 2)), (x, 0))
        d.text((x + 10, 8), name, fill=(31, 29, 27))
    sheet.save(os.path.join(OUT, "_contact_2a_b02.png"))
    print("contact ok")
