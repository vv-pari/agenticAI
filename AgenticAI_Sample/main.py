import argparse
import os
from datetime import datetime
from pathlib import Path
from rich import print

from utils.io import read_json, ensure_dir
from monitoring.telemetry import Telemetry
from monitoring.metrics import load_events, compute_metrics
from policies.policy_loader import load_policy_rules
from agents.router_agent import RouterAgent
from agents.draft_agent import DraftAgent
from agents.policy_agent import PolicyAgent
from workflows.support_triage_flow import run_ticket

def build_run_dir() -> str:
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir = f"runs/{ts}"
    ensure_dir(run_dir)
    return run_dir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["mock","live"], default=os.getenv("LLM_MODE","mock"))
    ap.add_argument("--data", default="data/tickets_sample.json")
    ap.add_argument("--limit", type=int, default=0, help="Limit number of tickets (0 = all)")
    ap.add_argument("--hitl-threshold", type=float, default=0.65)
    args = ap.parse_args()

    tickets = read_json(args.data)
    if args.limit and args.limit > 0:
        tickets = tickets[:args.limit]

    run_dir = build_run_dir()
    telemetry = Telemetry(run_dir=run_dir)

    policy_rules = load_policy_rules("policies/policy_rules.yaml")

    router = RouterAgent(mode=args.mode, prompt_path="prompts/router_v1.md")
    drafter = DraftAgent(mode=args.mode, prompt_path="prompts/drafter_v1.md")
    policy = PolicyAgent(mode=args.mode, prompt_path="prompts/policy_v1.md", policy_rules=policy_rules)

    print(f"[bold]Mode:[/bold] {args.mode}  |  [bold]Tickets:[/bold] {len(tickets)}  |  [bold]Run dir:[/bold] {run_dir}")
    print("")

    results = []
    for t in tickets:
        res = run_ticket(t, router, drafter, policy, telemetry, hitl_threshold=args.hitl_threshold)
        results.append(res)

        print(f"[cyan]Ticket[/cyan] {res['ticket_id']} → category={res['route'].get('category')} priority={res['route'].get('priority')} conf={res['route'].get('confidence')}")
        if res["hitl_required"]:
            print("  [yellow]HITL REQUIRED[/yellow]  risk=", res['policy'].get('risk_score'), " approved=", res['policy'].get('approved'))
        else:
            print("  [green]AUTO OK[/green]  risk=", res['policy'].get('risk_score'))
        if res['policy'].get('violations'):
            print("  [red]Violations:[/red]", res['policy']['violations'])
        print("  Draft (first 160 chars):", (res['draft'] or '')[:160].replace('\n',' '), "...")
        print("")

    events = load_events(f"{run_dir}/events.jsonl")
    metrics = compute_metrics(events)

    print("[bold]=== Metrics Summary ===[/bold]")
    for k, v in metrics.items():
        print(f"- {k}: {v}")

if __name__ == "__main__":
    main()
