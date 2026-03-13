from typing import Dict, Any
import json
from utils.io import read_text
from utils.llm import call_llm
from mocks.mock_llm import mock_policy_check
from policies.policy_checks import check_policy, must_escalate

class PolicyAgent:
    name = "policy"

    def __init__(self, mode: str, prompt_path: str, policy_rules: Dict[str, Any]):
        self.mode = mode
        self.prompt = read_text(prompt_path)
        self.rules = policy_rules

    def run(self, ticket: Dict[str, Any], route: Dict[str, Any], draft: str) -> Dict[str, Any]:
        ticket_text = ticket["message"]

        if self.mode == "mock":
            # deterministic + also apply YAML rules for teaching transparency
            base = mock_policy_check(ticket_text, draft)
            violations = check_policy(ticket_text, draft, self.rules)
            base["violations"].extend(violations)
            if violations:
                base["approved"] = False
                base["risk_score"] = max(base["risk_score"], 0.9)
                base["required_action"] = "hitl_required"
            if must_escalate(ticket_text, self.rules):
                base["risk_score"] = max(base["risk_score"], 0.75)
                base["required_action"] = "hitl_required"
            return base

        user = f"""Ticket:\n{ticket_text}\n\nRoute JSON:\n{json.dumps(route)}\n\nDraft Response:\n{draft}\n\nReturn policy JSON."""
        out = call_llm(self.prompt, user)
        try:
            return json.loads(out)
        except Exception:
            violations = check_policy(ticket_text, draft, self.rules)
            return {
                "approved": False if violations else True,
                "violations": violations or ["Failed to parse policy output JSON"],
                "risk_score": 0.8,
                "required_action": "hitl_required",
                "notes": "Fallback policy path used."
            }
