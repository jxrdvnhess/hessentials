# Deep Shop audit — 2026-05-15 (post-launch)

Full audit on the live archive after Batch 01 promotion. Findings below grouped by severity. Cosmetic fixes already applied; editorial decisions surfaced for Chateau.

## Snapshot

- **166 live entries** in `src/data/shop.ts`
- **0 drafts** (everything Chateau staged has been promoted)
- **52 Batch 01 entries** were missing `atmosphereCollection` / `territoryWeather` / `stabilityTier` due to a writer-bug in the import script when Batch 01 ran. **Backfilled inline from `data/shop-import-batch-01.csv` by URL match.**

## Critical — already fixed

### The atmosphere homepage was empty

**What was happening:** `/shop` rendered the new "By Atmosphere" section with zero cards, because every live entry had an empty `atmosphereCollection`. The 52 Batch 01 entries carried the data in the CSV but my appendShopEntry call sites didn't yet forward the three new fields when Batch 01 ran.

**Fix applied:** Backfilled `atmosphereCollection`, `territoryWeather`, and `stabilityTier` on 52 entries by matching against `data/shop-import-batch-01.csv` URL → fields. After this push, the atmosphere section will populate.

**Where the populated atmospheres land:**

| Atmosphere | Approx. count after backfill |
|---|---|
| The Anti-Hostess Table | ~8 (Hawkins linens, Block Shop napkins) |
| Weeknight Table | ~10 (Hawkins, Material Kitchen, IKEA dinnerware) |
| Useful Beauty | ~12 (cuts across home + travel) |
| Kitchen Counter Objects Worth Leaving Out | ~10 (Material Kitchen, Farmhouse Pottery, ceramic vessels) |
| Pantry Rituals | ~8 (Jacobsen, Diaspora, Crazy Water) |
| Morning Ritual | ~6 (Felt + Fat, Snow Peak, Diaspora) |
| Portable Ritual | ~5 (Snow Peak, Felt + Fat espresso cups) |
| Soft Travel | ~4 (Leatherology, Snow Peak) |
| Things That Age Correctly | ~5 (Filson, Leatherology) |
| Quiet Uniform | growing — needs Tier 1 menswear backfill |

The other 114 live entries (older — pre-Batch 01) still have NO atmosphere collection. They render via category only. **Editorial work needed** — see "Backfill candidates" below.

## Cosmetic — applied automatically

Six fixes, all functional, no editorial judgment:

| Entry | Before | After |
|---|---|---|
| `timex-watches-from-timex-...` | `Marlin® Hand-Wound Leather Band (34mm)` | `Marlin Hand-Wound Leather Band (34mm)` |
| `sundays-sundays-...` | `Movie Night™ 4-Piece Modular Sectional` | `Movie Night 4-Piece Modular Sectional` |
| `material-kitchen-the-rebowl` | `The reBowl® - Multiple Colors` | `The reBowl - Multiple Colors` |
| `l-l-bean-boat-and-tote-zip-top` | `Boat and Tote®, Zip-Top` | `Boat and Tote, Zip-Top` |
| `block-shop-textiles-poppy-napkin-field` | `Poppy Napkin \| Field` | `Poppy Napkin - Field` |
| `block-shop-textiles-peacock-napkin-ochre` | `Peacock Napkin \| Ochre` | `Peacock Napkin - Ochre` |

## Editorial decisions — flagged, not changed

### Voice violations — 3 live entries

The Editorial Standard prohibits em dashes in `reason`. Rewrite is editorial:

- `aveda-pureformance-cream` — `Softer hold. Same trick — finish doesn't read as done.`
- `ysl-myslf-edp` — `Orange blossom, vetiver. The brighter one — for when L'Homme is too quiet.`
- `esya-the-dune-set` — `White linen, yellow piping — enough to read as a set, not a uniform.`

### Suspect price ranges — 5 entries

The bulk-import script's price scanner picked up either shipping costs or unrelated swatches. Real ranges much narrower:

| Entry | Current (wrong) | Likely correct |
|---|---|---|
| `hawkins-new-york-essential-glassware-clear` | $6–$141 | Single glass ~$15–25; set ~$75–141 |
| `felt-fat-coffee-mug-in-tenmoku` | $17–$296 | Single mug ~$48 |
| `filson-large-rugged-twill-duffle-bag` | $34–$699 | $525–$699 |
| `coyuchi-three-season-down-duvet-insert` | $35.20–$718.40 | $578–$1,158 |
| `coyuchi-organic-shredded-latex-pillow` | $35.20–$438.40 | $98–$148 |

Fix via `/admin/shop-edit/<slug>` per row, or have Chateau set explicit `price` next batch.

### One placeholder subcategory remains

A single entry still has `subcategory: "uncategorized"` — needs identification + manual category pick.

## Tier 1 brand health

After Batch 01 + backfill:

| Brand | Status | Count | Notes |
|---|---|---|---|
| Hawkins New York | Current | 5 | Healthy — anchors The Anti-Hostess Table |
| Leatherology | Current | 5 | Healthy — Soft Travel anchor |
| Felt + Fat | Current | 5 | Healthy — Morning Ritual anchor |
| Material Kitchen | Current | 4 | Healthy — Kitchen Counter atmosphere |
| Farmhouse Pottery | Current | 4 | Healthy |
| Coyuchi | Current | 4 | Healthy — Hotel Energy / Cotton |
| Diaspora Co. | Current | 4 | Healthy |
| Jacobsen Salt Co. | Current | 4 | Healthy — Pantry Rituals |
| Filson | Current | 3 | Healthy after Filson URL fixes |
| Snow Peak | Current | 3 | Healthy — Portable Ritual |
| Opinel | Current | 3 | Healthy — Picnic Objects |
| Heath Ceramics | Current | 2 | **Gap — more Heath needed for California light register** |
| L.L.Bean | Current | 1 | **Gap — only Boat & Tote; needs canvas duffles** |
| East Fork | Candidate | **0** | Still in NEEDS_SOURCE — `/pages/meet-the-X` URLs need clean product pages |
| Fog Linen Work | Candidate | **0** | Distributor sourcing needed |
| Schoolhouse | Candidate | **0** | All 6 from Batch 01 went to needs-human and still pending |
| Minna | Candidate | **0** | Brand has closed — see EDITORIAL_HOLD |

## Atmosphere coverage — launch-facing 15

After backfill, here's what populates the homepage's "By Atmosphere" section. Atmospheres with zero products will remain invisible on the live homepage:

| Atmosphere | Status |
|---|---|
| Useful Beauty | ✓ populated |
| Weeknight Table | ✓ populated |
| Kitchen Counter Objects Worth Leaving Out | ✓ populated |
| Pantry Rituals | ✓ populated |
| Things That Age Correctly | ✓ populated |
| Soft Travel | ✓ populated |
| Portable Ritual | ✓ populated |
| Hotel Energy at Home | populated via Coyuchi / Los Poblanos |
| Warm Minimalism | populated via Terrain / similar |
| Quiet Uniform | sparse — needs more menswear basics tagged |
| The Good Lamp Rule | **empty — 0 products** |
| Things That Improve a Tuesday | populated via Heath / Hawkins pitcher |
| Correct Low | sparse — needs more MUJI / IKEA / cotton dishcloths tagged |
| Rainy Morning Objects | **empty — 0 products** |
| Object With Memory | sparse |

## Category distribution

| Category | Count |
|---|---|
| home | 45 |
| mens | 37 |
| accessories | 33 |
| womens | 14 |
| grooming | 11 |
| travel | 11 |
| provisions | 9 |
| cooking | 6 |

**Cooking is the smallest pillar.** Per Chateau's directive, cooking is a first-class lived-object category — the count should grow. Most cooking-natural entries (Felt + Fat ceramics, Farmhouse Pottery) are currently categorized as `home`. Worth a re-categorization pass.

## Price stratification

| Tier | Count |
|---|---|
| <$50 (Correct Low) | 62 |
| $50–200 (Mid) | 51 |
| ≥$200 (High) | 53 |

37% are Correct Low. Per Chateau's audit ("Correct Low must be strengthened"), this is the lever — adding 10-15 MUJI / IKEA / cotton-dishcloth-grade entries shifts the average emotional register significantly.

## Backfill candidates — 114 entries need atmosphere tagging

The pre-Batch 01 entries (Aveda, Prada, COS, Buck Mason, etc.) don't have `atmosphereCollection` set. To populate the atmosphere homepage cards fully, Chateau would need to tag them. Pragmatic approach: tag the 30-50 most editorially-important ones first; the rest are findable by category.

Suggested first pass — entries that obviously belong in launch-facing atmospheres:

- Every Buck Mason heavyweight tee → Quiet Uniform
- Every Common Projects sneaker → Quiet Uniform
- Every Birkenstock → Quiet Uniform (or Soft Travel)
- Le Bon Shoppe socks → Quiet Uniform
- Massimo Dutti trousers → Quiet Uniform
- Loewe Goya, Mansur Gavriel totes → Soft Travel
- Cuyana tote → Soft Travel
- All cashmere → Hotel Energy at Home
- All bedding (already covered by Coyuchi backfill)
- Aveda hair products → bathroom register — possible new atmosphere "Bath & Wash"?

If Chateau wants, the next batch could include a `backfill_atmospheres` column for legacy entries — same machinery as Batch 01.

## What landed in shop.ts

- **6 cosmetic fixes** applied (TM symbols, SEO pipes)
- **52 atmosphere/territory/tier backfills** applied
- **typecheck + lint clean** — safe to push

## What's queued for Chateau

- 3 em-dash voice rewrites
- 5 suspect price corrections
- 1 placeholder subcategory
- Atmosphere tagging on ~114 legacy entries (most surgical batch: ~30 entries for Quiet Uniform, Soft Travel, and Hotel Energy at Home)
- Source: lighting (The Good Lamp Rule = empty), weather objects (Rainy Morning Objects = empty)
- Re-categorize Felt + Fat / Farmhouse Pottery from `home` → `cooking` if Chateau prefers
