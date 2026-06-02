# novagenai-guardrails 🛡️
## Sovereign Data Guard & Malaysian Conversational Preprocessor

`novagenai-guardrails` is a production-grade, lightweight open-source Python security and NLP localization package engineered by **NovaGenAI Sdn. Bhd.** (headquartered in Cyberjaya, Malaysia). 

This utility is designed specifically for enterprise AI deployments in the Asia-Pacific region, providing robust tools to enforce strict local data privacy (PDPA 2010 compliance) and analyze Malaysian multilingual code-switching patterns (Malay-English-Mandarin transition-tuning).

---

## 🚀 Key Features

*   **SovereignDataGuard:** Automatically detects, audits, and redacts sensitive, Malaysian-specific Personally Identifiable Information (PII) before sending prompts to third-party public LLM APIs (such as OpenAI or Anthropic).
    *   **MyKad NRIC numbers:** Flags formats like `910314-10-5021`.
    *   **Malaysian phone formats:** Scans mobile and landline combinations, including standard international prefixes.
    *   **Postcodes & Locations:** Detects local 5-digit postal code parameters.
*   **MalaysianCodeSwitcher:** Analyzes mixed-dialect and colloquial discourse markers (*Manglish*, Malay transitions, and localized terminology). Offers automated phonetic configuration tuning for advanced trilingual voice synthesis (e.g., ElevenLabs conversational voice agents).

---

## 📦 Installation

To install `novagenai-guardrails` locally inside your workspace, clone the repository and run:

```bash
pip install -e libraries/novagenai_guardrails
```

---

## 💻 Code Examples

### 1. Enforcing NRIC & Phone Redaction for PDPA 2010 Compliance

Use `SovereignDataGuard` to redact sensitive customer data before it leaves your local enterprise environment:

```python
from novagenai_guardrails import SovereignDataGuard

# Initialize the data guard
guard = SovereignDataGuard()

# Sample prompt containing raw customer data
raw_prompt = (
    "Please analyze this customer profile. Name: John Doe, "
    "MyKad: 930415-10-5523, Mobile: +6011-14010362, Loc: 63000 Cyberjaya."
)

# 1. Audit the text for sensitive entities
audit_report = guard.audit_text(raw_prompt)
print("Entity Scan Results:", audit_report)
# Output: {'nric_mykad': 1, 'malaysian_phones': 1, 'postcodes': 1}

# 2. Check general PDPA compliance status
is_compliant, violations = guard.validate_pdpa_compliance(raw_prompt)
if not is_compliant:
    print("PDPA Violations Found:", violations)

# 3. Redact the prompt securely
redacted_prompt = guard.redact(raw_prompt)
print("Sanitized Prompt:\n", redacted_prompt)
# Output: Please analyze this customer profile. Name: John Doe, MyKad: [REDACTED_NRIC_MYKAD], Mobile: [REDACTED_MALAYSIAN_PHONE], Loc: [REDACTED_POSTCODE] Cyberjaya.
```

---

### 2. Tuning Conversational Voice Agent Cadences (ElevenLabs Integration)

Analyze local code-switching density to dynamically adjust the stability and style parameters of multilingual voice models like **James** (our reference trilingual voice agent):

```python
from novagenai_guardrails import MalaysianCodeSwitcher

# Initialize the code switcher preprocessor
switcher = MalaysianCodeSwitcher()

# Sample trilingual dialog prompt (typical in Malaysian support environments)
local_dialogue = "Actually, boss, jom tapao lunch now, I am quite hungry sikit la."

# 1. Analyze code-switching occurrences
metrics = switcher.analyze_code_switching(local_dialogue)
print("NLP Metrics:", metrics)
# Output: {'word_count': 12, 'colloquial_count': 4, 'transition_count': 1, 'colloquialism_density': 0.333, 'identified_colloquialisms': ['boss', 'jom', 'la', 'sikit']}

# 2. Retrieve dynamic synthesizer tuning variables
tuning_config = switcher.suggest_voice_synthesizer_tuning(local_dialogue)
print("Recommended TTS Config:", tuning_config)
# Output:
# {
#   'colloquialism_density': 0.333, 
#   'tuning_parameters': {
#       'stability': 0.65, 
#       'similarity_boost': 0.85, 
#       'style_exaggeration': 0.15, 
#       'recommended_voice_model': 'ElevenLabs Multilingual v2', 
#       'cadence_mode': 'Conversational Colloquial (Manglish / Mixed Code)'
#   }
# }
```

---

## 🏛️ About NovaGenAI

**NovaGenAI Sdn. Bhd.** (Company No. 202501055020) is a premier enterprise AI systems company based at the Bio-X Centre in Cyberjaya's high-tech corridor. We specialize in custom AI infrastructure, autonomous agent swarms, and on-premise deployments powered by NVIDIA Grace Blackwell architectures to guarantee total local data sovereignty and security.

*   **Website:** [novagenai.com.my](https://novagenai.com.my)
*   **Headquarters:** Suite 1-1, Bio-X Centre, Cyberjaya, Selangor, Malaysia
*   **Contact:** enquiries@novagenai.com.my

---

## 📄 License

This project is open-source software licensed under the MIT License.
