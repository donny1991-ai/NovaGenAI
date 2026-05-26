# NovaGenAI — Enterprise AI Systems

> 🌐 **Live Site:** [https://novagenai.com.my](https://novagenai.com.my)

**NovaGenAI Sdn. Bhd.** is a Malaysian enterprise AI company building production-grade AI systems for businesses across healthcare, biotech, finance, and manufacturing.

Headquartered in **Cyberjaya, Malaysia** with operations in **Australia** and **Singapore**.

---

## 🚀 What We Build

- **Autonomous AI Agents** — Task-completing systems for enterprise workflows
- **Voice AI Platforms** — Multilingual conversational agents (English, Bahasa Malaysia, Mandarin)
- **Computational Biotech Intelligence** — AI-driven drug discovery and in-silico cellular modelling
- **AI-Native CRM** — Clarify platform for enterprise sales teams
- **Custom Enterprise Software** — Document intelligence, workflow automation, predictive systems

---

## 🏢 About NovaGenAI

- **Founded:** November 2025
- **Headquarters:** Bio-X Centre, Cyberjaya, Selangor, Malaysia
- **Founder & CEO:** Don Calaki
- **Website:** [novagenai.com.my](https://novagenai.com.my)
- **Email:** enquiries@novagenai.com.my
- **Partnerships:** NVIDIA Inception Program member

---

## 🌍 Global Presence

- **Malaysia** — Headquarters, R&D, AI infrastructure
- **Australia** — Melbourne operations
- **Singapore** — Regional client services

---

## 🏗️ Technology Stack

- **AI Models:** OpenAI GPT-5, Anthropic Claude, Google Gemini
- **Voice AI:** ElevenLabs, custom synthesis engines
- **Infrastructure:** NVIDIA DGX, Google Cloud, Azure
- **Frameworks:** LangChain, LlamaIndex, Haystack
- **Frontend:** Next.js, React, Tailwind CSS
- **Backend:** Node.js, Python, n8n workflow automation

---

## ✉️ Email API

The website contact forms submit to an Azure Functions email microservice in `src/email-api`.

- **Azure environment:** `novagen-email-prod`
- **Resource group:** `rg-novagen-email-prod`
- **Function App:** `func-novagen-email-prod-email-75z4am2jefaks`
- **Contact endpoint:** `https://func-novagen-email-prod-email-75z4am2jefaks.azurewebsites.net/api/contact`
- **SMTP config:** stored directly in Function App environment variables

Deploy with:

```bash
azd provision
azd deploy
```

SMTP credentials are not stored in this repository. The Function App reads `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`, `MAIL_FROM`, and `MAIL_TO` directly from Azure Function App environment variables. See `src/email-api/README.md`.

---

## 📄 License

© 2026 NovaGenAI Sdn. Bhd. All rights reserved.

---

## 📞 Contact

- **Website:** [https://novagenai.com.my](https://novagenai.com.my)
- **Email:** enquiries@novagenai.com.my
- **WhatsApp:** +60 11-1401 0362
- **LinkedIn:** [linkedin.com/company/novagenai](https://www.linkedin.com/company/novagenai)
- **GitHub:** [github.com/donny1991-ai/NovaGenAI](https://github.com/donny1991-ai/NovaGenAI)

---

**Intelligence That Transforms Business**
