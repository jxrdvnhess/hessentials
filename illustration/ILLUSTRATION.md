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

| **U5 · A18 — The Attention Shift** (`loomis/sketch201_u5_a18_attention_shift.md`) | Unit 5 = **meaning / what the frame does to the viewer**; new concept: **attention has a cost** — every element that gains attention takes it from something else. Unit rule: no beauty/style/aesthetics. One photo (shirtless man on a dry hillside). First noticed = the **sunlit torso** (brightest, central, highest contrast, only vertical mass); second = the **patterned swim shorts** (only high-chroma hard-edged block); remove the torso → the **arid hillside** resolves as the real setting (present but unlooked-at); hard to notice *because* the torso dominates = the **raised shading hand/sunglasses (the only action)** and the **landscape's character** — both low-contrast, off-center. Banked: **the bright center buys instant legibility and pays by suppressing the gesture and the place — attention on the body is attention not spent on what it does or where it is.** Good illustrators ask not only what to show but what they're preventing the viewer from seeing. |

| **U5 · A19 — The Viewer Who Arrives Second** (`loomis/sketch201_u5_a19_viewer_who_arrives_second.md`) | images aren't received all at once — they unfold; the new concept is **sequence**. Photo: two old men on a marina bench. First = two men **together** on one bench (a pair); second = each **head-down over his own food, neither turned to the other** (separate). Understanding only after both: **co-presence without exchange.** Impossible from the first alone: the separateness (a pair reads as connection by default). Possible only after the second: proximity-without-interaction. The Unit-5 consequence (where A18 stopped short): **order makes the meaning** — because "together" lands first, the separateness reads as parallelism *within a pair*; reverse the order and the same two facts read as "two strangers sharing a bench." Identical evidence, opposite image; meaning is in which element the frame delivers first. (Recurring, noted not theorized: attention and subject keep separating.) |

| **U5 · A20 — The Image That Lies** (`loomis/sketch201_u5_a20_the_image_that_lies.md`) | ordinary photos that quietly produce a wrong first reading; verdict = did the image lie or did the viewer rush. Photo: a man reclined on a grassy lakebank, barefoot — **holding a phone up, looking at the screen.** Encouraged belief = *unplugged escape in nature* (loud cues: water/trees/grass/barefoot). Complicating evidence = the centrally-held phone and the gaze fixed on it; attention is on the device, the landscape unregarded. Verdict: **the viewer arrived too quickly — nothing is hidden;** the frame asserts only "a person by a lake," and the "present in nature" part was supplied by the viewer. Banked: **the false reading is a sequence effect** — the loud setting is seen first and installs the belief before the small grey phone arrives to overturn it; same attention-vs-subject split (setting vs where the man's attention goes). |

| **U5 · A21 — The Cost of Being Right** (`loomis/sketch201_u5_a21_cost_of_being_right.md`) | not which reading is correct, but what disappears when correctness arrives. Photo: man in an armchair, gaze turned to a bright window, in a warm room (room = most of the frame). Most accurate = **a figure turned to the window** (a vector: face→glass); less-accurate-but-common = **a man in his living room** (a volume: the whole interior as the scene). Lost when accuracy replaces it: **the room as content** — naming the gaze-vector demotes the plant/walls/floor/open space (the majority of the image) to "around him," though none of it left the frame. Banked: **accuracy ≠ completeness — the most accurate reading can be the narrowest; correctness trades a volume for a vector.** Mirror of A20 (loose read drops the small true thing; accurate read drops the large true thing — both weighting failures, opposite directions). |

| **U5 · A22 — The Thing That Changed Jobs** (`loomis/sketch201_u5_a22_thing_that_changed_jobs.md`) | separate the **most obvious element** from the **organizing element** and name each one's **function** (not importance/subject/meaning). Photo: man leaning to a laptop at the near end of a long table that recedes into a bright window wall. Obvious = **the man** (only figure, near, local-contrast peak — seen first); organizing = **the table** (the receding line that builds depth, carries every object, partitions the frame, places the man at its end). Not the same. Jobs: the man = **focal mass / terminus** (the eye lands and rests; organizes nothing); the table = **structural spine / route** (builds the space, aligns everything, *delivers* the eye to the focal mass). Banked: **the element carrying the structure can sit entirely apart from the element carrying the eye** — A21's correction made concrete (reorganization, not disappearance; obvious ≠ organizing). |

| **U5 · A23 — The Element Nobody Notices** (`loomis/sketch201_u5_a23_element_nobody_notices.md`) | find the **structural** element that quietly fails if removed — not subject/largest/brightest/focal. Photo: man walking toward camera on a pedestrian bridge, thin railings converging back into autumn trees. Mentioned = the man; overlooked = **the railing lines** (the converging perspective edges). Job: build the depth corridor, fix the figure's position in depth, establish the surface as a raised edged walkway; remove them and the deck flattens, recession weakens, the bridge read goes — the man remains, the space doesn't. Why overlooked: low/thin/low-contrast at the sides, out-competed by figure + bright trees; and **even when seen it's read as "a railing," not as the lines doing the depth-work — the function hides inside the literal object.** Banked: structural labor = the viewer consumes the result and never inspects the cause. |

| **U5 · A24 — The Thing Doing Two Jobs** (`loomis/sketch201_u5_a24_thing_doing_two_jobs.md`) | one element, two simultaneous functions (labor, not meaning). Photo: man perched on a carved stone block, rising right against a plain wall. Element = **the carved stone**. Jobs: **attractor** (brightest/highest-contrast/only sculptural form — a second pole the eye goes to) + **structural support & counterweight** (the seat that sets his pose and weights the lower-left to balance the right-rising figure). How both: **surface** (bright/carved) does the attracting, **mass+position** does the supporting — they coincide in one object. Break test: keep only the attractor → he loses his seat, balance tips right; keep only the support (dull seat) → lower-left loses its pole, frame settles to one pole on the figure. Banked: the two jobs are **separable in principle but fused in the object**; an element's surface and its mass can do different labor at once. |

| **U5 · A25 — The Necessary Mistake** (`loomis/sketch201_u5_a25_necessary_mistake.md`) | the wrong first reading isn't failure — *why is the viewer wrong first?* Photo: man reclined by a lake **on his phone** (lake/phone, completing the A20 arc). First reading = nature escape (loud foreground setting); surviving reading = a man looking at his phone, landscape unregarded; why first = size/contrast force the big bright nature before the small grey phone. **The job the mistake performs:** it installs the "immersed in nature" premise the phone then contradicts — the violation (gap between where the body is and where attention goes) is the image's actual content. Skip to "a man on his phone" and the lake collapses to backdrop, the tension never forms — the phone needs something to puncture, and the first reading is what it punctures. Banked: **the viewer is wrong first so that being right second can mean anything;** A20's "rush" reframed as the image's mechanism. (Kept tentative: the *order* is forced by visible weighting; what each viewer concludes I don't claim to measure.) |

| **U5 · A26 — The Honest Shortcut** (`loomis/sketch201_u5_a26_honest_shortcut.md`) | viewers don't all spend the same time; the image must survive a glance and a stare. Photo: man bowed over a phone in a plant-dense, sun-warmed corner. **Fast reading** = a figure enveloped by greenery in warm light (the whole, grasped at once); **complete reading** = a man bowed over a phone, hemmed in by plants, absorbed. Fast gets right: the **true envelopment** (plants on several sides, figure within) — accurate, not careless. Complete loses: the **openness** of that surround — once the bowed-phone + plants-as-enclosure register, the green stops being a place one is openly *in* and becomes an enclosure pressing around an absorbed figure; precision dilutes the immediate whole. Banked (no winner): **the shortcut is honest because what it grabs is genuinely there; the long look is not superior, only later — two true things at two durations.** (Heeds A25 caution: name what each duration receives, don't rank.) |

| **U5 · A27 — The Illustration That Survives** (`loomis/sketch201_u5_a27_illustration_that_survives.md`) | **observation turning back into image-making.** Run the A10 residue test on a Hessentials article ("What the Cows Know"). Residue: 1-min = cows-lying-in-a-field + two-ways-of-knowing + the human examples; 1-hour = the cows + "your body knows first"; next-day = just the field of lying-down cows carrying the whole point. Three illustrations matched to the three layers (a doorway-body-flag / the herd under a heavy storm sky / the bare lying-down herd). **Survivor across all three = the bare herd lying down** — defended from structure not taste: the cows are the only concrete image and they **bookend** the piece (open line 9, close 33–35, named through-line line 29); abstractions/inventory fade first, the concrete bookending carrier persists. The doorway serves only the immediate layer; the storm sky over-specifies (rain is the *explanation*, not the residue). Practical brand note: for this article, illustrate the lying-down herd, minimal — concrete/observed, not a symbol of "intuition" ([[feedback-refuses-to-signify]]). |

| **U5 · A28 — The Illustration That Fails** (`loomis/sketch201_u5_a28_illustration_that_fails.md`) | good illustrations fail more often than bad ones — bad ones are easy to reject, good ones are dangerous. Same article ("What the Cows Know"); three *tempting* failures, each diagnosed (why chosen / residue ignored / what it explains the article never shows): **head-gut duality** (diagrams the mechanism the text de-mystifies — "nothing mystical… the first five"); **the charged doorway** (stages a threat the text withholds — "the override doesn't produce catastrophe"); **birds fleeing a storm** (dramatizes the weather, which A27 flagged as the *explanation* not the residue). Shared fault, banked: **the dangerous illustration explains or dramatizes (the argument / the peril); the durable one shows the plain observed thing** the article keeps returning to. Directly operational for brand illustration ([[feedback-refuses-to-signify]]: illustrate what was seen, not the meaning). |

| **U5 · A29 — The Detail That Earned The Frame** (`loomis/sketch201_u5_a29_detail_that_earned_the_frame.md`) | ten concrete details from the cows article; pick the one that survives **longest pressure** (not dramatic/symbolic/beautiful). Winner = **the cows lying down — the posture, almost the whole herd settled in the grass.** Why not the nine: the **bodily/internal ones** (shoulders tighten, stomach drops, the override) aren't visible — they need the prose or collapse into generic drama; the **dramatic one** (birds before the hurricane) dramatizes the weather/explanation (A28 trap); the **context** (the drive, roadside, bare grass) carries nothing alone. The work it alone performs: it is **simultaneously fully visible AND already the article's claim** (an animal's posture standing in for "the body reads before the mind names"), needing neither caption nor storm. Kept attached to this article per the A28 caution (not promoted to a rule). |

| **U5 · A30 — The First Mark** (`loomis/sketch201_u5_a30_cows.png` + `_a30_cows.py` + `_a30_first_mark.md`) | first image-making of Unit 5: draw **only** the A29 detail — a herd of cows lying down in a field — plain filled silhouettes on warm paper, recumbent bodies, heads up, one faint far edge; no atmosphere/weather/symbolism/cleverness (a made drawing). Three answers: **gained** = the residue becomes an external, glance-legible object + drawing *forces commitment* the prose never had to make (count, facing, posture); **lost** = the words' openness ("every reader's herd" → one herd), the article's *claim* (meaning doesn't travel with the image, and mustn't try), and neutrality (my hand enters — the plain image still isn't neutral); **what changed** = the fact **acquired a viewer** — it re-enters every Unit-5 system (first/second, focal, structure, sequence, wrong-first) that didn't apply to a sentence; and the **selection→execution seam** crossed (provisional choices became fixed). Observation asked *what is true*; the image now asks *what does a viewer do with this.* |

| **U5 · A31 — The Same Cow, Ten Times** (`loomis/sketch201_u5_a31_cow_studies.png` + `_a31_cow_studies.py` + `_a31_same_cow_ten_times.md`) | the A30 diagnosis fixed: my cows were *symbols*, not observed. Drew a resting cow 10× from 10 **real photographs** (Unsplash "cow lying down," observed live via Claude-in-Chrome screenshots/zoom). Goal = observation (not beauty/recognition). What the photos corrected (vs A30's symmetric loaf): weight on the **brisket**; **near foreleg folds forward** to a hoof; **hind legs tuck to one side** (asymmetric, lies on one hip); topline is **two masses (withers + high hip, loin dip)** not a dome; **short low neck + forehead-and-muzzle head**; **big side ears** (not top-triangles); a **dewlap**; breed silhouettes (zebu hump, Highland horns/shag, Holstein bony hip). Ten genuinely differ because real resting cows differ. Banked: **selection found the cow survived; this is the first work that went and looked at what survived — execution needs observation, not just the right detail.** Browser is a usable reference path when the library lacks the subject. |

| **U5 · A32 — The One Cow, Ten Ways** (`loomis/sketch201_u5_a32_one_cow.png` + `_a32_one_cow.py` + `_a32_one_cow_ten_ways.md`) | hold one cow constant (the A31 zebu calf), draw it 10× through 10 lenses — **mass / outline / weight / balance / joints / negative space / major volumes / directional flow / posture / fewest marks** — built from ONE shared model. Depth, not variation. Directly answers the A31 note (parts → **relationships**): the volume/flow/balance/joint lenses only work by seeing how forms connect (head→hump→barrel→hindquarter as one chain; one arc muzzle-to-hip; CoG carried by the base; resting = acute joint *flexion*, not relaxation). Findings: weight sits back-and-low while the head cantilevers light; the pose is legible from its negative pockets; five marks identify it. Banked: **one cow contains ten — mass/weight/balance/volume/flow are not one statement seen twice but different true things about the same animal.** Left open (per critique): richer rendering would deepen it — the silhouette was my *use* of the medium, not its ceiling. |

| **U5 · A33 — The Cow That Disappears** (`loomis/sketch201_u5_a33_cow_vanishes.png` + `_a33_cow_vanishes.py` + `_a33_cow_that_disappears.md`) | same zebu calf, **removal only**: 10 line drawings, strictly fewer marks each (12→3), to the minimum that preserves *this* calf, not "a cow." Collapsed first = **locating/finishing/secondary detail** (ground, muzzle, dewlap, far ear, belly line); survived longest = **relational marks** (the humped back-arc — the single connected topline/gesture from A32's flow lens — and the folded foreleg). Findings: the **"this cow / a cow" line runs through the hump** — one small deflection in one arc carries the breed; the **big ear stands in for the whole head** once the head-tilt drops. Minimum = humped arc + big ear + folded foreleg (zebu + resting). Banked: **under reduction, relationships and one breed-specific deviation survive; the catalogue of parts collapses.** (Stated as evidence from this reduction, not a law — and deliberately *not* over-strengthened, per the recurring critique.) |

| **U5 · A34 — The Wrong Reduction** (`loomis/sketch201_u5_a34_wrong_reduction.png` + `_a34_wrong_reduction.py` + `_a34_the_wrong_reduction.md`) | the control for A33: same calf, same 12 marks, removed in the **wrong order** — destroy carrying **structure** first (back-arc, foreleg, belly-ground, rump, neck), protect **details** (ear, dewlap, muzzle) to the end. Removing the back-arc *first* wrecks it immediately (a head with dangling parts, no body); the detail-only end (ear+dewlap+muzzle) reports nothing and **misleads** (dewlap-curve reads as a "V"/beak, the cluster as a small bird). **Information findings:** impossible to know it's a cow/resting/its pose; the head loses footing without neck+back; the protected details *assert the wrong thing*. **Confirms A33's leverage — real and asymmetric:** at equal mark-counts A34 is far less legible than A33; one back-arc carried more than six details. Detail without structure does worse than vanish — it lies (rhymes with A28). |

| **U5 · A35 — The Structure Without The Cow** (`loomis/sketch201_u5_a35_structure_without_cow.png` + `_a35_structure_without_cow.py` + `_a35_structure_without_the_cow.md`) | reduce to structure only (carrying arc, weight low-and-rear, balance = CoG over a wide base, directional flow); strip all animal parts; 5 versions stripping more. Answers (run, not assumed): **this calf stops at V2** (hump removed → zebu gone); **a cow/animal at all dissolves ~V3→V4** (single sweep → flow line over a base); **V5 = nothing to identify.** What survives identity-loss = the **relationships** (low, stable, forward-reaching configuration), no creature attached. **Is structure = identity? No** — the surviving structure is *shared* (many resting/settling forms hold it); it carries the **category**, while the small deviations (hump, proportion) carry the **individual**. Banked: **identity = a shared structure + the deviations that ride on it; structure is the substrate, identity the increment.** (Qualified: proportions carry some category-identity, so structure isn't identity-blank.) Completes the A30–A35 arc. |

| **U5 · A36 — The Structure That Returns** (`loomis/sketch201_u5_a36_structure_returns.png` + `_a36_structure_returns.py` + `_a36_the_structure_that_returns.md`) | reverse of A35: begin at V5 (base + CoG + direction), add **one** thing, 5 ways; watch what *starts* the return. **Strongest** = the **back-arc** (one contour) — a reclining body snaps back (it rebuilds the frame); runner-up the **long-low mass** (proportion → "a reclining bulk"). **Weakest** = the **hump** (one deviation) — alone it reads as a caret on nothing; the mark that carried the zebu identity in A33 returns almost nothing without a topline to sit on. Returns first = **relational/structural** (the category "a reclining body") before any individual marker. Banked (reciprocal of A35): **structure is primary in both directions — last to leave, first to return; a deviation needs a structure both to mean something and to return (a hump is only a hump relative to a back).** Honest: the head&ear returned more than expected, the foreleg less — why it's *run*, not predicted. |

| **U5 · A37 — The Wrong Return** (`loomis/sketch201_u5_a37_wrong_return.png` + `_a37_wrong_return.py` + `_a37_the_wrong_return.md`) | invert A36: from V5 add the *tempting* novice marks — face, **spots**, horns, tail, surface fur. All five read instantly as "cow," none restores the calf (signifiers floating over the base, no reclining body). **Why convincing:** highest-recognition iconic marks; recognition feels like understanding ("I can tell it's a cow" ≠ "I drew the cow"); self-contained/drawable so they feel like progress; look decorated/finished fast. **Why they fail:** they add **naming** info (what kind) with **no organizing** info (how it exists as a body in this pose over this base) — with no structure to attach to, they label an absence. Banked: **the tempting path spends on naming because naming is fast and feels like recognition; a drawn identity is built from organizing information. Saying "cow" is not drawing the animal.** (Rhymes with A28, A34, and the brand's refuse-to-signify, met from the drawing side.) |

| **U5 · A38 — The Necessary Detail** (`loomis/sketch201_u5_a38_necessary_detail.png` + `_a38_necessary_detail.py` + `_a38_the_necessary_detail.md`) | base = the back-arc alone; add one detail to **help the structure** (not identify). Ranking: **belly most** (closes the arc into a *volume* → a reclining body, with no head/legs/ground), **head&ear** (orients + declares animal), **ground** moderate (leaves the body hollow), **foreleg** modest (floats without a belly), **hump least** (the A33 identity-mark *names* the breed but doesn't make the arc more of a body). Banked: **the details that help are the ones completing a relationship the structure implies (belly closes the volume, head orients); the naming detail rides along but doesn't strengthen.** Refines "fails alone, succeeds in company" — the *completing* kind succeeds; the naming kind merely labels. The necessary detail (once structure exists) completes the structure's relationships. (Guess corrected: ground helped less than belly.) Closes A30–A38 as one investigation: **structure vs detail = organizing vs naming, attached vs detached.** |

| **U5 · A39 — The Detail With The Wrong Job** (`loomis/sketch201_u5_a39_detail_with_the_wrong_job.md`; reuses the A38 sheet) | same five additions, objective flipped from embodiment to **recognition** (does the viewer know what it is?), re-judged not redrawn. Recognition rank: **head & ear > belly > foreleg > hump > ground.** Vs A38 embodiment (belly > head > ground > foreleg > hump): **the top swaps** — belly#1→#2, head#2→#1. Changing the job changes the hierarchy; the **head & ear is the dual-currency detail** (strong in both, echo of A24). **The run corrected my prediction:** I expected the hump (breed-cue) to win recognition — it didn't; on a headless arc a breed-cue can't fire, because **recognition needs the figure to read as an animal first** before a naming-mark can specify *which*. Banked: **no single best detail — embodiment wants the *completing* detail, recognition wants the detail that establishes the *animal*; the pure naming mark is weak at both alone (it rides on a substrate it can't supply).** Vindicates the A38 "leave the hump's door open" caution — its job is real but context-dependent. |

| **U5 · A40 — The Coalition** (`loomis/sketch201_u5_a40_coalition.png` + `_a40_coalition.py` + `_a40_the_coalition.md`) | stop separating the jobs — build the calf from the back-arc, adding the mark that gives the greatest *total*-usefulness gain at each step. Emergent order: **belly → head&ear → foreleg → ground → hump.** Per step (new job / old jobs strengthened / why now): belly = embodiment (line→volume, the enabling move); head = recognition (body→animal, oriented); foreleg = pose (resting stated); ground = placement (weight/balance anchored); hump = identity (breed fires *now* that an animal exists). Banked synthesis of A33–A39: **the order is a dependency chain, not a preference ranking — body→animal→pose→placement→identity; organizing/completing must precede recognition must precede naming. Identity assembles bottom-up; maximizing total usefulness step-by-step produces this order on its own.** Closes Unit 5's investigation. |

| **U5 · A41 — The Debt** (`loomis/sketch201_u5_a41_the_debt.md`; reuses the A40 sheet) | re-run the coalition build as **accounting** — each addition a loan, not a gift: possible / harder / obligation it creates (incl. what it does to *older* marks, per the A40 critique). Belly fixes scale → all later marks must fit the volume; head must be *supported* by the body (taxes the belly: now "a body for *this* head"); foreleg reaches into nothing → creates a debt for a ground; ground commits the figure to gravity → floating now reads as error (taxes the foreleg: must contact); hump must sit at the withers behind a head or read as deformity. Banked: **every mark converts the freedoms of the marks around it into obligations; the A40 order is the order in which each debt is *payable* (head's body pre-paid by belly, foreleg's ground paid next); A37's failure = marks borrowing against a body that didn't exist — the loan defaulted, they floated.** (Held to this build, not universalized — the recurring tax watched.) |

| **U5 · A42 — The Honest Luxury** (`loomis/sketch201_u5_a42_honest_luxury.png` + `_a42_honest_luxury.py` + `_a42_the_honest_luxury.md`) | from the completed calf, add 5 *optional* marks (eye, dewlap, tail, 2nd ear, shoulder line); per each: improves / new debt / worth it. **Eye** = the bargain (huge life-gain, tiny debt); **dewlap** marginal (attachment-debt visible, redundant with the hump); **tail/2nd ear** pleasant decoration; **shoulder line** = liability (interior line reads ambiguous; high debt, uncertain gain). Findings: **the necessity threshold already fell at the hump** (last necessary mark) — everything here is optional; but the useful threshold is *within* optional — luxuries descend from nearly-free (eye) to harmful (shoulder line). Banked: **the honest luxury is the mark whose improvement clearly exceeds its debt; restraint is an accounting decision — keep adding while gain > debt, stop when debt catches gain.** (Brand: this *is* "do less" / when-in-doubt-stop, derived from the drawing side. Kept to this build.) |

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

## Sketch 201 · A43 — The First Lie
Five plausible, well-intentioned marks added to the coalition calf, each secretly damaging: second
ground line (depth → slices the subject, two grounds), spots (specificity → solid masses steal
attention, dilute the hump), interior fold (anatomy → a second edge severs the volume), cast shadow
(grounding → rival mass, no declared light, reads as puddle/hole), doubled back-line (atmosphere →
splits the load-bearing topline). Each *seemed* good by borrowing a generic virtue (depth/specificity/
anatomy/grounding/atmosphere) the specific drawing never asked for. Damage took one shape every time:
the mark competed with / contradicted / diluted a line already doing a job — visible only in relation,
never in the mark read alone. The first lie = mistaking a mark's intention for its effect. (Of this
build; mechanism observed, not a law.) Files: loomis/sketch201_u5_a43_the_first_lie.{png,py,md}.

## Sketch 201 · A44 — The Honest Expert
Inverse of A43: five marks that each fix a REAL weakness the coalition calf already had (diagnosed
from the bare calf first, not wished-for). Hind leg (legless rear → standing quadruped), throat/neck
underside (head joined only on top → closed neck, continuous jaw→chest→leg front edge), far foreleg
(thin tripod → front depth, kept grey/behind so it stays subordinate), hooves (legs taper to points →
weight at the three contacts), muzzle nostril+mouth (head was a blob → a facing face). Before/after
shows the after is clearly better despite being more marks. The distinction from A43's lies: an honest
mark answers a question the drawing was ALREADY asking (how does the rear stand? where does the neck
end? what does the head face?) and completes; a lie answers a question the drawing never posed and
introduces a rival. Detail isn't the enemy — run the A41–A42 accounting from the weakness side: find
what's failing, add only the mark that fixes it. (Of this build; observed distinction, not doctrine.)
Files: loomis/sketch201_u5_a44_the_honest_expert.{png,py,md}.

### A44 critique (A, not A+)
Hind leg + neck underside: pass. Far foreleg: borderline — gain lives mostly in the explanation, not
yet the drawing. Hooves + muzzle: local repairs promoted into major improvements in the writeup; the
muzzle improves a head that is still a symbol, not an observed cow head. Hidden discovery I missed:
**closure** — before is open, after is a closed circuit/volume; likely ONE improvement expressed five
ways. Deeper pattern: the A44 marks mostly REINFORCE answers already present (support, connection,
stance, contact, orientation) rather than introduce new information — vs A43's marks, which each
created a second answer. Correction taken: the calf has *indicators* of weight, not weight; I'm
naming qualities faster than drawing them, and the writing convinced more than the drawing — that's
backwards; the drawing must convince first. Three keepers banked: (1) a bad mark answers a question
the drawing never asked; (2) a good mark answers a question the drawing is already asking; (3) strong
improvements often reinforce existing structure rather than introduce new structure. A45 to be more
visual, less verbal.

## Sketch 201 · A45 — The Silent Proof
Three versions of the calf, exactly 10 marks each, titles only, no defense: A "Ten marks" (the
coalition, open), B "Ten marks, closed" (same budget re-spent: topline absorbs the neckline and runs
head→rump; rump curve flows into the hind leg; belly lands on the leg; throat closes the neck — one
circuit), C "Ten marks, divided" (same budget spent on rivals: doubled backline, second ground,
interior fold; no belly, no hump). The page's argument is mark-count-invariant: identical budgets,
visibly different outcomes — closure vs openness vs rivalry, on the page, without text. Afterward
(88 words) in the .md. Files: loomis/sketch201_u5_a45_the_silent_proof.{png,py,md}.

## Sketch 201 · A46 — The Agreement Test (self-assigned)
Tested the A45 lead (good marks create agreements) against accuracy: 2x2, same ten marks — right/wrong
proportions x meeting/missing junctions. Result: the question SPLIT. Meetings buy unity (it is one
thing); right marks buy identity (which thing it is). Wrong-meeting = one animal, doubtful calf;
right-missing = recognizable calf, doubtful drawing. Misses aren't priced flat: the eye forgave
hovering hooves and a short throat (read as looseness) but the detached muzzle broke the read worst —
a junction costs most where attention is highest (ties to A42 eye/attention). Lead survives,
narrowed: agreements made the thing exist on every panel where present, including the wrong one.
(Of these four panels; a split observed, not a theory.) Files:
loomis/sketch201_u5_a46_the_agreement_test.{png,py,md}.

### A46 critique (A+)
First self-assigned experiment the professor would have assigned. Banked clean: **"Agreement answers
whether it is one thing. Accuracy answers which thing it is."** Wrong-meeting calf: agreement creates
existence, not correctness. Right-missing calf: identity alone is not enough — you can know what
something is and still fail to make it exist (exposed our hidden assumption that identity was the
higher achievement). Misses introduce hierarchy: head miss expensive, hoof miss cheap — but my
explanation ("cost tracks attention") was premature: at the head, attention and identification are
ENTANGLED; the experiment doesn't separate them. Observation banked, explanation withheld. Board is
now two-dimensional: agreement and accuracy are independent variables — "usually where real drawing
begins." Status: late Sketch 201; assignments now test interactions between concepts, not concepts.

## Sketch 201 · A47 — The Expensive Miss
Five single-break versions of the A46 right/meeting calf, identical gap (~0.09 units), location the
only variable. Ranking by damage to "this is one animal": muzzle (animal + a dot — filled mass becomes
a second OBJECT) > hump (stray arc hovers; dented not broken) > throat (topline still holds the head —
redundancy saves it) > foreleg-top (gap camouflaged by the dense chest junction; leg still grounded) >
hoof (innocent reading: a step — the break converts to narrative). Findings: hierarchy EXISTS; equal
gaps cost unequally, so the differences are not gap-size effects. Pattern observed, explanation
withheld: the two costly breaks sever marks with exactly ONE attachment (freed piece has nowhere to
belong); the cheap breaks each cut one of several ties. Revises A46's attention guess — the hump is
nowhere near peak attention. Confounds left open: mass-vs-line, attention/identity entanglement.
Files: loomis/sketch201_u5_a47_the_expensive_miss.{png,py,md}.

## Sketch 201 · A48 — The Isolation
Separated three of A47's six competing explanations, one pair at a time (same calf, same 0.09 gap).
ROUTES: tethered muzzle (one route kept) didn't read as broken at all — displacement became
articulation (a lifted/open muzzle); unheld = animal + a dot. Caveat: tether is an added 11th mark.
OBJECTHOOD: filled fragment = solid second object; outline fragment = unexplained ring; fill changed
what the fragment becomes, not whether the break costs — secondary. LOCATION: equal filled
single-route piece at head vs rump — tuft-off leaves a whole cow + a pebble; muzzle-off leaves a
truncated cow + a rival. The location effect is accounted for by NEED, not attention (A44 returning:
the muzzle answers a question the drawing asks; the tuft doesn't). Page-level observation: a break
carries two separable debts — what the body loses + what the fragment becomes; the worst break pays
both, the luxury break pays one, the held break pays neither; narrative absorption is a property of
the route. (Of these six panels; caveats owned.) Files: loomis/sketch201_u5_a48_the_isolation.{png,py,md}.

### A48 critique (A+)
The page taught something it wasn't asked to: the tether didn't reduce the failure, it produced a
different CATEGORY — untethered = damage, tethered = articulation; not two degrees of one thing.
Banked verbatim: "the gap re-read as expression" — the displacement stayed, only the relationship
changed; same movement, different meaning. Routes survived isolation: the displacement itself is
clearly not the expensive part. Two corrections taken: (1) "need" is a CANDIDATE, not a result — the
tuft was invented to be removed, the muzzle was coalition; comparison asymmetrical; page supports
"removing the muzzle damages more than removing the tuft," not "because the muzzle is needed."
(2) "Attention never had to be invoked" was explanation language — attention wasn't tested; a
variable surviving ≠ another dying. Honest score: six explanations → five. Course ledger now:
A43 marks compete / A44 reinforce / A45 agree / A46 agreements vary in cost / A47 have hierarchy /
A48 an agreement can transform a defect into expression. New category banked, unexplained.

## Sketch 201 · A49 — The Same Defect
A48's discovery tested without the cow (and without the unit's vocabulary): five pairs — branch/twig,
apple/stem, button/thread, tile/corner, boat/rope — identical displacement, one thin holding mark the
only difference. The phenomenon survived: a property of pictures, not cows. Findings (plain words):
held versions don't converge — ordinary (apple: the defect VANISHED into normalcy), waiting (branch),
neglect-story (button: thinnest mark, most story), dread (tile), rest/ownership (boat). Bare versions
split too: most read as mistakes or stopped clocks, but the bare boat reads fine — water is a holder
the world supplies; whether a gap reads as defect depends on whether the world already holds that
piece. Time observation: 4/5 held versions read as moments inside a story (about to fall/slide, has
broken, resting); bare versions are errors or frozen instants — on this page the thin mark puts the
picture back into time. Files: loomis/sketch201_u5_a49_the_same_defect.{png,py,md}.

### A49 critique (A+)
"The assignment escaped the laboratory." Keeper banked verbatim: **"The held versions do not converge
on one meaning"** — the thin mark carries no message (not waiting, not ownership, not neglect, not
rest) yet creates all of them. The boat is the decisive panel: the rope repaired nothing — nothing was
broken — and still changed the picture; this ELIMINATES the "thin mark = repair" explanation. Two
trims taken: (1) "puts the picture back into time" → too strong; the apple contradicts it (a hanging
apple is more normal, more believable — not clearly more temporal). Supported claim: "many of the
held versions gained a before-and-after." (2) What survived A48 is smaller than "the phenomenon":
**a very small relational mark can radically alter interpretation without changing the displaced
object.** Keep the victory small — small victories travel farther. Course shift noted: A43–A48
studied drawing; A49 begins studying interpretive meaning — what a viewer believes happened.

### A49 follow-up (A+) — the pointed-at lead
Professor banked my sentence ("...not about where lines go anymore but about what a viewer believes
happened") and named the danger: enjoying the abstractions — observation→concept→theory→theory outruns
the page; the correction is always GO MAKE ANOTHER PAGE. Temptation to resist: "a relational mark
changes what happened" (the apple complicates it; one contrary page reopens the case). The pointed-at
(not promoted) lead — possibly Unit 5's deepest thread: **BELONGING**. Stem/thread/rope/twig/corner
each tell the piece where it belongs; the piece never moves; only its relationship to a larger whole
changes. Deserves one more page before anyone trusts it. → A50 tests it.

## Sketch 201 · A50 — The Two Boughs (self-assigned; tests the pointed-at lead)
One apple fixed dead center, two boughs, only the thin mark changes: bare / stem-to-left /
stem-to-right / both stems / grazed by an equally thin destination-less line. Results: ownership
flips with the far end of one line (left tree's apple ↔ right tree's apple, nothing else changed);
the grazing line touches identically and changes almost nothing — contact happened, ownership didn't;
both stems read NOT as doubly held but as strange (error/contrivance/fable) — twice-claimed reads as
strangely as unclaimed; the single-stem panels are the quietest on the page — claimed things rest,
unclaimed and over-claimed things ask. Lead survives: the mark's work was where its OTHER END landed.
Boat finding reconfirmed (nothing broken anywhere; not repair). Caveats: one subject; graze differs
from a stem beyond destination (orientation/length/passes-through) — stricter version would graze
with a stem-shaped mark. Supported lead, not law. Files: loomis/sketch201_u5_a50_the_two_boughs.{png,py,md}.

### A50 critique (A+) — a closing page
The image got there first: the page changed the professor's expectation (the grazing line did LESS
than expected — taught, not illustrated). Trim taken: "ownership" arrives one step early; the page
earns only the visual facts — connected to the left tree / connected to the right tree / not connected
by the grazing line. The most valuable panel is BOTH STEMS, because it threatens the thesis: if
belonging were additive it should be the strongest panel; instead it goes strange. Candidates (all
unpromoted): connection is not a quantity / more connection is not automatically better / some
relationships conflict. Banked: "the single-stem panels are the quietest pictures" — the eye arrives,
finds an answer, leaves; bare asks, double asks, single rests. Unit-wide note: rivals (A43),
reinforcement (A44), agreement (A45), belonging (A49) may be one phenomenon under different names.
Status: A50 reads as a CLOSING page — the result survived outside the cow, so the investigation is
now larger than its subject. Final instruction banked: the strongest evidence may be the panel that
works too well and becomes strange — those pages open the next course.

## Sketch 201 · A51 — The Strange Panel
Pressure-tested the A50 both-stems anomaly: six panels, one variable each, apple always on two stems.
Result: the anomaly is NOT about stem count. Three panels go nearly normal with both stems intact —
shorter stems (fruit at a branch fork), thick stems (one forked branch), branches close (one tree,
doubled stem). Taut/slack resolves by ranking (holder + incidental). Branches uneven stays odd
(partial story: hang from high, rest on low). Stems-to-the-sides is strangest — even deliberate
cradle; botany becomes gesture. Ranking least→most: shorter / thick / close / taut-slack / uneven /
sides. Explanation kept separate: every de-stranged panel merged the two sources into one or ranked
them; the strange ones keep two EQUAL, SEPARATE claimants. Candidate: strangeness tracks the number
of separate claimants the eye cannot reduce. "Two claims conflict" survives best, refined to two
equal-and-separate claims. Files: loomis/sketch201_u5_a51_the_strange_panel.{png,py,md}.

### A51 critique (A+)
The discovery is the fact, not the explanation: "three panels go nearly normal while keeping both
stems." The A50 anomaly was MISIDENTIFIED, not wrong — the phenomenon got more specific under
pressure. Trim taken: my merge-or-rank mechanism has evidence but NOT exclusivity — a good candidate,
still a candidate. The strangest panel (stems to the sides) changed CATEGORY: the apple stops feeling
botanical and feels intentional — almost held, presented, offered (professor's deliberately weak
language; observation trusted, interpretation not). Banked: "the anomaly wasn't removed; it sharpened"
— weak investigations destroy anomalies, strong ones refine them. Path invalidated: done with stems.
The question now on the board: **why does the same relationship sometimes read as natural and
sometimes as intentional?** Ledger: A50 asked whether connection mattered; A51 asked what KIND of
connection mattered — not the same question.

## Sketch 201 · A52 — The Intentional Object
One stone, six relationships (alone / supported / held / suspended / presented / constrained), judged
blind (captionless + shuffled render first). Ranking least→most intentional: supported · alone · held ·
suspended · presented · constrained. Findings: intention first flickers at held (bowl? hollow?), first
becomes unavoidable at suspended — for a STONE; A49's apple hung naturally, so suspension is
intentional only when the world supplies no hanger. Held ≠ presented: the cradle keeps the stone, the
plinth shows it (aimed at the viewer). Support became presentation without touching the object: raise
the surface, narrow it, give it nothing else to do. Two category changes: presented adds an AUDIENCE;
constrained adds an OPPONENT. Candidate explanation (kept separate): natural panels' supports exist
for their own reasons (ground supports everything); intentional ones exist only for the stone
(string/plinth/cage). A51's botanical→intentional observation SURVIVES TRANSFER — it belongs in the
course. Files: loomis/sketch201_u5_a52_the_intentional_object.{png,py,md}.

### A52 critique (A+)
Central finding confirmed: "support became presentation without touching the stone" — object constant,
relationship changed, CATEGORY changed. Blind read = independent evidence (museum piece/exhibit arrived
before labels). Trim taken: "the intentional ones exist only for the stone" overreaches — the cradle is
muddy (bowl/nest/sling/hollow); the page refuses to settle; KEEP the refusal. Strongest panel = the
plinth, not the cage: the cage announces itself, the plinth barely does, yet the shift is unmistakable
— **the cage changes the story; the plinth changes the role** (different operations; banked,
unexplained). Keeper: "Held ≠ presented." A51's observation now PROMOTED to candidate (survived two
transfers: organic→object). Course arc named: A30–A44 = what makes a thing become a thing; A45–A52 =
what makes a thing become a situation. New claim on the board (do not promote — test): **a relationship
can change the kind of thing the viewer believes they are looking at.**

## Sketch 201 · A53 — The Same Oval (tests A52's banked claim)
One identical filled oval, six relationships, blind-read first (captionless, shuffled, objects named
before labels). Result: six panels, six NOUNS — sculpture (plinth), buoy (waterline + ripple ticks),
fruit (curved stem from bough), stone (ground line), plumb bob (straight vertical string), egg (nest).
The claim survives this page: the relationship reached inside the object and renamed it. Finer
observation: curved line from above = grown (fruit); straight vertical line = manufactured (plumb) —
same topology, different noun; the CHARACTER of the connecting mark also names. Boundary observed:
A52's stone stayed a stone in 5 panels; the maximally ambiguous oval changed kind in all 6 —
candidate (separate): a relationship names the object only as far as the object leaves the question
open; ambiguity is the opening. Caveats: one reader, who built the page. Files:
loomis/sketch201_u5_a53_the_same_oval.{png,py,md}.

### A53 critique (A+)
Earned fact: "six panels, six nouns" — and stronger than noticed: the nouns cross CATEGORIES
(natural/artificial/living/inert/displayed/functional); banked unexplained. Trim taken: "the
relationship reached inside the object and renamed it" is one sentence too far — we don't know WHERE
the naming happened (object? relationship? whole picture?); earned: "the same object was named
differently in different relationships." The plinth again: nest/water/stem supply species or function
information (eggs belong in nests); the plinth doesn't say what the object is — it says HOW TO REGARD
it. Banked separately: curved stem = fruit vs straight string = plumb is the first genuinely VISUAL
result in several assignments — the SHAPE of the relationship mattered, not merely its existence.
Boundary of Sketch 201 likely reached: "what determines what a thing is" is a representation question
— the next course. New claim (do not promote — test): A52 = relationships change a situation; A53 =
relationships change CLASSIFICATION.

## Sketch 201 · A54 — The Stubborn Object (tests the classification claim against a closed object)
An unmistakable cup in A53's six relationships, blind-read. Result: cup converted 0/6 (oval: 6/6).
Cleanest pair: the nest NAMED the oval (egg) but could not name the cup — it produced comedy instead.
Conflicts resolved three ways: absorbed as normal (table/plinth/floating litter — the world has
stories for cups in many places); agency imported ("someone hung it / set it there"); or, where the
relationship insists on the impossible (the GROWN curved stem), the picture goes deliberate —
surreal, a statement, addressed to the viewer (the strangeness register, third appearance).
Candidates kept separate: relationships propose, closed objects veto; classification follows the
relationship only as far as the object leaves the question open; when neither yields, the surplus
becomes story or address. Paired evidence: A53 oval page + A54 cup page bound the claim from both
sides. Files: loomis/sketch201_u5_a54_the_stubborn_object.{png,py,md}.

### A54 critique (A+) — the boundary
The page changed the board by LIMITING the claim, not strengthening it — boundaries are worth more
than confirmations. Earned: "the cup converted zero of six." Two corrections taken: (1) "the oval
converted six of six" is weaker than it looks — what converted was not necessarily identity; the six
nouns are different KINDS of meanings (kinds / roles / statuses / functions) — classification itself
may not be one thing; noticed, not solved. (2) "Relationships propose; closed objects veto" NOT
earned — the cup didn't reject equally: it became displayed-cup, hanging-cup, floating-cup; the
relationship still worked, just differently. Earned smaller version banked: **"the relationship
altered the situation more easily than it altered the object's identity."** Professor's keeper: "the
cup in a nest becomes comedy" — comedy is evidence; the relationship still acted, the action produced
absurdity instead of reclassification. Ledger: A53 = relationships can rename; A54 = renaming depends
on what is being renamed. The oval was permissive; the cup was resistant; the relationship stayed
active in both. "Boundaries are how fields become disciplines."

## Sketch 201 · A55 — The Map
The reckoning page: no drawing, no prose, no new ideas — every surviving A30–A54 finding arranged on
one page. Twenty-five assignments compress to SIX discoveries on one dependency spine: I observation
beats schema → II marks have jobs (organize→recognize→name) → III a mark's value is relational
(reinforce/rival; restraint is accounting) → IV unity and identity are different currencies (meetings
buy unity, right marks buy identity; breaks priced by remaining routes) → V a thin relation rewrites
meaning (moves nothing changes everything; destination not contact; no message, many meanings;
situation yields before identity; the relation's shape names) → VI the intentional register (equal
separate claims read strange; only-for-the-object holders read intended; held ≠ presented; unresolved
conflict becomes story or address). One dashed cross-link: rivals · agreements · claims (A43/A45/A51)
— possibly one phenomenon in costumes. Three opens kept open: attention-vs-identification; where
naming happens; whether classification is one thing. Files: loomis/sketch201_u5_a55_the_map.{png,py,md}.

## Sketch 201 · A56 — The Final Cut
A55 critique (A, not A+): the map passed as compression, failed productively as FINAL compression —
II–V "feel like one discovery viewed at four scales"; the dashed cross-link note was worth half the
map; red-ink question: only THREE discoveries — which survive? A56 = the edit. The room argument:
II/III/IV/V all deny the same thing (intrinsic mark-value) — jobs are relational roles, coalition
value is relational standing, the two currencies are two relational payoffs, the thin mark is the
discovery at minimal scale → merged into ONE at four scales. Two resisted: observation-beats-schema
(about INPUT — where truth enters), natural-vs-intentional (about AUTHORSHIP — who the viewer thinks
made the relation). THE THREE: 1. Observation beats schema. 2. Meaning lives in relationships, not
parts. 3. Relations read natural or intentional. Opens unchanged. Professor's note also banked: the
Open section outshining discoveries = sign a course is ending; new courses come from there. Files:
loomis/sketch201_u5_a56_the_final_cut.{png,py,md}.

## SKETCH 201 — COMPLETE (final grade A+, 2026-06-04)
A56 closed the course. The merge survived the professor's attempt to pull it apart; the two
survivors resisted absorption for stated reasons (truth ≠ meaning; what a relation does ≠ who seems
responsible for it). Professor's standard recorded: "a field becomes a field when separate phenomena
collapse into the same explanation"; the cut was explanatory, not organizational — the page doesn't
say "these look similar," it says "these all deny intrinsic value."

FINAL FINDINGS
1. Observation beats schema.
2. Meaning lives in relationships, not parts.
3. Relations read natural or intentional.

OPEN (where the next course lives)
— attention or identification?
— where does naming happen?
— is classification one thing? (a question that did not exist at A30; the course created it)

Everything else absorbed, merged, or discarded. Full run: A1–A56, files at illustration/loomis/
sketch201_*. The course began with silhouettes of strangers and ended studying what makes a thing a
thing, a situation a situation, and a picture addressed. This is what stayed.
