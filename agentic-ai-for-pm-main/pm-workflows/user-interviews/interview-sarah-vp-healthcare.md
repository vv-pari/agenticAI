# User Interview — Sarah L.
## VP of Engineering, MediBridge (healthcare technology, ~800 employees)
**Date:** 2026-02-18
**Interviewer:** James K. + Diana M. (Solutions Engineering)
**Trial Day:** 3 of 14
**Usage:** 2 logins, 1 project (test), 0 team members invited

---

**[0:00]** Sarah joined with her camera off initially. Very professional, measured tone. Had a list of questions prepared — she came with a doc open.

**James:** Sarah, thanks for making time. I know you're early in the trial — how's your first impression?

**Sarah:** So I'll be blunt. The product looks good. We've been on Jira for four years and everyone hates it. My teams complain constantly — it's slow, the UX is terrible, and Atlassian's support has been... [pauses] unhelpful. So we're actively looking. But I can't just pick a tool because it's pretty. I have a list.

**[1:15]** [She literally pulled up a spreadsheet. This is going to be a compliance-focused conversation.]

**Sarah:** First question. HIPAA. Are you HIPAA compliant? Do you sign BAAs?

**Diana:** We're currently—

**Sarah:** "If the answer is 'we're working on it,' that's a non-starter. We handle PHI adjacently — our project descriptions sometimes reference patient cohort data, clinical trial identifiers. I need a signed BAA before I can even do a real evaluation."

**[2:00]** [Diana explained we have SOC 2 Type II but HIPAA/BAA is in progress. Sarah's face... well her camera was off but you could hear the sigh.]

**Sarah:** OK. SOC 2 is fine, necessary but not sufficient. What about data residency? We need US-only data storage. Some of our contracts with hospital systems explicitly require it.

**Diana:** All data is stored in US-East AWS regions—

**Sarah:** Can you provide documentation on that? Like an actual data processing addendum? Not a blog post, a legal document.

**[3:30]** [She is thorough. Asking questions our sales team should be ready for but probably isn't]

**James:** What about the product itself — any impressions from your initial look?

**Sarah:** I mean I set up one test project. The interface is significantly better than Jira. The workflow builder is interesting — we have very specific workflows for regulated software development and it looks like I could model those. But I didn't go deep because honestly until the security stuff checks out there's no point falling in love with features I can't use.

**Sarah:** "I've been burned before. We evaluated Notion two years ago, everyone loved it, then legal killed it in week 3 because of data handling concerns. I'm not doing that again."

**[5:00]** James asked about her team setup and needs.

**Sarah:** We have about 120 engineers, 30 PMs, plus QA and design. So call it 180-200 seats. At your pricing that's... what, $3,600/month? $43,000 a year? That's actually fine, that's within what we pay Atlassian now. The money is not the problem. "The money is never the problem for us. The problem is always security and procurement."

**James:** What does your procurement process look like?

**Sarah:** [laughs darkly] It's a 6-8 week process. Security review, legal review, vendor risk assessment, data classification review, IT architecture review. I need to submit a vendor packet. Do you have a standard security questionnaire you can fill out? Like a SIG or CAIQ?

**[7:00]** Diana said she'd check. [We need to get this together ASAP if we want enterprise healthcare deals]

**Sarah:** Also — SSO. We're on Okta. Is there SAML SSO?

**Diana:** Yes, on our Enterprise plan—

**Sarah:** And SCIM provisioning? With 200 users I'm not manually managing accounts.

**Diana:** SCIM is on our roadmap for Q2—

**Sarah:** [silence] OK. That's a problem. We need automated provisioning and deprovisioning. When someone leaves the company their access needs to be revoked automatically. That's not optional for us.

**[8:30]** She asked about audit logs next. We have basic audit logs but she wanted to know about log retention, exportability, integration with their SIEM (Splunk).

**Sarah:** What about the Jira migration path? We have 4 years of data, probably 50,000 tickets across multiple projects. Can you handle that volume?

**James:** Our migration tool handles up to—

**Sarah:** And what about attachments? We have attachments on maybe 30% of tickets. Some contain sensitive information.

**[10:15]** [This is a big fish but the compliance gap is real. She's not going to half-do this.]

**Sarah:** Look, I want to be clear — I'm not trying to be difficult. I genuinely want off Jira. My teams would love this tool. But I'm responsible for 800 people's data and our patients' data indirectly. I have to be thorough.

**James:** Completely understand. What would help you move forward?

**Sarah:** "Get me a completed SIG questionnaire, a data processing addendum, a BAA timeline, and SCIM timeline. If those check out I'll start the procurement process next month."

**[11:40]** End.

**Post-interview notes:**
- HUGE potential deal — 200 seats at enterprise pricing = big ARR
- But compliance blockers are real: HIPAA/BAA, SCIM, audit log depth
- She's a decision maker with budget authority — not tire-kicking
- Hates Jira passionately, team is motivated to switch
- Price is NOT the concern — security and compliance are everything
- Need to fast-track: BAA capability, SCIM provisioning, SIG questionnaire
- Diana to follow up with security documentation packet
- Could be a 6-8 week sales cycle minimum even if we clear compliance
- If we land MediBridge this could be a reference account for all of healthtech
