#!/usr/bin/env python3
"""v5: Premium UI — grain, glass, animation, cinematic imagery."""
import json

# ── IMAGE MAP ──
HERO_IMG = {
    "enterprise": "images/aeo/enterprise-hero-v2.png",
    "healthcare": "images/aeo/healthcare-ai-hero.jpg",
    "agents": "images/aeo/agents-hero-v2.jpg",
    "automation": "images/aeo/automation-hero-v2.jpg",
    "company": "images/aeo/company-hero-v2.png",
}

CSS = """/* ═══════════════════════════════════════════
   NovaGenAI AEO — v5 Premium Design System
   ═══════════════════════════════════════════ */
:root{
  --bg:#060708;--bg-panel:#0c0d0e;--bg-surface:#111213;--bg-elevated:#161718;
  --text-primary:#f5f5f6;--text-secondary:#c8ced6;--text-tertiary:#848992;--text-quaternary:#5b5f66;
  --accent:#D4A017;--accent-glow:#00D4FF;
  --accent-bg:rgba(212,160,23,0.08);--accent-glow-bg:rgba(0,212,255,0.05);
  --border-subtle:rgba(255,255,255,0.04);--border-standard:rgba(255,255,255,0.07);--border-emphasis:rgba(255,255,255,0.10);
  --glass:rgba(12,13,14,0.75);--glass-border:rgba(255,255,255,0.06);
  --radius-sm:8px;--radius:12px;--radius-lg:16px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{background:var(--bg)}
body{
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  background:var(--bg);color:var(--text-secondary);line-height:1.6;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
  position:relative;
}
/* Grain overlay */
body::before{
  content:'';position:fixed;inset:0;z-index:9999;pointer-events:none;opacity:0.035;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E");
  background-size:256px;
}

/* ── NAV ── */
.nav{
  position:sticky;top:0;z-index:100;
  background:rgba(6,7,8,0.82);backdrop-filter:blur(24px) saturate(1.2);
  -webkit-backdrop-filter:blur(24px) saturate(1.2);
  border-bottom:1px solid var(--border-subtle);padding:0 40px;height:60px;
  display:flex;align-items:center;justify-content:space-between;
}
.nav__logo{font-size:18px;font-weight:600;color:var(--text-primary);text-decoration:none;letter-spacing:-0.3px;display:flex;align-items:center;gap:8px}
.nav__logo img{height:26px}
.nav__links{display:flex;gap:28px;align-items:center}
.nav__links a{font-size:13px;font-weight:500;color:var(--text-tertiary);text-decoration:none;transition:color .15s;letter-spacing:0.01em}
.nav__links a:hover{color:var(--text-primary)}
.nav__cta{font-size:13px;font-weight:500;color:var(--bg);background:var(--accent);padding:7px 16px;border-radius:var(--radius-sm);text-decoration:none;transition:all .2s}
.nav__cta:hover{filter:brightness(1.12);box-shadow:0 0 24px rgba(212,160,23,0.2)}

/* ── HERO ── */
.hero{
  position:relative;padding:180px 40px 140px;text-align:center;
  max-width:100%;overflow:hidden;min-height:85vh;display:flex;align-items:center;justify-content:center;
}
.hero__bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.22;pointer-events:none;filter:saturate(1.1)}
.hero__overlay{position:absolute;inset:0;background:linear-gradient(180deg,var(--bg) 0%,transparent 30%,transparent 65%,var(--bg) 100%)}
.hero__vignette{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 40%,rgba(6,7,8,0.6) 100%);pointer-events:none}
.hero__glow{position:absolute;top:30%;left:50%;transform:translateX(-50%);width:700px;height:500px;background:radial-gradient(ellipse,var(--accent-glow-bg) 0%,transparent 70%);pointer-events:none}
.hero__inner{position:relative;z-index:1;max-width:960px}
.hero__label{
  font-size:12px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;
  color:var(--accent);margin-bottom:24px;
  display:inline-block;padding:6px 16px;
  border:1px solid rgba(212,160,23,0.2);border-radius:100px;
  background:rgba(212,160,23,0.06);
}
.hero__title{font-size:clamp(42px,6vw,68px);font-weight:700;color:var(--text-primary);line-height:1.04;letter-spacing:-2px;margin-bottom:28px}
.hero__title span{color:var(--accent-glow)}
.hero__subtitle{font-size:19px;color:var(--text-tertiary);line-height:1.65;max-width:680px;margin:0 auto;font-weight:400}
.hero__cta-row{margin-top:40px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.hero__btn-primary{display:inline-block;font-size:15px;font-weight:500;color:var(--bg);background:var(--accent);padding:14px 28px;border-radius:var(--radius-sm);text-decoration:none;transition:all .2s}
.hero__btn-primary:hover{filter:brightness(1.12);box-shadow:0 0 32px rgba(212,160,23,0.25);transform:translateY(-1px)}
.hero__btn-secondary{display:inline-block;font-size:15px;font-weight:500;color:var(--text-secondary);padding:14px 28px;border-radius:var(--radius-sm);text-decoration:none;border:1px solid var(--border-standard);transition:all .2s}
.hero__btn-secondary:hover{border-color:var(--border-emphasis);background:var(--bg-surface)}

/* ── SECTION ── */
.section{padding:100px 40px;max-width:1140px;margin:0 auto;position:relative}
.section__label{font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--accent);margin-bottom:20px}
.section__title{font-size:32px;font-weight:700;color:var(--text-primary);letter-spacing:-0.7px;line-height:1.18;margin-bottom:16px}
.section__title span{color:var(--accent-glow)}
.section__text{font-size:16px;color:var(--text-tertiary);line-height:1.75;max-width:780px}
.section__text strong{color:var(--text-secondary);font-weight:500}
.section-divider{height:1px;background:linear-gradient(90deg,transparent,var(--border-standard) 20%,var(--border-standard) 80%,transparent);max-width:1140px;margin:0 auto}

/* ── ANSWER BOX ── */
.answer-box{
  background:var(--bg-panel);border:1px solid var(--border-standard);
  border-left:2px solid var(--accent-glow);border-radius:0 var(--radius) var(--radius) 0;
  padding:28px 32px;margin-top:36px;position:relative;
}
.answer-box::before{content:'';position:absolute;left:-1px;top:0;bottom:0;width:2px;background:var(--accent-glow);opacity:0.3;filter:blur(4px)}
.answer-box p{font-size:15px;color:var(--text-secondary);line-height:1.7;position:relative}
.answer-box p strong{color:var(--text-primary);font-weight:600}

/* ── STATS ── */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border-subtle);border-radius:var(--radius-lg);overflow:hidden;margin-top:48px}
.stat{background:var(--bg-panel);padding:36px 28px;text-align:center;transition:background .25s;position:relative}
.stat:hover{background:var(--bg-surface)}
.stat::after{content:'';position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:0;height:2px;background:var(--accent-glow);transition:width .3s}
.stat:hover::after{width:40px}
.stat__num{font-size:40px;font-weight:700;color:var(--text-primary);letter-spacing:-1px;margin-bottom:6px}
.stat__label{font-size:11px;font-weight:600;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:0.08em}
.stat__desc{font-size:12px;color:var(--text-quaternary);margin-top:8px;line-height:1.5}

/* ── CARDS — glass morphism ── */
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:48px}
.card{
  background:var(--glass);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:32px;
  transition:all .3s;position:relative;overflow:hidden;
}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent-glow),transparent);opacity:0;transition:opacity .3s}
.card:hover{background:var(--bg-surface);border-color:var(--border-standard);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,0.5),0 0 0 1px rgba(0,212,255,0.05)}
.card:hover::before{opacity:0.5}
.card__icon{font-size:32px;margin-bottom:20px;display:block}
.card__title{font-size:16px;font-weight:600;color:var(--text-primary);letter-spacing:-0.3px;margin-bottom:12px}
.card__text{font-size:13.5px;color:var(--text-tertiary);line-height:1.65}

/* ── WHY CARDS ── */
.why-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:48px}
.why-card{
  background:var(--glass);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:36px;
  transition:all .3s;position:relative;
}
.why-card:hover{background:var(--bg-surface);border-color:var(--border-standard);box-shadow:0 8px 30px rgba(0,0,0,0.4)}
.why-card__num{font-size:11px;font-weight:700;color:var(--accent);letter-spacing:0.14em;text-transform:uppercase;margin-bottom:16px}
.why-card__title{font-size:18px;font-weight:600;color:var(--text-primary);letter-spacing:-0.4px;margin-bottom:12px}
.why-card__text{font-size:14.5px;color:var(--text-tertiary);line-height:1.7}

/* ── PARTNERS ── */
.partners{display:flex;justify-content:center;align-items:center;gap:40px;flex-wrap:wrap;margin-top:32px;opacity:0.28;transition:opacity .3s}
.partners:hover{opacity:0.42}
.partners img{height:26px}

/* ── FAQ ── */
.faq{margin-top:48px;display:flex;flex-direction:column;gap:1px;background:var(--border-subtle);border-radius:var(--radius-lg);overflow:hidden}
.faq details{background:var(--bg-panel);transition:all .2s}
.faq details:hover{background:var(--bg-surface)}
.faq details[open]{background:var(--bg-surface);box-shadow:inset 0 0 0 1px var(--border-standard)}
.faq summary{
  font-size:15px;font-weight:500;color:var(--text-primary);padding:24px 32px;
  cursor:pointer;list-style:none;display:flex;align-items:center;
  justify-content:space-between;user-select:none;transition:color .15s;
}
.faq details[open] summary{color:var(--accent-glow)}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'+';font-size:22px;font-weight:300;color:var(--text-quaternary);transition:all .25s;flex-shrink:0;margin-left:20px}
.faq details[open] summary::after{content:'−';color:var(--accent-glow);transform:rotate(180deg)}
.faq .faq__a{font-size:14.5px;color:var(--text-tertiary);line-height:1.75;padding:0 32px 28px 32px}

/* ── CTA ── */
.cta{
  text-align:center;padding:100px 40px;
  background:linear-gradient(180deg,var(--bg) 0%,var(--accent-bg) 40%,rgba(0,212,255,0.02) 100%);
  border:1px solid var(--border-subtle);border-radius:var(--radius-lg);
  margin:80px 40px 0;position:relative;overflow:hidden;
}
.cta::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:500px;height:300px;background:radial-gradient(ellipse,var(--accent-glow-bg) 0%,transparent 70%);pointer-events:none}
.cta__title{font-size:30px;font-weight:700;color:var(--text-primary);letter-spacing:-0.7px;margin-bottom:16px;position:relative}
.cta__text{font-size:17px;color:var(--text-tertiary);margin-bottom:32px;position:relative}
.cta__btn{display:inline-block;font-size:16px;font-weight:500;color:var(--bg);background:var(--accent);padding:14px 32px;border-radius:var(--radius-sm);text-decoration:none;transition:all .25s;position:relative}
.cta__btn:hover{filter:brightness(1.12);box-shadow:0 0 40px rgba(212,160,23,0.3);transform:translateY(-2px)}

/* ── FOOTER ── */
.footer{border-top:1px solid var(--border-subtle);padding:56px 40px;text-align:center}
.footer__links{display:flex;justify-content:center;gap:28px;flex-wrap:wrap;margin-bottom:20px}
.footer__links a{font-size:13px;color:var(--text-quaternary);text-decoration:none;transition:color .15s}
.footer__links a:hover{color:var(--text-secondary)}
.footer__copy{font-size:12px;color:var(--text-quaternary)}

/* ── ANIMATIONS ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes subtleFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}

/* ── RESPONSIVE ── */
@media(max-width:768px){
  .stats{grid-template-columns:repeat(2,1fr)}.cards{grid-template-columns:1fr}.why-grid{grid-template-columns:1fr}
  .hero{padding:120px 24px 100px;min-height:70vh}.hero__title{font-size:clamp(30px,8vw,44px)}
  .section{padding:64px 24px}.nav{padding:0 20px}.nav__links{display:none}
  .cta{margin:48px 16px 0;padding:64px 24px}
}"""

PARTNERS = """    <div class="section-divider"></div>
    <section class="section"><p class="section__label">Technology Partners</p>
        <div class="partners">
            <img src="images/nvidia-logo.svg" alt="NVIDIA" style="filter:brightness(0) invert(1)">
            <img src="images/google-cloud-logo.svg" alt="Google Cloud" style="filter:brightness(0) invert(1)">
            <img src="images/anthropic-logo.svg" alt="Anthropic">
            <img src="images/amd-logo.svg" alt="AMD" style="filter:brightness(0) invert(1)">
            <img src="images/elevenlabs-logo.svg" alt="ElevenLabs">
        </div></section>"""

FOOTER = """    <footer class="footer"><div class="footer__links">
            <a href="solutions.html">Solutions</a><a href="agents.html">Agents</a><a href="case-studies.html">Case Studies</a>
            <a href="team.html">Team</a><a href="about.html">About</a><a href="blog/">Blog</a><a href="contact.html">Contact</a>
        </div><p class="footer__copy">&copy; 2026 NovaGenAI Sdn. Bhd.</p></footer>"""

def build(p, hero_key):
    fi="".join(f'            <details><summary>{f["q"]}</summary><div class="faq__a">{f["a"]}</div></details>\n' for f in p["faqs"])
    si="".join(f'            <div class="stat"><div class="stat__num">{s["num"]}</div><div class="stat__label">{s["label"]}</div><div class="stat__desc">{s["desc"]}</div></div>\n' for s in p["stats"])
    ci="".join(f'            <div class="card"><span class="card__icon">{c["icon"]}</span><div class="card__title">{c["title"]}</div><div class="card__text">{c["text"]}</div></div>\n' for c in p["cards"])
    wi="".join(f'            <div class="why-card"><div class="why-card__num">0{i+1}</div><div class="why-card__title">{w["title"]}</div><div class="why-card__text">{w["text"]}</div></div>\n' for i,w in enumerate(p["why_items"]))
    fl=[{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"][:280]+"..." if len(f["a"])>280 else f["a"]}} for f in p["faqs"]]
    fj=json.dumps(fl,ensure_ascii=False)
    bj=json.dumps([{"@type":"ListItem","position":1,"name":"Home","item":"https://novagenai.com.my/"},{"@type":"ListItem","position":2,"name":p["breadcrumb_name"],"item":p["canonical"]}],ensure_ascii=False)
    oj=""
    if "ai-company-malaysia" in p["file"]:
        oj='    <script type="application/ld+json">\n    {"@context":"https://schema.org","@type":"Organization","name":"NovaGenAI Sdn. Bhd.","url":"https://novagenai.com.my","logo":"https://novagenai.com.my/images/novagenai-logo-new.webp","description":"Enterprise AI company based in Cyberjaya, Malaysia.","foundingDate":"2025-11","founder":{"@type":"Person","name":"Don Calaki"},"address":{"@type":"PostalAddress","streetAddress":"Suite 1-1, 1st Floor, Bio-X Centre","addressLocality":"Cyberjaya","addressRegion":"Selangor","addressCountry":"MY"},"contactPoint":{"@type":"ContactPoint","telephone":"+60-11-1401-0362","contactType":"sales"},"sameAs":["https://www.linkedin.com/company/novagenai","https://x.com/Nova_GenAI","https://www.youtube.com/@Nova_GenAI"]}\n    </script>\n'

    h=f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
    <link rel="alternate" hreflang="en-MY" href="{p['canonical']}"/><link rel="alternate" hreflang="x-default" href="{p['canonical']}"/>
    <link rel="icon" type="image/x-icon" href="favicon.ico?v=7"><link rel="manifest" href="/manifest.json"/>
    <link rel="icon" type="image/png" sizes="64x64" href="images/favicon-64.png?v=7"><link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
    <title>{p['title']}</title><meta name="description" content="{p['desc']}"/><link rel="canonical" href="{p['canonical']}"/>
    <link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
    <meta property="og:title" content="{p['og_title']}"/><meta property="og:description" content="{p['og_desc']}"/>
    <meta property="og:image" content="https://novagenai.com.my/{HERO_IMG[hero_key]}"/><meta property="og:url" content="{p['canonical']}"/>
    <meta name="twitter:card" content="summary_large_image"/>
    <style>{CSS}</style>
</head>
<body>
    <header class="nav"><a href="index.html" class="nav__logo"><img src="images/novagenai-logo-new.webp" alt="NovaGenAI"> NovaGenAI</a>
        <nav class="nav__links"><a href="solutions.html">Solutions</a><a href="agents.html">Agents</a><a href="case-studies.html">Case Studies</a><a href="blog/">Blog</a><a href="contact.html" class="nav__cta">Get Started</a></nav></header>
    <section class="hero">
        <img src="{HERO_IMG[hero_key]}" alt="" class="hero__bg" loading="eager"><div class="hero__overlay"></div><div class="hero__vignette"></div><div class="hero__glow"></div>
        <div class="hero__inner"><p class="hero__label">{p['hero_label']}</p><h1 class="hero__title">{p['hero_title']}</h1><p class="hero__subtitle">{p['hero_subtitle']}</p>
        <div class="hero__cta-row"><a href="contact.html" class="hero__btn-primary">Get Started</a><a href="case-studies.html" class="hero__btn-secondary">View Case Studies →</a></div></div>
    </section>
    <div class="section-divider"></div>
    <section class="section"><p class="section__label">Direct Answer</p><h2 class="section__title">{p['answer_title']}</h2><p class="section__text">{p['answer_text1']}</p>
        <div class="answer-box">{p['answer_box']}</div><div class="stats">{si}</div></section>
    <div class="section-divider"></div>
    <section class="section"><p class="section__label">{p['cards_label']}</p><h2 class="section__title">{p['cards_title']}</h2><div class="cards">{ci}</div></section>
    <div class="section-divider"></div>
    <section class="section"><p class="section__label">Differentiation</p><h2 class="section__title">{p['why_title']}</h2><div class="why-grid">{wi}</div></section>
    {PARTNERS}
    <div class="section-divider"></div>
    <section class="section"><p class="section__label">FAQ</p><h2 class="section__title">Questions <span>Companies Actually Ask</span></h2><div class="faq">{fi}</div></section>
    <div class="cta"><div class="cta__title">{p['cta_title']}</div><p class="cta__text">{p['cta_text']}</p><a href="contact.html" class="cta__btn">Get Started</a></div>
    {FOOTER}
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{fj}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":{bj}}}</script>
{oj}</body></html>"""
    with open(f"/root/NovaGenAI/{p['file']}","w") as f: f.write(h)
    return len(h)

# ── Same page data as v4 (abbreviated import) ──
# Using the existing data from build_v4.py
import sys; sys.path.insert(0,'/root/NovaGenAI')
# Just inline the pages list from the previous build
exec(open("/root/NovaGenAI/build_v4.py").read().split("# ── PAGE DATA ──")[1].split("for p in PAGES:")[0])

hero_map = {
    "enterprise-ai-company-malaysia.html": "enterprise",
    "healthcare-ai-malaysia.html": "healthcare",
    "ai-agents-malaysia.html": "agents",
    "ai-automation-malaysia.html": "automation",
    "ai-company-malaysia.html": "company",
}

for p in PAGES:
    sz = build(p, hero_map[p["file"]])
    print(f"  {p['file']}: {sz} bytes")
print(f"\n✅ v5 done — {len(PAGES)} pages.")
