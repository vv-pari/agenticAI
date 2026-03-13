"""CrewAI Resolver Demo (Session 3)

This script demonstrates **multi-agent orchestration** visibly.

Concept:
- We first run the normal pipeline (router → drafter → policy).
- If the case is borderline (or forced), we invoke a **CrewAI resolver**:
  - Router re-checks classification under a stricter lens
  - Drafter rewrites with stricter constraints
  - Policy re-evaluates
  - Coordinator makes the final decision and explains tradeoffs

Modes:
- mock: deterministic trace (no API key)
- live: uses CrewAI with OPENAI_API_KEY
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from dotenv import load_dotenv
from rich import print

from agents.router_agent import RouterAgent
from agents.draft_agent import DraftAgent
from agents.policy_agent import PolicyAgent
from monitoring.telemetry import Telemetry
from monitoring.metrics import load_events, compute_metrics
from policies.policy_loader import load_policy_rules
from workflows.support_triage_flow import run_ticket
from utils.io import read_json, ensure_dir


def build_run_dir(prefix: str = "crew") -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir = f"runs/{prefix}_{ts}"
    ensure_dir(run_dir)
    return run_dir


def find_ticket(tickets: list[dict[str, Any]], ticket_id: str) -> dict[str, Any]:
    for t in tickets:
        if t.get("ticket_id") == ticket_id:
            return t
    raise SystemExit(f"Ticket id not found: {ticket_id}")


def is_borderline(policy: Dict[str, Any]) -> bool:
    # Borderline = where pipelines feel brittle and coordination pays off
    risk = float(policy.get("risk_score", 0.0) or 0.0)
    return 0.55 <= risk <= 0.75


def _safe_json_load(s: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(s)
    except Exception:
        return None


def mock_resolver_trace(ticket: Dict[str, Any], baseline: Dict[str, Any], telemetry: Telemetry) -> Dict[str, Any]:
    """Deterministic, classroom-safe "crew" trace."""
    tid = ticket["ticket_id"]
    msg = ticket["message"]

    telemetry.emit("crew_invoked", {"ticket_id": tid, "mode": "mock"})

    print("[bold]\n=== CrewAI Resolver (MOCK) ===[/bold]")
    print("[dim]Coordinator:[/dim] Borderline case detected. Initiating agent reassessment.")

    # Step 1: Router revises
    telemetry.emit("crew_step", {"ticket_id": tid, "step": "router_recheck"})
    revised_route = dict(baseline["route"])
    revised_route["priority"] = "P0" if revised_route.get("priority") in ("P1", "P2") else revised_route.get("priority")
    revised_route["confidence"] = 0.55
    revised_route["rationale"] = "Rechecked under worst-case impact lens; prioritizing safety and financial risk."

    print("\n[cyan][Router][/cyan] Re-evaluating with worst-case lens…")
    print("→", revised_route)

    # Step 2: Drafter revises
    telemetry.emit("crew_step", {"ticket_id": tid, "step": "drafter_rewrite"})
    revised_draft = (
        "Thanks for reaching out — I’m sorry for the issue. "
        "I understand this is urgent. I’m escalating this to our support team for priority review right away. "
        "To help us investigate quickly, could you confirm your order ID and the date/time of purchase? "
        "If you’re seeing any status message, please paste it here. "
        "We’ll update you as soon as we have more information."
    )
    print("\n[cyan][Drafter][/cyan] Revised draft (no promises, explicit escalation):")
    print(revised_draft)

    # Step 3: Policy re-check
    telemetry.emit("crew_step", {"ticket_id": tid, "step": "policy_recheck"})
    revised_policy = dict(baseline["policy"])
    revised_policy["approved"] = True
    revised_policy["violations"] = []
    revised_policy["risk_score"] = 0.64
    revised_policy["required_action"] = "hitl_required"
    revised_policy["notes"] = "No forbidden commitments detected; still high-risk category, keep HITL."

    print("\n[cyan][Policy][/cyan] Re-evaluating revised draft…")
    print("→", revised_policy)

    # Step 4: Coordinator requests an even stricter rewrite (to show back-and-forth)
    telemetry.emit("crew_step", {"ticket_id": tid, "step": "coordinator_request_stricter_rewrite"})
    print("\n[bold][Coordinator][/bold] This is still borderline. Requesting stricter rewrite to reduce operational risk.")

    telemetry.emit("crew_step", {"ticket_id": tid, "step": "drafter_rewrite_strict"})
    revised_draft_2 = (
        "Thanks for flagging this — I understand the urgency. "
        "I’m escalating this to a human support agent for priority review. "
        "Please confirm your order ID and purchase timestamp so we can investigate. "
        "We’ll respond as soon as we have an update."
    )
    print("\n[cyan][Drafter][/cyan] Strict rewrite (minimal commitments):")
    print(revised_draft_2)

    telemetry.emit("crew_step", {"ticket_id": tid, "step": "policy_recheck_strict"})
    revised_policy_2 = dict(revised_policy)
    revised_policy_2["risk_score"] = 0.61
    revised_policy_2["notes"] = "Still a financially sensitive case; keep HITL, but content is safe for assisted mode."
    print("\n[cyan][Policy][/cyan] Re-evaluating strict rewrite…")
    print("→", revised_policy_2)

    # Step 5: Coordinator decision
    telemetry.emit("crew_step", {"ticket_id": tid, "step": "coordinator_decision"})
    decision = {
        "final_route": revised_route,
        "final_draft": revised_draft_2,
        "final_policy": revised_policy_2,
        "hitl_required": True,
        "rationale": "Even with safer language, chargeback/urgency creates financial and trust risk. Keep human approval.",
        "trace": [
            "Coordinator invoked due to ambiguity",
            "Router revised classification under stricter lens",
            "Drafter rewrote response with constraints + escalation",
            "Policy approved content but kept HITL due to residual risk",
            "Coordinator requested stricter rewrite; policy re-approved",
        ],
    }

    print("\n[bold][Coordinator][/bold] Decision:")
    print("→ HITL required")
    print("→", decision["rationale"])

    print("\n[dim]Trace:[/dim]")
    for line in decision["trace"]:
        print("-", line)

    telemetry.emit("crew_round_end", {"ticket_id": tid, "hitl_required": True, "risk_score": decision["final_policy"]["risk_score"]})
    return decision


def run_crewai_round(
    ticket: Dict[str, Any],
    baseline: Dict[str, Any],
    telemetry: Telemetry,
    round_name: str,
    strictness: str = "standard",
) -> Dict[str, Any]:
    """Run one CrewAI orchestration round and return parsed outputs.

    We keep the crew small and focused: Router -> Drafter -> Policy -> Coordinator.
    """

    try:
        from crewai import Agent, Task, Crew, Process
    except Exception as e:
        raise SystemExit(
            "CrewAI is not installed or failed to import. Run `pip install -r requirements.txt` "
            "and try again.\n\nImport error: " + str(e)
        )

    tid = ticket["ticket_id"]
    msg = ticket["message"]

    telemetry.emit("crew_step", {"ticket_id": tid, "step": f"{round_name}_start"})

    router = Agent(
        role="Router Agent (Recheck)",
        goal="Minimize misclassification; when uncertain, prefer safer priority.",
        backstory="You triage support tickets. You are conservative under ambiguity.",
        verbose=True,
        allow_delegation=False,
    )
    drafter = Agent(
        role="Drafting Agent (Revise)",
        goal="Draft a helpful response with minimal risk: no promises, no sensitive data requests.",
        backstory="You write customer support drafts that are safe, polite, and escalation-friendly.",
        verbose=True,
        allow_delegation=False,
    )
    policy = Agent(
        role="Policy Agent (Re-evaluate)",
        goal="Detect risky language and enforce governance constraints. Prefer HITL if uncertain.",
        backstory="You are a strict compliance reviewer for support communications.",
        verbose=True,
        allow_delegation=False,
    )
    coordinator = Agent(
        role="Coordinator (Decision Owner)",
        goal="Resolve disagreement safely while minimizing human workload. Decide HITL vs assisted send.",
        backstory="You are accountable for incidents and user trust. You balance safety and ops load.",
        verbose=True,
        allow_delegation=False,
    )

    # Strictness knobs (used to show "back-and-forth" without complicating code)
    extra_constraints = ""
    if strictness == "high":
        extra_constraints = (
            "\n\nAdditional constraints (HIGH strictness): "
            "- Do not imply any timeline. "
            "- Do not imply refunds/credits. "
            "- Always include escalation path to a human agent."
        )

    route_task = Task(
        description=(
            f"Ticket:\n{msg}\n\n"
            f"Previous routing JSON:\n{json.dumps(baseline['route'], ensure_ascii=False)}\n\n"
            "Re-classify and re-prioritize under a *worst-case customer impact* lens. "
            "Return JSON ONLY with keys: category, priority, confidence, rationale."
        ),
        expected_output="JSON only: {category, priority, confidence, rationale}",
        agent=router,
    )

    draft_task = Task(
        description=(
            f"Ticket:\n{msg}\n\n"
            "You will receive revised routing from the prior task. "
            "Rewrite the response to minimize risk and avoid promises. "
            "Ask 1–2 clarifying questions if needed. "
            "Return plain text only." + extra_constraints
        ),
        expected_output="Plain text draft response",
        agent=drafter,
        context=[route_task],
    )

    policy_task = Task(
        description=(
            f"Ticket:\n{msg}\n\n"
            "Review the revised draft response for policy/gov risk. "
            "Return JSON ONLY with keys: approved (bool), violations (list of strings), risk_score (0..1), required_action (auto_ok|hitl_required|block_and_rewrite), notes."
        ),
        expected_output="JSON only policy decision",
        agent=policy,
        context=[route_task, draft_task],
    )

    coord_task = Task(
        description=(
            "You are the decision owner. Using prior task outputs, decide whether HITL is required. "
            "Return JSON ONLY with keys: hitl_required (bool), rationale (string), next_action (one of: keep_hitl|assisted_ok|rewrite_again), trace (list of 3-6 short bullet strings)."
        ),
        expected_output="JSON only coordinator decision",
        agent=coordinator,
        context=[route_task, draft_task, policy_task],
    )

    crew = Crew(
        agents=[router, drafter, policy, coordinator],
        tasks=[route_task, draft_task, policy_task, coord_task],
        process=Process.sequential,
        verbose=True,
    )

    telemetry.emit("crew_invoked", {"ticket_id": tid, "mode": "live", "round": round_name, "strictness": strictness})
    _ = crew.kickoff()

    def task_text(task: Task) -> str:
        out = getattr(task, "output", None)
        if out is None:
            return ""
        # CrewAI output objects often expose .raw
        raw = getattr(out, "raw", None)
        return raw if isinstance(raw, str) else str(out)

    route_text = task_text(route_task)
    draft_text = task_text(draft_task)
    policy_text = task_text(policy_task)
    coord_text = task_text(coord_task)

    route_json = _safe_json_load(route_text) or baseline["route"]
    policy_json = _safe_json_load(policy_text) or baseline["policy"]
    coord_json = _safe_json_load(coord_text) or {
        "hitl_required": True,
        "rationale": "Coordinator output parse failed; defaulting to HITL.",
        "next_action": "keep_hitl",
        "trace": ["Parse failure fallback"],
    }

    telemetry.emit(
        "crew_round_end",
        {
            "ticket_id": tid,
            "round": round_name,
            "hitl_required": bool(coord_json.get("hitl_required", True)),
            "risk_score": float(policy_json.get("risk_score", 1.0) or 1.0),
        },
    )

    return {
        "route": route_json,
        "draft": draft_text.strip(),
        "policy": policy_json,
        "coord": coord_json,
    }


def main() -> None:
    load_dotenv()

    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["mock", "live"], default=os.getenv("LLM_MODE", "mock"))
    ap.add_argument("--data", default="data/tickets_drifted.json")
    ap.add_argument("--id", required=True, help="Ticket id to run (e.g., T-2001)")
    ap.add_argument("--force", action="store_true", help="Force CrewAI resolver even if not borderline")
    ap.add_argument("--hitl-threshold", type=float, default=0.65)
    args = ap.parse_args()

    tickets = read_json(args.data)
    ticket = find_ticket(tickets, args.id)

    run_dir = build_run_dir()
    telemetry = Telemetry(run_dir=run_dir)

    policy_rules = load_policy_rules("policies/policy_rules.yaml")
    router = RouterAgent(mode=args.mode if args.mode == "mock" else "live", prompt_path="prompts/router_v1.md")
    drafter = DraftAgent(mode=args.mode if args.mode == "mock" else "live", prompt_path="prompts/drafter_v1.md")
    policy_agent = PolicyAgent(
        mode=args.mode if args.mode == "mock" else "live",
        prompt_path="prompts/policy_v1.md",
        policy_rules=policy_rules,
    )

    print(f"[bold]Crew resolver mode:[/bold] {args.mode}  |  [bold]Ticket:[/bold] {ticket['ticket_id']}  |  [bold]Run dir:[/bold] {run_dir}")
    baseline = run_ticket(ticket, router, drafter, policy_agent, telemetry, hitl_threshold=args.hitl_threshold)

    print("\n[bold]=== Baseline pipeline result ===[/bold]")
    print(f"Route → category={baseline['route'].get('category')} priority={baseline['route'].get('priority')} conf={baseline['route'].get('confidence')}")
    print(f"Policy → risk={baseline['policy'].get('risk_score')} approved={baseline['policy'].get('approved')} required_action={baseline['policy'].get('required_action')}")
    print(f"HITL required → {baseline['hitl_required']}")

    borderline = is_borderline(baseline["policy"])
    if not borderline and not args.force:
        print("\n[dim]Not a borderline case. Use --force to run CrewAI anyway.[/dim]")
        events = load_events(f"{run_dir}/events.jsonl")
        metrics = compute_metrics(events)
        print("\n[bold]Metrics Summary[/bold]")
        for k, v in metrics.items():
            print(f"- {k}: {v}")
        return

    # Resolver section
    if args.mode == "mock":
        decision = mock_resolver_trace(ticket, baseline, telemetry)
        # Show the "final" snapshot (what a product would store)
        print("\n[bold]Final snapshot (mock):[/bold]")
        print(json.dumps({"ticket_id": ticket["ticket_id"], **decision}, indent=2))
    else:
        print("[bold]\n=== CrewAI Resolver (LIVE) ===[/bold]")
        print("[dim]If this fails, run --mode mock.[/dim]")

        # Round 1: standard
        r1 = run_crewai_round(ticket, baseline, telemetry, round_name="round1", strictness="standard")
        print("\n[bold]--- Round 1 outputs (parsed) ---[/bold]")
        print("[cyan]Router revised:[/cyan]", r1["route"])
        print("[cyan]Drafter revised:[/cyan]", (r1["draft"] or "")[:240], "...")
        print("[cyan]Policy recheck:[/cyan]", r1["policy"])
        print("[cyan]Coordinator:[/cyan]", r1["coord"])

        next_action = (r1.get("coord") or {}).get("next_action", "keep_hitl")
        # Round 2: show back-and-forth (only if coordinator wants another rewrite or risk remains high)
        risk = float((r1.get("policy") or {}).get("risk_score", 1.0) or 1.0)
        if next_action == "rewrite_again" or risk >= args.hitl_threshold:
            print("\n[bold]Coordinator requested stricter rewrite → running Round 2[/bold]")
            r2_baseline = {
                "route": r1["route"],
                "draft": r1["draft"],
                "policy": r1["policy"],
            }
            r2 = run_crewai_round(ticket, r2_baseline, telemetry, round_name="round2", strictness="high")
            print("\n[bold]--- Round 2 outputs (parsed) ---[/bold]")
            print("[cyan]Policy recheck:[/cyan]", r2["policy"])
            print("[cyan]Coordinator:[/cyan]", r2["coord"])

    # Metrics
    events = load_events(f"{run_dir}/events.jsonl")
    metrics = compute_metrics(events)
    print("\n[bold]=== Metrics Summary ===[/bold]")
    for k, v in metrics.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
