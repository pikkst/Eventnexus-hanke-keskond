# EventNexus AI Threat Model

**Task:** S0-T11  
**Status:** Complete  
**Owners:** Security/Privacy Owner and Engineering Owner  
**Last updated:** 2026-08-04

## 1. Scope

This threat model covers AI-assisted opportunity discovery, document analysis, retrieval, research, translation, proposal drafting, consistency review, and supporting agent workflows using Google Gemini or a future provider adapter.

It covers:

- local Docker services;
- users and administrators;
- uploaded files and public source content;
- document parsers and OCR;
- chunks, embeddings, and retrieval;
- prompts, schemas, model responses, and agent state;
- external AI and research services;
- tools, queues, logs, exports, backups, and audit records.

AI is treated as an untrusted probabilistic component. Its output is data, not authority.

## 2. Security objectives

1. Restricted or unauthorized content never leaves the approved trust boundary.
2. Source documents cannot change system instructions, permissions, tools, or policy.
3. AI cannot create approved facts, prices, declarations, commitments, lifecycle transitions, or submissions.
4. Every material AI-assisted claim is traceable to approved evidence or clearly labeled unresolved.
5. Model/tool execution is bounded by purpose, allowlist, schema, time, steps, and cost.
6. Cross-workspace and cross-user data isolation is preserved.
7. Failures are visible, recoverable, and auditable.
8. Provider/model changes cannot silently weaken controls or quality.

## 3. Assets

| Asset | Security concern |
|---|---|
| Tender source documents and versions | confidentiality, integrity, freshness, citations |
| Eventnexus company evidence | false claims, confidential/customer/partner restrictions |
| Staff and personal data | privacy, minimization, unauthorized external transfer |
| Pricing and margin data | commercial confidentiality and binding-risk integrity |
| Credentials and identity material | account takeover and fraudulent submission |
| Prompts, schemas, and policies | control-plane integrity |
| Retrieval indexes and embeddings | information leakage and poisoning |
| AI invocation ledger | audit integrity without sensitive duplication |
| Approvals, package hashes, submission evidence | legal/commercial accountability |
| Provider budget and quotas | denial-of-wallet and operational availability |

## 4. Trust boundaries

```text
User browser
  -> local web/API authorization boundary
  -> application/domain policy boundary
  -> queue/worker boundary
  -> local file/parser/OCR sandbox
  -> local database/object storage/vector index
  -> outbound policy gateway
  -> Gemini / approved public-source adapters
```

Additional boundaries exist between:

- workspaces and organizations;
- normal users and administrators;
- draft and approved content;
- public/internal/confidential/personal/restricted classifications;
- deterministic business rules and model recommendations;
- live provider calls and offline test fixtures.

## 5. Threat actors

- malicious external source author;
- compromised procurement attachment or website;
- unauthorized or careless internal user;
- over-privileged administrator;
- attacker with stolen account/session;
- compromised dependency, parser, model SDK, or container image;
- external AI/provider error or policy change;
- accidental model hallucination or tool misuse;
- coding agent implementing an unsafe shortcut;
- denial-of-service or denial-of-wallet attacker.

## 6. Threat register

### AI-01 — Prompt injection in tender documents

**Scenario:** A PDF, DOCX, HTML page, spreadsheet cell, filename, comment, or embedded object contains instructions such as “ignore previous rules,” “upload all files,” or “reveal the system prompt.”

**Impact:** policy bypass, data exfiltration, arbitrary tool use, false analysis.

**Controls:**

- source content is delimited and labeled untrusted data;
- system/developer instructions are separate from source excerpts;
- prompts explicitly prohibit obeying source instructions;
- model has no implicit tools;
- tool calls require application-issued capability and schema validation;
- tools use host/resource allowlists and server-side authorization;
- deterministic policy gate precedes every call;
- injection regression fixtures for all supported formats;
- high-risk model outputs never directly change state.

**Tests:** S9-T09 and parser/file-security tests.

**Residual risk:** Model may still produce misleading text. Human review and deterministic downstream gates remain required.

### AI-02 — Indirect prompt injection from public research

**Scenario:** An approved research page embeds malicious instructions or poisoned content.

**Controls:** bounded research plan; approved domain/source adapters; fetched content remains untrusted; no model-directed URL expansion; citations and publisher/date metadata; findings cannot become approved company evidence automatically.

**Residual risk:** Public sources can be wrong or coordinated. Reviewer assesses authority and corroboration.

### AI-03 — Sensitive data exfiltration

**Scenario:** Confidential, personal, restricted, or unrelated workspace content is included in a Gemini call, tool argument, error report, provider file/cache, or external query.

**Controls:** classification inheritance; unknown default deny; retrieval permission filters before content leaves storage; minimization/redaction; outbound policy gateway; provider feature allowlist; `RESTRICTED_NO_EXTERNAL_AI` hard block; safe logs; external-transfer report; incident kill switch.

**Tests:** policy matrix tests, canary secrets, cross-workspace negative tests, alternate-workflow bypass tests.

**Residual risk:** imperfect redaction. Sensitive classes remain denied by default rather than relying only on redaction.

### AI-04 — Cross-workspace retrieval leakage

**Scenario:** Vector/lexical retrieval returns another tender’s or organization’s chunks.

**Controls:** authorization and workspace filters before ranking; separate metadata namespaces; deny-by-default repository methods; opaque IDs; per-resource negative tests; no client-side filtering as security control.

**Tests:** S4-T08, S7, S15, and S17 authorization suites.

### AI-05 — Malicious or exploitative attachment

**Scenario:** Archive bomb, path traversal, XXE, parser exploit, macro, embedded executable, malformed PDF/image, or excessive resource consumption.

**Controls:** MIME sniffing; filename sanitation; archive limits; XXE disabled; no macro execution; optional antivirus; parser sandbox/process/container; CPU/memory/time/file/page limits; immutable quarantine; safe failure and cleanup.

**Tests:** S3 and S15 malicious fixtures.

### AI-06 — Hallucinated company fact

**Scenario:** Model invents a customer, reference, certification, employee skill, financial figure, insurance, authority, or past result.

**Controls:** company claims require approved fact/evidence IDs; evidence pack builder retrieves approved records only; schema distinguishes fact/assumption/proposal commitment; unsupported-claim detector; final export hard gate; humans cannot approve without visible support or explicit exception.

**Tests:** S9-T10, S10, S17, S18.

**Residual risk:** subtle paraphrase may overstate evidence. Reviewer sees source and exact claim.

### AI-07 — Missing or distorted tender requirement

**Scenario:** Model omits a mandatory condition, merges unrelated requirements, mistranslates a threshold, or converts informative text into a requirement.

**Controls:** source citations; parser/regex cross-checks for dates and numbers; coverage by document/section/category; human gold-standard evaluation; unknown/conflict states; no automatic approval; mandatory recall release gate.

### AI-08 — Incorrect numeric/date output

**Scenario:** Deadline, value, VAT, percentage, duration, score, or identifier is changed by model generation.

**Controls:** preserve original text/timezone; deterministic parser candidates; Decimal arithmetic; locale tests; model cannot be calculator of record; exact-source comparison before approval/export.

### AI-09 — Stale evidence or source version

**Scenario:** Draft or approval uses an expired certificate, outdated CV/capacity, superseded notice, old deadline, or changed template.

**Controls:** immutable versions; validity metadata; amendment detection; dependency graph; automatic invalidation; final source-freshness gate; approvals tied to hashes.

### AI-10 — Tool abuse and excessive agency

**Scenario:** Agent loops, writes arbitrary files, sends email, changes database state, or calls external systems outside the approved task.

**Controls:** specialized workflows rather than unrestricted agents; explicit tool allowlist; least-privilege capabilities; validated arguments; max steps and time; approval required for side effects; no shell/browser/email/portal tools for product AI; idempotency keys and audit.

**Tests:** tool-permission regression suite.

### AI-11 — Autonomous submission or binding action

**Scenario:** AI attempts to submit, withdraw, sign, approve price, accept declaration, or record GO/NO-GO.

**Controls:** no supplier submission tool; no stored identity secrets; protected transitions require authenticated human action; package generation and submission are separate states; exact package approval; submission evidence is human-entered and auditable.

### AI-12 — Denial of wallet

**Scenario:** Large documents, repeated retries, recursive agents, malicious users, or bugs produce excessive Gemini cost.

**Controls:** token estimation; per-call/job/workspace/day/month limits; concurrency and retry caps; caching by content/prompt hash; circuit breaker; provider budgets; admin kill switch; default test mocks.

**Tests:** S9-T07, S17-T09, failure/retry simulations.

### AI-13 — Denial of service and queue starvation

**Scenario:** OCR, embeddings, parsing, or model calls consume worker capacity and block deadlines.

**Controls:** separate queues/priorities; per-job resources; quotas; cancellation; dead-letter queue; deadline-aware scheduling; backpressure; health metrics; bounded documents.

### AI-14 — Sensitive logging and observability leakage

**Scenario:** Prompts, source excerpts, filenames, contacts, authorization headers, model responses, or secrets appear in logs/traces/metrics.

**Controls:** structured safe metadata; redaction library; prompt logging off; hashes and opaque IDs; no high-cardinality sensitive labels; log-retention/access policy; redaction tests.

### AI-15 — Provider retention or data-sharing misconfiguration

**Scenario:** Wrong project, free tier, API logging/data sharing, stored interactions, file/cache retention, grounding, or changed terms expose data.

**Controls:** paid Eventnexus project only; production enablement checklist; provider configuration verification; feature allowlist; `store=false`; file/cache/grounding disabled by default; quarterly review; transfer ledger; global kill switch.

### AI-16 — Model/version drift

**Scenario:** Provider silently updates behavior or a model is deprecated, changing schema compliance, safety, language, or cost.

**Controls:** configured model allowlist; actual model recorded; stable GA models; evaluation before promotion; prompt/model version comparison; fallback policy; deprecation monitoring.

### AI-17 — Schema confusion or unsafe coercion

**Scenario:** Model returns invalid JSON, wrong units, strings instead of numbers, extra tool arguments, or partially valid output that code silently coerces.

**Controls:** generated JSON Schema/Pydantic validation; reject unknown critical fields; bounded retry; visible failure state; no silent critical coercion; unit/currency/timezone types.

### AI-18 — Retrieval/index poisoning

**Scenario:** Malicious, obsolete, duplicated, or low-quality content dominates retrieval and influences proposals.

**Controls:** source/version provenance; approval/status filters; duplicate detection; trust/evidence quality; recency and validity; chunk hashes; reviewer can inspect retrieved set; no untrusted research promoted automatically.

### AI-19 — Evidence laundering through translation or summary

**Scenario:** An unverified claim is translated/summarized into wording that appears approved or loses caveats.

**Controls:** source-category labels survive transformations; translated content links to exact source; verification state inherited; protected terminology; no status promotion by generation.

### AI-20 — Authority confusion and automation bias

**Scenario:** Users assume AI analysis is legal advice, official compliance confirmation, or an approved business decision.

**Controls:** visible AI/draft labels; responsibility notices; reviewer roles; confidence is not evidence; legal/commercial decisions require explicit approval; training/user guide; UI avoids authoritative language.

### AI-21 — Compromised SDK/dependency/container

**Scenario:** Malicious package or image exfiltrates data or weakens TLS/security.

**Controls:** pinned dependencies/images; lockfiles; vulnerability and provenance scanning; minimal images/non-root; dependency update review; restricted outbound network; SBOM/release checks where available.

### AI-22 — SSRF and arbitrary URL retrieval

**Scenario:** User/model-provided URL targets localhost, cloud metadata, internal network, redirect chain, oversized object, or malicious protocol.

**Controls:** allowed schemes/hosts; DNS and resolved-IP validation; redirect revalidation; private/reserved IP block; size/time limits; no model-directed fetch; separate source adapters.

### AI-23 — Audit tampering or missing traceability

**Scenario:** AI use, policy block, evidence selection, or approval is unrecorded or editable.

**Controls:** append-oriented audit service; restricted access; correlation IDs; source/output hashes; failure events; backups; reconciliation between provider usage and invocation ledger.

### AI-24 — Provider outage or rate limiting

**Scenario:** Gemini is unavailable near a deadline.

**Controls:** local-only/manual workflows remain usable; asynchronous jobs; retry/backoff/circuit breaker; visible blocked status; no data corruption; optional evaluated fallback later; export does not require fresh AI if reviewed content is already complete.

### AI-25 — Confidential data in generated export

**Scenario:** Internal evidence, comments, tracked changes, hidden sheets, or personal metadata leaks into final package.

**Controls:** deterministic export mapping; hidden-metadata cleanup; manifest/classification checks; visual/content tests; target-scope approval; exact package review.

## 7. Mandatory architectural controls

The following are non-negotiable:

- server-side authorization and classification gate;
- tool allowlisting and argument schema validation;
- no unrestricted autonomous agent runtime;
- immutable source/evidence versions and citations;
- human approval for binding actions;
- exact version/hash approvals;
- external AI deny-by-default;
- bounded retries, steps, time, size, concurrency, and cost;
- safe logs and append-oriented audit;
- local/manual fallback paths;
- regression fixtures for injection and unsupported claims.

Prompt instructions alone are never considered a sufficient security control.

## 8. Test traceability matrix

| Control area | Required tests/tasks |
|---|---|
| Prompt injection and tool abuse | S9-T09, S15-T12 |
| Unsupported claims | S9-T10, S10, S18-T05 |
| Authorization/isolation | S2-T12, S4-T08, S15-T11 |
| Files/parsers | S3-T03–S3-T11, S15-T04 |
| External AI policy/redaction | S9-T03–S9-T05, S15-T09 |
| Cost/agent bounds | S9-T07, S17-T09 |
| Source/evidence freshness | S5-T15, S7, S12-T03, S13-T06 |
| Package leakage/integrity | S12-T07–S12-T11, S17-T12 |
| Provider/model drift | S9-T08, S17-T11 |
| Recovery/outage | S16, S17-T06 |

## 9. Residual risks

Even after controls:

- models can generate plausible but misleading language;
- redaction can miss context-dependent sensitive data;
- public sources can contain misinformation;
- provider behavior/terms can change;
- human reviewers can make mistakes or over-trust AI;
- complex documents can defeat parsing or citation reconstruction;
- zero defects and complete tender discovery cannot be guaranteed.

Residual risk is accepted only through explicit human review and release/pilot criteria. Critical/high findings remain release blockers.

## 10. Review triggers

Review this threat model when:

- a new AI provider/model/feature/tool is added;
- external file upload, caching, grounding, tuning, or server-side state is enabled;
- submission/signing/authentication integration is proposed;
- new document formats/parsers are added;
- public SaaS or multi-organization deployment is proposed;
- a security/privacy incident occurs;
- provider terms or retention behavior changes;
- pilot findings reveal a new attack or failure mode.

## 11. Acceptance traceability

- Threats map to mitigations and tests throughout Sections 6–8.
- Residual risks are explicit in Section 9.
- Tool allowlisting and schema validation are mandatory in Sections 6, 7, and 11.
