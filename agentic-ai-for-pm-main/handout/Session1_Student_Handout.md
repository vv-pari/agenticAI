# Session 1 Student Handout — Agent-driven Automation in Products

**Institute of Product Leadership**
**Course:** Agent-driven Automation in Products
**Session 1:** Foundations of Agentic AI and Agent Design Patterns

---

## Session Agenda

| Block | Topic | Duration |
|-------|-------|----------|
| 1 | Google Antigravity PM workflows demo | 25 min |
| 2 | PPT Walkthrough: Agentic AI Concepts & Foundations | 60 min |
| 3 | Make.com build-along — Rule-Based → AI-Powered automation | 70 min |
| 4 | Wrap-up + Assignment for Session 2 | 15 min |

---

## 1. Eight Agent Design Patterns Cheat Sheet

| # | Pattern | Definition | When to Use | Real-World Analogy |
|---|---------|-----------|-------------|-------------------|
| 1 | **Pipeline / Prompt Chaining** | Sequential chain where each step's output feeds the next step's input. | When a task breaks into ordered stages (e.g., extract, score, act). | Assembly line — each station adds value before passing the part forward. |
| 2 | **Routing** | A decision node directs input to one of several downstream paths based on conditions. | When different inputs require different handling (e.g., intent-based triage). | Airport immigration — separate lanes for citizens, residents, and visitors. |
| 3 | **Parallelization** | Multiple sub-tasks execute simultaneously, then results are aggregated. | When independent analyses can run at the same time to save latency. | A team of reviewers each grading a different section of a proposal at the same time. |
| 4 | **Reflection** | The agent critiques its own output and iterates to improve it before finalizing. | When output quality matters and you can afford an extra LLM call (writing, code, analysis). | An author writing a draft, then re-reading it as an editor before submitting. |
| 5 | **Tool Use** | The agent calls external tools (APIs, databases, calculators) to get information it cannot generate from memory. | When the task requires real-time data, computation, or actions in external systems. | A chef who checks a thermometer rather than guessing if the oven is hot enough. |
| 6 | **MCP (Model Context Protocol)** | A standardized protocol that lets agents discover and invoke tools dynamically via a universal interface. | When you want plug-and-play tool integration without hard-coding each API. | USB-C — one standard port that works with any compatible device. |
| 7 | **Planning** | The agent decomposes a complex goal into a sequence of sub-goals before executing. | When the task is open-ended and requires a multi-step strategy (e.g., research projects). | A project manager creating a work breakdown structure before assigning tasks. |
| 8 | **Multi-Agent Collaboration** | Multiple specialized agents work together, each handling a distinct role, coordinated by an orchestrator. | When no single prompt/agent can handle the full scope and specialization improves quality. | A cross-functional product squad — PM, designer, and engineer each contribute expertise. |

---

## 2. Key Concepts Quick Reference

### Agentic AI vs Generative AI vs Predictive AI

| Dimension | Predictive AI | Generative AI | Agentic AI |
|-----------|--------------|---------------|------------|
| **Core task** | Classify or forecast from historical data | Generate new content (text, image, code) | Autonomously pursue goals via reasoning + action |
| **Interaction** | Input in, prediction out (one-shot) | Prompt in, content out (one-shot or conversational) | Goal in, multi-step execution with tool calls |
| **Autonomy** | None — deterministic output | Low — follows the prompt | High — decides what to do next |
| **Memory** | Training data only | Context window | Context window + external memory / state |
| **Examples** | Churn prediction, fraud detection | ChatGPT drafting an email | An agent that researches competitors, drafts a report, and emails it to stakeholders |

### What Makes an Agent "Agentic"

An AI system is agentic when it exhibits these four capabilities:

- **Autonomy** — Can decide what step to take next without human instruction at each step.
- **Tool Use** — Can call external systems (APIs, databases, browsers) to gather info or take action.
- **Memory** — Can retain and reference information across steps or sessions.
- **Planning** — Can decompose a goal into sub-tasks and sequence them.

---

## 3. Make.com Exercise Instructions

> **BUSINESS PROBLEM:** NovaByte gets 3,200 trial signups per month but sends everyone the same generic drip emails. The sales team manually reviews a spreadsheet once a week and reaches out to ~20 users. How would you automatically classify each user's conversion intent and route them to the right action?

### Before You Start: Setup

1. **Make.com account:** Go to [make.com](https://www.make.com/) and sign up for a free account (if you haven't already). The free tier gives you 1,000 operations per month — more than enough.
2. **Google Sheet:** Click the link shared in class chat, then click **File → Make a copy** to get your own copy of the NovaByte Trial Users data.
3. **OpenAI API key:** Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys), sign in (or create an account), and create a new API key. Copy it somewhere safe — you'll need it later.

---

### Exercise 1: Rule-Based Flow — Google Sheets + Gmail

**Goal:** Build a simple automation that reads trial users from a Google Sheet and routes them using IF-THEN rules: high-intent users get an email, low-intent users get logged.

**What you'll learn:** The **Routing** pattern — and its limitations when implemented with hard-coded rules.

#### Step-by-Step Instructions

**Step 1: Create a new Scenario**
1. Log into Make.com
2. Click **"Create a new scenario"** (top right, or the big + button)
3. You'll see a blank canvas with one empty circle (a +). This is your starting point.

**Step 2: Add Google Sheets — Read Your Data**
1. Click the **+ circle** on the canvas
2. In the search box, type **Google Sheets** and click on it
3. Select **"Search Rows"**
4. Click **"Add"** next to Connection → sign in with your Google account
5. **Spreadsheet:** Find and select your copy of "NovaByte Trial Users"
6. **Sheet:** Select the first tab (Sheet1 or the tab with trial user data)
7. **Filter:** Click "Add a filter condition"
   - Column: **last_login_days_ago**
   - Condition: **Less than or equal to**
   - Value: **7**
8. Click **OK**

**Step 3: Test it**
1. Click the **Run once** button (▶ at bottom left)
2. After it runs, click the **bubble/number** that appears on the module
3. You should see trial user data — names, companies, logins, etc.

**Step 4: Add a Router**
1. Hover over the **right edge** of the Google Sheets module — a small semicircle appears
2. Click and drag to the right to create a new connection
3. In the search box, type **Router** and select **Flow Control → Router**

**Step 5: Path 1 — High Intent → Send an Email**
1. From the Router, a path already exists. Click the **+ at the end** of that path
2. Search for **Gmail** → select **Send an Email**
3. Click **Add** to connect your Gmail account (sign in and grant permissions)
4. **Before configuring the email**, click on the **line between the Router and Gmail**
5. A filter panel opens. Set:
   - **Label:** `High Intent`
   - **Condition 1:** Select **logins** (from Google Sheets dropdown) → **Greater than** → `10`
   - Click **AND** to add another condition
   - **Condition 2:** Select **team_members_invited** → **Greater than** → `3`
   - Click **OK**
6. Now click the **Gmail module** to configure it:
   - **To:** Your own email address (for testing)
   - **Subject:** Type `[HIGH INTENT] ` then select **name** from the dropdown, then type ` from ` then select **company**
   - **Content:** Type a template and insert variables from the dropdown:
     ```
     Hi Sales Team,

     This trial user looks ready to convert:
     Name: {name}
     Company: {company} ({company_size} employees)
     Role: {role}
     Logins: {logins}
     Team Invites: {team_members_invited}
     Trial Day: {trial_day} of 14

     Recommended: Send a personalized conversion email.
     ```
     *(Replace each {field} by clicking inside the text and selecting the variable from the left panel)*
   - Click **OK**

**Step 6: Path 2 — Low Intent → Log to Sheet**
1. Hover on the Router — click the **small + button** that appears to add another path
2. Search for **Google Sheets** → select **Add a Row**
3. Set the **filter** on the connecting line:
   - **Label:** `Low Intent`
   - **Condition:** **logins** → **Less than or equal to** → `3`
   - Click **OK**
4. Configure the Google Sheets module:
   - First, go to your Google Sheet and **add a new tab** (click the + at the bottom). Name it **Low Intent Log**. Add headers in row 1: `id`, `name`, `company`, `logins`, `last_login_days_ago`
   - Back in Make.com, select your spreadsheet, select the "Low Intent Log" tab
   - Map each column to the matching field from the Google Sheets Search Rows output
   - Click **OK**

**Step 7: Save and Test**
1. Click the **floppy disk icon** (💾) at the bottom to save
2. Click **Run once** (▶)
3. Check: Which users went to Gmail? Which went to the log? Did any fall through both filters?

---

### The Problem with Rules — Class Discussion

After building the rule-based flow, we'll discuss why it breaks down:

| Problem | Example |
|---------|---------|
| **Misses context** | Sarah Chen (VP, 800-person healthcare company, 2 logins) → rules say "Low Intent" but she's an enterprise prospect asking about HIPAA compliance |
| **Arbitrary thresholds** | Why 10 logins? Why not 8 or 12? Every threshold creates a cliff edge |
| **Can't combine signals** | Raj Patel has 14 logins + 8 invites + 3 pricing visits + tried a discount code. Rules can't weigh these together with nuance |
| **No personalization** | The email is a generic template — it can't mention Sarah's HIPAA question or Raj's discount code attempt |

---

### Exercise 2: AI-Powered Flow — Replace Rules with OpenAI

**Goal:** Build the same flow, but replace IF-THEN rules with an AI that analyzes each user holistically and classifies them — then routes based on the AI's classification.

**What you'll learn:** The **Pipeline** pattern (data → AI processing → structured output) combined with the **Routing** pattern.

#### Step-by-Step Instructions

**Step 1: Create a new Scenario**
1. Go back to your Make.com dashboard (click the Make logo at top left)
2. Click **"Create a new scenario"**
3. Add **Google Sheets > Search Rows** — same configuration as Exercise 1 (same spreadsheet, same filter)

**Step 2: Add OpenAI**
1. Click the semicircle on the right of the Google Sheets module → drag to create a connection
2. Search for **OpenAI** (or **ChatGPT**) and click it
3. Select **"Create a Chat Completion"**
4. Click **"Add"** to create a connection → paste your OpenAI API key → click **Save**
5. Configure:
   - **Model:** Select **gpt-4o-mini**
   - **Messages:** Click **"Add item"**
     - **Role:** System
     - **Message Content:** Copy and paste this entire prompt:

```
You are a SaaS trial conversion analyst for NovaByte, a project management tool.
Analyze this trial user's data and classify their conversion intent.

Consider ALL signals holistically:
- Engagement: logins, projects, team invites, features used, session duration
- Buying signals: pricing page visits, payment method, discount codes
- Risk signals: days since last login, support tickets
- Context: company size, industry, role (a VP at an 800-person company is different from a solo freelancer, even with similar usage numbers)

Respond in this exact JSON format and nothing else (no markdown, no code blocks, just raw JSON):
{
  "intent_category": "HIGH",
  "intent_score": 85,
  "reasoning": "2-3 sentences explaining your analysis",
  "recommended_action": "specific personalized action to take",
  "email_draft": "if HIGH or RISKY, draft a short personalized email; otherwise write null"
}

Classification guidance:
- HIGH (70-100): Strong usage + buying signals, ready for conversion push
- MEDIUM (40-69): Some engagement but needs nurturing
- LOW (0-39): Minimal engagement, at risk of churning
- RISKY: High-value prospect needing human attention (enterprise, compliance, unusual patterns) — score can be any number
```

6. Click **"Add item"** again:
   - **Role:** User
   - **Message Content:** Type the following, selecting each variable from the Google Sheets dropdown on the left panel:

```
Analyze this trial user:
- Name: {select name from dropdown}
- Company: {select company} ({select company_size} employees, {select industry})
- Role: {select role}
- Trial Day: {select trial_day} of 14
- Logins: {select logins}
- Projects Created: {select projects_created}
- Team Members Invited: {select team_members_invited}
- Features Activated: {select features_activated}
- Support Tickets: {select support_tickets}
- Pricing Page Visits: {select pricing_page_visits}
- Payment Method Added: {select payment_method_added}
- Avg Session Duration: {select session_duration_avg_min} min
- Last Login: {select last_login_days_ago} days ago
```

7. Click **OK**

**Step 3: Add JSON Parse**
1. Drag from the OpenAI module to create a new connection
2. Search for **JSON** → select **Parse JSON**
3. **JSON string:** Select the **message content** from the OpenAI module output (click the field, then select from the left panel)
4. Click **OK**

**Step 4: Add a Router**
1. Drag from the Parse JSON module → search for **Router** → select it

**Step 5: Set up the four paths**

| Path | Filter | Module | What it does |
|------|--------|--------|-------------|
| 1 — HIGH | intent_category **equals** `HIGH` | Gmail > Send an Email | Sends the AI-drafted personalized email |
| 2 — RISKY | intent_category **equals** `RISKY` | Gmail > Send an Email | Alerts sales team with AI assessment |
| 3 — MEDIUM | intent_category **equals** `MEDIUM` | Google Sheets > Add a Row | Logs to "Nurture Queue" tab |
| 4 — LOW | intent_category **equals** `LOW` | Google Sheets > Add a Row | Logs to "Low Intent Log" tab |

For each path:
- Click the connecting line to set the filter (label + condition using **intent_category** from Parse JSON)
- Configure the module (Gmail for email, Google Sheets for logging)
- For Gmail modules, use fields from Parse JSON: **email_draft** for the body, **intent_score** and **reasoning** for context

**Step 6: Save and Run**
1. Save (💾) and click **Run once** (▶)
2. Check your email — you should receive emails for HIGH and RISKY users
3. Check your Google Sheet tabs — MEDIUM and LOW users should appear in the logs
4. Click the **clock icon** at the bottom to see the full execution history

---

### Compare the Results

| User | Rule-Based | AI-Powered |
|------|-----------|------------|
| Sarah Chen — VP, 800 employees, 2 logins | LOW (low logins) | RISKY (enterprise prospect, HIPAA needs) |
| Priya Sharma — 11 logins, 6 invites | HIGH | HIGH + personalized email mentioning Jira integration |
| Raj Patel — 14 logins, discount code | HIGH | HIGH + email offering annual billing discount |
| Marcus Rivera — freelancer, 3 logins | LOW | LOW + reasoning about solo workflow mismatch |

---

## 4. Assignment for Session 2

### Assignment 1: Identify 5 Agentic Use Cases

Think about your day-to-day work or your product. Identify **5 workflows** that could be improved with agentic AI. For each one:

- What is the workflow today? (manual, rule-based, or partially automated?)
- Which agent design pattern(s) would apply?
- What would the "before vs. after" look like?

**Come to Session 2 ready to share at least 2 of these with the class.**

### Assignment 2: Tweak the Make.com Scenario

Take the AI-powered scenario and make **one meaningful change**. Pick one:

**Option A — Add a Reflection step:**
Add a second OpenAI module after the first one on the HIGH intent path. Give it a system prompt that reviews the draft email for quality (overpromising, tone, personalization). Send the *reviewed* email instead.

**Option B — Add Parallelization:**
Split the AI analysis into two parallel OpenAI calls — one for engagement signals, one for buying signals. Combine the results before routing.

**Option C — Prompt Engineering Iteration:**
Log every AI classification to a new "AI Audit Log" tab. Review the results. Tweak the system prompt to fix any classifications you disagree with. Run again and compare.

---

## 5. Tool Links

| Tool | URL | Notes |
|------|-----|-------|
| Make.com | https://www.make.com/ | Free tier: 1,000 ops/month |
| Google Antigravity | https://antigravity.withgoogle.com/ | PM workflows demo tool |
| OpenAI API Keys | https://platform.openai.com/api-keys | Needed for Make.com AI modules |
| Make.com Help | https://www.make.com/en/help | Scenario building reference |

---

## 6. Glossary

| Term | Definition |
|------|-----------|
| **Agentic AI** | AI systems that autonomously pursue goals through iterative reasoning, tool use, and decision-making. |
| **Agent Design Pattern** | A reusable architectural template for building agentic workflows (e.g., Pipeline, Routing, Reflection). |
| **Guardrails** | Constraints and safety checks placed on an agent to prevent undesirable actions. |
| **HITL (Human-in-the-Loop)** | A design pattern where a human reviews or approves agent actions at critical decision points. |
| **MCP (Model Context Protocol)** | An open standard that allows AI agents to discover and use external tools through a universal interface. |
| **MVA (Minimum Viable Agent)** | The simplest agentic workflow that delivers value — start with one pattern, prove value, then expand. |
| **Pipeline / Prompt Chaining** | A sequential pattern where the output of one LLM call becomes the input of the next. |
| **Reflection** | A pattern where the agent evaluates its own output and iterates to improve quality. |
| **Routing** | A pattern where a decision node directs input to different processing paths. |
| **Scenario** | Make.com's term for an automation workflow — a series of connected modules that run in sequence. |
| **Module** | Make.com's term for a single step in a scenario (e.g., "Read Google Sheet," "Send Gmail," "Call OpenAI"). |
| **System Prompt** | Instructions given to an AI model that define its role, behavior, and output format. |
| **Token** | The basic unit of text processed by an LLM; roughly 0.75 words in English. |

---

*Session 1 of 6 — Agent-driven Automation in Products — Institute of Product Leadership*
