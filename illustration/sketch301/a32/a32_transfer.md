# Sketch 301 — Assignment 32: Transfer

As assigned, attacking the model's weakest point: does a recruited schema enforce its
own roster regardless of roster size? Geometric polygon schemas (triangle = 3-slot,
hexagon = 6-slot), each with a surplus and a deficit. The model predicts the count
tracks the SCHEMA's roster, not the page (triangle → 3, hexagon → 6).

## Materials

- **a — triangle + surplus:** 3 vertices of a triangle + a dot near the centroid =
  4 elements. (Roster 3, surplus 1.)
- **b — triangle deficit:** 2 of 3 triangle vertices = 2 elements. (Roster 3,
  deficit 1.)
- **c — hexagon deficit:** 5 of 6 hexagon vertices = 5 elements. (Roster 6,
  deficit 1.)
- **d — hexagon surplus:** 6 hexagon vertices + a center dot = 7 elements. (Roster 6,
  surplus 1.)

Fresh viewers, 1 Sonnet + 1 Haiku per image = 8 sessions. "What is it?" only.

## The record

| | actual | roster predicted | Sonnet count | Haiku count | schema reported |
|---|---|---|---|---|---|
| a tri+surplus | 4 | 3 | **4 ✓** ("triangle... one in the middle") | **4 ✓** | "triangle/diamond pattern" — but counted 4 |
| b tri deficit | 2 | 3 | **2 ✓** ("the 2-pip face of a die") | **2 ✓** | two dots; no third invented |
| c hex deficit | 5 | 6 | **5 ✓** ("loose circle") | **5 ✓** | circle/ring of five; no sixth invented |
| d hex surplus | 7 | 6 | **7 ✓** ("center + six around") | **7 ✓** ("heptagon / seven-pointed") | hexagon-with-center; no deletion |

## Observations

1. **Transfer FAILED — cleanly, 8/8.** Not one viewer enforced the polygon's roster.
   Every count matched the actual element number; no surplus deleted, no deficit
   invented, across both roster sizes and both cohorts. The prediction "schema fixes
   its own number" did not survive transfer off the die-five. **This is the failure
   the A31 verdict asked for, and it localizes the overfit precisely.**

2. **The triangle and hexagon were RECOGNIZED but did not COUNT.** Viewers named the
   shapes — "triangle pattern," "loose circle/ring," "hexagon with a center" — and
   then reported the true element count anyway, including the intruder ("triangle...
   one in the middle" = 4) and the missing vertex ("loose circle" of 5, not "ring
   of six minus one"). Shape-recognition and roster-enforcement are different events;
   the polygons delivered the first without the second.

3. **The discriminating property is FIXED OCCUPANCY, not recognizability.** The
   die-five enforced its roster (A30, A31) because a die's 5-face has, BY DEFINITION,
   exactly five pips — its roster is constitutive. A triangle is a shape three dots
   can make, but "triangle" does not forbid a fourth dot inside it; "a ring" does not
   forbid a center; "six around" tolerates a seventh. Polygon schemas name a FORM,
   which is occupancy-indifferent; die/domino schemas name an OBJECT WITH A FIXED
   PART-COUNT. Roster enforcement transfers only to the second kind. The professor's
   A30 phrasing was the correct one all along — "a finite object with KNOWN
   OCCUPANCY" — and my looser word "schema" was the overfit.

4. **The model survives, narrowed.** A31's factorization stands where it was earned —
   over a known-occupancy schema. Its scope clause is now explicit: the count tracks
   the recruited structure's roster ONLY WHEN that structure carries a fixed,
   constitutive part-count. Recognizable form alone does not enforce a roster.
   "Schema" splits into two kinds, and only one counts.

5. **Cohort lock did not even engage.** With no roster-bearing schema available, the
   Sonnet's relational-surplus mechanism had nothing to enforce, so both cohorts
   counted the page — 8/8 agreement, the first full cohort convergence in the census
   arc. The lock appears only when one cohort recruits an occupancy-bearing schema
   and the other doesn't (A30-c, A31). No occupancy schema, no divergence. This is
   strong indirect support for the narrowing: the cohort split IS the
   roster-enforcement signature, and it vanished exactly where roster-enforcement was
   predicted to vanish.

## Explanations (held separately, tentative)

- The census model now reads, with the A32 scope clause folded in: **a recruited
  structure with a constitutive part-count sets the reported count to that count;
  the field's attention landscape places the resulting surplus/deficit; structures
  that name only a form do not set a count, and their elements are tallied directly.**
  The die-five and domino are constitutive-count objects; triangle, ring, hexagon,
  constellation, "cluster" are forms. A21–A29's +1/−1 came from forms that
  IMPLIED an arithmetic (pairs imply even, equal-clusters imply balance) without a
  constitutive count — a third, weaker category: forms with a numeric BIAS but no
  fixed roster. Possible three-way split: constitutive count (enforced) / numeric
  bias (drifts) / pure form (tallied). Offered, not promoted — A32 only firmly
  establishes the first vs the rest.
- Why "two dots" recruited the die-2 (b) but didn't enforce anything: the viewer
  named the die-2 face as a SIMILE ("like the 2-pip face") after counting two — the
  object was retrieved by the count, not the count by the object. Naming-after is not
  recruitment-before. (Consistent with A19's badge-not-analysis.)

## Open questions

- The cleanest confirmation of the narrowing: a SECOND constitutive-count object
  (domino-six, or the 6-pip die-face) over a mismatched field — does roster
  enforcement reappear the moment occupancy is constitutive again? (Predicts yes;
  the positive control A32 lacks.)
- The three-way split (Obs / Expl): is "numeric bias" real — does a pairs-form
  reliably drift toward even counts while a triangle-form does not? A matched
  bias-vs-form pair would test it.
- Does the die-five even enforce its roster for the HAIKU, or only the Sonnet? (A31
  showed Haiku counting the true six under the quincunx — so occupancy-enforcement
  may itself be cohort-specific, which would fold the whole roster story back into
  the cohort-lock question.) This is now the sharpest loose thread.

*No findings. The polygons were recognized and then counted honestly — roster
enforcement did not travel, because a shape is not an object, and only an object with
a fixed number of parts can tell a viewer how many things to see.*

---
Files: `generate.py`, `a_tri_surplus.png`–`d_hex_surplus.png`, `_contact.png`.
Sessions: 8 fresh viewers, 2026-06-04.
