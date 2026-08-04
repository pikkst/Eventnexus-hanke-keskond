# Legal, Procurement, Privacy, Security, and Commercial Review Checkpoints

**Task:** S0-T15  
**Status:** Complete  
**Document owner:** Eventnexus OÜ Authorized Business Decision-Maker  
**Last updated:** 2026-08-04

## 1. Purpose and limitation

This document defines where qualified human review is required in EventNexus workflows. It does not provide legal advice and does not determine whether a particular tender, declaration, contract term, data transfer, or signature is legally valid.

AI may extract, summarize, compare, draft, and flag. AI must never be represented as a lawyer, procurement authority, data-protection officer, security certifier, accountant, auditor, authorized signatory, or official submission system.

## 2. Responsibility notice

The product must display a clear notice substantially equivalent to:

> EventNexus is an AI-assisted procurement preparation tool. AI-generated analysis and drafts may be incomplete or incorrect. The authorized Eventnexus OÜ reviewers remain responsible for verifying the current procurement documents, legal and eligibility conditions, company facts and evidence, price, commitments, declarations, data handling, signatures, final package, official submission, and receipt.

The default UI notice is in Estonian. English is available for bilingual workspaces. Final legal wording must be approved by the responsible human reviewer before production release.

## 3. Review roles

| Role | Review authority |
|---|---|
| `BID_LEAD` | process completeness, source/version readiness, requirement ownership, review coordination |
| `AUTHORIZED_BUSINESS_DECISION_MAKER` | GO/NO-GO, risk acceptance, binding business commitments, final package approval |
| `LEGAL_COMPLIANCE_REVIEWER` | exclusion/eligibility declarations, contract/legal terms, authority, disputes, regulatory obligations |
| `COMMERCIAL_REVIEWER` | price, margin, tax/VAT assumptions, guarantees, liability, payment, indexation, financial exposure |
| `TECHNICAL_REVIEWER` | feasibility, architecture, staffing, schedule, acceptance, support, technical commitments |
| `SECURITY_PRIVACY_REVIEWER` | security controls, personal data, confidentiality, external AI, data location, incident and subcontractor terms |
| `AUTHORIZED_SUBMITTER` | official portal verification, signing/identity action, submission and receipt evidence |
| `SYSTEM_ADMIN` | technical operation only; no implied authority to accept legal/commercial risk |

A small company may assign multiple roles to one person. The system must still record the specific role/authority used for every review and approval.

## 4. Risk levels

| Level | Meaning | Minimum consequence |
|---|---|---|
| `CRITICAL` | Could create invalid submission, unauthorized commitment/disclosure, fraudulent declaration, material loss, or missed deadline | Hard block until authorized resolution |
| `HIGH` | Material legal, commercial, security, privacy, eligibility, or delivery exposure | Required specialist/authorized review |
| `MEDIUM` | Significant ambiguity or manageable exposure | Named owner and documented decision |
| `LOW` | Minor wording or operational concern | Normal review workflow |

AI confidence must not reduce a required risk level.

## 5. Mandatory review checkpoints

### CP-01 — Opportunity qualification

**When:** Before final `GO`.

**Required reviewers:** Bid Lead and Authorized Business Decision-Maker; specialist reviewers when hard conditions are detected.

Check:

- procedure and selected lots;
- deadlines and source freshness;
- exclusion and eligibility conditions;
- required turnover, references, staff, certificates, insurance, guarantees, permissions, and registrations;
- capacity, partner dependency, conflicts of interest, sanctions/export-control concerns where relevant;
- tender/customer restrictions on AI, data location, confidentiality, subcontractors, or consortiums;
- strategic and financial exposure.

AI recommendation cannot perform the GO/NO-GO transition.

### CP-02 — Source and amendment review

**When:** After intake and after every material amendment/clarification.

**Required reviewer:** Bid Lead; specialist owners for affected areas.

Check:

- authoritative source and exact version;
- missing/inaccessible documents;
- changed deadline, scope, lot, evaluation, evidence, form, or contract term;
- invalidation of requirements, drafts, pricing, approvals, package, and submission readiness.

No “no change” conclusion may rely only on an AI summary; deterministic diff and source inspection are required.

### CP-03 — Requirement approval

**When:** Before compliance planning/drafting treats extracted requirements as authoritative.

**Required reviewer:** Bid Lead and relevant domain reviewer.

Check:

- mandatory/scored/informative/contractual distinction;
- exact citation;
- thresholds, dates, values, counts, formats, and signatures;
- conflicting or ambiguous source language;
- requested evidence and validation method;
- lot-specific applicability.

### CP-04 — Company fact and evidence approval

**When:** Before company claims are reusable or included in a tender.

**Required reviewer:** owner authorized for the fact/evidence domain.

Check:

- exact supported claim;
- evidence version, source location, issuer, validity, scope, and quality;
- customer/partner/staff permission;
- confidentiality and personal-data treatment;
- whether translation or summary changes meaning;
- tender-specific reuse restrictions.

AI cannot verify a fact.

### CP-05 — Research finding approval

**When:** Before public research is used in strategy or proposal claims.

**Required reviewer:** Bid Lead or relevant specialist.

Check:

- source authority, publisher, date, retrieval time, and relevance;
- speculation versus verified fact;
- corroboration for material conclusions;
- personal profiling and inappropriate inference;
- freshness requirements;
- whether finding is public external evidence rather than company evidence.

### CP-06 — Technical commitment review

**When:** Before technical sections are marked approved.

**Required reviewer:** Technical Reviewer.

Check:

- feasibility and actual capability;
- solution architecture and integrations;
- security, hosting, data location, environments, migration, testing, acceptance, support, SLA, documentation, and transition;
- staffing, effort, dependencies, assumptions, exclusions, and schedule;
- consistency with price and contract terms;
- tender-specific commitments versus non-binding explanation.

Every material technical claim about Eventnexus capability requires approved evidence.

### CP-07 — Privacy and personal-data review

**When:** Whenever the tender, proposed solution, staff evidence, external AI, or export involves personal data.

**Required reviewer:** Security/Privacy Reviewer; legal review where required.

Check:

- processing purpose, necessity, minimization, roles, data subjects, categories, sources, recipients, transfers, location, retention, deletion, security, incident response, subcontractors, and data-subject rights;
- whether Eventnexus is controller, processor, joint controller, or another role;
- tender-specific DPA/security annexes;
- staff CV/contact consent and permitted use;
- whether Gemini/external processing is allowed.

AI must not present a data-protection legal conclusion as approved.

### CP-08 — Security review

**When:** Tender requests security architecture, controls, certifications, compliance, hosting, access, logging, incident, business continuity, or testing commitments.

**Required reviewer:** Security Reviewer and Technical Reviewer.

Check:

- each claimed control is actually implemented/planned and accurately scoped;
- certifications/audits require evidence and valid scope;
- no generic boilerplate falsely claims production controls;
- customer/tender requirements map to concrete response/owner/evidence;
- residual risks, deviations, exceptions, and dependencies are explicit;
- penetration-testing, vulnerability, audit, backup, RTO/RPO, encryption, and incident claims are accurate.

### CP-09 — AI and external-processing review

**When:** Tender content or solution design involves Gemini, another AI provider, automated decision support, or restricted data.

**Required reviewer:** Security/Privacy Reviewer and Authorized Business Decision-Maker; legal review for contractual/data issues.

Check:

- approved provider/account/tier/features;
- classification and permitted use;
- data minimization, redaction, region/retention, logging, grounding, files/caches;
- human oversight and explainability;
- prohibited autonomous decisions/actions;
- cost and outage behavior;
- tender/customer AI restrictions;
- disclosure requirements.

### CP-10 — Commercial and pricing review

**When:** Before pricing approval and whenever price-affecting assumptions change.

**Required reviewer:** Commercial Reviewer and Authorized Business Decision-Maker.

Check:

- currency, VAT, units, quantities, rates, roles, effort, third-party costs, licenses, travel, contingency, margin, discounts, options, indexation, rounding, and tender form totals;
- fixed-price and schedule risk;
- guarantees, insurance, penalties, service credits, liability, IP, payment terms, retention, acceptance, warranty, and termination;
- consistency between technical commitments and cost;
- partner/subcontractor price and commitment evidence;
- negative/insufficient margin and unbounded exposure.

AI is not the calculator or pricing approver of record.

### CP-11 — Legal and contractual review

**When:** Before approving high-risk declarations or accepting material contract terms.

**Required reviewer:** Legal/Compliance Reviewer or qualified external counsel where Eventnexus policy requires it.

Triggers include:

- exclusion and eligibility self-declarations;
- authority/signing representations;
- consortium/joint liability;
- unlimited or disproportionate liability;
- indemnities;
- IP assignment/licensing and open-source restrictions;
- confidentiality and publicity;
- personal-data/DPA terms;
- security/audit obligations;
- sanctions/export control;
- insurance/guarantees;
- governing law, jurisdiction, dispute/appeal;
- termination, suspension, step-in, warranty, penalties;
- deviations from mandatory terms;
- use of third-party/subcontractor resources;
- conflicts of interest.

The product may flag clauses but must not state that legal review has occurred without an explicit human approval record.

### CP-12 — Declaration approval

**When:** Before any declaration is included or accepted in the final package/portal.

**Required reviewer:** Legal/Compliance Reviewer and Authorized Business Decision-Maker; Authorized Submitter verifies portal declaration.

Each declaration stores:

```text
declaration_id
source_requirement_id
exact_text_or_form_version
facts_and_evidence_dependencies
risk_level
reviewers
approved_version_hash
approved_at
valid_until_or_recheck_event
signing_or_submitter_authority
```

High-risk declarations require explicit approval and cannot use bulk “approve all” without displaying exact text and dependencies.

### CP-13 — Final readiness review

**When:** Before `APPROVED_FOR_EXPORT`.

**Required reviewers:** Bid Lead plus all configured technical, commercial, legal/compliance, security/privacy roles.

Check:

- current source and amendments;
- mandatory requirement coverage;
- approved facts/evidence;
- unresolved findings and accepted risks;
- technical/commercial/legal consistency;
- required forms/declarations/attachments;
- exact price version;
- placeholders, tracked changes, hidden metadata, filename/format constraints;
- authorized submitter assignment.

Readiness is deterministic and cannot be overridden by AI.

### CP-14 — Final package approval

**When:** After deterministic export and validation.

**Required reviewer:** Authorized Business Decision-Maker.

Check exact:

- package hash;
- selected lots;
- source notice versions;
- file manifest;
- technical/content approvals;
- pricing approval;
- declaration approvals;
- validation report;
- accepted exceptions;
- deadline and official destination.

Any material package/content change invalidates approval.

### CP-15 — Official submission review

**When:** During human official submission.

**Required reviewer:** Authorized Submitter.

Check:

- correct procedure/lot;
- official portal deadline/status;
- every uploaded file matches approved hash/version;
- price and portal fields match approved values;
- declarations and signatures are understood/authorized;
- successful official confirmation and receipt/reference.

EventNexus cannot perform this review automatically.

### CP-16 — Post-submission clarification, withdrawal, and result

**When:** Official follow-up occurs.

**Required reviewers:** Bid Lead, Authorized Business Decision-Maker, Authorized Submitter, and affected specialists.

Check:

- authoritative source/request;
- deadline and permitted response;
- whether answer changes price, scope, risk, declarations, or prior commitments;
- new approvals/package if required;
- official evidence of response, withdrawal, award, non-award, or cancellation.

## 6. High-risk declarations and actions

The following always require explicit human approval:

- no-exclusion-ground and eligibility declarations;
- legal authority and signing authority;
- turnover, financial capacity, tax status, insurance, guarantees;
- reference/customer permission and accuracy;
- named expert experience, availability, employment/commitment;
- consortium/partner/subcontractor commitment;
- data-protection and security compliance representations;
- certification/audit status;
- IP ownership/licensing and third-party rights;
- acceptance of liability, penalties, warranty, SLA, payment, audit, confidentiality, or termination terms;
- final price and discount;
- final package;
- submission, withdrawal, and clarification response.

## 7. Review exceptions

An exception must never be hidden. It requires:

```text
exception_id
checkpoint
requirement_or_finding
risk_level
reason
alternatives_considered
accepted_by
accepted_role
accepted_at
scope
expires_or_recheck_trigger
mitigation
```

Critical legal invalidity, unauthorized disclosure, missing authority, prohibited data transfer, missing mandatory submission item, or known stale package cannot be accepted merely as a convenience exception.

## 8. Required UI behavior

- AI-generated content is labeled `AI DRAFT` until reviewed.
- Approval state and reviewer role are visible.
- Source citations and exact versions are accessible.
- High-risk findings appear prominently and cannot be dismissed without reason.
- Legal-review-required items must not display “legally compliant” based on model output.
- Pricing and final package approvals are separate.
- A system administrator cannot approve business content by virtue of admin role.
- Bulk actions cannot bypass high-risk declaration review.
- Changed content visibly invalidates approvals.
- Official submission remains outside the product and human-controlled.

## 9. Export notices

Internal validation reports and checklists may include:

- “AI-assisted draft — human review required”;
- source freshness and version;
- unresolved/accepted risk summary;
- approval/version references;
- responsibility notice;
- statement that export is not proof of official submission.

Do not insert an internal AI disclaimer into customer-facing tender content unless appropriate and approved. Customer-facing disclosures must follow tender requirements, law, contract, and review decisions.

## 10. Audit requirements

Record:

- review assignment and due date;
- exact reviewed versions/hashes;
- findings and severity;
- approval/rejection/exception and rationale;
- role exercised;
- invalidation event and dependency;
- re-review completion;
- package and submission evidence.

Audit logs do not duplicate unnecessary confidential/legal content.

## 11. Legal escalation triggers

Escalate to qualified legal counsel when:

- internal reviewer lacks competence/authority;
- material terms are ambiguous or conflicting;
- a mandatory requirement appears unlawful/impossible or requires challenge/clarification;
- consortium/joint liability, major IP transfer, unlimited liability, unusual guarantee, sanctions/export-control, regulated-sector, cross-border data, or dispute/appeal issue exists;
- AI or data processing terms conflict with tender restrictions;
- Eventnexus plans a deviation/reservation;
- potential misrepresentation, conflict of interest, or prior incident is identified.

The system should support an escalation record but does not choose or contact counsel autonomously.

## 12. Acceptance traceability

- **UI and exports can display correct responsibility notices:** Sections 2, 8, and 9.
- **Legal review is not represented as AI capability:** Sections 1, 5, 8, and 11.
- **High-risk declarations require explicit approval:** Sections 5 CP-12 and 6.
