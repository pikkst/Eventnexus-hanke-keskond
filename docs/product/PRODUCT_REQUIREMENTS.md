# EventNexus Hanke Keskond — Product Requirements Document

**Document ID:** PRD-001  
**Task:** S0-T01  
**Status:** Draft complete; awaiting product-owner approval  
**Product owner:** Eventnexus OÜ  
**Primary market:** Estonia  
**Default product language:** Estonian (`et-EE`)  
**Deployment:** Local, self-hosted Docker environment  
**External AI provider:** Google Gemini through a controlled provider adapter  
**Last updated:** 2026-08-04

---

## 1. Executive summary

EventNexus Hanke Keskond is a local-first procurement intelligence and tender preparation workspace for Eventnexus OÜ. It helps a small internal team find relevant Estonian and European IT procurements, understand tender requirements, assess whether Eventnexus OÜ should participate, conduct controlled research, prepare evidence-backed proposal content, coordinate reviews, and export a submission-ready package.

The product reduces manual search, document reading, requirement tracking, repetitive drafting, and review work. It does not transfer legal, commercial, or submission responsibility to AI. Every binding claim, declaration, price, attachment, approval, signature, and submission remains under human control.

The application runs locally in Docker. Google Gemini is an external service, so the product must clearly distinguish local processing from external AI processing and must enforce data-classification, redaction, access-control, audit, and cost policies before any content is sent outside the local environment.

The MVP succeeds when Eventnexus OÜ can use one reproducible local installation to process real IT tender opportunities from discovery to a reviewed export package, while achieving measurable improvements in coverage, preparation time, traceability, and error prevention.

---

## 2. Product decision summary

| Decision area | MVP decision |
|---|---|
| Primary user | Procurement and Bid Lead responsible for daily opportunity triage and proposal coordination |
| Final decision-maker | Authorized Business Decision-Maker who approves participation, commercial terms, declarations, final package, and submission |
| Supporting users | Technical contributors, commercial reviewers, legal/compliance reviewers, and local system administrators |
| Market | Estonia first, with relevant EU opportunities supported through TED and English-language source material |
| Deployment | Single-organization, local Docker installation on an Eventnexus-controlled workstation or server |
| AI | Google Gemini used only through policy-gated application workflows; AI outputs are drafts and recommendations |
| Submission | Human-controlled submission through the official procurement channel |
| Autonomous submission | Explicitly excluded from the MVP |
| Public SaaS | Explicitly excluded from the MVP |
| Product language | Estonian-first UI and workflows; English tender ingestion, analysis, drafting, and export supported |
| Source integrations | Official and permitted RHR/TED paths where validated; manual import is the guaranteed fallback |

---

## 3. Problem statement

Eventnexus OÜ needs to identify suitable IT procurement opportunities and prepare compliant bids without maintaining a large procurement department. Current work is fragmented across procurement portals, downloaded files, spreadsheets, notes, email, document editors, and individual memory.

The primary problems are:

1. Relevant opportunities are difficult to find consistently and early enough.
2. Procurement notices and attachments are distributed across sources and versions.
3. Mandatory requirements, deadlines, evaluation criteria, forms, and exclusions are easy to overlook.
4. Eligibility and strategic-fit decisions rely on incomplete or unstructured company knowledge.
5. Proposal content is repeatedly recreated instead of being assembled from approved evidence.
6. AI can accelerate analysis and drafting but may hallucinate, omit requirements, lose citations, or expose restricted data.
7. Pricing, declarations, attachments, and approvals require clear ownership and version control.
8. Amendments can make prior analysis, drafts, or approvals stale.
9. Final submission packages can contain missing, outdated, inconsistent, or incorrectly named files.
10. After submission, evidence of what was submitted and why decisions were made is difficult to reconstruct.

---

## 4. Product goals and user outcomes

The following outcomes define what the MVP must achieve. All MVP features must map to at least one outcome.

| Outcome ID | User outcome |
|---|---|
| O1 | The team discovers relevant IT opportunities early enough to make an informed participation decision. |
| O2 | The primary user can understand a tender's scope, dates, eligibility rules, evaluation method, required forms, and major risks without manually rereading every document. |
| O3 | The decision-maker can make a traceable `GO`, `NO-GO`, or `NEEDS-MORE-INFORMATION` decision using evidence, capacity, commercial, and risk information. |
| O4 | Every material tender requirement is tracked with its source, response status, owner, evidence, and open questions. |
| O5 | Proposal drafts reuse approved company facts and references without inventing qualifications, experience, certificates, personnel, customers, or financial data. |
| O6 | Users can use Gemini for permitted work while restricted data, secrets, and unapproved content remain protected. |
| O7 | Technical, commercial, legal, security, and management reviewers can review exact versions and see what changed. |
| O8 | The team can export a complete, deterministic, internally approved package and submission checklist. |
| O9 | An authorized person can submit manually and record verifiable submission evidence without the system storing identity secrets. |
| O10 | Administrators can operate, audit, back up, restore, and troubleshoot the local system without depending on a public cloud deployment. |

---

## 5. Users and roles

### 5.1 Primary user — Procurement and Bid Lead

The **Procurement and Bid Lead** is the primary daily user.

Responsibilities:

- configure opportunity interests and review discovered tenders;
- create and manage tender workspaces;
- coordinate document ingestion and requirement review;
- prepare the participation recommendation;
- assign content, evidence, pricing, and review tasks;
- use approved AI workflows for analysis, research, and drafting;
- maintain the compliance matrix;
- assemble the package for final approval;
- record submission and outcome information.

The primary user may recommend participation but cannot be assumed to possess final legal or commercial authority.

### 5.2 Final decision-maker — Authorized Business Decision-Maker

The **Authorized Business Decision-Maker** is the explicit final decision-maker. This role may be fulfilled by a board member, managing director, or another person formally authorized by Eventnexus OÜ.

Responsibilities:

- approve or reject participation;
- approve binding commitments and material assumptions;
- approve final pricing and risk acceptance;
- approve declarations and representations;
- approve the exact final export package;
- perform or explicitly delegate the official submission;
- confirm withdrawal, material clarification responses, or other high-impact actions.

AI, automated scoring, or the Procurement and Bid Lead cannot replace this role.

### 5.3 Technical Contributor

Responsibilities:

- answer solution and architecture questions;
- validate technical feasibility, delivery assumptions, integrations, security, support, and staffing;
- provide approved evidence and references;
- review technical proposal sections.

### 5.4 Commercial and Pricing Reviewer

Responsibilities:

- validate units, effort, rates, expenses, margin, VAT treatment, contingency, payment terms, and commercial assumptions;
- approve or reject pricing versions;
- verify consistency between narrative commitments and price calculations.

### 5.5 Legal, Compliance, and Security Reviewer

Responsibilities:

- review declarations, contractual risks, privacy, data-processing, security, eligibility, exclusion grounds, intellectual property, liability, and other high-risk conditions;
- identify matters requiring external professional advice;
- approve only within actual authority and expertise.

The product must not represent AI output as legal advice or legal approval.

### 5.6 Local System Administrator

Responsibilities:

- install and update the Docker environment;
- manage users, roles, configuration, API key references, backup, restore, retention, and monitoring;
- review security and system audit events;
- manage Gemini enablement and budgets according to approved policy;
- troubleshoot integrations and background jobs.

The administrator does not automatically receive authority to approve bids or prices.

### 5.7 Auditor / Read-only Reviewer

Optional MVP role for management or internal review.

Responsibilities:

- inspect opportunities, decisions, evidence, approvals, exports, submission records, and audit events;
- produce reports without changing approved business data.

---

## 6. Role and decision authority matrix

| Activity | Bid Lead | Decision-Maker | Technical | Commercial | Legal/Security | Admin | Auditor |
|---|---:|---:|---:|---:|---:|---:|---:|
| Review opportunities | R/W | R | R | R | R | R | R |
| Create tender workspace | Yes | Yes | No | No | No | No | No |
| Request AI analysis | Yes, policy-gated | Yes, policy-gated | Limited | Limited | Limited | Configure only | No |
| Review extracted requirements | Yes | R | Yes | Yes | Yes | No | R |
| Recommend `GO/NO-GO` | Yes | Yes | Advisory | Advisory | Advisory | No | No |
| Final participation decision | No | **Yes** | No | No | No | No | No |
| Draft technical response | Coordinate | R | Yes | No | Advisory | No | R |
| Edit pricing | Limited by permission | Yes | Assumptions only | Yes | R | No | R |
| Final price approval | No | **Yes** | No | Advisory | No | No | No |
| Approve legal declarations | No | **Yes** | No | No | Advisory/review | No | R |
| Approve final package | Prepare | **Yes** | Section approval | Section approval | Section approval | No | R |
| Submit through official channel | No unless authorized | **Yes or explicit delegate** | No | No | No | No | No |
| Manage system configuration | No | R | No | No | No | **Yes** | R |

`R/W` means read and edit within assigned permissions. Server-side authorization must enforce actual permissions; the table is a product requirement, not a substitute for authorization logic.

---

## 7. Jobs to be done

### 7.1 Opportunity discovery

**When** new procurements are published or changed,  
**the Bid Lead wants to** see likely relevant IT opportunities ranked and explained,  
**so that** Eventnexus OÜ can react before deadlines become operationally unsafe.

### 7.2 Tender understanding

**When** a potentially relevant tender is opened,  
**the Bid Lead wants to** obtain a cited overview of scope, dates, eligibility, lots, evaluation, deliverables, forms, and risks,  
**so that** the team can understand the opportunity quickly without losing source traceability.

### 7.3 Participation decision

**When** the tender has been analyzed,  
**the decision-maker wants to** see hard disqualifiers, capability fit, missing evidence, partner needs, capacity, commercial potential, risk, and unresolved questions,  
**so that** participation is an explicit business decision rather than an AI score or intuition alone.

### 7.4 Requirement control

**When** the team begins preparing a bid,  
**the Bid Lead wants to** track every mandatory, scored, administrative, contractual, and submission requirement,  
**so that** no requirement is silently omitted.

### 7.5 Evidence-backed drafting

**When** a response section is prepared,  
**contributors want to** retrieve approved company facts and relevant tender evidence,  
**so that** drafts are fast to produce, defensible, and free from fabricated claims.

### 7.6 Controlled AI assistance

**When** analysis, research, translation, or drafting would benefit from Gemini,  
**users want to** know what data will leave the local environment and whether the action is permitted,  
**so that** productivity does not create uncontrolled confidentiality, privacy, or cost risk.

### 7.7 Review and approval

**When** a draft, price, declaration, or package is ready,  
**reviewers want to** approve an exact version and see later changes,  
**so that** approvals cannot remain attached to modified content.

### 7.8 Package preparation and submission handoff

**When** the bid is ready,  
**the Bid Lead wants to** generate a deterministic package, validation report, and checklist,  
**so that** an authorized person can perform the official submission with fewer preventable errors.

### 7.9 Audit and learning

**When** a tender is submitted, lost, won, cancelled, or abandoned,  
**management wants to** reconstruct inputs, decisions, versions, approvals, submission evidence, and outcomes,  
**so that** the company can improve future bids and demonstrate internal control.

---

## 8. Pain points and required product responses

| Pain point | Required product response |
|---|---|
| Opportunities are spread across sources | Unified normalized opportunity list with source provenance and freshness |
| Search results contain noise | Explainable fit scoring, hard filters, exclusions, and manual feedback |
| Deadlines and amendments are missed | Preserved source dates, amendment detection, visible freshness, and prioritized alerts |
| Tender files are difficult to navigate | Versioned document storage, parsing, OCR fallback, search, summaries, and citations |
| Requirements are overlooked | Human-reviewable requirement extraction and compliance matrix |
| Company knowledge is scattered | Structured company evidence library with validity and approval state |
| Drafts contain unsupported claims | Evidence retrieval, citations, claim classification, and unsupported-claim checks |
| AI may expose data | Classification-aware Gemini policy gate, redaction, audit, and local-only path |
| AI output is unreliable | Structured schemas, confidence, visible unknowns, evaluation, and mandatory human review |
| Pricing changes are hard to track | Versioned pricing assumptions, calculations, approvals, and package invalidation |
| Reviews happen in disconnected channels | Assigned review workflow, exact-version approvals, comments, and change history |
| Final packages are inconsistent | Deterministic export templates, naming rules, completeness checks, and manifest |
| Submission credentials are sensitive | No credential storage; manual official submission and evidence recording |
| Local operations can fail | Health checks, structured logs, backup, restore, and documented runbooks |

---

## 9. Core workflows

### 9.1 Configure company and opportunity interests

1. Administrator creates the local installation and users.
2. Authorized users record Eventnexus OÜ capabilities, technologies, sectors, CPV interests, exclusions, capacity, geographic preferences, risk appetite, references, personnel, certificates, partners, and approved evidence.
3. Factual company claims remain distinguishable from preferences and derived scores.
4. Evidence receives an owner, source, validity period, classification, and approval state.

Detailed company-profile fields are defined in S0-T02.

### 9.2 Discover and triage opportunities

1. The system synchronizes configured official sources through validated adapters.
2. Users can manually import a notice or tender package when an official integration is unavailable.
3. The system preserves raw source data, normalizes fields, detects duplicates, and records source freshness.
4. Deterministic rules and AI-assisted classification identify likely IT relevance.
5. Each opportunity receives an explainable fit assessment, hard disqualifiers, missing information, confidence, and source evidence.
6. The Bid Lead marks the item as ignored, monitoring, candidate, or workspace-ready.

### 9.3 Create a tender workspace

1. The Bid Lead creates a workspace from an opportunity or manual import.
2. The workspace records source identifiers, lots, deadlines, buyer, procedure, language, team, and current lifecycle state.
3. All original files are immutable and versioned.
4. Uploaded and downloaded documents are classified before external AI use.
5. Parsing, OCR, indexing, and malware checks run as controlled background jobs.

### 9.4 Analyze the tender

1. The system produces a cited tender overview.
2. It extracts candidate dates, requirements, evaluation criteria, requested evidence, forms, contractual obligations, risks, and open questions.
3. Users review and correct candidate extraction before it becomes authoritative.
4. Conflicting dates or source statements remain visible and are not silently resolved.
5. Amendments create new versions and invalidate affected analysis.

### 9.5 Make the participation decision

1. The system compares the tender against approved company facts, available evidence, capacity, exclusions, and risk preferences.
2. The team records technical, commercial, legal, security, staffing, partner, and timing considerations.
3. The Bid Lead prepares a recommendation.
4. The Authorized Business Decision-Maker records `GO`, `NO-GO`, or `NEEDS-MORE-INFORMATION`, with rationale.
5. No state transition to active bid preparation depends only on model output.

### 9.6 Build the compliance matrix

1. Reviewed requirements are grouped as mandatory, scored, informative, contractual, administrative, and submission-related.
2. Each requirement has source location, owner, due date, planned response, evidence, status, reviewer, and open questions.
3. `COMPLIANT` requires linked evidence or a reviewed explanation.
4. Gaps, contradictions, expired evidence, and missing attachments remain visible.

### 9.7 Conduct controlled research

1. A user defines or approves a bounded research question.
2. The system creates a research plan with allowed sources, freshness needs, confidentiality limits, and stopping conditions.
3. Research results retain source identifiers, retrieval time, excerpts, and confidence.
4. Public research does not automatically become an approved company claim.
5. Research that requires unavailable or prohibited sources is marked incomplete rather than guessed.

### 9.8 Draft the proposal

1. The system creates a requirement-to-section outline.
2. Approved tender evidence and company evidence are retrieved for each section.
3. Gemini drafts content using structured instructions and explicit evidence constraints.
4. Drafts label assumptions, estimates, commitments, unresolved questions, and source-backed facts.
5. Unsupported-claim and citation validation run before review.
6. Contributors edit and review exact versions.

### 9.9 Prepare and approve pricing

1. Users define resources, quantities, units, rates, expenses, contingency, margin, currency, and VAT treatment.
2. The system calculates scenarios deterministically.
3. AI may explain or suggest scenarios but cannot approve binding prices.
4. Commercial review and final decision-maker approval are recorded separately.
5. Material price changes invalidate affected approvals and exports.

### 9.10 Review, approve, and export

1. The Bid Lead requests technical, commercial, legal/security, and final reviews according to configured gates.
2. Approvals refer to exact versions and content hashes.
3. Any approved-content change invalidates the relevant approval.
4. The export validator checks required responses, evidence, forms, signatures, filenames, formats, totals, deadlines, and unresolved blockers.
5. The system generates a deterministic package, manifest, validation report, and submission checklist.
6. The Authorized Business Decision-Maker approves the exact final package.

### 9.11 Manual submission and submission evidence

1. The authorized person opens the official procurement channel outside the product or through a safe user-controlled link.
2. The authorized person authenticates and submits manually.
3. The product never stores ID-card PINs, Smart-ID/Mobile-ID secrets, signing keys, reusable portal credentials, or equivalent identity secrets.
4. The user records submission time, submitter, official reference, package hash, receipt, screenshots or receipt documents where appropriate, and notes.
5. Submission evidence is linked to the exact exported package.

### 9.12 Monitor changes and outcomes

1. The system continues to detect amendments, clarifications, cancellation, award, and outcome notices where supported.
2. Material source changes flag or invalidate stale analysis, drafts, decisions, and approvals.
3. Users record clarification responses, withdrawal, submitted, awarded, not-awarded, cancelled, or archived outcomes.
4. Outcome data supports later retrospective analysis without changing historical evidence.

---

## 10. MVP feature set and user-outcome mapping

Every feature below maps to one or more outcomes from Section 4.

| Feature ID | MVP feature | Required user outcome(s) |
|---|---|---|
| F01 | Local Docker installation with authenticated users and role-based permissions | O7, O10 |
| F02 | Eventnexus OÜ profile and approved evidence library | O3, O4, O5 |
| F03 | Configurable RHR/TED ingestion through validated official or permitted adapters | O1 |
| F04 | Manual notice, URL metadata, and tender-package import fallback | O1, O2 |
| F05 | Raw-source preservation, normalization, deduplication, freshness, and amendment detection | O1, O2, O7 |
| F06 | Estonian-first opportunity search, filters, saved views, and explainable relevance ranking | O1, O3 |
| F07 | Explainable eligibility and strategic-fit assessment with gaps and disqualifiers | O3 |
| F08 | Versioned tender workspace with team, lots, dates, states, and audit history | O2, O7 |
| F09 | Immutable document storage, parsing, OCR fallback, indexing, and source citations | O2, O4, O10 |
| F10 | Human-reviewable tender summary and requirement extraction | O2, O4 |
| F11 | Compliance matrix with owners, evidence, status, review, and open questions | O4, O7 |
| F12 | Bounded public-research workflow with provenance and freshness metadata | O2, O3, O5 |
| F13 | Classification-aware Gemini policy gate, redaction, budget limits, and invocation audit | O6, O10 |
| F14 | Estonian and English analysis, translation assistance, terminology control, and source-language preservation | O2, O5, O6 |
| F15 | Proposal outline and evidence-grounded section drafting | O4, O5 |
| F16 | Citation validation, unsupported-claim detection, assumption labeling, and visible confidence | O4, O5, O7 |
| F17 | Deterministic pricing workspace with versions, assumptions, VAT, margin, and approvals | O3, O7, O8 |
| F18 | Versioned comments, assignments, review gates, approvals, and invalidation rules | O7, O8 |
| F19 | Deterministic DOCX/PDF/XLSX/ZIP export, manifest, completeness checks, and submission checklist | O8 |
| F20 | Human-controlled submission record linked to exact package hash and receipt evidence | O9 |
| F21 | Structured audit trail for security, AI, decisions, approvals, exports, and submission records | O3, O6, O7, O9, O10 |
| F22 | Local health monitoring, logs, backup, restore, retention, and administrator runbooks | O10 |
| F23 | Amendment and clarification impact detection with stale-content warnings | O1, O2, O4, O7, O8 |
| F24 | Outcome recording and basic bid retrospective data | O3, O10 |

A feature is not complete merely because its screen or endpoint exists. It must demonstrably produce the mapped user outcome and satisfy its security, traceability, language, and review requirements.

---

## 11. MVP boundaries

### 11.1 Included in the MVP

The MVP includes:

- one Eventnexus OÜ organization per installation;
- a small internal team with explicit roles and permissions;
- installation and operation on one local Docker host;
- PostgreSQL/pgvector, local object storage, background jobs, and local audit data;
- official/permitted RHR and TED ingestion paths that pass discovery and policy review;
- manual import as a supported fallback;
- Estonian-first opportunity discovery and tender workspaces;
- English-language tender ingestion and response handling;
- document parsing, OCR fallback, citation, versioning, and search;
- explainable opportunity matching and participation recommendation support;
- requirement extraction and a reviewed compliance matrix;
- approved company evidence and reusable content;
- policy-gated Gemini analysis, research, translation assistance, and drafting;
- unsupported-claim checks and human review;
- deterministic pricing calculations and approval workflow;
- package export, validation report, manifest, and checklist;
- human-controlled official submission and local submission evidence record;
- audit, logging, health checks, backup, restore, and pilot evaluation.

### 11.2 Conditionally included

The following are included only when the relevant discovery, legal, security, and technical decisions approve them:

- automated synchronization from RHR;
- source polling frequency and amendment alerts;
- specific Gemini file, cache, grounding, or retention features;
- retrieval from public web sources beyond configured source adapters;
- automated notifications to email or another external channel.

The manual workflow must remain usable when a conditional integration is unavailable.

### 11.3 Explicitly excluded from the MVP

The MVP does not include:

1. **Autonomous tender submission.**
2. Browser automation that logs into RHR or another portal and submits on behalf of a user.
3. Storage of ID-card PINs, Smart-ID or Mobile-ID secrets, signing keys, reusable procurement-portal credentials, or equivalent authentication secrets.
4. Autonomous legal approval, legal advice, or replacement of qualified professional review.
5. Autonomous final `GO/NO-GO`, price, declaration, commitment, signature, or package approval.
6. A public multi-tenant SaaS service.
7. Multi-company billing, subscriptions, marketplace features, or reseller administration.
8. A native mobile application.
9. Certified legal translation or a guarantee that machine-assisted translation has legal equivalence.
10. General-purpose unrestricted AI agents with arbitrary shell, network, browser, email, or filesystem access.
11. A promise that all processing is offline while Gemini is enabled.
12. Guaranteed tender discovery, compliance, award, profitability, or legal validity.
13. Full ERP, CRM, accounting, payroll, invoicing, or project-delivery management.
14. Full post-award contract execution; the MVP records outcomes and may preserve handoff information only.
15. Production use for other organizations before a later multi-organization security and product review.

---

## 12. Estonian-first and English tender requirements

### 12.1 Product interface language

- Estonian (`et-EE`) is the default and complete MVP interface language.
- Core navigation, actions, validation messages, errors, review states, notifications, help text, exports, and administrator workflows must be available in Estonian.
- User-facing strings must be stored in localization resources rather than hard-coded in application code.
- English UI resources may be added for development, support, and English-speaking contributors, but Estonian completeness is the release gate.
- Missing translations must fail visibly in development and must not silently expose localization keys in production.

### 12.2 Locale behavior

- User-visible dates and times default to Estonian conventions and the `Europe/Tallinn` timezone.
- The system stores canonical timestamps in UTC while preserving original tender date text and source timezone information.
- Decimal, currency, VAT, and thousands separators must follow the selected locale while calculations use locale-independent numeric types.
- Estonian names, Unicode characters, filenames, and search terms must be preserved correctly.
- Search should support Estonian inflection and common English technology terms where feasible.

### 12.3 Tender source language preservation

- Every document and extracted segment records detected or declared source language.
- Original source text remains authoritative and immutable.
- Translated text never replaces the original.
- Citations point to the original document version and source location even when the working draft is translated.
- The UI must clearly label original text, machine-assisted translation, human-edited translation, and approved final wording.

### 12.4 English tender handling

The MVP must support tenders whose notice, attachments, questions, requirements, or response templates are partly or fully in English.

Required behavior:

1. ingest and index English documents without forcing Estonian translation;
2. produce an Estonian working summary when requested;
3. extract requirements from English source material while preserving original quotations and terminology;
4. allow the compliance matrix to show original English requirement text beside an Estonian working translation;
5. draft proposal sections in English when the required response language is English;
6. allow Estonian internal comments and review notes on an English proposal;
7. maintain a tender-specific bilingual glossary for defined terms, acronyms, product names, legal terms, role names, and repeated phrases;
8. validate terminology consistency across English sections and attachments;
9. retain an explicit `response_language` for each deliverable and export;
10. warn when the response language is unknown, conflicting, or differs between lots or forms.

### 12.5 Translation safety rules

- Machine-assisted translation is a draft unless a human explicitly approves it.
- Legal, eligibility, exclusion, liability, warranty, penalty, security, privacy, intellectual-property, and pricing clauses require source-text review.
- The system must not silently simplify or normalize legally material wording.
- Ambiguous or conflicting terms remain visible with an open question.
- Numbers, dates, currencies, percentages, units, named entities, and identifiers require deterministic comparison against the source.
- Gemini must not invent an Estonian equivalent when a controlled glossary term is required.
- Export must indicate the selected response language and must not accidentally mix languages in required forms.

---

## 13. AI-assisted product requirements

### 13.1 Human accountability

- AI output is always a candidate, draft, classification, extraction, calculation explanation, or recommendation.
- AI cannot create approved business facts.
- AI cannot approve participation, pricing, declarations, commitments, packages, or submission.
- Critical decisions must identify the human actor, timestamp, exact version, and rationale.

### 13.2 Evidence grounding

- Material tender facts must cite an immutable document version and location.
- Company claims must link to approved company evidence.
- Public research must retain provenance and cannot silently become approved company evidence.
- Missing evidence produces an explicit gap, not a fabricated completion.
- AI-generated commitments and assumptions must be clearly labeled and reviewed.

### 13.3 External processing transparency

Before a Gemini request, the application must:

1. determine the workspace and document classifications;
2. identify permitted excerpts;
3. apply configured redaction;
4. show or record that external processing will occur;
5. enforce configured token and cost limits;
6. record safe invocation metadata;
7. prevent restricted or unknown-classification data from external processing.

The product must not claim to be fully offline while Gemini is enabled.

### 13.4 AI failure behavior

- Schema-invalid output is rejected or retried within a small configured limit.
- Unsupported claims remain visible as errors or review blockers.
- Gemini outage, quota, budget, or policy denial must leave the tender workspace usable through manual and local workflows.
- A failed AI job must not delete source documents or previously reviewed content.
- Model confidence must never be converted directly into a legal or compliance decision.

---

## 14. Functional requirements

### 14.1 Opportunity management

- Store source identity, source version, raw payload, normalized fields, CPV codes, buyer, procedure, lots, dates, language, links, status, and freshness.
- Support filters for source, CPV, technology, buyer, location, value, deadline, procedure, status, fit, and hard exclusions.
- Show why an opportunity matched and what information is missing.
- Preserve ignored opportunities according to retention policy so matching can be evaluated.
- Detect or allow users to record amendments and cancellations.

### 14.2 Documents and citations

- Preserve immutable originals and SHA-256 hashes.
- Create explicit document versions.
- Record MIME type, size, source, acquisition time, language, classification, parser identity, parser version, OCR status, and confidence.
- Support at minimum common tender PDF, DOCX, XLSX, and archive workflows subject to safe parser support.
- Prevent unsafe archive extraction, path traversal, decompression bombs, executable content, and unbounded parsing.
- Citations must remain valid after later document versions are added.

### 14.3 Requirements and compliance

- Distinguish mandatory, scored, informative, administrative, contractual, and submission requirements.
- Store source excerpt and source location.
- Track owner, due date, status, response, evidence, review, confidence, and open questions.
- Prevent `COMPLIANT` without evidence or a reviewed explanation.
- Show conflicts, duplicate requirements, dependencies, and amendment impact.

### 14.4 Proposal content

- Maintain a requirement-to-section plan.
- Support versioned outlines and sections.
- Retrieve only approved and permitted evidence.
- Keep verified facts, source facts, commitments, estimates, assumptions, and questions distinguishable.
- Check citations, unsupported claims, terminology, unresolved placeholders, and internal contradictions.
- Support Estonian and English deliverables.

### 14.5 Pricing

- Use decimal-safe deterministic calculations.
- Store currency, VAT treatment, units, quantities, rates, margin, contingency, assumptions, and calculation version.
- Separate technical effort assumptions from commercial approval.
- Require a reason and audit event for manual overrides.
- Invalidate approval when material pricing content changes.

### 14.6 Review and approval

- Support assignments, comments, review requests, blockers, approvals, rejection, and rework.
- Attach approval to exact content version and hash.
- Record actor, role, timestamp, decision, and rationale.
- Enforce server-side permissions.
- Invalidate approvals when affected content or source material changes.

### 14.7 Export and submission handoff

- Produce deterministic exports from approved content.
- Support required office and archive formats selected by tender needs and renderer capability.
- Generate a manifest containing filenames, hashes, versions, and generation time.
- Run completeness and consistency validation before final approval.
- Generate a submission checklist.
- Record manual submission evidence against the exact package hash.

---

## 15. Non-functional requirements

### 15.1 Security and privacy

- Deny access by default and enforce permissions server-side.
- Store secrets outside normal application data and never commit them.
- Use strong password hashing and secure browser sessions.
- Protect uploads, downloads, exports, and background jobs with the same authorization model as metadata.
- Redact secrets and sensitive content from logs.
- Treat all tender documents, web pages, emails, model output, and attachments as untrusted input.
- Prevent arbitrary model-directed tool use and arbitrary URL retrieval.

### 15.2 Auditability

The system must record sufficient metadata to reconstruct:

- source synchronization and imports;
- document versions and parsing;
- AI invocations and policy decisions;
- requirement edits;
- evidence changes;
- participation decisions;
- pricing changes and approvals;
- export generation and hashes;
- submission records;
- authentication and administrative security events.

Audit events must be append-oriented and protected from normal business-data editing.

### 15.3 Reliability and recoverability

- Core local services expose health and readiness states.
- Jobs are idempotent where feasible and use bounded retries.
- Source outages do not delete existing opportunities.
- Failed AI calls do not corrupt reviewed content.
- Backup and restore cover database, object storage, configuration references, and required metadata.
- A documented restore drill is required before pilot acceptance.

### 15.4 Performance

Pilot targets on the approved local reference machine:

- standard authenticated page navigation: p95 under 2 seconds excluding long-running jobs;
- opportunity filter/search response: p95 under 2 seconds for the pilot dataset;
- document upload acknowledgement: under 3 seconds before asynchronous processing begins;
- long-running parsing and AI work: asynchronous, cancellable where safe, and visibly tracked;
- no user request should remain open while waiting for an entire tender package to parse.

Exact reference hardware and dataset size are recorded during the platform sprint.

### 15.5 Accessibility and usability

- Keyboard-accessible primary workflows.
- Visible focus states and semantic labels.
- Status must not rely only on color.
- Errors must explain the problem and next action in Estonian.
- Destructive and binding actions require clear confirmation.
- AI-generated and human-approved states must be visually distinguishable.

### 15.6 Maintainability

- External systems use ports and adapters.
- Critical business rules are enforced in application/domain code, not only prompts.
- Configuration is typed and validated.
- Prompt assets, schemas, evaluation fixtures, migrations, and runbooks are versioned.
- Tests use mocks or fixtures by default instead of paid or live external services.

---

## 16. Pilot definition and measurable success criteria

### 16.1 Pilot scope

The MVP pilot will use:

- one Eventnexus OÜ local installation;
- at least one primary Bid Lead and one Authorized Business Decision-Maker;
- at least five representative IT tenders, including at least:
  - one Estonian-language tender;
  - one English-language or bilingual tender;
  - one multi-document tender;
  - one tender with an amendment or changed source package;
  - one tender that results in a justified `NO-GO` decision;
- a documented manual baseline for comparable work;
- real or sanitized company evidence approved for pilot use;
- manual final submission for any tender actually submitted.

The pilot may include historical tenders for repeatable evaluation, but at least one current real workflow should be used before declaring the MVP pilot-ready.

### 16.2 Success criteria

| Metric | Pilot success target | Measurement approach |
|---|---:|---|
| Opportunity recall | `>= 90%` | Relevant opportunities found by the system divided by relevant opportunities in a manually reviewed reference set for the same sources and period |
| Opportunity false-positive rate | `<= 30%` among items presented as strong matches | Strong matches later marked irrelevant divided by all reviewed strong matches |
| Mandatory requirement recall | `>= 95%` | Reviewed mandatory requirements captured by the system divided by the gold-standard requirements identified by human review |
| Citation correctness | `>= 98%` | Sampled material statements whose citation points to the correct document version and supporting location |
| Unsupported company claims in approved export | `0` | Human and automated review of every approved pilot export |
| Critical numeric/date transcription errors | `0` in approved export | Comparison of deadlines, prices, units, percentages, identifiers, and other critical fields against authoritative sources |
| Preparation-time reduction | `>= 40%` median reduction | Compare active human time from intake to submission-ready package against the documented baseline for comparable tenders |
| Human review-time reduction | `>= 25%` median reduction | Compare active review time for analysis and proposal sections against baseline |
| Export completeness | `100%` of approved pilot packages pass configured validation | Required-file, manifest, hash, placeholder, naming, totals, and checklist validation before approval |
| Approval integrity | `100%` | All final approvals refer to the exact exported versions; changed approved content invalidates approval |
| Submission control | `100%` human-controlled | Every real submission is completed or explicitly delegated by an authorized person; no autonomous portal submission occurs |
| Amendment safety | `100%` of pilot amendments produce a visible impact review | Verify changed source versions trigger stale-content warnings or invalidation where relevant |
| AI policy compliance | `100%` sampled invocations permitted and auditable | Review classification, redaction, model, purpose, token/cost metadata, and actor records |
| Critical/high security findings | `0` open at pilot release | Security review, dependency checks, authorization tests, and threat-model verification |
| Backup/restore | Successful restore within `4 hours`; no loss beyond the documented `24-hour` backup objective | Execute and document a restore drill on the pilot installation |
| Core workflow reliability | `>= 95%` successful completion without administrator intervention | Track ingestion, parsing, extraction, drafting, validation, and export jobs; exclude user-cancelled jobs |
| User usefulness rating | Average `>= 4.0/5` | Structured rating by primary and decision-maker users after each pilot tender |

S0-T04 will refine metric definitions, baseline collection, sample sizes, confidence treatment, and links to automated evaluation tasks. The targets above are binding provisional MVP criteria and cannot be replaced by subjective statements such as “works well.”

### 16.3 Pilot failure conditions

The pilot is not successful if any of the following occurs:

- the system performs or attempts autonomous official submission;
- an approved export contains a fabricated Eventnexus OÜ qualification, reference, certificate, person, customer, or financial claim;
- restricted data is sent to Gemini contrary to policy;
- a material source amendment remains invisible and causes stale approved content to be used;
- final pricing or package approval is inferred from AI output rather than recorded from an authorized user;
- the package cannot be tied to exact source, content, pricing, approval, and submission evidence versions;
- backup restoration cannot recover the pilot workspace;
- critical authorization failures remain unresolved.

---

## 17. Product analytics and operational measurements

The local installation should collect privacy-conscious operational metrics needed to evaluate the pilot:

- opportunities ingested, deduplicated, shortlisted, ignored, and converted to workspaces;
- match recommendations and human outcomes;
- documents, pages, parser status, OCR status, and processing duration;
- extracted requirements, human additions, corrections, and missed requirements;
- AI invocations by purpose, policy result, model, duration, tokens, estimated cost, and outcome;
- unsupported claims and citation validation findings;
- active human time where users explicitly start/stop or confirm work sessions;
- review requests, rework cycles, approval duration, and invalidations;
- export validation errors and package generations;
- source amendments and impact-review completion;
- system/job failures, retries, backup, and restore results.

Metrics must not store full confidential content merely for analytics. Sensitive metrics remain local and follow configured retention.

---

## 18. Assumptions and dependencies

### 18.1 Assumptions

- Eventnexus OÜ will identify at least one responsible Bid Lead and one Authorized Business Decision-Maker.
- Users will maintain approved company evidence and will not treat AI suggestions as facts.
- The local host has sufficient resources for Docker services and document processing.
- Internet connectivity is available for approved source APIs and Gemini when those functions are enabled.
- Official-source access and reuse conditions will be validated before production synchronization.
- Tender submission remains possible through the official human-operated channel even when integrations are unavailable.

### 18.2 Dependencies

- S0-T02: company-profile and evidence requirements;
- S0-T03: lifecycle states, transitions, permissions, and invalidation rules;
- S0-T04: detailed measurement specification;
- S0-T05 to S0-T08: RHR/TED integration and freshness decisions;
- S0-T09 to S0-T12: Gemini, classification, threat-model, and cost policies;
- S0-T13 to S0-T15: submission and legal-review boundaries;
- later architecture decisions for queue, object storage, pgvector, exports, backup, and deployment topology.

---

## 19. Open product decisions

These decisions are intentionally not guessed in this PRD and must be resolved in later tasks:

1. Exact Eventnexus OÜ company-profile fields and initial evidence set.
2. Which official RHR ingestion method is permitted and technically reliable.
3. Approved TED query and synchronization strategy.
4. Approved Gemini billing tier, project, data-processing terms, regions, models, and optional API features.
5. Document classes permitted for external AI.
6. Pilot reference hardware and expected maximum tender-package size.
7. Required first-release export templates and file formats for selected pilot tenders.
8. Whether email notifications are required in the MVP or local in-app alerts are sufficient.
9. Named people assigned to each decision and review role.
10. Retention periods for source data, documents, AI metadata, audit events, exports, and submission evidence.

Open decisions must not be silently implemented using unsafe defaults.

---

## 20. Acceptance traceability for S0-T01

| Acceptance requirement | PRD evidence | Status |
|---|---|---|
| Primary user is explicit | Section 5.1 identifies the Procurement and Bid Lead | Met |
| Decision-maker role is explicit | Sections 5.2 and 6 identify the Authorized Business Decision-Maker and exclusive authorities | Met |
| Users, jobs, pain points, success metrics, workflows, non-goals, and MVP boundaries are defined | Sections 3 through 16 | Met |
| Estonian-first requirements are defined | Section 12.1 and 12.2 | Met |
| English tender handling is defined | Sections 12.3 through 12.5 | Met |
| Every MVP feature maps to a user outcome | Section 10 maps F01–F24 to O1–O10 | Met |
| Autonomous submission is explicitly excluded | Sections 2, 9.11, 11.3, and 16 | Met |
| Measurable pilot success criteria exist | Section 16 | Met |

---

## 21. Approval

This document is complete for task S0-T01 but remains a product draft until approved by Eventnexus OÜ's product owner or Authorized Business Decision-Maker.

Approval should record:

- approver name;
- role;
- date;
- decision: `APPROVED`, `APPROVED_WITH_ACTIONS`, or `REJECTED`;
- required changes or conditions;
- approved document commit SHA.

Do not mark the Milestone M0 checklist item **Product requirements approved** as complete until this approval is recorded.