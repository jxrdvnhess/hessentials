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
| `figure_construction.py` | **Stage 3 — figure construction.** The reclined-gazing-up gesture built into a believable body (Loomis masses): torso volume, real lap/back, limbs as weighted tubes, a propping arm — no sticks, no tangles — that stays alive head-covered (`reclined_body(hide_head=True)`). Believable-gate: proportion-in-heads / name-the-masses / squint human-not-insect. |
| `value_light.py` | **Stage 4 — value & light.** The built body in the lit room under one warm raking light: light = bare linen, shadow = a few big soft warm masses on the form. Gates (in code): light reads / no mud-no wedge / body survives head-covered. Carries the THREE GUARDS for honestly changing any lock. |
| `master_copy.py` | **Stage 5 — composition & master copies.** First copy: a Hammershøi-structured interior (figure from behind, quiet value, off-centre, active void) reconstructed in our marks — bones not trace. Composition lock: name-what-it's-about (off-centre decision) + active negative space (real lookspace, not leftover). |

### The course (building the illustrator from the foundation, in causal order)

Each stage is a fundamental encoded as a procedure + a self-check, banked here as
it passes. 1 construction & space (`construction.py`) → 2 gesture / line of
action (`line_figure.py`) → 3 figure construction (Loomis masses) → 4 value &
light (restraint: light = bare linen, shadow = few soft masses, never mud) → 5
composition & master copies. Graduation: take one source and return a composed,
lit, alive, *made* illustration that holds the charge and breaks no doctrine.

## Sketch 201 — Observation, Identity & Real Humans

101 taught construction (invent believable people). 201 begins where construction
ends: observe real people and read **why this body is this body**. Each unit is
banked as a procedure + its own gate, same as the 101 stages. The engine carries
over — the 101 graduation surface (superellipse-swept torso, sloping shoulders,
deltoid caps, limb volumes) — flattened to pure silhouette and given a **pose
layer** (arms/stance carry identity), plus a hip cap that closes the old
hip-to-thigh notch (load-bearing once the silhouette itself is the subject).

| unit | what it banks |
|---|---|
| **U1 — The Silhouette Test** (`loomis/sketch201_unit1.py`) | if every detail is removed, is the person still recognizable? **A1** our own 101 cast (youth/elder/bruiser/aristocrat/brooder) in pure black, each distinctly posed — cover the names, still nameable. **A2** twenty unlabeled ordinary people, each describable differently. **A3** the memory test, encoded honestly: the recalled figure keeps only the landmarks that survive a glance (overall mass, dominant posture, stance) and the reference is ghosted behind it so the gap reads — survived vs. vanished. Gate: nameable / describable-differently / the survived-vanished split reads true. **PASSED** (professor critique). A3 was strongest; its result — **posture and weight survive memory more reliably than exact proportions** — is a load-bearing principle for the course. |
| **U1 · A4 — Twenty Real Strangers** (supplemental) (`loomis/sketch201_u1_a4_rig.py` + `_a4_figures.py` + `_a4_plate.py` → `sketch201_u1_a4_strangers.png`) | **Source: Jordan's curated candid-photograph library** (`Sketch 201 Reference Library/`). Two attempts, and the gap between them is the unit's whole lesson. **Attempt 1 (rejected):** reduce each photo to its real outline by automated segmentation (OpenCV GrabCut) and composite that as final art. Result: blobs and camera-crops. Professor: *segmentation is extraction; observation is selection — you cannot outsource judgment.* A cropped shoulder or torso fragment is not a stranger. **Attempt 2 (the rebuild):** a posable 2D figure mannequin (`_a4_rig.py`) whose silhouette always reads as a human; each of the twenty is *posed by reading a real photo* — gesture from the joints, build from the limb radii — full-body photos only, the segmentation mask used as reference, never as art. Test per figure: remove the face, is it still a person? Gate: do the twenty read as twenty people or one person in twenty costumes? They read as twenty (walking / standing / seated / floor / crouch / recline / dance / reach / arms-raised). The deep lesson banked: **A computer asks which pixels are foreground; an illustrator asks what makes this person themselves.** 201 is the second question. |

| **U2 — Landmarks · A5 — Same Pose, Different Humans** (`loomis/sketch201_u2_rig.py` + `_u2_landmarks.py` + `_u2_a5.py` → `sketch201_u2_a5_samepose.png`) | the unit the A4 critique demanded: *what remains of identity when gesture is removed?* Ten ordinary standers, one frozen identical pose, same direction — **forbidden** to separate them by gesture / action / costume / props / face. Identity must come only from observed landmarks: proportion, weight distribution, shoulder slope, neck length, torso shape, hip structure, leg relationship, stance. The rig was rebuilt to kill the A4 accent — **sloped shoulders + a trapezius line instead of a flat bar with deltoid balls**, and every landmark driven by reading the photo, then validated crop-by-crop so differences stay observed, not invented. Finding: with pose stripped, real landmarks separate *most* people clearly (the stocky one, the slumped one, the V-taper, the lean-leggy two), but similar-build individuals (slim-average young men) blur to the finest landmarks — **standing is merciless; that residue is the true subject.** Height is not recoverable from mixed crops, so the read is proportional. |

| **U2 · A5 (revision) — Observation, no marks** (`loomis/sketch201_u2_a5_observations.md`) | the A5 plate failed (grade C): the ten standers were *ten descendants of one rig* — parameter variation (Arial Bold / Condensed / Light), not identity. Identity is **structural** variation; observation runs backwards — start from *this person*, discover "human" afterward. The standing pose became camouflage for the rig. Revision, by instruction: **no rig, no drawing, no silhouette** — observe ten standing strangers and write 25 factual landmark statements each (250 total): relationships, asymmetries, carriage, where clothing hides a landmark. Looking again *corrected* the earlier parameter-reads (jose is not "average + belly slider" — he is a large belly-forward bearded man; talha a long column; linkedin a forward diagonal; zachary a tipped-off-plumb folded lean). The point banked: **landmarks are relationships, not slider values — what sits ahead of what, what tips toward what, where the mass collects.** Next thing 201 teaches is not drawing — it is learning to see. |

| **U2 · A6 — Twin Strangers** (`loomis/sketch201_u2_a6_twin_strangers.md`) | A5-revision earned A-; the eye is now stronger than the system, so the next enemy is **assumption** — the category that makes a stranger disappear. Two young men interchangeable at thumbnail (slim, dark hair, dark open layered streetwear, candid): wassim (puffer/hoodie, standing) and nima (vest/shirt, mid-stride). 50 evidence statements each, **relationship-led not measurement-led** (per the A5 note: dimensions are one step removed from identity; relationships are where recognition lives). Part 1 — why they seemed one type (shared surface: age, slimness, dark open-shell-over-layer, urban candid; the label recognises instead of the eye). Part 2 — why they aren't (head-over-chest vs head-ahead-and-down; upright-moving vs settled-curling; hard small cropped head vs soft large curled head; fitted vest revealing the true frame vs puffer hiding it). Lesson banked: **the category is faster than the eye and usually wrong.** |

| **U2 · A7 — Three People Waiting** (`loomis/sketch201_u2_a7_three_waiting.md`) | A6 earned A; next study is **behaviour, not posture** — and the professor's escalation: ask *what is this fact doing?* not *what fact exists?* (object-inventory is low-value; relationship/behaviour is high). Three benchsitters all waiting: brock (reclined, leg crossed, hands laced at mouth — ease, watches time pass), dali (older, folds in around a propping hand, gaze off — withdrawal, the wait endured), podmatch (leans forward, elbows on thighs, feet planted — readiness, aimed at an expected arrival). 30 behaviour-led observations each. Answer banked: **waiting is empty time, so the action hides no one — identity is the relationship each body strikes with the blank, and its direction: outward / inward / forward (ease / withdrawal / readiness).** Behaviour outruns posture because posture is the shape a body takes, behaviour is what the person does with the situation that shape is in. |

| **U2 · A8 — The Same Room** (`loomis/sketch201_u2_a8_same_room.md`) | next subject is **presence** (a foundation of editorial illustration). Three people in the same type of space — a sunlit, plant-touched interior, each seated and attending to something: sweet (bowed into a laptop at a long bright table, faces the work not the windows), michael (leans back in an armchair, gazes *out* to the light, leaves the room open), jamie (bows over a phone, hemmed into a dense plant corner, folds inward). 30 evidence-first observations each (heeding the A7 note: let evidence force the reading, don't narrate ahead). Answer banked: **none moved any furniture, yet each is a different room — the occupant assigns the room its centre, tempo, temperature, and purpose just by sitting: workplace / repose / refuge. Presence is the field a body throws over a space — where it pulls the eye, whether it opens or closes the volume, what it silently makes the space FOR.** A figure in a scene tells the reader what the scene is for. |

| **U3 · A9 — The Ten-Second Stranger** (`loomis/sketch201_u3_a9_ten_second_stranger.md`) | Unit 3 studies **memory — what survives observation** (the discarded is often what matters; what survives memory is what reaches the drawing). Honest method given an AI's persistent context: encode a fresh stranger *once at gist-level size*, lock 50 statements (no hedging, gaps left empty), then re-open at full res only to compare. Result reproduced the predicted pattern **without assuming it**: composition + figure-to-room relationship + gross posture + tonal relationships survived intact; face, garment identity, chair type, local detail vanished. Two findings banked: **memory keeps relationships and discards identities** ("warm accent against dark jacket" survived, "cream cardigan" didn't); and **the one place memory lied instead of leaving a gap** — I wrote "knees close together" (unretained → mind supplied its default → wrong; knees are apart). The invention arrives in the same voice as the memory; catching it is the only defence. Directly trains [[the A8 correction]]: report only what remained. |

| **U3 · A10 — The Fading Stranger** (`loomis/sketch201_u3_a10_fading_stranger.md`) | A9 studied what survives one viewing; A10 adds a **real ≥24h cross-session decay** and watches what survives *consolidation*. A heavily muscular man holding a pineapple up to inspect it in a bright produce aisle: 20 immediate statements (Phase 2) → genuine session reset → 7 delayed items (Phase 4, from a one-line gist alone) → reopen + compare (Phase 5). The 7 delayed were a clean subset of the 20 — nothing spurious survived. What faded was **the staging** (orientation, the wall sign, front fruit bins, single-occupancy, skin-tone, brightest-object); four separate arm statements **merged** into one gesture (*holding it, raised, looking at it*). A10's trap is **attachment** — mourning the lost detail as the prize. But what memory protected was the act of **regard**: a huge built man giving his whole attention to one ordinary pineapple — the incongruity that *is* the picture. Banked: **forgetting was editing, and it edited toward the one true thing; trust the delayed memory to illustrate from — it already did the cut, arriving as a drawing where the immediate version is still a list.** |

| **U4 · A11 — The Last Three Things** (`loomis/sketch201_u4_a11_last_three_things.md`) | Unit 4 = **selection** (of what survives, what *deserves* to remain; the illustrator is an editor, not a camera; unit rule: nothing added, only removed; the enemy is *significance* — announcing importance before evidence earns it). Method: careful look, close, lock exactly **three** surviving elements, reopen, answer four. Subject: two old men on a marina bench, both eating heads-down over their own food, boats behind. The three held accurately. Findings banked: selection kept the **load-bearing structure (who / the one action / the place that explains them) and dropped every attribute**; the men survived as a **pair, not as individuals**; and a **relationship — together-but-separate — survived as one of the three elements in its own right.** Noted, not explained: the harbour stayed where A10's staging fell away — there location was navigation and left, here it is the reason and stayed. |

| **U4 · A12 — One Scene, Three Crops** (`loomis/sketch201_u4_a12_one_scene_three_crops.md`) | framing is the illustrator's greatest power. One photo (lean man shading his eyes on a sun-blasted dry hillside), three crops of the same frame: **what it IS about** (a person meeting hard light in a barren place — figure + shading hand + glare), **what it APPEARS to be about** (a fit shirtless body posed; setting as décor), **what disappears if the most important element is removed** (drop the eye-shading hand → the single action and the figure's relation to the light vanish; physique stays, event leaves; "a person under hard light" becomes "a man posing outdoors"). Observed, banked: the load-bearing element was **the smallest moving part (the hand), not the largest mass (the body)** — change the selection and the subject changes though the pixels barely do. (Heeds the A11 note: held to content/emphasis, kept off motive and meaning.) |

| **U4 · A13 — The Wrong Subject** (`loomis/sketch201_u4_a13_the_wrong_subject.md`) | framing creates assumptions; the illustrator's job is testing whether they're true. Three photos — common read vs actual subject, **defended only with visible evidence** (gaze, hands, orientation, what is lit, filled vs empty space; no psychology/motive/story). Muscular shopper (physique → the act of inspecting one pineapple); older man in a sunlit room (relaxing interiors → working with the room shut out); young man in an armchair (styled object → a figure turned to the window, room left open). Pattern visible across the three but left un-elevated: the "wrong" (surface) subject was the largest/most obvious element; the actual subject was **wherever the attention and the single action visibly go.** Heeds the A12 correction — claims kept to where content/attention sit, defended by frame evidence, not to meaning. |

| **U4 · A14 — The One Thing Missing** (`loomis/sketch201_u4_a14_one_thing_missing.md`) | editors change a picture by removing the unnoticed thing holding it together, not the obvious one. Three photos; remove an element that is **not** the person, the subject, or the largest object, then state what became *impossible* (evidence only). Three different connector types: the **harbour bench** (the only object touching both men → remove it and they can't read as a pair); the **sunroom table** (the surface the posture rests on → remove it and "working at a desk" can't be shown — laptop/hands/lean all depended on it); the **produce shelves** (the only marks of "store" → remove them and the act of inspection survives but "a shopper choosing fruit" can't be read). The connector is distinct from both the subject and the attention-commander — left as observation, not promoted. |

| **U4 · A15 — The Competing Subjects** (`loomis/sketch201_u4_a15_competing_subjects.md`) | many frames hold multiple valid subjects; the illustrator's task is often to **choose** among them, not discover the one. One photo (bearded man in hat/bow-tie/suspenders on a carved scrolled stone seat, plaster wall). Three claimants — the **man**, the **carved stone seat**, the **assembled wardrobe** — each given case-for, case-against, and the evidence that would force the call, on visible grounds only (mass, brightness, contrast, gaze line, what's cropped, what survives removal). Deciding evidence is **the crop**: tighten to the face → portrait; to the torso → clothing image; remove the man and the cropped stone doesn't survive as a whole. Strongest single claim = the man (only one that survives every crop that still reads complete), but the frame as composed genuinely shares the subject — **the subject is chosen, not found.** No winner forced (the assignment is the contest). |

| **U4 · A16 — The Image That Loses** (`loomis/sketch201_u4_a16_the_image_that_loses.md`) | selection is often **elimination**; understanding why the runner-up loses matters. Three photos, two genuinely strong subjects each, tie broken on **in-frame evidence, not crop** (heeding the A15 warning). Produce man vs the pineapple → pineapple loses on **dependence** (can't stand without the man; man stands without it). Lakebank figure vs the lake/treeline → landscape loses on **focus** (large area, no internal point; the figure is the only one). Man vs a saturated red field → red loses on **internal form** (intensity without shape; its one contour is on loan from the man). Closing (stated narrowly, not as doctrine): **the tie-breaker differed each time — independence / focus / form — there is no universal tie-breaker; the losing subject was strong in one currency and lost in another the specific frame made decisive.** |

| **U4 · A17 — The Illustration Choice** (`loomis/sketch201_u4_a17_illustration_choice.md`) | the course's selection discipline applied to real brand work: decide which illustration *deserves to exist*, not draw it. Article: Practice/"The single object you carry." Appears about *what to carry*; actually about **attaching a named decision to an object so the body recalls it through touch** (text: "what it is doesn't matter… the object is just where you parked the memory"). Three candidates — the object alone / a hand closing around it in the pocket / the full meeting scene. **Eliminated the object** (the article calls object-focus "aesthetic accessorizing," the error it corrects) and **the scene** (article forbids it: "don't talk about it… it's just for you"). **Survivor: the hand in contact** — the only image that depicts the practice ("the contact is the practice"), keeps the object incidental, and stays private; defended entirely from article lines. Selection by elimination, evidence = the text. |

Doctrine resolution (A4 settled it for the "real" units): units that need *real*
people require a real-observation INPUT. **ANSUR II was rejected** — it gives
proportions, not posture, so it answers a measurement question, not a recognition one;
and statistics are still abstraction, not a *stranger*. The honest source is Jordan's
real photographs, reduced by observation — synthesis posing as a captured moment stays
out. The same logic governs **Unit 6 (Reality)** and the **Final (Stranger Test)** ahead.
A1's "famous figures" was likewise resolved brand-clean: our own cast, never real named
public figures.

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
