# Brief for Chat — the new homepage (cover model) + how July plugs in

*From Cowork, 2026-06-07. Context handoff so you can shape July's essay to fit the
homepage direction we just landed. Everything below is built and viewable locally; none
of it is on the live homepage or committed to `main` yet — the live site still runs the
old hero + the "Half revealed." featured-moment block.*

**See it first:** open **http://localhost:3000/illustration-flow/final** in the browser
where Jordan's dev server is running (`npm run dev`). That's the approved direction. The
A/B/C/D sprint that got us there lives at `/illustration-flow/styled`, `/sprint-b`,
`/sprint-c`, `/sprint-d` if you want the comparison.

---

## 1. The big shift — the homepage is the cover

We reframed the homepage as a **magazine cover, not a landing page.** This is now a
doctrine amendment (drafted as **Amendment II**, "The Homepage Is the Cover,"
`doctrine-amendment-homepage-is-the-cover.md` in the repo root — Jordan approved it;
it still needs to be placed in the canonical Drive doc).

Two layers:

- **The masthead — permanent.** Wordmark, tagline, nav, typography, structure. *The
  standards stay.*
- **The cover — per issue (monthly).** One illustration, one cover story, one theme. *The
  selections change.*

One cover per issue. No rotation, no slideshow, no arc. The Mother's Day → Memorial Day →
Half Revealed swaps were already covers; this just names the system. One-line doctrine:
**the standards stay, the selections change.**

Governing model: **the essay is the content, the illustration is the room, the masthead is
the house, the monthly feature is the room we're currently occupying.** A framework meant
to carry July, August, Thanksgiving, January, a recipe issue, a grief essay — without
changing the system.

## 2. The page is the work, not the image

The most important principle from the sprint: Hessentials needs **great editorial pages
that happen to contain illustrations, not great illustrations.** The page composition
carries the emotional weight. Whitespace is doing real work — it reads as silence, not
emptiness. Do not fill it.

Page anatomy (top to bottom on `/illustration-flow/final`):

1. **Masthead** — wordmark + tagline "Life, edited well." + nav + a drawn hand-rule.
2. **The cover** — issue line ("June 2026") · cover-story title ("Half revealed.") ·
   the dek/question (italic) · "Read the essay →" · the made illustration, integrated.
3. **Currently** — four departments: *In the Kitchen / At Home / On the Table / In
   Practice*, each a short line + link.
4. **Closing whisper** — one italic line ("The year isn't half over. It's half
   revealed.") + a "JH" signature.

Contained, authored magazine page — **not** full-bleed. We explicitly rejected the
wall-to-wall hero image (it makes us look like every other editorial site).

## 3. The illustration direction (locked: "D + C")

- **Made, not captured.** Per the Hessentials Image Standard: reconstruct, never trace or
  filter. The cover is a *drawing*, not a photo or a photo run through a sketch filter.
  No simulated/“faked” construction or drafting marks (that violates the amendment).
- **Evidence only — no figures.** We tested a standing figure and removed it. The room is
  a mystery ("what happened here?") not a protagonist ("who is that?"). Evidence-only is
  inhabitable — the reader projects themselves in. June's cover is a bedroom told only by
  a bed, a half-packed bag at the threshold, a doorway, and light.
- **Embedded in the page.** The drawing's edges feather into the cream (`#f8f6f3`) so
  there's no image boundary — it reads as drawn onto the same sheet the type sits on.
- **Graphite on warm cream.** The light is the bare paper; soft shadow describes form; a
  whisper of warm only where the light falls.

Open question we're consciously sitting with: *how invisible can the illustration become
while still carrying emotional weight?* And the one real fork ahead — the actual covers
likely want a skilled human hand (or much more in-house drawing practice); the current
drawing is a faithful placeholder that proves the system.

## 4. What an "issue" needs — the July checklist

To plug July into the framework, July needs to supply exactly these, nothing more:

1. **Issue line** — "July 2026".
2. **Cover-story title** — sentence case, the essay's title (e.g., the way "Half
   revealed." reads).
3. **The dek / the question** — one or two italic sentences. This is the *question the
   essay asks*, not a summary.
4. **The cover illustration concept** — a single room/scene, **evidence only, no
   figures**, that carries the feeling and illustrates the *question, not the article*
   ("something happened here," without revealing what). Describe the room + the few traces
   so Cowork can draw it (made, graphite on cream).
5. **"Read the essay →"** (label can stay).
6. **Currently / departments** — the four lines (In the Kitchen / At Home / On the Table /
   In Practice) refreshed for the month, each one short line + a destination.
7. **The closing whisper** — one italic line, usually the essay's own pivot/thesis.
8. **The essay itself** — the long-form cover story, in brand voice, drafted against the
   relevant pillar spec.

## 5. Constraints to honor when drafting July

- Voice: warm melancholy felt not performed; evidence over interpretation; **refuses to
  signify** — no Statement, no Image-with-a-message. Avoid the filler words (curated,
  thoughtful, intentional, elevated, luxe, vibes, journey, mindful).
- Typography: sentence case preserved in titles/headers; em dashes spaced ( word — word ),
  en dashes for ranges ( July 1–7 ), hyphens only for compounds.
- The cover art illustrates the **question**, and is evidence-only / no figures / made-not-
  captured. If July's feeling wants a different room, that's the selection changing — the
  system holds.
- Remember the division of labor: **Chat writes the spec; Cowork executes.** Hand the July
  issue back as a spec and Cowork builds + verifies against the real files.

## 6. Status

All prototype, local only, uncommitted. Live homepage unchanged. Once July proves the
framework survives new content, the next step is porting this to the live homepage as a
clean commit for Jordan to push.
