# Shop product images

Drop product images here as `.jpg` files using the slugs below. Each card on
`/shop` automatically picks up its image as soon as the file lands — no code
change needed.

## Image specs

- Aspect ratio: **4:5** (cards are pre-shaped for this — anything else will be
  cropped via `object-cover`)
- Tightly cropped on the product
- Warm-neutral tone preferred; avoid harsh white cutouts
- Minimal background distraction
- No model-heavy compositions when avoidable
- No text overlays

## Filenames

Each filename matches the product `slug` from `src/data/shop.ts` plus `.jpg`.

### 01 — Getting Dressed

- `prada-americas-cup-sneaker.jpg`
- `massimo-dutti-tailored-trouser.jpg`
- `club-monaco-ribbed-tank.jpg`
- `quince-linen-pant.jpg`
- `goodfellow-chino-shorts.jpg`
- `birkenstock-arizona-sandal.jpg`

### 02 — In Transit

- `prada-leather-duffle.jpg`
- `prada-belt-bag.jpg`
- `johnston-murphy-xc4-backpack.jpg`
- `away-carry-on.jpg`

### 03 — Daily Use

- `prada-paradigme-eau-de-parfum.jpg`
- `aveda-pure-formance-grooming-system.jpg`

### 04 — Finishing Touches

- `ahlem-place-de-la-concorde.jpg`
- `mejuri-box-chain-necklace.jpg`

### 05 — Carry & Keep

- `jcrew-medium-canvas-tote.jpg`
- `baggu-standard-tote.jpg`

## Until images land

Each card renders a quiet plaster placeholder with the brand name in muted
serif italic. The page reads clean without images — they replace the
placeholders one by one as you add them.

## Other formats

If you want to use `.png` or `.webp`, update the `image` field for the
matching product in `src/data/shop.ts` (e.g. `/shop/prada-belt-bag.webp`).
