# Sketch 301 — Assignment 34: Numeric Identity

As assigned, the confirm-or-collapse test: does enforcement belong specifically to
numeric-identity objects? Object family chosen to be **non-pip** so a positive result
confirms "numeric identity" broadly rather than "pip patterns only": the flagged
musical note (flag count IS the name — eighth = 1 flag, sixteenth = 2). The note also
has the defining numeric-identity property: you cannot add a flag while preserving the
identity, because the flag count is the identity.

## Materials

Filled notehead + stem + N flags:

- **a — control:** 1 flag (eighth note).
- **b — surplus:** 2 flags (a sixteenth note; "surplus" relative to the eighth).
- **c — deficit:** 0 flags (a quarter note).
- **d — salient violation:** 1 flag on the stem + a large detached flag floating to
  the right, off the note.

Fresh viewers, 1 Sonnet + 1 Haiku per image = 8 sessions. "What is it?" only.

## The record

| | actual flags | Sonnet | Haiku | flags reported | enforcement? |
|---|---|---|---|---|---|
| a eighth | 1 | "eighth note... a single flag" ✓ | "eighth note... a single flag" ✓ | 1, 1 | n/a |
| b surplus | **2** | **"an eighth note... a single flag"** | **"a single eighth note... a single flag"** | **1, 1 (deleted one)** | **YES — both cohorts** |
| c deficit | 0 | "a quarter note" (re-identified) | "a quarter note" | 0, 0 | re-identify, not invent |
| d salient | 1 + detached | "a quarter note... a separate gestural element / either a flag or..." | "an eighth note... a partial comma to the upper right" | territory: extra parked | extra read SEPARATE |

## Observations

1. **Enforcement RETURNED — on a non-pip numeric-identity object, in BOTH cohorts.**
   The two-flag image (a sixteenth note) was reported as a ONE-flag eighth note by
   both viewers. The surplus flag was deleted to fit the recruited identity. This is
   the die-five deletion, reproduced off the die, off pips, and — critically — NOT
   cohort-locked: both Sonnet and Haiku enforced. The model's surviving pillar
   (enforcement belongs to numeric-identity objects) gains its first POSITIVE
   confirmation beyond dice. The asymmetry the professor flagged is now resolved on
   the positive side: dice were not unique; pips were not the secret. The number
   being the name is.

2. **The cohort lock is NOT about enforcement-vs-not — it is about WHICH count.**
   A32/A33 converged because no enforcement happened at all; A34 converged WITH
   enforcement (both deleted the flag). So the A31 Sonnet/Haiku divergence under the
   quincunx was not "Sonnet enforces, Haiku doesn't" — both cohorts enforce a
   numeric identity when one is recruited. The earlier divergence must be re-explained
   (likely: the quincunx-over-six recruited the die-five for the Sonnet but a bare
   scatter for the Haiku — a RECRUITMENT difference, not an enforcement difference).
   This corrects my standing cohort-lock reading. (Carried, not yet retested.)

3. **Surplus deletes; deficit RE-IDENTIFIES — an asymmetry.** Two flags → "eighth,
   one flag" (delete down to the default identity). Zero flags → "quarter note"
   (re-identify to the matching identity; no flag invented). The system did not invent
   a flag to force an eighth on the quarter — it accepted the lower-flag identity. So
   numeric-identity enforcement is not symmetric: a SURPLUS is trimmed toward the
   recruited/default identity, but a DEFICIT is honored by switching to the identity
   that fits. (Consistent with the whole census arc: nothing absent is ever missed —
   the missing flag was not experienced as missing; it just made a different, valid
   note.) Possibly the deepest single result here.

4. **The salient detached flag was parked as a separate element — territory rule,
   fourth object family.** D: the floating extra flag became "a separate gestural
   element" / "a partial comma to the upper right," not a second flag on the note.
   The note kept its own flag count; the outsider stayed outside. The
   territory/salient-outsider rule has now transferred across dice (A31), traffic
   lights (A33), and notes (A34) — it is the robust, object-independent half of the
   model, about figure-ground catchment, not counting.

5. **Confound owned:** two flags stacked 34px apart are easier to merge perceptually
   than two separated dots, so part of b's "one flag" could be under-perception
   rather than identity-enforcement. But the report was not "two flags close
   together" or "a thick flag" — it was the NAMED identity "eighth note... a single
   flag," the recruited-identity's roster recited over the image. Recital-naming, not
   blur-merging, is the better read; the confound is logged, not dismissed.

## Explanations (held separately, tentative)

- The enforcement clause survives and is now confirmed positively: **a recruited
  configuration whose IDENTITY IS A COUNT (the number is the name) reports the count
  its identity demands — trimming a surplus toward the recruited identity, and
  honoring a deficit by switching to the identity that fits.** Dice, dominoes, and
  flagged notes qualify; traffic lights and polygons do not (their count is typical,
  not constitutive). The category "numeric identity" is real, not merely "pip
  patterns" — A34 was built specifically to separate those and it separated them.
- The surplus/deficit asymmetry suggests enforcement is really DEFAULT-RECRUITMENT
  plus the census arc's standing law: the viewer recruits the most available
  identity (eighth, the prototype flagged note; quarter, the prototype plain note),
  then the count follows that identity, and since absence is never experienced, only
  surpluses get visibly trimmed. The "enforcement" is the recital of the recruited
  identity's constitutive number — the same recital mechanism running since A10, now
  on an identity whose number is constitutive.

## Open questions

- The asymmetry, directly: an object whose DEFAULT identity is the high-count one
  (so a deficit would have to trim UP or invent) — does deficit ever invent a member?
  (A "sixteenth note" prototype with one flag shown — is it called a "sixteenth
  missing a flag" or re-identified to eighth?)
- Is the deletion in b really identity-recital or flag-merging? A version with the
  two flags widely separated (unmergeable) would isolate it — the cleanest follow-up.
- The cohort re-explanation (Obs 2): re-run the A31 quincunx-over-six and check
  whether the Haiku FAILS TO RECRUIT the die (counts six as scatter) rather than
  recruits-and-doesn't-enforce. This retires or confirms the corrected reading.
- With dice, dominoes(pip), and notes(non-pip) all enforcing, the model is now on
  firm positive ground — the remaining question is the LIMIT: is there a
  numeric-identity object that does NOT enforce, and if so what disqualifies it?

*No findings. The number that is a name kept its number — two flags became one because
the note they make has one, a missing flag made a different note rather than a broken
one, and a flag thrown clear of the stem stayed a thing of its own.*

---
Files: `generate.py`, `a_eighth.png`–`d_salient.png`, `_contact.png`. Sessions: 8
fresh viewers, 2026-06-04.
