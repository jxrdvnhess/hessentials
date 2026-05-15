# Tier 1 Expansion List

Running internal list of brands the archive intentionally deepens into. Per Chateau (2026-05-14): not products — brands. The skeleton of the Shop.

A Tier 1 brand passes all four of the sourcing-policy tests:

1. Aesthetic + emotional alignment with the editorial register
2. Operational stability (stable SKUs, stable URLs, no anti-bot wall)
3. Structured-data reliability (JSON-LD `Product` + `offers` + `image` ships consistently)
4. Image scrape reliability (gallery parses)

The strategy: stable foundation + rotating discoveries layered on top. Density over breadth. Density creates world-building.

This list is living. Brands enter when they prove durable across a sourcing cycle; brands exit when they break any of the four tests. Updates here should be paired with `stability_tier: 1` on the corresponding shop entries.

---

## Emotional territories

A Tier 1 brand should anchor an emotional territory inside the archive — not just a category. The territory is what makes density create world-building instead of product accumulation. Reader-side, the territory should feel coherent: the same warm undertone across every product carrying that brand.

Per Chateau (2026-05-14):

| Brand | Emotional territory |
|---|---|
| Snow Peak | soft travel / outdoor calm / analog movement |
| Hawkins New York | table softness / linen texture / understated hosting |
| Filson | weather / canvas / patina / durable movement |
| East Fork | morning ritual / bowls / ceramic permanence |
| Fog Linen Work | lived-in utility / brass / imperfect texture |
| Material Kitchen | countertop clarity / soft utility / daily prep |
| Leatherology | quiet transit / structured calm / personal order |
| Heath Ceramics | California light / stoneware permanence / architectural warmth |
| Farmhouse Pottery | kitchen ritual / handmade utility / ceramic warmth |
| Felt + Fat | espresso ritual / tactile mornings / intimate utility |
| Coyuchi | washed cotton / softened light / quiet rest |
| Diaspora Co. | pantry depth / spice warmth / grounded flavor |
| Opinel | picnic utility / pocket ritual / weathered simplicity |

The pattern: a short three-to-five-word phrase that captures the emotional weather a reader should feel when they see anything from that brand. Categories describe what something is. Territories describe what it feels like to live with. Sensory, atmospheric, slightly cinematic, but restrained.

---

## Current Tier 1 — currently in the archive

| Brand | Emotional territory | Category coverage | Live entries |
|---|---|---|---|
| **Hawkins New York** | table softness / linen texture / understated hosting | Home / Table / Dining | 2 |
| **Filson** | weather / canvas / patina / durable movement | Travel / Bags / Weekend | 2 |
| **Material Kitchen** | countertop clarity / soft utility / daily prep | Home / Kitchen / Prep | 2 |
| **Leatherology** | quiet transit / structured calm / personal order | Travel / Organization | 2 |
| **Heath Ceramics** | California light / stoneware permanence / architectural warmth | Home / Objects / Flowers | 1 |
| **Farmhouse Pottery** | kitchen ritual / handmade utility / ceramic warmth | Cooking / Kitchen Counter / Ceramics | 2 |
| **Felt + Fat** | espresso ritual / tactile mornings / intimate utility | Cooking / Coffee / Ceramics | 2 |
| **Coyuchi** | washed cotton / softened light / quiet rest | Home / Bedroom / Bath | 2 |
| **Diaspora Co.** | pantry depth / spice warmth / grounded flavor | Cooking / Pantry / Spices | 1 |
| **Opinel** | picnic utility / pocket ritual / weathered simplicity | Cooking / Picnic / Travel | 1 |

## Tier 1 candidates — Chateau-named, not yet in archive

These are the brands Chateau identified as the operational skeleton but the archive doesn't carry yet (or carries thinly). Each represents a deliberate expansion direction, not a random hunt.

| Brand | Why Tier 1 | Suggested entry direction |
|---|---|---|
| **East Fork** | Stable SKUs, clean JSON-LD, deep ceramicist density | Bowls, mugs, side plates — the Tier 1 dinnerware anchor we don't have yet |
| **Snow Peak** | Stable, clean structured data, travel/outdoor register fits | Titanium cups, mugs, picnic objects (note: Ti-Single 450 and Ti-Double 450 are in pending — promote when reviewed) |
| **Fog Linen Work** | Japanese textile authority; route via US distributor (Heath / Rikumo / Of A Kind) for English structured data | Brass trays, linen napkins, kitchen linens |
| **Minna** | Mexican-loomed textiles; small studio, clean site | Throws, runners, napkins — gaps in the table register |
| **Schoolhouse** | Stable, clean structured data, lighting + hardware authority | Lighting fixtures, hardware, utility cart (3 entries currently in pending — promote when polished) |
| **Jacobsen Salt Co.** | Stable Shopify, finishing salt register | Flake salt, slide tin (in pending) |
| **L.L.Bean** | Generational stability, canvas tote heritage | Boat & Tote variants, canvas duffles |

## Watch list — brands worth tracking but not yet validated

These could become Tier 1 with one good sourcing cycle. The pre-flight ritual catches them either way.

- **Burlap & Barrel** — single-origin spices; one cycle through the sourcing ritual would confirm
- **Brightland** — flagged for performative-taste risk per the 2026-05-14 audit; if it earns its place, Tier 2 at best
- **Felt + Fat** — already in archive but small catalog; deepening would push toward Tier 1 density

## Anti-Tier 1 — operational blacklist

These have explicit anti-bot infrastructure or fundamentally unstable URL patterns. Per the sourcing policy:

- Aritzia
- Tod's
- Lululemon
- West Elm
- Zara Home
- Williams Sonoma
- AllSaints

Can appear in editorial copy. Should not be the Shop's load-bearing infrastructure.

---

## How to use this list

**When sourcing new items.** Prefer a Tier 1 deepening over a brand-new discovery, unless the discovery is genuinely additive. Editorial coherence beats variety.

**When auditing.** Entries from Tier 1 brands carry `stability_tier: 1` in the data file. The drafts admin and the bulk-import script can be filtered by tier in future tooling if needed (not built yet — wait for the actual ask).

**When a Tier 1 brand breaks a test.** If a brand starts shipping unstable URLs, gating with anti-bot, or losing structured data, move it to Tier 2 / 3 / 4 in this doc AND in the shop entries' `stability_tier` field. Don't pretend the brand is still Tier 1.

**When a candidate proves out.** After one successful sourcing cycle through the pre-flight ritual (5+ entries staged cleanly via `manual_images` and clean JSON-LD), promote from Candidate → Current.
