"""Malaysian PII detection and redaction for LLM/voice pipelines.

Detection is intentionally transparent: regexes, structural validation, and
optional phone-number parsing. This is a DLP pre-filter, not a PDPA compliance
certification layer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Dict, Iterable, List, Optional, Tuple

try:
    import phonenumbers  # type: ignore

    _HAVE_PHONENUMBERS = True
except ImportError:  # pragma: no cover - exercised in minimal installs
    _HAVE_PHONENUMBERS = False


_VALID_NRIC_STATE_CODES = frozenset(
    {f"{n:02d}" for n in range(1, 14)}
    | {f"{n:02d}" for n in range(21, 60)}
    | {
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "98",
        "99",
    }
)


@dataclass(frozen=True)
class Finding:
    """A single detected PII entity."""

    label: str
    value: str
    start: int
    end: int


class SovereignDataGuard:
    """Detect and redact Malaysian PII before text leaves local infrastructure."""

    _NRIC_RE = re.compile(
        r"(?<!\d)(\d{6})[- ](\d{2})[- ](\d{4})(?!\d)"
        r"|(?<!\d)(\d{6})(\d{2})(\d{4})(?!\d)"
    )
    _PHONE_FALLBACK_RE = re.compile(
        r"(?<![\w.])(?:\+?60[- ]?|0)1[0-9][- ]?\d{3,4}[- ]?\d{4}\b"
        r"|(?<![\w.])(?:\+?60[- ]?|0)[3-9][- ]?\d{7,8}\b"
    )
    _EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
    _PASSPORT_RE = re.compile(r"\b[AHK]\d{8}\b")
    _CARD_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")
    _POSTCODE_RE = re.compile(
        r"\b\d{5}\b(?=\s+[A-Z][a-z]+)"
        r"|(?<=,\s)\b\d{5}\b"
        r"|(?<=(?i:poskod)\s)\b\d{5}\b"
        r"|(?<=(?i:poskod):\s)\b\d{5}\b"
        r"|(?<=(?i:postcode)\s)\b\d{5}\b"
        r"|(?<=(?i:postcode):\s)\b\d{5}\b",
    )

    _LABELS = {
        "nric": "NRIC_MYKAD",
        "phone": "MALAYSIAN_PHONE",
        "email": "EMAIL",
        "passport": "PASSPORT",
        "card": "PAYMENT_CARD",
        "postcode": "POSTCODE",
    }

    def __init__(self, default_region: str = "MY", validate_nric: bool = True):
        self.default_region = default_region
        self.validate_nric = validate_nric
        self.phone_backend = "phonenumbers" if _HAVE_PHONENUMBERS else "regex_fallback"

    @staticmethod
    def _coerce(text: object) -> str:
        if isinstance(text, str):
            return text
        if isinstance(text, (bytes, bytearray)):
            return bytes(text).decode("utf-8", errors="replace")
        raise TypeError(f"text must be str or bytes, got {type(text).__name__}")

    @staticmethod
    def _luhn_ok(digits: str) -> bool:
        checksum = 0
        parity = len(digits) % 2
        for i, char in enumerate(digits):
            n = int(char)
            if i % 2 == parity:
                n *= 2
                if n > 9:
                    n -= 9
            checksum += n
        return checksum % 10 == 0

    @classmethod
    def _nric_structurally_valid(cls, yymmdd: str, state: str) -> bool:
        if state not in _VALID_NRIC_STATE_CODES:
            return False

        yy, mm, dd = int(yymmdd[:2]), int(yymmdd[2:4]), int(yymmdd[4:6])
        if not (1 <= mm <= 12 and 1 <= dd <= 31):
            return False

        century = 1900 if yy > (date.today().year % 100) else 2000
        try:
            date(century + yy, mm, dd)
        except ValueError:
            return False
        return True

    @classmethod
    def supported_labels(cls) -> Dict[str, str]:
        """Return accepted short label names mapped to emitted finding labels."""

        return dict(cls._LABELS)

    def _find_nric(self, text: str, *, strict: bool) -> List[Finding]:
        findings: List[Finding] = []
        for match in self._NRIC_RE.finditer(text):
            groups = match.groups()
            yymmdd, state = (groups[0], groups[1]) if groups[0] else (groups[3], groups[4])
            if strict and self.validate_nric and not self._nric_structurally_valid(yymmdd, state):
                continue
            findings.append(Finding("NRIC_MYKAD", match.group(0), match.start(), match.end()))
        return findings

    def _find_phones(self, text: str) -> List[Finding]:
        if _HAVE_PHONENUMBERS:
            return [
                Finding("MALAYSIAN_PHONE", match.raw_string, match.start, match.end)
                for match in phonenumbers.PhoneNumberMatcher(text, self.default_region)
            ]

        return [
            Finding("MALAYSIAN_PHONE", match.group(0), match.start(), match.end())
            for match in self._PHONE_FALLBACK_RE.finditer(text)
        ]

    def _find_cards(self, text: str) -> List[Finding]:
        findings: List[Finding] = []
        for match in self._CARD_RE.finditer(text):
            digits = re.sub(r"[ -]", "", match.group(0))
            if 13 <= len(digits) <= 19 and self._luhn_ok(digits):
                findings.append(Finding("PAYMENT_CARD", match.group(0), match.start(), match.end()))
        return findings

    @staticmethod
    def _find_simple(text: str, regex: re.Pattern[str], label: str) -> List[Finding]:
        return [Finding(label, match.group(0), match.start(), match.end()) for match in regex.finditer(text)]

    def scan(self, text: object, *, strict: bool = True) -> List[Finding]:
        """Return findings sorted by position. In strict mode, NRICs are validated."""

        coerced = self._coerce(text)
        findings: List[Finding] = []
        findings += self._find_nric(coerced, strict=strict)
        findings += self._find_phones(coerced)
        findings += self._find_simple(coerced, self._EMAIL_RE, "EMAIL")
        findings += self._find_simple(coerced, self._PASSPORT_RE, "PASSPORT")
        findings += self._find_cards(coerced)
        findings += self._find_simple(coerced, self._POSTCODE_RE, "POSTCODE")
        return sorted(findings, key=lambda finding: (finding.start, finding.end))

    def audit_text(self, text: object) -> Dict[str, int]:
        """Return counts per entity label."""

        counts: Dict[str, int] = {label: 0 for label in self._LABELS.values()}
        for finding in self.scan(text):
            counts[finding.label] = counts.get(finding.label, 0) + 1
        return counts

    def _wanted_labels(self, labels_to_redact: Optional[Iterable[str]]) -> set[str]:
        if labels_to_redact is None:
            return set(self._LABELS.values())

        unknown = sorted(label for label in labels_to_redact if label not in self._LABELS)
        if unknown:
            known = ", ".join(sorted(self._LABELS))
            raise ValueError(f"unknown label(s): {', '.join(unknown)}. Known labels: {known}")

        return {self._LABELS[label] for label in labels_to_redact}

    def redact(
        self,
        text: object,
        labels_to_redact: Optional[Iterable[str]] = None,
        *,
        strict: bool = False,
    ) -> str:
        """Replace detected PII with ``[REDACTED_<LABEL>]`` placeholders."""

        coerced = self._coerce(text)
        wanted = self._wanted_labels(labels_to_redact)
        findings = [finding for finding in self.scan(coerced, strict=strict) if finding.label in wanted]

        result = coerced
        last_start = len(coerced) + 1
        for finding in sorted(findings, key=lambda item: (item.start, item.end), reverse=True):
            if finding.end > last_start:
                continue
            result = result[: finding.start] + f"[REDACTED_{finding.label}]" + result[finding.end :]
            last_start = finding.start
        return result

    def validate_pdpa_compliance(self, text: object) -> Tuple[bool, List[str]]:
        """Heuristically report whether this string contains detectable PII."""

        counts = self.audit_text(text)
        violations = [
            f"Contains {count} unredacted {label.replace('_', ' ').title()} value(s)."
            for label, count in counts.items()
            if count > 0
        ]
        return not violations, violations
