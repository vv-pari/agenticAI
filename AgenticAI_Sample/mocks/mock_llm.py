from typing import Dict, Any
import re

def mock_route(message: str) -> Dict[str, Any]:
    m = message.lower()
    # heuristic routing
    if any(k in m for k in ["hacked", "fraud", "account takeover", "login attempts", "stolen"]):
        return {"category":"account","priority":"P0","confidence":0.9,"rationale":"Security/account compromise signals detected."}
    if "chargeback" in m or "paid" in m and ("nothing arrived" in m or "didn't get" in m):
        return {"category":"billing","priority":"P1","confidence":0.8,"rationale":"Payment dispute / delivery mismatch."}
    if any(k in m for k in ["spoiled", "leaking", "bad", "rotten"]):
        return {"category":"quality","priority":"P1","confidence":0.8,"rationale":"Product quality issue reported."}
    if any(k in m for k in ["late", "delayed", "when will it arrive", "missing delivery", "not arrived"]):
        return {"category":"delivery","priority":"P1","confidence":0.7,"rationale":"Delivery delay or missing delivery."}
    if any(k in m for k in ["crash", "error", "bug", "checkout"]):
        return {"category":"technical","priority":"P2","confidence":0.7,"rationale":"App/tech issue reported."}
    return {"category":"general","priority":"P2","confidence":0.6,"rationale":"General inquiry."}

def mock_draft(message: str, category: str, priority: str) -> str:
    base = "Thanks for reaching out — I’m sorry for the trouble. "
    m = message.lower()
    if category == "account":
        return (base +
                "For your security, we’ll escalate this to our support team right away. "
                "Please confirm whether you still have access to your account and whether you noticed any unauthorized changes. "
                "Do not share any passwords or OTPs.")
    if category == "billing":
        return (base +
                "We’ll look into the payment and delivery details and get back to you quickly. "
                "Could you share your order ID and the date/time of purchase? "
                "If you’re seeing any specific error or status message, please paste it here. "
                "We’ll escalate this for priority review.")
    if category == "quality":
        return (base +
                "That sounds frustrating. Could you share a quick photo of the items and the label/box if available? "
                "Also confirm the delivery date/time so we can investigate. We’ll escalate this for quick resolution.")
    if category == "delivery":
        return (base +
                "Could you share your order ID and delivery location/slot? "
                "We’ll check the latest status and update you. If this is time-sensitive, mention it and we’ll prioritize.")
    if category == "technical":
        return (base +
                "Sorry about the crash. Could you share your device model + OS version and what step you were on when it crashed? "
                "A screenshot (if available) will help. We’ll escalate to the technical team.")
    return (base +
            "Could you share a bit more detail about what you’re trying to do and what you expected to happen? "
            "We’ll take it from there.")

def mock_policy_check(ticket: str, draft: str) -> Dict[str, Any]:
    text = draft.lower()
    violations = []
    forbidden = [
        "we will refund",
        "refund will be processed",
        "share your password",
        "share your otp",
        "send your cvv",
        "legal advice",
        "guarantee",
    ]
    for f in forbidden:
        if f in text:
            violations.append(f"Contains forbidden phrase: '{f}'")
    risk = 0.2
    if any(k in ticket.lower() for k in ["hacked", "fraud", "account takeover", "chargeback", "unsafe", "injury"]):
        risk = 0.75
    if violations:
        risk = max(risk, 0.9)
    approved = (len(violations) == 0)
    required_action = "auto_ok" if (approved and risk < 0.65) else "hitl_required"
    return {
        "approved": approved,
        "violations": violations,
        "risk_score": float(risk),
        "required_action": required_action,
        "notes": "Strict mode: escalate if risk is high or any violation exists."
    }
