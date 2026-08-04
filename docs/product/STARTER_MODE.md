# EventNexus STARTER Mode

**Document ID:** PRD-005  
**Status:** Accepted product-direction addendum  
**Product owner:** Eventnexus OÜ  
**Effective date:** 2026-08-04  
**Applies to:** MVP prioritization, company onboarding, opportunity matching, GO/NO-GO, partnership analysis, growth planning, and pilot evaluation

## 1. Decision

EventNexus will be implemented **STARTER-first**.

The first useful product experience is not a universal tender-writing system. It is a local-first procurement opportunity and growth assistant for a real early-stage company. It must help Eventnexus OÜ avoid wasting limited bid capacity, identify opportunities it can realistically pursue, identify larger opportunities where it could contribute through a partner, and explain which verified capabilities, references, people, finances, or agreements are missing for future qualification.

This document is an authoritative addendum to:

- `PRODUCT_REQUIREMENTS.md`;
- `COMPANY_PROFILE_REQUIREMENTS.md`;
- `PILOT_SUCCESS_METRICS.md`;
- matching, GO/NO-GO, partner, capacity, and growth work in `TASKS.md`.

Where a general product requirement permits several implementation priorities, this STARTER-first decision controls the initial priority. Security, privacy, legal, submission, evidence, and human-approval policies remain unchanged.

## 2. Confirmed initial operating context

The initial Eventnexus context supplied by the product owner is:

| Field | Initial value | Required system status |
|---|---:|---|
| Legal organization | Eventnexus OÜ exists | Verify from authoritative evidence before exporting as a verified fact |
| Annual turnover | `0 EUR` | `USER_CONFIRMED_PENDING_EVIDENCE` until linked to approved accounting or annual-report evidence |
| Available workers | `1` | `USER_CONFIRMED_PENDING_EVIDENCE`; relationship, role, skills, availability, and tender-use permission remain separate facts |
| Approved company references | Unknown | Must not be converted to zero or assumed present without profile review |
| Committed delivery partners | Unknown | Must not be assumed; tender-specific written commitment is required before use |
| Certifications, insurance, finance capacity | Unknown | Missing until verified evidence exists |

The product must distinguish user-confirmed onboarding data from verified evidence. It must not describe Eventnexus as unqualified merely because a field is unknown, and it must not describe Eventnexus as qualified merely because a user entered a claim.

## 3. Product promise

The STARTER experience must answer five questions quickly:

1. **Can Eventnexus bid directly?**
2. **Could Eventnexus participate through a partner, consortium, reliance arrangement, or subcontracting role?**
3. **Which hard requirements prevent participation?**
4. **What concrete evidence, capacity, references, people, finances, or permissions would remove those blockers?**
5. **Is the likely value worth the bid-preparation, delivery, cash-flow, legal, and opportunity cost?**

The product must prefer an early, explained negative decision over a persuasive but unrealistic bid draft.

## 4. Company maturity profile

Company maturity is a versioned derived assessment, not a marketing label and not a manually trusted claim.

Initial maturity values:

```text
STARTER
GROWTH
ESTABLISHED
```

### 4.1 STARTER

Typical characteristics:

- very low or no verified turnover;
- one or a small number of available people;
- few or no approved company references;
- limited ability to finance long delivery or payment cycles;
- limited replacement capacity;
- partner network still being created;
- primary goal is safe revenue, references, evidence, and partner development.

### 4.2 GROWTH

Typical characteristics:

- recurring verified turnover;
- multiple named delivery resources;
- approved references in selected service areas;
- some delivery concurrency and replacement capacity;
- established partner relationships;
- ability to pursue medium-complexity opportunities with bounded risk.

### 4.3 ESTABLISHED

Typical characteristics:

- stable finances and operating history;
- broad verified references and specialist coverage;
- mature delivery, security, quality, and continuity controls;
- ability to lead larger procurements and framework agreements where requirements are met.

### 4.4 Calculation rules

- Stage is calculated from verified facts and explicitly identified pending data.
- A missing field is not silently scored as a positive fact.
- A single high turnover value does not prove delivery capacity.
- A skilled individual does not automatically prove organization-level experience.
- Partner capability counts only when the procurement permits the arrangement and a current, scoped commitment exists.
- Historical stage changes are preserved for audit and learning.

## 5. Opportunity classification

Every analyzed opportunity must receive one primary STARTER classification. A percentage score alone is insufficient.

### 5.1 `DIRECT_BID`

Use when:

- no known hard eligibility blocker exists;
- verified or reviewable evidence can satisfy mandatory requirements;
- the required delivery team and availability are realistic;
- bid effort, contract exposure, payment timing, and delivery scope fit approved limits;
- the authorized decision-maker may reasonably consider a direct bid.

`DIRECT_BID` is not final approval. It means that direct participation is not currently blocked by known facts.

### 5.2 `PARTNER_OPPORTUNITY`

Use when direct participation is blocked or unsafe, but Eventnexus has a credible, evidence-backed contribution and the procurement permits a suitable collaboration structure.

The result must identify:

- the missing prime or partner capabilities;
- the permitted participation structures visible in the sources;
- the Eventnexus contribution supported by evidence;
- required partner evidence and commitment;
- commercial, confidentiality, dependency, and delivery risks;
- the recommended next contact or partner action.

### 5.3 `GROWTH_TARGET`

Use when the opportunity is not currently actionable but exposes reusable development goals.

Examples:

- a missing reference category;
- a recurring turnover threshold;
- a specialist role repeatedly required;
- insurance or certification frequently requested;
- a technology or process capability strategically worth developing.

A growth target must state the source requirement, the verified current gap, the evidence needed to close it, and whether closing it is strategically approved.

### 5.4 `NO_GO`

Use when:

- a hard requirement cannot be met through an allowed and committed structure;
- the work is outside approved strategy;
- bid effort is disproportionate;
- delivery, finance, legal, security, or cash-flow exposure exceeds approved limits;
- the deadline is operationally unsafe;
- the required evidence cannot be obtained truthfully;
- the opportunity should not consume further bid capacity.

The system must retain the explanation and may separately identify a long-term learning signal.

## 6. Hard blockers before scoring

Deterministic blockers are evaluated before weighted fit scores.

Initial blocker categories include:

- minimum turnover or financial-standing requirement;
- minimum team size;
- named specialist roles;
- project/reference counts, values, dates, or scope;
- mandatory technology experience;
- certification, insurance, authorization, or registration;
- delivery geography or language;
- sanctions or exclusion conditions;
- deadline and mandatory attendance constraints;
- prohibited or unavailable collaboration structure;
- required evidence or signature authority;
- capacity, continuity, or cash-flow limit;
- explicit strategic exclusion.

Each blocker must include:

```text
blocker_id
requirement_version_id
requirement_type
normalized_operator
required_value
verified_company_value_or_missing_state
evidence_links
partner_coverability
resolution_options
confidence
review_state
```

AI may assist extraction and explanation, but deterministic policy controls whether a known hard blocker prevents `DIRECT_BID`.

## 7. Low-barrier opportunity definition

A low-value procurement is not automatically low-barrier. STARTER matching must separately assess:

- financial thresholds;
- team size and specialist roles;
- company and person reference requirements;
- technology and domain requirements;
- certifications and insurance;
- proposal, prototype, interview, or sample-work workload;
- unpaid bid effort;
- delivery duration and concurrency;
- payment schedule and pre-financing;
- warranties, support, penalties, liability, and intellectual-property terms;
- language, location, and meeting requirements;
- partner and subcontractor rules;
- reference value if successfully delivered.

A low-barrier opportunity is one where the total qualification, bid, delivery, and commercial burden is proportionate to the company's verified current capacity.

## 8. Separate direct and partner assessments

The system must maintain separate results.

### 8.1 Direct Fit

Recommended initial dimensions:

| Dimension | Initial weight |
|---|---:|
| Eligibility and mandatory evidence | 35% |
| Delivery capacity and continuity | 25% |
| Evidence readiness | 15% |
| Commercial and cash-flow safety | 15% |
| Bid-preparation effort | 10% |

A known unresolvable hard blocker overrides the weighted score and prevents `DIRECT_BID`.

### 8.2 Partner Fit

Recommended initial dimensions:

| Dimension | Initial weight |
|---|---:|
| Evidence-backed Eventnexus contribution | 30% |
| Permitted and feasible partner structure | 25% |
| Reference and growth value | 20% |
| Commercial potential | 15% |
| Partnership and bid effort | 10% |

Weights are configurable and versioned. They are not evidence and do not replace human decisions.

## 9. Partner opportunity brief

For `PARTNER_OPPORTUNITY`, the system must produce a reviewable brief containing:

- opportunity and buyer summary;
- deadline and freshness;
- why Eventnexus cannot or should not lead alone;
- required prime-contractor profile;
- required partner roles, finances, references, certifications, and technologies;
- Eventnexus capabilities that are verified for the proposed role;
- unsupported contribution ideas shown only as gaps or drafts;
- possible collaboration form as supported by the tender source;
- expected bid contribution and delivery responsibility;
- major dependency and confidentiality risks;
- next action, owner, due date, and outreach status.

The first release may use a manually maintained partner directory. It must not invent partners, commitments, availability, or permission to reuse partner evidence.

## 10. Growth roadmap

The product must aggregate recurring blockers into an evidence-backed growth roadmap.

Example categories:

- first qualifying reference;
- reference above a recurring value threshold;
- additional specialist capacity;
- recurring technology requirement;
- insurance, certificate, or policy;
- public-sector delivery evidence;
- annual turnover threshold;
- partner category;
- security or quality process maturity;
- reusable tender content and supporting evidence.

Each recommendation must include:

```text
growth_gap_id
source_opportunities
normalized_requirement
current_verified_state
frequency_and_value_signal
recommended_action
evidence_needed
owner
status
target_date
strategic_approval
```

The product must not encourage obtaining a credential or hiring a person solely because one tender requested it. Recommendations require frequency, value, strategic fit, and cost context.

## 11. STARTER onboarding

The initial onboarding flow must capture or explicitly mark unknown:

- legal identity and authority;
- turnover by completed financial period;
- available workers and contractors;
- skills and project-level experience;
- approved company and personal references;
- practical delivery concurrency;
- minimum and maximum project size;
- bid-preparation capacity;
- working languages and geography;
- technology preferences and exclusions;
- cash-flow and payment-term tolerance;
- warranty, support, liability, and risk limits;
- partner relationships and commitment status;
- immediate growth goals.

Every value must retain fact category, verification state, evidence, owner, review date, and classification.

## 12. First usable vertical slice

The first STARTER vertical slice is:

```text
company onboarding and evidence readiness
→ manual tender package import
→ deterministic eligibility and threshold extraction
→ company-versus-requirement comparison
→ hard-blocker review
→ DIRECT_BID / PARTNER_OPPORTUNITY / GROWTH_TARGET / NO_GO
→ partner brief or growth actions
→ human decision and feedback
```

Full proposal drafting, pricing, approval, export, and submission remain later capabilities. The architecture must still support them, but they must not displace the first useful STARTER workflow.

## 13. UX requirements

The opportunity list and detail view must show:

- primary STARTER classification;
- direct-fit and partner-fit results separately;
- hard blockers before soft scores;
- verified facts versus missing or pending evidence;
- bid-effort estimate;
- delivery and cash-flow risk summary;
- partner needs;
- growth value;
- source citations and calculation version;
- human review state and final decision.

The UI must not use celebratory language for a high score when a hard blocker exists.

## 14. Safety and governance

- No company fact, partner fact, reference, turnover value, worker availability, certification, or commitment may be fabricated.
- Unknown data remains unknown.
- Partner participation must be supported by tender rules and a real commitment before bid approval.
- Personal CV and partner data retain their classifications and use permissions.
- AI output cannot change company maturity, hard blockers, or participation state without validated structured data and human review.
- Growth recommendations are business suggestions, not legal, financial, or employment advice.
- Original tender files remain local and must not be committed to the public repository.
- Human submission boundaries remain unchanged.

## 15. STARTER pilot requirements

The pilot dataset must include:

- at least one plausible `DIRECT_BID` opportunity;
- at least one `PARTNER_OPPORTUNITY`;
- at least one `GROWTH_TARGET`;
- at least one justified `NO_GO`;
- at least one opportunity where a low contract value still contains a material qualification or contract barrier;
- at least one opportunity where direct fit is low but partner fit is high.

The gold standard must be reviewed against the same company-profile version used by the system.

### 15.1 STARTER metrics

| Metric | Formula or assessment | Initial target |
|---|---|---:|
| Hard-blocker recall | Correctly identified gold-standard blockers / all gold-standard blockers | `100%` for blockers that invalidate direct participation |
| Unsafe direct-bid rate | `DIRECT_BID` results with a known unresolved hard blocker / all `DIRECT_BID` results | `0` |
| Classification agreement | Human agreement with the four-way classification using the same profile version | `>= 90%` |
| Partner-brief usefulness | Human rating of capability gap, contribution, structure, evidence, and next action | `>= 4.0/5` |
| Growth-gap traceability | Approved growth actions linked to source requirement, current state, evidence need, and owner | `100%` |
| Triage-time reduction | Reduction in active time to an evidence-backed initial classification | Median `>= 50%` for clear blocker or partner-path cases |
| Low-value false-safety rate | Opportunities treated as low-barrier solely because their value is low | `0` |

## 16. Product non-goals for the first STARTER release

The first release does not:

- guarantee that a buyer will accept a consortium, reliance, or subcontracting structure;
- automatically contact or commit partners;
- infer private financial data;
- promise work under a framework agreement;
- treat a framework maximum value as expected Eventnexus revenue;
- generate a binding joint-bid agreement;
- replace legal or procurement review;
- automatically submit a tender;
- optimize solely for the highest contract value.

## 17. Implementation workstream

These tasks are cross-phase and must respect their platform and domain dependencies.

### `ST-T01 — Document STARTER-first product strategy` — complete

Acceptance:

- this canonical document exists;
- the initial baseline distinguishes user-confirmed and verified facts;
- maturity, classifications, hard blockers, partner analysis, growth roadmap, first vertical slice, and pilot metrics are explicit.

### `ST-T02 — Add STARTER company maturity and onboarding contracts`

Dependencies: typed API contracts, organization/company-profile persistence, evidence and classification foundations.

Acceptance:

- `STARTER`, `GROWTH`, and `ESTABLISHED` are derived and versioned;
- unknown data remains unknown;
- one person's skills do not automatically become company capability;
- sensitive fields have authorization tests.

### `ST-T03 — Implement deterministic STARTER opportunity classification`

Dependencies: normalized opportunities, document and requirement extraction, company evidence, and lifecycle decision records.

Acceptance:

- hard blockers run before weighted scores;
- all material results have source and company-evidence traceability;
- missing evidence cannot create a positive qualification result;
- tests include low-value tenders with high qualification or contract barriers.

### `ST-T04 — Add partner opportunity brief and outreach tracking`

Dependencies: ST-T03 and partner-profile/evidence support.

Acceptance:

- no partner, commitment, availability, or evidence permission is invented;
- unsupported contribution ideas remain drafts;
- confidential partner terms are access-controlled and denied from external AI by default.

### `ST-T05 — Add evidence-backed growth roadmap`

Dependencies: ST-T03, outcome feedback, and pilot metrics.

Acceptance:

- every growth action links to source requirements and current verified facts;
- recommendations have owner, status, and strategic approval;
- the system does not recommend hiring, certification, or expenditure from a single tender signal alone;
- STARTER metrics are included in pilot reporting.

## 18. Acceptance criteria

STARTER-first product alignment is complete when:

- repository entry documents and the agent guide reference this decision;
- company maturity and onboarding states are modeled as evidence-aware data;
- the four opportunity classifications are represented in contracts and UI;
- deterministic hard blockers are evaluated before soft scoring;
- direct and partner fit are separate;
- partner briefs identify real missing capabilities and supported Eventnexus contributions;
- recurring blockers can produce traceable growth actions;
- pilot metrics measure unsafe direct-fit classifications, partner usefulness, gap traceability, and triage time;
- tests include early-stage company profiles with missing evidence;
- no test or demo silently upgrades user-confirmed data to verified facts.
