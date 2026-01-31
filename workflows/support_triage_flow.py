from typing import Dict, Any, Optional
from agents.router_agent import RouterAgent
from agents.draft_agent import DraftAgent
from agents.policy_agent import PolicyAgent
from monitoring.telemetry import Telemetry
from utils.time import now_ms

def run_ticket(ticket: Dict[str, Any], router: RouterAgent, drafter: DraftAgent, policy: PolicyAgent,
               telemetry: Telemetry, hitl_threshold: float = 0.65) -> Dict[str, Any]:
    tid = ticket.get("ticket_id", "unknown")

    telemetry.emit("agent_start", {"ticket_id": tid, "agent": router.name})
    route = router.run(ticket)
    telemetry.emit("agent_end", {"ticket_id": tid, "agent": router.name, "output": route})

    telemetry.emit("handoff", {"ticket_id": tid, "from": "router", "to": "drafter"})

    telemetry.emit("agent_start", {"ticket_id": tid, "agent": drafter.name})
    draft = drafter.run(ticket, route)
    telemetry.emit("agent_end", {"ticket_id": tid, "agent": drafter.name})

    telemetry.emit("handoff", {"ticket_id": tid, "from": "drafter", "to": "policy"})

    telemetry.emit("agent_start", {"ticket_id": tid, "agent": policy.name})
    pol = policy.run(ticket, route, draft)
    telemetry.emit("agent_end", {"ticket_id": tid, "agent": policy.name, "output": pol})

    # policy violations
    for v in pol.get("violations", []) or []:
        telemetry.emit("policy_violation", {"ticket_id": tid, "agent": "policy", "violation": v})

    # HITL decision
    risk = float(pol.get("risk_score", 0.0) or 0.0)
    approved = bool(pol.get("approved", False))
    hitl_required = (not approved) or (risk >= hitl_threshold) or (pol.get("required_action") == "hitl_required")

    if hitl_required:
        telemetry.emit("hitl_required", {"ticket_id": tid, "risk_score": risk, "approved": approved})

    telemetry.emit("policy_decision", {"ticket_id": tid, "approved": approved, "risk_score": risk, "hitl_required": hitl_required})
    telemetry.emit("ticket_processed", {"ticket_id": tid})

    return {
        "ticket_id": tid,
        "route": route,
        "draft": draft,
        "policy": pol,
        "hitl_required": hitl_required
    }
