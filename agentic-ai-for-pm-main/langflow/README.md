# Langflow Pre-Built Flows — Session 1

## Two Flows Included

### 1. `Reflection_Pattern_NovaByte.json`
**Pattern:** Reflection (Agent self-critique and revision)

**Flow:**
```
[User Profile: Raj, Day 12]
  → [Drafter Agent: writes nudge email]
    → [Reviewer Agent: critiques against 7 criteria]
      → [Combine: merges draft + feedback]
        → [Reviser Agent: produces polished email]
          → [Output: final email]
```

**Exercise:** Students modify the Reviewer Agent's system prompt to change what it checks for, then re-run to see how output changes.

---

### 2. `ToolUse_Pattern_NovaByte.json`
**Pattern:** Tool Use (Agent fetches its own data)

**Flow:**
```
[User ID Input]
  → [Tool: Mixpanel Usage API (mock)]  ─┐
  → [Tool: Stripe Billing API (mock)]  ─┤
                                        ↓
                              [Combine Data Sources]
                                        ↓
                              [Analyzer Agent]
                                        ↓
                              [Recommendation Output]
```

**Exercise:** Students try different user IDs (TU-001 through TU-010) and modify the Analyzer Agent's weighting. The API Request nodes fetch real data from endpoints.

---

## How to Import into Langflow

### Option A: Langflow Cloud (DataStax Astra)
1. Go to your Langflow workspace
2. Click **"New Flow"** or the **"+"** button
3. Click **"Import"** (upload icon)
4. Select the `.json` file
5. The flow will appear with all nodes and connections

### Option B: Self-hosted Langflow
1. Open Langflow in your browser
2. Click **"Import"** from the sidebar or main menu
3. Upload the `.json` file
4. All nodes, edges, and prompts will be pre-configured

### After Import
1. **Add your OpenAI API key** to each OpenAI Model node (click the node → paste key in the API Key field)
2. **Run the flow** using the Play button
3. Check the output at the final node

---

## Mock API Setup (Tool Use Flow)

The Tool Use flow uses **API Request** nodes that call real endpoints to fetch usage and billing data. Three options are available:

### Option A: Create Your Own Beeceptor Mock API (Recommended)
Create your own mock API endpoints — it takes 5 minutes and is a useful PM skill:

1. Go to [beeceptor.com](https://beeceptor.com), enter a subdomain name (e.g., `your-name-novabyte`), click **Create Endpoint**
2. Click **Mocking Rules** → **Create New Rule**
3. Create a rule for `/usage_data` (GET, 200, paste contents of `sample_data/mock_api/usage_data.json`)
4. Create a rule for `/billing_data` (GET, 200, paste contents of `sample_data/mock_api/billing_data.json`)
5. Replace the URLs in the Langflow flow nodes with your Beeceptor URLs

These return data for all 10 trial users (TU-001 through TU-010). The Analyzer Agent extracts the relevant user by ID from the full JSON response.

### Option B: GitHub Raw URLs (Zero-Setup Fallback)
Static GitHub URLs that always work as a fallback:

| API | URL |
|-----|-----|
| **Usage Data** | `https://raw.githubusercontent.com/shameekc/agentic-ai-for-pm/main/sample_data/mock_api/usage_data.json` |
| **Billing Data** | `https://raw.githubusercontent.com/shameekc/agentic-ai-for-pm/main/sample_data/mock_api/billing_data.json` |

These return data for all 10 trial users. To use these, paste the URLs into the API Request nodes.

### Option C: Make.com Webhook APIs (Advanced)
Build two Make.com scenarios that accept a `user_id` and return only that user's data. See the **Instructor Runbook** for step-by-step Make.com build instructions.

Once built, paste your Make.com webhook URLs into the API Request nodes and switch the HTTP Method to **POST** with body: `{"user_id": "TU-004"}`.

### API Data Reference
Each API returns rich, realistic mock data:

**Usage Data** (mimics Mixpanel): login streaks, feature adoption rates, session duration trends, collaboration scores, onboarding completion, integration activity

**Billing Data** (mimics Stripe): pricing page visit dates, plan comparisons, cart abandonment events, discount code attempts, payment method status, estimated MRR

---

## Important Notes

- The Tool Use flow uses **API Request** nodes that call real endpoints (GitHub raw URLs by default, or Make.com webhooks)
- The flows use **gpt-4o-mini** by default — change the model name in each OpenAI node if needed
- If import has issues with your Langflow version, you can **recreate the flows manually** using the prompts below as reference — the key value is in the prompts themselves

---

## Fallback: Key Prompts for Manual Recreation

If the JSON import doesn't work perfectly with your Langflow version, here are the exact prompts to copy-paste when building manually:

### Drafter Agent (Reflection Flow)
```
You are a conversion specialist at NovaByte, a B2B SaaS project management platform.

Your job is to draft a personalized nudge email to convert a free trial user to a paid plan.

Rules:
- Be genuinely helpful, not salesy or pushy
- Reference the user's SPECIFIC usage patterns (projects, team members, integrations)
- Highlight value they would lose if they don't convert
- Offer something concrete: a best practices session, custom onboarding call, or advanced feature walkthrough
- Keep the email under 150 words
- Do NOT offer discounts, credits, or pricing promises
- Do NOT create false urgency
- Include a clear, low-pressure call to action
- Sign off as "The NovaByte Team"

Write ONLY the email. No preamble.
```

### Reviewer Agent (Reflection Flow) — THE ONE STUDENTS MODIFY
```
You are a Senior Product Manager reviewing a draft conversion nudge email.

Critique against these criteria:

1. PERSONALIZATION: Does it reference specific usage data? Generic emails fail.
2. TONE: Helpful and warm, or salesy/pushy?
3. UNAUTHORIZED PROMISES: Any discounts, credits, extended trials? Flag immediately.
4. FALSE URGENCY: Any manipulative language? Flag it.
5. CLARITY OF CTA: Clear, specific, low-pressure?
6. LENGTH: Under 150 words?
7. VALUE PROPOSITION: Communicates what they'd GAIN, not just what they'd lose?

For each: PASS or FAIL with specific feedback.
End with: APPROVE, REVISE (with changes), or REJECT (with reason).
```

### Analyzer Agent (Tool Use Flow)
```
You are a Trial Conversion Analyst at NovaByte.

You have data from multiple sources (usage analytics and billing signals).
Analyze ALL data and produce:

## CONVERSION ANALYSIS
**Intent Score:** [0-100]
**Intent Category:** [HIGH | MEDIUM | LOW | RISKY]
**Confidence:** [0-100%]

## KEY SIGNALS
- [3-5 most important signals with interpretation]

## RISK FACTORS
- [Any concerns]

## RECOMMENDED ACTION
**Primary Action:** [specific]
**Timing:** [IMMEDIATE | THIS_WEEK | CAN_WAIT]
**Channel:** [Email | Slack to Sales | In-app | Phone]

## REASONING
[2-3 sentences with specific data points]

## WHAT NOT TO DO
[1-2 things to avoid with this user]
```
