# MVP Tender Submission Policy

**Task:** S0-T13  
**Status:** Complete  
**Policy owner:** Eventnexus OÜ Authorized Business Decision-Maker  
**Last updated:** 2026-08-04

## 1. Policy statement

The EventNexus MVP prepares, validates, versions, and exports a submission-ready tender package and checklist. It does **not** submit the tender autonomously.

An authenticated and authorized human must:

1. approve the exact final package;
2. authenticate to the official procurement channel outside EventNexus;
3. upload/complete the submission;
4. review the official portal summary;
5. perform any required signing or identity confirmation;
6. confirm submission before the official deadline;
7. record or import the official receipt/evidence into EventNexus.

Package generation, package approval, and official submission are separate lifecycle states.

## 2. Responsibilities

| Activity | Responsible role | AI/system role |
|---|---|---|
| Determine whether to bid | Authorized Business Decision-Maker | analysis and recommendation only |
| Confirm selected lots | Authorized Business Decision-Maker / Bid Lead | highlight lot scope and conflicts |
| Confirm tender documents/source version | Bid Lead | synchronize/import, compare, warn |
| Prepare technical content | Contributors and Technical Reviewer | evidence-grounded drafts and checks |
| Prepare price | Commercial Reviewer/authorized owner | deterministic calculations and scenarios |
| Approve legal/declarations | Authorized legal/compliance and business roles | extract and flag; no legal approval |
| Approve final package | Authorized Business Decision-Maker | readiness checks and immutable snapshot |
| Authenticate/sign/submit | Authorized Submitter | no credential handling or autonomous action |
| Verify receipt and deadline | Authorized Submitter | record/check metadata and package hash |
| Handle clarification/withdrawal | Authorized human roles | draft/support and audit only |

## 3. Pre-submission gates

The system must not allow `APPROVED_FOR_SUBMISSION` unless:

- authoritative source freshness passes or an authorized exception exists;
- selected procedure and lots are explicit;
- submission deadline, timezone, and official channel are confirmed;
- every mandatory requirement has an approved response/evidence or visible authorized exception;
- required forms, declarations, attachments, signatures, and formats are identified;
- no unresolved critical readiness or review finding exists;
- technical review is complete;
- commercial/pricing approval is complete and tied to exact version/hash;
- required legal, privacy, security, and management reviews are complete;
- final package was generated from approved versions only;
- package manifest, validation report, checklist, and SHA-256 exist;
- authorized submitter is assigned.

AI cannot waive or mark these gates passed.

## 4. Submission package

The deterministic package builder produces:

```text
submission-package.zip
submission-checklist.pdf_or_html
package-manifest.json
validation-report.json_or_pdf
```

The manifest includes:

```text
package_id
workspace_id
procedure_reference
selected_lots
source_notice_versions
created_at
renderer_versions
file_name
file_role
mime_type
size_bytes
sha256
source_or_generated_version
approval_ids
classification
required_or_optional
```

The package builder must not silently add the latest file from a directory. Every included artifact is selected by an approved immutable version.

## 5. Checklist content

The human-readable checklist must include:

- official destination and source URL/reference;
- deadline in source timezone and Europe/Tallinn;
- selected lots;
- package hash and generation time;
- required files and expected portal fields;
- filename/format/size constraints;
- signature and declaration requirements;
- pricing totals and currency cross-check reference;
- authorized submitter;
- source freshness and amendment status;
- unresolved warnings accepted by authorized role;
- steps to verify uploaded files and portal-generated summary;
- steps to save official receipt/reference;
- instruction not to rely on EventNexus as proof of successful submission.

## 6. Credentials and identity secrets

EventNexus must never request, store, proxy, log, export, or autofill:

- RHR or procurement portal passwords;
- ID-card PIN1/PIN2;
- Smart-ID/Mobile-ID secrets or challenge answers;
- signing keys or private certificates;
- reusable session cookies;
- authentication QR codes or recovery codes;
- operating-system credential-store exports;
- one-time passcodes.

The UI must not contain normal data fields for these values. If detected in uploads or text, the content is quarantined/blocked and handled as a security incident or cleanup task.

## 7. Official submission flow

1. Authorized Submitter opens the official channel using a trusted browser/device.
2. Submitter authenticates directly with the official system.
3. Submitter selects the correct procurement and lot(s).
4. Submitter uploads the approved package files or enters required portal fields.
5. Submitter verifies filenames, versions, totals, declarations, signatures, and portal preview.
6. Submitter confirms official submission.
7. Submitter verifies success in the official system.
8. Submitter downloads/saves receipt and records the submission in EventNexus.

Opening an official link from EventNexus is a convenience only and must not be recorded as submission.

## 8. Submission evidence model

A submission record must include:

```text
submission_id
workspace_id
package_id
package_sha256
procedure_reference
selected_lots
channel
submitted_by_user_id
submitted_by_role
submitted_at_original
submitted_at_utc
official_timezone
official_reference_or_receipt_number
receipt_document_version_id
receipt_sha256
portal_status_text
portal_confirmation_url_if_safe
source_notice_version
notes
verification_status
verified_by
verified_at
created_at
```

If the official system provides no downloadable receipt, store:

- official reference/status;
- timestamp;
- authorized user attestation;
- screenshot or other permitted evidence where appropriate;
- reason the standard receipt is unavailable.

The system must distinguish `RECORDED`, `VERIFIED`, `DISPUTED`, and `FAILED` submission evidence.

## 9. Submission failure

A failed attempt must record:

- time and actor;
- exact package hash;
- safe error category/status;
- whether any upload or signature completed;
- remaining time to deadline;
- next action and owner;
- support/contact reference where used.

Do not log passwords, identity challenges, full screenshots containing unrelated personal information, or secret browser data.

If package/source/approval changed during retry, a new final approval is required.

## 10. Withdrawal

EventNexus may prepare a withdrawal checklist and record evidence, but an authorized human performs withdrawal through the official channel.

Required:

- reason;
- authority;
- official channel;
- timestamp;
- related submission/package;
- official confirmation;
- impact and follow-up.

AI cannot approve or execute withdrawal.

## 11. Clarifications and post-submission communication

The product may:

- import a clarification request;
- link it to requirements/source versions;
- draft a response;
- run impact and consistency checks;
- prepare a reviewed response package;
- record manual sending/submission evidence.

The MVP does not autonomously send clarification questions or responses.

## 12. Amendments after package approval

A material source amendment after package generation or approval must:

- display a critical warning;
- block submission approval or mark it invalid;
- compare affected source versions;
- invalidate relevant requirements, drafts, prices, and approvals;
- require impact review;
- generate a new package and hash after re-approval.

Historical package snapshots remain immutable.

## 13. Deadline behavior

- Preserve original source text and timezone.
- Display Europe/Tallinn conversion with DST handling.
- Do not infer official deadline from email/calendar reminders alone.
- Final submission remains the submitter’s responsibility.
- System reminders and readiness status are support tools, not guarantees.
- The UI must advise submitting before the deadline with an internal safety margin.
- A local/system outage does not extend the official deadline.

## 14. Audit events

Audit at minimum:

- readiness checks and failures;
- approval requests, approvals, rejections, invalidations;
- package generation and hashes;
- checklist access/export;
- assignment/change of authorized submitter;
- submission record creation/verification/dispute;
- receipt upload/version;
- withdrawal and clarification records;
- administrative exceptions.

Normal users cannot edit historical audit events.

## 15. Prohibited MVP capabilities

- autonomous submission;
- browser automation that logs into a procurement portal;
- hidden form filling or automatic confirmation;
- credential/session capture;
- automatic electronic signing;
- recording submission without human evidence;
- treating package export as official submission;
- AI approval of declarations, price, package, withdrawal, or submission;
- bypassing portal access controls or CAPTCHA;
- retry loops against official portal actions.

## 16. Responsibility notice

The UI and checklist must communicate substantially:

> EventNexus is an AI-assisted preparation and validation tool. It does not submit the tender or replace the official procurement system. The authorized submitter is responsible for verifying the current procurement documents, deadline, selected lots, files, declarations, price, signatures, official portal status, and receipt before treating the tender as submitted.

Estonian is the default displayed version; English may be provided for bilingual workflows. Legal wording is finalized by the responsible reviewer.

## 17. Acceptance traceability

- **No credentials or identity secrets stored:** Section 6.
- **Submission evidence fields defined:** Section 8.
- **Responsibilities before and after submission explicit:** Sections 2, 3, 7, 9–13.
