# Shop audit — 2026-05-14

Walked every entry in `src/data/shop.ts`. Cosmetic fixes already applied; editorial decisions surfaced below for your call.

## Current state

- **128 total entries** in shop.ts
- **117 live** (filtered to the public Shop)
- **11 drafts** (waiting on `/admin/shop-drafts`)

You promoted 32 entries during your earlier session — good clip.

---

## Cosmetic fixes applied automatically

18 changes. All purely functional — no editorial judgment. The script ran them inline; lint and typecheck both pass.

### Trademark / registered symbols stripped from names

| Slug | Before | After |
|---|---|---|
| `breville-the-bambino` | `the Bambino®` | `the Bambino` |
| `breville-the-barista-express` | `the Barista Express®` | `the Barista Express` |
| `baratza-suggested-encore-esp` | `Encore™ ESP` | `Encore ESP` |

### Brand cruft cleanup

| Slug | Field | Before | After |
|---|---|---|---|
| `baratza-suggested-encore-esp` | brand | `Baratza (suggested)` | `Baratza` |
| `scalperscompany-contrast-travel-bag` | brand | `scalperscompany` | `Scalpers` |

### SCREAMING UPPERCASE product names → title case

| Slug | Before | After |
|---|---|---|
| `soeur-blue-imani-dress` | `BLUE IMANI DRESS` | `Blue Imani Dress` |
| `soeur-grey-hyacinthe-coat` | `GREY HYACINTHE COAT` | `Grey Hyacinthe Coat` |
| `soeur-grey-ila-tank-top` | `GREY ILA TANK TOP` | `Grey Ila Tank Top` |
| `scalperscompany-contrast-travel-bag` | `CONTRAST TRAVEL BAG` | `Contrast Travel Bag` |
| `scalperscompany-fine-knit-cardigan` | `FINE KNIT CARDIGAN` | `Fine Knit Cardigan` |
| `scalperscompany-hoodie-with-front-pocket` | `HOODIE WITH FRONT POCKET` | `Hoodie with Front Pocket` |
| `esya-the-dune-set` | `THE DUNE SET` | `The Dune Set` |
| `favorite-daughter-the-striped-triangle-scarf` | `THE STRIPED TRIANGLE SCARF` | `The Striped Triangle Scarf` |
| `cos-linen-popover-shirt` | `LINEN POPOVER SHIRT` | `Linen Popover Shirt` |
| `cos-jersey-tank-top` | `JERSEY TANK TOP` | `Jersey Tank Top` |
| `cos-boat-neck-cotton-t-shirt` | `BOAT-NECK COTTON T-SHIRT` | `Boat-Neck Cotton T-Shirt` |

### SEO suffix stripped from names

| Slug | Before | After |
|---|---|---|
| `apieceapart-volta-twist-top-apiece-apart` | `Volta Twist Top \| Apiece Apart` | `Volta Twist Top` |
| `veja-brody-leather-low-top-sneakers-black-allsaints-us` | `Brody Leather Low Top Sneakers Black \| ALLSAINTS US` | `Brody Leather Low Top Sneakers Black` |

### Not touched (could be intentional brand stylization)

- `COS` (brand field across 3 entries) — the brand's actual stylization
- `ESYA` (brand field on `esya-the-dune-set`)
- `FAVORITE DAUGHTER` (brand field) — brand uses all-caps in their logo. Possibly intentional. Flag if you want it normalized.

---

## Editorial decisions waiting on you

### A. Voice violations — em dashes in 3 live entry `reason` fields

Editorial Standard explicitly says "Avoid em dashes." How to rewrite each is your call; I didn't touch them.

| Slug | Current reason |
|---|---|
| `aveda-pureformance-cream` | `Softer hold. Same trick — finish doesn't read as done.` |
| `ysl-myslf-edp` | `Orange blossom, vetiver. The brighter one — for when L'Homme is too quiet.` |
| `esya-the-dune-set` | `White linen, yellow piping — enough to read as a set, not a uniform.` |

Quickest fix is usually a period or a colon instead of the em dash, but the rewrite is editorial. The Editorial Standard says: "Write with specificity, authority, restraint, emotional precision."

### B. Three draft names are still SEO blobs — needs your replacement

The cosmetic pass couldn't fix these because the right name isn't algorithmically derivable. URL gives a hint per row.

| Slug | Current name | URL hint | Suggested name |
|---|---|---|---|
| `timex-watches-from-timex-digital-analog-and-water-resistant` | `Watches from Timex \| Digital, Analog, & Water Resistant` | `/products/marlin-hand-wound-34mm-leather-strap-watch-tw2t18200` | `Marlin Hand-Wound 34mm` |
| `sundays-sundays-beautiful-furniture-made-for-real-life` | `Sundays - Beautiful furniture, made for real life.` | `/products/movie-night-sofa-cream-linen` | `Movie Night Sofa` |
| `veja-brody-leather-low-top-sneakers-black-allsaints-us` | (already cleaned to) `Brody Leather Low Top Sneakers Black` | URL is AllSaints, not Veja | Decide: is brand "Veja" or "AllSaints"? |

Edit each at `/admin/shop-edit/<slug>` before clicking Promote.

### C. One draft has a wide / wrong price range

| Slug | Current priceRange | Note |
|---|---|---|
| `le-creuset-signature-round-dutch-oven` | `$30–$650` | $30 is wrong — scanner picked up a Le Creuset accessory. Real range is closer to `$280–$580` depending on size. |

### D. All 11 drafts have `subcategory: "uncategorized"`

The placeholder. The drafts page dropdown is autocompleted with the canonical subcategories for each top-level — pick the right one per row, then Promote.

| Slug | Top-level | Likely subcategory |
|---|---|---|
| `profitec-profitec-go-espresso-machine` | home | `kitchen` |
| `veja-brody-leather-low-top-sneakers-black-allsaints-us` | accessories | `footwear` (or move to `mens/footwear`) |
| `timex-watches-from-timex-digital-analog-and-water-resistant` | accessories | `watches` |
| `sundays-sundays-beautiful-furniture-made-for-real-life` | home | `furniture` |
| `snow-peak-ti-single-450-cup` | travel | `kits` or `outdoor` |
| `snow-peak-ti-double-450-mug` | travel | `kits` or `outdoor` |
| `le-bon-shoppe-her-socks-mc-cotton-classic-white` | womens | `basics` |
| `le-bon-shoppe-her-socks-mc-cotton-dark-tan` | womens | `basics` |
| `buck-mason-black-field-spec-cotton-heavy-tee` | mens | `basics` |
| `buck-mason-white-field-spec-cotton-heavy-tee` | mens | `basics` |
| `buck-mason-dress-navy-field-spec-heavy-tee` | womens | (should this be mens too? — has womens category placeholder) |

Note on the last row: `buck-mason-dress-navy-field-spec-heavy-tee` is currently in `womens` but the other two Buck Mason tees are in `mens`. Probably a placeholder slip — likely should be `mens` like the others.

---

## Light recommendations (no action required)

### E. The Brightland Awake reason

You already promoted this one during your earlier session. Worth a re-read against the Editorial Standard's "performative taste" guardrail: the reason explicitly says "the oil is good, but the reason it belongs here is visibility, color, and the ritual of pouring." That's defensible if the editorial intent is to acknowledge the bottle-as-table-object move, but it's also exactly the kind of reasoning the Standard warns against. Reflect when you're back.

### F. Reuse of Chateau-adds CSV pattern is working well

The `csv_price` + `csv_category` columns rescued 27 of 48 rows that would have otherwise needed-human. Worth carrying forward for future Chateau-driven adds.

---

## Build & deploy state

- Typecheck: ✓ clean
- Lint: ✓ clean
- Local commits ahead of origin: at least 2 — the subcategory backfill (`c5754c7`) and these cosmetic fixes
- Vercel: last successful deploy is the bulk-import bundle. Next push will deploy the cosmetic fixes + whatever new drafts/promotions you've made locally.

Push order when you're back:
1. GitHub Desktop → push all pending commits
2. Wait for Vercel deploy
3. Run promote-or-edit pass on the 11 remaining drafts on `/admin/shop-drafts`
4. After all promotions, do one more push for the editorial state
