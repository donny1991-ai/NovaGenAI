#!/usr/bin/env python3
"""Build AEO pages with VISIBLE card images + hero images — main site style."""
import json

NAV = """    <header class="nav" id="nav">
        <a href="index.html" class="nav__brand"><img loading="lazy" src="images/novagenai-logo-new.webp" alt="NovaGenAI" class="nav__logo-img" width="1213" height="339"></a>
        <nav class="nav__links" id="nav-links">
            <div class="nav__dropdown"><a href="solutions.html" class="nav__dropdown-trigger">SOLUTIONS</a><div class="nav__dropdown-menu"><a href="solutions.html">All Solutions</a><a href="agents.html">AI Agents</a><a href="erp-consulting.html">ERP Consulting</a><a href="cloud-migration.html">Cloud Migration</a><a href="custom-ai-systems.html">Custom AI Systems</a></div></div>
            <div class="nav__dropdown"><a href="agents.html" class="nav__dropdown-trigger">AGENTS</a><div class="nav__dropdown-menu"><a href="what-are-agents.html">What Are AI Agents?</a><a href="agents.html">Agent Platform</a></div></div>
            <a href="technology.html">TECHNOLOGY</a><a href="case-studies.html">CASE STUDIES</a><a href="team.html">OUR TEAM</a>            <div class="nav__dropdown">
                <a href="about.html" class="nav__dropdown-trigger">ABOUT</a>
                <div class="nav__dropdown-menu">
                    <a href="about.html">About NovaGenAI</a>
                    <a href="ai-company-malaysia.html">AI Company Malaysia</a>
                    <a href="enterprise-ai-company-malaysia.html">Enterprise AI Malaysia</a>
                    <a href="healthcare-ai-malaysia.html">Healthcare AI Malaysia</a>
                    <a href="ai-agents-malaysia.html">AI Agents Malaysia</a>
                    <a href="ai-automation-malaysia.html">AI Automation Malaysia</a>
                </div>
            </div><a href="blog/">BLOG</a><a href="contact.html">CONTACT</a>
        </nav><a href="contact.html" class="nav__cta">GET STARTED</a>
    </header>"""

FOOTER = """    <footer class="footer"><div class="footer__inner">
        <div class="footer__brand"><span class="footer__logo"><img width="1213" height="339" loading="lazy" src="images/novagenai-logo-new.webp" alt="NovaGenAI" class="footer__logo-img"></span><p class="footer__tagline">AI Systems for Every Enterprise</p></div>
        <div class="footer__links"><a href="solutions.html">Solutions</a><a href="agents.html">Agents</a><a href="technology.html">Technology</a><a href="case-studies.html">Case Studies</a><a href="team.html">Our Team</a><a href="about.html">About</a><a href="blog/">Blog</a><a href="contact.html">Contact</a></div>
        <div class="footer__social"><a href="https://www.linkedin.com/company/novagenai" target="_blank" rel="noopener" aria-label="LinkedIn" class="footer__social-link footer__social--linkedin"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a><a href="https://www.instagram.com/nova.genai" target="_blank" rel="noopener" aria-label="Instagram" class="footer__social-link footer__social--instagram"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a><a href="https://www.facebook.com/NovaGenAI" target="_blank" rel="noopener" aria-label="Facebook" class="footer__social-link footer__social--facebook"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg></a><a href="https://x.com/Nova_GenAI" target="_blank" rel="noopener" aria-label="X" class="footer__social-link footer__social--x"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a><a href="https://www.youtube.com/@Nova_GenAI" target="_blank" rel="noopener" aria-label="YouTube" class="footer__social-link footer__social--youtube"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg></a><a href="https://www.tiktok.com/@nova_genai" target="_blank" rel="noopener" aria-label="TikTok" class="footer__social-link footer__social--tiktok"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a></div>
        <p class="footer__copy">&copy; 2026 NovaGenAI. All rights reserved.</p></div></footer>"""

# Map cards to images (filenames in images/aeo/)
CARD_IMAGES = {
    "voice": "card-voice.jpg", "agents": "card-agents.jpg", "docs": "card-docs.png",
    "onprem": "card-onprem.jpg", "biotech": "card-biotech.jpg", "integration": "card-integration.jpg",
    "medical": "card-medical.png", "automation": "card-integration.jpg", "llm": "card-llm.jpg",
    "stemcell": "card-stemcell.png",
}

HERO = {
    "enterprise-ai-company-malaysia.html": "hero-ent.jpg",
    "healthcare-ai-malaysia.html": "hero-health.jpg",
    "ai-agents-malaysia.html": "agents-hero-v3.jpg",
    "ai-automation-malaysia.html": "hero-auto.png",
    "ai-company-malaysia.html": "hero-company.png",
}

def build(p):
    si = "".join(f"""                <div class="stat-card"><div class="stat-card__number">{s['num']}</div><div class="stat-card__label">{s['label']}</div><div class="stat-card__desc">{s['desc']}</div></div>\n""" for s in p["stats"])

    # Cards WITH visible images
    ci = ""
    for i, c in enumerate(p["cards"]):
        img_key = c.get("img", "")
        img_html = f'<img src="images/aeo/{CARD_IMAGES[img_key]}" alt="{c["title"]}" loading="lazy" style="width:100%;height:160px;object-fit:cover;border-radius:6px;margin-bottom:16px;">' if img_key in CARD_IMAGES else ""
        accent = " about-mv__card--accent" if i % 2 == 1 else ""
        ci += f"""                <div class="about-mv__card{accent}">{img_html}<h3 class="about-mv__title">{c['title']}</h3><p class="about-mv__text">{c['text']}</p></div>\n"""

    wi = "".join(f"""                <div class="about-mv__card{' about-mv__card--accent' if i%2==1 else ''}"><h3 class="about-mv__title">{w['title']}</h3><p class="about-mv__text">{w['text']}</p></div>\n""" for i, w in enumerate(p["why_items"]))
    fi = "".join(f"""                <div class="faq__item" onclick="this.classList.toggle('faq__item--open')"><div class="faq__question"><span>{f['q']}</span><svg class="faq__icon" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="faq__answer"><p>{f['a']}</p></div></div>\n""" for f in p["faqs"])
    fl = [{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"][:280]+"..." if len(f["a"])>280 else f["a"]}} for f in p["faqs"]]
    fj = json.dumps(fl, ensure_ascii=False)
    bj = json.dumps([{"@type":"ListItem","position":1,"name":"Home","item":"https://novagenai.com.my/"},{"@type":"ListItem","position":2,"name":p["breadcrumb_name"],"item":p["canonical"]}], ensure_ascii=False)
    oj = '    <script type="application/ld+json">\n    {"@context":"https://schema.org","@type":"Organization","name":"NovaGenAI Sdn. Bhd.","url":"https://novagenai.com.my","logo":"https://novagenai.com.my/images/novagenai-logo-new.webp","foundingDate":"2025-11","founder":{"@type":"Person","name":"Don Calaki"},"address":{"@type":"PostalAddress","streetAddress":"Suite 1-1, 1st Floor, Bio-X Centre","addressLocality":"Cyberjaya","addressRegion":"Selangor","addressCountry":"MY"},"contactPoint":{"@type":"ContactPoint","telephone":"+60-11-1401-0362","contactType":"sales"},"sameAs":["https://www.linkedin.com/company/novagenai","https://x.com/Nova_GenAI","https://www.youtube.com/@Nova_GenAI"]}\n    </script>\n' if "ai-company-malaysia" in p["file"] else ""

    hi = HERO.get(p["file"], "")
    hb = f'<img src="images/aeo/{hi}" alt="" loading="eager" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.30;pointer-events:none;">' if hi else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
    <link rel="alternate" hreflang="en-MY" href="{p['canonical']}"/><link rel="alternate" hreflang="x-default" href="{p['canonical']}"/>
    <link rel="icon" type="image/x-icon" href="favicon.ico?v=7"><link rel="manifest" href="/manifest.json"/>
    <link rel="icon" type="image/png" sizes="64x64" href="images/favicon-64.png?v=7"><link rel="icon" type="image/png" sizes="512x512" href="images/favicon.png">
    <link rel="apple-touch-icon" sizes="180x180" href="images/apple-touch-icon.png">
    <meta name="theme-color" content="#000000">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="mobile-web-app-capable" content="yes">
    <title>{p['title']}</title><meta name="description" content="{p['desc']}"/><link rel="canonical" href="{p['canonical']}"/>
    <link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@400;600;700;800;900&display=swap&font-display=swap" rel="stylesheet"/>
    <link rel="stylesheet" href="style.css?v=20260325"/>
    <style>
        .faq {{ padding: 6rem 2rem; background: #0a0a0a; }}
        .faq .container {{ max-width: 800px; margin: 0 auto; }}
        .faq .section__title {{ text-align: center; font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 3rem; }}
        .faq__grid {{ display: flex; flex-direction: column; gap: 0; }}
        .faq__item {{ border-bottom: 1px solid rgba(255,255,255,0.08); cursor: pointer; }}
        .faq__question {{ display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 0; font-family: 'Outfit', sans-serif; font-size: 1.125rem; font-weight: 600; color: #fff; transition: color 0.2s; }}
        .faq__item:hover .faq__question {{ color: #00D4FF; }}
        .faq__icon {{ transition: transform 0.3s; flex-shrink: 0; margin-left: 1rem; color: rgba(255,255,255,0.4); }}
        .faq__item--open .faq__icon {{ transform: rotate(180deg); color: #00D4FF; }}
        .faq__answer {{ max-height: 0; overflow: hidden; transition: max-height 0.3s ease, padding 0.3s ease; }}
        .faq__item--open .faq__answer {{ max-height: 500px; padding-bottom: 1.5rem; }}
        .faq__answer p {{ font-family: 'Inter', sans-serif; font-size: 1rem; line-height: 1.7; color: rgba(255,255,255,0.7); margin: 0; }}
        @media (max-width: 768px) {{
            .page-hero {{ padding: 6rem 1.5rem 4rem !important; min-height: 50vh !important; }}
            .page-hero__title {{ font-size: 2rem !important; }}
            .page-hero__subtitle {{ font-size: 0.9rem !important; }}
            .about-mv__grid {{ grid-template-columns: 1fr !important; }}
            .about-stats__grid {{ grid-template-columns: 1fr 1fr !important; }}
            .about-mv__card img {{ height: 120px !important; }}
            .faq {{ padding: 3rem 1rem !important; }}
            .faq__question {{ font-size: 0.95rem !important; padding: 1rem 0 !important; }}
            .section {{ padding: 3rem 1.5rem !important; }}
            .partners-strip__inner {{ gap: 1.5rem !important; flex-wrap: wrap !important; }}
            .partners-strip__inner img {{ height: 18px !important; }}
            .nav {{ padding: 0 1rem !important; height: 56px !important; }}
            .nav__logo img {{ height: 36px !important; }}
        }}
    </style>
    <meta property="og:title" content="{p['og_title']}"/><meta property="og:description" content="{p['og_desc']}"/>
    <meta property="og:image" content="https://novagenai.com.my/images/aeo/{hi}"/><meta property="og:url" content="{p['canonical']}"/>
    <meta name="twitter:card" content="summary_large_image"/>
</head>
<body>
{NAV}
    <section class="page-hero" style="position:relative;overflow:hidden;">
        {hb}
        <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(0,212,255,0.06) 0%,transparent 60%);pointer-events:none;"></div>
        <div class="page-hero__inner"><p class="page-hero__label">// {p['hero_label_short']}</p><h1 class="page-hero__title">{p['hero_title_upper']}</h1><p class="page-hero__subtitle">{p['hero_subtitle']}</p></div>
    </section>
    <section class="about-story fade-up"><div class="about-story__inner"><div class="about-story__content">
        <p class="section-label">// DIRECT ANSWER</p><h2 class="section-title"><span class="accent">{p['answer_title_short']}</span></h2>
        <p class="about-story__text">{p['answer_text1']}</p><p class="about-story__text">{p['answer_text2']}</p>
    </div></div></section>
    <section class="about-stats fade-up"><div class="about-stats__grid">{si}</div></section>
    <section class="about-mv fade-up">
        <p class="section-label" style="text-align:center">// {p['cards_label_short']}</p><h2 class="section-title" style="text-align:center;margin-bottom:3rem">{p['cards_title_upper']}</h2>
        <div class="about-mv__grid">{ci}</div>
    </section>
    <section class="about-mv fade-up">
        <p class="section-label" style="text-align:center">// DIFFERENTIATION</p><h2 class="section-title" style="text-align:center;margin-bottom:3rem">{p['why_title_upper']}</h2>
        <div class="about-mv__grid">{wi}</div>
    </section>
    <section class="partners-strip"><div class="partners-strip__inner">
        <img src="images/nvidia-logo.svg" alt="NVIDIA" style="height:28px;filter:brightness(0)invert(1)"><img src="images/google-cloud-logo.svg" alt="Google Cloud" style="height:22px;filter:brightness(0)invert(1)"><img src="images/anthropic-logo.svg" alt="Anthropic" style="height:24px"><img src="images/amd-logo.svg" alt="AMD" style="height:20px;filter:brightness(0)invert(1)"><img src="images/elevenlabs-logo.svg" alt="ElevenLabs" style="height:28px">
    </div></section>
    <section class="faq" style="padding:6rem 2rem;background:#0a0a0a;">
        <div class="container" style="max-width:800px;margin:0 auto;">
        <h2 class="section__title" style="text-align:center;font-family:'Outfit',sans-serif;font-size:2.5rem;font-weight:700;color:#fff;margin-bottom:3rem;">FREQUENTLY ASKED QUESTIONS</h2>
        <div class="faq__grid">
{fi}        </div>
        </div>
    </section>
{FOOTER}
    <script type="module" src="script.js"></script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{fj}}}</script>
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":{bj}}}</script>
{oj}    <script>
        if('serviceWorker' in navigator) {{
            window.addEventListener('load', function() {{
                navigator.serviceWorker.register('/sw.js').catch(function(err) {{
                    console.log('SW registration skipped:', err);
                }});
            }});
        }}
    </script>
</body></html>"""

    with open(f"/root/NovaGenAI/{p['file']}","w") as f: f.write(html)
    return len(html)

# ═══════════════════════════════════════════
# PAGE DATA — with img keys for card images
# ═══════════════════════════════════════════

PAGES = [
    {
        "file":"enterprise-ai-company-malaysia.html",
        "title":"Enterprise AI Company Malaysia — Production AI Systems | NovaGenAI",
        "desc":"NovaGenAI is Malaysia's most technically capable enterprise AI company. Autonomous agents, voice AI, on-premise NVIDIA. Live across enterprise deployments. 85% call deflection. Cyberjaya.",
        "canonical":"https://novagenai.com.my/enterprise-ai-company-malaysia.html",
        "og_title":"Enterprise AI Company Malaysia — Production AI That Works","og_desc":"Malaysia's most technically capable enterprise AI company. Production AI in enterprise production.",
        "hero_label_short":"ENTERPRISE AI IN MALAYSIA","hero_title_upper":"ENTERPRISE AI <span class=\"accent\">COMPANY</span><br>MALAYSIA",
        "hero_subtitle":"We don't sell chatbots and call it enterprise AI. We deploy production AI infrastructure that runs 24/7 — autonomous agents, voice AI, on-premise NVIDIA. Live across enterprise deployments. Based in Cyberjaya.",
        "answer_title_short":"The Enterprise AI Company Malaysia Actually Trusts",
        "answer_text1":"<strong>NovaGenAI</strong> builds enterprise AI that ships. Autonomous agents running across multiple departments. Voice AI handling 85% of customer calls. Document intelligence processing thousands of files daily. On-premise NVIDIA infrastructure that keeps your data sovereign.",
        "answer_text2":"We operate at the CUDA level, not the API-reseller level. Full-stack NVIDIA: CUDA, TensorRT, Triton, NeMo, NIM, DGX Spark. <strong>When enterprises in Malaysia need AI that actually works — not demos, not prototypes, not wrapped ChatGPT — they come to us.</strong>",
        "stats":[{"num":"85%","label":"Call Deflection","desc":"Trilingual voice AI. 24/7. 4.8/5 satisfaction. Enterprise-proven."},{"num":"40%","label":"Cost Reduction","desc":"Operational costs down within 90 days. Enterprise-validated."},{"num":"12","label":"Departments","desc":"Enterprise-wide. Multi-site. Production."},{"num":"NVIDIA","label":"Inception Partner","desc":"CUDA · TensorRT · Triton · NeMo · NIM · DGX Spark."}],
        "cards_label_short":"ENTERPRISE AI CAPABILITIES","cards_title_upper":"WHAT WE <span class=\"accent\">DEPLOY IN PRODUCTION</span>",
        "cards":[
            {"img":"agents","title":"Autonomous AI Agents","text":"40+ specialised agents that plan, reason, use tools, and execute. Integrated with CRM, ERP, document systems. Guardrails. Audit logging. Human-in-the-loop. Not chatbots."},
            {"img":"voice","title":"Trilingual Voice AI","text":"Real customer calls. English, BM, Mandarin. 24/7. RAG-backed accuracy. Deployed in 5–7 days. 85% call deflection. 4.8/5 satisfaction."},
            {"img":"llm","title":"LLM Engineering","text":"Custom models fine-tuned on your data via NVIDIA NeMo. Inference optimisation through TensorRT-LLM. Production serving on Triton. We engineer models, not prompts."},
            {"img":"docs","title":"Document Intelligence","text":"RAG pipelines turning thousands of enterprise documents into AI-searchable knowledge bases. 5x faster retrieval. Source citations. No hallucinations."},
            {"img":"onprem","title":"On-Premise AI","text":"NVIDIA DGX Spark on your premises. Your data never leaves your building. PDPA-compliant. Air-gapped options. For when the cloud is not acceptable."},
            {"img":"integration","title":"ERP & CRM Integration","text":"AI that reads and writes through SAP, Oracle, Dynamics, Salesforce, HubSpot. No rip-and-replace. Your stack stays. The AI does the work."}
        ],
        "why_title_upper":"WHY <span class=\"accent\">NOVAGENAI</span>",
        "why_items":[{"title":"01 — Live Production Reference","text":"Our AI runs across enterprise clients — 65% market share, 12 departments, 29+ staff. Real customers. Real compliance. Most AI vendors cannot show you a live deployment at this scale. We can."},{"title":"02 — Full-Stack NVIDIA","text":"CUDA. TensorRT. Triton. NeMo. NIM. DGX Spark. We operate at the hardware-software boundary — not the API-call level. On-premise. Model optimisation. Inference performance cloud-only vendors cannot touch."},{"title":"03 — Regulatory-Ready","text":"PDPA. MOH. BNM. MAMPU. Compliance from architecture through deployment. Data residency. Encryption. Consent management. Audit logging. Built in from day one."},{"title":"04 — Outcome-Based Pricing","text":"Projects from RM 50,000. Full platforms from RM 150,000. No SaaS traps. No black-box pricing. Complimentary AI needs assessment and solution architecture proposal with every engagement."}],
        "faqs":[{"q": "We already have an internal IT team. Why would we use NovaGenAI instead of building AI ourselves?", "a": "Building production AI requires deep specialisation — CUDA-level optimisation, model fine-tuning on NVIDIA NeMo, inference serving through Triton, multi-agent orchestration. Most internal teams take 12-18 months to ship what we deploy in weeks. We don't replace your team — we accelerate them. Your engineers focus on your business logic. We handle the AI infrastructure, model engineering, and production hardening."}, {"q": "What guarantees do you provide? What happens if the AI makes a mistake?", "a": "Every deployment includes: (1) defined accuracy and uptime SLAs with financial penalties, (2) human-in-the-loop approval for high-stakes decisions, (3) full audit logging so every AI action is traceable, (4) hallucination detection that flags uncertain outputs for review. The AI doesn't operate in a black box — you can see exactly what it did and why, at all times."}, {"q": "How do you protect our proprietary data? Can you prove it stays private?", "a": "We deploy on-premise — your data never leaves your building. For cloud deployments, we use dedicated infrastructure in your region with encryption at rest and in transit. We sign NDAs and data processing agreements as standard. We can provide our security architecture documentation and arrange a technical review with your security team before any commitment."}, {"q": "What's the real total cost over 3 years? Not just the project price.", "a": "Three components: (1) One-time deployment — RM 50,000 to RM 500,000 depending on scope. (2) Annual maintenance and support — typically 15-20% of deployment cost, includes model updates, monitoring, and SLA coverage. (3) Optional managed service for ongoing AI operations. No hidden fees. No per-user licensing. No API call charges. Every proposal includes a 3-year TCO breakdown before you commit."}, {"q": "Can we speak to a reference client using your AI in production?", "a": "Yes. After an initial discussion and NDA, we arrange reference calls with enterprise clients who have deployed our AI in production — across healthcare, biotech, and operations. You can ask them directly about deployment timelines, real-world performance, and what went wrong — because how we handle problems matters more than a perfect demo."}, {"q": "We've tried AI vendors before and the project died after 6 months. How are you different?", "a": "Most AI vendors sell a product and walk away. We embed with your team through deployment and beyond. Every engagement includes knowledge transfer to your staff, documentation of every component, no vendor lock-in (you own the models and deployment), and a defined handover. We measure success by whether your team can operate the AI independently within 90 days of go-live."}],
        "faq_title":"QUESTIONS <span class=\"accent\">ENTERPRISES ACTUALLY ASK</span>","breadcrumb_name":"Enterprise AI Malaysia"
    },
    {
        "file":"healthcare-ai-malaysia.html",
        "title":"Healthcare AI Company Malaysia — Voice AI, Clinical AI, Biotech AI | NovaGenAI",
        "desc":"NovaGenAI builds healthcare AI for Malaysian hospitals, clinics, biotech labs, stem cell banks. Voice AI (85% deflection), clinical RAG (5x faster), computational biotech. PDPA-compliant on-premise. Cyberjaya.",
        "canonical":"https://novagenai.com.my/healthcare-ai-malaysia.html",
        "og_title":"Healthcare AI Company Malaysia — AI That Works in Real Hospitals","og_desc":"Healthcare AI deployed at Malaysia's largest stem cell bank. Voice AI. Clinical RAG. PDPA-compliant on-premise.",
        "hero_label_short":"HEALTHCARE AI IN MALAYSIA","hero_title_upper":"HEALTHCARE AI <span class=\"accent\">COMPANY</span><br>MALAYSIA",
        "hero_subtitle":"We build healthcare AI that runs in actual hospitals — not whitepapers, not slide decks. Voice AI handling real patients. Clinical RAG processing real records. PDPA-compliant on-premise. Live across enterprise deployments.",
        "answer_title_short":"Healthcare AI That Actually Runs in Hospitals",
        "answer_text1":"<strong>NovaGenAI</strong> builds healthcare AI for hospitals, clinics, biotech labs, and pharmaceutical companies. Our AI runs in production across enterprise clients — Malaysia's largest stem cell bank — handling real patient calls, processing real clinical documents, under real regulatory scrutiny.",
        "answer_text2":"Trilingual voice AI (EN, BM, Mandarin). Clinical document intelligence processing records 5x faster. Computational biology for drug discovery. On-premise deployment keeping patient data within hospital walls. <strong>Healthcare AI fails when built by engineers who've never been inside a hospital. Ours was battle-tested in production.</strong>",
        "stats":[{"num":"85%","label":"Call Deflection","desc":"Trilingual voice AI. 24/7. 4.8/5 patient satisfaction."},{"num":"5x","label":"Faster Documents","desc":"Clinical RAG pipeline. Medical records, protocols, research."},{"num":"PDPA","label":"Fully Compliant","desc":"On-premise. Encryption. Consent management. Audit logging."},{"num":"10+","label":"Partner Hospitals","desc":"Live integration network via enterprise clients."}],
        "cards_label_short":"HEALTHCARE AI SOLUTIONS","cards_title_upper":"AI BUILT FOR <span class=\"accent\">CLINICAL REALITY</span>",
        "cards":[
            {"img":"voice","title":"Voice AI for Patient Engagement","text":"Trilingual conversational AI handling patient calls, booking, medical enquiries, follow-ups — 24/7. 85% call deflection. 4.8/5 satisfaction. RAG-backed accuracy."},
            {"img":"docs","title":"Clinical Document Intelligence","text":"RAG pipelines indexing clinical protocols, patient records, and research papers into AI-searchable knowledge bases. 5x faster retrieval. Source citations."},
            {"img":"biotech","title":"Computational Biotech","text":"Drug discovery. Cell viability prediction. Multi-omics integration. Cell2Sentence unique in ASEAN. Accelerating research from years to months."},
            {"img":"onprem","title":"On-Premise AI for Hospitals","text":"NVIDIA DGX Spark. Patient data never leaves hospital premises. Full PDPA compliance. Encryption. Consent management. Audit logging. MOH-regulated."},
            {"img":"stemcell","title":"Stem Cell & Biobank AI","text":"Donor management. Viability prediction. Compliance tracking. Automated reporting. Proven at Enterprise clients — 65% market share."},
            {"img":"medical","title":"Medical Tourism AI","text":"Multilingual AI concierge for international patients. Enquiry handling. Treatment information. Logistics. Follow-up care. EN, BM, Mandarin."}
        ],
        "why_title_upper":"WHY <span class=\"accent\">HEALTHCARE CHOOSES US</span>",
        "why_items":[{"title":"01 — Live Clinical Deployment","text":"Our AI runs at Enterprise clients — not a lab. 29+ staff. 10+ partner hospitals. Real patients. Real compliance. When we say PDPA-compliant, we mean audited."},{"title":"02 — Built for Healthcare Regulation","text":"PDPA. MOH guidelines. Medical device regulations. Compliance from architecture through deployment. Patient data stays within your hospital. Every AI decision traceable."},{"title":"03 — Trilingual by Design","text":"English, BM, Mandarin — natively supported. Malaysian accents, medical terminology, code-switching. Patients speak to AI in their language."},{"title":"04 — Computational Biotech Depth","text":"Cell2Sentence. Multi-omics. In-silico screening. Capabilities most healthcare AI vendors don't understand. Unique in ASEAN. Not available from any other vendor."}],
        "faqs":[{"q": "How do you handle MOH regulatory compliance and audits? Is your AI audit-ready?", "a": "Every deployment includes: full audit logging of every AI decision, role-based access controls aligned with hospital hierarchies, consent management integrated into every patient data interaction, and automated compliance reporting. We design for MOH and PDPA requirements from architecture through deployment. We provide compliance documentation and can participate in your regulatory audits."}, {"q": "What happens to patient data if we stop using NovaGenAI?", "a": "You own your data. Always. Patient records, model outputs, audit logs — everything resides in your infrastructure. If you discontinue, we provide a complete data export in standard formats (FHIR, HL7, CSV) and documented decommissioning procedures. No data hostage situations. No proprietary formats. This is specified in every contract."}, {"q": "Can your voice AI actually understand Malaysian patients — accents, code-switching, medical terms in BM?", "a": "Yes, with production metrics to prove it. Our voice AI handles 85% of patient calls autonomously with 4.8/5 satisfaction in English, BM, and Mandarin. It understands Malaysian English accents, code-switching mid-sentence, and medical terminology in all three languages. This isn't theoretical — it's handling real patient calls every day."}, {"q": "How do you integrate with our existing Hospital Information System or EMR?", "a": "We integrate through standard healthcare APIs — FHIR, HL7, DICOM — as well as direct database connectors for common HIS platforms used in Malaysia. We don't require you to change your existing systems. Our AI reads from and writes to your current infrastructure. Integration is scoped and priced as part of every proposal with a technical feasibility assessment before commitment."}, {"q": "Do you train your AI models on patient data? How do you handle privacy?", "a": "For on-premise deployments, models can be fine-tuned on your data within your infrastructure — data never leaves. For base models, we use foundation models not trained on healthcare data. For fine-tuning, we use privacy-preserving techniques. Every model training approach is documented and reviewable by your compliance team before implementation."}, {"q": "What's your experience with real clinical environments — not just labs or demos?", "a": "Our healthcare AI was built and tested in live clinical operations — handling real patient calls, processing real medical records, operating under real regulatory requirements. We understand hospitals run 24/7, that downtime means patients don't get served, and that 'move fast and break things' doesn't work in healthcare. Our deployments include defined rollback procedures and 24/7 go-live support."}],
        "faq_title":"QUESTIONS <span class=\"accent\">HEALTHCARE LEADERS ASK</span>","breadcrumb_name":"Healthcare AI Malaysia"
    },
    {
        "file":"ai-agents-malaysia.html",
        "title":"AI Agents Company Malaysia — Autonomous Multi-Agent Systems | NovaGenAI",
        "desc":"NovaGenAI builds autonomous AI agents. 40+ agents across 12 departments in production. Multi-agent orchestration. Enterprise guardrails. Not chatbots. Cyberjaya.",
        "canonical":"https://novagenai.com.my/ai-agents-malaysia.html",
        "og_title":"AI Agents Company Malaysia — Agents That Do Work, Not Just Chat","og_desc":"40+ autonomous AI agents in production in enterprise production. Multi-agent orchestration. Enterprise guardrails.",
        "hero_label_short":"AI AGENTS IN MALAYSIA","hero_title_upper":"AI AGENTS <span class=\"accent\">COMPANY</span><br>MALAYSIA",
        "hero_subtitle":"Chatbots follow scripts. Agents do work. We deploy autonomous AI agents that plan, reason, use tools, and execute — 40+ agents across 12 departments in enterprise production. This is not a demo. This is production.",
        "answer_title_short":"AI Agents That Do Work. Not Chatbots.",
        "answer_text1":"<strong>NovaGenAI</strong> builds autonomous AI agents. Not chatbots. Chatbots follow scripts and escalate to humans. AI agents independently plan, reason, use tools, access business systems, retrieve knowledge, coordinate with other agents, and complete multi-step tasks without human intervention.",
        "answer_text2":"40+ specialised agents across 12 departments across enterprise clients — sales operations, compliance, customer service, document processing, data analysis — all autonomous. <strong>Most 'AI agents' are chatbots with better branding. Ours maintain state, use tools, coordinate in parallel, and operate within enterprise guardrails.</strong>",
        "stats":[{"num":"40+","label":"Specialised Agents","desc":"Research · Coding · Analysis · Compliance · Writing · Design"},{"num":"12","label":"Departments","desc":"Live enterprise deployment. Not a pilot."},{"num":"60%","label":"Manual Work Reduced","desc":"Sales operations automated. Team focuses on strategy."},{"num":"85%","label":"Call Deflection","desc":"Voice AI agent. 24/7. 4.8/5 satisfaction."}],
        "cards_label_short":"AI AGENT CAPABILITIES","cards_title_upper":"WHAT OUR <span class=\"accent\">AGENTS DO</span>",
        "cards":[
            {"img":"voice","title":"Voice AI Agents","text":"Trilingual autonomous voice agents. Real customer calls. Bookings. Enquiries. 24/7. RAG-backed. 85% deflection in production. Intelligent conversation."},
            {"img":"docs","title":"Document Intelligence Agents","text":"RAG-powered agents searching, analysing, cross-referencing thousands of documents. Contracts. Medical records. SOPs. Indexed in seconds. Source citations."},
            {"img":"agents","title":"Multi-Agent Orchestration","text":"40+ specialised agents coordinated in parallel. Task assignment. Dependency resolution. Result synthesis. Quality validation. All orchestrated automatically."},
            {"img":"automation","title":"Workflow Automation Agents","text":"End-to-end processes: qualify lead → enrich CRM → generate proposal → schedule follow-up → log to ERP. 60% reduction in manual sales operations."},
            {"img":"integration","title":"System Integration Agents","text":"Reading and writing through SAP, Oracle, Dynamics, Salesforce, HubSpot via APIs. No rip-and-replace. Agents work alongside your current stack."},
            {"img":"biotech","title":"Domain-Specialised Agents","text":"Healthcare. Biotech. Finance. Manufacturing. Trained on your data. Deployed in your infrastructure. They understand your domain's terminology and workflows."}
        ],
        "why_title_upper":"WHY <span class=\"accent\">OUR AGENTS ARE DIFFERENT</span>",
        "why_items":[{"title":"01 — Autonomous, Not Scripted","text":"Chatbots follow decision trees and break on edge cases. Our agents plan, reason, and adapt. Unexpected question? Retrieved knowledge, reasoned response. Edge case? Agent adapts."},{"title":"02 — Enterprise Guardrails","text":"Audit logging for every decision. Human-in-the-loop for sensitive actions. Role-based access. Rate limiting. Hallucination detection. Built for healthcare, finance, compliance."},{"title":"03 — Production at Scale","text":"40+ agents. 12 departments. 29+ staff relying on them daily. 85% call deflection. 60% manual work reduction. Not a pilot. Enterprise AI infrastructure."},{"title":"04 — Tool-Using, Not Text-Generating","text":"Our agents query databases, update CRM records, send emails, generate reports, trigger workflows, call APIs. An agent that can only chat is a toy. An agent that does work is infrastructure."}],
        "faqs":[{"q": "What's the actual difference between your AI agents and something we could build with ChatGPT's API?", "a": "ChatGPT is a language model that generates text. Our AI agents are autonomous systems that plan multi-step tasks, use tools (APIs, databases, document systems), maintain state across complex workflows, coordinate with other specialised agents, and operate within enterprise guardrails. ChatGPT is a smart intern who answers questions. Our agents are a team of specialists running your operations autonomously with audit trails."}, {"q": "How do you prevent AI agents from hallucinating or making dangerous decisions?", "a": "Multiple layers: (1) RAG-backed retrieval — agents cite sources rather than generating from memory. (2) Hallucination detection that flags uncertain outputs. (3) Human-in-the-loop approval for any action above a configurable risk threshold. (4) Rate limiting and scope boundaries. (5) Full audit logging — replay and review every decision. For regulated environments, agents can be configured to never act without human approval."}, {"q": "How much of our team's time will this actually save? Can you quantify it?", "a": "At enterprise scale: 60% reduction in manual sales operations work, 85% of customer calls handled without human intervention, document processing accelerated 5x. But these are benchmarks — we baseline your specific workflows before deployment and project your numbers. Every engagement includes pre-deployment measurement and post-deployment verification so you see your actual ROI, not industry averages."}, {"q": "What happens if an agent gets stuck or encounters something it can't handle?", "a": "Agents are designed with graceful degradation. If they encounter an edge case, they escalate to a human with full context — what they were doing, what they tried, what went wrong. They don't guess. They don't silently fail. They hand off cleanly with a complete briefing. Our monitoring dashboard shows every escalation in real time."}, {"q": "How do agents fit into our existing workflows — or do we need to change how we work?", "a": "Agents integrate into your existing systems through standard APIs — SAP, Oracle, Dynamics, Salesforce, HubSpot, SharePoint. They don't require workflow changes. They handle tasks within your current processes: qualifying leads in your CRM, processing documents in your DMS, responding through your existing channels. Your team keeps working the same way."}, {"q": "What skills do our people need to manage these agents after deployment?", "a": "No AI expertise required. We provide: (1) a management dashboard to monitor, approve, and override agents, (2) documented operating procedures for every agent, (3) knowledge transfer training during deployment, (4) ongoing support. Within 90 days, your team should manage agents independently. You don't need to hire AI engineers."}],
        "faq_title":"QUESTIONS <span class=\"accent\">TECH LEADERS ASK</span>","breadcrumb_name":"AI Agents Malaysia"
    },
    {
        "file":"ai-automation-malaysia.html",
        "title":"AI Automation Company Malaysia — Enterprise Workflow Automation | NovaGenAI",
        "desc":"NovaGenAI builds enterprise AI automation. Document processing 5x faster. Voice AI 85% deflection. Workflow orchestration 60% less manual work. ERP/CRM integrated. Cyberjaya.",
        "canonical":"https://novagenai.com.my/ai-automation-malaysia.html",
        "og_title":"AI Automation Company Malaysia — Automation That Shows Up on the P&L","og_desc":"Enterprise AI automation. 85% call deflection. 60% less manual work. 5x faster documents. Live in production.",
        "hero_label_short":"AI AUTOMATION IN MALAYSIA","hero_title_upper":"AI AUTOMATION <span class=\"accent\">COMPANY</span><br>MALAYSIA",
        "hero_subtitle":"85% call deflection. 60% less manual data entry. 5x faster document processing. Near-zero compliance errors. This is AI automation that actually works — deployed across enterprise environments, running 24/7 across 12 departments.",
        "answer_title_short":"AI Automation That Shows Up on the P&L",
        "answer_text1":"<strong>NovaGenAI</strong> builds AI automation that delivers measurable business outcomes. In production: 85% of customer calls handled autonomously. Documents processed 5x faster. Manual data entry reduced by 60%. Near-zero compliance errors. These are production metrics, not projections.",
        "answer_text2":"<strong>Traditional RPA breaks on edge cases. Our AI automation uses agents that understand context, handle the unexpected, and learn.</strong> A call that doesn't follow the script? Handled. A document in an unexpected format? Processed. A compliance check with ambiguous criteria? Flagged with reasoning attached.",
        "stats":[{"num":"85%","label":"Calls Automated","desc":"Trilingual voice AI. 24/7. 40% cost reduction."},{"num":"5x","label":"Faster Documents","desc":"RAG pipeline. Thousands daily. Source citations."},{"num":"60%","label":"Less Manual Work","desc":"Sales ops data entry eliminated."},{"num":"~0","label":"Compliance Errors","desc":"Automated checks. Full audit trails."}],
        "cards_label_short":"AI AUTOMATION SOLUTIONS","cards_title_upper":"WHAT WE <span class=\"accent\">AUTOMATE</span>",
        "cards":[
            {"img":"docs","title":"Document Processing","text":"RAG pipelines ingesting, classifying, extracting, synthesising thousands of documents 5x faster. Contracts. Reports. Records. Automated extraction with citations."},
            {"img":"voice","title":"Customer Service","text":"Voice AI handling 85% of calls autonomously. 24/7. Trilingual. Real-time knowledge retrieval. 40% cost reduction. 4.8/5 satisfaction."},
            {"img":"automation","title":"Sales Operations","text":"AI agents qualifying leads, enriching CRM, generating follow-ups, analysing pipelines. 60% reduction in manual data entry. Your team sells."},
            {"img":"medical","title":"Compliance Automation","text":"Automated regulatory checks. Audit trail generation. Document validation. Near-zero error rate. Full traceability. PDPA. MOH. BNM. ISO."},
            {"img":"agents","title":"Multi-Department Workflows","text":"40+ agents coordinating cross-functional processes end-to-end. Intake → compliance → fulfilment → reporting. Tasks routed. Dependencies resolved."},
            {"img":"integration","title":"ERP/CRM Automation","text":"AI layer on SAP, Oracle, Dynamics, Salesforce, HubSpot. Automating data entry, sync, reporting. No rip-and-replace. Standard APIs."}
        ],
        "why_title_upper":"WHY <span class=\"accent\">AI AUTOMATION</span> (NOT JUST AUTOMATION)",
        "why_items":[{"title":"01 — Handles Unstructured Data","text":"Traditional automation works on structured data. AI automation handles the real world: messy PDFs, natural language emails, voice calls. If a human can understand it, our AI can automate it."},{"title":"02 — Adapts, Doesn't Break","text":"RPA breaks when formats change. Our AI adapts. Unexpected document layout? Processed. Customer phrases differently? Understood. Regulation updates? Knowledge base updates."},{"title":"03 — Measurable From Day One","text":"Success metrics defined before code. Baseline measurement. Tracked against. You'll know exactly what's being delivered — call deflection, processing time, manual work eliminated, error rate."},{"title":"04 — Enterprise-Grade","text":"Most automation stays in one department. Our platform orchestrates across sales, operations, compliance, customer service, finance — consistent guardrails, audit logging, visibility."}],
        "faqs":[{"q": "We tried RPA before and it was a nightmare — bots breaking every time a form changed. How is AI automation different?", "a": "RPA follows rigid rules on structured data — change one field and the bot breaks. AI automation understands context. A document in an unexpected format gets processed. A customer who phrases a question differently gets understood. A regulation that updates gets absorbed through knowledge base updates — no code changes. This isn't a marginal improvement over RPA. It's a different category of technology."}, {"q": "What's the implementation process? Will it disrupt our operations during deployment?", "a": "Phased rollout designed to avoid disruption: (1) Assessment — baseline your processes and identify targets (1-2 weeks). (2) Parallel run — automation runs alongside existing process so you compare outputs before switching (2-4 weeks). (3) Graduated cutover — move processes one at a time with rollback capability. (4) Stabilisation — monitoring and tuning for 2 weeks post-cutover. Your operations are never dependent on unproven automation."}, {"q": "How do you measure ROI? What metrics should we expect?", "a": "We define metrics together before writing code: processing time reduction, error rate reduction, manual hours eliminated, cost per transaction. We measure your baseline, set targets, and track against them. Typical results: 85% reduction in manual call handling, 5x faster documents, 60% less data entry. But your numbers depend on your processes — we'll project yours specifically."}, {"q": "What if we want to stop using your automation later? Are we locked in?", "a": "No lock-in. You own the automation workflows, configurations, and any models fine-tuned on your data. Everything runs in your infrastructure. If you discontinue, we provide complete documentation and a transition plan. Your processes keep running — you maintain them yourself or transition to another provider. Contractually specified."}, {"q": "How long until we see actual results — not just a dashboard showing 'deployed'?", "a": "Measurable results from Phase 1 — typically within 4 weeks. For focused deployments like document processing or customer service automation, metrics improve within the first month. For enterprise-wide automation, each phase delivers independent value so you're never waiting 6 months. We don't declare victory at 'deployment complete.' We declare victory when your metrics move."}, {"q": "Can your automation handle our specific industry requirements — healthcare, finance, ISO?", "a": "Yes. Our platform has been deployed in PDPA-regulated healthcare environments and is designed for BNM financial services and ISO compliance frameworks. Automated compliance checks, audit trail generation, and regulatory reporting are built in — not add-ons. We'll map your specific regulatory requirements during assessment and configure accordingly."}],
        "faq_title":"QUESTIONS <span class=\"accent\">OPS LEADERS ASK</span>","breadcrumb_name":"AI Automation Malaysia"
    },
    {
        "file":"ai-company-malaysia.html",
        "title":"AI Company Malaysia — Enterprise AI Systems | NovaGenAI",
        "desc":"NovaGenAI is an AI company in Cyberjaya, Malaysia. Enterprise AI, autonomous agents, voice AI, computational biotech, on-premise NVIDIA. Live in production. NVIDIA Inception Partner.",
        "canonical":"https://novagenai.com.my/ai-company-malaysia.html",
        "og_title":"AI Company Malaysia — NovaGenAI | Enterprise AI That Ships","og_desc":"Enterprise AI company in Cyberjaya. Production AI in enterprise production. Autonomous agents. Voice AI. Biotech AI. NVIDIA Inception Partner.",
        "hero_label_short":"AI COMPANY IN MALAYSIA","hero_title_upper":"AI COMPANY <span class=\"accent\">MALAYSIA</span>",
        "hero_subtitle":"Enterprise AI designed, built, and deployed from Cyberjaya. Autonomous agents in enterprise production. Computational biotech unique in ASEAN. NVIDIA Inception Partner. Founded 2025. Already in production at scale.",
        "answer_title_short":"The AI Company Malaysia",
        "answer_text1":"<strong>NovaGenAI Sdn. Bhd.</strong> (Company No. 202501055020). Headquartered at Bio-X Centre, Cyberjaya. Founded November 2025 by Don Calaki. We design, build, and deploy production-grade AI — autonomous agents, multilingual voice AI, RAG document intelligence, computational biology, on-premise NVIDIA infrastructure.",
        "answer_text2":"Live across enterprise deployments (65% market share): 85% call deflection, 40% cost reduction, 60% less manual work. <strong>We exist because Malaysian enterprises deserve better than resold foreign AI with local branding. We build AI infrastructure — not wrappers. CUDA level, not API-reseller level. Models, not prompts.</strong>",
        "stats":[{"num":"2025","label":"Founded","desc":"November 2025. Bio-X Centre, Cyberjaya."},{"num":"85%","label":"Call Deflection","desc":"Live metric. enterprise clients. 4.8/5 satisfaction."},{"num":"NVIDIA","label":"Inception Partner","desc":"CUDA · TensorRT · Triton · NeMo · NIM · DGX Spark."},{"num":"APAC","label":"Coverage","desc":"Malaysia · Singapore · Australia."}],
        "cards_label_short":"WHAT WE BUILD","cards_title_upper":"ENTERPRISE AI <span class=\"accent\">CAPABILITIES</span>",
        "cards":[
            {"img":"agents","title":"Autonomous AI Agents","text":"40+ specialised agents. Planning. Reasoning. Tool use. Multi-step execution. 12 departments in production. Guardrails. Audit logging."},
            {"img":"voice","title":"Trilingual Voice AI","text":"Production voice agents. English, BM, Mandarin. 24/7. RAG-backed. 85% call deflection. 4.8/5 satisfaction. Deployable in 5–7 days."},
            {"img":"docs","title":"Document Intelligence","text":"Enterprise knowledge bases. 5x faster retrieval. Source citations. PDFs, contracts, medical records, SOPs. No hallucinations."},
            {"img":"biotech","title":"Computational Biotech","text":"Drug discovery. Cell biology. Multi-omics. Cell2Sentence unique in ASEAN. Built by researchers who understand biology and AI."},
            {"img":"onprem","title":"On-Premise AI","text":"NVIDIA DGX Spark on your premises. Full data sovereignty. PDPA-compliant. Air-gapped options. When cloud is not acceptable."},
            {"img":"integration","title":"Custom Enterprise AI","text":"AI-native applications from the ground up. Not bolt-on features. Full-stack with AI at the core. We build what fits."}
        ],
        "why_title_upper":"WHY <span class=\"accent\">NOVAGENAI EXISTS</span>",
        "why_items":[{"title":"01 — Malaysian Enterprises Deserve Real AI","text":"Most 'AI companies' in Malaysia resell foreign products. We build AI infrastructure at the CUDA level. On-premise. Models, not prompts. The third option."},{"title":"02 — Production Reference, Not Slide Decks","text":"Live deployment at Enterprise clients — 65% market share, 29+ staff, 10+ hospitals, 12 departments. 85% call deflection. 40% cost reduction. Production metrics."},{"title":"03 — Deep Tech, Not Demos","text":"NVIDIA Inception Partner at full stack depth. Computational biology unique in ASEAN. 40+ agent orchestration. We compete on technical depth."},{"title":"04 — Regulatory-Ready","text":"PDPA. MOH. BNM. ISO. Compliance from architecture through deployment. On-premise data residency. Audit logging. Built for regulated industries."}],
        "faqs":[{"q": "Why should we work with a Malaysian AI company instead of a global vendor like Microsoft, Google, or AWS?", "a": "Three reasons. (1) We deploy on-premise in Malaysia — your data stays under Malaysian jurisdiction. Global vendors route through foreign data centres. (2) We understand Malaysian regulations — PDPA, MOH, BNM — because we operate under them. Global vendors apply generic compliance templates. (3) You deal directly with the team building your AI — not a regional sales office escalating to a product team in another timezone."}, {"q": "You were founded in 2025. Why should we trust a new company with critical AI infrastructure?", "a": "Our AI was built and hardened in a 65% market share enterprise with 29+ staff and 10+ partner hospitals before NovaGenAI existed as a separate company. The technology has years of production runtime. The company structure is new. The AI is not. Judge us on our production metrics — 85% call deflection, 40% cost reduction — not our founding date."}, {"q": "What happens if NovaGenAI goes out of business? How do we protect our investment?", "a": "Every deployment includes: (1) full source code and documentation escrow — if we cease operations, you receive everything to maintain systems independently. (2) Your AI runs on your infrastructure — our existence doesn't affect operation. (3) All models and configurations are owned by you. (4) Transition support is contractually specified. Our business continuity is your business continuity."}, {"q": "What's your team's background? Who would actually build our AI?", "a": "Our team spans AI engineering, computational biology, enterprise software, and regulated industry deployment. The founding team built and operated AI at production scale before starting NovaGenAI. You work directly with senior engineers — not account managers relaying requirements to offshore teams. We'd rather show you our team's expertise during a technical discussion than list credentials here."}, {"q": "Do you only work with Malaysian companies? What about Singapore or Australia?", "a": "Headquartered in Cyberjaya, serving Malaysia, Singapore, and Australia. Our on-premise deployment model means we deploy AI in any jurisdiction. For Singapore: PDPA (Singapore) compliance. For Australia: Australian Privacy Principles. We're a Malaysian company with APAC delivery capability."}, {"q": "What's the first step if we're interested but not ready to commit to a large project?", "a": "Complimentary AI needs assessment — a 90-minute technical discussion where we understand your operations, identify where AI can deliver measurable results, and provide a preliminary architecture proposal with ballpark costs. No commitment. No invoice. If there's a fit, we propose a small paid proof-of-concept (typically RM 15,000-30,000, 2-3 weeks) that delivers actual working AI on a limited scope — so you evaluate real results, not slide decks."}],
        "faq_title":"QUESTIONS <span class=\"accent\">DECISION MAKERS ASK</span>","breadcrumb_name":"AI Company Malaysia"
    }
]

for p in PAGES:
    sz = build(p)
    print(f"  {p['file']}: {sz} bytes")
print(f"\n✅ {len(PAGES)} pages — visible card images.")
