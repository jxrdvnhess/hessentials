"""
THE BEST MAN — anatomy pass on the painter (2026-06-11, Jordan's
direction: lean into 101 / Loomis bodies; quietly sexy from behind).

Everything the course earned stays: the settled counterpose (v5), the
crane toward the work, the canonical head (face #3 lesson — never
lose the good head), economy where economy works. What 101 adds back
is STRUCTURE, placed by observation, not by rig:

  the V — shoulders ~2.4 head-widths over a drawn-in waist; the lat
      sweep is the single sexiest line a clothed back owns
  traps — the neck flares into real trapezius slopes; strong neck,
      not a stem
  the raised arm — deltoid, rolled cuff, then a BARE FOREARM tapering
      hard to the wrist (the croquis lesson: fabric vs skin behave
      differently; the taper is the tell)
  the back — one light spine furrow, one light blade-pull toward the
      working arm; evidence of muscle, never a diagram of it
  the seat — fitted trousers: thigh-calf S-curves, center seam, ONE
      light under-seat crease on the weight side; shape, not display
  legs — long, weight ankle under the neck pit, free heel a breath
      off the ground

Restraint note: sexy here = built and unbothered. The drawing flexes
nothing. He is just a man with a good back who isn't performing for
us — which is, per the whole record, exactly why it works.
"""


def best_man(cx):
    S = []
    def a(ctrl, w, lead=0.12, tail=0.18, swell=0.2, sm=0.65, cs=False, ce=False):
        S.append(dict(ctrl=ctrl, w=w, lead=lead, tail=tail, swell=swell,
                      smoothing=sm, cap_start=cs, cap_end=ce))

    # ---- HEAD — canonical, untouched ----
    a([(cx - 64, 200), (cx - 72, 142), (cx - 48, 80), (cx + 4, 60), (cx + 54, 78),
       (cx + 74, 144), (cx + 65, 198)], 2.4, swell=0.18)
    a([(cx - 52, 184), (cx - 20, 192), (cx + 16, 192), (cx + 54, 182)], 1.9,
      swell=0.1)
    a([(cx - 22, 88), (cx - 30, 128), (cx - 32, 168)], 0.9, swell=0.08)
    a([(cx + 16, 84), (cx + 22, 126), (cx + 20, 166)], 0.9, swell=0.08)
    a([(cx - 72, 156), (cx - 81, 174), (cx - 70, 190)], 1.4, swell=0.1)
    a([(cx + 74, 154), (cx + 84, 172), (cx + 72, 188)], 1.4, swell=0.1)

    # ---- NECK into TRAPS — strong, flared, asymmetric ----
    a([(cx - 26, 202), (cx - 30, 246)], 1.8)
    a([(cx + 27, 202), (cx + 32, 250)], 1.8)
    a([(cx - 30, 246), (cx - 98, 284), (cx - 158, 314)], 2.6, swell=0.16)   # raised side
    a([(cx + 32, 250), (cx + 102, 310), (cx + 170, 338)], 2.6, swell=0.16)  # dropped side
    # the fitted tee declares itself: collar arc + sleeve ends. The
    # anatomy stays under fabric — restraint is the seduction.
    a([(cx - 34, 240), (cx, 232), (cx + 38, 242)], 1.4, swell=0.08)         # collar, back
    a([(cx + 186, 428), (cx + 148, 438)], 1.0, cs=True, ce=True)            # sleeve end, right

    # ---- RAISED LEFT ARM — deltoid, elbow above the shoulder, rolled
    # cuff, bare forearm tapering hard to the wrist ----
    a([(cx - 158, 314), (cx - 200, 282), (cx - 222, 248)], 2.7, swell=0.2)  # upper, outer
    a([(cx - 126, 372), (cx - 168, 320), (cx - 190, 278)], 1.8, lead=0.2,
      swell=0.16)                                                           # upper, inner
    a([(cx - 224, 250), (cx - 196, 266)], 1.1, cs=True, ce=True)            # rolled cuff
    a([(cx - 222, 244), (cx - 208, 196), (cx - 190, 158)], 2.1, swell=0.26) # forearm, outer
    a([(cx - 188, 272), (cx - 176, 222), (cx - 166, 176)], 1.4, lead=0.22,
      swell=0.16)                                                           # forearm, inner
    a([(cx - 168, 158), (cx - 186, 152), (cx - 193, 138), (cx - 187, 124),
       (cx - 171, 121), (cx - 161, 133), (cx - 163, 150)], 1.6, swell=0.1)  # fist, round

    # ---- HANGING RIGHT ARM — deltoid bulge, long taper, easy hand ----
    a([(cx + 170, 338), (cx + 190, 430), (cx + 184, 560), (cx + 168, 690),
       (cx + 156, 758)], 2.4, swell=0.18)
    a([(cx + 128, 408), (cx + 150, 540), (cx + 146, 680), (cx + 140, 742)],
      1.6, lead=0.22, swell=0.14)
    a([(cx + 156, 760), (cx + 166, 786), (cx + 154, 802), (cx + 140, 786)],
      1.6, swell=0.1)

    # ---- TORSO — the V: lat sweep into a drawn-in waist, fitted shirt ----
    a([(cx - 126, 372), (cx - 114, 470), (cx - 90, 575), (cx - 96, 665),
       (cx - 102, 738)], 2.3, swell=0.18)
    a([(cx + 132, 400), (cx + 118, 500), (cx + 96, 592), (cx + 102, 672),
       (cx + 108, 742)], 2.3, swell=0.18)
    # evidence of the back, never a diagram of it
    a([(cx + 2, 332), (cx - 2, 460), (cx, 556)], 0.8, lead=0.3, tail=0.35,
      swell=0.06)                                                           # spine furrow
    a([(cx - 58, 356), (cx - 104, 330)], 0.8, lead=0.3, tail=0.35,
      swell=0.05)                                                           # blade pull
    # hem — tilted with the weight hip
    a([(cx - 104, 754), (cx + 2, 762), (cx + 108, 740)], 1.5, swell=0.1)

    # ---- TROUSERS — fitted; thigh-calf S; the seat has shape ----
    a([(cx - 104, 756), (cx - 114, 838), (cx - 100, 930), (cx - 86, 1070),
       (cx - 80, 1140), (cx - 90, 1248), (cx - 76, 1350), (cx - 62, 1458)],
      2.4, swell=0.18)                                                      # free leg
    a([(cx + 108, 742), (cx + 120, 824), (cx + 106, 916), (cx + 88, 1064),
       (cx + 82, 1136), (cx + 90, 1244), (cx + 70, 1350), (cx + 58, 1468)],
      2.4, swell=0.18)                                                      # weight leg
    a([(cx + 2, 766), (cx + 8, 880)], 1.2, tail=0.3, swell=0.08)            # seat seam
    a([(cx + 12, 1010), (cx + 16, 1462)], 1.8, lead=0.25, swell=0.14)       # inseam
    a([(cx + 38, 902), (cx + 82, 894)], 0.8, lead=0.25, tail=0.3,
      swell=0.05)                                                           # under-seat, once

    # ---- FEET — settled; free heel a breath off the ground ----
    a([(cx + 58, 1468), (cx + 76, 1494), (cx + 24, 1500), (cx + 18, 1476)],
      1.7, swell=0.1)
    a([(cx - 62, 1458), (cx - 88, 1486), (cx - 34, 1494), (cx - 28, 1466)],
      1.7, swell=0.1)
    return S


# pole grip, figure space
FIST = (-178, 138)
