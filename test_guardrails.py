import sys
import os

# Append libraries directory to python path for testing import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'libraries')))

from novagenai_guardrails import SovereignDataGuard, MalaysianCodeSwitcher

def test_guardrails():
    print("--- RUNNING INTEGRATION TESTS ---")
    
    # 1. Test SovereignDataGuard
    guard = SovereignDataGuard()
    test_text = "Call +6011-14010362 for details. Patient ID Card is 910314-10-5021. Postcode: 63000."
    
    counts = guard.audit_text(test_text)
    print("Audit counts:", counts)
    assert counts["nric_mykad"] == 1
    assert counts["malaysian_phones"] == 1
    assert counts["postcodes"] == 1
    
    is_comp, violations = guard.validate_pdpa_compliance(test_text)
    print("PDPA Compliance Status:", is_comp)
    print("Violations:", violations)
    assert not is_comp
    
    redacted = guard.redact(test_text)
    print("Redacted output:", redacted)
    assert "[REDACTED_NRIC_MYKAD]" in redacted
    assert "[REDACTED_MALAYSIAN_PHONE]" in redacted
    assert "[REDACTED_POSTCODE]" in redacted
    print("✓ SovereignDataGuard integration test passed!")
    
    # 2. Test MalaysianCodeSwitcher
    switcher = MalaysianCodeSwitcher()
    dialogue = "Actually boss, jom makan now, I am very hungry sikit la."
    
    analysis = switcher.analyze_code_switching(dialogue)
    print("Code switching metrics:", analysis)
    assert analysis["word_count"] == 11
    assert analysis["colloquial_count"] == 5
    assert analysis["colloquialism_density"] == 0.455
    
    tuning = switcher.suggest_voice_synthesizer_tuning(dialogue)
    print("Tuning config:", tuning)
    assert tuning["tuning_parameters"]["cadence_mode"] == "Conversational Colloquial (Manglish / Mixed Code)"
    print("✓ MalaysianCodeSwitcher integration test passed!")
    
    print("\n=============================================")
    print(" ALL NOVAGENAI-GUARDRAILS TESTS PASSED! 🛡️ ✓ ")
    print("=============================================")

if __name__ == "__main__":
    test_guardrails()
