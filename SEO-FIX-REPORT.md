# SEO Fix Report — novagenai.com.my
**Date:** 2026-03-09  
**Commit:** 463d241

## Audit Summary

### ✅ Already Good
- **All 27 public pages** have self-referencing canonical tags with correct `https://novagenai.com.my/` domain
- **All pages** have unique `<title>` tags and `<meta name="description">`
- **Structured data** (JSON-LD) present on all main pages + blog posts (Organization, WebSite, Article schemas)
- **robots.txt** references sitemap correctly
- **CNAME** file present for GitHub Pages custom domain
- **No noindex tags** on any public page
- **Internal linking** structure is solid — nav links all main pages

### 🔴 Issues Found & Fixed

#### 1. Unblocked Non-Public Pages (→ GSC "Crawled - currently not indexed", "Discovered - currently not indexed")
**Problem:** `email-template-lead.html`, `email-preview.html`, `blog/_template.html`, `blog/_video-card.html` were crawlable. These are internal templates that should never be indexed. Google was discovering them and wasting crawl budget.
**Fix:** 
- Added `<meta name="robots" content="noindex, nofollow">` to email-template-lead.html, email-preview.html, blog/_template.html
- Added `Disallow` rules in robots.txt for all 4 files

#### 2. Duplicate Content (→ GSC "Duplicate without user-selected canonical", "Alternate page with proper canonical tag")
**Problem:** `blog/when-biology-becomes-code.html` is a shorter version of `blog/cell2sentence-computational-biotech.html` — same topic, overlapping content. Both had self-referencing canonicals, confusing Google.
**Fix:**
- Changed canonical on `when-biology-becomes-code.html` to point to `cell2sentence-computational-biotech.html`
- Removed `when-biology-becomes-code.html` from sitemap.xml

#### 3. Missing 404 Page
**Problem:** No custom 404 page existed. GitHub Pages would serve a generic one.
**Fix:** Created `404.html` with noindex, branded design, and link back to homepage.

#### 4. Stale Sitemap Dates
**Problem:** All `<lastmod>` dates were 2026-03-06, not reflecting actual update times.
**Fix:** Updated all lastmod dates to 2026-03-09.

#### 5. Missing IndexNow Key File
**Problem:** Bing IndexNow key file wasn't deployed to the website root.
**Fix:** Created `93904c29a0ae4128a677c8e72d025d64.txt` at site root.

## Crawl Notifications Sent
- ✅ **Bing IndexNow** — submitted all 27 URLs via batch API (HTTP 200)
- ℹ️ **Google Ping** — deprecated (Google relies on sitemap discovery via robots.txt + Search Console)

## GSC Issue Mapping

| GSC Issue | Likely Cause | Fix Applied |
|-----------|-------------|-------------|
| Page with redirect (1) | HTTP→HTTPS or www→non-www redirect (infrastructure level, handled by Caddy/GitHub Pages) | N/A — this is expected behavior, not an error |
| Alternate page with proper canonical tag (1) | `when-biology-becomes-code.html` now correctly canonicals to `cell2sentence-computational-biotech.html` | ✅ |
| Crawled - currently not indexed (2) | Email templates being crawled | ✅ Blocked with noindex + robots.txt |
| Duplicate without user-selected canonical (1) | Two biology blog posts with overlapping content | ✅ Set canonical |
| Discovered - currently not indexed (12) | Fresh pages + crawl budget wasted on templates | ✅ Blocked templates, updated sitemap, pinged IndexNow |

## Next Steps
1. **Wait 3-7 days** for Google to re-crawl with updated sitemap
2. **Request indexing** manually in GSC for any remaining unindexed pages via URL Inspection tool
3. **Monitor GSC** Coverage report for improvements
4. Consider adding more internal links from high-authority pages to blog posts to boost crawl priority
