# SEO Fix Report #2 — 9 March 2026

## Task 1: Product Snippet Fix (CRITICAL)

**Issue:** Google Search Console reported "Either 'offers', 'review', or 'aggregateRating' should be specified" on pages with Product schema.

**Root Cause:** No actual `Product` schema existed. The issue was `Offer` objects nested inside `ProfessionalService.hasOfferCatalog` on `index.html`. Google was interpreting the `Offer` type as requiring Product-level validation (offers/review/aggregateRating).

**Fix Applied:**
- Removed all `hasOfferCatalog` containing `Offer` wrappers from 3 `ProfessionalService` JSON-LD blocks in `index.html`
- Replaced with `knowsAbout` pointing directly to Service objects (no Offer wrapper)
- Removed `priceRange`, `currenciesAccepted`, `paymentAccepted` fields (not appropriate for B2B services)
- All existing standalone `Service` schema objects remain intact

**Files Changed:** `index.html`

---

## Task 2: Video Watch Pages

**Issue:** Google Search Console reported "Video isn't on a watch page" for 3 videos.

**Root Cause:** Videos were embedded inline within blog posts but had no dedicated watch pages where the video is the primary content.

**Videos Found (3 unique):**
1. `computational-biotech-dna.mp4` — used in `when-biology-becomes-code.html` and `novagenai-vision-2026.html`
2. `enterprise-security-vault.mp4` — used in `novagenai-vision-2026.html`
3. `ai-intelligence-eye.mp4` — used in `novagenai-vision-2026.html`

**Watch Pages Created:**
| Page | URL |
|------|-----|
| Computational Biotech | `https://novagenai.com.my/videos/computational-biotech-dna.html` |
| Enterprise Security | `https://novagenai.com.my/videos/enterprise-security-vault.html` |
| AI Intelligence | `https://novagenai.com.my/videos/ai-intelligence-eye.html` |

**Each watch page includes:**
- ✅ Video as hero element (large, top of page, autoplay)
- ✅ `VideoObject` JSON-LD schema (name, description, thumbnailUrl, uploadDate, contentUrl, publisher)
- ✅ Title tag: `[Video Title] | NovaGenAI`
- ✅ Meta description
- ✅ Self-referencing canonical tag
- ✅ Description/transcript text below video
- ✅ Link back to original blog post(s)
- ✅ Matches site design (Outfit/Inter fonts, dark theme, site CSS)

**Blog Post Updates:**
- Added "Watch the full video →" links after each video embed in:
  - `blog/when-biology-becomes-code.html` (1 video)
  - `blog/novagenai-vision-2026.html` (3 videos)

**Sitemap:** Updated `sitemap.xml` with all 3 new video pages.

---

## Deployment

- ✅ Git committed and pushed to `master`
- ✅ Bing IndexNow pinged (HTTP 200) for 7 URLs:
  - `index.html`, 2 blog posts, 3 video pages, `sitemap.xml`

## Expected Timeline
- Google should re-crawl within 1-3 days
- Product snippet warnings should clear within 1-2 weeks
- Video watch page issues should resolve after next crawl cycle
