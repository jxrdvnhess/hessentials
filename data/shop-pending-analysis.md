# Shop pending — analysis for Chateau

44 entries currently in pending. Grouped by failure pattern so future sourcing can avoid the systemic ones.

---

## 1. Anti-bot retailers — avoid these for direct linking

These retailers serve a 403 / CAPTCHA / HTTP2 protocol error to anything that isn't a real-human browser session. Real Chromium (Playwright) gets through some, but not all. Pricing layer can't refresh on these either, so even if we land an entry, prices will go stale. Treat as "don't link direct" and either find an alternate retailer or note this is a no-image-no-price entry.

| Retailer | Behavior | Examples |
|---|---|---|
| **Aritzia** | 403 to all bots | Effortless Pant Crepette |
| **Tod's** | HTTP/2 protocol error before page loads | Gommino Driving Shoes (scraped Tod's home page title) |
| **Lululemon** | HTTP/2 protocol error | ABC Slim-Fit Trouser |
| **West Elm** | 403 → home page title leaks through | Mid-century Floor Mirror, Anton Coffee Table |
| **Zara Home** | Page loads but body is `&nbsp;` (heavy JS gate) | Washed Linen Napkin |
| **Williams Sonoma** | Timeout / 403 | Maldon Sea Salt |
| **AllSaints** | 403 (Veja "Brody Leather Low Top Sneakers" — also see #2 below) | Veja sneakers via AllSaints |

**Action for Chateau:** when possible, source from the brand's own site (Veja sells direct) or a small reseller that doesn't gate scrapers. If you need AllSaints / Tod's / Lululemon, treat them as accept-no-pricing items and we'll enter price manually.

---

## 2. Scraper landed on a non-product page (404 / category / home)

These URLs technically returned 200 OK, but the scraper got back a landing page, search result, or "Products" index — not the product detail. The brand+name in pending is from the page's `<title>` tag, not the product itself. Easy giveaway: the name is the company's marketing copy.

| Brand | Pending name | Real URL fix needed |
|---|---|---|
| **IKEA** | "Products" (Hovet mirror URL) | URL should be the EXACT product page, not the category. Hovet may be discontinued. |
| **Leviton** | "Products" | Same. URL `/products/d26hd-2rw` lands on category. |
| **Rejuvenation** | "Heirloom-Quality Lighting, Hardware & More" | Ladd Wall Hook URL hit a 403 → landing page leaked. |
| **Tod's** | "Tod's Official Store: Italian luxury shoes & footwear" | HTTP2 error → home page. See #1. |
| **West Elm** (×2) | "West Elm: Modern Furniture, Home Decor, Lighting & More" | 403 → home page. See #1. |
| **Zara Home** | "&nbsp;" | JS gate. See #1. |

**Action for Chateau:** verify each URL renders the actual product when opened in incognito (without your cookies). If the URL goes to a category, search results, or home page, the link is dead even though it returns 200. Look for a URL with the specific SKU / slug in the path.

---

## 3. Wrong URL — name and URL don't match

The audit has a mismatch between the URL and the intended product. Worth flagging because this isn't a scraper issue — it's an audit-side data quality issue.

| Pending entry | Issue |
|---|---|
| **Madewell — "KULE The Twiggy Cardigan Sweater"** | URL is `/jewelry/earrings/chunky-small-hoop-earrings/NN563/` — earrings, not a cardigan. |
| **L.L.Bean Boat and Tote** | Same product staged twice: once at `/llb/shop/37037` and once at `/llb/shop/37037?page=boat-and-tote-bag-zip-top`. Keep one. |

**Action for Chateau:** the Madewell row needs a real URL for the actual product. The L.L.Bean dup can just lose the query-string version.

---

## 4. Editorial holds — Chateau-flagged before scraping

These pre-existed Chateau's review. Decisions waiting:

| Brand | Reason |
|---|---|
| **Sephora Vetiver** | Sephora is too broad — name a specific house (Guerlain, Le Labo, etc.) or remove the anchor. |
| **Alo Yoga (Triumph Bomber)** | May be too activewear-coded for the permanent archive. Only fits if the article wants softness and ease over tailoring. |

---

## 5. Sent back from drafts — needs another pass

These were staged at one point, sent back. Either the data was thin, the brand/name was wrong, or the editorial filter didn't fit.

- **Veja Brody Sneakers (AllSaints URL)** — brand says Veja, URL is AllSaints. Decide whose site to link to.
- **Snow Peak Ti-Single 450 Cup** — sent back, needs new look.
- **Snow Peak Ti-Double 450 Mug** — same.
- **Profitec GO (wholelattelove.com)** — sent back; maybe re-source from a different retailer.

---

## 6. Loaded fine, but no structured data on the page

These are the boring case. Page is real, product is real, but the retailer doesn't ship `Product` JSON-LD or `og:image` reliably, so scrape returns empty prices / 1–2 images instead of a full gallery. These are easiest to fix manually — open the entry, paste the price, paste a couple more product image URLs.

By retailer:

| Retailer | Entries | Pattern |
|---|---|---|
| **Schoolhouse** | 3 (Alabax, Grant Mirror, Miller Cart) | Only 1 image returned. JSON-LD has the product but skips the gallery. |
| **Coyuchi** | 2 (Cozy Cotton Blanket, Paperless Towels) | 2 images returned, gallery has more. |
| **IKEA** | 2 (FÄRGKLAR set + plate) | IKEA's structured data is famously sparse — pricing is in client-rendered JS. |
| **Il Bisonte** | 2 (crossbody bags) | Only 2 images. |
| **Jacobsen Salt** | 2 (flake salt + tin) | Only 2 images. |
| **MUJI** | 2 (recycled paper notebooks) | Only 2 images. |
| **Burlap & Barrel** | 1 (Royal Cinnamon) | Only 2 images. |
| **Delsey** | 1 (Chatelet Air 2.0) | Only 1 image. |
| **Bickmore** | 1 (Bick 4 Leather Conditioner) | Empty prices. |
| **Sonos** | 1 (Era 100) | Empty prices. |
| **Lutron Caseta** | 1 (Diva Dimmer) | Empty prices. |
| **Le Labo** | 1 (Santal 33) | Empty prices. |
| **Mejuri** | 1 (Bold Huggie Hoops) | Empty prices. |
| **Saphir** | 1 (Renovateur) | Empty prices. |
| **Rancilio** | 1 (Silvia Pro) | Empty prices + SEO blob name. |
| **Fable** | 1 (Premium Dinnerware) | Empty prices. |
| **L.L.Bean** | 1 (Boat and Tote — non-query-string version) | Empty prices. |

**Action:** these are individually fixable on `/admin/shop-edit/<slug>` — paste a price, use the new Re-scrape button or paste image URLs directly. The Re-scrape now also exposes scraped images individually with "Add to product" buttons. No URL changes needed.

---

## 7. Non-English structured data

| Brand | Pending name | Issue |
|---|---|---|
| **Fog Linen Work** | "ブラス トレー 楕円形 S" / "ブラス トレー 楈円形 M" | Japanese site. JSON-LD is in Japanese; the English alt may not exist or only renders on Fog Linen's distributor sites. |

**Action for Chateau:** Fog Linen ships through Heath, Rikumo, Of A Kind in the US — those may have English-language structured data for the same product.

---

## Pattern summary for future sourcing

When you're picking the URL for a Shop item:

1. **Avoid known anti-bot retailers as the source** unless you accept that pricing won't auto-refresh: Aritzia, Tod's, Lululemon, West Elm, Zara Home, Williams Sonoma, AllSaints.
2. **Verify the URL is a product page, not a category/landing** — open it in incognito and confirm the product name renders in the title bar.
3. **Prefer brand-direct over reseller** unless the brand site itself is bot-walled (Veja sells direct; better than AllSaints).
4. **Don't paste home-page URLs** for any reason — even if the product is visible on that page, the structured data won't be.
5. **For non-English brands** (Fog Linen, etc.), find a US distributor that ships JSON-LD in English.

The current 44 pending breaks down as: **7 anti-bot retailers**, **6 wrong-page hits**, **2 wrong-URL audit mistakes** (Madewell + L.L.Bean dup), **2 editorial holds**, **4 sent-back drafts**, **22 thin-but-fixable**, **1 non-English** (Fog Linen).
