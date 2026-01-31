# Session 3 Run Sheet (One Page)

## One non-negotiable rule
If anything fails → **switch to mock mode or observe mode**. No laptop debugging.

---

## Pre-class (instructor)
1) In a fresh Codespace, verify the repo runs:

```bash
python -m pip install -r requirements.txt
cp -n .env.example .env || true
python scripts/smoke_test.py
python run.py --mode mock --data data/tickets_sample.json
python run.py --mode mock --data data/tickets_drifted.json
python crew_resolver.py --mode mock --data data/tickets_drifted.json --id T-2001
```

2) Optional live CrewAI (only if reliable):
- Add key to `.env` (OPENAI_API_KEY)
- Then run:

```bash
python crew_resolver.py --mode live --data data/tickets_drifted.json --id T-2001
```

---

## In-class (recommended sequence)

### A) Intent PRD (12–15 min)
- Open: `PRD_INTENT.md`
- Use Cursor to ask adversarial questions (see `LIVE_TYPING_SCRIPT.md`)
- Fill live: Problem, 3 non-goals, top risks, HITL philosophy

### B) Executable governance (6–8 min)
- Open: `GOVERNANCE.md` + `policies/policy_rules.yaml`
- Add one forbidden phrase (e.g., `"we will compensate"`)

### C) Smoke test (5–7 min)
```bash
python scripts/smoke_test.py
```

### D) Baseline run + telemetry (10–12 min)
```bash
python run.py --mode mock --data data/tickets_sample.json
```
- See: output for 1 ticket + `runs/<latest>/events.jsonl`

### E) Controls / thresholds (5–6 min)
```bash
python run.py --mode mock --data data/tickets_sample.json --limit 2 --hitl-threshold 0.50
```

### F) Drift run (10–12 min)
```bash
python run.py --mode mock --data data/tickets_drifted.json
```
- Think: which metric moved and what PM action follows?

### G) CrewAI resolver (10–15 min)
Mock (everyone can run):
```bash
python crew_resolver.py --mode mock --data data/tickets_drifted.json --id T-2001
```

Optional live (only if stable):
```bash
python crew_resolver.py --mode live --data data/tickets_drifted.json --id T-2001
```

### H) PRD addendum (5–7 min)
- Open: `PRD_ADDENDUM.md`
- Use Curso, VSCode, Codespace browser IDE  to propose: policy change, rollout change, rollback

---

## Close line
**Define → Bound → Observe → Escalate → Scale**
