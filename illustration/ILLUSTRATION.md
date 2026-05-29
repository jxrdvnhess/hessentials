# Hessentials — Illustration System

Our own illustration toolkit and the craft thinking behind it. The goal Jordan
set: stop being stuck in single-line work, and grow the ability to **illustrate
all of our visions** — line, tone, and bold value-mass design — in a register
that belongs to Hessentials. Everything here is programmatic synthesis
(PIL / NumPy), no diffusion. Jordan is the approval gate; the rubric in
`../drawing-style-study.md` still governs.

## The growth path

    line  →  tone  →  scratch-tone  →  pattern / notan  →  narrative

1. **Line** — the wandering blind-contour / illustrator line. Honest but
   abstract on its own.
2. **Tone** — form revealed by light. Volume, not just edges.
3. **Scratch-tone** — tone built *out of* line: thousands of massed short
   strokes, value by stroke density. The union of line and tone; a head
   emerging from a scratch field.
4. **Pattern / notan** — the arrangement of light and dark *masses*; the
   squint view; bold two-value shape design.
5. **Narrative** — flat masses plus story and the brand's sincere-irony voice
   (the romance-comic register: serious and slightly absurd at once).

Still ahead (Jordan's references point here): soft-focus / lost-edge tone,
chiaroscuro, and **figural** gesture — couples and embraces, hands, the body,
in economical line (Matisse/Schmitz) — i.e. beyond the single head.

## The one principle that unlocks the rest (the Form Principle)

A face — or anything — reads as alive and dimensional when a loose hand wanders
over **correct structure**, not when the line wanders at random and not when the
drawing is mechanically symmetrical. Construction underneath, living line on
top. This resolves the brand rubric's tension: *structure is allowed; mechanical
symmetry is the corpse.*

Form is revealed by light, organized into a small set of **grouped values**:

- light → halftone → **core (form) shadow** → reflected light → cast shadow

Rules we hold to: keep the lights together and the shadows together (mass them,
don't scatter them); never let reflected light get as bright as the lights;
limit the value set; and **control edges** — hard where planes meet sharply,
soft where the form turns, *lost* where the subject melts into the ground. The
big abstract arrangement of those masses is **Pattern**, and pushed to two
values it becomes **notan**.

Picture-making principles we lean on (proportion, placement, perspective,
planes, pattern) come from Andrew Loomis, *Creative Illustration* (1947), which
Jordan assigned as our text. The principles here are stated in our own words and
applied to our own tools — no reproduction of the book.

## Register / references (where we're growing to)

The Hessentials illustration register stays warm, restrained, melancholic, and
intimate — drawing on linen, value massing on linen, never cold or clinical,
never decorative wall-art. The growth targets Jordan pulled (2026-05-28):
high-contrast **notan** with figure-ground reversal (a figure, a hand at the
neck; two silhouettes interlocking via negative space), and the flat-mass
**romance-comic** panel whose "pretend to be sorry / pretend to forgive" line is
our sincere-irony voice almost exactly. Next edge beyond this commit: full-figure
notan built on negative space, and narrative panels.

## The toolkit

| module | what it does |
|---|---|
| `linen.py` | woven-linen ground; ink-on-linen compositing; stroke primitives; the wandering blind-contour face (`proc_face`) |
| `face.py` | the **construction-based** face — Simonetti/Loomis armature (three equal thirds, eyes one-eye-width apart) posed by **emotion controls**, then a living-line pass. `EMOTIONS` presets, `render()` |
| `tone.py` | **Form Principle** modeling (`render_tonal`) and two-value **notan** (`render_notan`) |
| `scribble.py` | **scratch-tone** portrait (`scribble_portrait`) — value field rendered as massed short strokes |
| `scene.py` | **scene** translation (`scene_scratch`, `scene_notan`) — re-draws an owned photo as scratch-tone / notan on linen; strokes follow the forms |
| `line_figure.py` | **confident-line** figures — charcoal-weight tapered strokes (`stroke`, `render`); proven on a single figure and a two-figure embrace. The register the brand is aimed at: economical, made, restrained |
| `construction.py` | **Stage 1 — construction & space.** A pinhole `Camera` (one ground plane / horizon / VP); forms built as 3D solids (`cuboid`) and projected through one camera so a figure and a doorway share one room. Kills the floating arch. |
| `gesture.py` | **Stage 2 — gesture & line of action.** A pose hung on one dominant line-of-action curve so the figure reads alive and specific, not a stacked armature. Gate: the 3-word-name test + `render_gesture(headless=True)` (the body carries the attitude head-covered). |
| `figure_construction.py` | **Stage 3 — figure construction.** The reclined-gazing-up gesture built into a believable body (Loomis masses): torso volume, real lap/back, limbs as weighted tubes, a propping arm — no sticks, no tangles — that stays alive head-covered (`reclined_body(hide_head=True)`). |

### The course (building the illustrator from the foundation, in causal order)

Each stage is a fundamental encoded as a procedure + a self-check, banked here as
it passes. 1 construction & space (`construction.py`) → 2 gesture / line of
action (`line_figure.py`) → 3 figure construction (Loomis masses) → 4 value &
light (restraint: light = bare linen, shadow = few soft masses, never mud) → 5
composition & master copies. Graduation: take one source and return a composed,
lit, alive, *made* illustration that holds the charge and breaks no doctrine.

### The line register (current direction)

The brand's figures are **economical made line** — few committed marks, real
weight, restraint (cf. Matisse / Boris Schmitz; never scratch-density, never
sterile vector, never traced from a photo). Hard rules, all learned the hard way:
line of action first (the body carries the gesture, not just the head); trust
the first confident mark — don't spline-sand it into grace (`stroke(smoothing=)`,
~0.5 bodies / ~0.8 limbs); crop or recede the lower body rather than fold it into
a column; the hand is downstream of the arm — weld it as one stroke-path; short
strokes are densified so fingers don't render as two dots; ends crop at full
weight (`cap_start`/`cap_end`), never fade; no cast shadow; home on warm linen.

### Emotion controls (`face.py` → `EMOTIONS`)

How we translate a word into a face: `gaze_down`, `lid_open` (low = closed /
serene), `brow_inner` (inner-brow raise = the sadness oblique), `mouth_curve`,
plus head `tilt` / `turn`. Presets exist for melancholy, serene, tender, pensive.

## Running it

    cd illustration
    python3 linen.py      # blind-contour line studies
    python3 face.py       # emotion strip + a "This is what stayed." close candidate
    python3 tone.py       # tonal heads (Form Principle) + notan studies
    python3 scribble.py   # scratch-tone portraits (tone built from massed line)
    python3 scene.py      # translate an owned photo scene into the drawn vision

Outputs land in `illustration/samples/`. Requires Python with PIL + NumPy.

## Status

Working capability, not finished art. Every image still passes through Jordan
(or Aurelian) against the brand rubric before anything ships. The current live
test is the homepage close slot — a linen face carrying *"This is what
stayed."* — pending Jordan's gate.
