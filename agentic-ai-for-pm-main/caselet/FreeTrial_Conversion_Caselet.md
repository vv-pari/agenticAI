# NovaByte SaaS — The Free Trial Conversion Challenge

## A Caselet for Agent-driven Automation in Products | Session 1
### Institute of Product Leadership | ICAIPM2025L

---

## About NovaByte

**NovaByte** is a mid-stage B2B SaaS company offering a cloud-based project management and collaboration platform for engineering teams. Founded in 2021, NovaByte has grown to 2,800 paying customers and 45,000 monthly active users across its free and paid tiers.

**Product tiers:**
- **Free Plan:** Up to 5 users, 3 projects, basic features
- **Pro Plan:** $15/user/month — unlimited projects, integrations, advanced analytics
- **Enterprise Plan:** Custom pricing — SSO, audit logs, dedicated support, SLA guarantees

**Business model:** Product-led growth (PLG). Users sign up for a 14-day free trial of the Pro plan. After 14 days, they either convert to a paid plan or drop to the Free tier.

---

## The Problem

NovaByte's **free trial to paid conversion rate has stagnated at 8.2%** — well below the B2B SaaS industry benchmark of 15-25% for product-led companies.

The Growth team has identified that the problem is not acquisition (trial sign-ups are healthy at ~3,200/month) but **activation and conversion**. Most trial users never reach the "aha moment" — the point where they experience enough value to justify paying.

**Current state of trial management:**
- A single drip email sequence (7 emails over 14 days) goes to ALL trial users regardless of behavior
- The sales team manually reviews a spreadsheet of "high-potential" trials once a week and reaches out to ~20 users
- No systematic way to identify at-risk trials early, or to differentiate between users who need a nudge vs. users who need human help vs. users who should be left alone
- Customer Success only engages post-conversion

**The CEO has tasked the Product team with a bold goal:** *"Use AI agents to double our trial conversion rate to 16% within 6 months, without doubling the sales team."*

---

## Available Data

NovaByte has the following data sources that an AI agent system could potentially access:

### 1. Product Usage Data (Mixpanel)
| Signal | Example Values |
|---|---|
| Login frequency | 0-14 logins in trial period |
| Features activated | Project creation, team invite, integration setup, dashboard views |
| Time-to-first-action | Minutes from signup to first meaningful action |
| Session duration | Average minutes per session |
| Collaboration signals | Team members invited, comments made, files shared |

### 2. User Profile Data (CRM — HubSpot)
| Signal | Example Values |
|---|---|
| Company size | 1-10, 11-50, 51-200, 201-1000, 1000+ |
| Industry | Technology, Finance, Healthcare, Education, etc. |
| Role of signup user | IC Engineer, Team Lead, Engineering Manager, VP/Director, CTO |
| Source channel | Organic, Paid, Referral, Partner |
| Trial day | Day 1 through Day 14 |

### 3. Support Interactions (Zendesk)
| Signal | Example Values |
|---|---|
| Tickets raised during trial | 0, 1, 2, 3+ |
| Ticket topics | Setup help, billing questions, feature requests, bug reports |
| Sentiment | Positive, Neutral, Frustrated |
| Resolution status | Resolved, Pending, Escalated |

### 4. Billing Signals (Stripe)
| Signal | Example Values |
|---|---|
| Pricing page visits | 0, 1, 2+ |
| Plan comparison views | Yes/No |
| Payment method added | Yes/No |
| Discount code attempted | Yes/No |

---

## Five Trial Users — Who Gets What?

Below are five real trial users (anonymized). Read each profile and think about what action — if any — an intelligent system should take.

### User A: Priya — Engineering Manager at a fintech startup (Day 7)
- **Company size:** 35 employees
- **Usage:** Created 4 projects, invited 6 team members, set up Jira integration, 11 logins in 7 days
- **Support:** 0 tickets
- **Billing:** Visited pricing page twice, compared Pro vs Enterprise

### User B: Marcus — Solo freelance developer (Day 10)
- **Company size:** 1 (solo)
- **Usage:** Created 1 project, 0 team members invited, 3 logins total, last login 4 days ago
- **Support:** 0 tickets
- **Billing:** No pricing page visits

### User C: Sarah — VP of Engineering at a healthcare company (Day 3)
- **Company size:** 800 employees
- **Usage:** Created 1 project, invited 2 team members, 2 logins
- **Support:** 1 ticket — asked about HIPAA compliance and data residency
- **Billing:** No pricing page visits yet

### User D: Raj — Team Lead at an e-commerce company (Day 12)
- **Company size:** 120 employees
- **Usage:** Created 3 projects, invited 8 team members, daily logins, heavy use of analytics dashboards
- **Support:** 1 ticket — asked about annual billing discount
- **Billing:** Visited pricing page 3 times, attempted discount code (expired)

### User E: Chen — Junior developer, signed up from a blog post (Day 5)
- **Company size:** 2,000+ employees (large enterprise)
- **Usage:** Created 1 project, 0 team members invited, 5 logins, mostly explored settings and integrations
- **Support:** 0 tickets
- **Billing:** No pricing page visits

---

## Questions to Think About Before Class

Come prepared to discuss these. There are no "right" answers — but your reasoning matters.

### Business & Strategy
1. **For each of the five users above**, what action would you recommend? (Nudge to convert? Ignore? Escalate to human sales? Something else?) Why?
2. Which **data signals** are most predictive of conversion intent? How would you weight them?
3. What are the **risks** of getting the action wrong? (e.g., what happens if an AI agent sends an aggressive sales nudge to User C, the VP evaluating HIPAA compliance?)

### Agent Design Thinking
4. If you were to design an AI agent system for this problem, **how many agents would you need?** What would each one do?
5. Where would you want a **human in the loop**, and where would you trust the system to act autonomously? What would your confidence thresholds be?
6. What **guardrails** would you put in place? What should the system NEVER do?

### Product & UX
7. How would the **sales team** interact with this system? Would they trust it? What would make them trust or distrust it?
8. What would your **Minimum Viable Agent (MVA)** look like? What's the simplest version you'd ship first?
9. How would you **measure success**? What metrics matter beyond conversion rate?

### Broader Thinking
10. NovaByte's CEO wants to "double conversion without doubling the sales team." Is this the right framing? What's missing from this goal?

---

## What We'll Do in Class

In today's session, you will:
- **See** how an agentic IDE (Google Antigravity) can help PMs do market research, competitive analysis, and strategy work
- **Build** an automated trial conversion workflow using Make.com — implementing Pipeline and Routing patterns
- **Explore** agent reflection and tool-use patterns using Langflow
- **Learn** the 8 fundamental agent design patterns that power all agentic AI systems

**Come with Make.com and Langflow accounts ready.** If you haven't signed up yet, do so before class.

---

*NovaByte is a fictional company created for educational purposes.*
*Agent-driven Automation in Products | Prof. Shameek Chakravarty | Institute of Product Leadership*
