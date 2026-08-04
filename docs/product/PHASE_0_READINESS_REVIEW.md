# Phase 0 / Milestone M0 Readiness Review

**Review date:** 2026-08-04  
**Last updated:** 2026-08-04  
**Scope:** Discovery, product definition, integrations, AI governance, and submission/legal boundaries  
**Implementation boundary:** Reversible repository implementation begins at `S1-T01`

## 1. Executive conclusion

The research and documentation work required before repository implementation is complete. Tasks `S0-T01` through `S0-T15` have deliverables and acceptance-criteria traceability.

The project is ready for two parallel activities:

1. Eventnexus OÜ reviews and formally approves the M0 product, source, AI, classification, and submission decisions.
2. Engineering begins reversible, secret-free Phase 1 foundation work using only synthetic or sanitized data.

Formal organizational approval is distinct from document completion. M0 must not be reported as exited until the approval checklist in `TASKS.md` is complete.

The following work may begin before all M0 approval records are finalized:

- repository skeleton and development conventions;
- local application scaffolding;
- typed configuration with safe disabled defaults;
- Docker development foundations;
- quality tooling and secret-free CI;
- mock adapters, local-only interfaces, and fixture-based tests;
- architecture work that does not enable a governed external capability.

The following remain blocked until the applicable owner approves the governing policy or decision:

- real-data Gemini processing;
- production Gemini credentials or billing enablement;
- live automated TED synchronization;
- broader or scheduled RHR retrieval beyond the approved bounded path;
- confidential or personal company-evidence processing;
- production retention and external-transfer decisions;
- any signing, portal authentication, submission, withdrawal, or other binding external action.

## 2. Completed task register

| Task | Deliverable | Completion status |
|---|---|---|
| S0-T01 | `docs/product/PRODUCT_REQUIREMENTS.md` | Complete |
| S0-T02 | `docs/product/COMPANY_PROFILE_REQUIREMENTS.md` | Complete |
| S0-T03 | `docs/product/TENDER_LIFECYCLE.md` | Complete |
| S0-T04 | `docs/product/PILOT_SUCCESS_METRICS.md` | Complete |
| S0-T05 | `docs/integrations/RHR_DISCOVERY.md`, ADR-001 | Complete for selected MVP path |
| S0-T06 | `fixtures/rhr/` sanitized offline fixtures | Complete; provenance re-audited 2026-08-04 |
| S0-T07 | `docs/integrations/TED_DISCOVERY.md`, `fixtures/ted/` | Complete; result coverage added 2026-08-04 |
| S0-T08 | `docs/integrations/SOURCE_FRESHNESS_POLICY.md` | Complete |
| S0-T09 | `docs/security/GEMINI_DATA_POLICY.md` | Policy complete; production project provisioning deferred |
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
- The Bid Lead is the primary daily role.
- Final participation, commercial, declaration, package, signing, and submission decisions require authorized humans.
- Every AI result remains draft or decision support until validated and reviewed.

### Sources

- TED Search API v3 is the primary documented automated discovery source for relevant published EU notices.
- RHR supports user-directed public-notice import/enrichment and manual document import.
- No undocumented RHR bulk crawler, sequential ID crawler, authenticated portal scraper, or supplier submission automation is part of the MVP.
- Raw source identity and immutable versions are preserved.
- Amendments deterministically invalidate affected downstream work.

### Gemini

- Production free-tier use is prohibited by project policy.
- Production requires a dedicated Eventnexus-controlled paid project.
- Unknown and restricted content is blocked from external AI.
- Confidential and personal data are denied by default.
- Files API, explicit context caching, grounding, provider-side state, and shared logging/datasets are disabled by default.
- Cost, schema, tool, retry, step, classification, and audit controls are mandatory.

### Submission

- EventNexus creates a reviewed package, manifest, validation report, hash, and checklist.
- An authorized human authenticates, signs where required, submits through the official channel, and records the receipt.
- The MVP stores no portal, ID-card, Smart-ID, Mobile-ID, private signing, or reusable identity secrets.
- Supplier-side RHR submission automation is unsupported for the MVP.

## 4. Formal approvals still required

The following M0 exit items are organizational approvals rather than documentation tasks:

| Decision | Required owner | Evidence of approval |
|---|---|---|
| Product requirements and MVP scope | Authorized Business Decision-Maker | Dated approval record and document version |
| RHR ingestion approach and accepted coverage limitation | Product/Procurement Owner | ADR/policy approval |
| TED automated discovery approach | Product and Engineering Owner | Integration decision approval |
| Gemini account, tier, and data-processing policy | Business, Security/Privacy, and Financial Owners | Approved policy plus production-project verification |
| Document classification policy | Security/Privacy Owner | Approved policy version |
| Human-controlled submission boundary | Authorized Business Decision-Maker and legal reviewer where applicable | Approved submission policy |
| Pilot metrics and targets | Product Owner | Approved metric version |

Document completion does not silently grant these approvals. The authoritative checkbox status remains in `TASKS.md`.

## 5. Deferred decisions and latest safe points

| ID | Decision | Latest safe point |
|---|---|---|
| D-002 | Exact Gemini paid project, billing owner, administrators, and ZDR verification | Before any real-data Gemini enablement |
| D-003 | Celery versus Dramatiq | `S1-T04` ADR |
| D-004 | Backup encryption approach | Before pilot-data backup implementation |
| D-005 | First proposal DOCX template | Before proposal/export implementation |
| NEW-001 | Exact local reference hardware and resource envelope | `S1-T06` / performance baseline |
| NEW-002 | Initial approved company evidence set and named reviewers | Before company-profile or pilot data entry |
| NEW-003 | Whether to request written RHR support confirmation for broader non-TED discovery | Before proposing broader RHR automation |

## 6. Entry criteria for S1-T01

`S1-T01 — Create repository skeleton` may begin when:

- the contributor has read `README.md`, `AGENTS.md`, `TASKS.md`, and this review;
- the work remains reversible and does not enable real external processing;
- no live Gemini, RHR, or TED call is required;
- no real tender, customer, employee, partner, financial, or credential data is committed;
- the documented monorepo and service boundaries are followed unless changed through an ADR;
- Windows and Linux line-ending behavior is defined intentionally;
- secrets, local volumes, uploads, generated outputs, and private tender data are excluded from Git;
- work uses a focused commit and updates `TASKS.md` only after acceptance verification.

The initial development target may support both Windows 11 Docker Desktop and Linux-compatible containers. Exact production hardware sizing can remain deferred until Docker and performance tasks.

## 7. First implementation task

The next open backlog item is:

```text
S1-T01 — Create repository skeleton
```

It creates the documented directories, `.editorconfig`, `.gitattributes`, `.gitignore`, root tooling foundations, and documentation directories. It is the point where actual repository implementation begins.

## 8. Known limitations carried into implementation

- TED does not cover every Estonian procurement opportunity.
- No official documented RHR bulk-search contract was selected.
- RHR supplier submission automation is unsupported for the MVP.
- Gemini is an external processor; local deployment is not fully offline processing.
- External service behavior, terms, field lists, limits, and retention features may change and must be revalidated before production enablement.
- Sanitized and synthetic fixtures are internal test contracts, not official complete API schemas.
- AI cannot guarantee complete requirement extraction, legal compliance, factual correctness, or a successful tender outcome.
- Pilot targets require measurement and may lead to reprioritization.
- No executable product, Docker stack, CI, or automated test runner exists before Phase 1.

These limitations must remain visible and must not be hidden by UI or marketing language.
