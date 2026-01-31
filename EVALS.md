# Evals & Quality Checks (PM-Friendly)

We evaluate **behavior**, not model benchmarks.

## What “good” looks like
- Correct category and priority most of the time
- Conservative language (no risky promises)
- Escalates when risk is high
- Stable behavior when ticket mix changes

## Practical checks (used in this repo)
1. **Policy violations**: forbidden phrases/commitments (refunds, legal advice, etc.)
2. **Escalation sanity**: security/payment disputes should escalate
3. **Latency**: routing + drafting + policy check should be fast enough for ops

## Drift indicators
- escalation rate changes sharply week-to-week
- policy violation rate increases
- confidence drops for common categories

## What PMs do with evals
- tighten policy rules
- adjust prompts/version (rollback)
- change rollout percent
- increase HITL thresholds
