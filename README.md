# Agentic Governance Workshop (Session 3)

This repo is a **build-along demo** for PMs to learn how to **deploy, govern, monitor, and scale** AI agents inside products.

You will build a simplified (but realistic) product:

**AI-powered Customer Support Triage**
- Reads incoming support tickets
- Routes them (category + priority)
- Drafts a response
- Applies **policy guardrails**
- Escalates risky cases to **Human-in-the-Loop (HITL)**

✅ Works in **mock mode** (no API key needed)  
✅ Runs in **GitHub Codespaces** (recommended for mixed Windows/Mac)  
✅ Supports **live mode** via OpenAI-compatible API (optional)

---

## Quick Start (Codespaces recommended)

1. Open this repo in **GitHub Codespaces**
2. In the terminal:

```bash
python -m pip install -r requirements.txt
cp -n .env.example .env || true
python run.py --mode mock --data data/tickets_sample.json
```

You should see:
- The routed category + priority
- A drafted response
- Policy decision (approved / blocked)
- A metrics summary

---

## Run Modes

### 1) Mock Mode (recommended for class)
No API keys. Deterministic outputs.

```bash
python run.py --mode mock --data data/tickets_sample.json
```

### 2) Live Mode (optional)
Uses `OPENAI_API_KEY` and `OPENAI_MODEL` from `.env`.

1. Copy `.env.example` to `.env` and fill your key.
2. Run:

```bash
python run.py --mode live --data data/tickets_sample.json
```

> Tip: If live mode fails, switch back to mock mode immediately.

---

## CrewAI Demo (Multi-Agent Orchestration in Action)

This session includes a **CrewAI resolver** that makes multi-agent coordination visible.
It is invoked only for **ambiguous / borderline** cases.

### Run the CrewAI resolver (recommended: drift dataset)

Mock mode (works without an API key; prints a deterministic agent-to-agent trace):

```bash
python crew_resolver.py --mode mock --data data/tickets_drifted.json --id T-2001
```

Live mode (requires `OPENAI_API_KEY`):

```bash
python crew_resolver.py --mode live --data data/tickets_drifted.json --id T-2001
```

What to look for:
- Router revises classification under a stricter lens
- Drafter rewrites with stronger constraints
- Policy re-evaluates
- Coordinator makes a final call + explains why

---

## Drift Demo

Run the same workflow with a drifted ticket distribution:

```bash
python run.py --mode mock --data data/tickets_drifted.json
```

Compare:
- escalation rate
- policy violation rate
- latency

---

## Where to edit during class

- **Product & scope:** `product_brief.md`
- **Governance rules:** `GOVERNANCE.md`
- **Eval philosophy:** `EVALS.md`
- **Policy rules (machine-readable):** `policies/policy_rules.yaml`
- **Prompts:** `prompts/*.md`

---

## Session 3 Files (PM artifacts)

- `PRD_INTENT.md` — governance-first intent PRD template (pre-build)
- `PRD_ADDENDUM.md` — post-observation learnings template
- `LIVE_TYPING_SCRIPT.md` — slide-by-slide build-along script
- `INSTRUCTOR_GUIDE.md` — run-of-show + checkpoints + fallbacks
- `STUDENT_SETUP.md` — exact student instructions (no prior knowledge)

---

## Troubleshooting

### Smoke test (10 seconds)
```bash
python scripts/smoke_test.py
```

### Codespaces blocked?
Use **observe mode** in class. You will still get value from:
- the product/gov decisions
- metrics interpretation
- scaling discussion

---

## License
MIT
