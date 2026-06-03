"""Manglish / Malay-English-Mandarin code-switch detection.

The detector is lexicon-based and returns voice tuning profile defaults. It is
designed to be easy to audit and tune against local listening tests.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

try:
    import jieba  # type: ignore

    jieba.setLogLevel(60)
    _HAVE_JIEBA = True
except ImportError:  # pragma: no cover - exercised in minimal installs
    _HAVE_JIEBA = False


_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]+")
_TOKEN_RE = re.compile(r"[A-Za-z\u00C0-\u00FF\u0100-\u017F\u0180-\u024F']+", re.UNICODE)


class MalaysianCodeSwitcher:
    """Detect colloquial Malaysian code-switching and recommend voice profiles."""

    _STRONG_MARKERS: Dict[str, float] = {
        marker: 1.0
        for marker in (
            "lah",
            "leh",
            "meh",
            "lor",
            "mah",
            "wat",
            "sikit",
            "jom",
            "kan",
            "wey",
            "wei",
            "giler",
            "tapao",
            "belanja",
            "terbaik",
            "kantoi",
            "alamak",
            "aiyo",
            "aiya",
            "walao",
            "shiok",
            "bojio",
            "paiseh",
            "macam",
            "sebab",
            "tapi",
            "sekarang",
            "faham",
            "boleh",
            "tak",
        )
    }
    _WEAK_MARKERS: Dict[str, float] = {
        marker: 0.25
        for marker in ("boss", "bos", "best", "steady", "habis", "geng", "chop", "makan", "la")
    }
    _TRANSITION_MARKERS = frozenset(
        {"macam", "sebab", "sekarang", "tapi", "atau", "faham", "actually", "basically", "meaning"}
    )

    def __init__(self) -> None:
        self._markers = {**self._WEAK_MARKERS, **self._STRONG_MARKERS}

    @staticmethod
    def _coerce(text: object) -> str:
        if isinstance(text, str):
            return text
        if isinstance(text, (bytes, bytearray)):
            return bytes(text).decode("utf-8", errors="replace")
        raise TypeError(f"text must be str or bytes, got {type(text).__name__}")

    def tokenize(self, text: object) -> List[str]:
        """Return lowercase Latin tokens plus segmented CJK tokens."""
        coerced = self._coerce(text).lower()
        tokens: List[str] = []
        idx = 0
        for match in _CJK_RE.finditer(coerced):
            tokens += _TOKEN_RE.findall(coerced[idx : match.start()])
            cjk = match.group(0)
            tokens += list(jieba.cut(cjk)) if _HAVE_JIEBA else list(cjk)
            idx = match.end()
        tokens += _TOKEN_RE.findall(coerced[idx:])
        return [token for token in tokens if token.strip()]

    @staticmethod
    def _scripts_present(text: str) -> List[str]:
        scripts = []
        if re.search(r"[A-Za-z]", text):
            scripts.append("latin")
        if _CJK_RE.search(text):
            scripts.append("cjk")
        return scripts or ["unknown"]

    def analyze_code_switching(self, text: object) -> Dict[str, Any]:
        raw = self._coerce(text)
        tokens = self.tokenize(raw)
        scripts = self._scripts_present(raw)
        if not tokens:
            return {
                "word_count": 0,
                "colloquial_score": 0.0,
                "transition_count": 0,
                "colloquialism_density": 0.0,
                "identified_colloquialisms": [],
                "scripts_present": scripts,
                "is_code_switching": False,
            }

        found = {token: self._markers[token] for token in tokens if token in self._markers}
        transitions = [token for token in tokens if token in self._TRANSITION_MARKERS]
        weighted = sum(found.values())
        density = round(weighted / len(tokens), 3)

        # Code-switching is true if we have multiple scripts present, OR
        # if we have high-confidence colloquial markers mixed with standard tokens.
        # We define mixed_lexicon as having at least one strong marker (slang) 
        # and standard ASCII tokens, preventing weak markers like "best" or "boss" 
        # from falsely triggering code-switching in plain English.
        has_strong_marker = any(token in self._STRONG_MARKERS for token in tokens)
        mixed_lexicon = has_strong_marker and any(token.isascii() and token not in self._markers for token in tokens)

        return {
            "word_count": len(tokens),
            "colloquial_score": round(weighted, 3),
            "transition_count": len(transitions),
            "colloquialism_density": density,
            "identified_colloquialisms": sorted(found),
            "scripts_present": scripts,
            "is_code_switching": len(scripts) > 1 or mixed_lexicon,
        }

    def suggest_voice_synthesizer_tuning(self, text: object) -> Dict[str, Any]:
        """Map analysis to documented voice profile defaults."""
        analysis = self.analyze_code_switching(text)
        density = analysis["colloquialism_density"]
        transitions = analysis["transition_count"]

        if density > 0.12:
            profile = {
                "profile": "conversational_colloquial",
                "stability": 0.55,
                "similarity_boost": 0.85,
                "style_exaggeration": 0.20,
                "use_speaker_boost": True,
                "recommended_voice_model": "eleven_multilingual_v2",
                "cadence_mode": "Conversational Colloquial (Manglish / mixed code)",
            }
        elif transitions >= 2 or len(analysis["scripts_present"]) > 1:
            profile = {
                "profile": "bilingual_transition",
                "stability": 0.70,
                "similarity_boost": 0.80,
                "style_exaggeration": 0.10,
                "use_speaker_boost": True,
                "recommended_voice_model": "eleven_multilingual_v2",
                "cadence_mode": "Corporate Formal (Malay-English bilingual)",
            }
        else:
            profile = {
                "profile": "standard_formal",
                "stability": 0.80,
                "similarity_boost": 0.75,
                "style_exaggeration": 0.0,
                "use_speaker_boost": False,
                "recommended_voice_model": "eleven_multilingual_v2",
                "cadence_mode": "Standard Formal Broadcast",
            }

        return {
            "colloquialism_density": density,
            "scripts_present": analysis["scripts_present"],
            "is_code_switching": analysis["is_code_switching"],
            "tuning_parameters": profile,
            "calibration_note": "Hand-tuned defaults; validate with listening tests before production use.",
        }
