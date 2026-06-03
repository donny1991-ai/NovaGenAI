import pytest

from novagenai_guardrails import MalaysianCodeSwitcher, SovereignDataGuard


@pytest.fixture
def guard():
    return SovereignDataGuard()


def test_hyphenated_nric_detected(guard):
    assert guard.audit_text("IC 910314-10-5021")["NRIC_MYKAD"] == 1


def test_unhyphenated_nric_detected(guard):
    assert guard.audit_text("IC 910314105021")["NRIC_MYKAD"] == 1


def test_invalid_nric_state_code_rejected_in_strict_scan(guard):
    assert guard.audit_text("910314-60-5021")["NRIC_MYKAD"] == 0


def test_redact_failsafe_redacts_implausible_nric(guard):
    out = guard.redact("999999-99-9999", ["nric"])
    assert "[REDACTED_NRIC_MYKAD]" in out


def test_unknown_redaction_label_raises(guard):
    with pytest.raises(ValueError):
        guard.redact("hello", ["unknown"])


def test_bare_five_digits_not_redacted_as_postcode(guard):
    assert guard.redact("Invoice 63000 paid") == "Invoice 63000 paid"


def test_postcode_with_locality_redacted(guard):
    out = guard.redact("63000 Cyberjaya")
    assert "[REDACTED_POSTCODE]" in out


def test_email_detected(guard):
    assert guard.audit_text("reach me at don@novagenai.my")["EMAIL"] == 1


def test_card_luhn(guard):
    assert guard.audit_text("card 4111 1111 1111 1111")["PAYMENT_CARD"] == 1
    assert guard.audit_text("card 4111 1111 1111 1112")["PAYMENT_CARD"] == 0


def test_input_type_safety(guard):
    with pytest.raises(TypeError):
        guard.audit_text(12345)
    assert guard.audit_text(b"910314-10-5021")["NRIC_MYKAD"] == 1


@pytest.fixture
def code_switcher():
    return MalaysianCodeSwitcher()


def test_plain_english_low_density(code_switcher):
    analysis = code_switcher.analyze_code_switching("So basically the best boss and the steady team.")
    assert analysis["colloquialism_density"] < 0.12


def test_manglish_high_density(code_switcher):
    analysis = code_switcher.analyze_code_switching("Eh jom makan lah, tapi sikit only kan, alamak!")
    assert analysis["colloquialism_density"] > 0.12
    assert analysis["is_code_switching"]


def test_cjk_detected(code_switcher):
    analysis = code_switcher.analyze_code_switching("你好 can help me check 一下 lah?")
    assert "cjk" in analysis["scripts_present"]
    assert analysis["is_code_switching"]


def test_empty(code_switcher):
    analysis = code_switcher.analyze_code_switching("")
    assert analysis["word_count"] == 0
    assert analysis["colloquialism_density"] == 0.0


def test_tuning_profiles(code_switcher):
    formal = code_switcher.suggest_voice_synthesizer_tuning("The quarterly report is attached.")
    colloquial = code_switcher.suggest_voice_synthesizer_tuning("Jom lah, makan sikit, terbaik kan!")
    assert formal["tuning_parameters"]["profile"] == "standard_formal"
    assert colloquial["tuning_parameters"]["profile"] == "conversational_colloquial"
