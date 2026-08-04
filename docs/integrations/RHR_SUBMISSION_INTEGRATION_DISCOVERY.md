# RHR Supplier Submission Integration Discovery

**Task:** S0-T14  
**Status:** Complete  
**Conclusion:** `UNSUPPORTED_FOR_MVP`  
**Research date:** 2026-08-04

## 1. Research question

Does an official, supported RHR interface allow a supplier application to create a draft tender, upload bid material, sign, or submit an offer programmatically?

## 2. Official sources reviewed

- RHR public web application and public rendered notices: `https://riigihanked.riik.ee/rhr-web/`
- RHR user guides published by Riigi Tugiteenuste Keskus: `https://rtk.ee/riigihangete-korraldamine/registri-haldamine/rhr-kasutusjuhendid`
- RHR system information in RIHA: `https://www.riha.ee/Infos%C3%BCsteemid/Vaata/RHR`
- Current Riigihangete seadus: `https://www.riigiteataja.ee/akt/112072025026`
- TED Search API: `https://docs.ted.europa.eu/api/latest/search.html`
- TED Publication API: `https://docs.ted.europa.eu/api/latest/publication.html`

## 3. Findings

### 3.1 RHR public interfaces

Public RHR notice content is suitable for source discovery/import as documented in `RHR_DISCOVERY.md`. No current official public supplier API documentation was identified that supports:

- creating a supplier tender draft;
- uploading tender response files into a supplier workspace;
- completing supplier declarations;
- initiating or performing electronic signing;
- submitting or withdrawing an offer;
- retrieving an authenticated supplier submission receipt programmatically.

The absence of public documentation is not proof that no internal or partner interface exists. It means EventNexus has no supportable basis to implement supplier submission automation.

### 3.2 RHR user workflow

Official RHR guidance describes procurement participants using the register’s user interface and role/authorization flows. Supplier actions involve authenticated human use of the official environment.

This is materially different from public-notice retrieval. Authenticated supplier actions can create legal and commercial consequences and may involve identity/signing methods that EventNexus must not capture.

### 3.3 TED APIs

The TED Search API is for searching and reusing published procurement notices. It is not a supplier tender-submission API.

The TED Publication API supports publication workflows for contracting authorities/eSenders. It does not provide an interface for economic operators to submit tenders to a procurement procedure.

### 3.4 Legal and responsibility considerations

An offer is a binding business act and must conform to the procurement documents and official submission requirements. Automation that selects a procedure/lot, uploads files, accepts declarations, signs, or submits creates risks including:

- wrong procurement or lot;
- stale source version;
- wrong price or attachment;
- unauthorized declaration/commitment;
- missed or incorrectly interpreted deadline;
- identity/signing-secret handling;
- insufficient evidence of user intent;
- disputed submission status;
- unsupported use of the official portal.

These risks cannot be resolved by browser scripting or a confirmation dialog alone.

## 4. MVP conclusion

```text
status: UNSUPPORTED_FOR_MVP
supplier_submission_api_found: false
submission_automation_implemented: false
human_submission_required: true
official_written_support_required_before_reassessment: true
```

EventNexus will generate and approve a deterministic package, manifest, validation report, and checklist. An authorized person will authenticate, upload, verify, sign if required, submit, and save official evidence manually.

## 5. Explicitly prohibited implementations

The MVP must not implement:

- Playwright/Selenium/browser-extension login automation for RHR;
- credential, cookie, session, ID-card, Smart-ID, Mobile-ID, or signing-key storage;
- DOM selectors or reverse-engineered internal endpoints for submission;
- automatic declaration acceptance;
- “one-click submit” through hidden browser actions;
- automatic retry of a submission action;
- treating an upload or HTTP success as official submission;
- portal automation based only on user-provided credentials;
- direct use of TED Publication API for supplier offers.

## 6. Supported MVP handoff

The system may safely support:

- an official RHR link;
- selected procedure and lot identifiers;
- exact approved files and package hash;
- human-readable upload/submission checklist;
- filename, format, size, total, declaration, and signature checks;
- internal deadline safety margin;
- human confirmation checkpoints;
- manual recording of official receipt/reference;
- immutable submission evidence linked to the approved package.

Opening a link is not an official portal action and creates no submission state transition.

## 7. Future reassessment prerequisites

Supplier submission integration may be reconsidered only when all of the following exist:

1. official written documentation or support confirmation that the interface is intended for supplier integration;
2. documented authentication, authorization, signing, and consent semantics;
3. rate limits, test/sandbox environment, versioning, support, and error model;
4. legal review of electronic intent, authority, declarations, evidence, and liability;
5. data-protection and security review;
6. dedicated threat model covering identity, replay, wrong-lot/file, duplicate submission, withdrawal, and receipt integrity;
7. no requirement to store reusable identity secrets;
8. human-confirmed transaction design showing every binding action;
9. independent test/rehearsal without risk of accidental live submission;
10. explicit written approval from Eventnexus OÜ decision-maker.

If any prerequisite is absent, the conclusion remains `UNSUPPORTED` or `UNKNOWN`, and no implementation begins.

## 8. Support clarification template

A future support request should ask RHR support specifically:

- whether an official supplier-side API/integration exists;
- intended eligible integrators and contractual process;
- sandbox/test access;
- supported draft/upload/declaration/sign/submit/withdraw/receipt operations;
- authentication and authorization model;
- identity/signing boundaries;
- versioning, rate limits, audit/reference IDs, and duplicate protection;
- whether browser automation or internal endpoints are explicitly prohibited.

Do not send confidential tender, credentials, or personal data in the initial inquiry.

## 9. Post-MVP backlog linkage

Any future work belongs under:

- `S19-T11 — Reassess official RHR supplier integration`;
- `S19-T12 — Design human-confirmed portal assistant`;
- `S19-T13 — Threat model identity/signing integration`;
- `S19-T14 — Implement submission automation only after explicit approval`.

## 10. Acceptance traceability

- **No automation implemented:** research/documentation only.
- **Conclusion documented:** `UNSUPPORTED_FOR_MVP`.
- **Future work placed post-MVP:** Section 9 and existing Phase 19 tasks.
