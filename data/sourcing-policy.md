# Hessentials sourcing policy

Operating doctrine for how products enter the Hessentials archive. Written by Chateau on 2026-05-14 in response to the pending-list pattern analysis (see `data/shop-pending-analysis.md`). This document is canonical — future sourcing decisions reference back to it.

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
