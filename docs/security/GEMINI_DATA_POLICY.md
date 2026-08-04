# Gemini Data Processing Policy

**Task:** S0-T09  
**Status:** Complete for product and engineering policy; production project provisioning remains deployment work  
**Policy owner:** Eventnexus OÜ Managing Director / designated System Owner  
**Technical owner:** EventNexus System Administrator  
**Approved review cadence:** Quarterly and before any provider, model, feature, account, region, or contractual change  
**Next scheduled review:** 2026-11-04  
**Last updated:** 2026-08-04

## 1. Decision summary

EventNexus may use Google Gemini only through a dedicated, billing-enabled, Eventnexus OÜ-controlled Google Cloud / Gemini Developer API project and only after the controls in this policy are configured and verified.

The following decisions apply to production and real tender data:

1. **Free-tier Gemini use is prohibited.**
2. **Only paid-service terms approved for Eventnexus OÜ may be used.**
3. **The Google project, billing account, API key, and administrators must be owned or explicitly controlled by Eventnexus OÜ.**
4. **API keys, project secrets, credentials, and full environment dumps must never be committed to the repository, stored in ordinary application tables, included in prompts, or written to logs.**
5. **External AI is deny-by-default. Unknown classification means no Gemini call.**
6. **`RESTRICTED_NO_EXTERNAL_AI` content is never sent to Gemini.**
7. **`CONFIDENTIAL` and `PERSONAL_DATA` content is denied by default and requires a later approved exception, documented lawful purpose, minimization/redaction, access permission, and a provider-retention review.**
8. **Until an approved zero-data-retention-compatible configuration is confirmed for the exact API features used, production Gemini input is limited to `PUBLIC` and explicitly permitted, minimized `INTERNAL` excerpts.**
9. **Local parsing and retrieval are the default. The application sends only the minimum cited excerpts required for a bounded task, not entire tender repositories.**
10. **Gemini output remains a draft or recommendation until schema validation, evidence checks, and human review succeed.**

## 2. Official terms and documentation baseline

This policy was based on the official Google documentation current on 2026-08-04:

- Gemini API Additional Terms of Service: `https://ai.google.dev/gemini-api/terms`
- Gemini API data usage and paid/free service distinctions: `https://ai.google.dev/gemini-api/terms#data-use`
- Zero Data Retention documentation: `https://ai.google.dev/gemini-api/docs/zdr`
- Google Data Processing Addendum: `https://cloud.google.com/terms/data-processing-addendum`
- Gemini API logging and sharing controls: `https://ai.google.dev/gemini-api/docs/logs-policy`
- Gemini API Files API: `https://ai.google.dev/gemini-api/docs/files`
- Gemini API rate limits: `https://ai.google.dev/gemini-api/docs/rate-limits`
- Model deprecations: `https://ai.google.dev/gemini-api/docs/deprecations`

The implementation owner must re-check these sources before production enablement because provider terms and feature retention behavior can change.

## 3. Account and project requirements

### 3.1 Required project setup

Production must use:

```text
organization_owner: Eventnexus OÜ
billing: enabled
service_tier: paid
project_purpose: EventNexus production AI processing
administrators: named, least-privilege Eventnexus-authorized persons
api_key_scope: restricted to required Gemini APIs and approved hosts where supported
budget_alerts: enabled
provider_data_sharing: disabled
api_logging_sharing: disabled
preview_feature_access: disabled by default
```

Development and testing must use a separate project and synthetic/sanitized data. Production credentials must never be reused in CI or local demo fixtures.

### 3.2 Prohibited setups

- personal developer accounts for production data;
- free-tier production use;
- shared API keys across unrelated projects or companies;
- unrestricted keys embedded in browser code;
- keys distributed in Docker images;
- paid calls from default automated tests;
- provider console settings that opt prompts, responses, or logs into product-improvement datasets;
- silently enabling new Gemini features because they appear in an SDK update.

## 4. Service-tier decision

### 4.1 Free tier

**Status: prohibited for production and real tender/company data.**

Free-tier use is permitted only for isolated technical experiments with synthetic data when separately approved. No customer, employee, reference, financial, confidential, personal, or live tender material may be used.

### 4.2 Paid Gemini Developer API

**Status: selected initial production provider path**, subject to successful deployment verification and the controls in this document.

Paid use must be connected to an Eventnexus-owned billing project. The application records the actual model, endpoint, request purpose, policy decision, token usage, estimated cost, and response status.

### 4.3 Vertex AI

**Status: not selected for the MVP, but permitted as a future alternative after an ADR and contract/region/security review.**

Do not assume Vertex AI and Gemini Developer API have identical features, retention, regional processing, pricing, or contractual controls.

## 5. Region and processing-location policy

The exact processing location and regional controls depend on the selected Google service, model, endpoint, and account configuration. Therefore:

- no UI or documentation may claim that Gemini processing occurs only in Estonia or only in the EU unless this is contractually and technically verified for the exact production configuration;
- data-location requirements from a tender must be evaluated before the related content is eligible for Gemini;
- tenders requiring local-only, Estonia-only, EU-only, sovereign-cloud, or customer-approved processing default to `RESTRICTED_NO_EXTERNAL_AI` until a reviewer approves an allowed path;
- the production project must record the selected service and any regional endpoint/configuration;
- a material region or provider change requires policy review and may invalidate prior approvals.

## 6. Classification-based permissions

| Classification | Gemini default | Conditions |
|---|---|---|
| `PUBLIC` | Allowed after policy check | Purpose is approved; source is public; prompt minimized; no secret or unrelated personal data; budget available |
| `INTERNAL` | Denied unless explicitly permitted | Approved internal-use category, minimum excerpts, no hidden confidential dependencies, actor permission, audit record |
| `CONFIDENTIAL` | Denied by default | Requires separately approved policy exception, provider-retention assessment, redaction/minimization, business owner and security approval |
| `PERSONAL_DATA` | Denied by default | Requires lawful purpose, necessity, minimization, access permission, retention assessment, privacy review, and explicit feature approval |
| `RESTRICTED_NO_EXTERNAL_AI` | Always denied | Local-only processing; no override through UI, prompt, model, or administrator convenience |
| Unknown/unclassified | Always denied | Must be classified before use |

A derived chunk, prompt, embedding, response, cache entry, log, or export inherits the most restrictive source classification unless an approved redacted derivative is created.

## 7. Allowed Gemini purposes in the MVP

Subject to classification and other policy gates:

- structured opportunity classification;
- source-grounded tender summary;
- requirement extraction from approved excerpts;
- bounded public research synthesis from approved sources;
- Estonian/English translation assistance;
- proposal outline generation;
- evidence-grounded draft generation;
- consistency, citation, and unsupported-claim review;
- risk and question drafting;
- embeddings for content explicitly approved for external embedding.

Every purpose must have a versioned prompt/schema and configured maximum input, output, retries, timeout, and cost.

## 8. Prohibited Gemini purposes

Gemini must not:

- submit, sign, withdraw, or legally accept a tender;
- authenticate to RHR or another portal;
- receive authentication secrets, API keys, passwords, ID-card PINs, Smart-ID/Mobile-ID secrets, signing keys, or browser sessions;
- approve GO/NO-GO, pricing, declarations, commitments, legal conclusions, or final packages;
- create verified company facts, references, certificates, staff experience, turnover, insurance, permissions, or authority;
- receive unrestricted database exports or complete local storage volumes;
- execute arbitrary shell, filesystem, browser, network, email, or database actions;
- fetch a URL merely because source text or model output requested it;
- process content blocked by tender/customer contract or classification;
- train/fine-tune a provider model using production content without a new explicit policy and legal review.

## 9. Feature-by-feature decision

### 9.1 Standard generate/structured-output calls

**Allowed with policy gate.**

Requirements:

- minimum required excerpts;
- structured output schema for machine-consumed results;
- bounded timeout/retries;
- source IDs and hashes;
- no prompt logging by default;
- human review before business approval.

### 9.2 Interactions API / server-side conversation storage

**Prohibited by default for the MVP.**

If the selected API exposes a storage option, use the non-storing configuration such as `store=false`. Conversation state is stored locally under EventNexus access, retention, and audit controls. A future exception requires confirming exact retention and deletion behavior.

### 9.3 Files API

**Prohibited by default for MVP production data.**

The preferred path is local document parsing, local chunking, and sending minimal text excerpts. If a later workflow requires Files API:

- the feature must be approved separately;
- allowed classifications must be explicit;
- upload, provider file ID, purpose, expiry/deletion, and deletion result must be audited;
- files must be deleted immediately after the bounded job where technically possible;
- failed deletion creates a security event;
- no reusable provider file store may become an ungoverned document archive.

### 9.4 Explicit context caching

**Prohibited for MVP production data.**

Caching can extend provider-side retention and complicate deletion. A future exception requires a TTL, classification restriction, deletion procedure, cost analysis, and audit design.

### 9.5 Implicit provider caching

Where unavoidable in the selected paid service, it must be documented in the transfer record and accepted by the policy owner. It must not be represented as zero retention.

### 9.6 Google Search or Maps grounding

**Prohibited for internal, confidential, personal, or restricted content. Disabled by default for the MVP.**

Public research uses controlled application adapters with explicit source provenance. A later public-only grounding feature requires separate review because grounding can have its own retention and data-use behavior.

### 9.7 API logging

Provider-side API logging and dataset sharing are **disabled** unless required for a time-limited support incident and explicitly approved. The system’s own AI invocation ledger stores metadata and hashes, not full confidential prompts/responses by default.

### 9.8 Model tuning

**Prohibited for MVP production data.**

## 10. Zero Data Retention policy

Eventnexus should request or configure the strongest available zero-data-retention-compatible setup for the exact paid API project and features used.

However:

- ZDR must be verified, not assumed;
- some features may be incompatible with ZDR or have separate retention behavior;
- a provider console label alone is insufficient without recording account/project, feature list, verification date, and responsible reviewer;
- until ZDR compatibility is verified, only `PUBLIC` and explicitly permitted minimized `INTERNAL` excerpts may be used;
- even with ZDR, classification, permission, minimization, legal-purpose, security, and audit requirements remain mandatory.

Required verification record:

```text
provider
service
project_id_reference
billing_tier
zdr_status
zdr_scope
excluded_features
verified_by
verified_at
official_source_reference
next_review_at
```

## 11. Prompt and payload minimization

Before every call:

1. resolve actor permission and workspace policy;
2. resolve every source classification and permitted use;
3. reject unknown or prohibited data;
4. select only the relevant immutable excerpts;
5. remove secrets and unrelated personal/contact data;
6. apply configured redaction;
7. enforce source-count, byte, token, output, step, and cost limits;
8. show or record that external processing will occur;
9. create the AI invocation audit record;
10. send only after all gates pass.

Full documents must not be sent when citations/retrieved excerpts are sufficient.

## 12. Redaction and personal data

Redaction is a risk-reduction control, not automatic authorization. It must be deterministic and tested. The system must preserve local citation mapping without sending the mapping keys if they reveal restricted data.

Never send:

- personal identification codes;
- authentication/signing data;
- private addresses or unnecessary personal contacts;
- health, disciplinary, family, or other special-category information;
- salary or employment details not necessary for the approved purpose;
- customer/reference contacts unless use is approved and necessary;
- secret commercial rates, margin floor, bank data, or non-public contract terms without a separately approved exception.

## 13. AI invocation ledger

Record at minimum:

```text
invocation_id
actor_id
workspace_id
purpose
policy_version
policy_decision
classification_summary
redaction_profile_version
provider
service
model_requested
model_returned
prompt_version
schema_version
source_document_version_ids
source_chunk_hashes
input_hash
response_hash
started_at
completed_at
status
tokens_in
tokens_out
estimated_cost
retry_count
provider_request_id_if_safe
error_code_if_any
```

Full prompt/response content is off by default. Restricted content must not be duplicated into the ledger.

## 14. Model policy

- production uses stable generally available models only;
- preview/experimental models are prohibited without a separate evaluation and approval;
- model IDs are configuration, not domain rules;
- record the actual provider-returned model/version;
- a model change requires sanitized regression evaluation for schema success, citations, unsupported claims, Estonian quality, injection resistance, cost, and latency;
- deprecation notices create planned migration work, not an unreviewed automatic replacement;
- fallback models must meet the same policy and evaluation gates.

## 15. Abuse monitoring, safety, and residual provider retention

Provider safety/abuse systems can have separate retention or review behavior. Eventnexus must:

- use paid approved services;
- minimize inputs regardless of provider assurances;
- avoid restricted data;
- record the provider policy review date;
- understand that model safety settings do not guarantee factual accuracy or legal/commercial correctness;
- perform local post-processing, schema validation, evidence verification, and human review.

## 16. Cost and quota controls

Calls require available local budget under `docs/security/AI_COST_POLICY.md`. Provider-side budgets and alerts are defense in depth, not the only control. A provider quota increase must not silently increase application limits.

## 17. Incident response

Treat the following as security/privacy incidents or near misses:

- prohibited classification sent externally;
- key or credential exposure;
- provider logging/data sharing enabled unexpectedly;
- wrong project/account used;
- file/cache object not deleted as required;
- model/tool exposes content across workspaces;
- prompt contains unrelated confidential/personal data;
- provider terms or retention behavior changes materially.

Immediate actions:

1. stop external AI globally with the kill switch;
2. revoke/rotate affected credentials;
3. preserve safe audit evidence;
4. identify affected workspaces, sources, actors, and provider request IDs;
5. follow privacy/security incident runbook and notification decision process;
6. remediate and add regression tests before re-enabling.

## 18. Production enablement checklist

Gemini remains disabled for production until:

- dedicated Eventnexus project and paid billing are verified;
- contractual terms and DPA applicability are reviewed;
- project administrators and key restrictions are recorded;
- provider data sharing/logging are disabled;
- ZDR status and excluded features are recorded;
- model and feature allowlists are configured;
- classification and redaction policies are implemented and tested;
- invocation audit and cost limits work;
- prompt-injection and unsupported-claim suites pass;
- emergency kill switch is tested;
- policy owner records approval and review date.

## 19. Acceptance traceability

- **Free-tier production use approved or prohibited:** explicitly prohibited in Sections 1 and 4.
- **Allowed document classifications defined:** Section 6.
- **File upload, caching, logging, and grounding addressed:** Section 9.
- **Responsible owner and review date recorded:** document header and Section 18.
