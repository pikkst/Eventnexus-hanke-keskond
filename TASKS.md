# TASKS.md — EventNexus Hanke Keskond Delivery Backlog

This file is the executable delivery plan for Kilo Code and human contributors.

Read [`AGENTS.md`](AGENTS.md) before starting any task. Do not check a task as complete until its acceptance criteria, tests, documentation, and verification are complete.

## Status legend

- `[ ]` Not started
- `[~]` In progress
- `[x]` Complete
- `[!]` Blocked — add the blocker and required decision directly below the task
- `[?]` Requires user/product/legal decision

## Delivery rules

1. Work in dependency order unless the user explicitly reprioritizes.
2. Complete one coherent task or vertical slice per commit.
3. Every feature task includes tests and documentation.
4. Every external integration starts with a discovery spike and saved fixtures.
5. No real secrets, personal data, or tender documents may be committed.
6. No AI output may become approved business data without validation and human review.
7. No autonomous RHR submission is part of the MVP.
8. Update this file after every completed task.
9. Add newly discovered work as a task instead of hiding it inside another task.
10. Use ADRs for material architecture decisions.

## Milestone overview

| Milestone | Goal | Exit condition |
|---|---|---|
| M0 | Discovery and policy | Approved integration, data, AI, and submission decisions |
| M1 | Local platform foundation | Reproducible Docker system with auth, storage, jobs, and audit |
| M2 | Opportunity discovery | RHR/TED/manual import and explainable matching |
| M3 | Tender intelligence | Documents, citations, requirements, compliance, and evidence |
| M4 | AI-assisted proposal | Policy-gated Gemini workflows and proposal drafting |
| M5 | Review and package | Pricing, approval, export, and submission handoff |
| M6 | Pilot-ready MVP | Security, backup, observability, evaluations, and real pilot validation |

---

# Phase 0 — Discovery, legal boundaries, and product decisions

## Sprint 0.1 — Product definition

- [x] **S0-T01 — Write the product requirements document**
  - Create `docs/product/PRODUCT_REQUIREMENTS.md`.
  - Define users, jobs-to-be-done, pain points, success metrics, core workflows, non-goals, and MVP boundaries.
  - Define Estonian-first language requirements and English tender handling.
  - Acceptance:
    - primary user and decision-maker roles are explicit;
    - every MVP feature maps to a user outcome;
    - autonomous submission is explicitly excluded;
    - measurable pilot success criteria exist.

- [x] **S0-T02 — Define Eventnexus OÜ company profile requirements**
  - Document the fields needed for capabilities, technologies, industries, references, staff, certifications, finances, partners, exclusions, CPV interests, capacity, and risk appetite.
  - Identify which fields are facts, evidence, preferences, or derived scores.
  - Acceptance:
    - each factual field has an evidence and validity model;
    - sensitive fields have classification guidance;
    - required MVP fields are separated from optional fields.

- [ ] **S0-T03 — Define the MVP tender lifecycle**
  - Document states, transitions, permissions, validation gates, invalidation rules, and terminal states.
  - Include amendment, clarification, cancellation, withdrawal, submitted, awarded, and not-awarded paths.
  - Acceptance:
    - state diagram exists;
    - protected transitions identify authorized roles;
    - source changes invalidate affected analysis and approvals;
    - no transition depends only on model output.

- [ ] **S0-T04 — Define pilot success metrics**
  - Define measurable targets for opportunity recall, false-positive rate, requirement recall, citation accuracy, unsupported-claim rate, preparation time reduction, user review time, export correctness, and system reliability.
  - Acceptance:
    - metrics have calculation methods;
    - baseline and target values are recorded or marked for pilot measurement;
    - metrics are linked to later evaluation tasks.

## Sprint 0.2 — RHR and TED integration discovery

- [ ] **S0-T05 — RHR official integration discovery spike**
  - Investigate official RHR open data, documented APIs, public notice endpoints, export formats, authentication, rate limits, update/version semantics, and reuse conditions.
  - Contact official support if documentation is incomplete.
  - Record exact official sources and retrieval date.
  - Create `docs/integrations/RHR_DISCOVERY.md`.
  - Acceptance:
    - at least one permitted MVP ingestion path is selected;
    - unsupported assumptions are listed;
    - update detection strategy is documented;
    - no production scraper is created during the spike;
    - an ADR selects the initial RHR strategy.

- [ ] **S0-T06 — Capture sanitized RHR fixtures**
  - Save representative public notice payloads or exports for IT procurements, lots, amendments, cancellations, award notices, and attachments.
  - Remove unnecessary personal details when possible.
  - Acceptance:
    - fixture provenance and retrieval date are documented;
    - fixtures cover at least one multi-lot notice and one amendment;
    - fixture license/reuse status is documented;
    - tests can run without live RHR access.

- [ ] **S0-T07 — TED API discovery spike**
  - Validate TED API 3 Search API, query syntax, pagination/iteration, eForms identifiers, multilingual fields, downloadable formats, and limits.
  - Create `docs/integrations/TED_DISCOVERY.md`.
  - Acceptance:
    - example queries for Estonian IT tenders exist;
    - fields required by the normalized opportunity model are mapped;
    - pagination and replay strategy are documented;
    - sanitized fixtures are stored.

- [ ] **S0-T08 — Decide source freshness and synchronization policy**
  - Define polling intervals, manual refresh, backoff, source outage behavior, amendment urgency, retention, and cursor recovery.
  - Acceptance:
    - no source is polled more aggressively than permitted;
    - deadline/amendment notifications have a target latency;
    - failed sync does not delete existing opportunities;
    - source freshness is visible to users.

## Sprint 0.3 — AI data governance

- [ ] **S0-T09 — Gemini account and data-processing decision**
  - Decide which Google account/project, billing tier, contractual terms, API region constraints, and organizational controls are approved for production data.
  - Record whether zero-data-retention-compatible usage is required and which API features are allowed.
  - Create `docs/security/GEMINI_DATA_POLICY.md`.
  - Acceptance:
    - free-tier production use is either explicitly approved or prohibited;
    - allowed document classifications are defined;
    - file upload, caching, logging, and grounding features are individually addressed;
    - responsible owner and review date are recorded.

- [ ] **S0-T10 — Define document classification policy**
  - Define `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `PERSONAL_DATA`, and `RESTRICTED_NO_EXTERNAL_AI`.
  - Define defaults, user overrides, redaction requirements, retention, and external-AI permissions.
  - Acceptance:
    - unknown classification defaults to no external AI;
    - every class has allowed processing paths;
    - policy covers derived chunks, embeddings, prompts, responses, exports, and logs.

- [ ] **S0-T11 — Create AI threat model**
  - Cover prompt injection, data exfiltration, malicious attachments, unsupported claims, model hallucination, tool abuse, denial-of-wallet, sensitive logging, stale evidence, and provider outage.
  - Create `docs/security/AI_THREAT_MODEL.md`.
  - Acceptance:
    - threats map to mitigations and tests;
    - residual risks are explicit;
    - tool allowlisting and schema validation are mandatory controls.

- [ ] **S0-T12 — Define AI cost policy**
  - Define per-call, per-workspace, daily, monthly, and emergency-stop limits.
  - Define cost visibility and approval for unusually large jobs.
  - Acceptance:
    - budget enforcement behavior is deterministic;
    - the worker can stop safely when limits are reached;
    - production defaults cannot represent unlimited spending.

## Sprint 0.4 — Submission, signing, and legal boundaries

- [ ] **S0-T13 — Document MVP submission policy**
  - Create `docs/procurement/SUBMISSION_POLICY.md`.
  - Specify that the MVP produces a package and checklist while the authorized person submits through the official channel.
  - Acceptance:
    - no credentials or identity secrets are stored;
    - submission evidence fields are defined;
    - responsibilities before and after submission are explicit.

- [ ] **S0-T14 — Investigate official submission integration options**
  - Determine whether any official RHR interface supports supplier-side draft or submission automation.
  - Document legal, authentication, technical, and support constraints.
  - Acceptance:
    - no automation is implemented;
    - result is a documented `supported`, `unsupported`, or `unknown` conclusion;
    - any future work is placed in post-MVP tasks.

- [ ] **S0-T15 — Define legal disclaimer and review checkpoints**
  - Define where legal, procurement, privacy, security, commercial, and authorized-signatory review are required.
  - Acceptance:
    - the UI and exports can display correct responsibility notices;
    - legal review is not represented as an AI capability;
    - high-risk declarations require explicit approval.

## Milestone M0 exit checklist

- [ ] Product requirements approved.
- [ ] RHR ingestion approach approved.
- [ ] TED approach approved.
- [ ] Gemini data policy approved.
- [ ] Document classifications approved.
- [ ] Submission boundary approved.
- [ ] Pilot success metrics defined.

---

# Phase 1 — Repository and local platform foundation

## Sprint 1.1 — Monorepo bootstrap

- [ ] **S1-T01 — Create repository skeleton**
  - Create directories defined in `README.md`.
  - Add `.editorconfig`, `.gitattributes`, `.gitignore`, root tooling, and documentation directories.
  - Acceptance:
    - Windows and Linux line-ending behavior is intentional;
    - secrets, volumes, uploads, generated files, and local tender data are ignored;
    - empty directories use documented placeholders only where needed.

- [ ] **S1-T02 — Bootstrap Next.js web application**
  - Use TypeScript strict mode and current stable supported dependencies.
  - Add root layout, localization foundation, error boundary, loading state, and health page.
  - Acceptance:
    - app starts in Docker and locally;
    - no user-facing strings are hard-coded outside localization resources;
    - lint, typecheck, and unit test commands pass.

- [ ] **S1-T03 — Bootstrap FastAPI application**
  - Add typed configuration, application factory, health/readiness endpoints, safe error handling, correlation IDs, OpenAPI metadata, and structured logging.
  - Acceptance:
    - startup fails clearly on invalid critical configuration;
    - production mode does not expose stack traces;
    - unit tests cover health and error responses.

- [ ] **S1-T04 — Bootstrap worker application**
  - Select Celery or Dramatiq through ADR.
  - Add queue configuration, health reporting, sample idempotent job, retries, dead-letter strategy, and structured logs.
  - Acceptance:
    - sample job executes through Docker;
    - duplicate execution is handled safely;
    - timeout and retry behavior are tested.

- [ ] **S1-T05 — Add shared API contracts package**
  - Create a versioned approach for sharing generated OpenAPI types or schemas with the frontend.
  - Acceptance:
    - frontend does not maintain manually divergent API types;
    - contract generation is reproducible;
    - CI detects uncommitted generated contract changes if generated files are committed.

## Sprint 1.2 — Docker development environment

- [ ] **S1-T06 — Create base Docker Compose stack**
  - Add `web`, `api`, `worker`, `postgres`, `redis`, `minio`, and initialization services.
  - Use health checks, internal networks, named volumes, and restart policies appropriate for development.
  - Acceptance:
    - `docker compose up --build` succeeds on a clean machine;
    - only required host ports are exposed;
    - service readiness is verified, not based only on startup order.

- [ ] **S1-T07 — Harden container images**
  - Use multi-stage builds, non-root users, pinned base images, minimal runtime dependencies, and health checks.
  - Acceptance:
    - images do not contain development secrets;
    - runtime containers do not run as root where feasible;
    - vulnerability scan procedure is documented.

- [ ] **S1-T08 — Add development overrides**
  - Create `docker-compose.dev.yml` for hot reload, test mail, and developer-friendly mounts.
  - Acceptance:
    - production-like compose file does not depend on hot-reload mounts;
    - development mode is documented for PowerShell and Bash.

- [ ] **S1-T09 — Add root developer commands**
  - Add Makefile and Windows-friendly PowerShell scripts or equivalent task runner.
  - Commands: bootstrap, dev, stop, logs, lint, typecheck, test, integration, e2e, migrate, seed, backup, restore.
  - Acceptance:
    - commands invoke Docker consistently;
    - command help exists;
    - destructive commands require explicit confirmation.

- [ ] **S1-T10 — Create `.env.example` and configuration reference**
  - Include all required variables with safe empty or local defaults.
  - Create `docs/runbooks/CONFIGURATION.md`.
  - Acceptance:
    - no real secret is present;
    - every variable documents purpose, format, and restart requirement;
    - configuration validation tests exist.

## Sprint 1.3 — Code quality and CI

- [ ] **S1-T11 — Configure backend quality tooling**
  - Add Ruff, mypy, Pytest, coverage, import boundary checks, and dependency auditing.
  - Acceptance:
    - strict type checking baseline is documented;
    - generated/migration code exclusions are minimal and justified;
    - checks run from a single root command.

- [ ] **S1-T12 — Configure frontend quality tooling**
  - Add ESLint, Prettier, TypeScript strict mode, Vitest, Testing Library, and accessibility checks.
  - Acceptance:
    - format and lint are deterministic;
    - no blanket `any` allowance;
    - tests run headlessly.

- [ ] **S1-T13 — Add GitHub Actions CI**
  - Add secret-free lint, typecheck, unit test, build, migration, integration, and container validation jobs.
  - Acceptance:
    - PR checks fail on formatting, typing, test, or migration errors;
    - live Gemini/RHR/TED calls are disabled by default;
    - dependency caching does not cache secrets.

- [ ] **S1-T14 — Add dependency update and security policy**
  - Configure Dependabot or Renovate and create `SECURITY.md`.
  - Acceptance:
    - update grouping and review policy are documented;
    - security reporting channel is defined;
    - major updates are not auto-merged blindly.

- [ ] **S1-T15 — Add architecture decision record process**
  - Create ADR template and initial ADRs for stack, queue, pgvector, object storage, and deployment topology.
  - Acceptance:
    - accepted decisions match implemented foundations;
    - alternatives and consequences are recorded.

---

# Phase 2 — Identity, permissions, audit, and core persistence

## Sprint 2.1 — Database foundation

- [ ] **S2-T01 — Configure SQLAlchemy and Alembic**
  - Add async/sync strategy through ADR, connection pooling, transaction boundaries, and migration commands.
  - Acceptance:
    - clean migration succeeds;
    - rollback of initial migration is tested;
    - connection failures produce safe readiness errors.

- [ ] **S2-T02 — Add foundational database schema**
  - Implement users, roles, permissions, sessions, organizations/company profile shell, audit events, jobs, and system settings.
  - Acceptance:
    - critical uniqueness and foreign-key constraints exist;
    - timestamps are UTC;
    - soft delete is used only where justified.

- [ ] **S2-T03 — Enable pgvector**
  - Add extension migration and vector configuration.
  - Acceptance:
    - startup verifies extension availability;
    - dimension is configuration-compatible;
    - migration and similarity smoke test pass.

- [ ] **S2-T04 — Add repository/unit-of-work pattern**
  - Keep persistence details outside domain logic.
  - Acceptance:
    - use-case tests can use fake repositories;
    - transaction ownership is explicit;
    - no hidden commits occur inside repositories.

## Sprint 2.2 — Authentication and users

- [ ] **S2-T05 — Implement initial admin bootstrap**
  - Create one-time setup flow or controlled CLI command.
  - Acceptance:
    - default credentials do not exist;
    - bootstrap cannot recreate or overwrite an existing admin silently;
    - event is audited.

- [ ] **S2-T06 — Implement password authentication**
  - Use Argon2id, secure session design, rate limits, lockout/backoff, and generic errors.
  - Acceptance:
    - password hashes use reviewed parameters;
    - session cookie flags are tested;
    - brute-force controls exist;
    - password is never logged.

- [ ] **S2-T07 — Implement session management**
  - Support login, logout, session listing, expiration, revocation, and password-change invalidation.
  - Acceptance:
    - revoked sessions stop working immediately or within a documented bound;
    - CSRF is addressed;
    - session events are audited.

- [ ] **S2-T08 — Implement user administration**
  - Create, disable, reactivate, assign roles, and reset password through controlled flows.
  - Acceptance:
    - last active admin cannot be removed accidentally;
    - role changes invalidate authorization caches;
    - all changes are audited.

## Sprint 2.3 — Authorization and audit

- [ ] **S2-T09 — Implement permission policy engine**
  - Support global roles and object/workspace-level policy checks.
  - Acceptance:
    - deny-by-default behavior;
    - authorization enforced server-side;
    - permission matrix tests cover all roles.

- [ ] **S2-T10 — Implement append-only audit service**
  - Record actor, action, target, timestamp, correlation ID, safe metadata, before/after hashes where appropriate, and source IP/user agent where policy permits.
  - Acceptance:
    - normal users cannot edit/delete audit events;
    - sensitive values are redacted;
    - audit query access is restricted.

- [ ] **S2-T11 — Build audit UI**
  - Add filters by actor, action, workspace, date, and target.
  - Acceptance:
    - pagination works;
    - exported audit report is access-controlled;
    - hidden sensitive payload content is not exposed.

- [ ] **S2-T12 — Add authorization security tests**
  - Cover horizontal access, vertical escalation, protected downloads, exports, approvals, and audit access.
  - Acceptance:
    - tests fail when checks are removed;
    - every protected resource type has at least one negative test.

---

# Phase 3 — Object storage, files, and document processing

## Sprint 3.1 — Object storage and file integrity

- [ ] **S3-T01 — Implement MinIO storage adapter**
  - Separate originals, normalized artifacts, generated outputs, and temporary files.
  - Acceptance:
    - buckets are initialized idempotently;
    - protected files are not anonymously readable;
    - integration tests cover upload, stream, metadata, and deletion policy.

- [ ] **S3-T02 — Implement file metadata and immutable versions**
  - Store SHA-256, size, detected MIME, original name, storage key, source, classification, uploader, and acquisition time.
  - Acceptance:
    - duplicate detection works by hash within configured scope;
    - originals cannot be overwritten;
    - changed content creates a new version.

- [ ] **S3-T03 — Secure upload pipeline**
  - Add filename sanitation, MIME sniffing, limits, archive safety, content disposition, and temporary-file cleanup.
  - Acceptance:
    - path traversal fixtures are rejected;
    - oversized and unsupported files fail safely;
    - upload errors do not leave orphaned database/storage state.

- [ ] **S3-T04 — Add optional antivirus profile**
  - Integrate ClamAV or document the selected alternative.
  - Acceptance:
    - infected test signature is quarantined;
    - unavailable scanner behavior follows policy;
    - scan result is visible and audited.

## Sprint 3.2 — Parsing and OCR

- [ ] **S3-T05 — Define normalized document model**
  - Represent pages, headings, paragraphs, tables, lists, cells, metadata, and source locations.
  - Acceptance:
    - model supports citation reconstruction;
    - parser-specific fields do not leak into domain contracts;
    - schema is versioned.

- [ ] **S3-T06 — Implement PDF parser**
  - Extract text, page boundaries, metadata, links, and table candidates.
  - Acceptance:
    - fixtures preserve page citations;
    - encrypted/invalid PDFs fail visibly;
    - scanned PDF detection triggers OCR eligibility.

- [ ] **S3-T07 — Implement DOCX parser**
  - Extract headings, paragraphs, tables, lists, headers/footers where relevant, and document properties.
  - Acceptance:
    - heading hierarchy is preserved;
    - table cell locations are citeable;
    - embedded unsafe content is not executed.

- [ ] **S3-T08 — Implement XLSX parser**
  - Extract sheet names, cells, formulas and displayed values, merged regions, hidden-sheet metadata, and print areas where useful.
  - Acceptance:
    - formulas are not executed by the server;
    - source cell references are preserved;
    - large-sheet limits are enforced.

- [ ] **S3-T09 — Implement HTML, XML, TXT, and image ingestion**
  - Sanitize HTML, parse XML safely, detect encoding, and preserve image metadata.
  - Acceptance:
    - XXE is prevented;
    - HTML scripts do not execute;
    - unsupported encodings have clear errors.

- [ ] **S3-T10 — Implement local OCR**
  - Use Tesseract with Estonian and English language packs.
  - Store OCR confidence and page mapping.
  - Acceptance:
    - scanned Estonian fixture becomes searchable;
    - low-confidence result is visibly flagged;
    - OCR has CPU/memory/time limits.

- [ ] **S3-T11 — Create document processing job pipeline**
  - Stages: validate, scan, parse, OCR fallback, normalize, chunk, index, quality report.
  - Acceptance:
    - stages are idempotent;
    - progress and failures are visible;
    - retries do not duplicate versions or chunks;
    - dead-letter recovery is documented.

## Sprint 3.3 — Chunking and retrieval

- [ ] **S3-T12 — Implement structure-aware chunking**
  - Chunk by document structure with overlap, table handling, metadata, and stable hashes.
  - Acceptance:
    - chunks preserve citation boundaries;
    - reprocessing unchanged content reuses stable identifiers where possible;
    - large sections are bounded.

- [ ] **S3-T13 — Implement embedding provider interface**
  - Support Gemini embeddings and a mock/local test provider.
  - Acceptance:
    - embedding calls are policy-gated;
    - model/dimension metadata is stored;
    - changing model creates a distinct index version.

- [ ] **S3-T14 — Implement hybrid retrieval**
  - Combine metadata filters, lexical search, and vector similarity.
  - Acceptance:
    - workspace and permission filters occur before results return;
    - result includes score components and citations;
    - retrieval quality tests use sanitized fixtures.

- [ ] **S3-T15 — Build document viewer with citations**
  - Show original/normalized content, page/section navigation, parse quality, and citation deep links.
  - Acceptance:
    - keyboard navigation works;
    - users can copy a stable citation reference;
    - permissions protect both viewer and downloads.

---

# Phase 4 — Company knowledge and evidence library

## Sprint 4.1 — Company profile

- [ ] **S4-T01 — Implement Eventnexus OÜ profile model and UI**
  - Include legal details, contacts, languages, delivery locations, industries, technologies, service categories, capacity, exclusions, and risk preferences.
  - Acceptance:
    - factual fields distinguish evidence status;
    - edits are versioned and audited;
    - required fields are validated.

- [ ] **S4-T02 — Implement CPV interest model**
  - Support CPV codes, hierarchy, include/exclude rules, weights, and notes.
  - Acceptance:
    - imported notices can match parent/child codes;
    - exclusions override inclusions according to documented rules;
    - scoring tests cover hierarchy behavior.

- [ ] **S4-T03 — Implement capabilities and technologies**
  - Add proficiency/evidence, service type, delivery mode, recency, and strategic priority.
  - Acceptance:
    - unsupported capability cannot be marked verified;
    - expired or weak evidence is visible.

## Sprint 4.2 — Evidence

- [ ] **S4-T04 — Implement reference project library**
  - Store customer, scope, dates, value range, technologies, outcomes, contact restrictions, confidentiality, and supporting documents.
  - Acceptance:
    - public and confidential references are distinguishable;
    - expired permission or NDA restriction blocks reuse;
    - claims link to evidence.

- [ ] **S4-T05 — Implement staff profile and CV evidence**
  - Store roles, skills, experience, certifications, languages, availability, and approved CV content.
  - Acceptance:
    - personal data policy is enforced;
    - AI cannot infer unverified experience;
    - CV exports use approved facts only.

- [ ] **S4-T06 — Implement certificate and policy evidence**
  - Track issuer, identifier, validity, scope, file, and verification state.
  - Acceptance:
    - expiry warnings exist;
    - invalid evidence cannot satisfy a requirement silently.

- [ ] **S4-T07 — Implement approved content blocks**
  - Store reusable company descriptions, methodologies, security text, quality processes, sustainability text, and standard commitments.
  - Acceptance:
    - blocks are versioned and approved;
    - language variants are linked;
    - AI-generated edits create drafts, not replacements.

- [ ] **S4-T08 — Implement evidence search and permissions**
  - Support metadata and semantic search within allowed evidence.
  - Acceptance:
    - confidential evidence respects workspace permissions;
    - search results show validity and approval state;
    - retrieval tests prevent cross-workspace leakage.

---

# Phase 5 — Opportunity ingestion and discovery

## Sprint 5.1 — Normalized opportunity domain

- [ ] **S5-T01 — Implement opportunity and source version schema**
  - Include source identifiers, notice version, title, buyer, procedure, CPV, lots, value, currency, deadlines, contacts, locations, languages, status, URLs, and raw payload reference.
  - Acceptance:
    - raw and normalized data are linked;
    - source amendments create versions;
    - deadlines preserve original text and timezone.

- [ ] **S5-T02 — Implement lot model**
  - Support lot-specific scope, CPV, value, deadline, evaluation, eligibility, and decision.
  - Acceptance:
    - multi-lot notices can be assessed per lot;
    - parent opportunity status is derived predictably.

- [ ] **S5-T03 — Implement deterministic deduplication**
  - Use source ID, cross-source identifiers, buyer/title/date similarity, and manual merge/split controls.
  - Acceptance:
    - no source record is deleted during deduplication;
    - merge rationale is stored;
    - false merge can be reversed.

## Sprint 5.2 — Manual import

- [ ] **S5-T04 — Implement manual notice creation/import**
  - Accept source URL, reference number, notes, and attachments.
  - Acceptance:
    - manual import can create a complete workspace without live adapters;
    - duplicate warning appears before creation;
    - original files and source notes are preserved.

- [ ] **S5-T05 — Implement notice payload import**
  - Import approved RHR/TED JSON/XML/ZIP fixtures.
  - Acceptance:
    - validation errors identify field and source;
    - unsupported versions are retained and marked for manual handling;
    - import is idempotent.

## Sprint 5.3 — RHR adapter

- [ ] **S5-T06 — Implement approved RHR client**
  - Follow the selected ADR only.
  - Add allowlisted host, timeouts, retries, rate limits, safe logging, and health check.
  - Acceptance:
    - contract tests use fixtures;
    - live integration is feature-flagged;
    - source outage does not corrupt existing data.

- [ ] **S5-T07 — Implement RHR normalization**
  - Map notices, lots, CPV, buyer, deadlines, contacts, values, languages, and status.
  - Acceptance:
    - mapping coverage report exists;
    - unknown fields are retained in raw data;
    - multi-lot and amendment fixtures pass.

- [ ] **S5-T08 — Implement RHR document retrieval/import**
  - Import only through approved public/authorized mechanisms.
  - Acceptance:
    - source filename and URL are preserved;
    - failed attachments can be retried individually;
    - unauthorized documents are not bypassed.

- [ ] **S5-T09 — Implement RHR incremental sync**
  - Use cursor/version strategy from discovery.
  - Acceptance:
    - restart resumes safely;
    - duplicate imports do not create duplicate opportunities;
    - amendment detection creates user-visible change events.

## Sprint 5.4 — TED adapter

- [ ] **S5-T10 — Implement TED API client**
  - Support expert queries, syntax validation, iteration/pagination, timeouts, and retries.
  - Acceptance:
    - client handles result limits correctly;
    - queries and fields are configuration-driven;
    - fixtures and optional live smoke tests exist.

- [ ] **S5-T11 — Implement TED eForms normalization**
  - Map notice, procedure, lots, organizations, CPV, values, deadlines, languages, and downloadable formats.
  - Acceptance:
    - Estonian and English fixtures pass;
    - eForms version is recorded;
    - unknown notice types degrade safely.

- [ ] **S5-T12 — Implement TED incremental sync**
  - Store cursor and retrieve updates within configured scope.
  - Acceptance:
    - sync is idempotent;
    - source freshness and last error are visible;
    - rate limiting is respected.

## Sprint 5.5 — Opportunity inbox

- [ ] **S5-T13 — Build opportunity list and filters**
  - Filter by source, status, buyer, CPV, date, deadline, value, language, score, and assignment.
  - Acceptance:
    - pagination and sorting are server-side;
    - saved filter presets exist;
    - source freshness is shown.

- [ ] **S5-T14 — Build opportunity detail view**
  - Show normalized data, raw source link, lots, documents, changes, score, and decisions.
  - Acceptance:
    - source/version history is accessible;
    - missing/uncertain fields are clearly marked;
    - accessibility checks pass.

- [ ] **S5-T15 — Implement amendment change summary**
  - Compare normalized versions and identify changed deadlines, documents, scope, evaluation, values, and contacts.
  - Acceptance:
    - deterministic diff exists before AI summary;
    - important changes can invalidate decisions/workspaces;
    - users can inspect both versions.

---

# Phase 6 — Opportunity matching and GO/NO-GO

## Sprint 6.1 — Deterministic scoring

- [ ] **S6-T01 — Define scoring configuration**
  - Factors: CPV, keywords, technologies, service fit, value, geography, deadline, capacity, evidence coverage, buyer history, exclusions, and strategic priority.
  - Acceptance:
    - weights are configurable and versioned;
    - hard disqualifiers are not hidden inside a weighted score;
    - scoring version is stored with each result.

- [ ] **S6-T02 — Implement deterministic scoring engine**
  - Produce total score and factor breakdown.
  - Acceptance:
    - same inputs and version produce same result;
    - tests cover positive, negative, missing, and conflicting signals;
    - explanations do not require AI.

- [ ] **S6-T03 — Implement capacity and deadline risk rules**
  - Compare tender deadlines and likely delivery needs to current capacity/configured constraints.
  - Acceptance:
    - result is advisory and transparent;
    - timezone and business-day calculations are tested;
    - insufficient data is not treated as low risk.

## Sprint 6.2 — AI-assisted fit analysis

- [ ] **S6-T04 — Implement opportunity classification schema and prompt**
  - Output fit summary, matched capabilities, gaps, disqualifiers, partner needs, assumptions, questions, and confidence.
  - Acceptance:
    - every result is schema-validated;
    - company facts require evidence IDs;
    - prompt injection fixtures fail safely.

- [ ] **S6-T05 — Implement combined fit assessment**
  - Combine deterministic score with AI analysis without allowing AI to overwrite hard rules.
  - Acceptance:
    - UI separates deterministic and AI factors;
    - missing evidence is visible;
    - AI outage leaves deterministic scoring usable.

- [ ] **S6-T06 — Build GO/NO-GO review workflow**
  - Include decision, selected lots, reason, owner, due date, required partner, risks, and review record.
  - Acceptance:
    - final decision requires human action;
    - decisions are audited;
    - source amendment can reopen the decision.

- [ ] **S6-T07 — Add opportunity assignment and watchlist**
  - Assign owner/reviewer, set follow-up date, and watch changes.
  - Acceptance:
    - permissions are enforced;
    - overdue decisions are visible;
    - assignment changes are audited.

---

# Phase 7 — Tender workspace and analysis

## Sprint 7.1 — Workspace foundation

- [ ] **S7-T01 — Implement tender workspace creation**
  - Create from opportunity/lot or manual entry.
  - Acceptance:
    - workspace snapshots source version;
    - selected lots are explicit;
    - duplicate active workspace warning exists.

- [ ] **S7-T02 — Implement workspace membership and assignments**
  - Add owner, authors, reviewers, commercial approver, authorized submitter, and viewers.
  - Acceptance:
    - separation-of-duty policy is configurable;
    - object-level authorization tests pass.

- [ ] **S7-T03 — Build workspace dashboard**
  - Show deadline, phase, documents, requirements, unresolved gaps, assignments, AI usage, approvals, and recent activity.
  - Acceptance:
    - approaching deadline is prominent;
    - stale source warning is visible;
    - data is permission-filtered.

## Sprint 7.2 — Requirement extraction

- [ ] **S7-T04 — Define requirement taxonomy and schema**
  - Categories include eligibility, exclusion, mandatory technical, scored technical, commercial, contractual, security, privacy, team, reference, financial, form, signature, submission, and schedule.
  - Acceptance:
    - schema supports source citation, evidence, response, owner, status, risk, and questions;
    - requirement version history is defined.

- [ ] **S7-T05 — Implement requirement extraction pipeline**
  - Retrieve relevant chunks, call Gemini with structured output, validate citations, deduplicate candidates, and create review queue.
  - Acceptance:
    - no extracted requirement becomes approved automatically;
    - every candidate has a valid source reference;
    - bounded retries and cost checks exist.

- [ ] **S7-T06 — Implement deterministic date and amount extraction checks**
  - Cross-check model output against regex/parser candidates for deadlines, values, percentages, durations, and counts.
  - Acceptance:
    - conflicts are flagged;
    - locale-specific date/decimal formats are tested;
    - original text is preserved.

- [ ] **S7-T07 — Build requirement review UI**
  - Approve, edit, reject, merge, split, assign, and comment on candidate requirements.
  - Acceptance:
    - source excerpt is visible beside the requirement;
    - edits preserve extraction history;
    - bulk approval cannot bypass missing citation validation.

- [ ] **S7-T08 — Implement requirement completeness checks**
  - Detect missing analysis coverage by document, section, form, and category.
  - Acceptance:
    - completeness is not claimed solely from model confidence;
    - unparsed/failed documents block final readiness.

## Sprint 7.3 — Compliance matrix

- [ ] **S7-T09 — Implement compliance item model**
  - Fields: requirement, status, owner, response, evidence, document/section target, due date, risk, reviewer, and decision notes.
  - Acceptance:
    - status transitions are validated;
    - compliant status requires evidence or reviewed explanation;
    - changes are audited.

- [ ] **S7-T10 — Build compliance matrix UI**
  - Support filters, bulk assignment, source navigation, evidence linking, comments, and export.
  - Acceptance:
    - large matrices remain usable;
    - keyboard and screen-reader behavior is tested;
    - unresolved mandatory items are prominent.

- [ ] **S7-T11 — Implement AI compliance assistant**
  - Suggest evidence matches, draft responses, detect gaps, and identify contradictions.
  - Acceptance:
    - suggestions do not change approved status;
    - evidence permissions are enforced;
    - unsupported claim detection is included.

- [ ] **S7-T12 — Implement clarification question workflow**
  - Draft questions, link to source/requirement, review, mark sent manually, record response, and update analysis.
  - Acceptance:
    - system does not send automatically in MVP;
    - response documents are versioned;
    - affected requirements are re-evaluated.

---

# Phase 8 — Research and source-grounded intelligence

## Sprint 8.1 — Research domain

- [ ] **S8-T01 — Implement research task model**
  - Store objective, scope, allowed tools/sources, owner, freshness requirement, status, budget, findings, and citations.
  - Acceptance:
    - unbounded open-web research is not the default;
    - external research respects workspace classification;
    - findings remain separate from approved evidence.

- [ ] **S8-T02 — Implement research source model**
  - Store URL/source ID, publisher, title, date, retrieval time, excerpt, hash, confidence, and access notes.
  - Acceptance:
    - source provenance is visible;
    - stale or inaccessible sources are marked;
    - duplicate sources are detected.

- [ ] **S8-T03 — Implement bounded research planner**
  - Generate structured plans with allowed tools, queries, stopping criteria, and expected output.
  - Acceptance:
    - maximum steps and cost are enforced;
    - user can edit/approve the plan;
    - documents cannot expand tool permissions through prompt injection.

## Sprint 8.2 — Research workflows

- [ ] **S8-T04 — Implement contracting-authority research**
  - Cover public mission, current initiatives, procurement history, technology context, and stated strategy using approved sources.
  - Acceptance:
    - all findings have citations;
    - speculative conclusions are labeled;
    - personal profiling is excluded.

- [ ] **S8-T05 — Implement historical procurement research**
  - Find relevant prior notices, awards, framework agreements, suppliers, values, and recurring needs where public data permits.
  - Acceptance:
    - historical and current facts are distinguished;
    - award data is not treated as confidential insight;
    - source dates are visible.

- [ ] **S8-T06 — Implement technology and delivery research**
  - Research public technical standards, integration ecosystems, mandatory norms, and likely implementation dependencies.
  - Acceptance:
    - current official/primary technical sources are preferred;
    - unsupported architecture assumptions are labeled.

- [ ] **S8-T07 — Implement market and partner-gap research**
  - Identify partner categories and capability gaps without automatically selecting or contacting companies.
  - Acceptance:
    - recommendations state criteria and evidence;
    - no partner facts are invented;
    - contact actions are human-controlled.

- [ ] **S8-T08 — Build research review UI**
  - Approve findings for use, reject, request more research, and link to proposal/evidence.
  - Acceptance:
    - approved research still remains external evidence with source date;
    - changes are audited;
    - stale findings can be invalidated.

---

# Phase 9 — Gemini platform and AI governance implementation

## Sprint 9.1 — Provider and policies

- [ ] **S9-T01 — Implement generic AI provider interface**
  - Support structured generation, embeddings, health check, token/cost metadata, and cancellation.
  - Acceptance:
    - domain code has no Google SDK imports;
    - mock provider supports deterministic tests.

- [ ] **S9-T02 — Implement Gemini adapter**
  - Use the official Google Gen AI SDK.
  - Add configurable models, timeouts, retries, safety settings, structured output, and response metadata.
  - Acceptance:
    - no model is hard-coded in domain logic;
    - API key never appears in logs;
    - schema-invalid and rate-limited responses are handled.

- [ ] **S9-T03 — Implement AI external-processing policy engine**
  - Evaluate document classification, workspace policy, user permission, feature flag, redaction requirement, provider health, and budget.
  - Acceptance:
    - default deny for unknown classification;
    - policy decision is testable and audited;
    - UI explains blocked calls.

- [ ] **S9-T04 — Implement redaction pipeline**
  - Support configured personal identifiers, secrets, contact data, and custom terms while preserving citation mapping where possible.
  - Acceptance:
    - redaction is deterministic and tested;
    - redacted content cannot be reconstructed from logs;
    - users can inspect safe redaction summaries.

- [ ] **S9-T05 — Implement AI invocation ledger**
  - Store actor, purpose, provider, model, prompt version, input hashes, allowed source IDs, token usage, cost estimate, duration, status, and response hash.
  - Acceptance:
    - prompt content logging is off by default;
    - restricted content is not duplicated into ledger;
    - administrators can audit usage.

## Sprint 9.2 — Prompt and evaluation infrastructure

- [ ] **S9-T06 — Create prompt registry**
  - Load versioned prompts and schemas from repository assets.
  - Acceptance:
    - missing/invalid prompt fails startup or feature validation clearly;
    - prompt version is recorded in invocation;
    - changes are code-reviewed.

- [ ] **S9-T07 — Implement AI job limits**
  - Enforce max steps, timeout, input size, output size, retries, concurrency, and cost.
  - Acceptance:
    - agent loops cannot run indefinitely;
    - cancellation leaves consistent state;
    - budget-exhausted path is tested.

- [ ] **S9-T08 — Build sanitized AI evaluation harness**
  - Support fixture datasets, expected schemas, citation metrics, claim checks, language checks, latency, and estimated cost.
  - Acceptance:
    - evaluations run without production data;
    - result history can compare model/prompt versions;
    - minimum quality gates are documented.

- [ ] **S9-T09 — Add prompt-injection regression suite**
  - Include malicious instructions in PDFs, DOCX, HTML, comments, tables, and filenames.
  - Acceptance:
    - tool permissions cannot be expanded;
    - secrets are never exposed;
    - malicious instructions are treated as source data.

- [ ] **S9-T10 — Add unsupported-claim detection tests**
  - Attempt to induce fabricated references, certifications, CV facts, turnover, prices, and dates.
  - Acceptance:
    - outputs are blocked or labeled missing evidence;
    - regressions fail CI evaluation gates where deterministic.

---

# Phase 10 — Proposal planning and drafting

## Sprint 10.1 — Proposal structure

- [ ] **S10-T01 — Implement proposal template model**
  - Store template version, sections, required variables, language, style rules, and export mapping.
  - Acceptance:
    - templates are immutable after release;
    - new version does not alter existing packages;
    - validation catches missing required fields.

- [ ] **S10-T02 — Implement proposal section and version model**
  - Store status, author, source requirements, evidence, draft text, assumptions, comments, and approval state.
  - Acceptance:
    - edits create versions or concurrency-safe revisions;
    - approved text changes invalidate approval.

- [ ] **S10-T03 — Implement proposal architect workflow**
  - Generate outline and requirement coverage plan.
  - Acceptance:
    - every mandatory requirement is mapped or marked unresolved;
    - outline is reviewable before drafting;
    - schema validation and citations exist.

## Sprint 10.2 — Draft generation

- [ ] **S10-T04 — Implement evidence pack builder**
  - Retrieve only approved company evidence, reviewed tender requirements, and approved research for a section.
  - Acceptance:
    - permission and classification filters apply;
    - pack has token/size limits;
    - every item has a source ID.

- [ ] **S10-T05 — Implement section drafting workflow**
  - Plan, retrieve, draft, validate claims, validate requirement coverage, and create a reviewable version.
  - Acceptance:
    - no draft is auto-approved;
    - unsupported claims are blocked or highlighted;
    - assumptions are explicit;
    - Estonian output is default.

- [ ] **S10-T06 — Implement technical approach drafting**
  - Cover architecture, delivery method, integration, testing, deployment, support, documentation, and transition according to tender needs.
  - Acceptance:
    - commitments map to requirements;
    - non-applicable boilerplate is avoided;
    - technical claims cite approved capabilities/evidence.

- [ ] **S10-T07 — Implement project plan drafting**
  - Generate milestones, work packages, deliverables, dependencies, roles, acceptance, and timeline assumptions.
  - Acceptance:
    - dates and durations remain editable structured data;
    - impossible schedule conflicts are flagged;
    - plan can export to tables.

- [ ] **S10-T08 — Implement risk register drafting**
  - Generate risks, causes, probability, impact, mitigation, contingency, owner, and requirement linkage.
  - Acceptance:
    - tender-specific and company-specific risks are distinguished;
    - risk scoring is deterministic where numeric.

- [ ] **S10-T09 — Implement security and privacy section drafting**
  - Use approved policies and tender requirements.
  - Acceptance:
    - certifications and controls require evidence;
    - no generic security claim is presented as implemented fact without evidence;
    - legal review markers exist.

- [ ] **S10-T10 — Implement executive summary drafting**
  - Generate only after core sections and differentiators are reviewed.
  - Acceptance:
    - summary does not introduce new claims;
    - coverage and unsupported-claim validation pass.

## Sprint 10.3 — Editing and consistency

- [ ] **S10-T11 — Build proposal editor**
  - Support structured sections, comments, suggestions, citations, evidence panel, requirement links, and version history.
  - Acceptance:
    - concurrent edits are detected;
    - pasted content is sanitized;
    - autosave does not overwrite newer versions.

- [ ] **S10-T12 — Implement terminology glossary**
  - Store tender-defined terms, company terms, forbidden/required wording, translations, and abbreviations.
  - Acceptance:
    - terminology checks are deterministic;
    - language agent uses but cannot silently rewrite protected terms.

- [ ] **S10-T13 — Implement consistency review**
  - Check names, dates, numbers, roles, scope, deliverables, terms, cross-references, and duplicated/conflicting commitments.
  - Acceptance:
    - numeric conflicts identify both sources;
    - fixes are suggestions requiring review.

- [ ] **S10-T14 — Implement red-team review workflow**
  - Challenge compliance, evidence, ambiguity, delivery risk, overcommitment, security, and scoring weaknesses.
  - Acceptance:
    - findings have severity and source;
    - unresolved high findings block final approval unless explicitly accepted by authorized reviewer.

---

# Phase 11 — Pricing and commercial preparation

## Sprint 11.1 — Pricing model

- [ ] **S11-T01 — Define pricing schema**
  - Support fixed price, time and materials, unit prices, roles/rates, milestones, options, discounts, contingency, indexation, travel, licenses, third parties, VAT, and currency.
  - Acceptance:
    - calculations use decimal types;
    - gross/net and VAT basis are explicit;
    - tender pricing forms can map to structured fields.

- [ ] **S11-T02 — Implement deterministic pricing calculator**
  - Acceptance:
    - formulas are versioned and testable;
    - totals reconcile;
    - rounding rules are configurable;
    - AI is not the calculator of record.

- [ ] **S11-T03 — Implement pricing scenarios**
  - Create base, conservative, aggressive, and custom scenarios with assumptions and sensitivity.
  - Acceptance:
    - scenarios do not overwrite each other;
    - margin and risk effects are transparent;
    - final scenario requires human selection.

- [ ] **S11-T04 — Implement tender pricing-form mapping**
  - Map structured pricing to XLSX/DOCX fields where templates permit.
  - Acceptance:
    - formulas and required cells are validated;
    - exported totals match internal calculator;
    - hidden/locked sheet behavior is documented.

## Sprint 11.2 — Commercial approval

- [ ] **S11-T05 — Build pricing UI**
  - Show inputs, formulas, assumptions, scenario comparison, and validation.
  - Acceptance:
    - no silent rounding or currency conversion;
    - manual override requires reason;
    - permission checks exist.

- [ ] **S11-T06 — Implement commercial approval**
  - Separate pricing approval from general content approval.
  - Acceptance:
    - approval stores scenario/version hash;
    - price change invalidates approval;
    - authorized role is required.

- [ ] **S11-T07 — Implement commercial risk checks**
  - Flag negative margin, missing costs, inconsistent units, unrealistic effort, uncapped liability markers, guarantees, and long payment terms when extracted.
  - Acceptance:
    - checks are advisory except configured hard blocks;
    - source citations exist for tender terms.

---

# Phase 12 — Review, approval, and package generation

## Sprint 12.1 — Review workflows

- [ ] **S12-T01 — Implement review assignment model**
  - Assign sections/requirements/pricing/documents with due dates and status.
  - Acceptance:
    - reviewers see only permitted workspaces;
    - overdue and blocked reviews are visible;
    - reassignment is audited.

- [ ] **S12-T02 — Implement comments and change requests**
  - Support threaded comments, mentions, resolution, and source links.
  - Acceptance:
    - resolved comments retain history;
    - comments cannot alter content directly;
    - notifications respect user settings.

- [ ] **S12-T03 — Implement readiness checks**
  - Deterministically evaluate documents, mandatory requirements, approvals, pricing, declarations, attachments, source freshness, and unresolved high risks.
  - Acceptance:
    - each failure links to corrective action;
    - AI cannot override readiness;
    - checks are versioned/tested.

## Sprint 12.2 — Approvals

- [ ] **S12-T04 — Implement section and requirement approval**
  - Acceptance:
    - exact version/hash stored;
    - modification invalidates approval;
    - approval event is append-only.

- [ ] **S12-T05 — Implement final package approval workflow**
  - Require completed readiness checks, content approval, pricing approval, required declarations, and authorized submitter.
  - Acceptance:
    - stale source version blocks approval;
    - separation of duties follows configuration;
    - approval produces immutable package snapshot.

- [ ] **S12-T06 — Implement rejection and re-approval flow**
  - Acceptance:
    - rejection reason required;
    - changed scope is visible;
    - previous approvals remain in history but inactive.

## Sprint 12.3 — Export

- [ ] **S12-T07 — Implement DOCX template renderer**
  - Acceptance:
    - required variables are validated;
    - tables, headings, page breaks, and Estonian characters render correctly;
    - template version is recorded.

- [ ] **S12-T08 — Implement controlled PDF conversion**
  - Use local LibreOffice headless or approved renderer.
  - Acceptance:
    - conversion runs in bounded container/process;
    - failure does not create a misleading valid-looking file;
    - output hash and renderer version are stored.

- [ ] **S12-T09 — Implement attachment manifest**
  - Include required/optional status, source requirement, filename, type, size, SHA-256, version, approver, and missing warning.
  - Acceptance:
    - filenames are deterministic and safe;
    - duplicate/forbidden names are detected;
    - manifest export exists.

- [ ] **S12-T10 — Implement submission package builder**
  - Produce ZIP plus human-readable checklist and machine-readable manifest.
  - Acceptance:
    - package contents exactly match approved snapshot;
    - package is reproducible;
    - package hash is stored;
    - temporary files are cleaned.

- [ ] **S12-T11 — Add export visual and content tests**
  - Acceptance:
    - golden/snapshot fixtures cover primary templates;
    - totals, dates, and required sections are checked;
    - PDF text extraction smoke test verifies output is not blank.

---

# Phase 13 — Submission handoff, deadlines, and notifications

## Sprint 13.1 — Submission handoff

- [ ] **S13-T01 — Build submission checklist UI**
  - Include official destination, deadline, selected lots, required files, signatures, declarations, filenames, and final checks.
  - Acceptance:
    - checklist is tied to approved package version;
    - expired approval/source change is visible;
    - no portal credential field exists.

- [ ] **S13-T02 — Implement submission record**
  - Store channel, submitted package hash, timestamp, actor, confirmation/reference number, notes, and receipt attachment.
  - Acceptance:
    - only authorized role can record submission;
    - record cannot claim automatic submission;
    - receipt is immutable/versioned.

- [ ] **S13-T03 — Implement post-submission status workflow**
  - Track clarification, amendment, presentation/demo, award, not-awarded, cancellation, and contract follow-up.
  - Acceptance:
    - result changes are audited;
    - learning data can be captured without exposing confidential content.

## Sprint 13.2 — Deadlines

- [ ] **S13-T04 — Implement deadline model and calendar views**
  - Support submission, clarification, review, internal approval, validity, guarantee, milestone, and source-update deadlines.
  - Acceptance:
    - UTC/original timezone are preserved;
    - Europe/Tallinn display is correct across DST;
    - conflicting dates are flagged.

- [ ] **S13-T05 — Implement deadline reminders**
  - Local in-app and optional email reminders.
  - Acceptance:
    - reminder schedule is configurable;
    - duplicate reminders are prevented;
    - missed worker execution recovers safely.

- [ ] **S13-T06 — Implement amendment urgency alerts**
  - Alert on changed deadlines, documents, evaluation, scope, or cancellation.
  - Acceptance:
    - alert links to deterministic diff;
    - affected approvals/readiness status update automatically.

## Sprint 13.3 — Notifications

- [ ] **S13-T07 — Implement notification service and preferences**
  - Events: assignment, review request, comment mention, deadline, amendment, failed job, policy block, package ready.
  - Acceptance:
    - user preferences and role permissions apply;
    - sensitive content is not placed in email by default;
    - delivery failures are visible.

- [ ] **S13-T08 — Implement SMTP adapter**
  - Acceptance:
    - credentials are secret-managed;
    - TLS validation remains enabled;
    - test profile uses local SMTP capture;
    - email sending requires explicit configured enablement.

---

# Phase 14 — UX, localization, and accessibility

## Sprint 14.1 — Design system

- [ ] **S14-T01 — Create UI design system**
  - Define typography, spacing, forms, tables, badges, alerts, dialogs, empty states, and risk/status semantics.
  - Acceptance:
    - no color-only status meaning;
    - components have accessibility tests;
    - responsive behavior is documented.

- [ ] **S14-T02 — Implement Estonian localization**
  - Cover navigation, errors, workflows, requirement categories, approval statuses, and date/number formats.
  - Acceptance:
    - no core screen contains untranslated hard-coded strings;
    - Estonian pluralization and formats are tested.

- [ ] **S14-T03 — Implement English localization**
  - Acceptance:
    - users can switch UI language;
    - original tender language remains distinguishable from UI translation.

## Sprint 14.2 — Workflow usability

- [ ] **S14-T04 — Add global search**
  - Search opportunities, workspaces, documents, requirements, evidence, and proposal sections within permissions.
  - Acceptance:
    - results are permission-filtered;
    - source type and workspace context are visible.

- [ ] **S14-T05 — Add command/action shortcuts**
  - Provide keyboard-accessible common actions without bypassing confirmation/authorization.
  - Acceptance:
    - destructive/high-risk actions still require explicit confirmation;
    - shortcuts are documented.

- [ ] **S14-T06 — Run end-to-end accessibility audit**
  - Target WCAG 2.2 AA for MVP workflows.
  - Acceptance:
    - automated and manual keyboard findings are documented;
    - critical issues are fixed before pilot.

- [ ] **S14-T07 — Run usability test with real procurement workflow**
  - Observe at least one complete pilot flow.
  - Acceptance:
    - friction points and errors are recorded;
    - critical blockers become tasks;
    - no test uses unapproved confidential data.

---

# Phase 15 — Security hardening and privacy operations

## Sprint 15.1 — Application security

- [ ] **S15-T01 — Complete application threat model**
  - Cover trust boundaries, users, files, network, external APIs, storage, jobs, exports, and backups.
  - Acceptance:
    - threats map to controls/tests;
    - residual risks and owners are recorded.

- [ ] **S15-T02 — Add security headers and browser protections**
  - CSP, frame restrictions, MIME sniffing protection, referrer policy, permissions policy, and secure cookies.
  - Acceptance:
    - CSP does not rely on unsafe wildcards without justification;
    - headers are integration-tested.

- [ ] **S15-T03 — Add SSRF and outbound request controls**
  - Host allowlists, DNS/IP validation, redirect checks, private network restrictions, and size/time limits.
  - Acceptance:
    - private metadata endpoints cannot be reached through user/model URLs;
    - tests cover redirects and DNS rebinding assumptions where practical.

- [ ] **S15-T04 — Add file-parser sandboxing/resource controls**
  - Acceptance:
    - parser CPU/memory/time are bounded;
    - crashing parser does not crash the API;
    - malicious fixture tests exist.

- [ ] **S15-T05 — Add dependency and container scanning**
  - Acceptance:
    - CI reports known vulnerabilities;
    - severity handling policy exists;
    - release blockers are defined.

- [ ] **S15-T06 — Add secrets scanning**
  - Acceptance:
    - pre-commit/CI scanner detects representative test secrets;
    - false-positive handling does not disable the scanner globally.

## Sprint 15.2 — Privacy and retention

- [ ] **S15-T07 — Implement retention policy engine**
  - Configure retention for source files, drafts, prompts/metadata, logs, audit, exports, temporary files, and deleted workspaces.
  - Acceptance:
    - legal/audit retention exceptions are supported;
    - deletion is logged;
    - temporary files have short automatic cleanup.

- [ ] **S15-T08 — Implement data export and deletion workflows**
  - Acceptance:
    - access is restricted and audited;
    - immutable audit/legal records follow policy;
    - storage and database cleanup remain consistent.

- [ ] **S15-T09 — Implement external-AI transfer report**
  - Show what workspace/document excerpts were eligible/sent, classification, purpose, provider, model, timestamp, and actor.
  - Acceptance:
    - report avoids exposing secret prompt content;
    - administrators can investigate policy compliance.

- [ ] **S15-T10 — Create privacy and incident runbooks**
  - Include credential leak, mistaken AI upload, malicious file, unauthorized access, source outage, and data corruption.
  - Acceptance:
    - containment, evidence preservation, notification decision, recovery, and lessons-learned steps exist.

## Sprint 15.3 — Security validation

- [ ] **S15-T11 — Run authorization penetration tests**
  - Acceptance:
    - horizontal/vertical escalation attempts are documented;
    - critical issues are fixed and regression-tested.

- [ ] **S15-T12 — Run prompt-injection/red-team assessment**
  - Acceptance:
    - model cannot expand tool access;
    - restricted files are not sent externally;
    - findings become regression fixtures.

- [ ] **S15-T13 — Run backup confidentiality review**
  - Acceptance:
    - backup access and encryption decision are documented;
    - secrets are not included unnecessarily;
    - restore does not weaken permissions.

---

# Phase 16 — Observability, backup, and operations

## Sprint 16.1 — Logging and metrics

- [ ] **S16-T01 — Standardize structured logging**
  - Add correlation/job/workspace IDs, safe error codes, and redaction.
  - Acceptance:
    - no full document/prompt logging by default;
    - log schema is documented;
    - redaction tests exist.

- [ ] **S16-T02 — Add application metrics**
  - HTTP, jobs, parsing, OCR, source sync, AI, opportunities, requirements, deadlines, approvals, and exports.
  - Acceptance:
    - no secrets or tender text in labels;
    - high-cardinality risks are controlled.

- [ ] **S16-T03 — Add optional Prometheus/Grafana profile**
  - Acceptance:
    - dashboards start through Docker profile;
    - default dashboard covers health, jobs, sources, AI costs, and deadlines;
    - Grafana is not publicly exposed by default.

- [ ] **S16-T04 — Add health/readiness diagnostics**
  - Check database, Redis, MinIO, worker, source adapters, Gemini configuration, and storage capacity.
  - Acceptance:
    - readiness distinguishes required and optional dependencies;
    - health response does not expose secrets.

## Sprint 16.2 — Backup and recovery

- [ ] **S16-T05 — Implement backup tooling**
  - Back up PostgreSQL, MinIO objects, templates, prompts, and essential configuration references.
  - Acceptance:
    - backup is consistent and timestamped;
    - partial failure is visible;
    - credentials are not embedded in archive names/logs.

- [ ] **S16-T06 — Implement restore tooling**
  - Acceptance:
    - restore to clean environment is documented;
    - schema/version compatibility is checked;
    - destructive overwrite requires confirmation.

- [ ] **S16-T07 — Run restore drill**
  - Acceptance:
    - complete pilot workspace is restored;
    - hashes and approvals remain verifiable;
    - recovery time and data loss window are recorded.

- [ ] **S16-T08 — Implement storage cleanup and quota monitoring**
  - Acceptance:
    - originals are never removed contrary to retention policy;
    - temp/orphan cleanup is idempotent;
    - low-storage alerts exist.

## Sprint 16.3 — Operational runbooks

- [ ] **S16-T09 — Create installation runbook**
  - Windows 11 Docker Desktop and Linux server paths.
  - Acceptance:
    - clean installation is tested;
    - firewall, ports, volumes, and secrets are documented.

- [ ] **S16-T10 — Create upgrade runbook**
  - Include backup, migration, image update, health verification, and rollback.
  - Acceptance:
    - no instruction edits historical migrations;
    - rollback limitations are explicit.

- [ ] **S16-T11 — Create source/AI outage runbook**
  - Acceptance:
    - manual import/local-only workflows remain usable;
    - users can see stale data and blocked AI state;
    - retries do not create cost storms.

---

# Phase 17 — Comprehensive testing and quality gates

## Sprint 17.1 — Automated coverage

- [ ] **S17-T01 — Establish backend coverage thresholds**
  - Focus thresholds on domain, policy, authorization, pricing, and workflow logic.
  - Acceptance:
    - exclusions are justified;
    - critical modules have higher thresholds than adapters/UI glue.

- [ ] **S17-T02 — Establish frontend coverage and accessibility gates**
  - Acceptance:
    - core workflows have component tests;
    - accessibility violations fail CI for selected critical rules.

- [ ] **S17-T03 — Build Testcontainers integration suite**
  - PostgreSQL, Redis, MinIO, and optional supporting services.
  - Acceptance:
    - suite runs isolated in CI;
    - tests clean up resources.

- [ ] **S17-T04 — Build Playwright MVP workflow suite**
  - Login, profile, import, scoring, workspace, requirements, compliance, drafting, approval, export, submission record.
  - Acceptance:
    - tests use sanitized generated fixtures;
    - screenshots/traces do not contain secrets.

- [ ] **S17-T05 — Add migration test matrix**
  - Empty DB, previous release DB, downgrade where supported, and invalid data cases.
  - Acceptance:
    - release cannot proceed with untested migration path.

## Sprint 17.2 — Reliability and performance

- [ ] **S17-T06 — Test job idempotency and recovery**
  - Kill/restart workers during import, parse, embedding, generation, and export.
  - Acceptance:
    - no duplicate versions/packages;
    - failed jobs can be resumed/retried safely.

- [ ] **S17-T07 — Run document-scale performance tests**
  - Test realistic large tender sets, long PDFs, XLSX tables, and scanned documents.
  - Acceptance:
    - memory/time limits are documented;
    - UI remains responsive through async jobs.

- [ ] **S17-T08 — Run opportunity sync performance tests**
  - Acceptance:
    - pagination/cursor handles realistic volumes;
    - deduplication and normalization remain bounded.

- [ ] **S17-T09 — Run AI cost and latency benchmarks**
  - Acceptance:
    - per-workflow estimates exist;
    - budget defaults are adjusted based on evidence;
    - expensive regressions are visible.

## Sprint 17.3 — Quality gates

- [ ] **S17-T10 — Define release checklist**
  - Include tests, migrations, security scan, backup, docs, evaluation, source adapters, and rollback.
  - Acceptance:
    - release cannot be marked ready with failed critical gate.

- [ ] **S17-T11 — Define AI quality gates**
  - Minimum requirement recall, citation correctness, unsupported-claim rate, schema success, and injection resistance.
  - Acceptance:
    - thresholds are based on sanitized evaluation set;
    - model/prompt change requires comparison report.

- [ ] **S17-T12 — Define procurement package quality gates**
  - Mandatory requirement coverage, file manifest, totals, approvals, source freshness, deadline, and package hash.
  - Acceptance:
    - deterministic gate runs before final approval.

---

# Phase 18 — Pilot and MVP hardening

## Sprint 18.1 — Pilot preparation

- [ ] **S18-T01 — Select a real pilot tender**
  - Prefer a manageable public IT tender with clear documents and sufficient time.
  - Acceptance:
    - data classification and Gemini use are approved;
    - no confidential customer material is used without permission;
    - pilot goals and owners are documented.

- [ ] **S18-T02 — Create pilot company evidence set**
  - Acceptance:
    - every claim has approved evidence;
    - outdated or unavailable evidence is marked;
    - personal data is minimized.

- [ ] **S18-T03 — Run full dry-run workflow**
  - Discovery/import through export and simulated submission record.
  - Acceptance:
    - time spent and manual interventions are measured;
    - failures and confusion become tasks;
    - no real submission occurs accidentally.

## Sprint 18.2 — Pilot execution

- [ ] **S18-T04 — Run requirement extraction evaluation on pilot**
  - Human expert creates or reviews gold-standard requirements.
  - Acceptance:
    - recall, precision, citation accuracy, and severity of misses are measured;
    - mandatory misses are resolved before use.

- [ ] **S18-T05 — Run proposal drafting evaluation**
  - Acceptance:
    - unsupported claims, omissions, language quality, and editing time are measured;
    - all generated commitments are reviewed.

- [ ] **S18-T06 — Run package validation and submission rehearsal**
  - Acceptance:
    - files, names, formats, totals, signatures, and checklist are verified;
    - authorized user confirms handoff usability.

- [ ] **S18-T07 — Record pilot outcome and lessons**
  - Create `docs/pilots/PILOT_001_REPORT.md` with sanitized findings.
  - Acceptance:
    - metrics compare baseline to product result;
    - security/privacy incidents or near misses are documented;
    - backlog is reprioritized.

## Sprint 18.3 — MVP release

- [ ] **S18-T08 — Resolve pilot-critical findings**
  - Acceptance:
    - no unresolved critical security, compliance, data-loss, or package-integrity issue;
    - accepted residual risks have owner and rationale.

- [ ] **S18-T09 — Complete MVP documentation**
  - User guide, admin guide, installation, backup, restore, AI policy, source integration, incident, and troubleshooting.
  - Acceptance:
    - a new authorized user can complete core workflow from documentation.

- [ ] **S18-T10 — Tag MVP release**
  - Acceptance:
    - release checklist passes;
    - database migration and rollback notes exist;
    - container images/configuration are reproducible;
    - changelog and known limitations are published.

## Milestone M6 / MVP exit checklist

- [ ] Clean Docker installation succeeds.
- [ ] Estonian-first UI is complete for core workflows.
- [ ] Authentication, authorization, and audit tests pass.
- [ ] Approved RHR ingestion works.
- [ ] TED ingestion works.
- [ ] Manual import works as fallback.
- [ ] Document parsing/OCR and citations work.
- [ ] Explainable matching and GO/NO-GO work.
- [ ] Requirements and compliance matrix work.
- [ ] Gemini calls are policy-gated, audited, schema-validated, and cost-limited.
- [ ] Proposal drafting uses approved evidence.
- [ ] Pricing is deterministic and human-approved.
- [ ] Final package readiness checks pass.
- [ ] Submission remains human-controlled.
- [ ] Backup/restore drill passes.
- [ ] Security and AI evaluation gates pass.
- [ ] Real pilot report is complete.

---

# Phase 19 — Post-MVP roadmap

These tasks must not delay the MVP unless explicitly promoted.

## Sprint 19.1 — Integrations

- [ ] **S19-T01 — Approved email inbox import**
  - Import procurement invitations and attachments from a dedicated mailbox.
  - Requires separate credential, privacy, and retention design.

- [ ] **S19-T02 — Calendar integration**
  - Export internal deadlines or integrate with an approved calendar provider.

- [ ] **S19-T03 — CRM/reference integration**
  - Sync approved customer/reference data from a selected system.

- [ ] **S19-T04 — Official registry integrations**
  - Add company/financial/public data only through documented official interfaces.

- [ ] **S19-T05 — Partner workspace/export**
  - Controlled partner evidence requests and package exchange without exposing unrelated tender data.

## Sprint 19.2 — Advanced intelligence

- [ ] **S19-T06 — Win/loss learning**
  - Analyze reviewed outcomes without learning from confidential data outside policy.

- [ ] **S19-T07 — Buyer and category trend dashboards**
  - Historical values, CPV demand, seasonality, awards, and participation trends.

- [ ] **S19-T08 — Local LLM fallback**
  - Add a provider adapter for approved local models and compare quality/cost/privacy.

- [ ] **S19-T09 — Multimodal document retrieval**
  - Evaluate image/table/diagram embeddings after text workflow is stable.

- [ ] **S19-T10 — Advanced proposal scoring simulation**
  - Estimate coverage against published evaluation criteria without claiming actual buyer scoring.

## Sprint 19.3 — Submission automation research

- [ ] **S19-T11 — Reassess official RHR supplier integration**
  - Repeat legal and technical discovery if official capabilities change.

- [ ] **S19-T12 — Design human-confirmed portal assistant**
  - Only if permitted; must show every action and never store identity secrets.

- [ ] **S19-T13 — Threat model identity/signing integration**
  - Required before any implementation involving ID-card, Smart-ID, Mobile-ID, or signing.

- [ ] **S19-T14 — Implement submission automation only after explicit approval**
  - Blocked by official support, legal approval, security review, and user authorization.

## Sprint 19.4 — Deployment evolution

- [ ] **S19-T15 — Multi-user LAN deployment hardening**
  - Internal TLS, reverse proxy, backups, resource sizing, and workstation/server separation.

- [ ] **S19-T16 — High availability assessment**
  - Only when operational need is proven.

- [ ] **S19-T17 — Public SaaS feasibility study**
  - Separate product, privacy, legal, tenancy, billing, and security architecture; not an extension of the local MVP by default.

---

# Deferred decisions log

Add unresolved product/technical decisions here with owner and target date.

| ID | Decision | Options | Owner | Target date | Status |
|---|---|---|---|---|---|
| D-001 | Approved RHR ingestion method | Official API / export / manual import / other approved method | Eventnexus OÜ | TBD | Open |
| D-002 | Gemini production account/tier | Paid Gemini Developer API / Vertex AI / other approved setup | Eventnexus OÜ | TBD | Open |
| D-003 | Queue implementation | Celery / Dramatiq | Engineering | Phase 1 | Open |
| D-004 | Backup encryption | Host-managed / application-managed / encrypted destination | Security owner | Phase 16 | Open |
| D-005 | First proposal DOCX template | Eventnexus branded / tender-specific baseline | Procurement owner | Phase 10 | Open |

# Work log template

Use this under an in-progress task when useful:

```markdown
### Work log — Sx-Tyy

**Plan**
- ...

**Changes**
- ...

**Verification**
- command: result

**Security/privacy impact**
- ...

**Known limitations / follow-up**
- ...

**Commit**
- `<sha> <message>`
```
