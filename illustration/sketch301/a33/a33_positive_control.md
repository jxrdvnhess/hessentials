# Sketch 301 — Assignment 33: Positive Control

As assigned: does occupancy enforcement transfer to a second occupancy-bearing object?
Object family: the traffic light (identity "three lights"). Control + surplus +
deficit + a salient violation. The model predicts the die-five pattern returns — the
object enforces its roster of three, deleting a surplus and inventing a deficit.

## Materials

A traffic-light housing (tall rounded-rectangle, dark) with circular lights on a short
post:

- **a — control:** 3 lights. Correct occupancy.
- **b — surplus:** 4 lights inside the housing.
- **c — deficit:** 2 lights inside the housing.
- **d — salient violation:** 3 lights in the housing + a large, bright 4th light
  floating OUTSIDE it, lower-right.

Fresh viewers, 1 Sonnet + 1 Haiku per image = 8 sessions. "What is it?" only.

## The record

| | actual lights | roster predicted | Sonnet | Haiku | enforced? |
|---|---|---|---|---|---|
| a control | 3 | 3 | "three lenses" ✓ | "three lights" ✓ | n/a |
| b surplus | 4 | 3 | **"four... rather than the standard three" — counted 4** | **"four circular lights" — counted 4** | **NO** |
| c deficit | 2 | 3 | **"two lens openings" — counted 2** | **"two circular lights" — counted 2** | **NO** |
| d salient | 3 (+1 out) | 3 | "three lenses... a separate circle floating beside it" | "three... next to a blank circle" | housing kept 3; extra read SEPARATE |

## Observations

1. **The positive control FAILED to enforce — and it failed by REPORTING the
   violation, not absorbing it.** Four lights were counted as four (both cohorts, one
   explicitly flagging "rather than the standard three"); two were counted as two,
   with no third invented. The traffic light is occupancy-BEARING and was recognized
   as a traffic light, yet it did not force its count. The die-five enforcement did
   NOT transfer to a second object family. The model's one surviving pillar does not
   generalize on this test.

2. **The discriminator must be sharper than "fixed occupancy."** A traffic light's
   identity says "three," yet 2-light and 4-light traffic signals exist in the world,
   so "traffic light" TOLERATES a count range — and the viewer reports the actual
   number, flagging the unusual ones. The die-five does not tolerate a range: each
   die face IS a specific number; a "five" with six pips is not a five-with-extra,
   it is simply not a five. **Enforcement requires the COUNT to BE the identity, not
   merely to be typical of it.** The die-five (and each die face, and dominoes) are
   numeric-identity configurations; the traffic light is an object that has a usual
   count but survives violating it. A32's "fixed occupancy" was still too broad;
   A33 narrows it to "the number is the name."

3. **The salient-violation cell behaved exactly like A31's far outlier — and confirms
   that finding off the die.** With the extra light placed OUTSIDE the housing, both
   cohorts kept the housing's three intact and read the fourth as a separate object
   ("a separate circle floating beside it," "next to a blank circle"). The schema's
   territory protected its members; the salient intruder outside the catchment was
   neither deleted nor counted into the object. This is A31-d replicated in a new
   object family: a surplus outside the schema's bounding region is parked as a
   separate thing, not enforced against. So one half of the model — territory and
   the salient-outsider rule — DID transfer, even though roster-enforcement did not.

4. **Full cohort convergence again — 8/8.** As in A32, with no numeric-identity
   schema in play, Sonnet and Haiku agreed on every count. The cohort lock has now
   been absent in both post-die assignments and present only under die-faces. This
   tightens the A32 thread to a near-claim: **the cohort divergence is the signature
   of numeric-identity-schema recruitment specifically** — not occupancy, not
   recognition, not arrangement. Where the number is the name and one cohort enforces
   it, they split; everywhere else they converge.

5. **"Standard three" is the recital, observed directly** (b/Sonnet): the viewer
   stated the canonical occupancy ("the standard three") AND the actual count
   ("four") in one breath, holding both without conflict. The object's typical
   roster is available as KNOWLEDGE without being enforced as a COUNT — the cleanest
   separation yet of "what the object usually has" from "what this image shows." The
   die-five never offers that separation because its standard count and its identity
   are the same fact.

## Explanations (held separately, tentative)

- The census model's enforcement clause is now: **a recruited configuration enforces
  a count only when that count is constitutive of the configuration's IDENTITY (the
  number is the name) — die faces, dominoes, named pip-patterns. Objects with a
  typical-but-violable count (traffic lights, hands, the polygon "forms" of A32) are
  recognized and then tallied honestly, with the canonical count available as
  unenforced knowledge.** This survived a genuine transfer attempt and a positive
  control that failed — the failure is what sharpened it. (Held; it now rests on
  one positive family, dice, and two negatives, polygons and traffic lights — the
  asymmetry the professor warned about persists, but the POSITIVE side is the one
  still unconfirmed beyond dice.)
- The salient-outsider rule (territory protects members; an outside surplus is parked)
  transferred cleanly to the traffic light, suggesting it is the more general,
  object-independent half of the A31 result — it is about figure-ground catchment,
  not about counting.

## Open questions

- The still-missing positive: is there ANY second numeric-identity configuration that
  enforces like the die? Dominoes are the obvious candidate (a domino half's pip-count
  IS its name) but are dice-adjacent. A non-pip numeric-identity object — a "peace
  sign" (3 segments), a "quaver vs semiquaver" (beam count) — would be the real
  second pillar. If none enforces, "enforcement" may be unique to pip-patterns, and
  the whole roster story shrinks to a curiosity about dice.
- Does the die-five enforce for the HAIKU at all (the A32 sharpest thread, still open)?
  If enforcement is Sonnet-only even for dice, then "numeric-identity enforcement" is
  really "one cohort's pip-pattern habit," and the model is a cohort fact wearing a
  perceptual costume.
- The "standard three" separation (Obs 5): can a viewer be made to ENFORCE the
  canonical count — does any framing make "traffic light" delete the fourth light?
  (Probably a question-change; flagged.)

*No findings. The traffic light was a traffic light with four lights, and everyone
said so — because a traffic light can have four lights, but a five cannot have six
pips, and that gap is the whole phenomenon.*

---
Files: `generate.py`, `a_three.png`–`d_salient.png`, `_contact.png`. Sessions: 8
fresh viewers, 2026-06-04.
