"""
HUMAN STUDIES VOL. 1 — Assignment 1: One Hundred Heads.
Batch 03 (h021–h030). Observed June 11, 2026 — family archives (FB),
models.com New Faces, Wikimedia Commons photographs (1930s University
of Oregon students; two elders in severe profile). Session bias: young
and ordinary; the test is whether observation survives non-iconic faces.
Recognition standard for family heads: would the family know them?
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


# ---------------------------------------------------------------- h021
def h021_jim():
    """Jim Hess, 60. Black beret, full open grin. Lean tan face that
    has spent years outdoors — folds are weather AND joy. Pale eyes
    open despite the smile (unlike Lauren's). Head tips toward Jennifer."""
    S = []
    # beret: soft mass tilted across the crown, draping our right
    S += [s([(232,290),(238,222),(296,168),(372,150),(446,170),(488,222),(492,282),(470,310)], 3.8)]
    S += [s([(488,236),(508,270),(498,304)], 2.4)]               # the drape
    S += [s([(252,286),(330,262),(420,268),(470,296)], 2.2)]     # band edge
    # face: lean, tan; cheeks cut in, jaw still firm
    S += [s([(252,318),(246,388),(256,450),(274,510),(306,556),(348,576)], 2.8)]
    S += [s([(468,322),(472,392),(460,452),(438,512),(404,558),(354,578)], 3.4)]
    S += [s([(310,560),(336,574),(372,574),(398,560)], 2.2)]
    # brows: light, lifted by the grin
    S += [s([(276,360),(308,350),(340,356)], 2.0)]
    S += [s([(376,355),(408,347),(438,356)], 2.0)]
    # eyes: OPEN but crinkled — lower lid pushed up, iris still showing
    S += [s([(284,388),(310,380),(336,387)], 2.4)]
    S += [s([(302,384),(311,394),(300,394)], 2.4)]
    S += [s([(288,398),(312,402),(334,394)], 1.8)]
    S += [s([(380,386),(406,378),(430,385)], 2.4)]
    S += [s([(398,382),(407,392),(396,392)], 2.4)]
    S += [s([(384,396),(408,400),(428,392)], 1.8)]
    # crow's feet: two rays each — earned outdoors
    S += [s([(276,384),(262,378)], 1.2)]
    S += [s([(278,394),(264,396)], 1.2)]
    S += [s([(436,382),(450,376)], 1.2)]
    S += [s([(434,392),(448,394)], 1.2)]
    # nose: straight, weathered, slightly wide tip
    S += [s([(356,360),(352,430)], 1.9)]
    S += [s([(328,444),(352,455),(380,443)], 2.4)]
    # the GRIN: open, teeth, corners dug deep into the cheeks
    S += [s([(296,492),(330,481),(358,485),(386,479),(420,488)], 2.8)]   # upper lip
    S += [s([(308,500),(342,498),(376,497),(408,495)], 1.6)]             # tooth row
    S += [s([(304,510),(338,528),(374,530),(412,505)], 2.8)]             # open lower
    S += [s([(316,536),(356,546),(394,532)], 2.0)]
    # nasolabial: deep, structural, framing the grin
    S += [s([(326,448),(298,480),(292,500)], 2.2)]
    S += [s([(384,446),(414,476),(420,496)], 2.2)]
    # lean neck, open collar
    S += [s([(308,578),(302,636)], 2.6)]
    S += [s([(398,578),(406,634)], 2.6)]
    S += [s([(252,682),(310,644),(354,638)], 2.8)]
    S += [s([(456,678),(402,642),(360,638)], 2.8)]
    S = tilt(S, -6.0)
    G = [s([(252,386),(468,386)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h022
def h022_jennifer():
    """Jennifer Hess, ~60. Long blonde layered waves — real volume,
    crown to past the shoulders. Broad smile with upper teeth, eyes
    crinkled to warm crescents. The smile is her resting state."""
    S = []
    # hair: big — lifted crown, two LAYERED falls with real wave,
    # ends flipping away from the neck (not a hood)
    S += [s([(330,116),(282,128),(296,98),(360,90),(412,116)], 2.6)]   # crown lift
    S += [s([(330,120),(254,146),(208,220),(192,330),(206,452),(186,560),(214,656)], 3.6)]
    S += [s([(330,120),(404,142),(450,210),(462,318),(448,444),(472,552),(446,650)], 3.6)]
    S += [s([(214,656),(248,672),(282,660)], 2.4)]               # flip out
    S += [s([(446,650),(414,668),(382,658)], 2.4)]
    S += [s([(244,256),(218,350),(240,452),(218,548)], 1.6)]     # S-waves
    S += [s([(436,250),(460,346),(438,448),(460,542)], 1.6)]
    S += [s([(268,196),(246,266),(262,330)], 1.4)]               # layer break
    # hairline: soft side-swept
    S += [s([(280,300),(316,272),(360,264),(402,278),(428,308)], 1.9)]
    # face: soft oval, cheeks lifted by the smile, small round chin
    S += [s([(266,334),(260,402),(272,462),(292,516),(322,554),(356,570)], 2.8)]
    S += [s([(440,338),(446,406),(434,466),(412,520),(386,556),(360,572)], 3.2)]
    # brows: soft arcs, raised
    S += [s([(284,358),(314,346),(344,354)], 2.0)]
    S += [s([(376,352),(406,344),(434,354)], 2.0)]
    # eyes: warm crescents — nearly closed by the smile, tiny iris peek
    S += [s([(290,390),(316,382),(340,388)], 2.6)]
    S += [s([(294,397),(318,392),(338,395)], 1.5)]
    S += [s([(308,386),(316,393)], 1.8)]
    S += [s([(378,387),(404,379),(428,386)], 2.6)]
    S += [s([(382,394),(406,389),(424,393)], 1.5)]
    S += [s([(396,383),(404,390)], 1.8)]
    # crow's feet: one soft ray each — lighter than Jim's
    S += [s([(282,388),(270,384)], 1.1)]
    S += [s([(434,385),(446,381)], 1.1)]
    # nose: slim, neat
    S += [s([(354,362),(350,426)], 1.7)]
    S += [s([(330,438),(352,448),(376,437)], 2.1)]
    # smile: broad, upper teeth showing, lower lip soft
    S += [s([(298,490),(330,479),(358,483),(386,477),(418,487)], 2.8)]
    S += [s([(310,498),(342,496),(374,495),(406,493)], 1.5)]
    S += [s([(308,506),(340,520),(374,521),(410,502)], 2.6)]
    S += [s([(318,528),(356,537),(392,525)], 1.9)]
    # gentle folds bracketing the smile
    S += [s([(326,444),(302,474),(296,492)], 1.7)]
    S += [s([(382,442),(408,470),(414,488)], 1.7)]
    # drop earrings
    S += [s([(258,420),(254,448)], 1.5)]
    S += [s([(446,424),(452,450)], 1.5)]
    # neck, soft shoulder line
    S += [s([(316,572),(310,628)], 2.4)]
    S += [s([(392,572),(398,626)], 2.4)]
    S += [s([(244,676),(312,640),(360,634)], 2.8)]
    S += [s([(448,672),(400,638),(364,634)], 2.8)]
    S = tilt(S, 5.0)
    G = [s([(266,388),(440,388)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h023
def h023_jake():
    """Jake Hess — Jordan's cousin, early 30s. Selfie tilt, thin
    copper-rimmed round glasses, full dark beard wrapping the jaw,
    one-cheek smirk. The beard is a MASS with its own silhouette."""
    S = []
    # skull: round-ish, dark hair short with a low front
    S += [s([(240,302),(252,210),(316,160),(386,156),(448,194),(470,272),(474,314)], 3.2)]
    S += [s([(268,296),(306,260),(354,248),(404,262),(438,298)], 2.0)]
    S += [s([(348,250),(352,228)], 1.4)]                          # front tuft
    # face sides down to where the BEARD takes over
    S += [s([(246,318),(240,388),(252,448)], 2.8)]
    S += [s([(472,324),(476,394),(464,452)], 3.2)]
    # THE BEARD: silhouette first — wraps jaw, fuller at the chin
    S += [s([(252,448),(262,520),(290,572),(330,600),(376,602),(414,576),(442,522),(464,452)], 3.8)]
    S += [s([(276,452),(300,492),(296,524)], 1.4)]                # inner texture
    S += [s([(430,448),(412,490),(418,522)], 1.4)]
    # glasses: thin copper rounds, slightly down-tilted with the selfie
    S += [s([(272,366),(306,358),(338,366),(342,396),(330,416),(298,420),(272,408),(266,384),(272,366)], 2.2)]
    S += [s([(376,364),(410,356),(442,364),(446,392),(434,412),(402,416),(378,406),(372,382),(376,364)], 2.2)]
    S += [s([(342,382),(372,380)], 2.0)]
    S += [s([(266,378),(248,376)], 1.8)]
    S += [s([(446,376),(466,372)], 1.8)]
    # brows: straight, dark, just above the rims
    S += [s([(278,352),(310,346),(340,351)], 2.8)]
    S += [s([(378,350),(410,344),(440,350)], 2.8)]
    # eyes behind the lenses: medium, steady
    S += [s([(288,386),(310,380),(330,386)], 2.2)]
    S += [s([(304,383),(312,392),(302,392)], 2.2)]
    S += [s([(384,384),(406,378),(426,384)], 2.2)]
    S += [s([(400,381),(408,390),(398,390)], 2.2)]
    # nose: rounded tip resting just above the mustache
    S += [s([(356,372),(352,436)], 1.8)]
    S += [s([(334,448),(354,458),(378,447)], 2.2)]
    # mouth inside the beard: one-cheek smirk — right corner up
    S += [s([(318,506),(344,500),(362,503),(382,494),(404,488)], 2.6)]
    S += [s([(330,518),(360,524),(390,510)], 1.8)]
    S += [s([(408,480),(416,500)], 1.3)]                          # smirk crease
    # mustache joining the beard
    S += [s([(322,490),(352,482),(384,488)], 2.4)]
    # neck, tee collar
    S += [s([(318,602),(312,650)], 2.4)]
    S += [s([(388,602),(394,648)], 2.4)]
    S += [s([(296,656),(354,674),(410,652)], 2.6)]
    S = tilt(S, -8.0)
    G = [s([(246,386),(472,388)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h024
def h024_friend():
    """Jim's friend at the brewery, ~60. The anti-default skull: WIDE
    round head, thin side-parted hair flat to the scalp, small pouched
    eyes, ruddy full cheeks, broad closed smile, true double chin."""
    S = []
    # skull: WIDE — width rivals height
    S += [s([(206,330),(216,232),(282,168),(372,150),(458,172),(514,240),(520,334)], 3.4)]
    # thin hair: flat to scalp, side part, a few lie-down strands
    S += [s([(240,322),(290,282),(356,268),(424,280),(478,318)], 1.9)]
    S += [s([(300,278),(296,250)], 1.2)]                          # the part
    S += [s([(316,272),(366,258),(416,266)], 1.3)]                # combed over
    # face: full cheeks bulging the contour, short lower face
    S += [s([(210,344),(206,404),(220,458),(244,506),(280,544),(330,566)], 3.0)]
    S += [s([(516,348),(520,408),(504,462),(478,510),(440,548),(386,568)], 3.6)]
    # DOUBLE CHIN: chin shelf, then the second curve below
    S += [s([(284,540),(320,560),(372,562),(420,544)], 2.4)]
    S += [s([(268,576),(320,600),(390,600),(444,574)], 2.8)]
    # brows: faint, high on the big forehead
    S += [s([(258,372),(294,364),(330,370)], 1.8)]
    S += [s([(390,368),(426,361),(462,369)], 1.8)]
    # eyes: SMALL for the head — narrow, pouches beneath
    S += [s([(272,402),(296,396),(318,402)], 2.4)]
    S += [s([(288,399),(297,407)], 2.0)]
    S += [s([(276,412),(298,416),(316,410)], 1.4)]
    S += [s([(280,424),(300,428),(314,422)], 1.1)]                # the pouch
    S += [s([(400,400),(424,394),(446,400)], 2.4)]
    S += [s([(416,397),(425,405)], 2.0)]
    S += [s([(404,410),(426,414),(444,408)], 1.4)]
    S += [s([(406,422),(426,426),(440,420)], 1.1)]
    # nose: short, fleshy
    S += [s([(362,388),(358,442)], 1.8)]
    S += [s([(334,452),(360,464),(390,451)], 2.5)]
    # broad CLOSED smile pressed into full cheeks
    S += [s([(296,500),(334,512),(364,515),(396,509),(432,494)], 3.2)]
    S += [s([(308,524),(356,534),(408,518)], 2.2)]
    S += [s([(290,496),(282,512)], 1.5)]                          # cheek dig
    S += [s([(438,490),(446,506)], 1.5)]
    # ruddy cheek apples: one light arc each
    S += [s([(252,452),(272,470)], 1.2)]
    S += [s([(464,448),(444,466)], 1.2)]
    # thick neck flowing into polo collar; big shoulders
    S += [s([(280,604),(272,648)], 2.8)]
    S += [s([(436,602),(446,646)], 2.8)]
    S += [s([(268,652),(354,676),(450,648)], 3.0)]
    S += [s([(352,678),(348,720)], 2.0)]                          # placket
    S += [s([(220,700),(140,740)], 3.8)]
    S += [s([(496,696),(576,734)], 3.8)]
    S = tilt(S, 1.5)
    G = [s([(210,400),(516,400)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h025
def h025_nicolas():
    """Nicolas Knuth, under 30. Heavy LOW straight brows almost on the
    eyes, long straight nose, strong philtrum, lips a breath apart.
    Thick brown hair with lift. Young jaw — square but unweathered."""
    S = []
    # hair: thick mass with front lift, casual sides
    S += [s([(238,296),(244,206),(296,150),(372,130),(442,154),(472,216),(476,300)], 3.4)]
    S += [s([(296,166),(330,136),(372,128)], 1.8)]                # the lift
    S += [s([(262,290),(300,256),(352,244),(406,258),(442,292)], 2.0)]
    # face: young, square-ish jaw, smooth contour — minimal marks
    S += [s([(250,312),(244,384),(254,448),(272,510),(304,554),(348,574)], 2.8)]
    S += [s([(474,318),(478,390),(466,452),(444,514),(408,558),(354,576)], 3.2)]
    S += [s([(308,558),(334,572),(372,572),(398,558)], 2.2)]
    # BROWS: the feature — heavy, straight, LOW, almost touching the eyes
    S += [s([(276,374),(312,370),(344,374)], 3.8)]
    S += [s([(376,373),(410,368),(442,373)], 3.8)]
    # eyes directly beneath: steady, pale irises
    S += [s([(286,392),(312,386),(338,392)], 2.4)]
    S += [s([(304,389),(313,399),(302,399)], 2.4)]
    S += [s([(290,402),(314,405),(336,399)], 1.3)]
    S += [s([(380,390),(406,384),(430,390)], 2.4)]
    S += [s([(398,387),(407,397),(396,397)], 2.4)]
    S += [s([(384,400),(408,403),(428,397)], 1.3)]
    # nose: long, straight, defined tip
    S += [s([(358,380),(354,452)], 2.0)]
    S += [s([(334,462),(356,472),(382,461)], 2.3)]
    # philtrum + lips a breath apart
    S += [s([(354,478),(355,494)], 1.3)]
    S += [s([(318,508),(344,500),(360,504),(376,499),(400,507)], 2.7)]
    S += [s([(326,516),(358,521),(392,514)], 1.7)]
    S += [s([(326,528),(358,536),(390,526)], 2.2)]
    # tee neckline, young straight shoulders
    S += [s([(310,576),(304,632)], 2.4)]
    S += [s([(396,576),(402,630)], 2.4)]
    S += [s([(300,638),(356,656),(408,636)], 2.6)]
    S += [s([(246,676),(170,706)], 3.2)]
    S += [s([(460,672),(536,702)], 3.2)]
    S = tilt(S, -2.0)
    G = [s([(250,390),(474,390)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h026
def h026_simona():
    """Simona Bucekova, under 30. Sleek center-part falls flat on both
    sides. Deep-set eyes with a soft shadow beneath — shadow, not bag.
    Inner brow ends dip: a faint knit. Full lips held compressed."""
    S = []
    # hair: SLEEK — two flat falls, center part, no wave
    S += [s([(338,122),(270,140),(228,200),(212,300),(214,420),(226,540),(240,640)], 3.4)]
    S += [s([(338,122),(404,138),(444,196),(458,296),(454,416),(444,538),(434,636)], 3.4)]
    S += [s([(338,126),(336,170)], 1.6)]                          # the part
    S += [s([(244,300),(238,420),(248,530)], 1.3)]                # flat sheen
    S += [s([(430,296),(436,416),(428,528)], 1.3)]
    # face: lean but with a real jaw corner — not the default taper
    S += [s([(272,330),(266,398),(276,458),(286,506),(308,548),(348,566)], 2.8)]
    S += [s([(436,334),(442,402),(432,462),(422,510),(398,552),(354,568)], 3.2)]
    S += [s([(312,552),(336,564),(372,564),(394,552)], 2.0)]
    # brows: LOW, dark, straight — inner ends dipping (the knit)
    S += [s([(286,372),(316,366),(344,372),(350,378)], 2.9)]
    S += [s([(358,378),(364,371),(392,365),(420,371)], 2.9)]
    # deep-set eyes: lid + shadow arc beneath, irises dark and large
    S += [s([(292,396),(318,388),(342,395)], 2.5)]
    S += [s([(308,391),(318,402),(306,402)], 2.8)]
    S += [s([(296,406),(320,410),(340,403)], 1.3)]
    S += [s([(300,418),(320,421),(336,415)], 0.9)]                # the shadow
    S += [s([(366,394),(392,386),(416,393)], 2.5)]
    S += [s([(382,389),(392,400),(380,400)], 2.8)]
    S += [s([(370,404),(394,408),(414,401)], 1.3)]
    S += [s([(374,416),(394,419),(410,413)], 0.9)]
    # nose: straight, small flare
    S += [s([(356,378),(352,444)], 1.8)]
    S += [s([(332,454),(354,464),(378,453)], 2.2)]
    # mouth: full but COMPRESSED — pressure in the line between
    S += [s([(314,500),(340,494),(356,497),(372,492),(396,499)], 3.2)]
    S += [s([(322,492),(344,486),(357,489),(370,484),(388,490)], 1.9)]
    S += [s([(322,512),(355,520),(388,510)], 2.4)]
    # slim neck
    S += [s([(316,568),(312,628)], 2.3)]
    S += [s([(390,568),(394,626)], 2.3)]
    S += [s([(258,672),(316,640),(356,636)], 2.6)]
    S += [s([(444,668),(398,638),(360,636)], 2.6)]
    S = tilt(S, 1.0)
    G = [s([(272,392),(436,394)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h027
def h027_student_reading():
    """University of Oregon, 1930s. Head BOWED over a book, fist at
    the mouth, lost in the page. Near-profile from above-left: the
    crown dominates, the face foreshortens downward. She is not posing."""
    S = []
    # BOWED PROFILE facing left, head pitched down ~25°.
    # One skull sweep: nape high, crown forward-left, forehead diving.
    S += [s([(486,300),(458,222),(388,180),(310,184),(252,232),(232,300)], 3.4)]
    S += [s([(486,300),(492,360),(478,408)], 2.8)]                # nape
    # bob with soft fringe falling toward the brow — contour only
    S += [s([(232,300),(240,348),(260,376)], 2.6)]                # fringe mass
    S += [s([(478,408),(452,444),(420,458)], 2.4)]                # bob at nape
    S += [s([(300,196),(282,250),(290,300)], 1.4)]                # hair motion
    # the diving profile — ADULT proportions: face depth rivals cranium
    S += [s([(260,376),(250,416),(258,432)], 2.6)]                # brow
    S += [s([(258,432),(238,482),(242,498)], 2.4)]                # nose, down
    S += [s([(242,498),(258,508)], 1.8)]
    S += [s([(260,522),(276,530)], 2.0)]                          # upper lip
    S += [s([(268,540),(284,548)], 1.7)]                          # lower lip
    S += [s([(282,558),(300,582)], 2.2)]                          # small chin
    # downcast eye: a single lash arc, closed-looking — she reads
    S += [s([(284,442),(310,436),(328,440)], 2.4)]
    S += [s([(288,450),(310,446),(324,449)], 1.2)]
    S += [s([(278,414),(310,408),(334,412)], 1.9)]                # brow line
    # cheek, soft and young — one line home to the jaw
    S += [s([(300,582),(352,606),(420,610)], 2.8)]                # jaw back up
    # THE FIST tucked under the chin: back + two knuckles + thumb
    S += [s([(294,590),(278,614),(284,646),(308,662)], 2.6)]
    S += [s([(294,600),(312,594)], 1.6)]
    S += [s([(292,620),(312,614)], 1.6)]
    S += [s([(308,662),(332,650),(338,628)], 1.9)]
    # wrist into the lap
    S += [s([(300,668),(292,700),(298,724)], 2.4)]
    # shoulder hunched forward over the book; collar ticks
    S += [s([(420,610),(462,636),(500,680)], 3.2)]
    S += [s([(352,644),(396,668),(432,696)], 2.6)]
    S += [s([(372,658),(386,646)], 1.0)]
    S += [s([(400,676),(414,664)], 1.0)]
    # the book: one diagonal edge, lower left — where her eyes go
    S += [s([(180,660),(290,700),(400,720)], 2.8)]
    S += [s([(192,684),(290,720)], 1.8)]
    G = [s([(232,360),(486,340)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h028
def h028_student_bob():
    """University of Oregon, 1930s. Tight curly crop, squinting into
    the sun with a closed smile — cheeks up, lids low. Round young
    face. Checked dress. Holding a book that stays out of frame."""
    S = []
    # curly crop: bumpy OUTER contour carries the curl; hairline drops
    # low onto the forehead in two soft lobes — no interior squiggles
    S += [s([(244,318),(234,262),(252,224),(244,196),(280,170),(316,162),(344,144),(382,156),(416,158),(442,190),(462,222),(458,262),(466,316)], 3.2)]
    # hairline: ONE lazy arc, low on the forehead — no zigzag
    S += [s([(268,310),(330,334),(396,318),(428,314)], 2.0)]
    # face: round, young — full cheeks, small chin
    S += [s([(258,330),(252,396),(264,454),(286,506),(318,542),(352,556)], 2.8)]
    S += [s([(432,334),(438,400),(426,458),(404,510),(376,544),(356,558)], 3.2)]
    # brows: soft, lifted
    S += [s([(282,360),(312,350),(340,357)], 1.9)]
    S += [s([(374,355),(402,347),(428,356)], 1.9)]
    # SQUINT into the sun: lids low, small iris slivers, cheeks pushing up
    S += [s([(288,390),(314,383),(338,389)], 2.6)]
    S += [s([(304,387),(313,394)], 1.9)]
    S += [s([(292,398),(316,402),(336,395)], 1.7)]
    S += [s([(376,388),(402,381),(424,387)], 2.6)]
    S += [s([(392,385),(401,392)], 1.9)]
    S += [s([(380,396),(404,400),(422,393)], 1.7)]
    # nose: small, round tip
    S += [s([(354,366),(350,428)], 1.7)]
    S += [s([(332,438),(352,448),(374,437)], 2.1)]
    # closed smile, wide, pressed by the squint
    S += [s([(306,492),(338,502),(362,505),(388,499),(414,486)], 2.9)]
    S += [s([(316,514),(356,523),(398,508)], 2.1)]
    # young cheek apples — one short arc each, light
    S += [s([(280,448),(298,464)], 1.1)]
    S += [s([(412,444),(394,460)], 1.1)]
    # neck, checked collar V + ticks
    S += [s([(314,558),(308,612)], 2.4)]
    S += [s([(392,558),(398,610)], 2.4)]
    S += [s([(266,652),(322,620),(356,614)], 2.7)]
    S += [s([(444,648),(396,618),(360,614)], 2.7)]
    S += [s([(296,636),(312,650)], 1.0)]
    S += [s([(330,646),(346,660)], 1.0)]
    S += [s([(392,642),(408,628)], 1.0)]
    S = tilt(S, 3.0)
    G = [s([(258,388),(432,388)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h029
def h029_vintage_profile():
    """Early-20th-century photograph, ~70. TRUE left profile. Bald
    crown in one sweep, tuft at the nape, big central ear, hooked
    nose, mustache wedge, small chin into a high collar. Content."""
    S = []
    # the skull: one long sweep — forehead over crown to nape
    S += [s([(238,420),(232,330),(262,242),(330,186),(408,170),(474,196),(504,260)], 3.6)]
    S += [s([(504,260),(512,330),(498,392)], 3.0)]                # occipital
    S += [s([(494,396),(506,428),(492,456)], 2.0)]                # nape tuft
    # profile line: brow ridge → hooked nose → mustache → small chin
    S += [s([(238,420),(230,448),(236,464)], 2.8)]                # brow ridge
    S += [s([(236,464),(214,506),(212,520)], 3.0)]                # the hook
    S += [s([(212,520),(228,530),(238,534)], 2.0)]
    S += [s([(228,540),(208,548),(224,560),(248,562)], 2.6)]      # mustache wedge
    S += [s([(244,572),(256,578)], 1.8)]                          # lower lip
    S += [s([(252,588),(268,612),(290,630)], 2.6)]                # small chin
    S += [s([(290,630),(348,652),(420,650)], 3.0)]                # jaw back
    # the eye: deep socket under heavy brow, content squint
    S += [s([(248,440),(284,430),(312,434)], 3.0)]
    S += [s([(254,462),(280,456),(298,460)], 2.2)]
    S += [s([(262,470),(284,474),(298,468)], 1.3)]
    S += [s([(258,480),(276,484)], 1.0)]                          # under-crease
    # cheek: one hollow arc — age in the cheek, not the count
    S += [s([(286,500),(308,540),(304,576)], 1.5)]
    # EAR: big, central, the profile's anchor
    S += [s([(376,400),(412,386),(432,424),(420,478),(384,488)], 2.8)]
    S += [s([(392,414),(408,442),(396,466)], 1.5)]
    # high collar + tie knot; suit shoulder
    S += [s([(290,640),(286,676),(296,700)], 2.6)]
    S += [s([(420,652),(428,690)], 2.6)]
    S += [s([(296,676),(330,690),(326,716),(298,708),(296,676)], 2.0)]
    S += [s([(240,742),(330,704)], 3.6)]
    S += [s([(430,694),(540,738)], 3.6)]
    G = [s([(232,440),(504,440)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h030
def h030_holi_elder():
    """Holi festival, ~65+. Severe profile, head a touch down. The
    powder is ignored — structure only: sloped forehead, bushy brow,
    hooded downcast eye, strong hooked nose, wiry white mustache,
    furrowed brow. The mustache is the one place density is allowed."""
    S = []
    # skull: sloped forehead, head tipped down; hair short, rough
    S += [s([(262,400),(270,308),(318,234),(396,200),(468,212),(508,266)], 3.4)]
    S += [s([(508,266),(516,336),(502,400),(488,448)], 3.0)]
    S += [s([(330,224),(360,210)], 1.3)]                          # rough hair
    S += [s([(404,202),(434,206)], 1.3)]
    # brow furrows: two short lines — earned
    S += [s([(282,360),(316,348)], 1.4)]
    S += [s([(286,382),(318,372)], 1.4)]
    # profile: bushy brow step → hooked nose → mustache → chin down
    S += [s([(262,400),(252,424),(258,438)], 3.2)]                # brow step, heavy
    S += [s([(258,438),(232,486),(228,502)], 3.0)]                # the hook
    S += [s([(228,502),(244,512),(254,514)], 2.0)]
    # hooded DOWNCAST eye under the brow
    S += [s([(270,428),(300,420),(322,424)], 3.2)]                # bushy brow line
    S += [s([(276,448),(300,444),(316,448)], 2.2)]                # hood fold
    S += [s([(280,458),(300,454),(314,457)], 1.9)]                # lash, down
    # cheek: two deep folds — weathered, not ruined
    S += [s([(300,480),(322,520),(318,556)], 1.7)]
    S += [s([(338,470),(354,512)], 1.3)]
    # THE MUSTACHE: wiry white — five strokes, drooping past the lip
    S += [s([(246,524),(228,540),(216,558)], 2.2)]
    S += [s([(252,528),(238,548),(230,566)], 2.0)]
    S += [s([(258,532),(250,554),(246,572)], 1.8)]
    S += [s([(264,534),(262,558)], 1.6)]
    S += [s([(252,524),(282,530),(306,528)], 2.4)]                # its top edge
    # lower lip + chin, tucked
    S += [s([(268,580),(282,586)], 1.8)]
    S += [s([(276,596),(296,620),(322,636)], 2.6)]
    S += [s([(322,636),(380,656),(448,652)], 3.0)]
    # ear: high with the head tipped down
    S += [s([(404,384),(438,372),(456,408),(444,460),(410,468)], 2.6)]
    S += [s([(418,398),(434,424),(422,448)], 1.4)]
    # neck cords + simple collar
    S += [s([(322,646),(316,690)], 2.6)]
    S += [s([(448,656),(456,696)], 2.6)]
    S += [s([(346,652),(342,694)], 1.1)]
    S += [s([(310,700),(386,720),(460,702)], 2.8)]
    S = tilt(S, 3.0)
    G = [s([(262,430),(508,430)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h031
def h031_jordan():
    """Jordan Hess, 31 — from seventeen photos he provided. Anchor:
    the black-tank kitchen lean-in. The identity: textured quiff up
    and back, straight low brows over deep-set PALE eyes (irises
    outlined, never filled), strong straight nose, composed mouth
    with the fuller lower lip, lean cheeks, clean jaw. Youth = the
    marks stay out; the likeness lives in contour and gaze."""
    S = []
    # skull: front-heavy with the quiff's lift
    S += [s([(244,300),(254,210),(304,150),(368,138),(440,170),(468,252),(472,310)], 3.0)]
    # the quiff: curved SWEEPS following the brush direction, not hatching
    S += [s([(290,238),(308,184),(352,154),(396,148)], 2.2)]
    S += [s([(336,244),(358,196),(404,172)], 1.6)]
    # hairline: strong center, shallow temple recessions
    S += [s([(266,302),(300,262),(352,274),(402,260),(446,304)], 2.0)]
    # face: lean — narrower than instinct; high bone, clean jaw corner
    S += [s([(256,316),(250,388),(262,452),(280,514),(310,560),(352,580)], 2.8)]
    S += [s([(462,322),(466,394),(454,458),(434,518),(402,564),(356,582)], 3.3)]
    S += [s([(316,566),(338,580),(372,580),(396,566)], 2.3)]
    # brows: straight, level, low — they set the gaze
    S += [s([(280,360),(312,354),(342,358)], 2.8)]
    S += [s([(378,357),(410,351),(440,357)], 2.8)]
    # deep-set pale eyes: faint fold above, iris OUTLINED, small pupil
    S += [s([(288,378),(312,372),(336,377)], 1.3)]
    S += [s([(286,392),(312,384),(338,391)], 2.5)]
    S += [s([(306,386),(314,394),(307,401),(299,394),(306,386)], 1.3)]
    S += [s([(306,390),(310,394)], 1.7)]
    S += [s([(292,402),(314,406),(336,400)], 1.4)]
    S += [s([(382,376),(406,370),(430,375)], 1.3)]
    S += [s([(380,390),(406,382),(432,389)], 2.5)]
    S += [s([(400,384),(408,392),(401,399),(393,392),(400,384)], 1.3)]
    S += [s([(400,388),(404,392)], 1.7)]
    S += [s([(386,400),(408,404),(430,398)], 1.4)]
    # nose: strong, straight, defined tip and wings
    S += [s([(358,366),(354,440)], 2.0)]
    S += [s([(332,452),(354,462),(380,450)], 2.3)]
    S += [s([(326,444),(334,456)], 1.5)]
    S += [s([(386,442),(378,454)], 1.5)]
    # philtrum, then the composed mouth — corners level, lower lip fuller
    S += [s([(354,470),(355,484)], 1.2)]
    S += [s([(318,502),(344,496),(360,499),(376,494),(400,501)], 2.7)]
    S += [s([(326,494),(346,488),(360,491),(374,487),(392,493)], 1.7)]
    S += [s([(326,514),(358,522),(390,512)], 2.3)]
    # ears
    S += [s([(244,366),(230,382),(236,416),(252,424)], 2.0)]
    S += [s([(474,364),(488,380),(482,414),(466,422)], 2.0)]
    # long neck, athletic line, black tank straps
    S += [s([(312,582),(308,646)], 2.6)]
    S += [s([(396,582),(402,644)], 2.6)]
    S += [s([(308,648),(244,668),(168,684)], 3.2)]
    S += [s([(400,646),(464,666),(540,680)], 3.2)]
    S += [s([(286,668),(296,712)], 2.6)]
    S += [s([(420,664),(410,708)], 2.6)]
    S = tilt(S, -5.0)
    G = [s([(248,388),(470,390)], 1.0)]
    return S, G


HEADS = [
    ("h021", h021_jim),
    ("h022", h022_jennifer),
    ("h023", h023_jake),
    ("h024", h024_friend),
    ("h025", h025_nicolas),
    ("h026", h026_simona),
    ("h027", h027_student_reading),
    ("h028", h028_student_bob),
    ("h029", h029_vintage_profile),
    ("h030", h030_holi_elder),
    ("h031", h031_jordan),
]

if __name__ == "__main__":
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for name, fn in HEADS:
        if only and name not in only:
            continue
        S, G = fn()
        img = render(S, G, W, H, seed=hash(name) % 999)
        p = os.path.join(OUT, f"{name}.png")
        img.save(p)
        print("wrote", p)
