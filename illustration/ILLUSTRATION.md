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
