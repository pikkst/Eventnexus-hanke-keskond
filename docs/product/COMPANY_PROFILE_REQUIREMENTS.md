# EventNexus Hanke Keskond — Eventnexus OÜ Company Profile Requirements

**Document ID:** PRD-002  
**Task:** S0-T02  
**Status:** Requirements complete; company data population remains a later controlled activity  
**Organization:** Eventnexus OÜ  
**Primary market:** Estonia  
**Default language:** Estonian (`et-EE`)  
**Last updated:** 2026-08-04

---

## 1. Purpose

This document defines the information model required to represent Eventnexus OÜ inside EventNexus Hanke Keskond.

The company profile is the authoritative internal source used to:

- match procurement opportunities to Eventnexus OÜ capabilities and strategy;
- identify hard eligibility gaps and disqualifiers;
- support `GO`, `NO-GO`, and `NEEDS-MORE-INFORMATION` decisions;
- retrieve approved company facts and supporting evidence;
- prepare proposal sections without inventing qualifications or experience;
- assess capacity, delivery, commercial, security, and partner risks;
- populate tender forms and reusable content;
- track expiry, confidentiality, permissions, and evidence quality;
- explain every automated or AI-assisted fit score.

This document defines the required fields and governance rules. It does **not** assert that Eventnexus OÜ currently possesses any specific certification, reference, employee experience, turnover, insurance, partner agreement, or technical capability. Actual values must be entered and verified through approved evidence.

---

## 2. Product boundary

The company profile is a controlled knowledge and evidence system, not a marketing form and not an unrestricted AI memory.

The MVP must:

1. distinguish verified facts from preferences, evidence objects, derived assessments, and drafts;
2. preserve evidence provenance and validity;
3. prevent AI-generated content from becoming an approved fact automatically;
4. preserve historical versions and audit material changes;
5. restrict sensitive data by role, workspace, classification, and permitted use;
6. support Estonian and English variants without losing the authoritative source language;
7. make missing or expired evidence visible rather than silently assuming compliance;
8. support tender-specific use restrictions and partner permissions;
9. allow deterministic matching and explainable scoring;
10. export only facts and content approved for the target tender and audience.

The MVP does not attempt to replace Estonian official registers, accounting systems, HR systems, legal review, security certification bodies, or qualified procurement professionals.

---

## 3. Information categories

Every company-profile field or record must be assigned one primary information category.

| Code | Category | Meaning | May AI create it? | May it satisfy a tender requirement directly? |
|---|---|---|---|---|
| `FACT` | Company fact | A claim about Eventnexus OÜ, its people, projects, finances, policies, assets, permissions, or commitments | AI may propose an extraction, but a human must verify it | Only when verification and evidence rules are satisfied |
| `EVIDENCE` | Evidence object | A document, register extract, signed statement, certificate, contract excerpt, invoice summary, CV, policy, permission, or other source supporting one or more facts | AI may classify or extract metadata, but cannot approve it | Yes, when valid, permitted, scoped, and approved |
| `PREFERENCE` | Business preference | A strategic choice such as desired CPV areas, excluded work, target value, geography, margin floor, risk appetite, or preferred technologies | AI may suggest; an authorized human must set or approve | No; it influences matching and decisions |
| `DERIVED` | Derived value | A calculated score, status, warning, coverage ratio, confidence, capacity estimate, or recommendation generated from facts and preferences | Yes, through versioned deterministic or AI-assisted logic | No; it is decision support only |
| `CONTENT` | Approved content block | Reusable wording that may contain verified facts, standard methods, descriptions, or commitments | AI may draft a new version; human approval is required | Only after all embedded facts and commitments are validated |
| `DRAFT` | Unapproved working data | Imported, AI-generated, incomplete, or user-entered material awaiting review | Yes | No |

### 3.1 Non-negotiable category rules

- A `DERIVED` value must never overwrite its source `FACT` or `PREFERENCE` records.
- An `EVIDENCE` object is not itself proof of every claim contained in the file. Facts must link to specific supporting locations where practical.
- A `CONTENT` block must declare which facts, evidence records, commitments, languages, and approval version it depends on.
- A `DRAFT` record must never appear in a final proposal as an approved company fact without a review transition.
- AI confidence is not evidence quality and cannot change a fact to `VERIFIED`.

---

## 4. Verification, evidence, and validity model

Every factual field and factual record must use the following common model.

### 4.1 Fact record

Each fact must include:

```text
fact_id
organization_id
fact_type
value
unit_or_format
source_language
effective_from
effective_to
verification_status
validity_status
confidence_source
owner_role
reviewed_by
reviewed_at
last_checked_at
next_review_at
classification
permitted_uses
notes
version
created_at
updated_at
```

### 4.2 Verification status

| Status | Meaning | Permitted use |
|---|---|---|
| `UNVERIFIED` | Entered or extracted but not reviewed | Internal draft and gap identification only |
| `PENDING_EVIDENCE` | Believed to be correct but required evidence is missing | Cannot satisfy a tender requirement |
| `PENDING_REVIEW` | Evidence exists but human review is incomplete | Cannot be exported as approved fact |
| `VERIFIED` | Evidence, scope, and value were reviewed by an authorized user | May be used within evidence and permission limits |
| `REJECTED` | Evidence or claim was found incorrect, misleading, or unusable | Must not be used |
| `SUPERSEDED` | Replaced by a newer approved version | Historical use only |
| `REVOKED` | Previously approved but no longer permitted or trustworthy | Must not be used |

### 4.3 Validity status

Validity must be calculated from explicit dates and review rules, not guessed by AI.

| Status | Meaning |
|---|---|
| `NOT_YET_VALID` | Evidence or fact has a future effective date |
| `CURRENT` | Within the approved validity period |
| `EXPIRING` | Within a configurable warning period |
| `EXPIRED` | Past the validity date |
| `NO_EXPIRY_REVIEW_REQUIRED` | No fixed expiry, but periodic confirmation is required |
| `UNKNOWN` | Validity cannot yet be established |

Unknown validity must fail closed for mandatory eligibility claims when the tender requires current proof.

### 4.4 Evidence record

Each evidence object must include:

```text
evidence_id
organization_id
evidence_type
title
issuer_or_source
source_reference
source_url_if_permitted
original_document_version_id
source_location
file_hash_sha256
issue_date
effective_from
expiry_date
last_verified_at
next_review_at
verification_status
classification
contains_personal_data
contains_trade_secret
owner_role
permitted_uses
prohibited_uses
tender_or_customer_scope
partner_scope
language
translation_status
retention_rule
notes
created_at
updated_at
```

### 4.5 Evidence linkage

A fact-to-evidence link must include:

- exact fact and evidence versions;
- supporting page, section, cell, paragraph, register field, or excerpt where available;
- relationship type: `DIRECT`, `CORROBORATING`, `SELF_DECLARATION`, `THIRD_PARTY_CONFIRMATION`, or `DERIVED_FROM_SOURCE`;
- reviewer and review date;
- applicability scope;
- any limitations or contradictions.

### 4.6 Evidence quality levels

| Level | Description | Example use |
|---|---|---|
| `Q4_AUTHORITATIVE` | Official register, authority, accredited issuer, signed contract, audited statement, or equivalent primary evidence | Legal identity, certification, audited finances |
| `Q3_PRIMARY_INTERNAL` | Approved internal record with accountable owner and source | Capacity plan, policy version, approved rate card |
| `Q2_CORROBORATED` | Multiple consistent secondary sources or customer-approved material | Public reference description backed by several records |
| `Q1_SELF_ASSERTED` | Uncorroborated self-description or draft | Discovery and gap tracking only |
| `Q0_UNUSABLE` | Contradictory, expired, prohibited, unverifiable, or rejected | Must not support a claim |

Tender-specific rules may require a particular evidence type regardless of this quality level.

### 4.7 Fact approval rules

A fact may become `VERIFIED` only when:

1. at least one permitted evidence record is linked, unless the field is explicitly configured as human-attested internal operational data;
2. the evidence supports the exact value and scope;
3. the evidence is current or the lack of expiry is reviewed;
4. confidentiality and reuse permissions allow the intended use;
5. the reviewer has the required role;
6. conflicts are resolved or explicitly documented;
7. the event is written to the audit log.

---

## 5. Classification and sensitive-data guidance

The product must support the classifications defined below. Later task S0-T10 will refine the organization-wide policy, but the company profile must already be designed for these classes.

| Classification | Typical company-profile examples | Gemini default | Minimum access guidance |
|---|---|---|---|
| `PUBLIC` | Public website description, published reference, public register data, public certificate summary | Allowed only after policy check | Authenticated users or configured public export |
| `INTERNAL` | Service catalog, internal capability rating, standard methodology, non-sensitive capacity summary | Allowed only after policy check | Eventnexus internal users |
| `CONFIDENTIAL` | Rates, margin targets, non-public references, contracts, financial details, partner terms | Denied by default unless explicitly allowed and redacted | Restricted commercial/management roles |
| `PERSONAL_DATA` | CVs, names, contact details, availability, employment history, signatures | Denied by default; minimization and lawful-purpose controls required | Need-to-know roles and tender workspace scope |
| `RESTRICTED_NO_EXTERNAL_AI` | Identity secrets, signing material, highly restricted customer data, protected credentials, prohibited contract content | Always blocked from external AI | Explicitly authorized local-only access |

### 5.1 Field-level sensitivity rules

- A record inherits the most restrictive classification of its linked values and evidence unless an approved redacted derivative is created.
- Public availability does not automatically authorize unrestricted reuse in a tender.
- Staff and reference contact details must be minimized and displayed only when necessary.
- Exact salary, personal identification code, home address, health information, private contact data, authentication secrets, and signing secrets are not normal company-profile fields.
- Financial statements, insurance documents, contracts, partner agreements, and customer confirmations are at least `CONFIDENTIAL` unless an authorized reviewer classifies a specific derivative as less restrictive.
- AI prompts, chunks, embeddings, generated responses, exports, and logs must retain or increase the source classification; they must not silently downgrade it.

---

## 6. Required versus optional data

The MVP distinguishes three requirement levels.

| Level | Meaning |
|---|---|
| `MVP_REQUIRED` | Required before the company profile can be considered operational for pilot matching and proposal drafting |
| `CONDITIONAL_REQUIRED` | Required when Eventnexus OÜ wants to pursue a tender that depends on the field |
| `OPTIONAL` | Useful for better scoring, automation, analytics, or later maturity but not required for the first pilot |

An installation may start before all `MVP_REQUIRED` facts are verified, but the UI must show profile readiness and must block unsupported claims.

### 6.1 MVP readiness minimum

The profile is minimally ready for a pilot only when it contains:

- verified legal identity and organization identifiers;
- named profile owner and authorized business decision-maker;
- at least one approved service category and capability;
- at least one configured CPV include rule or manually approved search profile;
- delivery geography and supported working languages;
- explicit exclusions and prohibited opportunity types;
- current capacity statement with owner and review date;
- risk-preference baseline;
- at least one approved reference or an explicit `NO_APPROVED_REFERENCES` status;
- at least one approved reusable company-description block;
- data classification and external-AI policy defaults;
- evidence readiness warnings for missing finance, staff, certification, partner, or reference data.

---

## 7. Legal identity and organization details

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Registered legal name | `FACT` | `MVP_REQUIRED` | Authoritative register extract; review on change or at least annually | `PUBLIC` |
| Registry code | `FACT` | `MVP_REQUIRED` | Authoritative register extract; no normal expiry, annual review | `PUBLIC` |
| Legal form | `FACT` | `MVP_REQUIRED` | Authoritative register extract; annual review | `PUBLIC` |
| Registered address | `FACT` | `MVP_REQUIRED` | Authoritative register extract; review on change | `PUBLIC` or `INTERNAL` according to source |
| Country of registration | `FACT` | `MVP_REQUIRED` | Authoritative register extract | `PUBLIC` |
| VAT registration number and status | `FACT` | `CONDITIONAL_REQUIRED` | Tax/register evidence; current-status check before use | `CONFIDENTIAL` by default |
| Establishment date | `FACT` | `OPTIONAL` | Authoritative register extract | `PUBLIC` |
| Economic activity codes | `FACT` | `OPTIONAL` | Register extract; annual review | `PUBLIC` |
| Public website domains | `FACT` | `MVP_REQUIRED` | Domain/website ownership review; annual review | `PUBLIC` |
| Official company email | `FACT` | `MVP_REQUIRED` | Human verification; review on change | `INTERNAL` or `PUBLIC` |
| Official phone number | `FACT` | `OPTIONAL` | Human verification; review on change | `INTERNAL` or `PUBLIC` |
| Bank/account details | `FACT` | `CONDITIONAL_REQUIRED` | Controlled financial evidence; verify before each binding use | `RESTRICTED_NO_EXTERNAL_AI` |
| Beneficial-owner details | `FACT` | `CONDITIONAL_REQUIRED` | Authoritative source and lawful-purpose review | `PERSONAL_DATA` |
| Authorized representatives | `FACT` | `MVP_REQUIRED` | Register, board decision, or signed authorization; expiry/revocation tracked | `PERSONAL_DATA` |
| Signing authority scope | `FACT` | `CONDITIONAL_REQUIRED` | Register or authorization document; check before submission | `CONFIDENTIAL` / `PERSONAL_DATA` |

The product must never infer signing authority from a user role alone.

---

## 8. Profile ownership, contacts, and decision roles

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Company-profile owner | `FACT` | `MVP_REQUIRED` | Internal appointment; review on role change | `INTERNAL` / `PERSONAL_DATA` |
| Procurement/Bid Lead | `FACT` | `MVP_REQUIRED` | Internal appointment; review on role change | `INTERNAL` / `PERSONAL_DATA` |
| Authorized Business Decision-Maker | `FACT` | `MVP_REQUIRED` | Internal authorization and legal-authority check where relevant | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Commercial approver | `FACT` | `CONDITIONAL_REQUIRED` | Internal authorization; review on role change | `INTERNAL` / `PERSONAL_DATA` |
| Security/privacy reviewer | `FACT` | `CONDITIONAL_REQUIRED` | Internal appointment or external service agreement | `INTERNAL` / `PERSONAL_DATA` |
| Legal reviewer | `FACT` | `CONDITIONAL_REQUIRED` | Internal appointment or external service agreement | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Authorized submitter | `FACT` | `CONDITIONAL_REQUIRED` | Tender-specific assignment; validity limited to assignment | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Public tender contact | `FACT` | `OPTIONAL` | Person approval and contact verification | `PERSONAL_DATA` |
| Internal escalation contacts | `FACT` | `OPTIONAL` | Internal review | `INTERNAL` / `PERSONAL_DATA` |

Permissions and legal authority must be modeled separately. A system permission does not prove legal signing authority, and legal authority does not automatically grant all system-administration permissions.

---

## 9. Service categories and capabilities

Capabilities describe what Eventnexus OÜ can credibly deliver. Each capability must be a versioned record rather than free-form marketing text.

### 9.1 Capability fields

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Capability name | `FACT` | `MVP_REQUIRED` | Approved internal service catalog and supporting evidence | `INTERNAL` |
| Capability description | `CONTENT` | `MVP_REQUIRED` | Human-approved wording linked to evidence | `INTERNAL` |
| Service category | `FACT` | `MVP_REQUIRED` | Approved taxonomy assignment | `INTERNAL` |
| Delivery type | `FACT` | `MVP_REQUIRED` | Internal operating evidence; review annually | `INTERNAL` |
| Lifecycle coverage | `FACT` | `MVP_REQUIRED` | Approved process/service evidence | `INTERNAL` |
| Maturity level | `DERIVED` or reviewed `FACT` | `OPTIONAL` | Method and evidence required; periodic review | `INTERNAL` |
| Proficiency level | `DERIVED` | `OPTIONAL` | Calculated from staff, references, recency, and evidence | `INTERNAL` |
| Strategic priority | `PREFERENCE` | `MVP_REQUIRED` | Approved by business decision-maker; review quarterly or on strategy change | `CONFIDENTIAL` |
| Supported engagement models | `FACT` | `MVP_REQUIRED` | Approved operating model | `INTERNAL` |
| Supported delivery locations | `FACT` | `MVP_REQUIRED` | Approved operating statement | `INTERNAL` |
| Minimum/maximum practical project size | `PREFERENCE` | `OPTIONAL` | Commercial/operational approval; periodic review | `CONFIDENTIAL` |
| Known limitations | `FACT` | `MVP_REQUIRED` | Capability owner review | `CONFIDENTIAL` |
| Required partner capability | `PREFERENCE` | `OPTIONAL` | Business review | `CONFIDENTIAL` |
| Evidence links | `EVIDENCE` links | `MVP_REQUIRED` | At least one link or explicit unsupported status | Inherited |
| Last review / next review | `FACT` | `MVP_REQUIRED` | System metadata | `INTERNAL` |

### 9.2 Suggested service taxonomy

The taxonomy must be configurable. Initial categories may include:

- software architecture and technical analysis;
- custom software development;
- web and API development;
- AI/LLM integration and agent workflows;
- local-LLM and privacy-focused AI solutions;
- data integration and automation;
- cloud/API integration where permitted;
- DevOps, Docker, deployment, and observability;
- maintenance, support, and incident response;
- testing and quality assurance;
- technical documentation and training;
- security and privacy engineering capabilities supported by actual evidence;
- project management and delivery governance.

These category names are requirements candidates, not assertions that all are currently verified Eventnexus OÜ capabilities.

---

## 10. Technologies and technical competencies

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Technology name and normalized identifier | `FACT` | `MVP_REQUIRED` for core technologies | Approved capability/staff/reference evidence | `INTERNAL` |
| Technology category | `FACT` | `MVP_REQUIRED` | Controlled taxonomy | `INTERNAL` |
| Supported versions | `FACT` | `OPTIONAL` | Recent project, training, or implementation evidence; review for staleness | `INTERNAL` |
| Competency level | `DERIVED` | `OPTIONAL` | Versioned calculation from evidence, staff, and project recency | `INTERNAL` |
| Last used date | `FACT` | `CONDITIONAL_REQUIRED` | Reference or staff evidence | `CONFIDENTIAL` |
| Years of experience | `DERIVED` or carefully verified `FACT` | `CONDITIONAL_REQUIRED` | Calculated from non-overlapping evidence periods; human review | `CONFIDENTIAL` |
| Production-use evidence | `EVIDENCE` link | `CONDITIONAL_REQUIRED` | Reference, deployment, contract, or approved internal evidence | Inherited |
| Certification/training evidence | `EVIDENCE` link | `OPTIONAL` | Certificate validity and person scope | Inherited |
| Preferred / accepted / excluded status | `PREFERENCE` | `MVP_REQUIRED` | Technical/business approval; review periodically | `INTERNAL` |
| Delivery constraints | `FACT` | `OPTIONAL` | Technical review | `CONFIDENTIAL` |

The system must distinguish organization capability from one person's experience. A staff skill does not automatically prove company-level delivery capability, and company marketing text does not prove a named person's experience.

---

## 11. Industries, customer types, and domain experience

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Industry/domain name | `FACT` | `MVP_REQUIRED` when used in matching | Linked reference or approved experience evidence | `INTERNAL` |
| Experience scope | `FACT` | `MVP_REQUIRED` | Evidence-linked description | `CONFIDENTIAL` unless public |
| Customer type | `FACT` | `OPTIONAL` | Reference evidence | `INTERNAL` |
| Public/private sector experience | `FACT` | `OPTIONAL` | Reference evidence | `INTERNAL` |
| Regulatory familiarity | `FACT` | `CONDITIONAL_REQUIRED` | Specific training/project/policy evidence | `CONFIDENTIAL` |
| Strategic interest | `PREFERENCE` | `MVP_REQUIRED` | Business-owner approval | `CONFIDENTIAL` |
| Excluded industries | `PREFERENCE` | `MVP_REQUIRED` | Business/legal/ethical decision | `CONFIDENTIAL` |
| Domain fit score | `DERIVED` | `OPTIONAL` | Versioned scoring logic | `INTERNAL` |

Generic claims such as “strong public-sector experience” must not be produced unless supported by defined and approved evidence.

---

## 12. CPV interests and opportunity-search preferences

### 12.1 CPV interest record

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| CPV code | `PREFERENCE` | `MVP_REQUIRED` | Selected from controlled taxonomy | `INTERNAL` |
| CPV label and language | `FACT` from taxonomy | `MVP_REQUIRED` | Versioned official taxonomy source | `PUBLIC` |
| Include/exclude action | `PREFERENCE` | `MVP_REQUIRED` | Business approval | `CONFIDENTIAL` |
| Weight | `PREFERENCE` | `MVP_REQUIRED` | Business approval; versioned | `CONFIDENTIAL` |
| Apply to child/parent codes | `PREFERENCE` | `MVP_REQUIRED` | Deterministic configuration | `INTERNAL` |
| Keywords and synonyms | `PREFERENCE` | `MVP_REQUIRED` | Human-approved, language-specific | `INTERNAL` |
| Negative keywords | `PREFERENCE` | `OPTIONAL` | Human-approved | `INTERNAL` |
| Minimum/maximum contract value | `PREFERENCE` | `OPTIONAL` | Commercial approval | `CONFIDENTIAL` |
| Buyer/geography preferences | `PREFERENCE` | `OPTIONAL` | Business approval | `CONFIDENTIAL` |
| Deadline lead-time threshold | `PREFERENCE` | `MVP_REQUIRED` | Operational approval | `CONFIDENTIAL` |
| Strategic priority and rationale | `PREFERENCE` | `MVP_REQUIRED` | Decision-maker approval | `CONFIDENTIAL` |
| Match score | `DERIVED` | `OPTIONAL` | Versioned deterministic scoring | `INTERNAL` |

Hard exclusions must be evaluated before weighted scoring and must remain visible in explanations.

---

## 13. Reference projects and customer evidence

Reference projects are a high-risk factual area and require explicit evidence and reuse permissions.

### 13.1 Reference-project fields

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Reference title | `FACT` | `MVP_REQUIRED` when a reference exists | Contract/project evidence | `CONFIDENTIAL` unless public |
| Customer legal/display name | `FACT` | `CONDITIONAL_REQUIRED` | Contract, public source, or customer approval | `CONFIDENTIAL` unless public |
| Anonymized customer label | `CONTENT` | `OPTIONAL` | Approved derivation from protected record | `INTERNAL` or `PUBLIC` |
| Project scope | `FACT` | `MVP_REQUIRED` | Contract, acceptance, or approved project record | `CONFIDENTIAL` |
| Eventnexus role | `FACT` | `MVP_REQUIRED` | Contract, statement of work, or approved owner confirmation | `CONFIDENTIAL` |
| Start/end dates | `FACT` | `MVP_REQUIRED` | Project evidence; no silent date inference | `CONFIDENTIAL` |
| Contract/value range | `FACT` | `CONDITIONAL_REQUIRED` | Contract or finance evidence; currency and VAT basis explicit | `CONFIDENTIAL` |
| Technologies | `FACT` | `MVP_REQUIRED` | Project evidence | `CONFIDENTIAL` unless public |
| Team size and roles | `FACT` | `OPTIONAL` | Project/staff evidence | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Deliverables | `FACT` | `MVP_REQUIRED` | Acceptance/project evidence | `CONFIDENTIAL` |
| Measured outcomes | `FACT` | `CONDITIONAL_REQUIRED` | Customer-approved or verifiable measurement evidence | `CONFIDENTIAL` unless public |
| Acceptance status | `FACT` | `CONDITIONAL_REQUIRED` | Acceptance document or equivalent | `CONFIDENTIAL` |
| Customer contact | `FACT` | `OPTIONAL` | Explicit contact and reuse permission | `PERSONAL_DATA` |
| Contact permission expiry | `FACT` | `CONDITIONAL_REQUIRED` | Customer permission record | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Public-use permission | `FACT` | `MVP_REQUIRED` | Contract clause, written customer permission, or public source | `CONFIDENTIAL` |
| Tender-use permission | `FACT` | `MVP_REQUIRED` | Explicit permission scope and expiry | `CONFIDENTIAL` |
| NDA/reuse restrictions | `FACT` | `MVP_REQUIRED` | Contract or legal review | `RESTRICTED_NO_EXTERNAL_AI` or `CONFIDENTIAL` |
| Evidence links | `EVIDENCE` links | `MVP_REQUIRED` | Direct evidence and source locations | Inherited |
| Reference readiness | `DERIVED` | `MVP_REQUIRED` | Deterministic result from evidence, validity, and permission | `INTERNAL` |

A reference must be blocked from proposal use when the permission, scope, evidence, customer identity, project dates, or required outcomes are missing or expired.

---

## 14. Staff, experts, and CV evidence

### 14.1 Staff-profile fields

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Person identifier | `FACT` | `CONDITIONAL_REQUIRED` | HR/contractor record; active relationship checked | `PERSONAL_DATA` |
| Approved display name | `FACT` | `CONDITIONAL_REQUIRED` | Person approval | `PERSONAL_DATA` |
| Relationship type | `FACT` | `CONDITIONAL_REQUIRED` | Employment/contract evidence | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Current role | `FACT` | `CONDITIONAL_REQUIRED` | HR/contract evidence; review on change | `PERSONAL_DATA` |
| Proposed tender role | `PREFERENCE` | `CONDITIONAL_REQUIRED` | Tender-specific human assignment | `PERSONAL_DATA` |
| Skills and technologies | `FACT` | `CONDITIONAL_REQUIRED` | CV, project, certificate, or approved assessment evidence | `PERSONAL_DATA` |
| Experience periods | `FACT` | `CONDITIONAL_REQUIRED` | CV/project evidence | `PERSONAL_DATA` |
| Derived years of experience | `DERIVED` | `OPTIONAL` | Non-overlapping period calculation; reviewed | `PERSONAL_DATA` |
| Education | `FACT` | `CONDITIONAL_REQUIRED` | Diploma or approved verification | `PERSONAL_DATA` |
| Certifications | `FACT` + `EVIDENCE` | `CONDITIONAL_REQUIRED` | Certificate, issuer, scope, and expiry | `PERSONAL_DATA` |
| Languages and proficiency | `FACT` | `CONDITIONAL_REQUIRED` | Approved declaration or certificate where required | `PERSONAL_DATA` |
| Availability | `FACT` or `PREFERENCE` | `CONDITIONAL_REQUIRED` | Capacity owner confirmation; short review interval | `CONFIDENTIAL` / `PERSONAL_DATA` |
| Location/travel constraints | `PREFERENCE` | `OPTIONAL` | Person/manager approval | `PERSONAL_DATA` |
| CV content blocks | `CONTENT` | `CONDITIONAL_REQUIRED` | Person and company approval | `PERSONAL_DATA` |
| Use-consent scope | `FACT` | `MVP_REQUIRED` before use | Explicit internal consent/legal basis and tender scope | `PERSONAL_DATA` |
| Evidence links | `EVIDENCE` links | `CONDITIONAL_REQUIRED` | Direct evidence | Inherited |

The system must not infer a person's age, identity code, nationality, availability, employment status, years of experience, or certification from incomplete documents. Personal data must be minimized in AI calls and exports.

---

## 15. Certifications, policies, insurance, and organizational evidence

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Certificate/policy name | `FACT` | `CONDITIONAL_REQUIRED` | Issued certificate or approved policy document | `CONFIDENTIAL` unless public |
| Issuer/owner | `FACT` | `CONDITIONAL_REQUIRED` | Source document | `CONFIDENTIAL` |
| Identifier | `FACT` | `CONDITIONAL_REQUIRED` | Source document | `CONFIDENTIAL` |
| Scope | `FACT` | `CONDITIONAL_REQUIRED` | Exact source wording | `CONFIDENTIAL` |
| Issue/effective date | `FACT` | `CONDITIONAL_REQUIRED` | Source document | `CONFIDENTIAL` |
| Expiry/review date | `FACT` | `CONDITIONAL_REQUIRED` | Source document or policy review cycle | `CONFIDENTIAL` |
| Verification URL/method | `FACT` | `OPTIONAL` | Issuer-supported verification | `CONFIDENTIAL` or `PUBLIC` |
| Applicable legal entity/sites/services | `FACT` | `CONDITIONAL_REQUIRED` | Exact scope evidence | `CONFIDENTIAL` |
| Current status | `DERIVED` | `MVP_REQUIRED` when record exists | Deterministic validity calculation | `INTERNAL` |
| Evidence file/version | `EVIDENCE` | `CONDITIONAL_REQUIRED` | Immutable source version | Inherited |
| Tender-use restrictions | `FACT` | `MVP_REQUIRED` | Legal/compliance review | `CONFIDENTIAL` |

The product must not describe internal policies as independently certified unless authoritative evidence proves certification.

---

## 16. Financial and economic standing

Financial data must use decimal values, explicit currency, reporting period, accounting basis, VAT treatment where relevant, and source evidence.

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Annual turnover by period | `FACT` | `CONDITIONAL_REQUIRED` | Approved annual report, accounting evidence, or audited statement; period-specific | `CONFIDENTIAL` |
| Relevant-service turnover | `FACT` | `CONDITIONAL_REQUIRED` | Approved accounting calculation and methodology | `CONFIDENTIAL` |
| Balance-sheet totals | `FACT` | `OPTIONAL` | Approved financial statement | `CONFIDENTIAL` |
| Profit/loss values | `FACT` | `OPTIONAL` | Approved financial statement | `CONFIDENTIAL` |
| Tax-debt/compliance status | `FACT` | `CONDITIONAL_REQUIRED` | Current official evidence; short validity | `CONFIDENTIAL` |
| Credit/solvency evidence | `FACT` | `OPTIONAL` | Approved third-party source and date | `CONFIDENTIAL` |
| Professional liability insurance | `FACT` | `CONDITIONAL_REQUIRED` | Policy document, coverage, insured entity, territory, and expiry | `CONFIDENTIAL` |
| Other insurance | `FACT` | `OPTIONAL` | Policy evidence | `CONFIDENTIAL` |
| Minimum acceptable contract value | `PREFERENCE` | `OPTIONAL` | Commercial approval | `CONFIDENTIAL` |
| Maximum exposure/value | `PREFERENCE` | `MVP_REQUIRED` | Decision-maker approval and review cycle | `CONFIDENTIAL` |
| Margin floor | `PREFERENCE` | `MVP_REQUIRED` | Authorized commercial approval | `RESTRICTED_NO_EXTERNAL_AI` or `CONFIDENTIAL` |
| Payment-term tolerance | `PREFERENCE` | `OPTIONAL` | Commercial approval | `CONFIDENTIAL` |
| Guarantee/security capacity | `FACT` | `CONDITIONAL_REQUIRED` | Bank/finance evidence and current approval | `RESTRICTED_NO_EXTERNAL_AI` |
| Financial eligibility result | `DERIVED` | `CONDITIONAL_REQUIRED` | Tender rule plus verified facts; versioned calculation | `CONFIDENTIAL` |

Financial values must never be estimated by AI and presented as facts. Missing values must remain missing.

---

## 17. Partners, subcontractors, and consortium members

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Partner legal identity | `FACT` | `CONDITIONAL_REQUIRED` | Register/partner evidence | `CONFIDENTIAL` unless public |
| Relationship type | `FACT` | `CONDITIONAL_REQUIRED` | Agreement or approved relationship record | `CONFIDENTIAL` |
| Capabilities provided | `FACT` | `CONDITIONAL_REQUIRED` | Partner-approved evidence | `CONFIDENTIAL` |
| Geographic/market scope | `FACT` | `OPTIONAL` | Partner evidence | `CONFIDENTIAL` |
| Availability/commitment | `FACT` | `CONDITIONAL_REQUIRED` | Tender-specific letter or written confirmation; short validity | `CONFIDENTIAL` |
| Evidence-use permission | `FACT` | `MVP_REQUIRED` before use | Written partner permission with scope and expiry | `CONFIDENTIAL` |
| Confidentiality restrictions | `FACT` | `MVP_REQUIRED` | Agreement/legal review | `RESTRICTED_NO_EXTERNAL_AI` or `CONFIDENTIAL` |
| Contact persons | `FACT` | `OPTIONAL` | Permission and current contact verification | `PERSONAL_DATA` |
| Commercial terms | `FACT` | `OPTIONAL` | Agreement/quotation; tender-specific validity | `RESTRICTED_NO_EXTERNAL_AI` |
| Dependency risk | `DERIVED` | `OPTIONAL` | Versioned deterministic/human-reviewed assessment | `CONFIDENTIAL` |
| Preferred partner category | `PREFERENCE` | `OPTIONAL` | Business approval | `CONFIDENTIAL` |

Partner facts must never be mixed with Eventnexus OÜ facts. Every proposal claim must identify whose capability or evidence it relies on.

---

## 18. Exclusions and hard disqualifiers

Exclusions are business rules evaluated before weighted opportunity scoring.

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Excluded CPV codes | `PREFERENCE` | `MVP_REQUIRED` | Authorized business decision | `CONFIDENTIAL` |
| Excluded technologies | `PREFERENCE` | `MVP_REQUIRED` | Technical/business approval | `CONFIDENTIAL` |
| Excluded industries/use cases | `PREFERENCE` | `MVP_REQUIRED` | Legal/ethical/business approval | `CONFIDENTIAL` |
| Unsupported delivery locations | `FACT` or `PREFERENCE` | `MVP_REQUIRED` | Operational/business approval | `INTERNAL` |
| Minimum preparation lead time | `PREFERENCE` | `MVP_REQUIRED` | Bid Lead approval | `CONFIDENTIAL` |
| Maximum liability/penalty tolerance | `PREFERENCE` | `OPTIONAL` | Legal/commercial approval | `RESTRICTED_NO_EXTERNAL_AI` |
| Prohibited contract terms | `PREFERENCE` | `OPTIONAL` | Legal approval | `RESTRICTED_NO_EXTERNAL_AI` |
| Missing mandatory capability rule | `DERIVED` | `MVP_REQUIRED` | Deterministic comparison | `INTERNAL` |
| Missing mandatory evidence rule | `DERIVED` | `MVP_REQUIRED` | Deterministic comparison | `INTERNAL` |
| Conflict-of-interest restriction | `FACT` | `CONDITIONAL_REQUIRED` | Legal/management evidence and tender scope | `RESTRICTED_NO_EXTERNAL_AI` |
| Sanctions/exclusion status | `FACT` | `CONDITIONAL_REQUIRED` | Current authoritative check | `CONFIDENTIAL` |
| Hard-disqualifier result | `DERIVED` | `MVP_REQUIRED` | Versioned deterministic rules and source facts | `CONFIDENTIAL` |

A hard disqualifier must not be hidden inside a positive aggregate score. The user must see the rule, source, evidence status, and override authority. Overrides require rationale and audit, and some legal exclusions must not be overrideable.

---

## 19. Capacity and availability

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Capacity period | `FACT` | `MVP_REQUIRED` | Explicit date range | `CONFIDENTIAL` |
| Available role types | `FACT` | `MVP_REQUIRED` | Resource/capacity owner confirmation | `CONFIDENTIAL` |
| Available effort by role | `FACT` | `MVP_REQUIRED` | Internal capacity plan; frequent review | `CONFIDENTIAL` |
| Confirmed commitments | `FACT` | `MVP_REQUIRED` | Project plan or management record | `RESTRICTED_NO_EXTERNAL_AI` or `CONFIDENTIAL` |
| Tentative pipeline load | `FACT` or `DERIVED` | `OPTIONAL` | Approved forecast and method | `CONFIDENTIAL` |
| Earliest start date | `FACT` | `MVP_REQUIRED` | Capacity owner confirmation; short validity | `CONFIDENTIAL` |
| Maximum parallel projects | `PREFERENCE` | `OPTIONAL` | Management approval | `CONFIDENTIAL` |
| Required hiring/partner assumption | `PREFERENCE` | `OPTIONAL` | Management approval | `CONFIDENTIAL` |
| Delivery-mode constraints | `FACT` | `MVP_REQUIRED` | Operational review | `INTERNAL` |
| Capacity confidence | `DERIVED` | `OPTIONAL` | Versioned method based on data freshness | `INTERNAL` |
| Capacity risk | `DERIVED` | `MVP_REQUIRED` | Deterministic/human-reviewed assessment | `CONFIDENTIAL` |

Capacity data must have short review intervals. Stale capacity must be treated as unknown, not available.

---

## 20. Risk appetite and commercial preferences

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Overall risk posture | `PREFERENCE` | `MVP_REQUIRED` | Business decision-maker approval | `CONFIDENTIAL` |
| Technical novelty tolerance | `PREFERENCE` | `MVP_REQUIRED` | Technical/business approval | `CONFIDENTIAL` |
| Fixed-price risk tolerance | `PREFERENCE` | `MVP_REQUIRED` | Commercial approval | `CONFIDENTIAL` |
| Schedule compression tolerance | `PREFERENCE` | `MVP_REQUIRED` | Delivery approval | `CONFIDENTIAL` |
| Subcontractor dependency tolerance | `PREFERENCE` | `OPTIONAL` | Business approval | `CONFIDENTIAL` |
| Data sensitivity tolerance | `PREFERENCE` | `MVP_REQUIRED` | Security/privacy approval | `CONFIDENTIAL` |
| On-site/travel tolerance | `PREFERENCE` | `OPTIONAL` | Operational approval | `INTERNAL` |
| Warranty/support tolerance | `PREFERENCE` | `OPTIONAL` | Delivery/commercial approval | `CONFIDENTIAL` |
| Payment-delay tolerance | `PREFERENCE` | `OPTIONAL` | Commercial approval | `CONFIDENTIAL` |
| Liability/indemnity tolerance | `PREFERENCE` | `OPTIONAL` | Legal/commercial approval | `RESTRICTED_NO_EXTERNAL_AI` |
| IP ownership/licensing constraints | `PREFERENCE` | `MVP_REQUIRED` | Legal/business approval | `RESTRICTED_NO_EXTERNAL_AI` |
| Security/compliance minimums | `PREFERENCE` | `MVP_REQUIRED` | Security/legal approval | `CONFIDENTIAL` |
| Risk score | `DERIVED` | `OPTIONAL` | Versioned scoring model with factor breakdown | `CONFIDENTIAL` |

Risk scores must show individual factors, source values, missing inputs, model/rule version, and the human decision. They cannot make the final participation decision.

---

## 21. Languages, geography, and delivery model

| Field | Category | Requirement | Evidence and validity | Default classification |
|---|---|---|---|---|
| Working languages | `FACT` | `MVP_REQUIRED` | Staff/operating evidence | `INTERNAL` |
| Proposal-writing languages | `FACT` | `MVP_REQUIRED` | Approved operating capability | `INTERNAL` |
| Translation-review capability | `FACT` | `CONDITIONAL_REQUIRED` | Staff/partner evidence | `CONFIDENTIAL` |
| Supported countries/regions | `FACT` or `PREFERENCE` | `MVP_REQUIRED` | Business/operational approval | `INTERNAL` |
| Remote/on-site/hybrid delivery | `FACT` | `MVP_REQUIRED` | Approved operating model | `INTERNAL` |
| Travel constraints | `PREFERENCE` | `OPTIONAL` | Management approval | `CONFIDENTIAL` |
| Time-zone support | `FACT` | `OPTIONAL` | Operating evidence | `INTERNAL` |
| Support hours | `FACT` or `PREFERENCE` | `OPTIONAL` | Service-owner approval | `INTERNAL` |
| Data-location constraints | `PREFERENCE` | `MVP_REQUIRED` | Security/legal approval | `CONFIDENTIAL` |
| Cloud/local deployment constraints | `FACT` or `PREFERENCE` | `MVP_REQUIRED` | Technical/security approval | `CONFIDENTIAL` |

Estonian is the default internal product language. English variants must link to the same underlying fact/evidence version and record whether the translation is machine-assisted, human-reviewed, or legally reviewed.

---

## 22. Approved content blocks

The profile must support reusable, versioned content without treating prose as independent truth.

Suggested block types:

- short and long company description;
- service-category descriptions;
- technical capability summaries;
- delivery methodology;
- project management approach;
- quality assurance approach;
- security and privacy approach;
- support and maintenance model;
- sustainability and accessibility statements;
- standard assumptions and exclusions;
- reference summaries;
- staff/CV summaries;
- partner descriptions;
- Estonian and English language variants.

Each block must include:

```text
content_block_id
block_type
language
source_language
text
status
fact_dependencies
evidence_dependencies
commitment_dependencies
approved_by
approved_at
valid_from
valid_to
classification
permitted_uses
prohibited_uses
version
content_hash
```

Changing a linked fact, evidence status, permission, expiry date, or source amendment must flag affected content for re-review.

---

## 23. Derived scores and readiness indicators

The profile may calculate derived values, but each result must be explainable and versioned.

### 23.1 Permitted derived values

- profile completeness;
- evidence coverage;
- evidence freshness;
- capability strength;
- technology recency;
- reference readiness;
- staff eligibility coverage;
- certification validity;
- financial eligibility;
- CPV/keyword match;
- delivery-capacity risk;
- partner dependency risk;
- hard-disqualifier result;
- strategic-fit score;
- tender-specific readiness.

### 23.2 Required derived-value metadata

```text
derived_value_id
derived_type
subject_id
value
scale
status
factor_breakdown
missing_inputs
warnings
calculation_method
calculation_version
ai_model_and_prompt_version_if_used
source_fact_versions
source_preference_versions
created_at
expires_at_or_recompute_trigger
```

### 23.3 Derived-value restrictions

- Deterministic rules must be used for hard legal, date, expiry, threshold, and arithmetic checks.
- AI may summarize or classify evidence but cannot override hard rules.
- Missing inputs must reduce confidence or produce `UNKNOWN`; they must not default to a positive score.
- Users must be able to inspect why a score changed.
- The final `GO/NO-GO`, price, commitment, and approval remain human decisions.

---

## 24. Data-entry and review workflow

### 24.1 Create or import

1. An authorized user creates a record or imports a document.
2. The system assigns a safe default classification.
3. Imported documents remain immutable and receive hashes and versions.
4. AI or deterministic parsers may propose metadata and facts as `DRAFT` or `UNVERIFIED`.

### 24.2 Link evidence

1. The user selects the exact evidence version and source location.
2. The system records scope, permission, validity, and relationship type.
3. Contradictory evidence remains visible.

### 24.3 Review and verify

1. A reviewer checks the exact claim and evidence.
2. The reviewer confirms classification, permitted use, validity, and wording.
3. The system records actor, timestamp, rationale, and versions.
4. Only then may the fact become `VERIFIED`.

### 24.4 Use in a tender

1. Retrieval filters by workspace permission, classification, validity, approval, tender scope, language, and permission.
2. The proposal workflow receives only approved facts/evidence or clearly labeled unresolved data.
3. Every material company claim links back to exact fact and evidence versions.

### 24.5 Change and invalidation

The system must invalidate or flag dependent data when:

- a fact changes;
- evidence expires, is revoked, or is superseded;
- customer or partner permission changes;
- a person becomes unavailable or withdraws consent;
- a capacity period becomes stale;
- a financial reporting period changes;
- a content block dependency changes;
- a classification becomes more restrictive;
- a tender amendment changes the required scope.

Historical proposal packages retain their original snapshot and audit history.

---

## 25. Permissions and separation of duties

Minimum permission capabilities:

- view public/internal company profile;
- view confidential commercial data;
- view personal/staff data;
- view restricted evidence;
- create draft facts;
- upload evidence;
- verify legal identity;
- verify references;
- verify staff/CV information;
- approve reusable content;
- set business preferences;
- set commercial constraints;
- set security/privacy constraints;
- assign partner evidence;
- approve tender-specific use;
- administer classifications and retention;
- audit profile changes.

The same user may hold multiple roles in a small company, but the product must record which authority was exercised. High-risk fields such as signing authority, bank information, margin floor, personal data, and restricted partner/customer material require explicit permission checks.

---

## 26. Validation requirements

The implementation must validate at least:

- legal identifiers and country-specific formats where deterministic validation is possible;
- required fields and controlled taxonomies;
- date order and validity periods;
- currency and decimal precision;
- percentage and range boundaries;
- duplicate and conflicting records;
- evidence links and document versions;
- classification inheritance;
- permission and reuse expiry;
- current person/partner availability;
- unsupported or expired evidence;
- language-variant linkage;
- content dependency integrity;
- hard exclusions before weighted scoring;
- no final export uses unverified facts unless an authorized exception is explicit and visible.

A validation warning must identify the field, reason, severity, corrective action, and affected tenders/content.

---

## 27. Audit requirements

Audit events must cover:

- record creation, editing, verification, rejection, revocation, and supersession;
- evidence upload, parsing, classification, linking, and permission changes;
- sensitive-data access where policy requires it;
- business-preference and risk-threshold changes;
- derived-score calculation and version;
- AI extraction or drafting based on profile data;
- tender-specific evidence selection;
- content approval and invalidation;
- export use of company facts;
- administrative override and reason.

Audit logs must not duplicate full confidential documents or secrets.

---

## 28. Search, retrieval, and AI rules

### 28.1 Retrieval filters

Company-profile retrieval must apply all of the following before returning data:

1. authenticated actor and role;
2. organization and workspace scope;
3. record status and verification;
4. validity and freshness;
5. classification and external-AI policy;
6. tender/customer/partner permitted-use scope;
7. language and translation status;
8. evidence quality and required evidence type;
9. record version and amendment state;
10. configured token/size/cost limits.

### 28.2 AI restrictions

Gemini or another AI provider must not:

- create verified company facts;
- invent references, customers, staff, experience, certificates, finances, permissions, or capacity;
- infer legal authority;
- infer that silence means compliance;
- use expired or prohibited evidence without a visible warning;
- send restricted data externally;
- downgrade classification;
- convert a partner capability into an Eventnexus OÜ capability;
- approve a content block, price, commitment, or tender decision.

AI may:

- propose structured facts from permitted documents;
- suggest evidence links;
- detect conflicts and gaps;
- generate draft language from approved evidence;
- translate approved content while preserving source linkage;
- summarize why an opportunity may fit;
- propose questions for human review.

---

## 29. MVP required-field summary

The following table separates the required MVP profile from optional enrichment.

| Domain | MVP required | Conditional required | Optional enrichment |
|---|---|---|---|
| Legal identity | Legal name, registry code, legal form, registration country/address, official email, authorized representatives | VAT, signing authority, bank details, beneficial owner data | Establishment date, activity codes, phone |
| Roles | Profile owner, Bid Lead, Authorized Business Decision-Maker | Commercial, legal, security reviewer, submitter | Public tender contact, escalation contacts |
| Capabilities | At least one service category, description, delivery type, limitations, strategic priority, evidence/readiness status | Tender-specific capability evidence | Maturity and proficiency scores |
| Technologies | Core technologies, preferred/accepted/excluded status | Tender-required versions, recent-use evidence | Detailed competency scoring |
| Industries | Strategic interests and exclusions | Tender-required experience | Customer-type analytics |
| CPV/search | At least one include profile, exclusions, keywords, weight, lead-time rule | Tender-specific search rules | Buyer and value preferences |
| References | At least one approved reference or explicit none-available status, permission status | Tender-mandated comparable references | Rich outcome analytics |
| Staff | Consent/use model and ability to add staff evidence | Named experts, CV facts, availability, certificates | Travel preferences and detailed utilization |
| Certifications/policies | Ability to track and warn; explicit current inventory | Every tender-required certificate/policy | Verification URLs and dashboards |
| Finances | Maximum exposure and margin/risk policy | Turnover, tax, insurance, guarantees required by a tender | Detailed trend analytics |
| Partners | Ability to distinguish partner facts and permissions | Tender-specific partner commitment/evidence | Partner scoring and history |
| Exclusions | CPV, technology, industry, geography, lead time, data/security exclusions | Legal conflicts and sanctions checks | Advanced contract-clause rules |
| Capacity | Current period, roles, available effort, commitments, earliest start, delivery constraints | Tender-specific staffing plan | Forecast confidence and pipeline analytics |
| Risk appetite | Overall, technical, fixed-price, schedule, data, IP, compliance tolerances | Tender-specific legal/commercial thresholds | Multi-factor advanced scoring |
| Languages/geography | Estonian/English handling, delivery geography/mode, data-location constraints | Tender-specific translation or location evidence | Additional languages/time zones |
| Content | Approved company description and capability block | Tender-specific blocks and declarations | Extended content library |

---

## 30. Acceptance criteria traceability

### 30.1 Each factual field has an evidence and validity model

Satisfied through:

- Sections 4.1–4.7 defining the common fact, evidence, linkage, quality, verification, and validity model;
- domain tables specifying the expected evidence and review/expiry behavior for each fact family;
- invalidation rules in Section 24.5;
- validation and audit rules in Sections 26 and 27.

### 30.2 Sensitive fields have classification guidance

Satisfied through:

- the classification matrix in Section 5;
- field-level default classifications in Sections 7–21;
- inheritance and no-downgrade rules;
- specific treatment of finance, staff, customer, partner, signing, bank, and credential-related data.

### 30.3 Required MVP fields are separated from optional fields

Satisfied through:

- the three requirement levels in Section 6;
- requirement labels in each domain table;
- the consolidated MVP/conditional/optional matrix in Section 29.

---

## 31. Dependencies and follow-up tasks

This document is implemented by later backlog items, especially:

- `S0-T10` document classification policy;
- `S2-T09` permission policy engine;
- `S2-T10` append-only audit service;
- `S3-T02` immutable file/evidence versions;
- `S4-T01` Eventnexus OÜ profile model and UI;
- `S4-T02` CPV interest model;
- `S4-T03` capabilities and technologies;
- `S4-T04` reference project library;
- `S4-T05` staff profile and CV evidence;
- `S4-T06` certificate and policy evidence;
- `S4-T07` approved content blocks;
- `S4-T08` evidence search and permissions;
- `S6-T01` scoring configuration;
- `S9-T03` external-AI policy engine;
- `S15-T07` retention policy engine.

A later controlled onboarding activity must populate actual Eventnexus OÜ values and evidence. No placeholder or AI-generated value may be marked verified merely to make the profile appear complete.

---

## 32. Definition of done for company-profile implementation

The future implementation is not complete until:

- required records are versioned and auditable;
- every factual record supports evidence and validity metadata;
- sensitive data is permission- and classification-protected;
- profile readiness identifies missing, expired, prohibited, and unverified data;
- derived scores show factor breakdown and source versions;
- AI cannot promote drafts to verified facts;
- Estonian and English variants preserve source and approval linkage;
- partner and staff data cannot leak across workspaces or exports;
- invalidation propagates to affected content and tenders;
- automated tests cover verification, expiry, permissions, classification, retrieval, and unsupported-claim prevention.
