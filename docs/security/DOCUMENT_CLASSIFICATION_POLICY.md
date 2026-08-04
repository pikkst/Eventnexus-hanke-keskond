# Document Classification and Processing Policy

**Task:** S0-T10  
**Status:** Complete  
**Policy owner:** Eventnexus OÜ Managing Director / designated Security and Privacy Owner  
**Last updated:** 2026-08-04

## 1. Purpose

This policy defines how source documents, extracted content, chunks, embeddings, prompts, AI responses, drafts, exports, logs, and backups are classified and processed in EventNexus.

Classification is a mandatory security and workflow control. It is not merely a user-interface label. Every protected operation must resolve an effective classification before access, retrieval, external processing, export, retention, or deletion.

## 2. Classification levels

The MVP uses five classifications:

| Classification | Meaning | Examples |
|---|---|---|
| `PUBLIC` | Lawfully public information whose intended use is compatible with the workflow | published procurement notices, public authority strategy, public company website content, approved public references |
| `INTERNAL` | Non-public operational information intended for Eventnexus personnel, with limited harm if disclosed | internal service descriptions, draft capability taxonomy, non-sensitive workflow notes |
| `CONFIDENTIAL` | Non-public business information whose disclosure could cause commercial, contractual, legal, or reputational harm | pricing rates, margin assumptions, non-public references, contracts, partner terms, financial details |
| `PERSONAL_DATA` | Information relating to an identified or identifiable natural person | CVs, contact details, availability, employment history, signatures, reviewer comments tied to a person |
| `RESTRICTED_NO_EXTERNAL_AI` | Content that must remain local and must never be sent to Gemini or another external AI | credentials, authentication/signing secrets, prohibited customer data, highly restricted agreements, tender material with explicit no-external-processing requirement |

`PERSONAL_DATA` is a handling class rather than a simple severity rank. A record may be both personal and confidential; the effective controls must apply the union of restrictions. The implementation may represent flags in addition to the primary class.

## 3. Default classification rules

### 3.1 Unknown content

Unknown, unclassified, or parser-generated content defaults to:

```text
external_ai_allowed = false
export_allowed = false unless source workflow explicitly permits it
search_visibility = owner/admin review only
retention = preserve until classified or safely rejected
```

Unknown classification must never default to `PUBLIC` or `INTERNAL`.

### 3.2 Source defaults

| Source | Default classification |
|---|---|
| Official public RHR/TED notice | `PUBLIC`, subject to personal-data minimization and source use conditions |
| Public procurement attachment | `PUBLIC` only after access/provenance check; otherwise `INTERNAL` pending review |
| User-uploaded unknown document | `RESTRICTED_NO_EXTERNAL_AI` pending classification |
| Eventnexus internal methodology | `INTERNAL` |
| Price list, margin model, financial evidence | `CONFIDENTIAL` |
| Staff CV or named availability | `PERSONAL_DATA` plus `CONFIDENTIAL` where appropriate |
| Customer contract/reference evidence | `CONFIDENTIAL` unless a specific approved public derivative exists |
| Credentials, signing keys, PINs, tokens | prohibited data; reject/quarantine and treat as `RESTRICTED_NO_EXTERNAL_AI` |
| AI response | inherits the most restrictive source/input classification |
| Generated proposal section | inherits all supporting facts/evidence and may be raised by commitments or tender restrictions |

## 4. Classification inheritance

The effective classification of a derived artifact is the union of the strongest applicable source restrictions.

Examples:

- a chunk from a confidential contract is `CONFIDENTIAL`;
- an embedding of personal CV content remains `PERSONAL_DATA` and inherits external-processing restrictions;
- a prompt containing public tender text and confidential pricing is `CONFIDENTIAL`;
- an AI response based on confidential excerpts remains `CONFIDENTIAL` even if it does not visibly repeat every source fact;
- a redacted public derivative is a new version with its own reviewer, transformation record, and content hash; redaction does not silently downgrade the original;
- a ZIP or export inherits the union of every included file and manifest field.

The system must not support an automatic downgrade based only on AI classification or absence of detected sensitive terms.

## 5. Processing matrix

| Operation | PUBLIC | INTERNAL | CONFIDENTIAL | PERSONAL_DATA | RESTRICTED_NO_EXTERNAL_AI |
|---|---|---|---|---|---|
| Local storage | allowed | allowed | allowed with restricted permissions | allowed with purpose and restricted permissions | allowed only when required, strongly restricted |
| Local parsing/OCR | allowed | allowed | allowed in bounded local worker | allowed with minimization and authorized purpose | allowed only locally in isolated/bounded worker |
| Local lexical search | allowed | allowed by role | allowed by explicit role/workspace | allowed by need-to-know | restricted allowlist only |
| Local embeddings | allowed | allowed | allowed if approved local provider/storage | allowed only when necessary and approved | allowed only with approved local-only model and index |
| Gemini generation | policy check | explicit permission | denied by default | denied by default | always prohibited |
| Gemini embeddings | policy check | explicit permission | denied by default | denied by default | always prohibited |
| External web research | allowed for public question | no internal content in queries without approval | no confidential query content | no personal query content unless separately approved | prohibited |
| Email notification body | public/minimal | metadata only by default | no sensitive content by default | no personal detail by default | prohibited |
| Export | allowed by workflow | authorized users | explicit approval and target scope | lawful/necessary target and approval | only authorized local export if policy permits; never external AI |
| Logging | metadata only | metadata/hash | redacted metadata/hash | minimized actor IDs, no full content | metadata/hash only |
| Backup | allowed | allowed | protected backup | protected backup with retention/purpose | encrypted/restricted backup or excluded by policy |

## 6. User overrides

Classification may be changed only by users with explicit permission.

### 6.1 Raising classification

Users may raise classification immediately. The system must:

- block newly prohibited access and AI use;
- invalidate cached retrieval and external-processing eligibility;
- flag affected prompts, drafts, exports, and approvals;
- record actor, reason, old/new class, and affected versions.

### 6.2 Lowering classification

Lowering requires:

- authorized classifier/reviewer;
- reason and permitted use;
- review of linked evidence and inherited restrictions;
- confirmation that no customer, partner, tender, legal, or personal-data condition prevents downgrade;
- a new approved version or approved redacted derivative;
- audit record.

AI may recommend a classification but cannot approve a downgrade.

## 7. Redaction policy

Redaction is permitted when it produces a purpose-specific derivative.

Required metadata:

```text
source_document_version_id
redacted_artifact_id
redaction_profile_version
redaction_categories
created_by_or_job
reviewed_by
created_at
content_hash
classification_before
classification_after
permitted_purpose
expiry_or_review_date
```

Redaction must be deterministic where feasible and tested for:

- authentication secrets and tokens;
- personal identification codes;
- direct contact details;
- signatures;
- private addresses;
- bank data;
- customer/partner restricted names;
- custom project terms;
- hidden metadata, headers/footers, comments, tracked changes, spreadsheet hidden sheets, and embedded files.

A redaction summary may be shown, but logs must not contain the removed value.

## 8. External AI rules

Before every external AI call:

1. resolve all source versions;
2. calculate effective classification;
3. verify actor permission and approved purpose;
4. reject unknown or prohibited classifications;
5. apply minimization and required redaction;
6. enforce Gemini feature restrictions;
7. enforce cost and size limits;
8. record policy decision and source hashes;
9. send only approved excerpts;
10. classify the response at least as restrictively as the inputs.

No administrator override may make `RESTRICTED_NO_EXTERNAL_AI` eligible for Gemini. Changing that rule requires a new policy version and explicit product/security approval, not a runtime checkbox.

## 9. Chunks and embeddings

Each chunk and embedding record must contain:

```text
source_document_version_id
source_location
chunk_hash
classification
personal_data_flags
permitted_uses
external_ai_eligible
redaction_derivative_id_if_any
embedding_provider
embedding_model
embedding_location
created_at
invalidated_at
```

- deleting or restricting a source must invalidate/restrict its chunks and embeddings;
- model/index changes create new versions;
- cross-workspace retrieval is prohibited;
- confidential/personal/restricted content must not be embedded externally by default;
- embeddings are treated as potentially sensitive derived data, not anonymized proof.

## 10. Prompts and responses

Prompts and responses inherit source restrictions.

The default audit ledger stores:

- purpose;
- prompt/schema version;
- source IDs and hashes;
- classification summary;
- policy/redaction decision;
- model and usage metadata;
- input/output hashes;
- safe error details.

Full prompt/response storage is off by default. If enabled for an approved debugging incident, it requires short retention, restricted access, explicit case ID, and a cleanup verification.

## 11. Exports

Before export:

- calculate package classification;
- verify every included record’s permitted target and use;
- remove hidden metadata and comments according to template rules;
- validate that personal/contact data is necessary;
- require approval for confidential/personal material;
- include a classification label in internal manifests where appropriate;
- prevent public export of non-public evidence;
- store package hash and recipient/purpose scope.

A generated package is not automatically safe to email or upload merely because it passed content readiness.

## 12. Logs, metrics, and analytics

Logs and metric labels must not contain:

- full tender text;
- prompt/response bodies;
- filenames when sensitive naming could disclose content;
- personal identification codes;
- direct contact details;
- credentials or authorization headers;
- price/margin values unless an approved aggregated metric requires them;
- customer/reference confidential names.

Use stable opaque IDs, safe categories, counts, durations, hashes, and error codes.

## 13. Retention and deletion

Exact periods are configured later, but every class requires:

| Class | Retention principle |
|---|---|
| PUBLIC | retain as needed for source history and audit; respect source/reuse changes |
| INTERNAL | retain while operationally useful; periodic review |
| CONFIDENTIAL | minimum necessary period; contract/legal/audit exceptions documented |
| PERSONAL_DATA | purpose limitation and data minimization; delete or anonymize when no longer necessary unless retention is required |
| RESTRICTED_NO_EXTERNAL_AI | shortest necessary period, strongest access, documented backup/deletion behavior |

Deletion must cover or deliberately retain according to policy:

- originals and versions;
- normalized text;
- OCR output;
- chunks;
- embeddings;
- temporary files;
- prompts/responses if stored;
- exports;
- provider file/cache IDs;
- backups and deletion tombstones;
- audit references.

Immutable audit records may retain safe metadata and hashes without retaining prohibited full content.

## 14. Access control

Minimum permission dimensions:

- organization and workspace membership;
- global role;
- resource ownership;
- classification clearance;
- personal-data purpose;
- tender/customer/partner permitted use;
- operation type: view, download, edit, classify, redact, approve, export, external-process, delete;
- record state and validity.

Downloads and object-storage URLs must enforce the same policy as metadata endpoints.

## 15. Classification review events

Review is required when:

- a document is first imported;
- an AI/extraction job proposes sensitive content;
- a public derivative is created;
- customer/partner permission changes;
- a tender imposes processing/location/confidentiality restrictions;
- a user requests external AI for a denied class;
- a source becomes non-public or access-controlled;
- content is selected for export;
- retention expires;
- an incident or mistaken transfer occurs.

## 16. Required UI behavior

The UI must:

- display classification and external-AI eligibility;
- explain why a call/export is blocked;
- distinguish inherited and directly assigned classification;
- show pending review and unknown states;
- require reason for downgrade/override actions;
- warn when a selection combines multiple classifications;
- never conceal denied content behind a misleading empty result;
- show that Gemini processing is external when enabled.

## 17. Tests

Required test classes:

- unknown defaults to no external AI;
- inheritance selects the strongest restrictions;
- downgrade requires authorization and audit;
- redaction does not mutate original;
- hidden DOCX/XLSX/PDF metadata is handled;
- cross-workspace retrieval is denied;
- confidential/personal/restricted external embeddings are blocked;
- restricted content cannot be sent through alternate AI workflows;
- log redaction prevents secret/personal leakage;
- deletion/invalidation propagates to chunks and indexes;
- package classification reflects all included content.

## 18. Acceptance traceability

- **Unknown classification defaults to no external AI:** Section 3.1.
- **Every class has allowed processing paths:** Section 5.
- **Policy covers chunks, embeddings, prompts, responses, exports, and logs:** Sections 9–12.
