"""
HUMAN STUDIES VOL. 1 — Assignment 1: One Hundred Heads.
Batch 01. Observed June 11, 2026 — models.com trending/top50, Jordan's IG.
Reconstructed from observation, never traced. Line is the carrier.
Each head: its own skull, its own placements. No default face.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def s(ctrl, w=3.0, **kw):
    d = dict(ctrl=ctrl, w=w)
    d.update(kw)
    return d


def tilt(strokes, deg, cx=350, cy=400):
    """Roll the whole head. Nobody holds their skull plumb."""
    import math
    a = math.radians(deg)
    co, si = math.cos(a), math.sin(a)
    out = []
    for st in strokes:
        st = dict(st)
        st["ctrl"] = [(cx + (x - cx) * co - (y - cy) * si,
                       cy + (x - cx) * si + (y - cy) * co) for x, y in st["ctrl"]]
        out.append(st)
    return out


# ---------------------------------------------------------------- h001
def h001_gisele():
    """W cover. Mid-40s. Chin dropped, eyes up — stern authority.
    Long oval but WIDE through the cheekbones, firm squarish jaw with a
    real corner, flat low brows, hair scraped back, high dark collar.
    Eyes at the vertical midpoint of the whole head. Age in planes."""
    S = []
    # cranium: a real sphere — wide. Top of head y=130, chin y=640.
    S += [s([(218,300),(228,200),(290,138),(360,124),(430,142),(482,206),(488,300)], 3.2)]
    # HAIRLINE — without this arc the head reads bald. High forehead.
    S += [s([(248,318),(290,276),(352,262),(414,278),(458,322)], 2.4)]
    # scraped-back hair: sweeps INSIDE the hair zone, hairline → crown
    S += [s([(300,272),(282,210),(290,158)], 1.6)]
    S += [s([(352,262),(350,196),(352,140)], 1.6)]
    S += [s([(406,274),(422,212),(414,158)], 1.6)]
    # face sides: cheekbone out, then a near-vertical drop to a real
    # JAW CORNER, then in to the chin shelf — no 45° taper
    S += [s([(222,310),(218,372),(228,440),(240,516),(258,576),(296,616),(340,634)], 3.4)]
    S += [s([(486,312),(490,374),(480,442),(466,518),(446,578),(406,618),(364,634)], 4.0)]
    # chin shelf — firm, wide
    S += [s([(296,616),(322,634),(354,636),(384,628),(406,616)], 2.2)]
    # brows: flat, low; her left (our right) a hair higher
    S += [s([(262,378),(302,372),(340,375)], 2.6)]
    S += [s([(372,373),(412,367),(450,373)], 2.6)]
    # eyes UP under heavy lids (eye line y≈400 ≈ head midpoint)
    S += [s([(272,406),(300,397),(332,404)], 2.4)]
    S += [s([(378,402),(408,395),(440,402)], 2.4)]
    S += [s([(296,400),(305,412),(294,412)], 2.8)]   # iris high, tucked under lid
    S += [s([(402,398),(411,410),(400,410)], 2.8)]
    S += [s([(278,418),(302,422),(328,417)], 1.4)]
    S += [s([(384,416),(410,420),(434,415)], 1.4)]
    # nose: straight; tilt-down hides the base
    S += [s([(358,382),(354,438),(348,482),(336,502)], 2.2)]
    S += [s([(336,502),(356,512),(380,504)], 2.4)]
    # mouth: full, red, corners level-to-down; wide enough for the jaw
    S += [s([(306,552),(338,544),(357,548),(376,543),(408,550)], 3.0)]
    S += [s([(314,544),(342,532),(357,536),(372,531),(400,543)], 2.4)]
    S += [s([(318,560),(356,576),(394,559)], 2.6)]
    # ear, our right — rides high with the tilt
    S += [s([(488,372),(504,392),(498,430),(480,442)], 2.0)]
    # high collar — wide, running off toward the shoulders
    S += [s([(250,648),(290,690),(358,706),(420,688),(462,642)], 3.6)]
    S += [s([(236,700),(282,756),(330,790)], 3.0)]
    S += [s([(474,694),(432,752),(388,788)], 3.0)]
    S = tilt(S, -4.5)
    G = [s([(222,400),(486,400)], 1.1)]   # eye-line search mark
    return S, G


# ---------------------------------------------------------------- h002
def h002_rihanna():
    """72 Magazine. Three-quarter left, gaze cut further left — head and
    eyes split. Hair mass twice the skull. High thin arches, heavy lids,
    short nose, dark full mouth, long neck, bare sloping shoulders."""
    S = []
    # the hair: enormous soft cloud — few big wandering arcs, broken edges
    S += [s([(180,330),(150,240),(196,150),(280,96),(372,82)], 3.2)]
    S += [s([(372,82),(458,96),(528,150),(556,242),(540,330)], 3.2)]
    S += [s([(540,330),(560,396),(532,452)], 2.6)]
    S += [s([(180,330),(160,400),(190,456)], 2.6)]
    # inner hair motion — a few strands only
    S += [s([(250,140),(232,210),(244,280)], 1.5)]
    S += [s([(470,150),(492,220),(478,292)], 1.5)]
    # hairline: high ROUNDED arc, 3/4 — face center-left of hair mass
    S += [s([(258,258),(284,216),(330,200),(380,212),(406,242)], 2.2)]
    # face contour 3/4 left: near (our-left) side short, far side full.
    # Her face is WIDE and soft through the cheeks; chin small but round.
    S += [s([(244,242),(232,312),(238,372),(256,428),(288,478),(330,506)], 3.2)]
    S += [s([(412,214),(432,292),(428,368),(408,434),(370,490),(330,506)], 3.0)]
    # round chin shelf — soft, no point
    S += [s([(300,492),(326,504),(354,496)], 2.0)]
    # brows: thin, arched HIGH (70s register), far brow shorter
    S += [s([(272,302),(296,286),(322,290)], 2.0)]
    S += [s([(352,288),(378,282),(398,292)], 2.0)]
    # eyes glancing left: LARGE, irises parked hard left, lids heavy
    S += [s([(270,326),(298,314),(326,324)], 2.6)]
    S += [s([(274,328),(284,344),(298,340)], 3.2)]   # iris far left of opening
    S += [s([(274,342),(300,348),(324,338)], 1.4)]
    S += [s([(348,322),(374,310),(398,322)], 2.6)]
    S += [s([(352,324),(362,340),(374,336)], 3.2)]
    S += [s([(352,340),(376,346),(394,336)], 1.4)]
    # nose: short, soft rounded tip, 3/4
    S += [s([(330,310),(324,360),(314,392)], 2.0)]
    S += [s([(314,392),(330,404),(352,398)], 2.4)]
    # mouth: full, dark, defined bow; small for the face
    S += [s([(304,446),(326,440),(338,444),(352,439),(368,446)], 3.0)]
    S += [s([(310,440),(328,428),(338,432),(350,427),(362,440)], 2.6)]   # bow
    S += [s([(312,452),(338,464),(362,452)], 2.8)]
    # far ear + long earring
    S += [s([(414,330),(428,344),(424,376)], 1.8)]
    S += [s([(424,378),(428,420),(420,448)], 1.5)]
    # neck — long but a COLUMN, not a stem; shoulders slope away early
    S += [s([(298,508),(294,550),(286,586)], 2.8)]
    S += [s([(360,504),(368,548),(378,584)], 2.8)]
    S += [s([(286,586),(216,636),(120,680)], 3.2)]
    S += [s([(378,584),(452,632),(560,676)], 3.2)]
    S = tilt(S, 3.5)
    G = [s([(244,242),(412,214)], 1.1)]
    return S, G


# ---------------------------------------------------------------- h003
def h003_bai():
    """Celine. Narrow long face under loose black curls, chin a touch
    lifted, lids low — looking down past the nose. High cheekbones,
    flat planes, faint straight brows, small mouth. Red scarf bulk."""
    S = []
    # curls: LOOSE soft lobes drooping over the forehead — rounded scallops
    # along an IRREGULAR hairline, falling under their own weight
    S += [s([(240,260),(222,190),(258,130),(330,102),(404,98),(466,130),(492,196),(482,262)], 3.4)]
    # hairline: two long lazy scallops only — deep bellies, no zigzag
    S += [s([(258,252),(300,296),(356,262)], 2.2)]
    S += [s([(356,262),(412,294),(452,250)], 2.2)]
    # interior curl motion: two round hooks, falling
    S += [s([(300,150),(284,184),(308,206),(296,228)], 1.5)]
    S += [s([(412,140),(434,172),(414,196)], 1.5)]
    # face: narrow for a man but with real cheek width and JAW CORNERS;
    # chin slightly lifted so the underside shows
    S += [s([(258,280),(250,350),(258,416),(276,480),(308,532),(346,556)], 3.2)]
    S += [s([(474,290),(480,358),(470,422),(448,484),(408,536),(346,556)], 3.0)]
    # flat chin (lifted: underside visible as its own line)
    S += [s([(308,532),(330,548),(366,548),(396,534)], 2.0)]
    # brows: faint, straight, low
    S += [s([(288,330),(322,326),(352,329)], 1.6)]
    S += [s([(386,328),(418,324),(448,329)], 1.6)]
    # narrow eyes: single lid line each, lids low (looking down past us)
    S += [s([(294,360),(324,356),(352,360)], 2.6)]
    S += [s([(386,358),(416,354),(444,359)], 2.6)]
    S += [s([(302,366),(326,370),(348,366)], 1.2)]
    S += [s([(392,365),(416,368),(440,364)], 1.2)]
    # nose: long, low bridge; chin-lift shows a little base
    S += [s([(366,338),(364,408),(360,452)], 2.0)]
    S += [s([(342,460),(362,470),(386,462)], 2.2)]
    S += [s([(338,452),(344,462)], 1.6)]
    # mouth: small, closed, level
    S += [s([(326,500),(350,496),(364,498),(378,495),(398,500)], 2.6)]
    S += [s([(338,510),(364,516),(390,509)], 1.8)]
    # red scarf: loose wrapped bulk — open, asymmetric, swallowing the neck
    S += [s([(252,572),(232,628),(258,684),(330,712)], 3.4)]
    S += [s([(478,566),(498,622),(470,678),(396,706)], 3.2)]
    S += [s([(282,590),(330,624),(396,616),(444,584)], 2.6)]   # wrap fold
    S += [s([(310,650),(352,668),(404,654)], 2.0)]             # second fold
    S = tilt(S, -2.0)
    G = [s([(258,330),(474,336)], 1.1)]
    return S, G


# ---------------------------------------------------------------- h004
def h004_versace():
    """Versace campaign. Very young. Chin dropped further than h001,
    eyes up — but unguarded, not stern. Brows nearly invisible. Long
    waves frame the face and keep falling past the crop."""
    S = []
    # hair: center part, two heavy falls framing the face
    S += [s([(350,128),(282,148),(232,210),(208,310),(204,430),(216,560),(238,668)], 3.4)]
    S += [s([(350,128),(414,150),(458,214),(478,316),(474,444),(458,572),(440,672)], 3.0)]
    # part + inner wave motion
    S += [s([(350,132),(348,160),(344,184)], 1.8)]
    S += [s([(252,260),(238,360),(250,460),(240,560)], 1.5)]
    S += [s([(444,270),(458,372),(444,470),(452,566)], 1.5)]
    # hairline where the falls open: high forehead, soft widow's point
    S += [s([(284,302),(322,272),(352,266),(384,274),(418,308)], 2.0)]
    # face: young, soft; cheeks full, chin narrow but round
    S += [s([(268,340),(262,418),(274,496),(298,556),(332,592)], 2.8)]
    S += [s([(432,344),(440,422),(426,500),(400,560),(364,594)], 3.4)]
    S += [s([(316,584),(340,596),(360,594),(378,584)], 1.8)]   # small round chin
    # brows: barely there
    S += [s([(290,362),(318,356),(344,360)], 1.0)]
    S += [s([(376,359),(402,354),(428,361)], 1.0)]
    # eyes UP, large openings, pale irises tucked under lids
    S += [s([(292,394),(318,384),(344,392)], 2.6)]
    S += [s([(376,391),(402,382),(426,391)], 2.6)]
    S += [s([(312,388),(321,400),(310,400)], 2.2)]
    S += [s([(396,386),(405,398),(394,398)], 2.2)]
    S += [s([(296,406),(320,411),(342,404)], 1.3)]
    S += [s([(380,404),(404,409),(424,403)], 1.3)]
    # nose: small, slightly upturned — base tips up
    S += [s([(354,372),(350,428),(346,456)], 1.8)]
    S += [s([(332,464),(350,470),(370,462)], 2.0)]
    # mouth: parted a breath, soft
    S += [s([(314,516),(340,510),(356,513),(372,509),(396,516)], 2.4)]
    S += [s([(322,508),(344,500),(356,504),(370,499),(388,507)], 1.8)]
    S += [s([(322,530),(354,540),(386,528)], 2.0)]
    # slim neck, strap hints
    S += [s([(312,594),(308,650),(304,692)], 2.4)]
    S += [s([(380,594),(386,648),(392,690)], 2.4)]
    S += [s([(268,700),(306,718),(352,722)], 2.0)]
    S += [s([(352,722),(398,716),(434,698)], 2.0)]
    S = tilt(S, -3.0)
    G = [s([(268,392),(432,392)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h005
def h005_braien():
    """ICON cover. Head tipped back and rolled, resting on a wall —
    neck released, expression slack. Heavy brow ridge, deep-set eyes,
    short nose with nostrils showing, big chin. Light rakes one side."""
    S = []
    # skull + short fair hair flopping diagonally across the forehead
    S += [s([(252,288),(262,200),(326,152),(396,148),(452,190),(470,272)], 3.0)]
    S += [s([(262,238),(330,200),(404,196),(444,220)], 1.8)]   # fringe sweep
    S += [s([(286,262),(348,232),(414,236)], 1.6)]             # fringe underside
    # face: angular; tipped back so chin is LARGE, forehead short
    S += [s([(254,300),(248,372),(258,440),(276,502),(308,548),(348,566)], 2.6)]
    S += [s([(468,298),(474,372),(462,444),(440,506),(404,550),(352,566)], 4.2)]
    S += [s([(304,540),(330,560),(366,560),(396,542)], 2.6)]   # big chin shelf
    # brow ridge HEAVY — the architecture of the face
    S += [s([(274,344),(312,332),(348,340)], 3.6)]
    S += [s([(380,338),(418,328),(452,340)], 3.6)]
    # eyes: slack, half-closed slits under the ridge
    S += [s([(288,366),(318,360),(342,366)], 2.2)]
    S += [s([(384,364),(412,358),(438,365)], 2.2)]
    S += [s([(310,364),(320,370)], 2.4)]
    S += [s([(402,362),(412,368)], 2.4)]
    # nose: SHORT (tipped back), nostrils visible
    S += [s([(360,348),(356,398)], 2.0)]
    S += [s([(338,410),(358,420),(382,409)], 2.4)]
    S += [s([(344,404),(350,412)], 1.6)]
    S += [s([(372,402),(366,410)], 1.6)]
    # mouth: slack, barely open
    S += [s([(322,464),(350,458),(364,461),(380,457),(400,464)], 2.6)]
    S += [s([(330,478),(360,486),(392,477)], 1.6)]
    # neck off-axis — head rests, neck leaves at an angle
    S += [s([(308,564),(290,624),(280,668)], 2.8)]
    S += [s([(396,560),(420,616),(436,660)], 2.8)]
    # trench collar, heavy diagonals
    S += [s([(232,700),(296,664),(348,676)], 3.8)]
    S += [s([(484,688),(420,652),(366,672)], 3.8)]
    S = tilt(S, 9.0)
    G = [s([(254,340),(468,336)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h006
def h006_douta():
    """Balenciaga. Young Black man, head level, guarded stillness.
    One brow a hair up. Tight crop, full lips, smooth full cheeks,
    long neck, white collar and tie under a heavy coat."""
    S = []
    # round skull, crop drawn as doubled contour
    S += [s([(232,292),(246,192),(312,142),(382,136),(446,178),(478,264),(482,308)], 3.2)]
    S += [s([(262,298),(308,270),(366,264),(422,286),(454,314)], 2.0)]   # hairline
    # face: smooth full cheeks, soft strong jaw
    S += [s([(240,318),(236,390),(248,460),(268,522),(300,574),(344,596)], 2.8)]
    S += [s([(474,324),(478,396),(466,466),(444,526),(408,578),(360,598)], 3.6)]
    S += [s([(304,578),(330,594),(372,594),(404,578)], 2.4)]   # round chin shelf
    # brows: left level, right fractionally raised
    S += [s([(272,360),(304,352),(336,358)], 2.8)]
    S += [s([(372,352),(404,344),(436,352)], 2.8)]
    # eyes: calm, at us but past us — irises a touch off-center
    S += [s([(282,392),(308,384),(334,392)], 2.4)]
    S += [s([(376,390),(402,382),(428,390)], 2.4)]
    S += [s([(302,388),(311,399),(300,399)], 2.6)]
    S += [s([(398,386),(407,397),(396,397)], 2.6)]
    S += [s([(286,404),(310,408),(332,402)], 1.3)]
    S += [s([(380,402),(404,406),(426,400)], 1.3)]
    # nose: soft bridge, broader base, defined wings
    S += [s([(358,366),(354,442)], 1.8)]
    S += [s([(326,462),(354,474),(384,461)], 2.6)]
    S += [s([(320,450),(330,464)], 1.8)]
    S += [s([(390,448),(380,462)], 1.8)]
    # mouth: FULL — both lips carry volume; held closed
    S += [s([(310,520),(338,512),(356,516),(374,511),(404,519)], 3.0)]
    S += [s([(318,508),(340,496),(356,502),(372,495),(396,506)], 2.6)]
    S += [s([(318,534),(356,550),(394,532)], 3.2)]
    # long neck, white collar, slim tie, big coat
    S += [s([(310,598),(306,668)], 2.6)]
    S += [s([(398,596),(404,664)], 2.6)]
    S += [s([(282,682),(322,698),(344,690)], 2.0)]   # collar wings
    S += [s([(428,678),(386,696),(364,690)], 2.0)]
    S += [s([(342,692),(362,694),(360,716),(340,714),(342,692)], 2.2)]  # knot
    S += [s([(350,718),(346,778)], 2.2)]
    S += [s([(300,668),(206,700),(126,728)], 4.0)]   # coat shoulders, heavy
    S += [s([(406,664),(498,694),(576,720)], 4.0)]
    S += [s([(238,712),(296,690)], 2.8)]             # lapel
    S += [s([(464,706),(408,688)], 2.8)]
    S = tilt(S, -1.5)
    G = [s([(240,390),(474,392)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h007
def h007_elias():
    """Looking back over the shoulder — head past three-quarter,
    nearly profile. Pillbox hat low on the forehead, jug ear, hooded
    eye, downturned mouth, soft teen jaw. The neck does the work."""
    S = []
    # hat: flat top, band cutting low across the forehead
    S += [s([(266,242),(322,196),(412,186),(466,212),(458,258)], 3.4)]
    S += [s([(272,278),(360,252),(452,258)], 3.0)]   # band line
    # profile line: forehead → brow notch → short up-nose → lips → chin
    S += [s([(284,278),(272,322),(276,348)], 2.6)]
    S += [s([(276,348),(258,394),(252,404)], 2.8)]   # nose, slightly up
    S += [s([(252,404),(264,414),(272,420)], 2.0)]   # under-nose
    S += [s([(270,434),(282,440),(290,452)], 2.6)]   # upper lip, corner down
    S += [s([(278,456),(292,462)], 2.0)]             # lower lip, small
    S += [s([(286,470),(300,492),(326,520),(366,540)], 2.8)]  # soft chin → jaw
    # the visible eye: hooded, heavy lid
    S += [s([(292,330),(326,322),(348,328)], 2.6)]   # brow
    S += [s([(300,352),(322,346),(340,352)], 2.4)]   # lid
    S += [s([(312,350),(322,358)], 2.4)]             # iris dash
    S += [s([(304,362),(324,366),(338,360)], 1.2)]
    # jug ear — far side, proud of the head
    S += [s([(424,356),(452,342),(468,376),(456,420),(428,428)], 2.8)]
    S += [s([(436,372),(448,392),(440,408)], 1.4)]   # inner ear
    # skull back under hat, nape
    S += [s([(458,258),(472,300),(468,348)], 2.4)]
    S += [s([(456,424),(462,470),(452,510)], 2.4)]   # nape into collar
    # neck twisted: front line short, back line long
    S += [s([(366,540),(380,576),(390,604)], 2.6)]
    S += [s([(452,510),(440,556),(430,592)], 2.6)]
    # shoulder bulk in front — he looks back over it; heavy, close
    S += [s([(200,648),(310,606),(430,610),(548,656)], 4.4)]
    S += [s([(330,610),(400,592),(452,600)], 2.6)]   # collar edge
    S = tilt(S, -3.0)
    G = [s([(276,348),(420,360)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h008
def h008_jordan():
    """Jordan — restaurant, candle, birthday. Mid-30s. Hair brushed up
    and over with temple recession, short beard at the jaw, brows a
    touch raised, asymmetric half-smile: between pleased and caught."""
    S = []
    # skull + brushed-up hair (volume rides above the front)
    S += [s([(240,300),(252,202),(318,152),(390,148),(450,188),(472,274),(476,316)], 3.0)]
    S += [s([(290,180),(330,148),(382,140)], 2.2)]   # quiff lift
    # hairline: temples recede gently — shallow dips, not a deep W
    S += [s([(264,300),(304,262),(352,272),(400,260),(446,302)], 2.0)]
    S += [s([(322,238),(352,204),(392,184)], 1.5)]   # brush-over, inside hair
    # face: medium-long, beard firms the jaw
    S += [s([(244,316),(240,388),(252,458),(272,520),(306,566),(350,586)], 2.8)]
    S += [s([(472,322),(476,394),(464,462),(442,524),(406,570),(356,588)], 3.6)]
    S += [s([(310,570),(334,586),(372,586),(400,572)], 2.6)]   # chin in beard
    # brows: raised a touch — gentle arcs. NO forehead crease: in economy
    # line every interior mark is ten years.
    S += [s([(282,358),(314,344),(344,354)], 2.6)]
    S += [s([(380,352),(412,342),(442,356)], 2.6)]
    # eyes: warm, lower lids pushed up slightly by the almost-smile
    S += [s([(290,398),(314,388),(338,396)], 2.4)]
    S += [s([(384,394),(408,384),(432,394)], 2.4)]
    S += [s([(306,392),(315,403),(304,403)], 2.6)]
    S += [s([(400,388),(409,399),(398,399)], 2.6)]
    S += [s([(294,410),(316,415),(336,408)], 1.7)]
    S += [s([(388,406),(410,411),(430,404)], 1.7)]
    # nose
    S += [s([(358,370),(354,434)], 1.8)]
    S += [s([(336,448),(356,458),(378,447)], 2.2)]
    S += [s([(330,440),(338,452)], 1.5)]
    # mouth: half-smile, right corner higher; crease on that side only
    S += [s([(314,504),(342,498),(360,502),(380,492),(404,490)], 2.8)]
    S += [s([(322,496),(346,488),(362,492),(382,486),(398,484)], 1.8)]
    S += [s([(322,518),(356,528),(392,512)], 2.2)]
    S += [s([(410,474),(420,502)], 1.3)]             # smile crease, one side
    # beard: carried by a slightly heavier jaw line alone — no dashes
    # open floral collar — collar only, the print stays home
    S += [s([(300,592),(278,648),(296,702)], 2.6)]
    S += [s([(402,592),(430,646),(414,700)], 2.6)]
    S += [s([(330,640),(352,668),(374,638)], 1.8)]   # open V
    S += [s([(250,662),(168,702)], 3.2)]
    S += [s([(462,658),(542,696)], 3.2)]
    S = tilt(S, -2.5)
    G = [s([(244,394),(472,396)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h009
def h009_greg():
    """Greg — street selfie, square dark glasses, pressed-closed broad
    smile with deep-carved folds, square jaw, cropped sides. The smile
    is structural: it moves the whole lower face."""
    S = []
    # skull, crop: tight sides, up-flicks along the top
    S += [s([(238,300),(250,206),(312,158),(382,152),(444,190),(468,272),(472,312)], 3.2)]
    S += [s([(302,168),(318,136)], 1.8)]
    S += [s([(322,162),(334,128)], 1.8)]
    S += [s([(348,156),(360,124)], 1.8)]
    S += [s([(372,154),(382,126)], 1.8)]
    S += [s([(392,158),(406,132)], 1.8)]
    # crop hairline — without it the head reads bald
    S += [s([(262,302),(296,264),(352,252),(408,266),(444,304)], 2.2)]
    # glasses: heavy square frames + bridge + arms
    S += [s([(268,352),(306,346),(346,352),(350,380),(342,404),(304,408),(272,402),(266,376),(268,352)], 4.2)]
    S += [s([(376,350),(414,344),(452,350),(456,376),(448,400),(412,406),(380,402),(374,378),(376,350)], 4.2)]
    S += [s([(350,366),(376,364)], 3.2)]
    S += [s([(266,362),(244,362)], 2.4)]
    S += [s([(452,360),(472,358)], 2.4)]
    # face: tanned planes, SQUARE jaw — near-horizontal chin
    S += [s([(242,316),(238,390),(250,452),(268,512),(302,558),(348,580)], 3.0)]
    S += [s([(470,318),(474,392),(462,454),(442,514),(408,560),(356,582)], 3.8)]
    S += [s([(302,562),(332,576),(376,576),(406,562)], 2.8)]
    # nose under the frames
    S += [s([(358,408),(354,442)], 1.8)]
    S += [s([(336,452),(356,462),(378,451)], 2.2)]
    # the smile: wide, pressed closed, curving hard up — two lines only
    S += [s([(296,508),(330,520),(358,524),(386,518),(420,504)], 3.4)]
    S += [s([(314,530),(356,540),(398,527)], 2.4)]
    # nasolabial: short, light — present, not carved into age
    S += [s([(330,452),(312,486)], 1.6)]
    S += [s([(386,450),(406,484)], 1.6)]
    # ears, thick neck, tee collar, pack straps
    S += [s([(236,360),(222,376),(228,412),(244,420)], 2.2)]
    S += [s([(474,358),(488,374),(482,410),(466,418)], 2.2)]
    S += [s([(306,582),(300,648)], 2.8)]
    S += [s([(402,582),(410,646)], 2.8)]
    S += [s([(300,650),(356,672),(410,646)], 3.0)]
    S += [s([(294,656),(286,712)], 3.4)]
    S += [s([(316,662),(310,716)], 3.4)]
    S += [s([(398,654),(406,710)], 3.4)]
    S += [s([(420,650),(428,704)], 3.4)]
    S = tilt(S, 2.0)
    G = [s([(242,380),(470,378)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h010
def h010_amelia():
    """Perfect cover. Mask-frontal by intention — her power is the
    symmetry. Thick low brows almost meeting, lined deep-set eyes with
    pale irises (outlined, not filled), carved cheekbone, matte mouth."""
    S = []
    # skull, hair flat to it, center part, long dark falls behind
    S += [s([(244,290),(256,196),(318,150),(384,146),(440,184),(462,266),(466,300)], 3.0)]
    S += [s([(352,148),(350,196)], 1.8)]
    S += [s([(266,288),(310,262),(352,258),(396,260),(440,290)], 2.0)]
    S += [s([(240,300),(228,400),(236,520),(252,604)], 3.0)]
    S += [s([(466,302),(478,402),(470,522),(456,604)], 3.0)]
    # face: cheekbone bump then hollow, lives in the contour itself
    S += [s([(250,308),(242,370),(262,422),(254,468),(272,522),(304,562),(346,580)], 3.0)]
    S += [s([(460,310),(468,372),(448,424),(456,468),(438,522),(406,562),(352,582)], 3.4)]
    S += [s([(316,570),(340,582),(366,582),(390,572)], 2.0)]
    # brows: THICK, low, nearly meeting
    S += [s([(276,352),(312,348),(344,352)], 4.6)]
    S += [s([(362,352),(396,346),(432,352)], 4.6)]
    # eyes: liner doubled lids, IRISES OUTLINED pale
    S += [s([(286,376),(310,368),(334,376)], 2.8)]
    S += [s([(288,381),(310,374),(332,381)], 1.3)]
    S += [s([(306,371),(314,379),(307,387),(299,380),(306,371)], 1.4)]
    S += [s([(374,374),(398,366),(422,374)], 2.8)]
    S += [s([(376,379),(398,372),(420,379)], 1.3)]
    S += [s([(394,369),(402,377),(395,385),(387,378),(394,369)], 1.4)]
    S += [s([(290,390),(312,395),(332,388)], 1.9)]
    S += [s([(378,388),(400,393),(420,386)], 1.9)]
    # nose: narrow, straight
    S += [s([(356,360),(352,430)], 1.8)]
    S += [s([(344,442),(356,450),(370,441)], 2.0)]
    # mouth: matte, defined, corners straight
    S += [s([(314,500),(340,494),(356,498),(372,493),(396,500)], 3.0)]
    S += [s([(320,492),(342,482),(356,487),(370,481),(390,491)], 2.4)]
    S += [s([(322,512),(354,522),(388,510)], 2.6)]
    # neck, square shoulders
    S += [s([(314,582),(310,650)], 2.6)]
    S += [s([(392,582),(396,648)], 2.6)]
    S += [s([(310,652),(222,690)], 3.2)]
    S += [s([(396,650),(486,688)], 3.2)]
    S = tilt(S, -1.0)
    G = [s([(250,374),(460,374)], 1.0)]
    return S, G


HEADS = [
    ("h001", h001_gisele),
    ("h002", h002_rihanna),
    ("h003", h003_bai),
    ("h004", h004_versace),
    ("h005", h005_braien),
    ("h006", h006_douta),
    ("h007", h007_elias),
    ("h008", h008_jordan),
    ("h009", h009_greg),
    ("h010", h010_amelia),
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
