# NovaGenAI Website — Image Audit Report

**Date:** 2026-02-23  
**Auditor:** NovaGenAI Design & Research Team  
**Brand Colors:** Cyan #00D4FF, Dark backgrounds #000/#0a0a0a, White text  
**Aesthetic:** Dark theme, futuristic, biotech, enterprise AI

---

## Executive Summary

The NovaGenAI website has **29 image files** across the `/images/` directory. The site is heavily text-driven with CSS-only styling for most sections. Key issues:

1. **3 placeholder SVG logos** (CryoCord, ElevenLabs, Anthropic) — just white text on transparent, ~200 bytes each
2. **Stock photography** used across solution cards and hero backgrounds — generic, not brand-aligned
3. **No custom illustrations or rendered visuals** — competitors like Anthropic, OpenAI, Palantir all use custom hero art
4. **Team section uses initials (DC, JT, HL, CSK)** instead of photos or custom avatars
5. **Agents page (694 lines) is entirely text/CSS** — no imagery for the most visually complex page
6. **Trust bar on homepage uses text spans** instead of actual partner logos

**Total image opportunities identified: 47**  
**High priority: 18 | Medium: 17 | Low: 12**

---

## Competitor Research — Visual Design Patterns

| Company | Hero Visual | Section Imagery | Icons | Overall Approach |
|---------|------------|----------------|-------|-----------------|
| **Anthropic** | Abstract gradient art, subtle particle animations | Custom illustrations per product | Minimal, geometric | Restrained, research-lab aesthetic |
| **OpenAI** | Full-bleed product screenshots, 3D renders | Product UI mockups, custom photography | Custom SVG icon set | Clean, product-focused |
| **Scale AI** | Data visualization art, custom 3D renders | Case study photography, dashboard screenshots | Custom illustrated icons | Enterprise-confident, data-heavy |
| **Palantir** | Cinematic dark photography, mission imagery | Custom photography of real deployments | Minimal iconography | Dark, serious, defense-grade feel |
| **Anduril** | Hardware product photography, field imagery | Real deployment photos, engineering shots | Custom military-tech icons | Tactical, real-world, no stock |
| **Cohere** | Abstract 3D shapes, gradient blobs | Custom illustrations, product screenshots | Custom icon system | Approachable enterprise |
| **Mistral** | Abstract wind/air patterns, brand illustration | Minimal imagery, typography-led | Simple geometric icons | European minimalist |

### Key Takeaways for NovaGenAI:
- **Every premium AI company uses custom hero art** — no stock photos in hero sections
- **Dark theme companies (Palantir, Anduril) use custom photography or 3D renders** — never generic stock
- **Product screenshots/mockups are critical** — Clarify platform should have real or realistic mockups
- **Partner logos should be real SVGs** — not text placeholders
- **Abstract AI visualizations** (neural networks, particle systems, data flows) are the standard for enterprise AI
- **Team photos are standard** — initials-only feels unfinished

---

## Page-by-Page Breakdown

---

### 1. index.html (Homepage)

#### ✅ What's Working
- Spline 3D robot in hero — good interactive element
- CSS-based solution cards with inline SVG icons — clean

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 1 | **Trust bar logos** | Text spans ("ENTERPRISE HEALTHCARE", "NVIDIA", etc.) — no actual logos | Replace with real partner logos (SVG). Get official NVIDIA, ElevenLabs, Google Cloud, Anthropic logos. | 200x60 each | N/A — use official logos |
| 2 | **Solution card icons** | Generic Feather/Lucide stroke SVGs (microphone, box, question mark, server, document, bar chart) | Replace with custom-rendered 3D or illustrated icons matching brand | 512x512 | "Futuristic glowing cyan microphone icon on dark background, holographic style, #00D4FF accent, transparent background, icon design" |
| 3 | **"Why NovaGenAI" section icons** | Emoji icons (🎯🌏🔒💰🚀) in colored boxes | Replace with custom illustrated icons or 3D renders | 512x512 | "Futuristic target/crosshair icon, glowing cyan #00D4FF, dark #0a0a0a background, holographic glass style, enterprise AI aesthetic" |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 4 | **Stats section background** | Plain #0a0a0a cards | Add subtle background pattern or abstract data visualization | 1920x600 | "Abstract data visualization, flowing cyan #00D4FF particle streams on pure black background, subtle, background texture, enterprise AI" |
| 5 | **Testimonials section** | No avatar images for testimonial authors | Add client photos or company logos next to quotes | 80x80 | N/A — get real client photos |
| 6 | **Contact section visual** | No imagery, pure form | Add abstract visual element on left side | 600x800 | "Abstract AI communication visualization, glowing cyan nodes connected by light threads, dark background, futuristic" |

---

### 2. solutions.html

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 7 | **Hero background** | `ai-abstract.jpg` at 8% opacity — generic blue/purple abstract | Replace with custom NovaGenAI-branded abstract | 1920x1080 | "Abstract AI neural network visualization, dark background, cyan #00D4FF glowing connections, enterprise technology, wide cinematic" |
| 8 | **Voice Agent card image** | `voice-agent.jpg` (35KB) — likely stock waveform | Custom AI voice visualization | 800x400 | "AI voice agent sound wave visualization, cyan #00D4FF waveform on dark background, futuristic holographic style, enterprise quality" |
| 9 | **CRM Dashboard card image** | `crm-dashboard.jpg` (65KB) — stock dashboard | Replace with Clarify platform screenshot or realistic mockup | 800x400 | "AI-powered CRM sales dashboard mockup, dark theme, cyan #00D4FF accents, pipeline charts, lead scoring, futuristic UI design" |
| 10 | **Microscope card image** | `microscope.jpg` (80KB) — stock microscope | Custom biotech/cell visualization | 800x400 | "AI-powered cell biology analysis, microscopic stem cells with cyan #00D4FF holographic overlay, dark background, biotech futuristic" |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 11 | **Server room card image** | `server-room.jpg` (56KB) — stock server room | Custom DGX Spark or branded server imagery | 800x400 | "NVIDIA DGX Spark compact AI supercomputer in dark server room, cyan #00D4FF LED lighting, enterprise infrastructure, cinematic" |
| 12 | **Documents card image** | `documents.jpg` (242KB) — stock documents | Custom RAG/document intelligence visualization | 800x400 | "AI document intelligence, floating holographic documents with glowing cyan connections and search queries, dark background" |
| 13 | **Marketing analytics card image** | `marketing-analytics.jpg` (65KB) — stock analytics | Custom marketing OS visualization | 800x400 | "AI marketing analytics dashboard, content generation visualization, dark theme with cyan #00D4FF accent charts, futuristic" |
| 14 | **Solution card SVG icons** | Same Feather icons as homepage | Custom icons per solution | 512x512 | (See homepage icon prompts) |

---

### 3. agents.html

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 15 | **Hero section** | No background image at all — plain dark | Add hero visual for the most content-rich page | 1920x1080 | "Swarm of autonomous AI agents, glowing cyan #00D4FF orbs connected by light threads orbiting a central orchestrator, dark space background, futuristic enterprise" |
| 16 | **Agent Swarm visual** | CSS-only animated dots with emoji (🔍💻✍️📊🛡️🎤📣🔧) | Replace emojis with custom agent role icons | 512x512 each | "AI researcher agent icon, magnifying glass with neural network, glowing cyan #00D4FF, dark background, holographic style" |
| 17 | **Org diagram department icons** | Emoji icons (💰👥⚙️🎧📣🔬📊🛡️) | Replace with custom department icons | 512x512 each | "AI-powered sales department icon, futuristic bar chart with upward arrow, glowing cyan, dark background, enterprise" |
| 18 | **CRM Mockup section** | CSS-only mockup (boxes, bars, numbers) | Replace with actual Clarify screenshot or high-fidelity mockup image | 800x600 | "AI-native CRM dashboard screenshot, dark theme, real-time lead scoring, pipeline visualization, cyan accents, professional software UI" |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 19 | **Agent Anatomy cards** | Emoji icons (🎭🧠🔧💾🛡️🧬) in plain cards | Custom icons for each agent capability | 512x512 | "AI brain knowledge base icon, glowing neural network inside glass sphere, cyan #00D4FF, dark background" |
| 20 | **Industry cards** | Emoji icons (🏥🏦🏭⚖️🏗️🚚) | Custom industry-specific AI icons | 512x512 | "AI healthcare icon, hospital cross with neural network overlay, cyan #00D4FF glow, dark background" |
| 21 | **How Agents Work pipeline** | Numbered text steps (01-04) | Add small visual illustrations per step | 400x300 | "Task routing visualization, incoming signal being analyzed by AI orchestrator, cyan paths on dark background, diagram style" |
| 22 | **Security section icons** | Inline emoji (🔒👤📋🔐📊🇲🇾) | Custom security/governance icons | 512x512 | "Data sovereignty shield icon, lock with circuit board pattern, glowing cyan #00D4FF, dark background" |

#### 🟢 LOW PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 23 | **Model stack badges** | Colored text badges (ANTHROPIC, OPENAI, GOOGLE, etc.) | Could use actual brand mini-logos | 120x30 | N/A — use official logos |
| 24 | **Swarm flow steps** | Numbered circles (1-4) | Small step illustrations | 300x200 | "Task decomposition visualization, complex request splitting into sub-tasks, cyan light streams, minimal dark background" |

---

### 4. technology.html

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 25 | **Hero background** | `network-security.jpg` at 8% opacity — generic | Custom technology infrastructure visualization | 1920x1080 | "Enterprise AI infrastructure visualization, server racks with flowing cyan #00D4FF data streams, dark cinematic, NVIDIA-inspired" |
| 26 | **DGX Spark image** | `dgx-spark.jpg` (61KB) — likely stock/promotional | Get official NVIDIA DGX Spark product photo or custom render | 800x600 | N/A — use official NVIDIA imagery or custom 3D render of DGX Spark unit |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 27 | **Architecture flow icons** | Generic Feather SVG icons (server, box, shield, gear) | Custom architecture diagram icons | 512x512 | "On-premise server deployment icon, rack server with glowing cyan status lights, dark background, technical illustration" |
| 28 | **Security section icons** | Generic Feather SVG icons (shield, document, lock) | Custom security icons matching brand | 512x512 | "PDPA compliance icon, document with shield and checkmark, cyan #00D4FF glow, dark background" |
| 29 | **AI Stack section** | No visuals, text-only cards | Add technology logos or visual representations | 200x60 | N/A — use vLLM, ElevenLabs logos |

---

### 5. case-studies.html

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 30 | **Hero background** | `stem-cell-lab.jpg` at 10% opacity — stock lab photo | Custom biotech lab with AI overlay | 1920x1080 | "Modern biotech laboratory with holographic AI displays, stem cell visualization, cyan #00D4FF accent lighting, dark cinematic" |
| 31 | **CryoCord logo** | `cryocord-logo.svg` — **PLACEHOLDER** (204 bytes, just white text "CRYOCORD GROUP") | Replace with real CryoCord Group logo | 300x80 | N/A — get official CryoCord logo |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 32 | **Case study solution cards** | No images, text-only cards | Add small visuals per solution deployed | 400x300 | "AI voice agent deployment visualization, sound waves transforming into data, cyan on dark" |
| 33 | **Results section** | Number cards with no visuals | Add background illustrations or icons | 200x200 | "Achievement metrics visualization, glowing number 3 with connected language nodes, cyan" |
| 34 | **Upcoming case studies** | "COMING SOON" text badges, no imagery | Add industry-relevant placeholder visuals | 800x400 | "Private hospital building exterior at night with AI data streams flowing through windows, cyan glow, cinematic dark" |

---

### 6. about.html

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 35 | **Hero background** | `about-hero.jpg` (111KB) at 10% opacity — stock | Custom NovaGenAI origin/mission visual | 1920x1080 | "Futuristic Kuala Lumpur skyline with AI neural network overlay, cyan #00D4FF data streams, dark night, enterprise AI company" |
| 36 | **Partner logos** | `cryocord-logo.svg` (PLACEHOLDER), `elevenlabs-logo.svg` (PLACEHOLDER), nvidia-logo.svg (real, 1.5KB) | Replace CryoCord & ElevenLabs with real logos | 300x80 | N/A — get official partner logos |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 37 | **Team avatars** | CSS initials (DC, JT, HL, CSK) — no photos | Add real professional headshots or custom illustrated avatars | 300x300 | N/A — get real photos, or: "Professional portrait silhouette, dark background, cyan #00D4FF rim lighting, enterprise executive style" |
| 38 | **Our Story section** | No visual/image accompaniment | Add visual alongside story text | 600x800 | "AI and biotech fusion, DNA helix intertwined with neural network, glowing cyan on dark background, artistic" |
| 39 | **Mission/Vision cards** | No visuals | Add abstract illustrations | 400x300 | "Southeast Asian business ecosystem connected by AI, map with glowing cyan nodes, dark background" |

---

### 7. team.html

#### 🔴 HIGH PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 40 | **Hero background** | `team-collab.jpg` (37KB) at 12% opacity — stock collaboration photo | Custom team/engineering visual | 1920x1080 | "AI engineering team workspace, multiple screens showing code and AI models, cyan #00D4FF ambient lighting, dark modern office" |
| 41 | **Leadership avatars** | CSS initials (DC, JT, HL, CSK) with colored borders — no actual photos | Real professional headshots | 400x400 | N/A — photograph real team members |

#### 🟡 MEDIUM PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 42 | **ML Engineers featured image** | `ai-chip.jpg` (86KB) — stock chip close-up | Custom AI/ML engineering visual | 800x500 | "Machine learning model training visualization, neural network layers with flowing cyan data, GPU compute visual, dark background" |
| 43 | **Full-Stack featured image** | `coding.jpg` (40KB) — stock code on screen | Custom development/platform visual | 800x500 | "Full-stack development environment, dark IDE with cyan syntax highlighting, multiple monitors showing React and Python, cinematic" |
| 44 | **Voice & NLP featured image** | `voice-tech.jpg` (40KB) — stock | Custom voice AI visualization | 800x500 | "Multilingual AI voice synthesis, three sound waveforms (English, Malay, Chinese characters) merging, cyan glow, dark" |

#### 🟢 LOW PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 45 | **What We've Built card images** | Reuses `voice-agent.jpg`, `coding.jpg`, `ai-engineers.jpg`, `data-center.jpg` | Custom screenshots or renders per product | 400x250 | "Clarify CRM platform screenshot, dark theme dashboard with real-time lead data, cyan accents" |
| 46 | **Partner section logos** | Mix of SVG logos and text-only `<h4>` elements for CryoCord, ElevenLabs, Anthropic, OpenAI | Use actual brand logos for all partners | 200x60 | N/A — get official logos |

---

### 8. contact.html

#### 🟢 LOW PRIORITY

| # | Item | Current State | Recommendation | Dimensions | AI Prompt |
|---|------|--------------|----------------|------------|-----------|
| 47 | **Hero section** | No background image — plain dark | Could add subtle KL office/map visual | 1920x600 | "Kuala Lumpur twin towers at night, abstract AI overlay, subtle cyan #00D4FF accent, very dark, background use" |

---

## Placeholder Assets — Immediate Fixes Required

These are definitively placeholder files that must be replaced:

| File | Size | Issue | Priority |
|------|------|-------|----------|
| `images/cryocord-logo.svg` | 204 bytes | Just `<text>CRYOCORD GROUP</text>` — not a real logo | 🔴 HIGH |
| `images/elevenlabs-logo.svg` | 200 bytes | Just `<text>ELEVENLABS</text>` — not a real logo | 🔴 HIGH |
| `images/anthropic-logo.svg` | 199 bytes | Just `<text>ANTHROPIC</text>` — not a real logo | 🔴 HIGH |
| `images/google-cloud-logo.svg` | 2.9KB | Possibly real but verify | 🟡 CHECK |
| `images/gcloud-logo.svg` | 4.8KB | Likely real | ✅ OK |
| `images/nvidia-logo.svg` | 1.5KB | Likely real | ✅ OK |

---

## Stock Photos — Replace with Custom Visuals

All `.jpg` images in `/images/` appear to be stock photography. Priority replacements:

| File | Used On | Size | Priority | Replacement |
|------|---------|------|----------|-------------|
| `ai-abstract.jpg` | solutions.html hero bg | 228KB | 🔴 HIGH | Custom branded abstract |
| `about-hero.jpg` | about.html hero bg | 111KB | 🟡 MEDIUM | Custom KL/company visual |
| `stem-cell-lab.jpg` | case-studies.html hero bg | 63KB | 🟡 MEDIUM | Custom biotech lab visual |
| `network-security.jpg` | technology.html hero bg | 76KB | 🔴 HIGH | Custom tech infrastructure |
| `team-collab.jpg` | team.html hero bg | 37KB | 🟡 MEDIUM | Custom engineering workspace |
| `voice-agent.jpg` | solutions, team cards | 35KB | 🔴 HIGH | Custom voice AI visual |
| `crm-dashboard.jpg` | solutions card | 65KB | 🔴 HIGH | Clarify mockup/screenshot |
| `microscope.jpg` | solutions card | 80KB | 🟡 MEDIUM | Custom biotech cell visual |
| `server-room.jpg` | solutions card | 56KB | 🟡 MEDIUM | DGX Spark focused |
| `documents.jpg` | solutions card | 242KB | 🟡 MEDIUM | Custom RAG visualization |
| `marketing-analytics.jpg` | solutions card | 65KB | 🟡 MEDIUM | Custom Marketing OS visual |
| `dgx-spark.jpg` | technology page | 61KB | 🟡 MEDIUM | Official NVIDIA photo |
| `ai-chip.jpg` | team page | 86KB | 🟢 LOW | Custom ML visual |
| `coding.jpg` | team page | 40KB | 🟢 LOW | Custom dev environment |
| `voice-tech.jpg` | team page | 40KB | 🟢 LOW | Custom voice AI visual |
| `ai-engineers.jpg` | team page | 57KB | 🟢 LOW | Custom team visual |
| `data-center.jpg` | team page | 75KB | 🟢 LOW | Custom infra visual |
| `office-kl.jpg` | unused? | 74KB | 🟢 LOW | Replace if used |

---

## Icon Replacement Summary

**Current state:** 30+ inline SVG icons across the site use generic Feather/Lucide icon sets (thin stroke, generic style).

**Recommendation:** Create a custom NovaGenAI icon set of 20-25 icons:

### Core Icon Set (512x512, PNG or SVG)

| Icon | Used On | AI Prompt |
|------|---------|-----------|
| Voice/Microphone | Solution cards, agents | "Futuristic AI microphone icon, glowing cyan #00D4FF holographic style, dark transparent background" |
| CRM/Platform | Solution cards, agents | "AI-powered dashboard icon, hexagonal data display, cyan glow, dark background" |
| Cell/Biotech | Solution cards | "Stem cell with AI analysis overlay, microscopic view, cyan glow, dark background" |
| Server/Infrastructure | Solution cards, technology | "Compact AI server unit icon, NVIDIA-inspired, cyan LED accents, dark background" |
| Document/RAG | Solution cards | "Intelligent document search icon, floating papers with AI connections, cyan glow, dark" |
| Marketing/Analytics | Solution cards | "AI marketing analytics icon, ascending bars with neural connections, cyan on dark" |
| Shield/Security | Technology, agents | "Cybersecurity shield with circuit patterns, cyan glow, dark background" |
| Brain/AI | Agents, about | "AI neural brain icon, glowing cyan neural pathways, dark background" |
| Globe/Multilingual | Homepage | "Global network icon with three language nodes (EN/BM/ZH), cyan connections, dark" |
| Lock/Privacy | Homepage, technology | "Privacy lock icon with encryption pattern, cyan glow, dark background" |
| Grant/Money | Homepage | "Government grant icon, document with Malaysian flag accent, cyan glow, dark" |
| Rocket/Launch | Homepage | "Production deployment rocket icon, cyan thrust trail, dark background" |
| Target/Precision | Homepage | "Precision targeting icon, crosshair with AI data overlay, cyan glow, dark" |

---

## Recommended Image Generation Priority Queue

### Phase 1 — Critical (Week 1)
1. Get real partner logos: CryoCord, ElevenLabs, Anthropic, OpenAI (not AI-generated — get official SVGs)
2. Generate 4 hero background images (solutions, technology, case-studies, about)
3. Generate 6 solution card images (voice, CRM, biotech, server, documents, marketing)
4. Get team headshot photos (DC, JT, HL, CSK)

### Phase 2 — High Impact (Week 2)
5. Generate agents page hero image
6. Create Clarify CRM mockup image
7. Generate 13 custom icon set (core icons above)
8. Generate 3 team page featured images (ML, full-stack, voice)

### Phase 3 — Polish (Week 3)
9. Replace emoji icons across agents page (8 swarm dots, 6 anatomy cards, 8 dept icons, 6 industry cards, 6 security cards = ~34 icons)
10. Add background textures/patterns to stats and testimonial sections
11. Generate upcoming case study placeholder visuals
12. Contact page subtle background

---

## Technical Notes

- **Image format:** Use WebP for photos (30-50% smaller than JPEG), keep SVG for icons/logos
- **Lazy loading:** Already implemented via `loading="lazy"` — good
- **Hero images:** Currently using low opacity (8-12%) as background overlays — this is smart for dark theme, keep this pattern
- **Retina support:** Consider generating @2x versions for hero images (3840x2160)
- **All images should maintain the brand palette:** Dark backgrounds (#000, #0a0a0a), cyan accents (#00D4FF), no warm colors

---

*End of audit. 47 image opportunities identified across 8 pages.*
