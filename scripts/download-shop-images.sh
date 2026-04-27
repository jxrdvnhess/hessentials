#!/usr/bin/env bash
#
# Hessentials — one-shot shop image downloader.
#
# Reads from the imageSrc URLs declared in src/data/shop.ts and saves each one
# to public/shop/<slug>.jpg. Run from repo root:
#
#   bash scripts/download-shop-images.sh
#
# Idempotent: pass --force to re-download files that already exist.
#

set -e
cd "$(dirname "$0")/.."

DEST="public/shop"
FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

mkdir -p "$DEST"

# slug|imageSrc
ITEMS=(
  'loewe-goya-thin-briefcase|https://www.loewe.com/dw/image/v2/BBPC_PRD/on/demandware.static/-/Sites-Loewe_master/default/dwca31ef16/images_rd/337.12.P57/337.12.P57-1100/337.12.P57_1100_1F.jpg?sw=850&q=100'
  'omega-aqua-terra-small-seconds|https://www.omegawatches.com/media/catalog/product/o/m/omega-seamaster-aqua-terra-150m-co-axial-master-chronometer-small-seconds-41-mm-22022412103001-bdacfe.png?w=1200'
  'bedsure-waffle-blanket|https://m.media-amazon.com/images/I/91UYXcDdHnL._AC_SL1500_.jpg'
  'prada-court-leather-sneakers|https://www.prada.com/content/dam/pradabkg_products/2/2EE/2EE483/070F0009/2EE483_070_F0009_F_G000_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg'
  'massimo-dutti-linen-double-collar-tee|https://static.massimodutti.net/assets/public/dcac/dcf9/610443679566/3bdbbec2edff/00659198700-o6/00659198700-o6.jpg?ts=1777020874502&w=1600&f=auto'
  'lv-hippo-coffee-table|https://lvfurniturecollection.com/cdn/shop/files/hippo-coffee-table_6f30515d-913e-4667-9ad5-f86d1c03fe6b.png?v=1770254572&width=1946'
  'birkenstock-arizona-eva|https://www.birkenstock.com/dw/image/v2/BLZD_PRD/on/demandware.static/-/Sites-master-catalog-amer/default/dw6172c109/129421/129421.jpg?sw=1148&sh=1148&sm=fit&q=80'
  'ahlem-louxor|https://www.ahlemeyewear.com/cdn/shop/files/Louxor_SUN_WEB_greyGold_01_WEB_grey_1500x1002_crop_center.jpg?v=1714675082'
  'prada-linen-duffel|https://www.prada.com/content/dam/pradabkg_products/2/2VY/2VY011/2CX9F0018/2VY011_2CX9_F0018_V_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg'
  'crazy-water-sampler|https://drinkcrazywater.myshopify.com/cdn/shop/products/sampler_large.png?v=1509477709'
  'tag-heuer-aquaracer-quartz|https://www.tagheuer.com/on/demandware.static/-/Sites-tagheuer-master/default/dwced42cf4/TAG_Heuer_Aquaracer/CBP1112.BA0627/CBP1112.BA0627_Soldier.png?impolicy=TrimRatioResize&width=1254&ratioHeight=5&ratioWidth=4&expansion=true'
  'aveda-pureformance-clay|https://www.aveda.com/media/images/products/355x600/white/av_sku_A3TX01_34069_355x600_0.jpg'
  'massimo-dutti-tapered-jeans|https://static.massimodutti.net/assets/public/21d8/ffc7/26214fef9b7f/09b197e25617/00451110806-o8/00451110806-o8.jpg?ts=1770972782296&w=1600&f=auto'
  'tiffany-venetian-link-bracelet|https://media.tiffany.com/is/image/tco/60150727_BLT_ALT3X1?hei=1230&wid=1230&fmt=jpg'
  'prada-renylon-belt-bag|https://www.prada.com/content/dam/pradanux_products/2/2VL/2VL977/2DMGF0002/2VL977_2DMG_F0002_V_WOO_SLF.png/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg'
  'pacific-coast-down-pillow|https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcR0x7j0UnChScpFZasLpeJ_lNMm26PoSOladxNb7CMzTfPRvGlhXqLcX8ElmiJPGT33RMY_n8av0qcahg6r1Bpic8E3jS-ilcFXGXUmwSzcR7XW8R5JSOpU_w'
  'massimo-dutti-cotton-slim-pants|https://static.massimodutti.net/assets/public/0b67/83b3/c1f84fd3b74f/e1f1c5ab126a/00101001401-o6/00101001401-o6.jpg?ts=1773142882443&w=1600&f=auto'
  'birkenstock-arizona-leather|https://www.birkenstock.com/dw/image/v2/BLZD_PRD/on/demandware.static/-/Sites-master-catalog-amer/default/dw4dfcde85/452761/452761.jpg?sw=1148&sh=1148&sm=fit&q=80'
  'johnston-murphy-rhodes-backpack|https://www.johnstonmurphy.com/dw/image/v2/AANO_PRD/on/demandware.static/-/Sites-genesco-master/default/dw64925262/large/4611736_master.jpg?sw=1200&sh=1130&strip=false'
  'aveda-pureformance-cream|https://www.aveda.com/media/images/products/355x600/white/av_sku_A3TW01_34068_355x600_0.jpg'
  'ahlem-haussmann|https://www.ahlemeyewear.com/cdn/shop/files/Haussmann_SUN_Champagne_01_WEB_grey_2d6e74b6-308e-46f5-9ece-376eab17439b_1500x1002_crop_center.jpg?v=1736543132'
  'away-the-large|https://www.awaytravel.com/cdn/shop/files/872a3683-1382-44ea-b173-efa206cdd7d8_6a783a90-fdc2-4fab-ac47-a720cdc93b8e.jpg?v=1773689166&width=1200'
  'massimo-dutti-cotton-tee|https://static.massimodutti.net/assets/public/deb2/11c0/a0d24d6e8786/3f0d9377fc33/01418212712-o7/01418212712-o7.jpg?ts=1770630992252&w=1600&f=auto'
  'goodfellow-flat-front-shorts|https://target.scene7.com/is/image/Target/GUEST_4f30aa05-e862-4b91-82fb-b14c368bda9d?wid=1200&hei=1200&qlt=80'
  'prada-renylon-backpack|https://www.prada.com/content/dam/pradabkg_products/2/2VZ/2VZ048/2DMGF0002/2VZ048_2DMG_F0002_V_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg'
  'uniqlo-oxford-oversized-shirt|https://image.uniqlo.com/UQ/ST3/WesternCommon/imagesgoods/484905/sub/goods_484905_sub14_3x4.jpg'
  'abercrombie-premium-ribbed-tank|https://img.abercrombie.com/is/image/anf/KIC_124-5764-00037-900_model1?policy=product-extra-large'
  'prada-renylon-duffle|https://www.prada.com/content/dam/pradabkg_products/2/2VC/2VC013/2DMHF0002/2VC013_2DMH_F0002_V_XOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg'
  'away-bigger-carry-on|https://www.awaytravel.com/cdn/shop/files/215cd47b-8e23-4546-9a91-b5035b4d078c_9d00a95f-e0b6-4b8f-8ee6-ce6393f1b82e.jpg?v=1773689166&width=1200'
  'clayton-crume-canvas-tote|https://claytonandcrume.com/cdn/shop/files/CanvasMarketTote_1_1_e83c0901-e7be-49f1-972a-34e98cc9d5f9.jpg?v=1761077812&width=1200'
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
  out="$DEST/${slug}.jpg"

  if [[ -f "$out" && "$FORCE" != true ]]; then
    printf "[%2d/%d] skip %s (exists)\n" "$i" "$total" "$slug"
    ok=$((ok+1))
    continue
  fi

  printf "[%2d/%d] %s ... " "$i" "$total" "$slug"
  if curl -fsSL --max-time 30 -A "$UA" -o "$out" "$url"; then
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
  echo "Try again with: bash scripts/download-shop-images.sh --force"
fi
