"""
HUMAN STUDIES VOL. 1 — ASSIGNMENT 2A, batch 01 (f201–f210).
Ten drawn OBSERVATIONS, chosen directly from the Fifty Faces corpus.
The observation is the subject, not the label. Every head hand-built
from its source frames — no parametric helpers (the h086 confession
stands). Per drawing, the ledger states only: what changed / what
did not change.

f201  Entry 11 — the long neutral (Jordan, kitchen, glasses)
f202  Entry 20 — the smile that arrived before the gaze (Jordan, board)
f203  Entry 25 — the laugh that left mouth first, eyes last (Jordan)
f204  Entry 24 — the smile that modulated, never switched (Greg)
f205  Entry 18 — the question-landing hold (Cuban)
f206  Entry  5 — the offered chin (Greg, kissed, eyes closed)
f207  Entry  3 — the weather-check (Jordan, speech paused in the mouth)
f208  Entry 21 — the verdict pause (Jordan, mirror judge)
f209  Entry  1 — the over-stillness (Jordan, WWHL, pre-speech)
f210  Entry  9 — emphasis closure (homilist, eyes shut, mouth smiling on)
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from line_figure import render               # noqa: E402
from heads_batch01 import s, tilt            # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
W, H = 700, 850


def f201_long_neutral():
    """Entry 11. Jordan, kitchen, glasses, gaze on the hands below
    frame. Jaw level, mouth set not pressed, brow near-still. Head
    pitched down ~8: crown gains, jaw foreshortens slightly."""
    S = []
    # skull, mild bow: crown high, face plane shortened
    S += [s([(248,318),(254,216),(308,150),(376,138),(442,170),(468,258),(470,330)], 3.0)]
    S += [s([(286,238),(306,180),(352,150),(398,146)], 2.2)]            # quiff up-back
    S += [s([(266,318),(300,280),(350,290),(402,276),(446,322)], 2.0)]  # temple-notched hairline, low (bow)
    S += [s([(258,334),(252,402),(264,466),(284,528),(314,572),(354,590)], 2.8)]
    S += [s([(462,340),(464,408),(452,470),(430,532),(398,576),(358,592)], 3.2)]
    S += [s([(318,578),(340,590),(372,590),(394,578)], 2.2)]            # chin shelf
    # glasses: two rounded rects, owned edges; bridge
    S += [s([(284,376),(346,372),(350,412),(288,416),(284,376)], 2.0)]
    S += [s([(376,370),(438,366),(442,406),(380,410),(376,370)], 2.0)]
    S += [s([(350,390),(376,388)], 1.8)]
    S += [s([(284,380),(262,372)], 1.6)]                                # temple arm
    S += [s([(442,372),(462,362)], 1.6)]
    # eyes DOWN inside lenses: low lids, irises sunk to lower lid, outlined
    S += [s([(296,394),(318,390),(338,395)], 2.4)]                      # lid low
    S += [s([(306,396),(313,402),(306,407),(300,401),(306,396)], 1.2)]  # iris low, outlined
    S += [s([(386,392),(408,388),(428,393)], 2.4)]
    S += [s([(396,394),(403,400),(396,405),(390,399),(396,394)], 1.2)]
    # brows: straight, low, quiet — above lens line
    S += [s([(288,362),(318,357),(344,361)], 2.7)]
    S += [s([(380,359),(410,354),(436,359)], 2.7)]
    # nose foreshortened by bow; mouth set, level, unpressed
    S += [s([(360,386),(356,448)], 1.8)]
    S += [s([(336,460),(358,468),(382,458)], 2.2)]
    S += [s([(322,512),(346,508),(362,510),(380,506),(400,511)], 2.5)]  # set mouth
    S += [s([(330,524),(360,529),(390,522)], 1.9)]                      # fuller lower lip
    # neck into collar, hoodie line
    S += [s([(316,592),(312,650)], 2.4)]
    S += [s([(394,592),(400,648)], 2.4)]
    S += [s([(288,660),(354,682),(420,656)], 2.6)]
    S += [s([(276,690),(352,714),(430,686)], 1.4)]
    S = tilt(S, -3.0)
    return S, [s([(258,392),(462,392)], 1.0)]


def f202_smile_before_gaze():
    """Entry 20. Head and gaze still DOWN on the work; the mouth
    corners already rising. The smile predates the look."""
    S = []
    S += [s([(250,322),(258,218),(312,150),(378,140),(442,174),(466,262),(466,334)], 3.0)]
    S += [s([(290,240),(310,182),(356,152),(400,148)], 2.2)]
    S += [s([(268,322),(302,284),(352,294),(404,280),(444,326)], 2.0)]
    S += [s([(260,338),(254,406),(266,470),(286,530),(316,572),(356,590)], 2.8)]
    S += [s([(460,344),(462,410),(450,472),(428,532),(396,576),(360,592)], 3.2)]
    S += [s([(320,578),(342,590),(372,590),(392,578)], 2.2)]
    # eyes still down at the board: low lids, sunk outlined irises
    S += [s([(292,392),(316,387),(340,392)], 2.5)]
    S += [s([(303,394),(310,400),(303,405),(297,399),(303,394)], 1.2)]
    S += [s([(382,389),(406,384),(430,389)], 2.5)]
    S += [s([(393,391),(400,397),(393,402),(387,396),(393,391)], 1.2)]
    S += [s([(286,362),(316,357),(342,361)], 2.7)]
    S += [s([(378,358),(408,353),(434,358)], 2.7)]
    S += [s([(358,384),(354,446)], 1.8)]
    S += [s([(334,458),(356,466),(380,456)], 2.2)]
    # THE SUBJECT: corners rising while everything else stays down.
    # asymmetric beginning smile — right corner leads; cheek ball waking
    S += [s([(322,512),(344,506),(360,508),(380,500),(402,498)], 2.5)]  # right corner up
    S += [s([(330,524),(360,528),(392,514)], 1.9)]
    S += [s([(398,478),(412,494)], 1.3)]                                # waking cheek crease, right only
    S += [s([(316,592),(312,650)], 2.4)]
    S += [s([(394,592),(400,648)], 2.4)]
    S += [s([(290,660),(356,680),(420,656)], 2.6)]
    S = tilt(S, -4.0)
    return S, [s([(260,392),(460,392)], 1.0)]


def f203_laugh_leaving():
    """Entry 25. The drain, mid-order: mouth already closed to a soft
    smile, cheeks half-dropped, eye-crease still FULL. The eyes are
    the last to leave."""
    S = []
    S += [s([(248,306),(258,214),(310,152),(376,142),(442,172),(466,256),(468,318)], 3.0)]
    S += [s([(292,236),(312,180),(358,150),(402,146)], 2.2)]
    S += [s([(266,306),(300,266),(352,278),(404,264),(446,310)], 2.0)]
    S += [s([(258,322),(252,392),(264,456),(284,520),(314,564),(354,584)], 2.8)]
    S += [s([(462,328),(464,396),(452,460),(430,524),(398,568),(358,586)], 3.2)]
    S += [s([(318,572),(340,584),(372,584),(392,572)], 2.2)]
    # eyes: lids half-lowered, crow's feet still deep, lower-lid push
    S += [s([(286,378),(314,372),(340,377)], 2.6)]                      # heavy upper lid
    S += [s([(292,390),(314,384),(336,389)], 1.6)]                      # lowered lid edge
    S += [s([(296,400),(318,404),(338,398)], 1.5)]                      # lower-lid push, still up
    S += [s([(380,375),(408,369),(432,374)], 2.6)]
    S += [s([(386,387),(408,381),(428,386)], 1.6)]
    S += [s([(388,397),(410,401),(428,395)], 1.5)]
    S += [s([(278,372),(268,382)], 1.2)]                                # crow's feet, left
    S += [s([(278,384),(266,392)], 1.2)]
    S += [s([(440,369),(452,379)], 1.2)]                                # crow's feet, right
    S += [s([(440,381),(452,389)], 1.2)]
    S += [s([(284,356),(314,351),(340,355)], 2.7)]
    S += [s([(378,353),(408,348),(432,353)], 2.7)]
    S += [s([(358,378),(354,440)], 1.8)]
    S += [s([(334,452),(356,460),(380,450)], 2.2)]
    # mouth: closed soft smile — already home; cheek lines half-faded
    S += [s([(324,500),(346,494),(362,496),(380,492),(400,496)], 2.4)]
    S += [s([(332,512),(360,517),(390,508)], 1.9)]
    S += [s([(310,470),(322,492)], 1.1)]                                # fading cheek crease
    S += [s([(404,468),(396,490)], 1.1)]
    S += [s([(316,586),(312,644)], 2.4)]
    S += [s([(394,586),(400,642)], 2.4)]
    S += [s([(290,654),(356,674),(420,650)], 2.6)]
    S = tilt(S, 2.5)
    return S, [s([(258,380),(462,382)], 1.0)]


def f204_smile_that_modulated():
    """Entry 24. Greg receiving the story from inches away: head
    stationary and upright, gaze hard LEFT to the teller, brows
    popped, closed-mouth smile one notch below the laugh."""
    S = []
    # rounder, broader skull than Jordan's; fuller cheeks; mustache
    S += [s([(240,310),(252,212),(312,148),(386,140),(452,176),(474,262),(474,330)], 3.0)]
    S += [s([(284,232),(312,176),(362,148),(410,150)], 2.2)]            # short dark hair, low crown
    S += [s([(262,308),(298,272),(354,284),(410,270),(452,314)], 2.0)]
    S += [s([(252,326),(248,398),(262,464),(286,528),(320,572),(360,590)], 2.8)]
    S += [s([(470,334),(470,404),(458,468),(434,530),(400,574),(364,592)], 3.2)]
    S += [s([(324,580),(346,592),(376,592),(396,580)], 2.2)]
    # brows POPPED high — arcs lifted, gap to eyes wide
    S += [s([(284,344),(316,336),(346,342)], 2.8)]
    S += [s([(382,340),(414,332),(444,340)], 2.8)]
    # eyes: open, irises hard LEFT (to the teller), outlined
    S += [s([(288,382),(314,375),(340,381)], 2.4)]
    S += [s([(292,385),(300,392),(293,399),(286,392),(292,385)], 1.3)]  # iris at left corner
    S += [s([(294,397),(318,402),(338,396)], 1.4)]
    S += [s([(382,378),(408,371),(434,377)], 2.4)]
    S += [s([(385,381),(393,388),(386,395),(379,388),(385,381)], 1.3)]
    S += [s([(388,393),(410,398),(430,392)], 1.4)]
    # nose shorter/broader; mustache as one mass + closed wide smile
    S += [s([(362,368),(358,432)], 1.9)]
    S += [s([(336,444),(360,452),(386,442)], 2.3)]
    S += [s([(322,478),(360,486),(400,476)], 3.2)]                      # mustache mass
    S += [s([(318,502),(344,510),(364,512),(386,508),(410,498)], 2.5)]  # wide closed smile
    S += [s([(330,522),(362,528),(396,518)], 1.9)]
    S += [s([(302,468),(316,498)], 1.2)]                                # full cheek crease L
    S += [s([(418,464),(408,496)], 1.2)]                                # full cheek crease R
    S += [s([(320,592),(316,648)], 2.4)]
    S += [s([(398,592),(404,646)], 2.4)]
    S += [s([(292,658),(360,680),(428,654)], 2.6)]
    S = tilt(S, -1.5)
    return S, [s([(252,384),(470,384)], 1.0)]


def f205_question_landing():
    """Entry 18. The hold: mouth sealed and compressed, eyes steady
    on the questioner (left), head still — the micro-nod lives in a
    slightly dropped chin. Glasses; swept-back hair; the observed
    deep folds stay because the frames showed them."""
    S = []
    # broad squarish skull, age in the frame: heavier jaw, jowl break
    S += [s([(238,308),(250,214),(310,152),(388,142),(456,178),(478,264),(478,330)], 3.0)]
    S += [s([(280,222),(330,176),(390,160),(440,176)], 2.4)]            # gray sweep back
    S += [s([(262,288),(306,260),(360,268),(416,256),(458,296)], 2.0)]  # high hairline
    S += [s([(250,324),(246,398),(258,462),(280,524),(316,566),(360,584)], 2.8)]
    S += [s([(474,332),(474,402),(464,464),(442,524),(406,568),(364,586)], 3.2)]
    S += [s([(322,574),(344,586),(376,586),(398,574)], 2.4)]
    S += [s([(262,500),(282,538)], 1.6)]                                # jowl break L
    S += [s([(452,498),(434,536)], 1.6)]                                # jowl break R
    # dark heavy glasses
    S += [s([(278,362),(348,356),(352,404),(282,410),(278,362)], 2.6)]
    S += [s([(378,354),(450,348),(454,396),(382,402),(378,354)], 2.6)]
    S += [s([(352,380),(378,376)], 2.2)]
    # eyes steady LEFT inside lenses
    S += [s([(292,380),(316,374),(340,379)], 2.2)]
    S += [s([(296,382),(304,389),(297,396),(290,389),(296,382)], 1.3)]
    S += [s([(386,374),(412,368),(438,373)], 2.2)]
    S += [s([(390,376),(398,383),(391,390),(384,383),(390,376)], 1.3)]
    # brows above frames, level
    S += [s([(282,344),(314,339),(344,343)], 2.6)]
    S += [s([(380,338),(414,333),(446,338)], 2.6)]
    # nose broad; observed deep nasolabial folds; SEALED mouth
    S += [s([(364,372),(358,442)], 2.0)]
    S += [s([(334,454),(360,464),(388,452)], 2.4)]
    S += [s([(316,452),(306,506)], 1.5)]                                # nasolabial L
    S += [s([(412,448),(420,502)], 1.5)]                                # nasolabial R
    S += [s([(322,514),(360,518),(402,512)], 2.8)]                      # one firm sealed line
    S += [s([(316,520),(322,512)], 1.4)]                                # compression dimple L
    S += [s([(406,518),(400,510)], 1.4)]                                # compression dimple R
    S += [s([(334,532),(364,536),(394,530)], 1.7)]                      # pressed lower lip
    # chin dropped a degree: the nod in residence
    S += [s([(320,584),(316,640)], 2.5)]
    S += [s([(400,584),(406,638)], 2.5)]
    S += [s([(286,652),(360,676),(434,648)], 2.7)]
    S += [s([(274,684),(360,710),(444,680)], 1.4)]                      # jacket line
    S = tilt(S, -2.0)
    return S, [s([(250,382),(474,382)], 1.0)]


def f206_offered_chin():
    """Entry 5. Greg receiving the kiss: chin UP and held there,
    eyes closed, the singing shape collapsed into a pressed scrunch
    smile. Hat brim owns the forehead edge. Upward armature: eyes
    above midline, ears low, underside of jaw showing."""
    S = []
    # upward-tilted skull: jaw underside visible, crown hidden by hat
    S += [s([(252,304),(258,288)], 2.4)]                                # skull peek L of brim
    S += [s([(462,308),(458,292)], 2.4)]                                # skull peek R of brim
    # hat brim: strong ellipse owning the forehead edge, low over the brows
    S += [s([(236,300),(302,272),(394,266),(464,284),(488,308)], 3.6)]
    S += [s([(252,272),(322,236),(408,230),(468,256)], 2.8)]            # crown of hat
    S += [s([(236,300),(246,318)], 2.2)]                                # brim lip L
    S += [s([(488,308),(476,324)], 2.2)]                                # brim lip R
    # face sides; ears LOW (upward head)
    S += [s([(258,318),(254,380),(266,438),(288,494),(320,540),(360,560)], 2.8)]
    S += [s([(460,322),(462,386),(452,442),(432,496),(402,542),(364,562)], 3.2)]
    S += [s([(246,360),(232,376),(238,412),(256,418)], 2.2)]            # ear low L
    S += [s([(470,358),(484,372),(478,408),(460,414)], 2.2)]            # ear low R
    # jaw underside plane — the offered chin, stated twice
    S += [s([(322,548),(344,560),(374,560),(396,548)], 2.4)]
    S += [s([(330,572),(360,582),(392,570)], 2.0)]                      # underside shadow line
    S += [s([(304,360),(314,368)], 1.3)]                                # squeeze tick under eye L
    S += [s([(416,358),(406,366)], 1.3)]                                # squeeze tick under eye R
    # eyes CLOSED: down-curved lash lines high on the face (upward tilt)
    S += [s([(292,344),(316,352),(340,346)], 2.6)]
    S += [s([(384,342),(408,350),(432,344)], 2.6)]
    S += [s([(296,332),(318,338),(338,333)], 1.3)]                      # lid fold above
    S += [s([(388,330),(410,336),(430,331)], 1.3)]
    # brows easy, slightly lifted by the scrunch
    S += [s([(288,320),(318,314),(344,318)], 2.6)]
    S += [s([(382,316),(412,310),(440,315)], 2.6)]
    # nose from below: septum + nostril hints
    S += [s([(362,352),(358,402)], 1.8)]
    S += [s([(340,412),(360,420),(384,410)], 2.2)]
    S += [s([(348,408),(352,414)], 1.2)]
    S += [s([(372,407),(376,413)], 1.2)]
    # pressed scrunch smile: compressed curved lips, cheek balls HIGH
    S += [s([(324,462),(348,470),(366,472),(386,468),(408,458)], 2.7)]
    S += [s([(334,478),(364,484),(398,474)], 2.0)]
    S += [s([(306,428),(322,452)], 1.3)]                                # high cheek ball L
    S += [s([(420,424),(406,450)], 1.3)]                                # high cheek ball R
    # neck stretched by the lift
    S += [s([(326,564),(322,640)], 2.5)]
    S += [s([(396,564),(402,638)], 2.5)]
    S += [s([(296,652),(362,672),(430,648)], 2.6)]
    S = tilt(S, 5.0)
    return S, [s([(258,348),(462,350)], 1.0)]


def f207_weather_check():
    """Entry 3. The pause that funds the eyes: gaze UP-LEFT, mouth
    pressed closed mid-sentence, brows raised. One umbrella rib owns
    the top corner."""
    S = []
    S += [s([(248,300),(258,212),(312,150),(378,140),(442,172),(466,256),(468,316)], 3.0)]
    S += [s([(292,234),(312,178),(358,148),(402,144)], 2.2)]
    S += [s([(266,300),(300,262),(352,274),(404,260),(446,306)], 2.0)]
    S += [s([(258,318),(252,390),(264,454),(284,518),(314,562),(354,582)], 2.8)]
    S += [s([(462,324),(464,394),(452,458),(430,522),(398,566),(358,584)], 3.2)]
    S += [s([(318,570),(340,582),(372,582),(392,570)], 2.2)]
    # umbrella canopy: edge + scallops anchored across the whole top,
    # passing close over the crown so the edge is OWNED, not stray
    S += [s([(60,196),(280,126),(640,100)], 3.4)]                       # canopy edge
    S += [s([(60,196),(150,204),(238,182)], 2.2)]                       # scallop pair L
    S += [s([(238,182),(330,186),(420,158)], 2.2)]                      # scallop pair mid
    S += [s([(330,134),(322,96)], 1.8)]                                 # one rib to off-frame ferrule
    # eyes UP-LEFT: irises high under upper lid, whites below
    S += [s([(286,374),(314,368),(340,373)], 2.5)]
    S += [s([(292,375),(300,381),(293,388),(286,381),(292,375)], 1.3)]  # iris tucked up-left
    S += [s([(292,392),(316,396),(338,390)], 1.4)]                      # white showing below
    S += [s([(380,371),(408,365),(432,370)], 2.5)]
    S += [s([(385,372),(393,378),(386,385),(379,378),(385,372)], 1.3)]
    S += [s([(386,389),(410,393),(430,387)], 1.4)]
    # brows raised toward the weather
    S += [s([(284,348),(314,342),(340,347)], 2.7)]
    S += [s([(378,345),(408,339),(434,345)], 2.7)]
    S += [s([(358,376),(354,438)], 1.8)]
    S += [s([(334,450),(356,458),(380,448)], 2.2)]
    # mouth PRESSED — the sentence holding its breath
    S += [s([(326,504),(360,508),(396,502)], 2.7)]
    S += [s([(334,518),(362,522),(390,515)], 1.7)]
    S += [s([(316,584),(312,642)], 2.4)]
    S += [s([(394,584),(400,640)], 2.4)]
    # collar of the gray blazer, white shirt V
    S += [s([(288,652),(330,668),(354,690)], 2.4)]
    S += [s([(422,648),(382,666),(354,690)], 2.4)]
    S += [s([(312,652),(354,676)], 1.4)]
    S += [s([(398,650),(354,676)], 1.4)]
    S = tilt(S, -2.0)
    return S, [s([(258,378),(462,378)], 1.0)]


def f208_verdict_pause():
    """Entry 21. The judge face between adjustments: gaze dead-on at
    the reflection, inner brows a degree in, lips parted slack, one
    hand still in the hair — two curves inside the mass."""
    S = []
    S += [s([(250,304),(260,214),(314,152),(380,142),(444,174),(466,258),(468,318)], 3.0)]
    # hair mass pushed up by the working hand
    S += [s([(294,232),(318,172),(368,144),(410,148)], 2.4)]
    S += [s([(268,304),(302,266),(354,278),(406,264),(446,310)], 2.0)]
    # the hand IN the hair: wrist enters from upper right, two curves,
    # fingertips vanish into the mass (hair owns the meeting edge)
    S += [s([(478,128),(430,150),(396,168)], 2.8)]                      # wrist/back of hand
    S += [s([(470,150),(428,168),(398,180)], 2.2)]                      # finger curve
    S += [s([(412,160),(416,170)], 1.3)]                                # knuckle hint
    S += [s([(396,168),(382,186)], 1.6)]                                # tips entering the mass
    S += [s([(258,320),(252,392),(264,456),(284,518),(314,562),(354,582)], 2.8)]
    S += [s([(462,326),(464,396),(452,460),(430,522),(398,566),(358,584)], 3.2)]
    S += [s([(318,570),(340,582),(372,582),(392,570)], 2.2)]
    # eyes dead-on, fully open, outlined irises centered
    S += [s([(286,378),(314,372),(340,377)], 2.5)]
    S += [s([(304,380),(312,388),(305,396),(297,388),(304,380)], 1.3)]
    S += [s([(292,396),(316,400),(338,394)], 1.4)]
    S += [s([(380,375),(408,369),(432,374)], 2.5)]
    S += [s([(398,377),(406,385),(399,393),(391,385),(398,377)], 1.3)]
    S += [s([(386,393),(410,397),(430,391)], 1.4)]
    # brows: straight low + a single inner-knit tick between them
    S += [s([(284,356),(314,351),(340,355)], 2.8)]
    S += [s([(378,353),(408,348),(434,353)], 2.8)]
    S += [s([(352,352),(356,344)], 1.4)]                                # the micro-frown
    S += [s([(358,380),(354,442)], 1.8)]
    S += [s([(334,454),(356,462),(380,452)], 2.2)]
    # lips parted slack — judging, not speaking
    S += [s([(326,506),(348,502),(362,504),(380,500),(398,504)], 2.3)]
    S += [s([(330,516),(360,514),(394,512)], 1.6)]                      # dark parting hint
    S += [s([(334,526),(362,530),(390,523)], 1.8)]
    S += [s([(316,584),(312,642)], 2.4)]
    S += [s([(394,584),(400,640)], 2.4)]
    # tank strap lines
    S += [s([(300,652),(332,672)], 2.2)]
    S += [s([(412,648),(380,670)], 2.2)]
    S = tilt(S, 1.5)
    return S, [s([(258,382),(462,382)], 1.0)]


def f209_over_stillness():
    """Entry 1. The face doing LESS than rest: lips pressed level,
    brows level-low, gaze locked to lens, everything symmetric.
    Greg's arm crosses behind the shoulders — one soft diagonal."""
    S = []
    S += [s([(250,302),(260,212),(314,150),(380,140),(444,172),(466,256),(468,316)], 3.0)]
    S += [s([(294,232),(314,176),(360,146),(404,142)], 2.2)]
    S += [s([(268,302),(302,264),(354,276),(406,262),(446,308)], 2.0)]
    S += [s([(258,318),(252,390),(264,454),(284,516),(314,560),(354,580)], 2.8)]
    S += [s([(462,324),(464,394),(452,458),(430,520),(398,564),(358,582)], 3.2)]
    S += [s([(318,568),(340,580),(372,580),(392,568)], 2.2)]
    # eyes locked, symmetric, hooded; outlined pale irises dead center
    S += [s([(286,376),(314,370),(340,375)], 2.5)]
    S += [s([(290,388),(314,381),(338,387)], 1.4)]                      # hood line
    S += [s([(303,381),(311,389),(304,397),(296,389),(303,381)], 1.3)]
    S += [s([(292,397),(316,401),(338,395)], 1.4)]
    S += [s([(380,373),(408,367),(432,372)], 2.5)]
    S += [s([(384,385),(408,378),(430,384)], 1.4)]
    S += [s([(397,378),(405,386),(398,394),(390,386),(397,378)], 1.3)]
    S += [s([(386,394),(410,398),(430,392)], 1.4)]
    # brows: straight, LOW, perfectly level — the suppression
    S += [s([(284,356),(314,352),(340,355)], 2.8)]
    S += [s([(378,353),(408,349),(434,353)], 2.8)]
    S += [s([(358,378),(354,440)], 1.8)]
    S += [s([(334,452),(356,460),(380,450)], 2.2)]
    # mouth: pressed level line, fuller lower lip held flat
    S += [s([(326,506),(360,509),(396,504)], 2.6)]
    S += [s([(334,520),(362,524),(390,517)], 1.8)]
    S += [s([(316,582),(312,640)], 2.4)]
    S += [s([(394,582),(400,638)], 2.4)]
    # Greg's arm: one soft diagonal mass behind the shoulders
    S += [s([(230,640),(300,610),(390,604),(470,622)], 3.2)]
    S += [s([(244,664),(310,636),(396,630)], 1.6)]
    S += [s([(288,650),(354,672),(420,648)], 2.6)]
    S = tilt(S, -1.0)
    return S, [s([(258,380),(462,380)], 1.0)]


def f210_emphasis_closure():
    """Entry 9. Eyes shut WITH knit brows while the mouth goes on
    smiling-and-talking; the head tips into the phrase. Lean face,
    short dark hair, the observed vertical cheek creases."""
    S = []
    # lean long face
    S += [s([(258,296),(266,208),(318,150),(380,142),(438,172),(458,254),(458,318)], 3.0)]
    S += [s([(296,222),(326,170),(374,148),(412,152)], 2.2)]            # short hair tight
    S += [s([(274,296),(306,262),(354,272),(400,260),(436,300)], 2.0)]
    S += [s([(266,320),(262,392),(272,454),(290,516),(318,558),(354,576)], 2.8)]
    S += [s([(452,326),(454,396),(444,458),(424,518),(394,560),(358,578)], 3.0)]
    S += [s([(322,566),(342,578),(370,578),(390,566)], 2.2)]
    # eyes SHUT tight: curved lash lines + squeeze tick below each
    S += [s([(292,382),(316,389),(340,383)], 2.7)]
    S += [s([(298,395),(316,399),(334,394)], 1.3)]                      # squeeze line
    S += [s([(382,380),(406,387),(430,381)], 2.7)]
    S += [s([(388,393),(406,397),(424,392)], 1.3)]
    # brows KNIT while shut: inner ends pulled down-in, twin ticks
    S += [s([(290,360),(318,356),(342,362)], 2.8)]
    S += [s([(380,361),(408,355),(432,359)], 2.8)]
    S += [s([(348,366),(354,354)], 1.5)]                                # knit tick L
    S += [s([(366,354),(372,366)], 1.5)]                                # knit tick R
    # nose; the observed vertical cheek creases, deep
    S += [s([(360,380),(356,438)], 1.8)]
    S += [s([(336,450),(356,458),(378,448)], 2.2)]
    S += [s([(312,440),(304,506)], 1.6)]
    S += [s([(404,436),(412,502)], 1.6)]
    # mouth OPEN smiling-speech: upper line, teeth hint, lower curve deep
    S += [s([(318,498),(342,490),(360,492),(380,488),(404,494)], 2.6)]
    S += [s([(326,506),(360,510),(396,504)], 1.4)]                      # teeth line
    S += [s([(326,524),(360,534),(396,522)], 2.4)]                      # open lower lip
    S += [s([(318,498),(312,510)], 1.3)]                                # corner depth L
    S += [s([(404,494),(410,506)], 1.3)]
    # clergy collar: white band + vestment shoulders, owned edges
    S += [s([(318,578),(314,624)], 2.4)]
    S += [s([(392,578),(398,622)], 2.4)]
    S += [s([(296,636),(356,652),(418,632)], 2.6)]
    S += [s([(300,650),(356,666),(414,646)], 1.6)]                      # collar band
    S += [s([(238,700),(300,664),(356,668)], 2.8)]                      # vestment slope L
    S += [s([(472,696),(414,662),(356,668)], 2.8)]
    S = tilt(S, -5.0)
    return S, [s([(266,386),(454,386)], 1.0)]


SEQ = [("f201", f201_long_neutral),
       ("f202", f202_smile_before_gaze),
       ("f203", f203_laugh_leaving),
       ("f204", f204_smile_that_modulated),
       ("f205", f205_question_landing),
       ("f206", f206_offered_chin),
       ("f207", f207_weather_check),
       ("f208", f208_verdict_pause),
       ("f209", f209_over_stillness),
       ("f210", f210_emphasis_closure)]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    imgs = []
    for name, fn in SEQ:
        S, G = fn()
        im = render(S, G, W, H, seed=hash(name) % 999)
        im.save(os.path.join(OUT, f"{name}.png"))
        imgs.append((name, im))
        print("wrote", name)
    cols, rows = 5, 2
    sheet = Image.new("RGB", (cols * W // 2, rows * H // 2), (245, 241, 234))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(imgs):
        x, y = (i % cols) * W // 2, (i // cols) * H // 2
        sheet.paste(im.resize((W // 2, H // 2)), (x, y))
        d.text((x + 10, y + 8), name, fill=(31, 29, 27))
    sheet.save(os.path.join(OUT, "_contact_2a.png"))
    print("contact sheet ok")
