"""
HUMAN STUDIES VOL. 1 — Assignment 1: One Hundred Heads.
Batch 02 (h011–h020). Observed June 11, 2026 — models.com Legends
(women + men). Session bias per review: over fifty, profiles, hair as
MASS (silhouette first), and eyes drawn as relationships, not objects.
Age marks are legitimate here — everyone in this pool earned them.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


# ---------------------------------------------------------------- h011
def h011_carmen():
    """Carmen Dell'Orefice, 90s. TRUE PROFILE facing left, chin lifted —
    regal. Enormous sculptural hat: the mass drawn first, one form.
    Deep-set hooded eye, long straight nose, hollow cheek, wrapped neck."""
    S = []
    # THE HAT — silhouette first, heavy line, one huge form
    S += [s([(196,338),(150,250),(176,140),(290,72),(420,62),(534,120),(566,232),(530,330),(470,352)], 4.2)]
    # two interior folds only — the form does the work
    S += [s([(260,120),(310,180),(300,260)], 1.8)]
    S += [s([(460,110),(440,200),(470,280)], 1.8)]
    # white hair, a soft sweep at the hat's front edge
    S += [s([(238,300),(262,272),(292,260)], 2.0)]
    # PROFILE LINE — one spine: brow → straight nose → thin lips → chin
    S += [s([(252,328),(242,360),(230,394)], 2.8)]              # brow → bridge
    S += [s([(230,394),(212,442),(208,452)], 3.0)]              # the long nose
    S += [s([(208,452),(222,462),(230,468)], 2.0)]              # under-nose
    S += [s([(226,480),(240,486)], 2.2)]                        # thin upper lip
    S += [s([(232,494),(246,500)], 1.8)]                        # thin lower lip
    S += [s([(240,510),(258,540),(286,560)], 2.8)]              # lifted chin
    # jaw underside sweeping back — chin is UP
    S += [s([(286,560),(348,576),(412,560)], 2.6)]
    # deep-set hooded eye: heavy brow, lid fold, short lash line, no iris
    S += [s([(258,338),(296,326),(326,330)], 3.0)]
    S += [s([(262,360),(290,354)], 1.6)]                        # the fold
    S += [s([(258,372),(284,368)], 2.2)]                        # lashes, lowered
    # cheekbone and the hollow under it — she is built of bone
    S += [s([(300,388),(330,420),(338,456)], 1.6)]
    S += [s([(300,460),(316,496)], 1.2)]
    # ear, low and back
    S += [s([(396,400),(416,412),(412,452),(392,460)], 2.0)]
    # wrapped neck — high scarf, diagonal folds, neck cords implied not drawn
    S += [s([(296,580),(280,640),(286,700)], 3.0)]
    S += [s([(412,564),(432,628),(428,696)], 3.0)]
    S += [s([(292,612),(352,628),(414,610)], 2.2)]
    S += [s([(296,664),(356,680),(420,660)], 2.2)]
    S = tilt(S, 4.0)
    G = [s([(230,394),(396,404)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h012
def h012_iman():
    """Iman, ~70. Three-quarter left. Feline eyes — inner corner low,
    outer corner LIFTED with a flick; this eye is not the formula eye.
    Slicked hair with one finger-wave. Bone everywhere. Fur below."""
    S = []
    # skull, hair slicked tight to it
    S += [s([(238,300),(250,202),(316,154),(386,150),(446,190),(466,268),(470,308)], 3.2)]
    S += [s([(272,290),(312,262),(362,256),(412,272),(440,302)], 2.0)]
    # the finger-wave: one arc dipping onto the forehead
    S += [s([(298,262),(322,296),(296,318)], 2.0)]
    # face: high cheekbones, planes, sharp jaw with a real corner
    S += [s([(244,316),(238,386),(252,448),(272,510),(304,556),(348,578)], 3.0)]
    S += [s([(468,322),(472,392),(458,452),(438,512),(404,560),(354,580)], 3.8)]
    S += [s([(308,560),(334,576),(372,576),(400,562)], 2.4)]
    # cheekbone accents — following the bone, attached to the contour
    S += [s([(252,420),(276,446)], 1.4)]
    S += [s([(462,418),(438,444)], 1.4)]
    # brows: strong, tapering, arched
    S += [s([(268,362),(304,346),(342,352)], 3.0)]
    S += [s([(374,350),(408,342),(440,354)], 3.0)]
    # FELINE eyes: lid angled up to an outer flick; iris under outer third
    S += [s([(282,394),(310,382),(338,378)], 2.6)]
    S += [s([(338,378),(350,371)], 2.6)]                        # the flick
    S += [s([(316,381),(325,391),(314,392)], 2.6)]
    S += [s([(288,400),(314,402),(336,389)], 1.5)]
    S += [s([(376,378),(400,368),(420,366)], 2.6)]
    S += [s([(420,366),(432,359)], 2.6)]
    S += [s([(402,368),(411,378),(400,379)], 2.6)]
    S += [s([(380,384),(402,388),(418,376)], 1.5)]
    # nose: slim bridge, flared wings
    S += [s([(356,362),(352,436)], 1.8)]
    S += [s([(328,452),(352,462),(380,450)], 2.4)]
    S += [s([(322,442),(332,456)], 1.6)]
    S += [s([(386,440),(376,454)], 1.6)]
    # mouth: defined, firm, slight asymmetric set
    S += [s([(312,506),(340,498),(358,502),(376,496),(402,503)], 3.0)]
    S += [s([(320,497),(342,487),(358,492),(372,486),(394,496)], 2.2)]
    S += [s([(320,518),(356,530),(392,516)], 2.6)]
    # FUR — mass silhouette first: a full scalloped cloud around the neck
    S += [s([(150,690),(168,616),(228,576),(310,560),(396,558),(478,576),(534,614),(548,684)], 4.2)]
    S += [s([(196,648),(222,668),(208,696)], 1.5)]
    S += [s([(300,580),(316,604),(300,624)], 1.5)]
    S += [s([(420,576),(440,600),(426,622)], 1.5)]
    S += [s([(496,640),(516,664),(502,690)], 1.5)]
    S = tilt(S, -2.0)
    G = [s([(244,388),(468,390)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h013
def h013_isabella():
    """Isabella Rossellini, ~70. Head tipped hard onto her hand, ROUND
    face, wide closed red smile. The eyes are crescents — lower lids
    pushed up until the eye nearly closes. Crow's feet are joy here."""
    S = []
    # short dark curls: lumpy mass, hand sweeping into it
    S += [s([(236,288),(232,196),(296,138),(376,126),(444,162),(472,242),(470,296)], 3.6)]
    S += [s([(282,170),(306,196),(286,216)], 1.6)]
    S += [s([(388,148),(412,176),(392,200)], 1.6)]
    # the hand: two finger curves already INSIDE the curls — no sticks
    S += [s([(252,176),(282,196),(300,224)], 2.2)]
    S += [s([(276,156),(306,178),(322,206)], 2.0)]
    # hairline: soft, a little low
    S += [s([(268,294),(310,268),(360,262),(410,276),(444,304)], 2.0)]
    # face: ROUND — cheeks bulge, soft jowl S-curve before the chin
    S += [s([(242,318),(232,390),(240,456),(262,516),(280,548),(276,560),(304,584),(348,600)], 3.0)]
    S += [s([(466,324),(476,396),(468,460),(448,518),(432,548),(438,562),(410,586),(356,602)], 3.4)]
    # brows: soft, round, lifted by the smile
    S += [s([(276,358),(310,346),(342,354)], 2.4)]
    S += [s([(376,352),(408,344),(438,356)], 2.4)]
    # CRESCENT eyes: upper lid and pushed-up lower lid nearly meet
    S += [s([(284,392),(312,382),(338,390)], 2.6)]
    S += [s([(288,398),(314,392),(334,396)], 2.2)]
    S += [s([(380,390),(406,380),(430,389)], 2.6)]
    S += [s([(384,396),(408,390),(426,394)], 2.2)]
    # crow's feet: two rays each side — earned
    S += [s([(276,388),(262,382)], 1.2)]
    S += [s([(278,398),(264,400)], 1.2)]
    S += [s([(436,386),(450,380)], 1.2)]
    S += [s([(434,396),(448,398)], 1.2)]
    # nose: small, widened by the smile
    S += [s([(356,366),(352,428)], 1.8)]
    S += [s([(330,442),(354,452),(380,441)], 2.2)]
    # the SMILE: wide, closed, red — corners dug in; folds frame it
    S += [s([(296,496),(330,512),(358,516),(386,510),(420,492)], 3.6)]
    S += [s([(306,524),(354,540),(404,520)], 2.8)]
    S += [s([(292,500),(286,510)], 1.6)]                        # corner dimples
    S += [s([(424,496),(430,506)], 1.6)]
    S += [s([(322,446),(300,476),(294,494)], 1.8)]              # smile folds
    S += [s([(388,444),(412,474),(420,490)], 1.8)]
    # high red collar, folded
    S += [s([(280,600),(258,650),(276,706)], 3.2)]
    S += [s([(428,602),(452,648),(436,702)], 3.2)]
    S += [s([(288,640),(354,664),(424,636)], 2.4)]
    S = tilt(S, -10.0)
    G = [s([(242,390),(466,392)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h014
def h014_lauren():
    """Lauren Hutton, ~80. Open smile, teeth, THE GAP. Short tousled
    hair. Eyes nearly shut by the smile. Every fold on this face is
    information: age and delight in the same marks."""
    S = []
    # hair: short, tousled — scruffy mass contour, few flicks
    S += [s([(244,296),(240,212),(288,154),(360,134),(428,158),(462,224),(460,296)], 3.2)]
    S += [s([(296,160),(312,128)], 1.6)]
    S += [s([(352,140),(360,110)], 1.6)]
    S += [s([(404,156),(422,128)], 1.6)]
    S += [s([(270,290),(308,262),(356,254),(406,268),(438,298)], 1.9)]
    # face: high cheekbones, soft aged jaw
    S += [s([(248,312),(242,384),(252,448),(270,508),(300,552),(344,574)], 2.8)]
    S += [s([(462,318),(466,390),(454,452),(434,512),(402,556),(350,576)], 3.4)]
    # brows: light, raised by the smile
    S += [s([(274,356),(308,346),(340,352)], 1.8)]
    S += [s([(374,350),(406,342),(436,352)], 1.8)]
    # eyes nearly SHUT: single curved crease each + crow's rays
    S += [s([(282,390),(310,382),(336,388)], 2.6)]
    S += [s([(286,396),(312,392),(332,394)], 1.4)]
    S += [s([(378,388),(404,380),(428,387)], 2.6)]
    S += [s([(382,394),(406,390),(424,392)], 1.4)]
    S += [s([(274,386),(260,380)], 1.2)]
    S += [s([(276,396),(262,398)], 1.2)]
    S += [s([(434,384),(448,378)], 1.2)]
    S += [s([(432,394),(446,396)], 1.2)]
    # nose: strong, a little wide at the base
    S += [s([(354,362),(350,432)], 1.9)]
    S += [s([(326,446),(352,458),(382,445)], 2.4)]
    # the OPEN smile: upper lip up, tooth row, THE GAP, open lower curve
    S += [s([(298,494),(330,484),(358,488),(386,482),(416,490)], 2.8)]   # upper lip
    S += [s([(310,502),(342,500),(374,499),(406,498)], 1.6)]             # tooth row
    S += [s([(356,490),(357,500)], 1.8)]                                 # the gap
    S += [s([(306,512),(338,530),(372,532),(404,508)], 2.8)]             # open lower
    S += [s([(316,538),(354,548),(392,534)], 2.0)]                       # lower lip
    # smile folds, deep and honest
    S += [s([(322,450),(296,482),(292,502)], 2.0)]
    S += [s([(384,448),(412,478),(418,498)], 2.0)]
    # aged neck: two light cords, robe collar soft
    S += [s([(306,576),(300,634)], 2.4)]
    S += [s([(396,578),(404,632)], 2.4)]
    S += [s([(330,584),(328,628)], 1.1)]
    S += [s([(368,586),(370,630)], 1.1)]
    S += [s([(244,684),(310,646),(356,640)], 3.0)]
    S += [s([(458,680),(400,644),(360,640)], 3.0)]
    S = tilt(S, 3.0)
    G = [s([(248,388),(462,390)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h015
def h015_nadja():
    """Nadja Auermann, ~55. Chin tucked, hooded eyes UP — ice. The
    trench collar is a funnel around the head; it frames everything.
    Hooded eye = lid FOLD above the lash line, opening kept small."""
    S = []
    # tousled blonde bob: mass first, wind in it
    S += [s([(228,330),(224,224),(284,156),(364,138),(440,164),(472,242),(468,340)], 3.4)]
    S += [s([(252,250),(238,310),(252,372),(244,420)], 2.2)]   # bob falls
    S += [s([(456,256),(470,316),(458,378),(466,418)], 2.2)]
    S += [s([(300,170),(330,150)], 1.4)]
    S += [s([(380,146),(412,162)], 1.4)]
    S += [s([(268,300),(308,272),(356,264),(404,276),(436,306)], 1.9)]
    # face: squarish, softened; chin tucked so the jaw shortens
    S += [s([(256,318),(250,388),(260,448),(278,504),(308,544),(350,562)], 2.8)]
    S += [s([(452,322),(456,392),(446,452),(428,508),(398,548),(354,564)], 3.4)]
    S += [s([(312,540),(336,556),(372,556),(396,542)], 2.2)]
    # brows: straight, low
    S += [s([(280,364),(312,358),(342,362)], 2.4)]
    S += [s([(376,361),(408,355),(438,361)], 2.4)]
    # HOODED eyes up: fold line above lashes, iris hung, opening small
    S += [s([(286,384),(312,378),(336,383)], 1.6)]              # the fold
    S += [s([(288,396),(312,388),(336,394)], 2.6)]              # lash line
    S += [s([(306,390),(314,400),(304,400)], 2.4)]              # iris, up
    S += [s([(292,404),(314,407),(334,402)], 1.3)]
    S += [s([(380,382),(406,376),(430,382)], 1.6)]
    S += [s([(382,394),(406,386),(430,392)], 2.6)]
    S += [s([(398,388),(406,398),(396,398)], 2.4)]
    S += [s([(386,402),(408,405),(428,400)], 1.3)]
    # nose: straight, neat
    S += [s([(356,372),(352,436)], 1.8)]
    S += [s([(334,448),(354,457),(376,447)], 2.2)]
    # mouth: closed, level, faintly down at the corners
    S += [s([(316,498),(342,492),(358,495),(374,491),(398,498)], 2.8)]
    S += [s([(324,510),(356,519),(388,508)], 2.2)]
    # THE COLLAR — funnel: wide of the head, clear air between
    S += [s([(160,660),(178,520),(238,430)], 4.2)]
    S += [s([(552,650),(530,514),(474,426)], 4.2)]
    S += [s([(196,650),(212,540),(258,462)], 2.2)]              # inner edge
    S += [s([(518,642),(500,534),(456,458)], 2.2)]
    S += [s([(186,716),(356,676),(528,710)], 3.6)]              # coat body
    S = tilt(S, -3.0)
    G = [s([(256,390),(452,392)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h016
def h016_pat():
    """Pat Cleveland, ~70s. The curl cloud — mass silhouette FIRST,
    a ring of linked arcs twice the skull. Head back a touch, lids
    lowered, serene. Eyes nearly closed looking down: no iris at all."""
    S = []
    # THE CLOUD: one continuous bumpy silhouette, heavy
    S += [s([(208,400),(170,300),(196,190),(280,110),(390,92),(488,130),(540,230),(528,340),(488,416)], 4.2)]
    # interior: three small curl arcs only — the silhouette already won
    S += [s([(252,212),(276,238),(254,262)], 1.4)]
    S += [s([(420,160),(446,186),(424,210)], 1.4)]
    S += [s([(480,300),(500,328),(478,350)], 1.4)]
    # hairline: soft, oval face revealed low in the cloud
    S += [s([(280,318),(318,294),(364,288),(408,302),(434,330)], 2.0)]
    # face: oval, fine-boned, head tipped back slightly
    S += [s([(264,340),(258,404),(268,462),(286,514),(316,552),(354,568)], 2.8)]
    S += [s([(438,346),(444,410),(434,466),(414,518),(386,554),(358,570)], 3.2)]
    # brows: thin, HIGH arches — drawn, deliberate
    S += [s([(288,376),(316,362),(344,370)], 1.8)]
    S += [s([(376,368),(402,360),(426,372)], 1.8)]
    # LOWERED eyes: two down-curved lash lines each, no iris, no white
    S += [s([(294,404),(320,398),(342,404)], 2.6)]
    S += [s([(298,412),(322,408),(340,412)], 1.4)]
    S += [s([(378,402),(402,396),(424,403)], 2.6)]
    S += [s([(382,410),(404,406),(422,410)], 1.4)]
    # nose: slim, tipped-back base shows a little
    S += [s([(358,380),(354,440)], 1.7)]
    S += [s([(336,450),(356,460),(378,449)], 2.2)]
    # mouth: gentle, corners soft — almost a smile, not performed
    S += [s([(316,500),(342,494),(358,497),(374,493),(396,500)], 2.6)]
    S += [s([(324,512),(356,520),(388,510)], 2.0)]
    # drop earrings: two small marks each
    S += [s([(254,420),(250,444)], 1.6)]
    S += [s([(448,424),(454,448)], 1.6)]
    # necklace: arc of dashes; sequin wrap shoulders
    S += [s([(308,600),(356,612),(404,598)], 1.4)]
    S += [s([(280,640),(244,680),(232,720)], 3.4)]
    S += [s([(420,642),(458,678),(472,716)], 3.4)]
    S += [s([(300,656),(296,672)], 1.2)]
    S += [s([(396,654),(402,670)], 1.2)]
    S = tilt(S, 3.5)
    G = [s([(264,400),(438,404)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h017
def h017_paulina():
    """Paulina Porizkova, ~60. Full open laugh — mouth wide, tooth row,
    eyes crushed to crescents, brows up. Long gray waves as MASS. The
    folds bracketing the laugh are deep and they stay."""
    S = []
    # long gray waves: two big falls, drawn as silhouette masses
    S += [s([(330,118),(250,140),(196,210),(176,320),(186,450),(210,570),(238,660)], 3.6)]
    S += [s([(330,118),(408,134),(462,196),(486,300),(478,430),(456,556),(436,648)], 3.6)]
    S += [s([(238,250),(222,360),(236,470)], 1.6)]              # wave motion
    S += [s([(444,240),(460,350),(446,460)], 1.6)]
    # hairline high, face open
    S += [s([(282,296),(318,272),(360,266),(400,280),(426,308)], 1.9)]
    # face: heart-shaped, cheeks lifted hard by the laugh
    S += [s([(268,330),(262,398),(274,458),(294,512),(322,550),(354,566)], 2.8)]
    S += [s([(440,336),(446,404),(434,462),(412,516),(386,552),(358,568)], 3.2)]
    # brows: RAISED, open arcs
    S += [s([(286,352),(316,338),(346,348)], 2.2)]
    S += [s([(376,346),(406,336),(434,350)], 2.2)]
    # eyes CRUSHED shut: downward crescents + rays — pure laugh
    S += [s([(292,388),(318,380),(342,386)], 2.8)]
    S += [s([(296,394),(320,390),(338,392)], 1.4)]
    S += [s([(378,384),(404,376),(428,384)], 2.8)]
    S += [s([(382,392),(406,388),(424,390)], 1.4)]
    S += [s([(284,384),(270,378)], 1.3)]
    S += [s([(286,394),(272,396)], 1.3)]
    S += [s([(434,382),(448,376)], 1.3)]
    S += [s([(432,392),(446,394)], 1.3)]
    # nose: small, stretched by the smile
    S += [s([(356,360),(352,420)], 1.7)]
    S += [s([(332,432),(354,442),(378,431)], 2.2)]
    # the LAUGH: wide open — stretched upper lip, teeth, deep lower bowl
    S += [s([(294,478),(328,466),(358,470),(388,464),(422,474)], 2.8)]
    S += [s([(306,488),(340,485),(374,484),(410,483)], 1.6)]    # tooth row
    S += [s([(340,486),(341,495)], 1.0)]                         # tooth split
    S += [s([(374,485),(375,494)], 1.0)]
    S += [s([(302,496),(336,522),(372,526),(414,492)], 3.0)]    # open bowl
    S += [s([(318,534),(356,544),(396,530)], 2.0)]              # lower lip
    # laugh folds: from wing, around, deep — age and joy, same mark
    S += [s([(326,436),(298,468),(292,490)], 2.2)]
    S += [s([(384,434),(414,464),(420,486)], 2.2)]
    # her hand at the jaw: two soft curves cupping the cheek, no claws
    S += [s([(272,508),(258,548),(266,590),(288,614)], 2.4)]
    S += [s([(296,540),(288,574),(298,604)], 1.6)]
    # bare shoulder
    S += [s([(360,568),(420,620),(500,660)], 3.0)]
    S = tilt(S, 8.0)
    G = [s([(268,386),(440,388)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h018
def h018_penelope():
    """Penelope Tree, ~70s. Frontal mask — fringe cut LOW over the
    brows, enormous hooded eyes with bags beneath, gaunt cheek, thin
    downturned mouth. The opposite of every young face so far."""
    S = []
    # hair: heavy fringe + long dark falls — one mass
    S += [s([(232,420),(220,290),(248,180),(330,130),(412,134),(468,196),(478,310),(468,424)], 3.6)]
    # fringe edge: LOW, nearly on the eyes, slightly ragged
    S += [s([(258,330),(300,342),(352,346),(404,340),(442,328)], 2.6)]
    S += [s([(312,344),(316,356)], 1.2)]                        # ragged tips
    S += [s([(376,342),(380,354)], 1.2)]
    # long falls past the jaw
    S += [s([(232,420),(228,520),(238,620),(252,690)], 3.0)]
    S += [s([(468,424),(474,524),(464,624),(450,692)], 3.0)]
    # face: long, gaunt — hollow drawn into the contour
    S += [s([(260,360),(254,420),(266,468),(258,506),(276,556),(304,594),(346,612)], 2.8)]
    S += [s([(440,362),(446,422),(434,470),(442,508),(424,558),(396,596),(352,614)], 3.2)]
    # EYES: huge, hooded, bagged — under the fringe
    S += [s([(282,376),(312,368),(340,376)], 2.0)]              # fold
    S += [s([(284,390),(312,380),(340,389)], 2.8)]              # upper lash
    S += [s([(304,383),(314,395),(302,395)], 3.0)]              # large dark iris
    S += [s([(286,402),(312,407),(338,400)], 1.7)]              # lower lid
    S += [s([(290,414),(312,419),(334,412)], 1.2)]              # the bag
    S += [s([(366,375),(396,367),(424,375)], 2.0)]
    S += [s([(368,389),(396,379),(424,388)], 2.8)]
    S += [s([(388,382),(398,394),(386,394)], 3.0)]
    S += [s([(370,401),(396,406),(422,399)], 1.7)]
    S += [s([(374,413),(396,418),(418,411)], 1.2)]
    # nose: long, thin
    S += [s([(354,372),(350,452)], 1.8)]
    S += [s([(334,464),(352,472),(372,463)], 2.0)]
    # mouth: thin, pale, corners DOWN
    S += [s([(316,524),(340,520),(356,523),(372,519),(392,526)], 2.4)]
    S += [s([(316,524),(308,532)], 1.6)]
    S += [s([(392,526),(400,534)], 1.6)]
    S += [s([(326,538),(354,544),(384,537)], 1.6)]
    # black polo neck
    S += [s([(296,614),(286,664),(296,706)], 3.2)]
    S += [s([(406,616),(418,662),(408,704)], 3.2)]
    S += [s([(298,664),(352,676),(406,662)], 2.4)]
    S = tilt(S, -1.0)
    G = [s([(260,384),(440,384)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h019
def h019_john():
    """John Pearson, ~60. Three-quarter left, mid-word — lips parted.
    Salt-and-pepper swept back. One furrow between the brows, squint
    with a single crow tick each side. Weather, not ruin."""
    S = []
    # hair: swept BACK — mass rises off the forehead, flicks rearward
    S += [s([(244,310),(244,212),(300,150),(376,134),(446,162),(472,240),(474,310)], 3.2)]
    S += [s([(296,180),(346,158),(404,156)], 1.8)]              # sweep direction
    S += [s([(282,232),(330,206),(388,200)], 1.5)]
    S += [s([(268,300),(296,256),(344,240),(398,248),(434,284)], 1.9)]  # hairline up off the brow
    # face: angular, weathered; 3/4 left
    S += [s([(254,320),(246,392),(258,454),(278,514),(310,556),(352,576)], 2.8)]
    S += [s([(470,326),(474,398),(460,458),(438,516),(404,560),(358,578)], 3.6)]
    S += [s([(314,544),(340,560),(376,560),(400,546)], 2.2)]
    # brows: drawn DOWN — squint; single furrow tick between them
    S += [s([(274,366),(310,358),(342,366)], 3.0)]
    S += [s([(376,364),(410,354),(440,364)], 3.0)]
    S += [s([(358,352),(356,372)], 1.6)]                        # the furrow
    # squint eyes: narrow, dark iris dash, one crow tick each
    S += [s([(286,392),(314,386),(338,392)], 2.6)]
    S += [s([(306,388),(318,396)], 2.4)]
    S += [s([(290,400),(314,403),(336,397)], 1.4)]
    S += [s([(278,394),(266,392)], 1.2)]
    S += [s([(380,390),(406,384),(430,390)], 2.6)]
    S += [s([(398,386),(410,394)], 2.4)]
    S += [s([(384,398),(406,401),(428,395)], 1.4)]
    S += [s([(436,392),(448,390)], 1.2)]
    # nose: strong, a knuckle in the bridge
    S += [s([(356,372),(358,396),(352,444)], 2.0)]
    S += [s([(330,456),(354,466),(380,455)], 2.4)]
    # mouth: PARTED mid-word — dark gap between lips
    S += [s([(314,508),(342,500),(360,504),(378,499),(402,506)], 2.8)]
    S += [s([(322,516),(356,520),(392,514)], 2.0)]              # the gap
    S += [s([(324,530),(356,538),(390,528)], 2.2)]
    # nasolabial: present, structural
    S += [s([(330,462),(310,496)], 1.7)]
    S += [s([(382,460),(404,494)], 1.7)]
    # neck, shirt + tie + leather collar
    S += [s([(312,578),(306,636)], 2.6)]
    S += [s([(398,578),(406,634)], 2.6)]
    S += [s([(306,640),(336,660),(352,654)], 2.0)]
    S += [s([(406,638),(376,658),(360,654)], 2.0)]
    S += [s([(346,658),(364,660),(360,680),(344,678),(346,658)], 2.0)]   # knot
    S += [s([(354,682),(350,730)], 2.0)]
    S += [s([(256,700),(304,654)], 3.6)]                        # leather collar
    S += [s([(458,694),(410,652)], 3.6)]
    S = tilt(S, -2.5)
    G = [s([(254,390),(470,392)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h020
def h020_tyson():
    """Tyson Beckford, ~55. Shaved head, strong turn RIGHT — the skull
    carries everything: dome, occipital bulge, brow step, cheekbone.
    Full lips in near-profile, heavy jaw, bow tie. No hairline to hide
    behind; if the cranium is wrong, everything is wrong."""
    S = []
    # the SKULL: dome → occipital bulge → nape (facing right = back on our left)
    S += [s([(218,392),(212,300),(244,206),(322,150),(404,142),(458,184)], 3.6)]
    S += [s([(218,392),(228,448),(248,492)], 3.0)]              # nape into neck
    # face profile-ish right: brow step → nose → lips → chin
    S += [s([(458,184),(474,238),(470,290)], 3.0)]              # forehead slope
    S += [s([(470,290),(486,308),(482,322)], 2.8)]              # brow step
    S += [s([(482,322),(508,366),(504,380)], 2.6)]              # nose PROJECTS
    S += [s([(504,380),(486,390),(478,394)], 2.0)]
    S += [s([(484,404),(504,412)], 2.6)]                        # full upper lip
    S += [s([(482,424),(500,431)], 2.8)]                        # full lower lip
    S += [s([(478,442),(488,464),(472,498)], 2.8)]              # strong chin
    S += [s([(472,498),(420,534),(348,554)], 3.4)]              # heavy jaw home
    # the visible eye: HIGH, tucked under the brow step
    S += [s([(428,314),(456,306),(476,314)], 2.8)]              # brow
    S += [s([(436,332),(458,326),(474,332)], 2.4)]              # lid
    S += [s([(450,328),(460,336)], 2.2)]                        # iris edge
    S += [s([(440,340),(458,344),(472,338)], 1.3)]
    # cheekbone: one committed arc from under the eye toward the jaw
    S += [s([(424,352),(450,390),(448,420)], 1.7)]
    # ear: mid-skull, solid
    S += [s([(326,326),(356,314),(372,348),(360,394),(330,400)], 2.6)]
    S += [s([(340,340),(354,362),(344,382)], 1.4)]
    # nostril
    S += [s([(472,386),(480,393)], 1.6)]
    # neck: thick column; trapezius
    S += [s([(348,556),(344,620)], 3.0)]
    S += [s([(248,492),(282,560),(296,612)], 3.0)]
    # tux: wing collar, bow tie, lapels
    S += [s([(300,624),(338,644),(372,636)], 2.2)]
    S += [s([(340,632),(310,652),(308,676),(338,668),(340,632)], 2.6)]   # bow L
    S += [s([(340,632),(372,648),(374,672),(344,664),(340,632)], 2.6)]   # bow R
    S += [s([(232,700),(290,640)], 3.8)]
    S += [s([(452,690),(386,640)], 3.8)]
    S = tilt(S, -2.0)
    G = [s([(218,340),(484,340)], 1.0)]
    return S, G


HEADS = [
    ("h011", h011_carmen),
    ("h012", h012_iman),
    ("h013", h013_isabella),
    ("h014", h014_lauren),
    ("h015", h015_nadja),
    ("h016", h016_pat),
    ("h017", h017_paulina),
    ("h018", h018_penelope),
    ("h019", h019_john),
    ("h020", h020_tyson),
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
