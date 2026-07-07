#!/usr/bin/env bash
#
# Hessentials — image downloader for the 2026-06-18 Style + Living batch.
#
# Pulls each product's source image to public/shop/<slug>-1.jpg, matching
# the flat-file convention the rest of the catalog uses. Run from repo root:
#
#   bash scripts/download-shop-images-2026-06-18.sh
#
# Idempotent: pass --force to re-download files that already exist.
# After it finishes, the 19 new entries in src/data/shop.ts will resolve
# their local images. Then commit + push as usual.
#

set -e
cd "$(dirname "$0")/.."

DEST="public/shop"
FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

mkdir -p "$DEST"

# slug|imageSrc  (saved as <slug>-1.jpg)
ITEMS=(
  'gh-bass-larson-weejuns-penny-loafer|https://www.ghbass.com/cdn/shop/files/product_14334668_larson_20wj_mm_red_605-001-064_main_sq_gy.jpg?v=1775152940'
  'thursday-cavalier-chelsea-boot|https://thursdayboots.com/cdn/shop/products/1024x1024-Men-Cavalier-Black-092121-3.4_1200x1200.jpg?v=1633034593'
  'uniqlo-oxford-slim-shirt|https://image.uniqlo.com/UQ/ST3/WesternCommon/imagesgoods/462368/item/goods_01_462368_3x4.jpg'
  'cos-slim-merino-crew|https://media.cos.com/assets/001/9e/87/9e878bb973029466a85ee6dc0f0f1664310f6635_xxl-1.jpg?imwidth=2160'
  'cos-ribbed-knit-cotton-shirt|https://media.cos.com/assets/001/27/33/2733ac786286c1ba1e60e04417a1e9367ffaccda_xxl-1.jpg?imwidth=2160'
  'cos-relaxed-cotton-overshirt|https://media.cos.com/assets/001/3c/2a/3c2a378994cbc7af910d02c644607439a939468d_xxl-1.jpg?imwidth=2160'
  'uniqlo-milano-ribbed-cardigan|https://image.uniqlo.com/UQ/ST3/WesternCommon/imagesgoods/453763/item/goods_09_453763_3x4.jpg'
  'tanner-goods-standard-belt-natural|https://www.tannergoods.com/cdn/shop/products/Standard-Belt-Natural-Front-edit.jpg?v=1662153936'
  'anonymous-ism-american-rib-crew-sock|https://media.endclothing.com/media/catalog/product/1/2/12-02-2018_anonymous_ismamericanribcrewsock_3pack_navy_15182900-49_ja_1.jpg'
  'uniqlo-corduroy-cap|https://image.uniqlo.com/UQ/ST3/WesternCommon/imagesgoods/479827/item/goods_68_479827_3x4.jpg'
  'hay-matin-table-lamp|https://images.hermanmiller.group/m/2bc8d63e825831fc/W-HAY_2516467_100147569_white_a-tif.png'
  'aesop-ptolemy-aromatique-candle|https://www.aesop.com/dw/image/v2/AANG_PRD/on/demandware.static/-/Sites-aesop-us-master-catalog/default/dw68e81ede/images/products/HM02/Aesop_Home_Ptolemy_Aromatique_Candle_Web_Front_2000x2000px.jpg?sw=2000&sh=2000&sm=cut&sfrm=png&q=85'
  'onsen-supima-waffle-bath-towel|https://onsentowel.com/cdn/shop/products/ON_PDP_WaffleBathTowel_CinderGrey_1_main.jpg'
  'cultiver-linen-duvet-cover-set-natural|https://cdn.shopify.com/s/files/1/0894/5382/files/7-Duvet-Cover-Set-Pulled-Back-Natural_eb1771bb-069a-42c4-9346-0a466a990254.jpg'
  'hasami-porcelain-bowl-natural|https://jinenstore.com/cdn/shop/products/resized_square-7_1_grande.jpg?v=1690387491'
  'leuchtturm1917-a5-dotted-notebook|https://www.leuchtturm1917.us/media/productdetail/440x440/329398/notebook-medium-a5-hardcover-251-numbered-pages-dotted-black.jpg'
  'fog-linen-brass-tray-oval|https://cdn.shopify.com/s/files/1/1020/2551/products/FOG.100.60.002.BRS_b.jpg?v=1696016638'
  'hay-revolver-stool|https://images.hermanmiller.group/m/a0e73d3b0923c7b4/W-HAY_2514632_100127998_sky_grey_f.png'
  'mantas-ezcaray-stripe-mohair-throw|https://www.hawkinsnewyork.com/cdn/shop/products/Holiday20205261_RT_c0b2ee39-b82c-4820-a43b-7f530e798aaa_1024x1024.jpg?v=1630532717'
)

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
total=${#ITEMS[@]}
i=0
ok=0
fail=0
declare -a FAILED

for entry in "${ITEMS[@]}"; do
  i=$((i+1))
  slug="${entry%%|*}"
  url="${entry#*|}"
  out="$DEST/${slug}-1.jpg"

  if [[ -f "$out" && "$FORCE" != true ]]; then
    printf "[%2d/%d] skip %s (exists)\n" "$i" "$total" "$slug"
    ok=$((ok+1))
    continue
  fi

  printf "[%2d/%d] %s ... " "$i" "$total" "$slug"
  referer="https://$(printf '%s' "$url" | awk -F/ '{print $3}')/"
  if curl -fsSL --max-time 30 -A "$UA" -e "$referer" -H "Accept: image/avif,image/webp,image/apng,image/*,*/*" -o "$out" "$url"; then
    size=$(wc -c < "$out" | tr -d ' ')
    printf "ok (%s bytes)\n" "$size"
    ok=$((ok+1))
  else
    rm -f "$out"
    printf "FAILED\n"
    fail=$((fail+1))
    FAILED+=("$slug")
  fi
done

echo
echo "----"
echo "Done. $ok of $total saved. $fail failed."
if (( fail > 0 )); then
  echo "Failed slugs:"
  printf '  - %s\n' "${FAILED[@]}"
  echo "Retry with: bash scripts/download-shop-images-2026-06-18.sh --force"
  echo "If a slug keeps failing, tell Claude and that one entry can fall back to its external image URL."
fi
