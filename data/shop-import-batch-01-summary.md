# Sourcing Batch 01 — summary

Source: `Hessentials_Object_Archive_Sourcing_Batch_01.xlsx` (Chateau, 2026-05-15)
Converted CSV: `data/shop-import-batch-01.csv`

---

## Snapshot

| Tab | Rows | Disposition |
|---|---|---|
| READY_TO_IMPORT | 67 | Sourced + pre-vetted by Chateau. Bulk-import script runs pre-flight (HTTP / JSON-LD) on each. |
| NEEDS_SOURCE | 6 | URL not yet clean (landing page, collection page, missing). |
| NEEDS_MANUAL_IMAGES | 0 | None this batch. |
| EDITORIAL_HOLD | 5 | Decisions pending — see below. |
| REMOVE_OR_ARCHIVE | 3 | Removed for reasons noted below. |
| CATEGORY_ATMOSPHERE_MAP | 24 | Atmosphere collections expanded — reference for the data model. |
| TIER_1_BRANDS | 20 | Status updated per-batch. |
| ARTICLE_SHOP_REFS | 0 | Empty — populate post-launch. |

---

## READY_TO_IMPORT — Tier 1 density by brand

This batch is heavy on Tier 1 deepening — that's the doctrine working.

| Brand | Rows this batch | Notes |
|---|---|---|
| Hawkins New York | 4 | Linen napkins, glassware, pitcher — anchors table register |
| Material Kitchen | 4 | Prep boards (Angled, MK Free, Midi MK Free, Rebowl) |
| Snow Peak | 7 | French press, titanium mug, pour-over, drip, lantern (×2), beach chair |
| Farmhouse Pottery | 4 | Olive oil bottle, garlic keeper, silo pitchers, pantry bowl |
| Felt + Fat | 4 | Espresso cup, mug × 2 colorways, large mug, cappuccino cup |
| Jacobsen Salt | 4 | Flake salt, slide tin, salt cellar (×2) |
| Diaspora Co. | 4 | Pragati turmeric, trio tin, whole seeds trio, haldi doodh |
| Schoolhouse | 6 | Miller utility cart, Sidnie lamp, Alabax sconce, Perkins hook mirror, Eleanor pull, G40 bulb |
| Filson | 3 | Large duffle, medium duffle, tote-with-zipper |
| Leatherology | 3 | Travel organizer, nested trio, tech bag |
| L.L.Bean | 2 | Boat & Tote (×2) |
| Heath Ceramics | 2 | Bud vase (×2 colorways) |
| Coyuchi | 2 | Down duvet insert, organic latex pillow |
| Opinel | 3 | No.08 carbon, No.08 stainless, slide-top w/ olive wood handle |
| IKEA | 2 | FÄRGKLAR dinnerware (set + plate, matte light turquoise) |
| MUJI | 3 | Planting tree paper notebook, PET underlay, recycled polypropylene basket |
| Purely Sedona | 2 | 1L artesian spring water (×12), 500ml |
| Los Poblanos | 4 | Lavender hand soap, piñon bar soap, home duo gift set, lavender on-the-go |
| Block Shop Textiles | 4 | Otto, Dolly, Poppy, Peacock napkins |

---

## NEEDS_SOURCE — 6 rows waiting on clean URLs

| Brand | Item | Current URL | Issue |
|---|---|---|---|
| East Fork | The Mug | `eastfork.com/pages/meet-the-mug` | "Meet the X" landing page, not a classic product page. Needs operational test. |
| East Fork | Everyday Bowl | `eastfork.com/pages/meet-the-everyday-bowl` | Same |
| East Fork | Dinner Plate | `eastfork.com/pages/meet-the-dinner-plate` | Same |
| East Fork | Side Plate | `eastfork.com/collections/dinnerware` | Collection-level URL — needs specific product page or approved stockist |
| Weck | Classic Jar | `weckjars.com/shop/` | Shop/category only — find exact jar product page |
| Crazy Water | No. 4 | _(none)_ | Need direct product page from current official seller |

**Action:** these don't go through bulk import. Either source a cleaner URL and add to READY_TO_IMPORT, or accept manual entry through `/admin/shop-import`.

---

## EDITORIAL_HOLD — 5 rows pending decision

| Brand | Item | Why on hold |
|---|---|---|
| **Minna** | Handwoven Throws / Napkins | **Brand has closed.** Emotionally perfect but unstable launch source. Don't use as launch infrastructure unless a stable authorized stockist with current inventory is chosen. |
| **Brightland** | Awake Olive Oil | Bottle-as-object reasoning risks performative pantry energy. Tier 2 at best; keep only if copy centers taste and use, not visibility. |
| **Purely Sedona** | Glass Bottled Water | Jordan loves the glass-bottle version, but current product pages show plastic + AZ-limited shipping. Find glass-bottle SKU or mark as prose-only / local provision. |
| **Alo Yoga** | Triumph Bomber | Activewear-coded; only works if article context specifically needs softness over tailoring. Chateau leans remove. |
| **Sephora** | Vetiver Anchor | Too broad as an anchor. Name a specific house (Guerlain, Le Labo) or remove. |

---

## REMOVE_OR_ARCHIVE — 3 rows out

| Brand | Item | Why removed |
|---|---|---|
| **Theory** | Clinton Blazer | Discontinued / unstable. Archive rather than forcing a worse substitute. |
| **Michael Kors** | Marilyn Medium Tote | "Mall-luxury residue / off-price signal." Fails emotional durability. |
| **AllSaints** | Brody Leather Low Top | Anti-bot + the row caused Veja/AllSaints brand confusion in the prior batch. If sneaker logic remains, source Veja direct. |

---

## CATEGORY_ATMOSPHERE_MAP — what's new vs. policy doc

Chateau's tab has 24 atmosphere collections. Worth checking for additions vs. what's listed in `data/sourcing-policy.md`. New / refined collections to watch for:

- **Table Atmosphere** (general, may overlap with Weeknight Table / Anti-Hostess Table)
- **Better Hotel Energy** (variant of "Hotel Energy at Home")
- **Daily Prep** (Material Kitchen territory)
- **Ceramic Permanence** (East Fork, Felt + Fat)
- **Woven Warmth** (Minna, Block Shop)
- **Regional Provisions** (Crazy Water, Purely Sedona, Los Poblanos)
- **Texas Objects** (regional anchor — Crazy Water, possibly more)
- **Desert Calm** (Los Poblanos, Sedona)

If these stabilize across batches, they should move into `data/sourcing-policy.md`'s atmosphere collection list as canonical. For now they live on individual entries via the new `atmosphere_collection` field on `ShopProduct`.

---

## Pre-flight outcome (to be filled after `--commit` runs)

Run on Jordan's machine:

```
cd ~/hessentials
node scripts/shop-bulk-import.mjs --csv=data/shop-import-batch-01.csv              # dry-run preview
node scripts/shop-bulk-import.mjs --csv=data/shop-import-batch-01.csv --commit     # stage drafts
```

Expected disposition per row gets recorded in `data/shop-bulk-import-report.json`. Pending entries land in `data/shop-import-pending.json`. Anything that needs Chateau editorial review lands in `data/shop-import-needs-chateau.md` (if dead URL) or on `/admin/shop-drafts → Pending`.

---

## Notes for the next batch

1. The new `atmosphere_collection` and `territory_weather` columns now persist into `shop.ts`. Public detail pages can surface them later (post-launch architectural direction).
2. The script honors Chateau's `slug` and `subcategory` columns. The placeholder `uncategorized` only fires when she doesn't provide one.
3. Gender tags are parsed: `all` / `gender-neutral` → `["mens", "womens"]`, `men` → `["mens"]`, etc.
4. Anti-bot warning fires inline if a URL hits the blacklist hosts.
