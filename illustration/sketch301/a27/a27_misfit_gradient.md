# Sketch 301 — Assignment 27: Misfit Gradient

As assigned: does census behavior change gradually as fit degrades? Radial
organization, five elements, satellites fixed; only the central blob moves off the
satellites' centroid in four doses: 0, ~36, ~72, ~108 px (the last at the hull's
edge, never pairing with a satellite).

## The record

| | offset | Sonnet count | Haiku count | organization reported |
|---|---|---|---|---|
| a perfect | 0 | 5 ✓ | 5 ✓ | "one larger **central** dot surrounded by four" / "larger one roughly in the **center**" — radial, clean, 2/2 |
| b slight | ~36 | 5 ✓ | 5 ✓ | "one noticeably larger dot **near** the center" / "larger in the center, others around it" — radial, 2/2, first hedging |
| c moderate | ~72 | 5 ✓ | 5 ✓ | S: "largest sits roughly in the **center-right**... others clustered loosely **around it**" — radial held, displacement NAMED. H: structure dropped — full position-by-position enumeration, "no obvious symmetry or geometric order" |
| d severe | ~108 | 5 ✓ | 5 ✓ | S: **re-platformed** — "two roughly equal small dots on the left arranged vertically, and on the right a larger dot at the top with two smaller below" (an accurate 2+3 of the actual layout). H: strained radial held — "large circle in the center-right, four smaller around it" |

## Observations

1. **The census was perfect at every dose — 8 of 8.** No phantom appeared anywhere on
   the gradient. Misfit, dosed along this axis, produced zero census error.

2. **What degraded was not the count but the CLAIM.** The gradient is in the
   organization column: clean radial → radial-with-hedge ("near the center") →
   radial-with-named-displacement ("center-right... around it") → either structure-
   free enumeration (H, moderate) or re-platforming to the organization that
   actually fits (S, severe: an accurate 2+3). Claims were FLUID along this axis —
   no viewer held the radial against a field that had stopped supporting it. They
   renamed, enumerated, or switched. Sudden vs gradual, answered: claim-revision was
   gradual; census behavior was flat.

3. **A design limitation, discovered by the data and owned:** the radial claim's
   roster — one center plus N satellites — is COUNT-FLEXIBLE. It cannot dictate a
   census, because 1+4 totals five however strained the center's position. This
   gradient was structurally incapable of producing roster-driven error. The claims
   that have produced errors (pairs → 4; 4+4 symmetry → 8) have FIXED arithmetic.
   The dose-the-misfit experiment, run on the right claim, is a PAIR gradient — a
   2+2 field with a fifth element moved gradually in from the margin. Not run; now
   the obvious next cell.

4. **Severe misfit improved accuracy.** The S viewer's 2+3 at the severe dose is the
   truest structural description that arrangement received — the imposed claim
   failed and the page's actual organization surfaced. Misfit, when claims are
   fluid, is self-correcting: the field gets re-read until something fits. (The
   sticky cases — A26's pairs, A21/A25's loose orbit — are now the anomaly needing
   explanation, not the rule.)

5. **The mid-gradient enumeration (H, moderate) is the candidate-zone behavior
   again** — structure declined, members listed one by one, the census exact — the
   same near-abstention register that appeared mid-ladder in A21 and on the
   uniform scatter in A26. Where no claim has won, description does the counting,
   and counts well.

## Explanations (held separately, tentative)

- The record's census events now sort under two requirements, both necessary: a
  claim with FIXED ARITHMETIC (pairs, symmetric patterns — not radial, not
  constellation), and STICKINESS — the claim held despite global misfit, either
  because it is locally confirmed (A26's two clean-looking pairs) or because no
  better claim is available (A21/A25's loose orbit over a hierarchical scatter).
  Fluid claims revise; sticky claims collect. This gradient dosed misfit on a claim
  that was both arithmetic-free and fluid — hence eight clean censuses.
- If stickiness is real, the +1 scatters and the −1 pairs are the same event with
  different rosters, and the path to dosing the phantom is dosing STICKINESS, not
  offset: make the locally-confirming sub-structure stronger while the global fit
  worsens.

## Open questions

- The pair gradient (Obs 3): 2+2 plus a fifth element walked in from the edge — at
  what distance does the fifth join a pair's reading, become a third group, or
  vanish into the −1?
- Can stickiness be measured independently of its census effect (hedge-density
  again? the sticky A26 pair-reading was hedge-free; the fluid revisions here
  hedged)?
- H held a strained radial at severe offset where S re-platformed — the cohort that
  never miscounts is also the cohort that revises LESS. The lock may be about
  revision policy, not richness. (Cuts against my A25 explanation; both candidates
  now live.)
- Does claim-fluidity itself depend on the available alternatives — was the severe
  cell's accurate 2+3 only possible because the layout offered it?

*No findings. The misfit never reached the census — it spent itself on the claim,
which bent, renamed, and finally stepped aside; the phantom needs a claim that
won't.*

---
Files: `generate.py`, `a_perfect.png`–`d_severe.png`, `_contact.png`. Sessions: 8
fresh viewers, 2026-06-04.
