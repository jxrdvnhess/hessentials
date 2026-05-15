# Hessentials sourcing policy

Operating doctrine for how products enter the Hessentials archive. Written by Chateau on 2026-05-14 in response to the pending-list pattern analysis (see `data/shop-pending-analysis.md`). This document is canonical — future sourcing decisions reference back to it.

---

## The three simultaneous filters

The Shop is not a commerce layer. It is the physical manifestation of the Hessentials worldview. Every object now has to pass all three of these simultaneously:

1. **Editorial correctness** — does it earn its place under the Standard's product filter
2. **Emotional durability** — will it still feel correct a year from now
3. **Operational durability** — does the retailer's architecture support a long-term archive entry

None of those can collapse without damaging trust.

---

## The six doctrines

Locked in 2026-05-14. These govern every sourcing and curation decision from here forward.

1. **Density over breadth** — permanent doctrine. The archive deepens into trusted territories rather than expanding sideways.
2. **Tier 1 deepening over horizontal hunt** — see [`data/tier-1-brands.md`](./tier-1-brands.md). New products in known stable brands beat new brands in unknown territory.
3. **Atmosphere collections over retail taxonomy** — products group by emotional territory and lived-object logic, not department-store category trees.
4. **Cross-tagging follows lived-object logic, not department-store logic** — a heavyweight tee is both a basic AND a layer; categorize by how it's actually used, not which retail floor it'd sit on.
5. **Article objects and Shop objects must remain continuous** — no dead-end editorial references. Anything mentioned in an article body should have a live Shop entry or a deliberate editorial reason it doesn't.
6. **"Stable enough to survive long-term archival existence" is part of the editorial standard itself** — operational fragility is not a separate concern from editorial quality. They're the same concern.

---

## The frame

We need to stop thinking like: "find the best product."
And start thinking: "find the best product that can survive operationally inside a long-term archive."

That is a MASSIVE distinction.

Some incredible products are simply not worth the maintenance burden if:

- anti-bot systems break pricing
- structured data is garbage
- image galleries don't parse
- product pages constantly rotate
- URLs redirect unpredictably
- retailer architecture is unstable

That operational instability eventually damages trust.

## The operational law

**Prefer brand-direct over reseller unless the brand site itself is bot-walled.**

This is Hessentials Operational Law. Not just editorial law.

---

## The four tests for any new shop entry

Aesthetic alignment is no longer enough. Every product must pass:

1. **Aesthetic alignment** — does it fit the editorial register?
2. **Emotional alignment** — does it earn the Standard's product filter?
3. **Operational stability** — does the retailer's architecture support a long-term link?
4. **Structured-data reliability** — does JSON-LD / OG ship the product name, price, gallery?
5. **Image scrape reliability** — does the gallery actually parse?
6. **Canonical URL reliability** — does the URL stay put across the year?

---

## Anti-bot retailers — operationally blacklisted

These brands can exist editorially, but should almost never be operational dependencies:

- Aritzia
- Tod's
- Lululemon
- West Elm
- Zara Home
- Williams Sonoma
- AllSaints

Meaning:

- maybe mention in articles
- maybe manual image entries occasionally
- but NOT foundational shop infrastructure

The bulk import script warns at import time when a row's URL belongs to one of these. The warning is non-blocking — an override path exists for the rare case where manual entry is worth the maintenance burden — but the default answer should be: source from somewhere else.

---

## Forever Infrastructure Brands

The skeleton of the Shop. Brands with:

- stable SKUs
- stable URLs
- stable identity
- stable collections
- stable ecommerce
- stable image systems

Current foundation:

- East Fork
- Hawkins NY
- Snow Peak
- Fog Linen
- Minna
- Material Kitchen
- Farmhouse Pottery
- Filson
- Jacobsen Salt
- Leatherology

Not because they're trendy. Because they're stable, clear, direct, parseable, permanent. They earn their place as core infrastructure.

Layer seasonal discoveries, artisan finds, smaller makers, and emotional objects ON TOP of this stable foundation. Not instead of it.

The running, updated Tier 1 Expansion List with category coverage, gaps, and watch-list candidates lives at [`data/tier-1-brands.md`](./tier-1-brands.md).

---

## The distributor insight

Sometimes the best Hessentials link is:

- not the original brand
- not the biggest retailer
- but the cleanest operational source

Especially for:

- Japanese brands (Fog Linen via Heath, Rikumo, Of A Kind)
- artisan ceramics
- Scandinavian utilities
- linen makers
- lighting studios

When the original brand site doesn't ship English structured data or stable URLs, find the US distributor that does.

---

## What stays manageable

"Thin but fixable" is fine.

Sparse structured data, weak image galleries, missing price fields — those are human QA problems, not systemic instability problems. Schoolhouse, Coyuchi, MUJI, Jacobsen, Il Bisonte and others sit here. They just need manual polishing on `/admin/shop-edit/<slug>`.

---

## What this changes

We are not building a commerce scraper. We are building a curated object archive with technical durability.

Every object now has:

- editorial quality
- emotional quality
- operational quality

All three matter equally.

---

## Sourcing checklist — print and tape above the desk

Before adding a URL to the master CSV:

1. Open the URL in a fresh incognito tab. Confirm the product name renders in the title bar.
2. Check if the retailer is on the anti-bot blacklist above. If yes, look for an alternate source first.
3. View page source (`Cmd+U`). Search for `application/ld+json`. Confirm the JSON-LD `Product` block exists with `name`, `image`, `offers`.
4. Prefer brand-direct unless the brand site is bot-walled.
5. For non-English brands, find a US distributor.

If a candidate fails 1-3, do not add it. Restraint is the answer.

---

## Current phase plan

Locked 2026-05-14. The work between now and the revamp launch is:

1. **Clean the foundation** — finish the editorial pass on remaining drafts and pending entries. Fix em-dashes, wrong-URL audit rows, SEO-blob names.
2. **Strengthen Tier 1 density** — close gaps in the Current Tier 1 brands and elevate candidates per [`data/tier-1-brands.md`](./tier-1-brands.md).
3. **Expand atmosphere collections** — group products by emotional territory (the per-brand territories in the Tier 1 doc) rather than retail taxonomy. World-building, not product accumulation.
4. **Build the cleanest possible canonical import CSV** — the new schema (with `manual_images` + `stability_tier`) becomes the single source of truth Chateau works in.
5. **Launch the revamp with emotional coherence, not maximum inventory** — better objects, chosen slowly, kept longer.

---

## Article ↔ Shop continuity — the `shop_refs` convention

Doctrine 5 forbids dead-end editorial references. Operationalized as follows.

Every article that references an object available in the Shop must declare the connection explicitly in its frontmatter:

```yaml
---
title: Ditch the coffee machine. Get an espresso machine.
slug: ditch-the-coffee-machine-get-an-espresso-machine
category: living
section: Systems
shop_refs:
  - breville-the-bambino
  - breville-the-barista-express
  - baratza-suggested-encore-esp
---
```

The values are Shop slugs from `src/data/shop.ts`. Writers consciously decide which objects belong to each article's world before publishing — that's the editorial friction we want. The archive stays authored, not auto-inferred.

Post-launch, `scripts/check-article-shop-continuity.mjs` will become the auditor: walk every article, verify each declared `shop_ref` corresponds to a live Shop entry, and report orphans. The frontmatter remains the source of truth; the script is the QA layer.

Existing articles will be backfilled incrementally as they're touched. Until then, the lack of `shop_refs` on an old article is not a failure — it's a marker for future editorial passes.

---

## Launch-facing atmosphere collections

Per Chateau's 2026-05-15 post-live audit, these atmospheres are the foreground set — what surfaces on the Shop homepage as the emotional front door. Operational categories sit beneath. Source of truth: `src/data/atmospheres.ts`.

1. Soft Travel
2. Kitchen Counter Objects Worth Leaving Out
3. The Good Lamp Rule
4. Things That Improve a Tuesday
5. Hotel Energy at Home
6. Quiet Uniform
7. Pantry Rituals
8. Portable Ritual
9. Correct Low
10. Warm Minimalism
11. Weeknight Table
12. Rainy Morning Objects
13. Useful Beauty
14. Object With Memory
15. Things That Age Correctly

Other atmospheres referenced in products' `atmosphereCollection` arrays still render via the dynamic `/shop/atmosphere/[slug]` route — they just don't lead the homepage. New atmospheres earn launch-facing status when the sourcing density justifies it.

---

## Architectural direction (post-launch)

Eventually every Shop object inherits three orthogonal dimensions, not just one:

1. **Category** — the operational taxonomy (`mens`, `home`, `travel`, etc.)
2. **Atmosphere collection** — emotional grouping that cuts across category (Morning Ritual, Soft Travel, Weeknight Table, Hotel Energy at Home)
3. **Tier 1 territory weather** — the emotional climate of the brand that made it

A Snow Peak titanium mug lives in:

- **Category**: Travel / Coffee / Outdoor
- **Atmosphere**: Morning Ritual, Portable Ritual
- **Territory**: soft travel / outdoor calm / analog movement (Snow Peak)

That's where the archive starts feeling alive instead of hierarchical. Not built yet — wait for the editorial ask.

---

## The closing principle

The constraints are sharpening the philosophy instead of weakening it. Anti-decay is becoming one of Hessentials' strongest differentiators.

The reader should feel that Hessentials already filtered the noise for them.

Not: more products.

Better objects. Chosen slowly. Kept longer.

**The emotional product is: relief from noise.**

Not the tote, the mug, the blanket, the lamp.
