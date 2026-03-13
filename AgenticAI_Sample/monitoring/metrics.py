import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

def load_events(events_path: str) -> List[Dict[str, Any]]:
    p = Path(events_path)
    if not p.exists():
        return []
    events = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events

def compute_metrics(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    latencies = {}
    counts = {
        "tickets": 0,
        "handoffs": 0,
        "hitl_required": 0,
        "policy_violations": 0,
        "blocked": 0,
        "approved": 0,
        "crew_invocations": 0,
        "crew_rounds": 0,
    }

    # collect agent latency
    agent_start = {}  # (ticket_id, agent) -> ts
    for e in events:
        t = e.get("ticket_id")
        agent = e.get("agent")
        if e["type"] == "ticket_processed":
            counts["tickets"] += 1
        if e["type"] == "handoff":
            counts["handoffs"] += 1
        if e["type"] == "hitl_required":
            counts["hitl_required"] += 1
        if e["type"] == "policy_violation":
            counts["policy_violations"] += 1
        if e["type"] == "policy_decision":
            if e.get("approved") is True:
                counts["approved"] += 1
            else:
                counts["blocked"] += 1

        if e["type"] == "crew_invoked":
            counts["crew_invocations"] += 1
        if e["type"] == "crew_round_end":
            counts["crew_rounds"] += 1

        if e["type"] == "agent_start":
            agent_start[(t, agent)] = e["ts_ms"]
        if e["type"] == "agent_end":
            s = agent_start.get((t, agent))
            if s is not None:
                d = e["ts_ms"] - s
                latencies.setdefault(agent, []).append(d)

    avg_latency = {a: (sum(v) / len(v)) for a, v in latencies.items()} if latencies else {}

    # rates
    tickets = max(counts["tickets"], 1)
    counts["hitl_rate"] = round(counts["hitl_required"] / tickets, 3)
    counts["violation_rate"] = round(counts["policy_violations"] / tickets, 3)
    counts["avg_latency_ms"] = {k: int(v) for k, v in avg_latency.items()}
    return counts
