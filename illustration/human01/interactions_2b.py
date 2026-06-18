"""
HUMAN STUDIES VOL. 1 — ASSIGNMENT 2B: INTERACTION-CARRIED EVENTS.
Ten observations where the information exists BETWEEN people.
Per item: the event, the carrier, and the SMALLEST drawing that
still lets a stranger recover the event. Minimum structure is the
discipline — strokes are budgeted, not spent.

i01  receiving affection      — contact + two head attitudes
i02  reassurance arriving     — the arm + the tilt toward its owner
i03  telling <-> receiving    — the gaze axis + asymmetric states
i04  submitting to grooming   — hands at the head + parked eyes
i05  waiting for an answer    — the gap between two profiles
i06  tease across a room      — the pointing vector + answering arc
i07  posing together          — one shared aim, two programs
i08  the monitoring hold      — the cradle + the bow + the sprawl
i09  greeting the camera-hand — address vectors to an unseen person
i10  singing together         — synchrony: same shape, same lean
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import render               # noqa: E402
from heads_batch01 import s, tilt            # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def i01_receiving_affection():
    """A5DAD. Two contours meet; the receiver's chin is up, eyes
    closed, smile pressed. 11 strokes."""
    S = []
    # giver, profile from left: one travelling contour, crown to lips
    S += [s([(170,330),(176,240),(228,186),(292,176),(330,206),(346,250),(342,282),(356,300)], 3.2)]
    S += [s([(356,300),(352,316),(340,322)], 2.6)]       # lips at the cheek
    S += [s([(336,336),(310,386),(268,420)], 2.8)]       # giver jaw away
    S += [s([(196,206),(238,184),(284,180)], 2.0)]       # giver hair sweep
    # receiver, head tipped back-right
    S += [s([(360,296),(388,232),(452,206),(518,224),(548,288),(540,360),(508,428),(452,462)], 3.2)]
    S += [s([(452,462),(414,448),(380,406),(362,350),(360,296)], 2.8)]  # cheek the lips meet
    S += [s([(416,310),(442,320),(468,312)], 2.4)]       # closed eye, down-curve
    S += [s([(488,306),(512,314),(532,304)], 2.4)]       # second closed eye
    S += [s([(432,396),(462,408),(496,396)], 2.5)]       # pressed smile, curved up
    S += [s([(424,452),(452,468),(484,456)], 2.2)]       # lifted chin shelf
    S += [s([(444,470),(440,540)], 2.4)]                 # stretched throat
    return S, []


def i02_reassurance_arriving():
    """WWHL. Mid-speech, the arm comes around; the head tilts toward
    the arm's owner. The owner exists only as the arm. 9 strokes."""
    S = []
    # speaker's head, tilted right toward the arm's origin
    S += [s([(280,310),(296,222),(356,176),(424,182),(468,238),(470,318),(440,396),(380,428),(322,400),(288,348)], 3.2)]
    S += [s([(330,300),(356,294),(380,299)], 2.4)]       # eye line L (open, to lens)
    S += [s([(404,297),(428,291),(450,296)], 2.4)]       # eye line R
    S += [s([(346,368),(372,376),(400,366)], 2.5)]       # mouth mid-word, open a crack
    S += [s([(352,380),(376,386),(396,377)], 1.5)]
    # the speaker's torso, so there is a body to be held
    S += [s([(296,440),(266,500),(252,580)], 2.8)]            # near side
    S += [s([(448,420),(478,484),(492,566)], 2.8)]            # far side
    S += [s([(252,580),(360,604),(492,566)], 2.4)]            # chest line
    # the ARM: drapes over the far shoulder and crosses the chest
    S += [s([(680,380),(596,388),(516,416),(470,448)], 3.6)]  # upper edge, over the shoulder
    S += [s([(688,428),(606,434),(532,460),(486,486)], 3.0)]  # lower edge
    S += [s([(470,448),(410,492),(340,520)], 3.2)]            # forearm crossing the chest
    S += [s([(486,486),(428,520),(364,542)], 2.6)]
    S += [s([(340,520),(316,540),(326,562),(354,556)], 2.6)]  # the hand gripping the near shoulder
    S = tilt(S, 6.0)
    return S, []


def i03_telling_receiving():
    """F03EED. Teller mid-word; receiver's brows popped, smile one
    notch down, irises AT the teller. The axis carries it. 16."""
    S = []
    # teller, left, 3/4 toward right
    S += [s([(150,330),(160,248),(212,200),(276,196),(318,234),(326,304),(304,374),(252,406),(196,388),(160,352)], 3.0)]
    S += [s([(196,294),(220,288),(242,293)], 2.2)]       # teller eyes toward listener
    S += [s([(204,296),(212,303),(205,309),(198,303),(204,296)], 1.2)]  # iris right-shifted
    S += [s([(258,291),(280,286),(298,291)], 2.2)]
    S += [s([(266,293),(274,300),(267,306),(260,300),(266,293)], 1.2)]
    S += [s([(216,352),(240,364),(266,352)], 2.6)]       # mouth OPEN mid-word
    S += [s([(222,366),(244,372),(262,364)], 1.6)]
    # receiver, right, facing slightly left
    S += [s([(382,322),(394,240),(448,194),(514,192),(556,232),(562,304),(540,376),(486,408),(428,388),(392,348)], 3.0)]
    S += [s([(430,272),(456,262),(480,268)], 2.8)]       # brow popped HIGH
    S += [s([(498,266),(524,257),(546,264)], 2.8)]
    S += [s([(434,300),(458,293),(480,299)], 2.2)]
    S += [s([(438,302),(446,309),(439,315),(432,309),(438,302)], 1.2)]  # iris LEFT, at teller
    S += [s([(500,297),(524,290),(544,296)], 2.2)]
    S += [s([(503,299),(511,306),(504,312),(497,306),(503,299)], 1.2)]
    S += [s([(452,360),(484,370),(518,358)], 2.5)]       # closed smile, wide
    return S, []


def i04_submitting():
    """IMG_1154, minimum this time. One held head, two hand-wedges
    at the band, irises parked low-left. 12 strokes."""
    S = []
    S += [s([(266,330),(278,240),(338,194),(404,196),(452,242),(458,326),(430,402),(368,432),(306,404),(272,360)], 3.2)]
    S += [s([(282,276),(346,252),(414,256),(450,282)], 2.6)]            # the band
    # hand one, from left: short thick forearm, hand mass, fingertips ON the band
    S += [s([(140,242),(196,252),(232,264)], 3.4)]
    S += [s([(146,288),(198,292),(230,294)], 3.4)]
    S += [s([(232,264),(256,268),(272,278)], 2.8)]       # hand mass
    S += [s([(230,294),(254,296),(268,298)], 2.8)]
    S += [s([(272,278),(286,282)], 2.0)]                 # fingertip 1 at the band
    S += [s([(268,290),(284,292)], 2.0)]                 # fingertip 2
    S += [s([(264,300),(280,304)], 1.8)]                 # fingertip 3
    # hand two, from upper right: same anatomy, aimed at the band
    S += [s([(596,168),(548,196),(512,222)], 3.4)]
    S += [s([(624,204),(574,230),(540,254)], 3.4)]
    S += [s([(512,222),(492,238),(478,252)], 2.8)]
    S += [s([(540,254),(518,266),(502,276)], 2.8)]
    S += [s([(478,252),(464,264)], 2.0)]
    S += [s([(488,262),(474,274)], 2.0)]
    S += [s([(498,272),(486,282)], 1.8)]
    # parked eyes: lids level, irises low-left dots
    S += [s([(312,330),(336,324),(358,329)], 2.3)]
    S += [s([(316,336),(322,341),(317,345),(312,340),(316,336)], 1.2)]
    S += [s([(388,327),(412,321),(432,326)], 2.3)]
    S += [s([(391,333),(397,338),(392,342),(387,337),(391,333)], 1.2)]
    return S, []


def i05_waiting_for_answer():
    """Cuban two-shot. Two profiles facing across a gap; one mouth
    open, one sealed. The gap is the subject. 12 strokes."""
    S = []
    # asker, left profile: brow, nose, OPEN mouth
    S += [s([(150,250),(196,232),(226,252),(232,286),(222,300)], 3.0)]  # crown→brow
    S += [s([(222,300),(238,338),(232,356)], 2.6)]                      # nose
    S += [s([(228,372),(252,384),(244,402)], 2.6)]                      # open mouth wedge
    S += [s([(238,416),(226,452),(196,486)], 2.6)]                      # chin/jaw back
    S += [s([(150,250),(140,330),(152,420),(196,486)], 2.8)]            # back of head
    # answerer, right profile mirrored: brow, glasses tick, SEALED mouth
    S += [s([(548,242),(502,226),(472,248),(468,282),(478,296)], 3.0)]
    S += [s([(478,296),(462,336),(468,354)], 2.6)]
    S += [s([(486,304),(462,308)], 1.8)]                                # glasses arm tick
    S += [s([(460,382),(492,386)], 2.8)]                                # SEALED line
    S += [s([(466,400),(478,440),(508,478)], 2.6)]
    S += [s([(548,242),(560,326),(548,416),(508,478)], 2.8)]
    # the desk beneath the gap
    S += [s([(120,560),(350,552),(580,558)], 2.6)]
    return S, []


def i06_tease_across_room():
    """IMG_1326. The pointing vector and the answering laugh. Two
    seated masses; his arm is the sentence, her head-back the
    reply. 12 strokes."""
    S = []
    # him, left: seated mass + the long point
    S += [s([(120,420),(150,350),(202,330),(238,360),(240,420),(216,470)], 2.8)]   # torso mass
    S += [s([(186,322),(196,284),(228,272),(252,292),(248,326)], 2.6)]             # head
    S += [s([(240,360),(330,346),(430,338)], 3.4)]                                 # THE ARM, pointing
    S += [s([(430,338),(454,334)], 2.6)]                                           # finger
    S += [s([(140,470),(126,540)], 2.4)]                                           # chair leg hint
    # her, right: chair + head thrown BACK
    S += [s([(500,470),(508,396),(560,372),(610,392),(618,460),(598,500)], 2.8)]   # seated mass
    S += [s([(548,372),(540,330),(566,302),(602,306),(618,340),(610,372)], 2.6)]   # head tipped back
    S += [s([(560,330),(584,322),(604,330)], 2.2)]                                 # open laugh mouth, upturned
    S += [s([(486,430),(470,500)], 2.4)]
    # floor
    S += [s([(80,580),(360,572),(660,578)], 2.2)]
    return S, []


def i07_posing_together():
    """IMG_0426. One shared aim, two programs: four irises dead-on
    at the viewer; one mouth pouts, one holds level. 16 strokes."""
    S = []
    # head one, left — the pout
    S += [s([(150,340),(162,256),(218,212),(282,214),(322,256),(326,336),(298,402),(240,428),(186,402),(156,362)], 3.0)]
    S += [s([(196,300),(220,294),(242,299)], 2.2)]
    S += [s([(212,297),(220,304),(213,311),(206,304),(212,297)], 1.3)]  # iris dead-on
    S += [s([(258,297),(282,291),(302,296)], 2.2)]
    S += [s([(272,294),(280,301),(273,308),(266,301),(272,294)], 1.3)]
    S += [s([(228,366),(244,360),(258,366)], 2.6)]                      # pushed pout, small
    S += [s([(232,378),(246,384),(256,377)], 2.0)]
    # head two, right — the level program
    S += [s([(376,330),(388,248),(444,206),(508,208),(548,250),(552,330),(524,396),(466,422),(412,396),(382,356)], 3.0)]
    S += [s([(422,294),(446,288),(468,293)], 2.2)]
    S += [s([(438,291),(446,298),(439,305),(432,298),(438,291)], 1.3)]  # iris dead-on
    S += [s([(484,291),(508,285),(528,290)], 2.2)]
    S += [s([(498,288),(506,295),(499,302),(492,295),(498,288)], 1.3)]
    S += [s([(442,366),(468,369),(496,364)], 2.4)]                      # level mouth, held
    # shoulders touching: one continuous line under both
    S += [s([(140,470),(250,492),(360,478),(470,494),(572,472)], 2.8)]
    return S, []


def i08_monitoring_hold():
    """IMG_4988. The cradle arc, the bowed big head, the sprawled
    small one. Trust is the flung arm. 11 strokes."""
    S = []
    # his head, bowed deep toward the crook
    S += [s([(280,210),(296,150),(354,122),(416,134),(448,182),(440,242),(404,280)], 3.0)]
    S += [s([(404,280),(372,296),(338,290)], 2.4)]       # face turned down — jaw toward infant
    S += [s([(360,236),(382,244),(404,236)], 2.2)]       # downcast eye line (one is enough at this bow)
    # the cradle: one long arm arc from shoulder, under, and up
    S += [s([(250,320),(252,420),(310,490),(420,508),(510,470),(540,408)], 3.6)]
    S += [s([(540,408),(536,360),(508,330)], 2.8)]       # forearm closing the crook
    # the infant: small head in the crook, body along the arm
    S += [s([(452,366),(448,332),(480,316),(508,334),(508,368),(482,384),(452,366)], 2.6)]
    S += [s([(448,388),(404,418),(352,434)], 2.4)]       # body line down the cradle
    # THE SPRAWL: one arm flung out, open-handed, unheld
    S += [s([(486,388),(540,432),(584,448)], 2.4)]
    S += [s([(584,448),(598,442)], 1.6)]                 # tiny open hand
    S += [s([(396,430),(386,470)], 1.8)]                 # a leg dangling free
    return S, []


def i09_greeting_camera_hand():
    """IMG_8979. Both palms up AT the viewer, grin aimed the same
    way: the second person is wherever you are. 13 strokes."""
    S = []
    S += [s([(262,300),(274,218),(332,176),(396,178),(438,220),(442,300),(414,364),(356,392),(300,366),(268,326)], 3.0)]
    S += [s([(306,272),(330,266),(352,271)], 2.2)]
    S += [s([(318,269),(326,276),(319,283),(312,276),(318,269)], 1.3)]  # eyes at YOU
    S += [s([(368,269),(392,263),(412,268)], 2.2)]
    S += [s([(380,266),(388,273),(381,280),(374,273),(380,266)], 1.3)]
    S += [s([(312,330),(336,344),(366,346),(394,332)], 2.6)]            # open grin
    S += [s([(320,344),(354,354),(388,338)], 1.6)]
    # two raised palms flanking the face, fingers up, facing viewer
    S += [s([(180,360),(172,290),(186,250),(214,244),(226,300),(222,358)], 2.8)]
    S += [s([(186,250),(184,228)], 1.8)]
    S += [s([(202,246),(202,222)], 1.8)]
    S += [s([(478,352),(486,284),(474,246),(448,242),(438,296),(444,352)], 2.8)]
    S += [s([(474,246),(478,222)], 1.8)]
    S += [s([(458,240),(460,216)], 1.8)]
    # shoulders
    S += [s([(220,430),(354,458),(478,426)], 2.8)]
    return S, []


def i10_singing_together():
    """296ef. Synchrony: the same mouth shape twice, the same lean
    twice. The repetition IS the event. 14 strokes."""
    S = []
    # two heads, parallel lean (both tilted ~8 left), side by side
    # head one
    S += [s([(160,360),(150,276),(196,222),(260,210),(310,246),(322,322),(298,392),(240,422),(186,400)], 3.0)]
    S += [s([(206,300),(230,293),(252,299)], 2.2)]
    S += [s([(268,296),(292,289),(312,295)], 2.2)]
    S += [s([(226,356),(244,348),(262,352),(276,346)], 2.4)]            # the lyric shape: open oval
    S += [s([(230,368),(252,374),(272,364)], 2.0)]
    # head two — the SAME contour translated, the same mouth
    S += [s([(390,372),(380,288),(426,234),(490,222),(540,258),(552,334),(528,404),(470,434),(416,412)], 3.0)]
    S += [s([(436,312),(460,305),(482,311)], 2.2)]
    S += [s([(498,308),(522,301),(542,307)], 2.2)]
    S += [s([(456,368),(474,360),(492,364),(506,358)], 2.4)]            # same oval, same angle
    S += [s([(460,380),(482,386),(502,376)], 2.0)]
    # shoulders overlapping — leaning together
    S += [s([(130,470),(240,496),(350,482)], 2.8)]
    S += [s([(350,482),(460,506),(572,486)], 2.8)]
    S += [s([(316,430),(348,470)], 2.2)]                                # the lean contact line
    S = tilt(S, -6.0)
    return S, []


SEQ = [("i01", i01_receiving_affection), ("i02", i02_reassurance_arriving),
       ("i03", i03_telling_receiving),   ("i04", i04_submitting),
       ("i05", i05_waiting_for_answer),  ("i06", i06_tease_across_room),
       ("i07", i07_posing_together),     ("i08", i08_monitoring_hold),
       ("i09", i09_greeting_camera_hand),("i10", i10_singing_together)]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = []
    for name, fn in SEQ:
        Sx, G = fn()
        im = render(Sx, G, W, H, seed=hash(name) % 999)
        im.save(os.path.join(OUT, f"{name}.png"))
        imgs.append((name, im))
        print("wrote", name)
    cols = 5
    sheet = Image.new("RGB", (cols * W // 2, 2 * H // 2), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for n, (name, im) in enumerate(imgs):
        x, y = (n % cols) * W // 2, (n // cols) * H // 2
        sheet.paste(im.resize((W // 2, H // 2)), (x, y))
        d.text((x + 10, y + 8), name, fill=(31, 29, 27))
    sheet.save(os.path.join(OUT, "_contact_2b.png"))
    print("contact ok")
