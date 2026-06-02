import re
from typing import Dict, List, Tuple, Optional

class SovereignDataGuard:
    """
    SovereignDataGuard provides production-grade sanitization and redact filters
    for Malaysian-specific sensitive data to ensure absolute PDPA 2010 compliance
    before prompts are dispatched to public or third-party LLM APIs.
    """
    
    def __init__(self):
        # Malaysian NRIC / MyKad format: YYMMDD-SS-NNNN (e.g. 910314-10-5021)
        self.nric_pattern = re.compile(r'\b\d{6}-\d{2}-\d{4}\b')
        
        # Malaysian Mobile and Landline formats including country code (+60 or 60)
        # Matches: +6012-3456789, 0123456789, +60 11-1401 0362, 03-78901234, etc.
        self.phone_pattern = re.compile(
            r'\b(?:\+?60|0)(?:[1-9]\d{1,2}-?\d{7,8}|3-?\d{8})\b'
        )
        
        # Common Malaysian Address structures and postcodes (5 digits, e.g., 63000 Cyberjaya)
        self.postcode_pattern = re.compile(r'\b\d{5}\b')
        
        # Custom redaction placeholder
        self.placeholder_tpl = "[REDACTED_{label}]"

    def audit_text(self, text: str) -> Dict[str, int]:
        """
        Scans text and returns counts of sensitive entities identified.
        """
        return {
            "nric_mykad": len(self.nric_pattern.findall(text)),
            "malaysian_phones": len(self.phone_pattern.findall(text)),
            "postcodes": len(self.postcode_pattern.findall(text))
        }

    def redact(self, text: str, labels_to_redact: Optional[List[str]] = None) -> str:
        """
        Redacts NRICs, phone numbers, and postcodes with standardized placeholder tags.
        """
        if labels_to_redact is None:
            labels_to_redact = ["nric", "phone", "postcode"]
            
        sanitized = text
        
        if "nric" in labels_to_redact:
            sanitized = self.nric_pattern.sub(
                self.placeholder_tpl.format(label="NRIC_MYKAD"), sanitized
            )
            
        if "phone" in labels_to_redact:
            sanitized = self.phone_pattern.sub(
                self.placeholder_tpl.format(label="MALAYSIAN_PHONE"), sanitized
            )
            
        if "postcode" in labels_to_redact:
            sanitized = self.postcode_pattern.sub(
                self.placeholder_tpl.format(label="POSTCODE"), sanitized
            )
            
        return sanitized

    def validate_pdpa_compliance(self, text: str) -> Tuple[bool, List[str]]:
        """
        Checks if text is compliant with PDPA 2010. 
        Returns (is_compliant, list_of_violations).
        """
        violations = []
        counts = self.audit_text(text)
        
        if counts["nric_mykad"] > 0:
            violations.append(f"Contains {counts['nric_mykad']} unencrypted MyKad NRIC number(s).")
        if counts["malaysian_phones"] > 0:
            violations.append(f"Contains {counts['malaysian_phones']} unencrypted Malaysian telephone number(s).")
            
        return len(violations) == 0, violations
