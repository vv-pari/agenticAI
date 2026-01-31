from typing import Dict, Any, List
import re

def check_policy(ticket_text: str, draft_text: str, rules: Dict[str, Any]) -> List[str]:
    violations: List[str] = []
    low = draft_text.lower()

    for phrase in rules.get("forbidden_phrases", []):
        if phrase.lower() in low:
            violations.append(f"Forbidden phrase: {phrase}")

    # PII request patterns
    for pat in rules.get("pii_request_patterns", []):
        if pat.lower() in low:
            violations.append(f"PII request detected: {pat}")

    return violations

def must_escalate(ticket_text: str, rules: Dict[str, Any]) -> bool:
    low = ticket_text.lower()
    for kw in rules.get("must_escalate_keywords", []):
        if kw.lower() in low:
            return True
    return False
