"""
HUMAN STUDIES VOL. 1 — Assignment 1: One Hundred Heads.
Batch 04 (h032–h041). Observed June 11, 2026 — Personal Photos archive
(Jennifer/Jim/Jordan/Jensen folders) + Commons photographs (three bowed
readers). The session question: what survives when photographs disagree?
New constructions this batch: the UPWARD head (eyes above midline, jaw
underside visible, ears low) and the BOWED head (crown dominant, eyes
below midline, ears high) — designed as their own armatures, not bent
frontals. Lesson 12 honored.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import stroke, render  # noqa: E402
from heads_batch01 import s, tilt      # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


# ---------------------------------------------------------------- h032
def h032_jennifer_redraw():
    """Jennifer — the redraw. What makes Jennifer Jennifer when the
    hair changes: smile crescents, cheek apples, upper teeth, slim
    pointed chin. So: hair PULLED BACK with temple wisps (the bare-
    faced selfie), and the face carries everything."""
    S = []
    # skull with hair scraped back — contour near the bone, small bun
    S += [s([(240,296),(250,206),(314,158),(382,154),(444,192),(466,270),(470,310)], 3.2)]
    S += [s([(444,206),(478,196),(486,228),(462,242)], 2.2)]      # the bun, low
    # hairline high + soft temple wisps (two only)
    S += [s([(266,298),(302,260),(352,250),(404,264),(440,300)], 2.0)]
    S += [s([(272,306),(258,344),(264,374)], 1.3)]
    S += [s([(436,302),(452,340),(446,372)], 1.3)]
    # face: high cheekbones, cheeks lifted, slim chin — slightly pointed
    S += [s([(246,316),(240,384),(252,446),(274,506),(306,550),(348,570)], 2.8)]
    S += [s([(464,320),(468,390),(456,450),(434,510),(402,554),(354,572)], 3.3)]
    S += [s([(316,560),(338,572),(366,572),(388,560)], 2.0)]      # small chin
    # brows: soft, raised by the permanent smile
    S += [s([(276,356),(308,344),(340,352)], 2.0)]
    S += [s([(374,350),(406,342),(436,352)], 2.0)]
    # THE CRESCENTS: her eyes nearly close upward — two arcs each,
    # tiny iris glint surviving between them
    S += [s([(284,388),(312,378),(338,386)], 2.7)]
    S += [s([(288,395),(314,389),(336,393)], 1.6)]
    S += [s([(306,383),(313,390)], 1.7)]
    S += [s([(376,385),(404,375),(428,384)], 2.7)]
    S += [s([(380,392),(406,386),(424,391)], 1.6)]
    S += [s([(396,380),(403,387)], 1.7)]
    # one crow ray each — light
    S += [s([(278,386),(266,382)], 1.1)]
    S += [s([(432,382),(444,378)], 1.1)]
    # nose: slim, smile-widened base
    S += [s([(354,360),(350,424)], 1.7)]
    S += [s([(330,436),(352,446),(376,435)], 2.1)]
    # the smile: wide, upper teeth, CHEEK APPLES pushing it up
    S += [s([(296,486),(328,475),(356,479),(384,473),(416,483)], 2.9)]
    S += [s([(308,494),(340,492),(372,491),(404,489)], 1.5)]      # teeth
    S += [s([(306,502),(338,516),(372,517),(408,498)], 2.7)]
    S += [s([(318,524),(354,533),(390,521)], 1.9)]
    S += [s([(324,440),(300,470),(294,488)], 1.8)]                # smile folds
    S += [s([(380,438),(406,466),(412,484)], 1.8)]
    S += [s([(278,444),(296,462)], 1.2)]                          # cheek apples
    S += [s([(432,440),(414,458)], 1.2)]
    # beaded earrings — the selfie's one ornament
    S += [s([(244,378),(240,408)], 1.6)]
    S += [s([(468,374),(474,404)], 1.6)]
    # neck, fleece collar soft and high
    S += [s([(314,572),(308,624)], 2.4)]
    S += [s([(390,572),(396,622)], 2.4)]
    S += [s([(250,672),(312,634),(356,628)], 3.0)]
    S += [s([(452,668),(400,632),(360,628)], 3.0)]
    S = tilt(S, 6.0)
    G = [s([(246,386),(464,386)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h033
def h033_jim_multi():
    """Jim without the beret — thirty years of photographs agree on:
    the grin, the squint, the jaw. Short neat hair, side-combed,
    silver now. The grin is asymmetric: left corner leads."""
    S = []
    # skull: high forehead, short neat hair close to it
    S += [s([(242,300),(252,212),(314,164),(384,160),(446,196),(468,274),(472,312)], 3.0)]
    S += [s([(268,294),(302,258),(354,248),(406,260),(442,296)], 1.9)]
    S += [s([(300,256),(338,242),(380,242)], 1.3)]                # side-comb
    # face: lean, weathered, jaw still the architecture
    S += [s([(248,316),(242,386),(252,448),(272,508),(304,552),(348,572)], 2.8)]
    S += [s([(470,320),(474,392),(462,452),(440,512),(406,556),(354,574)], 3.4)]
    S += [s([(308,556),(334,570),(370,570),(396,556)], 2.3)]
    # brows: light, lifted
    S += [s([(274,358),(306,348),(338,354)], 2.0)]
    S += [s([(374,353),(406,345),(436,354)], 2.0)]
    # the SQUINT: eyes nearly gone, iris dash surviving
    S += [s([(282,386),(308,378),(334,385)], 2.6)]
    S += [s([(300,382),(309,390)], 1.9)]
    S += [s([(286,394),(310,398),(332,391)], 1.7)]
    S += [s([(378,384),(404,376),(428,383)], 2.6)]
    S += [s([(396,380),(405,388)], 1.9)]
    S += [s([(382,392),(406,396),(426,389)], 1.7)]
    # crow's feet: two rays each — his are deeper than hers
    S += [s([(274,382),(260,376)], 1.3)]
    S += [s([(276,392),(262,394)], 1.3)]
    S += [s([(434,380),(448,374)], 1.3)]
    S += [s([(432,390),(446,392)], 1.3)]
    # nose: straight, weathered tip
    S += [s([(354,358),(350,428)], 1.9)]
    S += [s([(326,442),(350,453),(378,441)], 2.4)]
    # the GRIN: open, asymmetric — our-left corner higher and deeper
    S += [s([(292,486),(326,477),(356,482),(386,478),(418,489)], 2.9)]
    S += [s([(304,495),(338,493),(372,492),(404,492)], 1.6)]      # teeth
    S += [s([(300,504),(334,522),(372,524),(410,506)], 2.9)]
    S += [s([(312,530),(352,540),(392,528)], 2.0)]
    S += [s([(322,444),(294,476),(288,496)], 2.2)]                # deep folds
    S += [s([(382,442),(412,472),(418,492)], 2.0)]
    # lean neck, polo collar
    S += [s([(306,574),(300,630)], 2.6)]
    S += [s([(396,574),(404,628)], 2.6)]
    S += [s([(258,674),(314,640),(356,634)], 2.8)]
    S += [s([(450,670),(400,638),(360,634)], 2.8)]
    S = tilt(S, -3.0)
    G = [s([(248,384),(470,384)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h034
def h034_jordan_synthesis():
    """Jordan — the one who survives all photographs. Not the most
    recent, not the most flattering: the constant. Quiff up-and-back,
    straight low brows, level deep-set pale eyes, strong straight
    nose, composed mouth. Sharpened from h031: chin a touch longer,
    outer eye corners a touch hooded."""
    S = []
    S += [s([(246,300),(256,210),(306,150),(370,138),(442,170),(468,252),(472,310)], 3.0)]
    S += [s([(292,236),(310,182),(354,152),(398,146)], 2.2)]      # quiff sweep
    S += [s([(338,242),(360,194),(406,170)], 1.6)]
    S += [s([(268,302),(302,262),(352,274),(402,260),(446,304)], 2.0)]
    # face: lean, a touch longer through the chin than h031
    S += [s([(256,316),(250,388),(262,452),(280,518),(310,566),(352,586)], 2.8)]
    S += [s([(462,322),(466,394),(454,458),(434,522),(402,570),(356,588)], 3.3)]
    S += [s([(316,572),(338,586),(372,586),(396,572)], 2.3)]
    # brows: straight, level, low
    S += [s([(280,360),(312,354),(342,358)], 2.8)]
    S += [s([(378,357),(410,351),(440,357)], 2.8)]
    # eyes: deep-set, pale (outlined iris), outer corners slightly hooded
    S += [s([(288,378),(312,372),(338,378)], 1.3)]
    S += [s([(286,392),(312,384),(334,390),(340,395)], 2.5)]      # hood at corner
    S += [s([(306,386),(314,394),(307,401),(299,394),(306,386)], 1.3)]
    S += [s([(306,390),(310,394)], 1.7)]
    S += [s([(292,402),(314,406),(336,400)], 1.4)]
    S += [s([(382,376),(406,370),(430,375)], 1.3)]
    S += [s([(378,394),(384,389),(406,382),(432,389)], 2.5)]
    S += [s([(400,384),(408,392),(401,399),(393,392),(400,384)], 1.3)]
    S += [s([(400,388),(404,392)], 1.7)]
    S += [s([(386,400),(408,404),(430,398)], 1.4)]
    # nose: the strong straight one — every photo agrees
    S += [s([(358,366),(354,442)], 2.0)]
    S += [s([(332,454),(354,464),(380,452)], 2.3)]
    S += [s([(326,446),(334,458)], 1.5)]
    S += [s([(386,444),(378,456)], 1.5)]
    # composed mouth, fuller lower lip, corners level
    S += [s([(354,472),(355,486)], 1.2)]
    S += [s([(318,504),(344,498),(360,501),(376,496),(400,503)], 2.7)]
    S += [s([(326,516),(358,524),(390,514)], 2.3)]
    # ears, long neck, tee
    S += [s([(248,366),(234,382),(240,416),(256,424)], 2.0)]
    S += [s([(470,364),(484,380),(478,414),(462,422)], 2.0)]
    S += [s([(314,588),(310,648)], 2.6)]
    S += [s([(394,588),(400,646)], 2.6)]
    S += [s([(306,652),(238,672),(166,686)], 3.2)]
    S += [s([(402,650),(466,668),(540,682)], 3.2)]
    S = tilt(S, -2.0)
    G = [s([(256,388),(462,390)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h035
def h035_jensen():
    """Jensen Hess. Long lean face — longest in the family. Heavy
    dark straight brows, the family's pale eyes, thick dark hair with
    a forward quiff, wide mouth held in a contained half-smile."""
    S = []
    # skull: LONG; thick dark hair, fringe-quiff pushing forward
    S += [s([(252,290),(258,202),(310,152),(376,142),(440,168),(464,244),(468,304)], 3.2)]
    S += [s([(296,210),(330,168),(378,150)], 2.2)]                # forward push
    S += [s([(282,256),(316,222),(360,206)], 1.6)]
    S += [s([(272,294),(304,258),(352,248),(402,262),(440,298)], 2.0)]
    # face: long, lean — the chin sits lower than instinct
    S += [s([(258,310),(250,386),(258,456),(274,526),(304,578),(346,598)], 2.8)]
    S += [s([(462,316),(466,392),(456,462),(436,530),(402,582),(352,600)], 3.3)]
    S += [s([(310,584),(334,598),(368,598),(392,584)], 2.2)]
    # BROWS: the heaviest in the family — dark, straight, low
    S += [s([(280,356),(314,350),(346,355)], 3.4)]
    S += [s([(376,354),(410,348),(442,354)], 3.4)]
    # pale eyes: outlined irises like his brother's, steadier opening
    S += [s([(288,386),(314,378),(340,385)], 2.5)]
    S += [s([(306,380),(314,388),(307,395),(299,388),(306,380)], 1.3)]
    S += [s([(292,396),(316,400),(338,394)], 1.4)]
    S += [s([(380,384),(406,376),(430,383)], 2.5)]
    S += [s([(398,378),(406,386),(399,393),(391,386),(398,378)], 1.3)]
    S += [s([(384,394),(408,398),(428,392)], 1.4)]
    # nose: longer, tip slightly wide
    S += [s([(356,364),(352,448)], 1.9)]
    S += [s([(330,460),(354,470),(380,458)], 2.3)]
    # wide mouth, contained half-smile — corners tucked, not lifted
    S += [s([(310,512),(340,506),(358,509),(378,504),(408,511)], 2.7)]
    S += [s([(306,514),(300,508)], 1.5)]                          # tucked corner
    S += [s([(412,510),(418,504)], 1.5)]
    S += [s([(322,526),(358,533),(394,524)], 2.1)]
    # ears: a touch proud of the head
    S += [s([(252,368),(236,382),(242,420),(260,428)], 2.2)]
    S += [s([(466,364),(482,378),(476,416),(458,424)], 2.2)]
    # long neck, tee
    S += [s([(312,600),(308,656)], 2.5)]
    S += [s([(392,600),(398,654)], 2.5)]
    S += [s([(296,662),(354,680),(410,660)], 2.6)]
    S = tilt(S, 2.0)
    G = [s([(258,384),(462,384)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h036
def h036_jensen_upward():
    """Jensen, patio selfie — the UPWARD armature. Head tipped back:
    eyes sit ABOVE the midline, the jaw underside is a visible plane,
    nostrils show, ears ride LOW, the neck is long and exposed."""
    S = []
    # skull tipped back: crown compressed, face plane long
    S += [s([(250,330),(262,250),(314,204),(380,194),(440,218),(462,288),(464,344)], 3.2)]
    S += [s([(300,254),(336,222),(382,206)], 1.8)]                # quiff, from below
    S += [s([(274,330),(308,302),(354,294),(402,306),(438,336)], 1.9)]  # hairline high
    # face: foreshortened DOWNWARD — features stack low-to-high
    S += [s([(258,346),(252,402),(262,452),(280,496),(308,532),(348,548)], 2.8)]
    S += [s([(460,350),(464,406),(454,456),(434,500),(402,536),(354,550)], 3.2)]
    # eyes ABOVE midline, looking down into the lens
    S += [s([(284,384),(314,376),(342,383)], 3.0)]                # heavy brows
    S += [s([(378,382),(408,374),(438,381)], 3.0)]
    S += [s([(290,404),(314,397),(338,403)], 2.4)]
    S += [s([(304,400),(312,408)], 1.9)]                          # iris, down
    S += [s([(294,412),(316,416),(336,410)], 1.4)]
    S += [s([(382,402),(406,395),(428,401)], 2.4)]
    S += [s([(396,398),(404,406)], 1.9)]
    S += [s([(386,410),(408,414),(426,408)], 1.4)]
    # nose FROM BELOW: short bridge, nostrils visible
    S += [s([(356,396),(352,438)], 1.8)]
    S += [s([(332,450),(356,462),(382,449)], 2.5)]
    S += [s([(340,444),(348,454)], 1.7)]                          # nostrils
    S += [s([(368,442),(360,452)], 1.7)]
    # mouth: slight open smile, compressed against the chin
    S += [s([(316,488),(344,481),(362,484),(380,479),(404,487)], 2.6)]
    S += [s([(324,497),(360,501),(396,495)], 1.5)]
    S += [s([(326,508),(358,515),(390,506)], 2.0)]
    # THE JAW UNDERSIDE — the upward head's signature plane
    S += [s([(308,532),(330,546),(370,546),(398,534)], 2.8)]      # chin shelf
    S += [s([(312,550),(344,566),(386,564),(408,548)], 2.6)]      # underside, heavy
    S += [s([(326,572),(356,582),(388,574)], 1.6)]                # second plane
    # ears LOW
    S += [s([(254,410),(240,424),(246,458),(262,464)], 2.2)]
    S += [s([(462,406),(476,420),(470,454),(454,460)], 2.2)]
    # long exposed neck, tee collar far down
    S += [s([(316,552),(310,640)], 2.6)]
    S += [s([(392,552),(398,636)], 2.6)]
    S += [s([(330,570),(336,620)], 1.2)]                          # throat line
    S += [s([(296,648),(356,668),(412,646)], 2.6)]
    S = tilt(S, -4.0)
    G = [s([(258,400),(460,400)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h037
def h037_jordan_upward():
    """Jordan, car selfie A — mild upward. Chin lifted, eyes down at
    the lens: the appraising look his selfies agree on, made of brow
    compression against a downward iris."""
    S = []
    S += [s([(250,326),(260,246),(312,200),(376,190),(438,214),(460,284),(462,340)], 3.0)]
    S += [s([(294,248),(316,210),(360,190)], 2.0)]
    S += [s([(272,326),(306,298),(352,290),(400,302),(436,332)], 1.9)]
    S += [s([(258,342),(252,398),(262,448),(280,494),(310,530),(350,546)], 2.8)]
    S += [s([(458,346),(462,402),(452,452),(432,498),(400,534),(354,548)], 3.2)]
    # straight brows pressed low by the chin lift
    S += [s([(282,380),(314,374),(344,379)], 2.9)]
    S += [s([(376,378),(408,372),(438,378)], 2.9)]
    # eyes: lids half-drawn, irises at the BOTTOM of the openings
    S += [s([(288,398),(312,392),(336,397)], 2.4)]
    S += [s([(302,398),(310,406),(303,410)], 1.9)]
    S += [s([(292,408),(314,412),(334,406)], 1.5)]
    S += [s([(380,396),(404,390),(426,395)], 2.4)]
    S += [s([(394,396),(402,404),(395,408)], 1.9)]
    S += [s([(384,406),(406,410),(424,404)], 1.5)]
    # nose from below: nostrils, short bridge
    S += [s([(356,392),(352,434)], 1.8)]
    S += [s([(330,446),(354,458),(380,445)], 2.4)]
    S += [s([(338,440),(346,450)], 1.6)]
    S += [s([(370,438),(362,448)], 1.6)]
    # composed mouth, compressed space below
    S += [s([(318,486),(344,480),(360,483),(376,478),(398,485)], 2.6)]
    S += [s([(326,498),(358,505),(390,496)], 2.1)]
    # jaw underside + chin shelf
    S += [s([(310,530),(332,544),(370,544),(396,532)], 2.4)]
    S += [s([(318,546),(348,558),(384,556),(402,544)], 1.7)]
    # ears low, neck long
    S += [s([(254,406),(240,420),(246,452),(262,458)], 2.1)]
    S += [s([(460,402),(474,416),(468,448),(452,454)], 2.1)]
    S += [s([(318,550),(312,634)], 2.6)]
    S += [s([(390,550),(396,630)], 2.6)]
    S += [s([(298,642),(356,660),(410,640)], 2.5)]
    S = tilt(S, -3.0)
    G = [s([(258,396),(458,396)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h038
def h038_jordan_upward_severe():
    """Jordan, car selfie B — the SEVERE tip. Head fully back against
    the seat: the face becomes planes seen from underneath; the throat
    and jaw underside take half the head's height."""
    S = []
    # skull from below: crown nearly gone behind the face plane
    S += [s([(256,356),(272,286),(322,248),(384,240),(440,262),(458,322),(458,372)], 3.2)]
    S += [s([(300,288),(330,258),(372,242)], 1.8)]
    S += [s([(278,358),(312,336),(354,330),(398,340),(432,366)], 1.8)]  # hairline
    # face: severely foreshortened — brow to nose-base is most of it
    S += [s([(264,376),(258,420),(268,458),(286,492),(314,520),(350,534)], 2.8)]
    S += [s([(456,380),(460,424),(450,460),(430,494),(398,524),(354,536)], 3.2)]
    # brows pressed onto the eyes
    S += [s([(288,404),(318,398),(346,403)], 2.9)]
    S += [s([(378,402),(408,396),(436,402)], 2.9)]
    # eyes: slits looking down the nose
    S += [s([(294,420),(318,414),(340,419)], 2.3)]
    S += [s([(306,420),(314,427)], 1.8)]
    S += [s([(382,418),(406,412),(426,417)], 2.3)]
    S += [s([(394,418),(402,425)], 1.8)]
    # nose almost purely from below: nostril plane
    S += [s([(358,414),(354,440)], 1.6)]
    S += [s([(330,452),(356,466),(384,451)], 2.6)]
    S += [s([(338,446),(348,458)], 1.8)]
    S += [s([(372,444),(362,456)], 1.8)]
    # mouth tight under the nose
    S += [s([(322,486),(348,481),(362,484),(378,480),(398,486)], 2.5)]
    S += [s([(330,497),(360,503),(390,495)], 1.9)]
    # the chin/jaw underside — HALF the head now
    S += [s([(314,520),(336,532),(370,532),(394,520)], 2.5)]
    S += [s([(308,540),(340,556),(376,554),(404,538)], 2.2)]
    S += [s([(322,562),(352,574),(386,568)], 1.7)]                # second plane
    # throat, long; collar far down
    S += [s([(320,560),(314,648)], 2.6)]
    S += [s([(388,558),(394,644)], 2.6)]
    S += [s([(334,584),(340,634)], 1.2)]
    S += [s([(300,656),(356,674),(410,652)], 2.5)]
    # ears: LOWEST of the three upward heads
    S += [s([(260,430),(246,444),(252,474),(268,480)], 2.1)]
    S += [s([(456,426),(470,440),(464,470),(448,476)], 2.1)]
    S = tilt(S, 2.5)
    G = [s([(264,416),(456,416)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h039
def h039_bolsevik_reader():
    """Uzbekistan, 1933. Skullcap reader, head BOWED 35° into the
    paper. Brow knit of pure concentration; eyes all but closed
    downward. The crown and cap dominate; the paper crops the chest."""
    S = []
    # bowed skull: cap + crown take the top half
    S += [s([(238,388),(240,300),(290,228),(368,200),(444,222),(482,292),(478,372)], 3.6)]
    # the embroidered cap: band + dome seam, two pattern ticks only
    S += [s([(262,300),(310,266),(368,254),(424,268),(462,302)], 2.6)]
    S += [s([(310,266),(330,234),(380,222)], 1.6)]
    S += [s([(330,280),(342,266)], 1.1)]
    S += [s([(386,264),(398,252)], 1.1)]
    # face below, foreshortened: brow knit is the event
    S += [s([(258,398),(254,448),(266,492),(286,528),(318,552)], 2.8)]
    S += [s([(474,384),(478,436),(464,482),(438,520),(396,546),(352,556)], 3.2)]
    # the KNIT: two short verticals between brows + bunched brow lines
    S += [s([(348,420),(346,442)], 1.8)]
    S += [s([(362,418),(361,440)], 1.8)]
    S += [s([(288,432),(320,420),(344,428)], 3.2)]
    S += [s([(366,426),(396,416),(426,426)], 3.2)]
    # eyes: closed-down curves under the bunch
    S += [s([(296,452),(322,446),(344,451)], 2.4)]
    S += [s([(300,460),(324,456),(342,459)], 1.3)]
    S += [s([(372,450),(398,444),(420,449)], 2.4)]
    S += [s([(376,458),(400,454),(418,457)], 1.3)]
    # broad nose, foreshortened long by the bow
    S += [s([(356,440),(352,496)], 1.9)]
    S += [s([(328,506),(354,518),(384,505)], 2.6)]
    # mouth: pressed, mostly shadow under the mustache line
    S += [s([(322,538),(352,532),(384,537)], 2.3)]
    # weathered cheek planes — one carved line each side
    S += [s([(282,470),(300,506)], 1.5)]
    S += [s([(446,462),(428,498)], 1.5)]
    # ears: HIGH with the bow, wide of the head
    S += [s([(238,396),(220,408),(226,446),(244,454)], 2.4)]
    S += [s([(478,388),(496,400),(490,438),(472,446)], 2.4)]
    # the newspaper edge crops everything below
    S += [s([(160,640),(360,600),(560,628)], 3.6)]
    S += [s([(174,668),(360,628),(546,654)], 2.0)]
    S = tilt(S, -2.0)
    G = [s([(258,444),(474,436)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h040
def h040_cafe_reader():
    """Athens, 1981. Café reader bowed over a held-up broadsheet —
    the paper's top edge crops him at the mustache. Thick side-parted
    hair falls forward; the nose and the mustache do all the talking."""
    S = []
    # bowed head over the paper: hair mass forward
    S += [s([(244,380),(250,292),(304,228),(380,204),(450,228),(480,300),(474,376)], 3.4)]
    S += [s([(290,250),(338,226),(394,220)], 1.8)]                # part sweep
    S += [s([(266,330),(258,372),(268,398)], 2.2)]                # forelock falls
    S += [s([(272,374),(308,344),(354,334),(402,346),(438,376)], 1.9)]
    # face to the mustache only — the paper takes the rest
    S += [s([(262,392),(258,436),(268,470)], 2.8)]
    S += [s([(470,388),(474,432),(462,466)], 3.0)]
    # brows: drawn down, reading
    S += [s([(286,420),(318,410),(344,417)], 2.8)]
    S += [s([(372,415),(402,406),(430,415)], 2.8)]
    # eyes: down, hooded by concentration
    S += [s([(294,440),(320,433),(342,439)], 2.4)]
    S += [s([(298,448),(322,444),(340,447)], 1.3)]
    S += [s([(376,437),(400,431),(420,437)], 2.4)]
    S += [s([(380,445),(402,441),(418,444)], 1.3)]
    # the strong nose — biggest committed line of the head
    S += [s([(354,428),(350,478),(342,496)], 2.4)]
    S += [s([(342,496),(358,506),(380,496)], 2.4)]
    # the MUSTACHE: dense, drooping — then the paper
    S += [s([(316,516),(352,508),(390,517)], 3.6)]
    S += [s([(320,526),(352,520),(386,527)], 2.6)]
    # THE PAPER: held high, slightly tilted, cropping at the mustache
    S += [s([(140,560),(360,528),(580,552)], 3.8)]
    S += [s([(154,590),(360,556),(566,580)], 2.2)]
    S += [s([(200,572),(220,570)], 1.1)]                          # column ticks
    S += [s([(260,564),(280,562)], 1.1)]
    S += [s([(420,564),(440,566)], 1.1)]
    # hands gripping the page edges
    S += [s([(168,560),(158,600),(170,640)], 2.6)]
    S += [s([(548,556),(560,596),(550,636)], 2.6)]
    S = tilt(S, 2.0)
    G = [s([(262,436),(470,430)], 1.0)]
    return S, G


# ---------------------------------------------------------------- h041
def h041_stool_reader():
    """Elderly reader on a stool. Bowed ~30°, glasses slid down the
    hooked nose, white hair open at the crown, hollow cheek. The
    paper droops from both hands below."""
    S = []
    # bowed skull: bald crown toward us, white side-hair
    S += [s([(248,376),(252,290),(304,224),(378,198),(448,222),(478,292),(472,368)], 3.4)]
    S += [s([(272,330),(262,366),(272,392)], 1.8)]                # side tuft
    S += [s([(452,322),(464,358),(454,386)], 1.8)]
    S += [s([(286,360),(320,334),(364,326),(408,336),(440,364)], 1.7)]  # open crown line
    # face: gaunt, hollow-cheeked, foreshortened down
    S += [s([(266,388),(260,436),(272,478),(292,514),(322,538)], 2.8)]
    S += [s([(466,380),(470,428),(456,470),(430,506),(392,532),(350,542)], 3.2)]
    # GLASSES slid down: frames riding the nose tip, eyes OVER them
    S += [s([(296,452),(330,446),(352,452),(354,472),(344,484),(312,486),(296,476),(294,460),(296,452)], 2.4)]
    S += [s([(366,450),(398,444),(420,450),(422,468),(412,480),(382,482),(366,472),(364,456),(366,450)], 2.4)]
    S += [s([(354,462),(366,460)], 2.0)]
    # eyes above the frames, lids down — he reads over the glasses
    S += [s([(302,432),(326,426),(346,431)], 2.3)]
    S += [s([(372,429),(396,423),(416,429)], 2.3)]
    S += [s([(306,440),(328,436),(344,439)], 1.2)]
    S += [s([(376,437),(398,433),(414,436)], 1.2)]
    # brows: white, sparse
    S += [s([(298,416),(326,410),(348,415)], 1.9)]
    S += [s([(370,413),(396,407),(418,413)], 1.9)]
    # hooked nose carrying the glasses
    S += [s([(356,420),(352,470),(344,490)], 2.2)]
    S += [s([(344,490),(358,500),(378,491)], 2.2)]
    # mouth: thin, set; hollow cheek lines
    S += [s([(322,520),(350,514),(382,520)], 2.2)]
    S += [s([(330,530),(354,535),(378,528)], 1.4)]
    S += [s([(288,464),(304,502)], 1.5)]
    S += [s([(444,458),(426,494)], 1.5)]
    # ears high (bowed)
    S += [s([(248,388),(232,400),(238,434),(254,442)], 2.2)]
    S += [s([(472,382),(488,394),(482,428),(464,436)], 2.2)]
    # the drooping paper below, both hands
    S += [s([(180,620),(300,586),(330,600)], 3.0)]                # left wing
    S += [s([(370,598),(420,584),(540,614)], 3.0)]                # right wing
    S += [s([(196,648),(300,614),(326,626)], 1.8)]
    S += [s([(374,624),(424,610),(524,640)], 1.8)]
    S += [s([(312,604),(308,648),(320,668)], 2.2)]                # hand
    S += [s([(388,602),(396,644),(386,664)], 2.2)]
    S = tilt(S, -1.5)
    G = [s([(266,430),(466,424)], 1.0)]
    return S, G


HEADS = [
    ("h032", h032_jennifer_redraw),
    ("h033", h033_jim_multi),
    ("h034", h034_jordan_synthesis),
    ("h035", h035_jensen),
    ("h036", h036_jensen_upward),
    ("h037", h037_jordan_upward),
    ("h038", h038_jordan_upward_severe),
    ("h039", h039_bolsevik_reader),
    ("h040", h040_cafe_reader),
    ("h041", h041_stool_reader),
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
