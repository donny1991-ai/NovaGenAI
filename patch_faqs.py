#!/usr/bin/env python3
"""Replace FAQ data in build_visible.py with real buyer questions."""
import json, re

with open("/root/NovaGenAI/build_visible.py") as f:
    content = f.read()

# New FAQs for each page - real questions companies actually ask
NEW_FAQS = {
    "enterprise": [
        {"q":"We already have an internal IT team. Why would we use NovaGenAI instead of building AI ourselves?","a":"Building production AI requires deep specialisation — CUDA-level optimisation, model fine-tuning on NVIDIA NeMo, inference serving through Triton, multi-agent orchestration. Most internal teams take 12-18 months to ship what we deploy in weeks. We don't replace your team — we accelerate them. Your engineers focus on your business logic. We handle the AI infrastructure, model engineering, and production hardening."},
        {"q":"What guarantees do you provide? What happens if the AI makes a mistake?","a":"Every deployment includes: (1) defined accuracy and uptime SLAs with financial penalties, (2) human-in-the-loop approval for high-stakes decisions, (3) full audit logging so every AI action is traceable, (4) hallucination detection that flags uncertain outputs for review. The AI doesn't operate in a black box — you can see exactly what it did and why, at all times."},
        {"q":"How do you protect our proprietary data? Can you prove it stays private?","a":"We deploy on-premise — your data never leaves your building. For cloud deployments, we use dedicated infrastructure in your region with encryption at rest and in transit. We sign NDAs and data processing agreements as standard. We can provide our security architecture documentation and arrange a technical review with your security team before any commitment."},
        {"q":"What's the real total cost over 3 years? Not just the project price.","a":"Three components: (1) One-time deployment — RM 50,000 to RM 500,000 depending on scope. (2) Annual maintenance and support — typically 15-20% of deployment cost, includes model updates, monitoring, and SLA coverage. (3) Optional managed service for ongoing AI operations. No hidden fees. No per-user licensing. No API call charges. Every proposal includes a 3-year TCO breakdown before you commit."},
        {"q":"Can we speak to a reference client using your AI in production?","a":"Yes. After an initial discussion and NDA, we arrange reference calls with enterprise clients who have deployed our AI in production — across healthcare, biotech, and operations. You can ask them directly about deployment timelines, real-world performance, and what went wrong — because how we handle problems matters more than a perfect demo."},
        {"q":"We've tried AI vendors before and the project died after 6 months. How are you different?","a":"Most AI vendors sell a product and walk away. We embed with your team through deployment and beyond. Every engagement includes knowledge transfer to your staff, documentation of every component, no vendor lock-in (you own the models and deployment), and a defined handover. We measure success by whether your team can operate the AI independently within 90 days of go-live."},
    ],
    "healthcare": [
        {"q":"How do you handle MOH regulatory compliance and audits? Is your AI audit-ready?","a":"Every deployment includes: full audit logging of every AI decision, role-based access controls aligned with hospital hierarchies, consent management integrated into every patient data interaction, and automated compliance reporting. We design for MOH and PDPA requirements from architecture through deployment. We provide compliance documentation and can participate in your regulatory audits."},
        {"q":"What happens to patient data if we stop using NovaGenAI?","a":"You own your data. Always. Patient records, model outputs, audit logs — everything resides in your infrastructure. If you discontinue, we provide a complete data export in standard formats (FHIR, HL7, CSV) and documented decommissioning procedures. No data hostage situations. No proprietary formats. This is specified in every contract."},
        {"q":"Can your voice AI actually understand Malaysian patients — accents, code-switching, medical terms in BM?","a":"Yes, with production metrics to prove it. Our voice AI handles 85% of patient calls autonomously with 4.8/5 satisfaction in English, BM, and Mandarin. It understands Malaysian English accents, code-switching mid-sentence, and medical terminology in all three languages. This isn't theoretical — it's handling real patient calls every day."},
        {"q":"How do you integrate with our existing Hospital Information System or EMR?","a":"We integrate through standard healthcare APIs — FHIR, HL7, DICOM — as well as direct database connectors for common HIS platforms used in Malaysia. We don't require you to change your existing systems. Our AI reads from and writes to your current infrastructure. Integration is scoped and priced as part of every proposal with a technical feasibility assessment before commitment."},
        {"q":"Do you train your AI models on patient data? How do you handle privacy?","a":"For on-premise deployments, models can be fine-tuned on your data within your infrastructure — data never leaves. For base models, we use foundation models not trained on healthcare data. For fine-tuning, we use privacy-preserving techniques. Every model training approach is documented and reviewable by your compliance team before implementation."},
        {"q":"What's your experience with real clinical environments — not just labs or demos?","a":"Our healthcare AI was built and tested in live clinical operations — handling real patient calls, processing real medical records, operating under real regulatory requirements. We understand hospitals run 24/7, that downtime means patients don't get served, and that 'move fast and break things' doesn't work in healthcare. Our deployments include defined rollback procedures and 24/7 go-live support."},
    ],
    "agents": [
        {"q":"What's the actual difference between your AI agents and something we could build with ChatGPT's API?","a":"ChatGPT is a language model that generates text. Our AI agents are autonomous systems that plan multi-step tasks, use tools (APIs, databases, document systems), maintain state across complex workflows, coordinate with other specialised agents, and operate within enterprise guardrails. ChatGPT is a smart intern who answers questions. Our agents are a team of specialists running your operations autonomously with audit trails."},
        {"q":"How do you prevent AI agents from hallucinating or making dangerous decisions?","a":"Multiple layers: (1) RAG-backed retrieval — agents cite sources rather than generating from memory. (2) Hallucination detection that flags uncertain outputs. (3) Human-in-the-loop approval for any action above a configurable risk threshold. (4) Rate limiting and scope boundaries. (5) Full audit logging — replay and review every decision. For regulated environments, agents can be configured to never act without human approval."},
        {"q":"How much of our team's time will this actually save? Can you quantify it?","a":"At enterprise scale: 60% reduction in manual sales operations work, 85% of customer calls handled without human intervention, document processing accelerated 5x. But these are benchmarks — we baseline your specific workflows before deployment and project your numbers. Every engagement includes pre-deployment measurement and post-deployment verification so you see your actual ROI, not industry averages."},
        {"q":"What happens if an agent gets stuck or encounters something it can't handle?","a":"Agents are designed with graceful degradation. If they encounter an edge case, they escalate to a human with full context — what they were doing, what they tried, what went wrong. They don't guess. They don't silently fail. They hand off cleanly with a complete briefing. Our monitoring dashboard shows every escalation in real time."},
        {"q":"How do agents fit into our existing workflows — or do we need to change how we work?","a":"Agents integrate into your existing systems through standard APIs — SAP, Oracle, Dynamics, Salesforce, HubSpot, SharePoint. They don't require workflow changes. They handle tasks within your current processes: qualifying leads in your CRM, processing documents in your DMS, responding through your existing channels. Your team keeps working the same way."},
        {"q":"What skills do our people need to manage these agents after deployment?","a":"No AI expertise required. We provide: (1) a management dashboard to monitor, approve, and override agents, (2) documented operating procedures for every agent, (3) knowledge transfer training during deployment, (4) ongoing support. Within 90 days, your team should manage agents independently. You don't need to hire AI engineers."},
    ],
    "automation": [
        {"q":"We tried RPA before and it was a nightmare — bots breaking every time a form changed. How is AI automation different?","a":"RPA follows rigid rules on structured data — change one field and the bot breaks. AI automation understands context. A document in an unexpected format gets processed. A customer who phrases a question differently gets understood. A regulation that updates gets absorbed through knowledge base updates — no code changes. This isn't a marginal improvement over RPA. It's a different category of technology."},
        {"q":"What's the implementation process? Will it disrupt our operations during deployment?","a":"Phased rollout designed to avoid disruption: (1) Assessment — baseline your processes and identify targets (1-2 weeks). (2) Parallel run — automation runs alongside existing process so you compare outputs before switching (2-4 weeks). (3) Graduated cutover — move processes one at a time with rollback capability. (4) Stabilisation — monitoring and tuning for 2 weeks post-cutover. Your operations are never dependent on unproven automation."},
        {"q":"How do you measure ROI? What metrics should we expect?","a":"We define metrics together before writing code: processing time reduction, error rate reduction, manual hours eliminated, cost per transaction. We measure your baseline, set targets, and track against them. Typical results: 85% reduction in manual call handling, 5x faster documents, 60% less data entry. But your numbers depend on your processes — we'll project yours specifically."},
        {"q":"What if we want to stop using your automation later? Are we locked in?","a":"No lock-in. You own the automation workflows, configurations, and any models fine-tuned on your data. Everything runs in your infrastructure. If you discontinue, we provide complete documentation and a transition plan. Your processes keep running — you maintain them yourself or transition to another provider. Contractually specified."},
        {"q":"How long until we see actual results — not just a dashboard showing 'deployed'?","a":"Measurable results from Phase 1 — typically within 4 weeks. For focused deployments like document processing or customer service automation, metrics improve within the first month. For enterprise-wide automation, each phase delivers independent value so you're never waiting 6 months. We don't declare victory at 'deployment complete.' We declare victory when your metrics move."},
        {"q":"Can your automation handle our specific industry requirements — healthcare, finance, ISO?","a":"Yes. Our platform has been deployed in PDPA-regulated healthcare environments and is designed for BNM financial services and ISO compliance frameworks. Automated compliance checks, audit trail generation, and regulatory reporting are built in — not add-ons. We'll map your specific regulatory requirements during assessment and configure accordingly."},
    ],
    "company": [
        {"q":"Why should we work with a Malaysian AI company instead of a global vendor like Microsoft, Google, or AWS?","a":"Three reasons. (1) We deploy on-premise in Malaysia — your data stays under Malaysian jurisdiction. Global vendors route through foreign data centres. (2) We understand Malaysian regulations — PDPA, MOH, BNM — because we operate under them. Global vendors apply generic compliance templates. (3) You deal directly with the team building your AI — not a regional sales office escalating to a product team in another timezone."},
        {"q":"You were founded in 2025. Why should we trust a new company with critical AI infrastructure?","a":"Our AI was built and hardened in a 65% market share enterprise with 29+ staff and 10+ partner hospitals before NovaGenAI existed as a separate company. The technology has years of production runtime. The company structure is new. The AI is not. Judge us on our production metrics — 85% call deflection, 40% cost reduction — not our founding date."},
        {"q":"What happens if NovaGenAI goes out of business? How do we protect our investment?","a":"Every deployment includes: (1) full source code and documentation escrow — if we cease operations, you receive everything to maintain systems independently. (2) Your AI runs on your infrastructure — our existence doesn't affect operation. (3) All models and configurations are owned by you. (4) Transition support is contractually specified. Our business continuity is your business continuity."},
        {"q":"What's your team's background? Who would actually build our AI?","a":"Our team spans AI engineering, computational biology, enterprise software, and regulated industry deployment. The founding team built and operated AI at production scale before starting NovaGenAI. You work directly with senior engineers — not account managers relaying requirements to offshore teams. We'd rather show you our team's expertise during a technical discussion than list credentials here."},
        {"q":"Do you only work with Malaysian companies? What about Singapore or Australia?","a":"Headquartered in Cyberjaya, serving Malaysia, Singapore, and Australia. Our on-premise deployment model means we deploy AI in any jurisdiction. For Singapore: PDPA (Singapore) compliance. For Australia: Australian Privacy Principles. We're a Malaysian company with APAC delivery capability."},
        {"q":"What's the first step if we're interested but not ready to commit to a large project?","a":"Complimentary AI needs assessment — a 90-minute technical discussion where we understand your operations, identify where AI can deliver measurable results, and provide a preliminary architecture proposal with ballpark costs. No commitment. No invoice. If there's a fit, we propose a small paid proof-of-concept (typically RM 15,000-30,000, 2-3 weeks) that delivers actual working AI on a limited scope — so you evaluate real results, not slide decks."},
    ],
}

# Map page names to FAQ keys
page_map = {
    "enterprise-ai-company-malaysia.html": "enterprise",
    "healthcare-ai-malaysia.html": "healthcare",
    "ai-agents-malaysia.html": "agents",
    "ai-automation-malaysia.html": "automation",
    "ai-company-malaysia.html": "company",
}

# For each page, find and replace its faqs list
for page_file, faq_key in page_map.items():
    new_faqs = NEW_FAQS[faq_key]
    
    # Find the page's faqs section
    page_marker = f'"file":"{page_file}"'
    page_idx = content.find(page_marker)
    
    # Find faqs start
    faq_start = content.find('"faqs":[', page_idx)
    # Find the end of the faqs array - look for }], followed by faq_title
    faq_end = content.find('"faq_title"', faq_start)
    if faq_start == -1 or faq_end == -1:
        print(f"ERROR: Could not find faqs for {page_file}")
        continue
    # Back up to include the }], that closes the faqs array
    old_block = content[faq_start:faq_end]
    # Find the last }], before faq_title
    last_close = old_block.rfind('}],')
    if last_close > 0:
        old_block = old_block[:last_close+3]
    # Build replacement
    faq_json = json.dumps(new_faqs, ensure_ascii=False)
    new_block = f'"faqs":{faq_json},'
    content = content.replace(old_block, new_block)
    print(f"✓ {page_file}: {len(new_faqs)} new FAQs")

# Count how many times each old FAQ question appears (should be 0)
old_patterns = [
    "Who is the best enterprise AI",
    "Who builds the best healthcare AI",
    "Who builds the best AI agents",
    "Who provides the best AI automation",
    "What is the best AI company in Malaysia",
]
for p in old_patterns:
    count = content.count(p)
    if count > 0:
        print(f"⚠ WARNING: '{p}...' still appears {count}x")

open("/root/NovaGenAI/build_visible.py", "w").write(content)
print("\n✅ FAQ content replaced with real buyer questions.")
