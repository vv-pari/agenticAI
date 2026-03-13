# Agent-driven Automation in Products

**Course:** ICAIPM2025L | Institute of Product Leadership
**Faculty:** Prof. Shameek Chakravarty
**Schedule:** Sundays 6:00 PM – 9:00 PM | March 2026

---

## Course Overview

This course teaches product leaders how to design, build, and govern AI agent systems within products. You will learn 8 fundamental agent design patterns and apply them using real tools — from no-code automation to agentic IDEs.

### Sessions

| Session | Date | Theme |
|---|---|---|
| **Session 1** | 1 Mar 2026 | Foundations + First Patterns + First Builds |
| **Session 2** | 8 Mar 2026 | Antigravity Deep-Dive + Advanced Patterns + MCP |
| **Session 3** | 15 Mar 2026 | Governance, Guardrails + Scaling |
| **Session 4** | 22 Mar 2026 | Capstone Presentations |

### Tools We Use

| Tool | What It Does | Setup Required |
|---|---|---|
| [Make.com](https://www.make.com/) | No-code workflow automation | Free account |
| [Langflow](https://www.langflow.org/) | Visual agent/flow builder | Free account |
| [Google Antigravity](https://antigravity.google/) | Agentic IDE for PMs and developers | Download + install |
| [GitHub Codespaces](https://github.com/codespaces) | Cloud dev environment (Session 3) | GitHub account |

---

## Quick Start

### 1. Pre-Class Setup (Do This Before Session 1)

- [ ] **Make.com** — Create a free account at [make.com](https://www.make.com/en/register)
- [ ] **Langflow** — Create a free account at [langflow.org](https://www.langflow.org/) or use [DataStax Langflow](https://astra.datastax.com/langflow)
- [ ] **OpenAI API Key** — Get one at [platform.openai.com](https://platform.openai.com/api-keys) (needed for Langflow exercises)
- [ ] **Google Antigravity** — Download at [antigravity.google/download](https://antigravity.google/download)
- [ ] **Read the caselet** — See [`caselet/`](./caselet/) folder

### 2. Clone This Repo

```bash
git clone https://github.com/shameekc/agentic-ai-for-pm.git
cd agentic-ai-for-pm
```

Or open directly in Google Antigravity:
1. Open Antigravity
2. File → Open Folder → select the cloned repo
3. You're ready

---

## Repository Structure

```
├── README.md                  ← You are here
├── caselet/
│   └── FreeTrial_Conversion_Caselet.md   ← Read before class
├── sample_data/
│   ├── trial_users.json       ← 10 trial user profiles (for exercises)
│   ├── trial_users.csv        ← Same data, Make.com compatible
│   └── scoring_rules.json     ← Scoring logic and thresholds
├── langflow/
│   ├── README.md              ← Import instructions
│   ├── Reflection_Pattern_NovaByte.json  ← Langflow flow (import this)
│   └── ToolUse_Pattern_NovaByte.json     ← Langflow flow (import this)
├── pm-workflows/              ← Antigravity PM workflow demos
│   ├── user-interviews/       ← 6 raw NovaByte trial user interview transcripts
│   ├── meeting-notes-raw.md   ← Messy product sync meeting notes
│   ├── prd-template.md        ← PRD template for Socratic questioning exercise
│   ├── novabyte-context.md    ← Company context doc (metrics, OKRs, competitive landscape)
│   └── trial-funnel-data.csv  ← 200-row funnel dataset for data analysis exercise
└── handout/
    └── Session1_Student_Handout.md       ← Reference during class
```

---

## Session 1: What to Prepare

### Read the Caselet
The [`caselet/`](./caselet/) folder contains the **NovaByte SaaS** case study — a B2B SaaS company struggling with free trial conversion. Read it and come prepared to discuss:

- For each of the 5 trial users: what action would you take and why?
- Where would you want a human in the loop?
- What guardrails would you put in place?

### Have Your Tools Ready
You will build during class. Make sure you can log into:
1. **Make.com** — we build a trial conversion pipeline from scratch
2. **Langflow** — we import pre-built flows and modify them
3. **Google Antigravity** — we use it for PM workflows (market research, analysis)

### Sample Data
The [`sample_data/`](./sample_data/) folder contains trial user profiles you'll use in the Make.com exercise. You'll send this data through the workflow you build.

### Langflow Flows
The [`langflow/`](./langflow/) folder contains two pre-built flows you'll import into Langflow during class:
1. **Reflection Pattern** — Agent drafts a nudge email, reviewer critiques it, reviser improves it
2. **Tool Use Pattern** — Agent fetches data from mock APIs before making a recommendation

See [`langflow/README.md`](./langflow/README.md) for import instructions.

### PM Workflow Files (Sessions 1 & 2)
The [`pm-workflows/`](./pm-workflows/) folder contains supporting files for Antigravity PM workflow demos:
- **`user-interviews/`** — 6 raw interview transcripts from NovaByte trial users (for synthesis exercises)
- **`meeting-notes-raw.md`** — Messy meeting notes from a product sync (for multi-format output demos)
- **`prd-template.md`** — PRD template for Socratic questioning exercise (Session 2)
- **`novabyte-context.md`** — Company context with metrics, OKRs, and competitive landscape (Session 2)
- **`trial-funnel-data.csv`** — 200-row funnel dataset for data analysis and segmentation (Session 2)

Open these files in Google Antigravity to use them in PM workflow exercises.

---

## The 8 Agent Design Patterns

These are the conceptual backbone of the course. Every agentic system is a composition of these patterns.

| # | Pattern | One-Line Definition |
|---|---|---|
| 1 | **Pipeline** | Output of one step feeds the next |
| 2 | **Routing** | Direct inputs to different paths based on classification |
| 3 | **Parallelization** | Run multiple tasks simultaneously |
| 4 | **Reflection** | Agent critiques and improves its own output |
| 5 | **Tool Use** | Agent calls external APIs and services |
| 6 | **MCP** | Standardized protocol for agent-tool connectivity |
| 7 | **Planning** | Agent creates multi-step strategies before executing |
| 8 | **Multi-Agent** | Multiple specialized agents collaborating |

---

## Need Help?

- **During class:** Ask in the Zoom chat or unmute
- **Tool issues:** If something breaks, switch to "observe mode" — watch the instructor and follow the logic. You can build later.
- **After class:** Revisit this repo — all materials remain accessible

---

*Agent-driven Automation in Products | Institute of Product Leadership | March 2026*
