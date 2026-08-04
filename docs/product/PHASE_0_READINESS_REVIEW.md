# Phase 0 / Milestone M0 Readiness Review

**Review date:** 2026-08-04  
**Scope:** Discovery, product definition, integrations, AI governance, and submission/legal boundaries  
**Implementation boundary:** Product code begins at `S1-T01`

## 1. Executive conclusion

The research and documentation work required before repository and application implementation is complete. Tasks `S0-T01` through `S0-T15` have deliverables and acceptance-criteria traceability.

The project is ready for an Eventnexus OÜ decision review. Formal organizational approval is distinct from document completion. Coding should begin only after the decision owners accept the policies and deferred decisions relevant to the first implementation phase.

## 2. Completed task register

| Task | Deliverable | Completion status |
|---|---|---|
| S0-T01 | `docs/product/PRODUCT_REQUIREMENTS.md` | Complete |
| S0-T02 | `docs/product/COMPANY_PROFILE_REQUIREMENTS.md` | Complete |
| S0-T03 | `docs/product/TENDER_LIFECYCLE.md` | Complete |
| S0-T04 | `docs/product/PILOT_SUCCESS_METRICS.md` | Complete |
| S0-T05 | `docs/integrations/RHR_DISCOVERY.md`, ADR-001 | Complete for selected MVP path |
| S0-T06 | `fixtures/rhr/` sanitized offline fixtures | Complete |
| S0-T07 | `docs/integrations/TED_DISCOVERY.md`, `fixtures/ted/` | Complete |
| S0-T08 | `docs/integrations/SOURCE_FRESHNESS_POLICY.md` | Complete |
| S0-T09 | `docs/security/GEMINI_DATA_POLICY.md` | Complete policy decision; project provisioning deferred to implementation/deployment |
| S0-T10 | `docs/security/DOCUMENT_CLASSIFICATION_POLICY.md` | Complete |
| S0-T11 | `docs/security/AI_THREAT_MODEL.md` | Complete |
| S0-T12 | `docs/security/AI_COST_POLICY.md` | Complete |
| S0-T13 | `docs/procurement/SUBMISSION_POLICY.md` | Complete |
| S0-T14 | `docs/integrations/RHR_SUBMISSION_INTEGRATION_DISCOVERY.md` | Complete; conclusion `UNSUPPORTED_FOR_MVP` |
| S0-T15 | `docs/legal/LEGAL_REVIEW_CHECKPOINTS.md` | Complete |

## 3. Decisions established by Phase 0

### Product

- Estonia-first, local, single-organization MVP for Eventnexus OÜ.
- Estonian is the default UI/workflow language; English tender material is preserved and supported.
- Primary daily role is Bid Lead; final business decisions and final package approval require an authorized human.
- Every AI result is draft/decision support until validated and reviewed.

### Sources

- TED Search API v3 is the primary documented automated opportunity-discovery source.
- RHR supports user-directed public notice import/enrichment and manual document import.
- No undocumented RHR bulk crawler or authenticated portal scraper is part of the MVP.
- Source versions are immutable, and amendments invalidate affected downstream work.

### Gemini

- Production free tier is prohibited.
- Production requires a dedicated Eventnexus-controlled paid project.
- Unknown/restricted content is blocked from external AI.
- Confidential and personal data are denied by default.
- Files API, explicit context caching, grounding, provider-side state, and shared logging/datasets are disabled by default.
- Cost, schema, tool, retry, step, and audit controls are mandatory.

### Submission

- EventNexus creates an approved package, manifest, validation report, and checklist.
- An authorized human authenticates, signs where required, submits, and records the official receipt.
- The MVP stores no portal, ID-card, Smart-ID, Mobile-ID, or signing secrets.
- Supplier-side RHR submission automation is unsupported for the MVP.

## 4. Formal approvals still required

The following M0 exit items remain organizational approvals rather than research tasks:

| Decision | Required owner | Evidence of approval |
|---|---|---|
| Product requirements and MVP scope | Authorized Business Decision-Maker | dated approval record/version |
| RHR ingestion approach and accepted coverage limitation | Product/Procurement Owner | ADR/policy approval |
| TED automated discovery approach | Product and Engineering Owner | integration decision approval |
| Gemini account/tier/data-processing policy | Business, Security/Privacy, and Financial Owners | approved policy plus production project verification |
| Document classification policy | Security/Privacy Owner | approved policy version |
| Human-controlled submission boundary | Authorized Business Decision-Maker / Legal reviewer as applicable | approved submission policy |
| Pilot metrics and targets | Product Owner | approved metric version |

Document completion does not silently grant these approvals.

## 5. Deferred decisions before or during Phase 1

| ID | Decision | Latest safe point |
|---|---|---|
| D-002 | Exact Gemini paid project, billing owner, administrators, and ZDR verification | Before any real-data Gemini enablement |
| D-003 | Celery vs Dramatiq | S1-T04 ADR |
| D-004 | Backup encryption approach | Before pilot data backup implementation |
| D-005 | First proposal DOCX template | Before proposal/export implementation |
| NEW-001 | Exact local reference hardware and resource envelope | S1-T06/S17 performance baseline |
| NEW-002 | Initial approved company evidence set and named reviewers | Before company profile/pilot workflows |
| NEW-003 | Whether to request written RHR support confirmation for broader non-TED discovery | Before proposing any RHR bulk automation |

## 6. Entry criteria for S1-T01

Before beginning the repository skeleton:

- authorized owner accepts the documented MVP and human-submission boundary;
- no requested architecture change conflicts with README/AGENTS/Phase 0 policies;
- local deployment target is confirmed as Windows 11 Docker Desktop, Linux server, or both for development support;
- engineering accepts the monorepo and service boundaries already defined;
- work starts on a focused branch or through the explicitly approved repository workflow;
- no live Gemini/RHR/TED call or real tender data is required to bootstrap the repository.

## 7. First implementation task

The next open backlog item is:

```text
S1-T01 — Create repository skeleton
```

It creates the documented directories, line-ending rules, ignore rules, root tooling, and documentation structure. It is the point where actual program/repository implementation begins.

## 8. Known limitations carried into implementation

- TED does not cover every Estonian procurement opportunity.
- No official documented RHR bulk search contract was selected.
- RHR supplier submission automation is unsupported for MVP.
- Gemini is an external processor and local deployment is not equivalent to fully offline processing.
- AI cannot guarantee complete requirement extraction, legal compliance, winning a tender, or factual correctness.
- Pilot targets require measurement and may lead to reprioritization.

These limitations must be visible in product documentation and must not be hidden by marketing language.
