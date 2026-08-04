# EventNexus Hanke Keskond

Local-first, AI-assisted procurement intelligence and tender preparation workspace for **Eventnexus OÜ**.

> **Project status:** Pre-alpha / architecture and delivery planning
>
> **Primary market:** Estonia
>
> **Primary language:** Estonian (`et-EE`), with English support where tender material requires it
>
> **Deployment model:** Self-hosted on a local workstation or company server with Docker Compose
>
> **AI provider:** Google Gemini API through a configurable provider adapter

## 1. Product vision

EventNexus Hanke Keskond helps Eventnexus OÜ discover relevant IT procurement opportunities, understand tender requirements, perform evidence-backed background research, prepare compliant bid documents, coordinate internal review, and create a submission-ready package.

The system is intended to reduce repetitive procurement work without removing human responsibility. AI outputs are drafts and decision support. A named, authorized person must approve the final commercial terms, declarations, attachments, and submission.

The target workflow is:

1. Collect procurement notices from supported official data sources.
2. Normalize and deduplicate opportunities.
3. Match opportunities against the company profile, capabilities, references, exclusions, and capacity.
4. Rank opportunities and explain the score with evidence.
5. Create a tender workspace and ingest all available source documents.
6. Extract requirements, dates, eligibility conditions, evaluation criteria, forms, risks, and unanswered questions.
7. Build a traceable compliance matrix.
8. Run controlled AI-assisted research.
9. Draft technical, commercial, administrative, and supporting content.
10. Review every claim, number, requirement, and attachment.
11. Approve the package through a human-controlled workflow.
12. Export a deterministic submission package and checklist.
13. Record submission evidence and monitor later changes or clarification requests.

## 2. Important deployment clarification

The application itself runs locally in Docker and is not deployed as a public cloud service. However, Google Gemini is an external API. Any content sent to Gemini leaves the local Docker environment and is processed by Google according to the selected account, billing tier, contract, region, and applicable terms.

The product must therefore never describe itself as fully offline. It is **local-first with controlled external AI processing**.

Mandatory safeguards:

- classify documents before AI use;
- minimize and redact data sent to external APIs;
- require an explicit policy for confidential, personal, security-sensitive, or restricted documents;
- record what content was sent, to which model, for which purpose, by whom, and when;
- allow a local-only processing path that does not call Gemini;
- keep model names configurable instead of hard-coding a preview model;
- use a paid/contractually approved Gemini setup for production procurement data;
- never send secrets, credentials, private keys, access tokens, or signing material to a model.

## 3. Product principles

### 3.1 Human authority

- AI must not autonomously submit a tender, accept contractual terms, set a final binding price, sign a declaration, or impersonate an authorized representative.
- Every external action must show the exact payload or document to a human before execution.
- Approval records must identify the user, timestamp, version, and content hash.

### 3.2 Evidence before prose

- Every extracted requirement must link to its source document, page/section, and source text span when technically possible.
- Every generated factual claim must be linked to approved company evidence or a cited external source.
- Unsupported claims must be labeled as assumptions or open questions.
- The system must never invent references, certifications, staff experience, turnover, prices, dates, or compliance statements.

### 3.3 Deterministic workflow

- AI output must use JSON Schema or another validated structured format before entering business logic.
- Workflow state transitions are controlled by application code, not model prose.
- Generated files must be reproducible from versioned templates, source data, and approved content blocks.

### 3.4 Local ownership

- PostgreSQL, object storage, logs, prompt versions, generated files, and audit history remain under Eventnexus OÜ control.
- Docker services bind to localhost or a private network by default.
- External integrations are opt-in and individually configurable.

### 3.5 Procurement safety

- The system assists with legal and procurement work but does not replace a lawyer, procurement specialist, accountant, security officer, or authorized signatory.
- Changes to procurement law, tender documents, deadlines, or source APIs must be treated as time-sensitive.
- A late or incomplete package must never be marked ready merely because AI generated all sections.

## 4. Scope

### 4.1 MVP capabilities

#### Opportunity discovery

- Import Estonian procurement opportunities from approved Riigihangete Register open/public data mechanisms.
- Import EU notices from the TED Search API.
- Support manual URL, notice identifier, JSON/XML, ZIP, PDF, DOCX, XLSX, and email attachment import.
- Deduplicate notices and preserve source versions.
- Detect amendments, deadline changes, cancellations, and clarification updates when source data supports them.

#### Relevance and qualification

- Maintain an Eventnexus OÜ capability profile.
- Maintain CPV interests, positive keywords, negative keywords, regions, budget ranges, contract types, technologies, security constraints, and capacity limits.
- Produce a configurable relevance score with a transparent factor breakdown.
- Separate factual eligibility failures from subjective strategic fit.
- Support `GO`, `NO_GO`, `REVIEW_REQUIRED`, and `INSUFFICIENT_DATA` decisions.

#### Tender workspace

- Store source notices, attachments, versions, deadlines, contacts, lots, evaluation criteria, and clarification questions.
- Parse PDF, DOCX, XLSX, TXT, HTML, XML, and common image formats.
- Preserve original files and immutable hashes.
- Create page- or section-aware text chunks for retrieval.
- Track extraction quality and OCR confidence.

#### Requirement analysis

- Extract mandatory requirements, scored requirements, eligibility criteria, exclusion grounds, deliverables, milestones, service levels, security requirements, data protection requirements, forms, signatures, guarantees, insurance, references, team roles, pricing rules, and submission instructions.
- Generate a compliance matrix with status, owner, source citation, evidence, response, risk, and review fields.
- Detect conflicting dates and inconsistent requirements.
- Generate clarification questions without sending them automatically.

#### Research

- Run controlled research tasks for the contracting authority, business context, technology environment, likely delivery risks, market context, partner needs, and public historical procurement information.
- Store sources, retrieval timestamps, excerpts, and research confidence.
- Separate public-source research from internal company evidence.
- Require source citations for externally verifiable claims.

#### Proposal drafting

- Create a structured proposal outline from tender requirements.
- Draft technical approach, implementation plan, governance, team structure, quality assurance, security, privacy, support, maintenance, risk management, sustainability, and executive summary sections.
- Reuse only approved company content blocks and references.
- Generate Estonian by default and support controlled English output.
- Produce DOCX and PDF exports from versioned templates.
- Build a final attachment manifest and submission checklist.

#### Review and approval

- Support role-based review of requirements, claims, pricing, legal declarations, attachments, and the final package.
- Block approval when mandatory checks are unresolved.
- Store immutable approval events and package hashes.
- Allow controlled rejection, revision, and re-approval.

#### Submission handoff

- For the MVP, generate a submission-ready package and step-by-step handoff for the authorized user.
- Record the submitted version, timestamp, source portal, confirmation identifier, and uploaded receipt.
- Do not automate RHR login or final submission unless an official, permitted, tested integration is documented and approved.

### 4.2 Explicit MVP non-goals

- Autonomous legal advice or legal sign-off.
- Autonomous tender submission.
- Browser automation that bypasses portal controls, authentication requirements, CAPTCHA, rate limits, or terms of use.
- Storing Smart-ID, Mobile-ID, ID-card PIN codes, private signing keys, or reusable signing secrets.
- Fabricating company qualifications or staff CV content.
- Automatic final pricing without a human commercial decision.
- Public multi-tenant SaaS deployment.
- Full accounting, CRM, ERP, or contract-management replacement.
- Scraping as the default source strategy where an official API, feed, export, or manual import exists.

## 5. Official source strategy

### 5.1 Estonian Riigihangete Register (RHR)

RHR is the primary source for Estonian public procurement notices and tender participation. The implementation must start with a documented integration discovery task.

Preferred order:

1. officially documented public/open-data API;
2. officially provided downloadable open-data export;
3. stable public notice endpoint intended for reuse;
4. user-driven manual import;
5. browser-assisted collection only after legal, technical, and operational approval.

The adapter must not assume undocumented search endpoints are stable. Store raw source payloads and source version identifiers so parsing can be replayed.

Official entry points:

- https://riigihanked.riik.ee/
- https://www.fin.ee/riigihanked-riigiabi-osalused/riigihangete-register
- https://www.riigiteataja.ee/akt/112072025026

### 5.2 Tenders Electronic Daily (TED)

Use TED API 3 Search API for EU procurement notices when relevant. Implement pagination/iteration handling, query validation, rate limiting, source caching, and raw XML/JSON storage.

Official documentation:

- https://docs.ted.europa.eu/api/latest/search.html
- https://docs.ted.europa.eu/api/latest/
- https://docs.ted.europa.eu/eforms/latest/

### 5.3 Other future sources

Possible later integrations, each requiring a separate approval and adapter:

- official company registry data;
- Estonian public-sector document registers;
- contracting-authority websites;
- approved email inboxes;
- internal CRM or project-reference sources;
- EU funding and programme databases;
- partner or subcontractor evidence stores.

## 6. Proposed architecture

```mermaid
flowchart LR
    U[Local browser] --> W[Next.js web application]
    W --> A[FastAPI application API]
    A --> DB[(PostgreSQL + pgvector)]
    A --> OBJ[(MinIO object storage)]
    A --> R[(Redis)]
    A --> Q[Job queue]
    Q --> WK[Python worker]
    WK --> DOC[Document extraction and OCR]
    WK --> RHR[RHR source adapter]
    WK --> TED[TED source adapter]
    WK --> G[Gemini provider adapter]
    WK --> DB
    WK --> OBJ
    A --> AUD[Audit and approval service]
    A --> EXP[DOCX/PDF/export service]
    MON[Prometheus/Grafana] -. optional .-> A
    MON -. optional .-> WK
```

### 6.1 Recommended stack

| Area | Technology | Reason |
|---|---|---|
| Web UI | Next.js, React, TypeScript | Strong typed UI, server/client flexibility, mature document workflow ecosystem |
| API | Python 3.12, FastAPI, Pydantic | Excellent document/AI tooling and schema validation |
| Background jobs | Celery or Dramatiq with Redis | Retryable long-running imports, OCR, embeddings, and generation |
| Database | PostgreSQL | Reliable transactional business data |
| Vector search | pgvector | Keeps MVP operationally simple and local |
| Object storage | MinIO | S3-compatible local storage for originals and generated packages |
| AI SDK | Official Google Gen AI SDK behind an internal adapter | Avoid provider coupling in domain logic |
| Document extraction | PyMuPDF, python-docx, openpyxl, Apache Tika where useful | Broad local format support |
| OCR | Tesseract with Estonian and English language packs | Local scanned-document fallback |
| Document generation | docxtpl or python-docx, LibreOffice headless for controlled PDF conversion | Template-based reproducible output |
| Authentication | Local accounts, Argon2id, secure sessions/JWT as appropriate | Self-hosted RBAC |
| Testing | Pytest, Vitest, Playwright, Testcontainers | Unit, integration, and end-to-end coverage |
| Quality | Ruff, mypy, ESLint, Prettier | Enforced static quality |
| Observability | Structured logs, OpenTelemetry, Prometheus/Grafana profile | Auditable local operation |

A technology may be replaced only through an Architecture Decision Record (ADR) explaining the operational and security impact.

## 7. Service boundaries

### `web`

- Estonian-first interface;
- opportunity inbox and filters;
- tender workspace;
- document viewer with citations;
- compliance matrix;
- research and generation controls;
- review and approval UI;
- administration, policy, and audit views.

### `api`

- authentication and RBAC;
- domain commands and queries;
- workflow state transitions;
- validation;
- signed download links or protected local streaming;
- audit events;
- export orchestration;
- external action approval gates.

### `worker`

- source synchronization;
- document parsing and OCR;
- chunking and embedding;
- AI extraction and generation;
- research retrieval;
- file rendering;
- integrity scans;
- retries and dead-letter handling.

### `source adapters`

Every external procurement source implements a common contract:

```text
search(criteria) -> SourceNoticeSummary[]
fetch_notice(source_id, version?) -> RawNotice
fetch_documents(source_id) -> SourceDocument[]
check_updates(cursor) -> SourceChange[]
normalize(raw_notice) -> NormalizedOpportunity
health_check() -> AdapterHealth
```

Adapters must preserve raw source material and must not leak source-specific assumptions into the core tender domain.

### `AI provider adapter`

The domain layer must call internal capabilities such as:

```text
extract_requirements(input, schema, policy)
classify_opportunity(input, company_profile, schema)
generate_draft(context, approved_evidence, schema)
review_compliance(context, response, schema)
create_research_plan(question, allowed_tools, schema)
```

It must not call a hard-coded Gemini model directly from controllers or UI code.

## 8. Core domain model

Minimum entities:

- `User`
- `Role`
- `CompanyProfile`
- `Capability`
- `ReferenceProject`
- `PersonProfile`
- `PartnerProfile`
- `SourceConnection`
- `SourceCursor`
- `Opportunity`
- `OpportunityVersion`
- `Lot`
- `TenderWorkspace`
- `TenderDocument`
- `DocumentVersion`
- `DocumentChunk`
- `Requirement`
- `ComplianceItem`
- `ClarificationQuestion`
- `ResearchTask`
- `ResearchSource`
- `EvidenceItem`
- `ContentBlock`
- `ProposalSection`
- `PricingScenario`
- `Review`
- `Approval`
- `ExportPackage`
- `SubmissionRecord`
- `Notification`
- `AIInvocation`
- `PromptTemplate`
- `AuditEvent`

Important invariants:

- original source files are immutable;
- edits create new versions;
- citations refer to immutable document versions;
- generated claims require evidence or explicit assumption status;
- approvals refer to exact version hashes;
- an approved package becomes invalid when a mandatory source document changes;
- deadlines are stored in UTC with original timezone and source text preserved;
- monetary values store currency, net/gross status, and calculation basis;
- AI-generated output never directly mutates approved records.

## 9. Tender lifecycle

```text
DISCOVERED
  -> TRIAGE_REQUIRED
  -> QUALIFICATION_IN_PROGRESS
  -> GO | NO_GO | ON_HOLD
  -> DOCUMENTS_INCOMPLETE
  -> ANALYSIS_IN_PROGRESS
  -> DRAFTING
  -> INTERNAL_REVIEW
  -> CHANGES_REQUIRED
  -> APPROVAL_PENDING
  -> APPROVED_FOR_SUBMISSION
  -> SUBMISSION_IN_PROGRESS
  -> SUBMITTED
  -> CLARIFICATION
  -> AWARDED | NOT_AWARDED | CANCELLED | WITHDRAWN
  -> ARCHIVED
```

State changes must be permission-checked, validated, and audited. The model can recommend a transition but cannot perform protected transitions without application and human authorization.

## 10. AI and RAG design

### 10.1 Retrieval

- Index normalized document chunks locally in PostgreSQL/pgvector.
- Store chunk metadata: document version, page, heading path, table identity, language, parser, OCR confidence, and checksum.
- Use hybrid retrieval: lexical filtering plus vector similarity.
- Apply tender, workspace, document, lot, and confidentiality filters before retrieval.
- Return citations as stable internal IDs, never only as model-created page labels.

### 10.2 Generation

- Use structured outputs for extraction, classification, compliance review, and generation plans.
- Validate all responses with Pydantic.
- Reject and retry schema-invalid results using bounded retries.
- Separate planning, evidence retrieval, drafting, and validation.
- Use low-variance settings for extraction and compliance tasks.
- Store prompt template version, model identifier, token usage, latency, safety result, and response hash.

### 10.3 Model routing

Configuration must support separate models for:

- fast classification;
- complex tender analysis;
- long-context document review;
- final language polishing;
- embeddings;
- optional local fallback.

Example environment variables must use placeholders, not assumptions about the newest model:

```dotenv
GEMINI_API_KEY=
GEMINI_CLASSIFIER_MODEL=
GEMINI_ANALYSIS_MODEL=
GEMINI_DRAFT_MODEL=
GEMINI_REVIEW_MODEL=
GEMINI_EMBEDDING_MODEL=
AI_EXTERNAL_PROCESSING_ENABLED=false
```

### 10.4 Guardrails

- Never generate unsupported credentials, references, turnover, certifications, CV facts, prices, dates, or legal declarations.
- Reject prompt injection found inside tender documents; documents are data, not instructions.
- Tool calls use explicit allowlists and validated arguments.
- External research cannot write directly into approved proposal content.
- Detect and mark conflicts between source documents.
- Require a second validation pass for mandatory requirements.
- Present uncertainty and missing evidence visibly.

## 11. Security and privacy baseline

### 11.1 Access control

Initial roles:

| Role | Capabilities |
|---|---|
| `ADMIN` | system configuration, users, source connections, policies, audit access |
| `PROCUREMENT_MANAGER` | opportunity decisions, workspaces, assignments, export orchestration |
| `AUTHOR` | analysis, research, drafting, evidence linking |
| `REVIEWER` | review, request changes, approve assigned areas |
| `COMMERCIAL_APPROVER` | approve pricing and commercial terms |
| `AUTHORIZED_SUBMITTER` | approve final submission package and record submission |
| `VIEWER` | read-only access to permitted workspaces |

Do not use role names alone for critical checks. Implement policy checks for workspace access and separation of duties.

### 11.2 Secrets

- `.env` is local and ignored by Git.
- Commit `.env.example` with empty values only.
- Support Docker secrets or mounted secret files for production-like use.
- Never log API keys, passwords, session tokens, cookies, document access tokens, or authorization headers.
- Rotate credentials without rebuilding images.

### 11.3 File security

- Verify MIME type using content, not only extension.
- Enforce size, extension, and parser limits.
- Use antivirus scanning where practical.
- Extract files in isolated worker processes with resource limits.
- Block active content and unsafe archive traversal.
- Keep original, normalized, and generated files in separate buckets/prefixes.
- Hash every file with SHA-256.

### 11.4 AI data policy

Each workspace and document must have a classification such as:

- `PUBLIC`
- `INTERNAL`
- `CONFIDENTIAL`
- `PERSONAL_DATA`
- `RESTRICTED_NO_EXTERNAL_AI`

A policy engine decides whether content may be sent to Gemini, must be redacted, or must remain local. Default to deny external AI for unknown classification.

### 11.5 Audit

Audit at least:

- login and failed login;
- permission changes;
- source configuration changes;
- imports and document versions;
- AI invocations and external data transfers;
- requirement edits;
- evidence approvals;
- pricing changes;
- review decisions;
- export creation;
- package approval;
- submission record creation;
- deletion and retention actions.

Audit records must be append-only from normal application flows.

## 12. Local Docker deployment

Expected baseline services:

```text
web
api
worker
postgres
redis
minio
minio-init
ocr
```

Optional profiles:

```text
observability: prometheus, grafana, otel-collector
security: clamav
conversion: libreoffice
mail: local SMTP test service
```

Networking rules:

- expose only the web reverse proxy to the host by default;
- do not expose PostgreSQL, Redis, or MinIO publicly;
- use internal Docker networks;
- use health checks and dependency readiness checks;
- run containers as non-root where feasible;
- use read-only filesystems and dropped Linux capabilities where feasible;
- persist data in named volumes or explicitly configured host paths;
- provide documented backup and restore commands.

## 13. Planned repository structure

```text
.
├── README.md
├── AGENTS.md
├── TASKS.md
├── LICENSE
├── .env.example
├── .gitignore
├── .editorconfig
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile
├── apps/
│   ├── web/
│   ├── api/
│   └── worker/
├── packages/
│   ├── contracts/
│   ├── ui/
│   └── config/
├── services/
│   ├── document-converter/
│   └── ocr/
├── infrastructure/
│   ├── docker/
│   ├── observability/
│   └── backup/
├── templates/
│   ├── proposals/
│   └── exports/
├── prompts/
│   ├── extraction/
│   ├── matching/
│   ├── research/
│   ├── drafting/
│   └── review/
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── api/
│   ├── security/
│   ├── procurement/
│   └── runbooks/
├── tests/
│   ├── fixtures/
│   ├── integration/
│   ├── e2e/
│   └── security/
└── scripts/
```

## 14. Environment configuration

The final `.env.example` must document at least:

```dotenv
# Application
APP_ENV=development
APP_BASE_URL=http://localhost:3000
APP_TIMEZONE=Europe/Tallinn
APP_DEFAULT_LOCALE=et-EE
APP_ENCRYPTION_KEY=

# Authentication
SESSION_SECRET=
INITIAL_ADMIN_EMAIL=
INITIAL_ADMIN_PASSWORD=

# Database
POSTGRES_DB=eventnexus_hanked
POSTGRES_USER=eventnexus
POSTGRES_PASSWORD=
DATABASE_URL=postgresql+psycopg://eventnexus:change-me@postgres:5432/eventnexus_hanked

# Redis
REDIS_URL=redis://redis:6379/0

# Object storage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_SECURE=false
MINIO_BUCKET_ORIGINALS=tender-originals
MINIO_BUCKET_GENERATED=tender-generated

# Google Gemini
GEMINI_API_KEY=
GEMINI_CLASSIFIER_MODEL=
GEMINI_ANALYSIS_MODEL=
GEMINI_DRAFT_MODEL=
GEMINI_REVIEW_MODEL=
GEMINI_EMBEDDING_MODEL=
AI_EXTERNAL_PROCESSING_ENABLED=false
AI_LOG_PROMPT_CONTENT=false
AI_MAX_DAILY_COST_EUR=

# Procurement sources
RHR_SOURCE_ENABLED=false
RHR_BASE_URL=https://riigihanked.riik.ee
TED_SOURCE_ENABLED=false
TED_API_BASE_URL=https://api.ted.europa.eu

# Files
MAX_UPLOAD_SIZE_MB=100
OCR_LANGUAGES=est+eng
ANTIVIRUS_ENABLED=false

# Notifications
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM=

# Observability
LOG_LEVEL=INFO
OTEL_ENABLED=false
PROMETHEUS_ENABLED=false
```

Real values must never be committed.

## 15. Development commands

The repository must eventually expose consistent root commands:

```bash
make bootstrap
make dev
make stop
make logs
make lint
make typecheck
make test
make test-integration
make test-e2e
make migrate
make seed
make backup
make restore BACKUP=path/to/backup
```

Equivalent Windows-friendly PowerShell commands or documented Docker commands must be provided.

## 16. Testing strategy

### Unit tests

- domain rules;
- scoring functions;
- state transitions;
- schema validation;
- deadline calculations;
- pricing calculations;
- redaction and policy decisions;
- source normalization;
- prompt assembly without external calls.

### Contract tests

- Gemini adapter with recorded safe fixtures;
- RHR adapter against approved snapshots;
- TED API query and response fixtures;
- document parser fixtures;
- export schema and template tests.

### Integration tests

- PostgreSQL migrations;
- object storage lifecycle;
- job retries and dead-letter behavior;
- import-to-workspace flow;
- extraction-to-compliance flow;
- approval invalidation after source change;
- package generation and hash verification.

### End-to-end tests

- first admin setup;
- create company profile;
- import opportunity;
- perform `GO/NO_GO` assessment;
- create workspace;
- upload and parse documents;
- review requirements;
- draft proposal;
- approve package;
- export and record submission.

### AI evaluation

Maintain a sanitized evaluation set with expected:

- requirement recall;
- mandatory-vs-optional classification;
- citation correctness;
- unsupported-claim rate;
- language quality;
- scoring stability;
- prompt-injection resistance;
- cost and latency.

No AI feature is complete without measurable evaluation criteria.

## 17. Definition of MVP done

The MVP is complete only when:

- a clean machine can start the system through documented Docker commands;
- the application is usable in Estonian;
- users and permissions are enforced;
- at least one approved RHR ingestion method and the TED Search API adapter work;
- source notices and document versions are preserved;
- PDF and DOCX extraction work with citations;
- opportunity scoring is explainable and configurable;
- the compliance matrix covers mandatory requirements and evidence;
- Gemini calls are schema-validated, audited, cost-limited, and policy-gated;
- proposal drafts can be generated only from approved evidence and cited tender context;
- review and approval gates block incomplete packages;
- DOCX/PDF export and attachment manifests work;
- final submission remains human-controlled;
- backup and restore are tested;
- critical security tests pass;
- all required documentation and runbooks exist.

## 18. Roadmap summary

### Phase 0 — Discovery and policy

Validate RHR integration options, Gemini data policy, user roles, document classifications, legal boundaries, and the first real pilot tender.

### Phase 1 — Platform foundation

Build the monorepo, Docker environment, authentication, database, storage, job processing, and audit system.

### Phase 2 — Discovery and ingestion

Implement RHR/TED adapters, manual import, document extraction, version tracking, and opportunity matching.

### Phase 3 — Tender intelligence

Implement requirement extraction, compliance matrix, research, evidence management, and clarification workflows.

### Phase 4 — Proposal production

Implement approved content blocks, structured drafting, pricing scenarios, templates, review, approval, and export.

### Phase 5 — Pilot hardening

Run real tender pilots, measure extraction quality, harden security, test backup/restore, and improve usability.

Detailed implementation work is maintained in [`TASKS.md`](TASKS.md). Coding-agent behavior and architecture constraints are maintained in [`AGENTS.md`](AGENTS.md).

## 19. Legal and operational notice

This repository does not provide legal advice. Procurement requirements, official notices, deadlines, submission rules, and applicable laws must be checked against current official sources. The authorized user remains responsible for the final offer and submission.

## 20. License

No open-source license has been selected yet. Until a license is added, all rights are reserved by the repository owner and Eventnexus OÜ as applicable.
