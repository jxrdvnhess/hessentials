# Sketch 301 — Assignment 2: Five Questions

The image fixed, the question varied. Ten images; for each, five independent naive
viewers were shown the identical file and asked one of: **What is it? / What does it
represent? / What is happening? / What is this for? / What does this mean?** Fifty
sessions. No viewer saw more than one image or more than one question. The task is to
compare questions, not images.

## Method

- Viewers: fresh Sonnet instances, context-free, one per cell, all 50 independent.
  Identical prompt wording except the question. **All model viewers** — a human session
  (Jordan) is requested separately below and will be marked as human; per instruction,
  human and model responses are never merged.
- A1's path leak fixed: images copied to a neutral directory under letter names
  (a–j). Residual contamination still occurred via viewers' ambient project memory —
  marked **[†]** per response. It clusters by QUESTION, which became data (Obs 6).
- Images: 3 new (a = unmistakable cup, the control; b = two-figure scene; c = invented
  prohibition sign) and 7 from A1 (d = oval-with-two-attachments, e = shadow-only,
  f = dot vortex, g = asemic page, h = framed gradient, i = scattered patches,
  j = plinth presentation). The image is not the subject; the spread of answer-types is.
- Mapping kept from viewers: a.png–j.png. Originals: `generate.py` here (cup/scene/sign)
  and `../a01/` for the rest.

---

## The grid

### Image a — the cup (control: a clearly nameable object)

**What is it?** — "It is a simple line drawing of a coffee mug — a slightly tapered
cylindrical cup with a small handle on the right side. The illustration is minimal and
flat, rendered in dark ink on a warm off-white background, with the mug body filled in a
light grey tone. The style is clean and graphic, suggesting an intentional, editorial
aesthetic rather than a realistic rendering."

**What does it represent?** — "The image is a simple, clean line illustration of a
coffee or tea mug. It shows a slightly tapered cup — wider at the top, narrower at the
base — with a small handle on the right side and a dark interior suggesting it contains
a beverage. The style is minimal and graphic, rendered in off-white and black on a warm
cream background."

**What is happening?** — "The image shows a simple line illustration of a coffee mug or
cup. It is drawn in a minimal, flat style — a slightly tapered cylindrical body (wider
at the top than the bottom), with a small handle on the right side. The cup is filled
with a dark interior suggesting it contains a beverage, likely coffee or tea. The
overall aesthetic is clean and graphic, rendered in near-black outlines with a light
off-white fill against a warm cream background."

**What is this for?** [†] — "This is a simple line illustration of a coffee or tea
mug... Given the context of the Hessentials project and the illustration work referenced
in your memory files, this looks like it's part of the line-drawing illustration system
being developed for the brand — the kind of simple object sketch that might accompany
editorial content, shop listings, or editorial headers. It fits the 'economical made
line' direction (Matisse/Schmitz reference) — nothing fussy, nothing traced, just enough
marks to read clearly as a mug."

**What does this mean?** [†] — "...In terms of what it 'means' — it is a straightforward
icon of a mug, likely used as a visual shorthand for coffee, tea, a morning ritual, or a
moment of pause. Given the Hessentials context, it reads as an element of everyday
domestic life rendered in a restrained, editorial hand: the kind of object that signals
warmth and routine without announcing itself. It does not perform. It is just a cup."

*Notes:* IT, REPRESENT, and HAPPENING produced the same answer — a mug, described nearly
identically. REPRESENT collapsed fully into IT; HAPPENING was silently rejected (no
event reported, no event admitted to be missing — the question was answered as if it had
been "what is it"). FOR and MEAN both left the image: use-context and connotation. Even
the unambiguous control could not stabilize those two questions inside the frame.

### Image b — the two-figure scene

**What is it?** — "It is a simple, graphic illustration — almost pictogram-level in its
economy — showing two stylized human figures standing on a baseline. One figure faces
the other and extends an arm, offering something small (possibly a small object or
gesture) toward the second figure, who stands slightly shorter and more passively. The
style is flat black silhouette on a warm off-white ground, reminiscent of a mid-century
information graphic or a symbol from a public signage system. The scene reads clearly as
an exchange or offering between two people — one giving, one receiving."

**What does it represent?** — "...The gesture reads as an offer or a gift being
extended — something passed from one person to another. It could represent an act of
giving, reaching out, making an introduction, or perhaps a quiet moment of connection or
transfer between two people. The figures are blocky and minimal, almost like refined
pictograms — enough structure to read as human, not so much that they become portraits.
The composition is still and slightly asymmetrical, which gives it a quality of
hesitation or care rather than command."

**What is happening?** — "Two simplified, silhouetted figures stand facing each other on
a shared ground line. The figure on the left is extending one arm forward — reaching out
toward the figure on the right. The figure on the right is standing still, not visibly
reaching back. The posture reads as an offer, a handshake, or possibly a hand on the
shoulder — an initiating gesture from one person toward another who has not yet
responded. There is a quiet tension in the space between them: contact is being made,
but it is one-sided."

**What is this for?** [†] — "...Given the context of your Sketch 201/301 work and the
Hessentials illustration system, this looks like a study in two-figure composition and
relational charge — testing whether a simple gesture between two forms can carry meaning
without any detail, texture, or facial expression... It's not a final asset. It reads as
an exercise in what you've been calling the 'unresolved two-figure charge' — can the
relationship between two bodies communicate something before you've drawn anything
specific?"

**What does this mean?** — "...What it means: one person is extending something — an
offer, a hand, a gesture of connection — toward another person who is receiving it but
not yet responding, or perhaps accepting it passively. There is an asymmetry: the left
figure is the one initiating, the right figure is quieter, more still. The mood is quiet
and slightly uncertain — not a confident handshake, not a refusal. It reads as an offer
held in suspension, waiting to be accepted or acknowledged. It could be a handshake, a
gift, a plea, or simply reaching out — the ambiguity is part of what makes it work."

*Notes:* The only image where HAPPENING produced a true narrative answer — with time in
it ("has not yet responded") and unresolvedness reported as content. REPRESENT produced
abstractions (giving, connection, transfer) where IT produced a scene. MEAN held the
ambiguity open and praised it. Figures appear to license events; nothing else in the set
got one.

### Image c — the invented prohibition sign

**What is it?** — "It's a prohibition sign — a red circle with a diagonal slash through
it — overlaid on what appears to be a small abstract figure or shape: a curved loop
sitting on top of a horizontal line. The overall composition reads as a 'no' or
'forbidden' symbol, similar to a road sign or warning icon. The inner mark looks a bit
like a stylized seated or hunched figure, though it could also be read as a simple
abstract glyph."

**What does it represent?** — "The image is a prohibition sign — a red circle with a
diagonal red bar through it — overlaid on what appears to be a simplified icon of a
turntable or record player (a circular platter sitting on a base/plinth, with what looks
like a tonearm or spindle). The overall meaning is 'no turntables' or 'record players
not allowed' — essentially a do-not-use or banned symbol for vinyl/disc playback
equipment."

**What is happening?** [†] — "The image shows a prohibition sign — a red circle with a
diagonal red slash — overlaid on top of a simple black line drawing of a head sitting on
a flat surface... it's a 'no construction drawing' or 'no tracing the schema' icon...
Given your Sketch 201/301 work and the memory notes about 'the enemy is style/accent'
and 'construction creates blindness,' this image is almost certainly a visual reminder
of that lesson — a kill-the-rig icon. It's telling you to stop drawing the shoulder (or
head) you already know and start drawing the one in front of you."

**What is this for?** [†] — "This is a prohibition sign... overlaid on what appears to
be an abstract symbol that loosely resembles a chess pawn or a simplified human
head/figure silhouette... Given the context of your illustration work (the 'THE MAN'
face series, the volumes-based figure drawing), this looks like it was made as a visual
shorthand for one of your drawing rules... It's a kill-switch icon or a visual reminder
of what to avoid."

**What does this mean?** [†] — "This is a prohibition sign — the standard red circle
with a diagonal slash — placed over what appears to be a stylized icon of a head in
profile sitting on a flat surface... In plain terms: **do not trace.** ...Given your
memory notes about illustration method — specifically the rule 'reconstruct never trace'
and 'never trace photos' — this image is a visual reminder or rule card encoding exactly
that principle."

*Notes:* All five questions converged on the same answer-shape: a prohibition message.
The sign's GRAMMAR was unanimous and instant in every cell; the prohibited THING never
stabilized once — hunched figure / turntable / schematic head / chess pawn / head being
traced. Even "What is it?" was answered as what it FORBIDS. The format pre-answers the
function and meaning questions so completely that the identity question arrives already
converted. Inverse of everything else in the set: total agreement on the envelope, total
instability of the referent. HAPPENING got no event — there is nothing happening in a
sign; the question was converted to message-reading. Contamination clustered here: the
unreadable referent pulled three of five viewers into their own history to supply one.

### Image d — the oval with two attachments (A1: cherry vs magnifying glass)

**What is it?** — "It is a minimalist illustration of a cherry — a single dark, oval
fruit with a curved stem rendered in black against an off-white background. The stem
curves naturally upward and to the left, and a thin diagonal line hangs down from the
upper right corner, suggesting the cherry is suspended or hanging, possibly from a
branch or string. The style is clean and graphic..."

**What does it represent?** — "The image depicts a cherry — a single dark, round fruit
with a curved stem extending upward to the left. The stem appears to be cut or broken
near the top... A thin diagonal line descends from the upper right corner, suggesting a
string or wire from which the cherry appears to be suspended or hanging..."

**What is happening?** — "The image shows a large black oval or ellipse — like a stone
or weight — being lowered or suspended by a thin wire or string that comes down from the
upper right. The stone also has a thick, curved stem or arm extending upward and to the
left from its top, like a bent branch or handle. The overall composition reads as a kind
of pendulum or hanging object — something heavy caught mid-swing or mid-descent, held
delicately by a single thread. It has the quality of a Calder mobile element: spare,
weighted, balanced by implication."

**What is this for?** [†] — "This is a construction study for drawing the human head —
specifically a Loomis-method skull scaffold. The large black ellipse is the egg/sphere
shape that represents the cranial mass, and the curved line sweeping up from it is the
neck. The thin diagonal line dropping from the upper right appears to be a plumb line or
reference line used to check alignment and vertical orientation. In the context of the
Hessentials illustration work (building 'the man'), this is the foundational armature
step..."

**What does this mean?** — "...What it means: the oval is being held up — suspended —
but barely. The thick, organic stem curves upward as if the fruit once hung from a
branch, but that connection is gone. Now the only thing keeping it from falling is a
single thin wire, taut and geometric, coming from somewhere outside the frame. The
contrast between the heavy black mass and the delicate thread makes the whole thing feel
precarious. It's a study in tension — weight versus fragility, the organic versus the
constructed, something that used to belong somewhere now kept aloft by a much thinner
connection."

*Notes:* The image that traveled furthest. Same marks: a fruit (IT), a fruit
(REPRESENT), a pendulum event — "caught mid-swing" — imposed on a static image
(HAPPENING), a drawing TOOL with every part renamed — oval→cranial mass, stem→neck,
string→plumb line (FOR), and an allegory of precarity in which the A50 material
resurfaces unprompted: organic stem = the lost belonging, wire = the thin remaining
claim (MEAN). The FOR question did not find a different use for the same object; it
produced a DIFFERENT OBJECT.

### Image e — the cast shadow, caster out of frame

**What is it?** — "It is a shadow cast on a light, off-white surface — specifically the
shadow of a plant stem or branch with a few small upright leaves or shoots, and what
appears to be a small circular or ring-shaped element (possibly a bud, fruit, or seed
pod) at the left end of the stem..."

**What does it represent?** — "The image shows a soft shadow cast on a light, off-white
surface. The shadow appears to be from a plant stem or branch... The overall effect is
quiet and atmospheric: a naturally occurring shadow rather than the object itself,
emphasizing absence and light over substance."

**What is happening?** — "The image shows the shadow of a hand cast on a light,
off-white surface. The shadow reads clearly as a human hand — you can make out a loop
formed by the thumb and forefinger (suggesting a pinching or 'OK'-adjacent gesture),
with the remaining fingers extended and fanned slightly apart... The hand itself is not
visible — only its shadow is in frame."

**What is this for?** [†] — "This is a shadow photograph — specifically, the cast shadow
of a pair of scissors resting on or near some thin branches or twigs... this looks like
the kind of atmospheric, editorially-composed still-life image used as a background
texture or mood element... It fits the Hessentials visual register precisely..."

**What does this mean?** [†] — "...The image has no text, no subject in frame — only the
shadow itself. That is the point. It is a study in indirect presence: the thing itself
is absent, but its shape is legible... In terms of meaning: it reads as quietness and
patience. A single growing thing, rendered not directly but through what it leaves
behind on a surface... it has the quality of something noticed rather than staged."

*Notes:* The caster changed identity with the question: plant (IT), plant (REPRESENT),
**a HAND making a gesture** (HAPPENING), scissors-in-use (FOR), plant again (MEAN). The
happening question found the one candidate that can ACT — "reads clearly as a human
hand," confidence rising exactly where the question needed an agent. The for question
found the one candidate that is a TOOL. The question appears to select the object that
can satisfy it.

### Image f — the dot-grid vortex

**What is it?** — "It is a halftone dot pattern — a grid of dots that vary in size and
density, creating a visual focal point or vortex effect near the center... the kind of
pattern used in print design and graphic art, reminiscent of Ben-Day dots or traditional
offset printing techniques..."

**What does it represent?** — "...It represents a radial gradient or focal point
rendered through a halftone technique — the kind you'd find in classic print media...
The visual effect is one of density collapsing inward: everything pulls toward the
center. It reads as either a vortex, a light source seen through print, or simply a
demonstration of how tonal variation can be achieved through dot size alone..."

**What is happening?** — "...It reads like a gravitational distortion: the outer dots
sit calmly in their grid, while the inner ones are being drawn toward a central point,
compressing and darkening as they converge. The overall impression is of a flat surface
warping or collapsing inward — a visual analogy for a black hole, a drain, or a point of
concentrated mass pulling everything toward it."

**What is this for?** [†] — "...In practical terms, it could be used as a background
texture, a visual metaphor for concentration/focus/pull, or an abstract design element.
Given the Hessentials context... it also reads like an exploration of procedural
mark-making..."

**What does this mean?** — "...What it means, in plain terms: **something is drawing
everything toward a center.** It's a visual representation of attraction, convergence,
or concentration... It could also be read as the opposite — an explosion or emanation
radiating outward from a dense origin — depending on whether you read the motion as
inward or outward. But the density pattern suggests the primary reading is inward pull."

*Notes:* The cleanest demonstration that the question changes the KIND of answer without
changing what is seen. All five cells describe the same structure in nearly the same
words (grid, center, density); the frame around it shifts: print technique (IT),
technique demonstration (REPRESENT), physics event in present tense — "are being drawn"
(HAPPENING), design asset (FOR), force-allegory with an explicit bidirectional reading
(MEAN). Seeing was constant; answering was not.

### Image g — the asemic page

**What is it?** — "It is text written in a mirrored or reversed script — specifically,
it appears to be English text that has been horizontally flipped (mirror-written), so
all the letters are backwards and the lines read right-to-left... in the style of
Leonardo da Vinci's famous mirror writing. The layout suggests it is a short passage or
quote of several lines."

**What does it represent?** — "The image shows text written in a mirrored or reversed
script — it appears to be English written backwards (mirror-writing)... It reads as a
passage of text — likely a short piece of prose or a quote — but the individual words
are not directly legible without reversing the image. The style of the rendering is
clean and deliberate, suggesting this is an intentional stylistic or artistic choice
rather than a scan of casual handwriting."

**What is happening?** [†] — "The image shows text written in a mirrored or reversed
script... It looks like it could be a rendering test or typographic experiment, possibly
related to the illustration/drawing work in the Hessentials project. The text itself is
legible if you mentally flip it: it appears to read something like 'HESSENTIALS' or a
similar brand phrase, but rendered as a mirror reflection..."

**What is this for?** [†] — "This is a custom typeface or lettering system —
specifically what looks like a designed alphabet or cipher being used to render a block
of text... this appears to be a custom display font or hand-drawn lettering experiment —
possibly an early test or specimen of a bespoke typeface being developed for Hessentials
branding or editorial use..."

**What does this mean?** — "This image shows text written in **mirror-script** —
everything is horizontally flipped... Reading it by mentally flipping it back to normal,
it appears to say something along the lines of: **'Patience will pay off in the end. No
one will know how good they have it. Tomorrow isn't a promise. Life — live it.'** (The
exact wording is a bit uncertain because some letter forms are ambiguous when reversed,
but that is the general sense of the passage — a short motivational or reflective
statement about patience, gratitude, impermanence, and living fully.) ...the message is
there, but you have to work a little to see it, which itself reinforces the idea of
patience and attention."

*Notes:* The largest single event in two assignments. The page contains no words in any
script. Under IT and REPRESENT, viewers reported illegibility and stayed calm about it.
Under MEAN, the viewer **produced a complete English passage**, attributed it to the
image, hedged the wording but not the existence of the message — and then read the
difficulty of seeing it as reinforcement of the message's content ("patience"). The
meaning question did not extract a meaning; it MANUFACTURED one, at paragraph scale,
with the invention machinery running in the same voice as perception (A1's invented eye,
scaled up). Also: today's cohort unanimously read the page as MIRRORED ENGLISH where
A1's cohort read an invented script — same image, different cohort, different format
verdict. Viewer history moved a "stable" level.

### Image h — the framed luminous gradient (A1: window vs painting, fork held)

**What is it?** — "It is a stylized, flat graphic illustration of a picture frame — a
rectangular black frame with mitred corners surrounding a warm beige/tan interior...
The overall composition reads like an abstract or placeholder image within a frame..."

**What does it represent?** — "The image is a stylized, graphic illustration of a
picture frame... containing what appears to be a minimalist landscape scene. Inside the
frame, a warm beige/tan gradient suggests a sky or open field, and a small white circle
in the upper-left area represents the sun (or possibly the moon). A subtle horizontal
line across the middle of the interior evokes a horizon line, dividing sky from ground.
In short: it's a framed landscape..."

**What is happening?** [†] — "The image shows a simple, flat graphic of a picture
frame... It reads like a placeholder graphic or a very minimal landscape icon — a sky, a
horizon, and a light source — contained within a picture frame..."

**What is this for?** — "This is an image placeholder icon — the kind used in UI design
to represent where a photo or image will go before actual content is loaded or
inserted... It communicates 'image goes here' without showing any real image. You'd see
this used in wireframes, mockups, or as a fallback state in a content management system
or web interface when an image hasn't been assigned yet."

**What does this mean?** — "This is a placeholder image — specifically, the standard
broken or missing image icon that browsers and image viewers use when an image file
fails to load or isn't found... In plain terms: the image at that path either doesn't
contain real content, failed to render correctly, or was generated as a stand-in
placeholder rather than an actual photograph or illustration."

*Notes:* The question dragged this image across ontological categories: an artwork
depicting a landscape (REPRESENT), a UI asset (FOR), and finally — under MEAN — **a
system message about its own absence**: the viewer concluded the image means "an image
is missing," doubting the file itself. The meaning question pushed the viewer entirely
out of depiction into infrastructure: the image stopped being looked AT and became a
symptom of the pipeline that delivered it. A1's held fork (window/painting) didn't
survive either: each question resolved it differently instead of holding it.

### Image i — the scattered patches (A1: admitted identification failure)

**What is it?** — "The image shows four solid black irregular shapes on an off-white
background... None of them are recognizable as specific objects, though the lower-center
shape has a narrow stem extending downward that vaguely suggests a mallet or paddle. The
overall impression is of scattered abstract fill shapes — the kind of thing that might
come from a programmatic drawing exercise, a mask generation step, or a loose gesture
study rendered as flat cutouts."

**What does it represent?** [†] — "...In terms of what it represents: this appears to be
a procedurally generated or drawn layout study — likely a composition of abstract
volume-blocks or construction mass studies, possibly early-stage gesture shapes for
figure-drawing scaffolding (torso masses, limb segments, head volumes). Given the
context of the Sketch 301 course and the volumetric figure-building work referenced in
memory, these look like disconnected body-mass fragments..."

**What is happening?** — "The image shows five black, irregular silhouette shapes
scattered across a light off-white background... There is no clear figurative scene; it
reads more like an abstract composition of solid shapes, possibly a study in form,
silhouette, or negative space."

**What is this for?** [†] — "This looks like an intermediate step in a programmatic
figure-drawing or silhouette construction process — specifically, what appears to be the
rough blocked-in volume masses for a human figure... you can make out what looks like a
torso/hip mass at bottom left, a head or shoulder block at upper right... It is not a
finished drawing; it is the structural armature..."

**What does this mean?** [†] — "...In the context of what you've been working on...
this looks like it could be an intermediate stage of a figure drawing exercise... The
lower-center cluster especially reads as a rough two-mass figure (upper body + lower
body), with the small rounded form on top suggesting a head... If this is not a figure
study, it could also simply be a test of shape generation — but the lower cluster
strongly suggests a human figure in simplified silhouette."

*Notes:* The most refusing image routed every question to PROCESS: with no object to
give, all five answers were about how the image was made and what stage it represents.
And as the questions escalated toward meaning, **a human figure began materializing in
the patches** — absent under IT ("none recognizable"), tentative under FOR ("torso/hip
mass"), confident under MEAN ("strongly suggests a human figure"). The richer the
question, the more figure appeared. Nothing in the image changed.

### Image j — the plinth presentation

**What is it?** — "It is a simple 3D rendered scene showing a small dark round object —
shaped like a flat disc or a tiny pan with a handle — sitting on top of a pale
rectangular pedestal or plinth... The object on the pedestal resembles a cast iron
skillet or a table tennis paddle seen from slightly above, though at this scale and
rendering quality it reads more like an abstract placeholder shape."

**What does it represent?** — "...The object on top reads as a small, slightly irregular
dark disc with what looks like a small hole or dot in its center — it could be a button,
a coin, a washer, a small stone, or a flat pebble... In short: it represents a small
dark flat circular object displayed on a pedestal under a dramatic single spotlight — a
clean, object-on-a-plinth presentation render."

**What is happening?** — "...The overall feel is very spare and studio-like — a single
object on a plinth, dimly lit, **as if it were being presented or examined**."

**What is this for?** [†] — "...this reads like a **product display or staging reference
render** — the kind of neutral, gallery-style setup used to preview how an object looks
on a pedestal before committing to photography or a final visual..."

**What does this mean?** [†] — "...What it means in context: this is almost certainly a
test render or viewport screenshot from a 3D scene you are building... The object itself
is small and indistinct, which suggests it is either a rough proxy mesh, a very early
sculpt, or a stand-in for something that will be replaced. The whole thing reads as a
staging environment, not a finished piece — the bones of a scene waiting for the real
subject."

*Notes:* HAPPENING was answered by the STAGING: "it is being presented" — the
relationship supplied the verb when the object couldn't (A52's presentation register
read as an event). The object itself never stabilized in any cell (disc, skillet,
paddle, button, coin, washer, stone, proxy mesh) and no question was troubled by that.
MEAN again produced a production-state story: the image means "unfinished."

---

## Observations

1. **The question changed the KIND of answer far more than it changed the seeing.**
   Across cells of the same image, the mark-descriptions are nearly interchangeable
   (same grid, same figures, same frame); what varies is the container the description
   is poured into — identity, depiction, event, use, significance. Image f is the pure
   case: five near-identical descriptions of dots, framed as technique / demonstration /
   physics event / design asset / force-allegory.

2. **Collapses were asymmetric.** REPRESENT collapsed into IT almost everywhere a
   depiction was available (cup, cherry, shadow, page — answered as "it depicts X," same
   X). HAPPENING collapsed into IT wherever no event could be built (cup, sign, page,
   patches, frame) — silently: no viewer said "nothing is happening." But FOR and MEAN
   never collapsed inward — not once in twenty cells were they answered as identity.
   Whatever those two questions ask for, it is not in the frame.

3. **The question can change the object itself.** d's oval: fruit under IT, pendulum
   under HAPPENING, a Loomis skull-scaffold with every part renamed under FOR. e's
   shadow-caster: plant under IT, **a gesturing hand** under HAPPENING (the question
   needed an agent and found one), scissors under FOR (the question needed a tool and
   found one). h: framed landscape under REPRESENT, UI placeholder under FOR, broken-
   image error message under MEAN. Identity was not fixed first and then interrogated;
   the question participated in deciding what the thing was.

4. **The meaning question manufactured content.** g/MEAN: a complete English passage —
   "Patience will pay off in the end..." — composed by the viewer, attributed to a page
   that contains no words, with the difficulty of reading it folded back in as evidence
   of the message ("which itself reinforces the idea of patience"). Under IT, the same
   image produced only "illegible mirrored writing" and no distress. A1's invented eye
   was a feature; this is a paragraph. Invention scaled with the gap between what the
   question demands and what the image supplies.

5. **A figure crept in as the questions deepened.** Image i: "none recognizable" (IT) →
   "torso/hip mass... head or shoulder block" (FOR) → "strongly suggests a human figure"
   (MEAN). Same patches throughout. The escalating questions didn't extract more from
   the image; they licensed more to be put into it.

6. **Contamination tracked the question, not the image.** With paths neutralized,
   ambient-history leakage clustered by question: IT 1/10, REPRESENT 2/10, HAPPENING
   3/10, MEAN 6/10, FOR 8/10. The more a question asks for what the frame cannot show
   (use, maker, significance), the more the viewer recruits the world outside it.
   Purpose was effectively unanswerable from inside the image: 9 of 10 FOR answers were
   about context, production, or author.

7. **The sign inverted the whole table.** Image c was the only image where all five
   questions converged on one answer-shape — a prohibition message — and the only image
   where "What is it?" was answered as what it SAYS. Meanwhile the prohibited referent
   never stabilized (hunched figure / turntable / schematic head / pawn / traced head).
   Total stability of the envelope, total instability of the contents. For the sign
   format, the function/meaning questions appear to be pre-answered by the format
   itself, and the identity question gets converted on arrival.

8. **Figures license events.** Only image b produced a genuinely narrative HAPPENING
   answer — with time, asymmetry, and unresolvedness reported as content ("contact is
   being made, but it is one-sided"). Static objects produced either borrowed physics
   (f, d) or the staging-as-event (j: "it is being presented") or a silent conversion to
   identity.

9. **A "stable" level moved between cohorts.** A1's two viewers called image g an
   invented script; A2's five independent viewers unanimously called it mirrored
   English. Same file. The format level — A1's most stable — turned out to be stable
   within a cohort, not across them. Viewer history reached a level the single-cohort
   data had shown as solid.

## Explanations (held separately, tentative)

- The five questions may name different OPERATIONS rather than five aspects of one
  operation. Their collapse pattern is ordered: represent→is (for depictions),
  happening→is (absent an event), but for and mean never reduce inward. Some questions
  can be satisfied by looking; others structurally cannot, and are satisfied instead
  from the viewer's world. That would account for the contamination gradient without any
  appeal to viewer carelessness.
- The object-switching (Obs 3) reads like demand-driven selection: each question defines
  what a satisfying answer would need (an agent, a tool, a use, a message), and
  perception supplies the candidate that meets the demand. Akin to A1's
  anchor-then-translate, but here the anchor is chosen BY the question.
- The sign behavior suggests some formats carry their question with them: a prohibition
  sign IS an answer to "what does this mean," whatever is asked. Where A1 found
  re-leveling (answers migrating when one level fails), the sign shows pre-leveling —
  the format assigns the level before any question lands.

## Open questions

- IT and REPRESENT separated only at the sign and the scene — never for plain
  depictions. Is the depiction/symbol line not a property of images but a difference in
  WHICH QUESTIONS an image can distinguish?
- Did the happening question fail on objects because images cannot show time, or did it
  succeed secretly — by replacing the object with one that can act (the hand)? What is
  the difference between answering a question and changing the subject until the
  question fits?
- h/MEAN read the image as a symptom of its delivery system ("failed to load"). When
  does a viewer stop reading THROUGH an image and start reading it AS infrastructure?
  What flips that?
- Is the contamination gradient (it < represent < happening < mean < for) a fact about
  the questions, or about these viewers' training? Human data needed (below).
- The format level moved across cohorts (g). How many of A1's "stable" levels were
  cohort artifacts?
- The protected question stays protected — noting only that A2 multiplied it: in A1 one
  question behaved like many; in A2 five questions sometimes behaved like one
  (represent→is). Recorded, not worked on.

*No findings. Not earned.*

---

## Human session — PENDING

Per instruction, human viewers whenever available. One human viewer is available:
Jordan. Requested protocol (within-viewer version — sequence is deliberate and is
itself data; the model sessions above are the between-viewer version):

- Image: **d** (the oval — it traveled furthest for the model viewers).
- The five questions in order: What is it? / What does it represent? / What is
  happening? / What is this for? / What does this mean?
- First answer that comes, one or two lines each, no deliberation, no revisiting
  earlier answers.
- Marked as: HUMAN, maker-adjacent history (has seen the A1 contact sheet and knows the
  course exists). History is part of the experiment.

Responses will be appended here verbatim and never merged with the model grid.

---
Files: `generate.py` (cup/scene/sign), `cup.png`, `scene.png`, `sign.png`; images d–j
from `../a01/`. Sessions: 50 independent model viewers, 2026-06-04.
