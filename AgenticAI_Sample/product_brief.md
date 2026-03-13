# Product Brief: AI Support Triage (Demo Product)

## Goal
Reduce time-to-first-response and prevent urgent tickets from being missed, while avoiding risky/incorrect commitments.

## Users
- Support agents (primary)
- Support managers (secondary)
- Customers (indirect)

## What the system does (in this demo)
1. Reads a support ticket
2. **Routes**: category + priority + confidence + explanation
3. **Drafts** a suggested response
4. Applies **policy guardrails**
5. If risk is high → **Human-in-the-Loop** required

## Non-goals (explicit)
- No autonomous refunds
- No legal/medical advice
- No account changes
- No sending emails to customers (we only draft)

## Main risks
- Wrong advice causes customer harm
- Promising refunds creates legal/financial exposure
- Missing urgent safety/security issues damages brand trust

## Human-in-the-Loop (HITL)
HITL required when:
- policy agent flags a violation
- risk score above threshold
- low confidence routing
