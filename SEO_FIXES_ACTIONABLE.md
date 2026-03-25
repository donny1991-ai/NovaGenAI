# NovaGenAI SEO Fixes — Quick Action Checklist

**Audit Date:** March 25, 2026  
**Total Issues:** 12 (2 Critical, 3 High, 4 Medium, 3 Low)  
**Time to Fix Critical Issues:** ~2-4 hours

---

## ✅ CRITICAL FIXES (Do This Week)

### 1. Fix Empty Alt Tags on All Images

**Problem:** Decorative/hero images have `alt=""` which fails WCAG 2.1 AA accessibility standards.

**Files to Fix:**
```bash
about.html:193
contact.html (all <img> tags)
solutions.html (hero images)
case-studies.html (background images)
technology.html (hero images)
agents.html (background images)
team.html (background images)
```

**How to Fix:**
- **Decorative images** (no info): Add `role="presentation"` or `aria-hidden="true"` alongside `alt=""`
- **Hero/background images**: Add descriptive alt text

**Example Fix (about.html:193):**
```html
<!-- BEFORE -->
<img src="images/about-hero-new.jpg" alt="" loading="lazy" ...>

<!-- AFTER (Option 1: Decorative) -->
<img src="images/about-hero-new.jpg" alt="" role="presentation" loading="lazy" ...>

<!-- AFTER (Option 2: Descriptive) -->
<img src="images/about-hero-new.jpg" alt="NovaGenAI headquarters in Cyberjaya, Malaysia" loading="lazy" ...>
```

---

### 2. Fix robots.txt

**Current robots.txt:**
```
Sitemap: https://novagenai.com.my/sitemap.xml
```

**Fixed robots.txt:**
```
User-agent: *
Allow: /

Sitemap: https://novagenai.com.my/sitemap.xml
```

**File:** `/root/.openclaw/workspace/novagenai-website/robots.txt`

---

## 🔥 HIGH PRIORITY FIXES (This Week)

### 3. Optimize Title Tags (Too Short)

| File | Line | Current | Fix To |
|------|------|---------|--------|
| about.html | ~9 | "About — NovaGenAI" (18 chars) | "About NovaGenAI — Enterprise AI from Cyberjaya, Malaysia" (59 chars) |
| solutions.html | ~9 | "Solutions — NovaGenAI" (22 chars) | "AI Solutions — Agents, Voice AI & Custom Systems \| NovaGenAI" (60 chars) |
| technology.html | ~9 | "Technology — NovaGenAI" (23 chars) | "AI Technology Stack — NVIDIA DGX, LLM & RAG \| NovaGenAI" (58 chars) |
| agents.html | ~9 | "AI Agents — NovaGenAI" (22 chars) | "AI Agents Platform — Autonomous Enterprise AI \| NovaGenAI" (59 chars) |
| contact.html | ~9 | "Contact — NovaGenAI" (20 chars) | "Contact NovaGenAI — Book Your AI Consultation Today" (58 chars) |
| team.html | ~9 | "Our Team — NovaGenAI" (21 chars) | "Our Team — AI Engineers & Leaders at NovaGenAI Malaysia" (60 chars) |
| case-studies.html | ~9 | "Case Studies — NovaGenAI" (25 chars) | "Case Studies — Real AI Results for Enterprise \| NovaGenAI" (60 chars) |

**Target:** 50-60 characters for optimal SERP display.

---

### 4. Fix Meta Descriptions (Too Short)

| File | Line | Current Length | Fix To |
|------|------|----------------|--------|
| contact.html | ~10 | 82 chars (TOO SHORT) | "Contact NovaGenAI for enterprise AI solutions. Book a demo, request a consultation, or discuss your AI transformation. Response within 1 business day." (158 chars) |

**Also optimize:**
- about.html — Extend from 136 to ~155-160 chars (add CTA)
- technology.html — Trim from 169 to 160 chars (remove filler words)

---

## ⚠️ MEDIUM PRIORITY (Next 2 Weeks)

### 5. Create Custom Open Graph Images

**Current:** Most pages use generic `og-image.png`

**Create unique OG images for:**
- agents.html → "AI Agents Platform" visual
- technology.html → DGX Spark hardware image
- case-studies.html → Client results/logos collage
- team.html → Team photo or org chart

**Files to update (meta property="og:image"):**
```
agents.html:20
technology.html:20
case-studies.html:20
team.html:20
```

---

### 6. H1 Tag Screen Reader Testing

**Action:** Test H1 tags with NVDA or JAWS screen readers to ensure `<span class="accent">` tags don't break semantic flow.

**Example:**
```html
<h1>AI <span class="accent">AGENTS</span><br/>IN YOUR ORGANISATION</h1>
```

**If broken:** Remove `<br/>` from H1 tags or restructure.

---

## 💡 LOW PRIORITY (Nice-to-Have)

### 7. Add Service Schema to Solutions Pages

**Example for agents.html:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "AI Agents Platform",
  "provider": {
    "@id": "https://novagenai.com.my/#organization"
  },
  "description": "Autonomous AI agents for enterprise deployment",
  "serviceType": "Enterprise AI Software",
  "areaServed": ["Malaysia", "Singapore", "Australia"]
}
</script>
```

---

### 8. Add More Internal Links

**Action:** Link related blog posts to each other and link service pages to technology pages when mentioning specific tech (e.g., "NVIDIA DGX Spark" → technology.html).

---

## 📊 WHAT'S ALREADY GOOD (No Action Needed)

✅ **Canonical tags** — All correct, self-referencing  
✅ **HTTPS** — Fully enforced, no mixed content  
✅ **Mobile viewport** — Present on all pages  
✅ **Sitemap.xml** — Valid, 28 URLs, all return 200  
✅ **Schema markup** — Comprehensive (Organization, FAQ, Person, Article)  
✅ **No duplicate content** — All pages unique  
✅ **No broken links** — Internal links verified  
✅ **HTTP status codes** — All pages return 200 OK

---

## Quick Fix Script (Optional)

If you want to batch-fix title tags:

```bash
cd /root/.openclaw/workspace/novagenai-website

# Backup first
cp about.html about.html.bak
cp solutions.html solutions.html.bak
# ... etc

# Then use sed or manual editing to replace title tags
```

**Recommendation:** Manually edit to ensure quality control.

---

## Priority Timeline

| Week | Focus | Tasks |
|------|-------|-------|
| Week 1 | Critical | Fix alt tags, robots.txt, title tags |
| Week 2 | High | Meta descriptions, blog post optimization |
| Week 3-4 | Medium | OG images, H1 testing |
| Ongoing | Low | Service schema, internal linking |

---

**Questions?** Review the full audit at `SEO_AUDIT_REPORT.md`
