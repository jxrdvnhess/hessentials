"""
HUMAN STUDIES VOL. 1 — ASSIGNMENT 2A, batch 03 (f213–f215).
Draw only the carrier.

f213  Entry 26 — the lent head. Carrier: interaction. Foreign hands
      enter from the frame edges; the subject's eyes park elsewhere;
      his own hand keeps the drink up.
f214  Entry 19 — the wait that won't sit. Carrier: posture +
      environment. Standing mid-room between two devices and a
      screen; the scene is the sentence.
f215  Entry 13 — the palm-rub. Carrier: the hand. The face changes
      only while being touched; drawn mid-touch.

NOT DRAWN, recorded in the ledger: Entry 22 (act close, judge far).
Carrier is the alternation between two distances over time. A still
holds one distance. The failure is recorded, not forced.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import render               # noqa: E402
from heads_batch01 import s, tilt            # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def f213_lent_head():
    """Entry 26. Head held still for other people's hands; eyes
    parked down-left at nothing; the drink stays up. Two foreign
    hands own their entries from the frame edges."""
    S = []
    # skull, level, deliberately still; headband as a simple band
    S += [s([(252,310),(262,220),(316,158),(382,148),(444,178),(466,262),(468,322)], 3.0)]
    S += [s([(266,282),(316,254),(380,246),(440,266)], 2.8)]            # headband lower edge
    S += [s([(262,260),(314,232),(382,224),(444,244)], 2.2)]            # headband upper edge
    S += [s([(294,222),(330,200),(376,194)], 2.0)]                      # hair above band
    S += [s([(260,326),(254,396),(266,458),(286,518),(316,560),(354,580)], 2.8)]
    S += [s([(462,330),(464,400),(452,462),(430,522),(398,566),(358,582)], 3.2)]
    S += [s([(318,568),(340,580),(372,580),(392,568)], 2.2)]
    # eyes OPEN but parked down-left — averted from both hands
    S += [s([(288,376),(314,370),(340,375)], 2.4)]
    S += [s([(294,378),(302,385),(295,392),(288,385),(294,378)], 1.3)]  # iris low-left
    S += [s([(294,392),(318,396),(338,390)], 1.4)]
    S += [s([(382,373),(408,367),(432,372)], 2.4)]
    S += [s([(386,375),(394,382),(387,389),(380,382),(386,375)], 1.3)]
    S += [s([(388,389),(412,393),(432,387)], 1.4)]
    # brows easy — no address to the handlers
    S += [s([(286,354),(316,349),(342,353)], 2.6)]
    S += [s([(380,351),(410,346),(436,351)], 2.6)]
    S += [s([(358,376),(354,438)], 1.8)]
    S += [s([(334,450),(356,458),(380,448)], 2.2)]
    # mouth: half-held tolerance smile, unaddressed
    S += [s([(326,502),(348,498),(362,500),(382,496),(400,500)], 2.4)]
    S += [s([(334,514),(362,518),(392,510)], 1.8)]
    # FOREIGN HAND ONE: forearm MASS entering frame-left, hand at the band
    S += [s([(60,226),(140,238),(208,258)], 3.0)]                       # forearm top edge
    S += [s([(60,268),(138,276),(204,290)], 3.0)]                       # forearm bottom edge
    S += [s([(208,258),(238,262),(258,276)], 2.6)]                      # back of hand wedge
    S += [s([(204,290),(234,296),(254,300)], 2.6)]
    S += [s([(238,262),(262,270)], 1.8)]                                # finger 1 on band
    S += [s([(240,276),(264,284)], 1.8)]                                # finger 2
    S += [s([(238,290),(260,296)], 1.8)]                                # finger 3
    # FOREIGN HAND TWO: forearm MASS from upper-right, fingertips at band
    S += [s([(648,128),(566,164),(498,206)], 3.0)]
    S += [s([(668,162),(590,196),(520,234)], 3.0)]
    S += [s([(498,206),(474,222),(460,238)], 2.6)]                      # hand wedge to band
    S += [s([(520,234),(496,246),(478,256)], 2.6)]
    S += [s([(474,222),(456,242)], 1.8)]                                # fingertip 1
    S += [s([(484,232),(466,252)], 1.8)]                                # fingertip 2
    S += [s([(494,242),(478,258)], 1.6)]                                # fingertip 3
    # HIS OWN arm from frame-bottom keeps the drink up: forearm + cup
    S += [s([(560,760),(548,700),(534,660)], 3.0)]                      # forearm rising
    S += [s([(608,756),(596,700),(586,664)], 3.0)]
    S += [s([(508,624),(504,584)], 2.4)]                                # cup side L
    S += [s([(580,620),(584,582)], 2.4)]                                # cup side R
    S += [s([(502,582),(544,572),(586,580)], 2.0)]                      # rim
    S += [s([(508,624),(548,636),(582,622)], 2.4)]                      # cup base
    S += [s([(534,660),(508,640),(514,616)], 2.6)]                      # his fingers wrap the cup
    S += [s([(586,664),(590,632)], 2.2)]                                # thumb side
    # neck + party shoulders
    S += [s([(316,582),(312,640)], 2.4)]
    S += [s([(394,582),(400,638)], 2.4)]
    S += [s([(284,652),(354,674),(424,648)], 2.6)]
    S = tilt(S, 1.0)
    return S, [s([(258,380),(462,380)], 1.0)]


def f214_wait_that_wont_sit():
    """Entry 19. Standing mid-room, remote in one hand, phone in the
    other, face to the screen; the sofa waits unused. The stance is
    the sentence."""
    S = []
    # TV: rectangle right, glow ticks
    S += [s([(520,200),(672,188),(676,330),(524,344),(520,200)], 2.8)]
    S += [s([(534,216),(660,206)], 1.2)]                                # screen glow line
    S += [s([(534,250),(662,240)], 1.0)]
    S += [s([(536,290),(660,282)], 1.0)]
    S += [s([(586,344),(584,374)], 2.0)]                                # stand
    S += [s([(548,378),(628,372)], 2.2)]
    # sofa: low mass left, unused
    S += [s([(48,560),(60,470),(120,452),(232,446),(260,470),(262,556)], 2.8)]
    S += [s([(60,470),(96,488),(228,482),(260,470)], 1.8)]              # seat line
    S += [s([(48,560),(262,556)], 2.2)]
    # floor line
    S += [s([(40,640),(360,628),(680,636)], 2.0)]
    # ---- the figure: standing 3/4 back, head turned to the TV
    # head: back-of-skull dominant, jaw line toward screen
    S += [s([(352,238),(346,196),(372,170),(410,166),(436,186),(440,222)], 2.8)]
    S += [s([(360,180),(396,164),(428,172)], 2.0)]                      # hair mass
    S += [s([(440,222),(432,244),(414,254)], 2.2)]                      # jaw toward TV
    S += [s([(428,214),(436,212)], 1.4)]                                # far-eye hint only
    # neck, shoulders square to the room, weight EVEN — nobody leans
    S += [s([(384,256),(382,286)], 2.4)]
    S += [s([(414,254),(418,284)], 2.4)]
    S += [s([(322,300),(384,288),(452,296)], 3.0)]                      # shoulder line
    # torso straight — no settle, no slouch
    S += [s([(330,302),(326,392),(332,470)], 2.8)]                      # near side
    S += [s([(448,298),(454,388),(446,466)], 2.8)]                      # far side
    S += [s([(334,470),(390,482),(444,466)], 2.4)]                      # hip line
    # RIGHT arm: remote half-raised toward the screen
    S += [s([(448,310),(492,340),(520,376)], 2.7)]
    S += [s([(520,376),(548,372)], 2.4)]                                # hand
    S += [s([(548,372),(576,362)], 2.6)]                                # the remote, aimed
    # LEFT arm: phone held low at the hip
    S += [s([(330,312),(318,376),(326,432)], 2.7)]
    S += [s([(326,432),(346,444)], 2.2)]                                # hand at hip
    S += [s([(342,436),(362,452),(352,466)], 2.0)]                      # phone slab
    # legs: parallel, planted — the not-sitting
    S += [s([(348,478),(344,556),(346,624)], 2.8)]
    S += [s([(428,474),(434,552),(430,620)], 2.8)]
    S += [s([(346,624),(318,634)], 2.4)]                                # foot L
    S += [s([(430,620),(458,630)], 2.4)]                                # foot R
    S = tilt(S, 0.0)
    return S, [s([(384,256),(560,250)], 1.0)]


def f215_palm_rub():
    """Entry 13. Mid-rub: the palm owns half the face; the covered
    eye is gone beneath it, the free eye is closed too — the face
    yields ONLY while touched. Cap above; jaw slack under the hand."""
    S = []
    # cap: brim + crown, low over the face
    S += [s([(244,272),(308,250),(392,246),(458,262),(482,284)], 3.2)]
    S += [s([(258,250),(322,218),(404,214),(462,238)], 2.6)]
    # skull sides below cap
    S += [s([(252,288),(248,356),(260,420),(280,484),(310,530),(350,550)], 2.8)]
    S += [s([(470,292),(472,360),(462,424),(440,486),(406,532),(354,552)], 3.0)]
    S += [s([(314,538),(336,550),(368,550),(390,538)], 2.2)]
    # THE HAND: a closed silhouette that OWNS the covered half-face.
    # outer edge: heel at jaw → palm bulge → up past the eye → index base
    S += [s([(296,548),(258,508),(244,448),(248,388),(268,330),(296,298)], 3.4)]
    # inner edge: the boundary the face yields at — owned by the hand
    S += [s([(332,540),(346,470),(352,406),(346,352),(330,314)], 3.0)]
    # knuckle ridge closing the silhouette at the top
    S += [s([(296,298),(316,294),(330,314)], 2.6)]
    # fingers over the brow, rising PAST the cap edge (overlap resolves to hand)
    S += [s([(300,300),(308,268)], 2.4)]                                # index over brow
    S += [s([(316,296),(326,266)], 2.2)]                                # second
    S += [s([(330,302),(342,276)], 2.0)]                                # third
    S += [s([(296,524),(330,532)], 2.4)]                                # heel crease at jaw
    # forearm leaving frame lower-left
    S += [s([(282,560),(238,632),(196,700)], 3.0)]
    S += [s([(330,560),(296,636),(262,704)], 2.4)]
    # the FREE side of the face: eye closed, brow eased, mouth slack
    S += [s([(386,366),(412,372),(436,366)], 2.6)]                      # closed eye, down-curve
    S += [s([(392,380),(412,385),(430,380)], 1.3)]                      # lid fold
    S += [s([(382,344),(412,340),(440,345)], 2.5)]                      # brow eased
    S += [s([(372,388),(368,432)], 1.7)]                                # nose, half-hidden
    S += [s([(352,444),(372,452),(394,443)], 2.1)]
    # slack mouth, pulled slightly toward the rubbing hand
    S += [s([(340,494),(364,490),(386,494),(404,490)], 2.3)]
    S += [s([(348,506),(372,510),(396,503)], 1.7)]
    # neck
    S += [s([(318,552),(314,610)], 2.4)]
    S += [s([(388,552),(394,608)], 2.4)]
    S += [s([(290,622),(356,644),(422,618)], 2.6)]
    S = tilt(S, -2.0)
    return S, [s([(258,372),(470,372)], 1.0)]


SEQ = [("f213", f213_lent_head),
       ("f214", f214_wait_that_wont_sit),
       ("f215", f215_palm_rub)]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = []
    for name, fn in SEQ:
        Sx, G = fn()
        im = render(Sx, G, W, H, seed=hash(name) % 999)
        im.save(os.path.join(OUT, f"{name}.png"))
        imgs.append((name, im))
        print("wrote", name)
    sheet = Image.new("RGB", (3 * (W // 2) + 40, H // 2), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(imgs):
        x = i * (W // 2 + 20)
        sheet.paste(im.resize((W // 2, H // 2)), (x, 0))
        d.text((x + 10, 8), name, fill=(31, 29, 27))
    sheet.save(os.path.join(OUT, "_contact_2a_b03.png"))
    print("contact ok")
