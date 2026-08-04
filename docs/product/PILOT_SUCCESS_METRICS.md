# EventNexus Hanke Keskond — Pilot Success Metrics

**Document ID:** PRD-004  
**Task:** S0-T04  
**Status:** Complete  
**Last updated:** 2026-08-04

## 1. Purpose

This document defines how the MVP pilot is measured. Metrics must be reproducible, based on recorded evidence, and comparable with a manual baseline. Subjective statements such as “the AI worked well” are not sufficient.

## 2. Pilot sample

The minimum pilot dataset is five representative IT procurements:

- at least one Estonian-language tender;
- at least one English-language or bilingual tender;
- at least one multi-document tender;
- at least one tender with an amendment or changed source package;
- at least one justified NO-GO case;
- at least one current real workflow before declaring the MVP pilot-ready.

For recall and citation metrics, a human-reviewed gold standard must be created independently of the system output. Historical public tenders may be added to increase sample size.

## 3. Measurement principles

1. Store numerator, denominator, exclusions, sample IDs, evaluator, date, and calculation version.
2. Report both aggregate and per-tender results.
3. Do not hide failed or incomplete cases.
4. Separate model quality from workflow quality and system reliability.
5. Record active human time, not unattended background processing time, for productivity metrics.
6. A critical miss cannot be averaged away by many trivial correct items.
7. Any metric affected by a source amendment must identify the source version used.

## 4. Baseline protocol

Before using EventNexus for a pilot tender, record a comparable manual baseline using existing tools and process.

Required baseline fields:

```text
baseline_id
tender_id_or_reference
complexity_class
language
page_count
attachment_count
lot_count
manual_discovery_time_minutes
manual_analysis_time_minutes
manual_requirement_matrix_time_minutes
manual_drafting_time_minutes
manual_review_time_minutes
manual_export_time_minutes
rework_cycles
issues_found_after_internal_review
performed_by
measurement_method
notes
```

When a live tender cannot be processed twice, use either a comparable historical tender or a controlled split workflow and document the limitation.

## 5. Opportunity discovery metrics

### M-OPP-01 Opportunity recall

**Question:** Did the system find the relevant opportunities present in the reference set?

```text
recall = relevant_reference_opportunities_found / all_relevant_reference_opportunities
```

Target: `>= 90%`.

Reference set: all opportunities manually reviewed from the same approved sources, query scope, and time range.

A missed opportunity is critical when it would likely have qualified for human GO/NO-GO review and was not visible before the decision deadline.

### M-OPP-02 Strong-match false-positive rate

```text
false_positive_rate = strong_matches_marked_irrelevant / all_reviewed_strong_matches
```

Target: `<= 30%`.

“Strong match” must be defined by a versioned score threshold. Human irrelevance reasons are categorized to improve scoring without rewriting historical results.

### M-OPP-03 Discovery latency

```text
latency = first_system_visibility_time - authoritative_source_publication_time
```

Target:

- TED/RHR synchronized source: median `<= 6 hours`, p95 `<= 24 hours` after publication, subject to permitted polling limits;
- manual import: visible immediately after successful import.

Amendments use the same metric from source update time to visible change event.

## 6. Requirement extraction metrics

### M-REQ-01 Mandatory requirement recall

```text
mandatory_recall = correctly_captured_mandatory_requirements / gold_standard_mandatory_requirements
```

Target: `>= 95%` overall and `100%` for requirements classified as submission-blocking during human review.

A requirement counts as captured only when its normalized meaning and source citation are sufficient for a reviewer to act.

### M-REQ-02 Requirement precision

```text
precision = valid_extracted_requirements / all_reviewed_extracted_requirements
```

Provisional target: `>= 85%`.

Duplicates, invented requirements, and statements incorrectly promoted from informative text count as false positives.

### M-REQ-03 Critical field accuracy

Critical fields include deadlines, values, percentages, durations, identifiers, lot numbers, required counts, and minimum thresholds.

```text
critical_field_accuracy = correct_critical_fields / all_sampled_critical_fields
```

Target: `100%` in approved exports and `>= 99%` before human correction during pilot evaluation.

### M-REQ-04 Citation correctness

```text
citation_correctness = statements_with_correct_supporting_citation / sampled_cited_statements
```

Target: `>= 98%`.

A citation is correct only when it points to the correct immutable document version and a location that supports the material statement.

### M-REQ-05 Citation coverage

```text
citation_coverage = material_extracted_statements_with_citation / all_material_extracted_statements
```

Target: `100%` for approved requirements, tender facts, and compliance findings.

## 7. Proposal and claim metrics

### M-CLAIM-01 Unsupported company-claim rate

```text
unsupported_claim_rate = unsupported_company_claims / all_sampled_company_claims
```

Targets:

- approved export: `0` unsupported claims;
- AI draft before review: `<= 2%`, with every unsupported claim automatically blocked or visibly flagged.

Claims about customers, references, personnel, certifications, turnover, insurance, legal authority, and delivery capacity require approved evidence.

### M-CLAIM-02 Unsupported commitment rate

```text
unsupported_commitment_rate = unreviewed_or_unmapped_commitments / all_material_commitments
```

Target: `0` in approved export.

A commitment must map to a reviewed requirement, proposal decision, or explicit authorized business choice.

### M-CLAIM-03 Requirement coverage in proposal

```text
coverage = mandatory_requirements_mapped_to_response_or_explicit_exception / all_mandatory_requirements
```

Target: `100%` before final approval.

### M-LANG-01 Estonian language usability

Human reviewers score clarity, correctness, terminology, and professional suitability from 1 to 5.

Target: average `>= 4.0/5`, with no critical mistranslation in binding content.

### M-LANG-02 Source-language preservation

Target: `100%` of translated material retains the original source, original language, translation status, and reviewer state.

## 8. Productivity metrics

### M-TIME-01 Preparation-time reduction

Active preparation time includes intake, analysis, requirement work, drafting, pricing preparation, export preparation, and rework. It excludes unattended processing and official buyer waiting time.

```text
reduction = (baseline_active_minutes - product_active_minutes) / baseline_active_minutes
```

Target: median `>= 40%` reduction across comparable pilot tenders.

### M-TIME-02 Human review-time reduction

```text
reduction = (baseline_review_minutes - product_review_minutes) / baseline_review_minutes
```

Target: median `>= 25%` reduction.

Review time must still be sufficient for required approvals; a reduction caused by skipped review is invalid.

### M-TIME-03 Rework cycles

A rework cycle begins when a reviewer requests material changes and ends when a new reviewable version is submitted.

Target: no increase from baseline, and a desired `>= 20%` reduction for repeated company-content issues.

### M-TIME-04 Time to GO/NO-GO decision

```text
duration = final_decision_time - first_visibility_time
```

Report median by complexity. Initial pilot target: `<= 2 business days` for ordinary opportunities with complete public documents.

## 9. Export and approval metrics

### M-EXP-01 Export completeness

```text
pass_rate = approved_packages_passing_all_configured_checks / all_approved_packages
```

Target: `100%`.

Checks include required files, placeholders, filenames, formats, totals, manifests, hashes, selected lots, current source version, and approval versions.

### M-EXP-02 Deterministic reproducibility

Generating the same approved snapshot with the same renderer version must produce an equivalent manifest and content. Where file-format metadata prevents byte-identical output, the renderer must normalize it or document a semantic equivalence test.

Target: `100%` of tested package rebuilds pass the documented reproducibility rule.

### M-APP-01 Approval integrity

Target: `100%` of approvals reference exact versions and hashes, and every material post-approval change invalidates the relevant approval.

### M-SUB-01 Human submission control

Target: `100%` of real submissions are performed or explicitly delegated by an authorized human. Any autonomous portal submission attempt is a pilot failure.

### M-SUB-02 Submission evidence completeness

Target: `100%` of real submissions link submitter, time, channel, package hash, and official reference/receipt or a documented reason why the receipt is unavailable.

## 10. Amendment safety metrics

### M-AMD-01 Amendment detection recall

```text
recall = detected_reference_amendments / all_reference_amendments
```

Target: `100%` for pilot amendments present in monitored sources.

### M-AMD-02 Impact-review completion

Target: `100%` of detected material amendments create a visible impact review before final package approval or further submission action.

### M-AMD-03 Stale approval prevention

Target: `0` packages approved or submitted using a known stale source version without an explicit authorized exception recorded after impact review.

## 11. AI governance and cost metrics

### M-AI-01 Policy compliance

```text
compliance = sampled_permitted_and_correctly_audited_invocations / sampled_invocations
```

Target: `100%`.

Review classification, redaction decision, allowed sources, actor, purpose, model, prompt version, token/cost metadata, response status, and content hashes.

### M-AI-02 Schema success rate

```text
success = valid_structured_results_without_manual_repair / completed_structured_calls
```

Initial target: `>= 98%` after bounded retry.

### M-AI-03 Prompt-injection resistance

Target: `100%` of regression fixtures fail safely: no permission expansion, secret disclosure, arbitrary URL fetch, unauthorized tool call, or policy bypass.

### M-AI-04 Budget adherence

Target: `100%` of calls and jobs stay within configured hard limits; `0` unbounded jobs; `0` paid external calls in default automated tests.

### M-AI-05 Cost per tender

```text
cost_per_tender = sum(provider_estimated_or_billed_costs_linked_to_workspace)
```

No fixed business target is imposed before real pilot measurement. Record median, p95, and cost by workflow. S0-T12 defines initial caps.

## 12. Reliability and recovery metrics

### M-REL-01 Core workflow success

```text
success_rate = successful_core_jobs / all_non_cancelled_core_jobs
```

Target: `>= 95%` without administrator intervention.

Report separately for ingestion, parsing, OCR, extraction, retrieval, drafting, validation, and export.

### M-REL-02 User-facing availability

During agreed pilot operating windows:

```text
availability = (scheduled_minutes - unplanned_unavailable_minutes) / scheduled_minutes
```

Target: `>= 99%` for core local UI/API, excluding planned maintenance and unavailable optional external services.

### M-REL-03 Backup recovery

Targets:

- recovery time objective: restore pilot installation within `4 hours`;
- recovery point objective: no more than `24 hours` of data loss under the approved backup schedule;
- one documented clean-environment restore drill before pilot acceptance.

### M-REL-04 Data integrity

Target: `100%` of sampled originals, evidence files, generated packages, and restored artifacts match recorded SHA-256 values.

## 13. Security and privacy metrics

### M-SEC-01 Open critical/high findings

Target at pilot release: `0` open critical or high findings from authorization tests, dependency/container scanning, file-security tests, threat-model validation, and AI red-team testing.

### M-SEC-02 Restricted external transfer

Target: `0` instances of `RESTRICTED_NO_EXTERNAL_AI` content sent to Gemini or another external AI provider.

### M-SEC-03 Authorization negative-test coverage

Target: every protected resource type has at least one horizontal and one vertical access-denial test where applicable.

### M-SEC-04 Secret exposure

Target: `0` secrets in repository, logs, exports, screenshots, fixtures, prompts, or audit payloads.

## 14. User outcome metrics

### M-UX-01 Usefulness rating

After each pilot tender, the Bid Lead and Authorized Business Decision-Maker rate usefulness from 1 to 5.

Target: average `>= 4.0/5`.

### M-UX-02 Decision confidence

Users rate whether the system made evidence, gaps, risks, and next actions clearer than the baseline.

Target: at least `80%` of responses are “better” or “significantly better”.

### M-UX-03 Critical workflow completion

Target: an authorized new user can complete import, analysis review, GO/NO-GO, compliance, review, export, and simulated submission record from documentation without developer intervention.

## 15. Severity model

| Severity | Meaning |
|---|---|
| `CRITICAL` | Could cause invalid submission, material false claim, unauthorized disclosure, incorrect binding price, missed deadline, or loss of audit integrity |
| `HIGH` | Material compliance, security, or workflow failure requiring correction before pilot use |
| `MEDIUM` | Significant usability or quality issue with available workaround |
| `LOW` | Minor issue without material procurement impact |

Metrics must report critical/high misses separately from aggregate percentages.

## 16. Evaluation linkage

| Metric group | Later implementation/evaluation tasks |
|---|---|
| Opportunity discovery | S5-T06–S5-T15, S6-T01–S6-T07, S17-T08 |
| Requirement quality | S7-T04–S7-T08, S9-T08, S17-T11, S18-T04 |
| Claims and drafting | S9-T10, S10-T04–S10-T14, S18-T05 |
| Pricing/export/approval | S11, S12, S17-T12, S18-T06 |
| AI policy/cost | S9-T03–S9-T10, S17-T09, S17-T11 |
| Reliability/recovery | S16, S17-T06–S17-T09, S18-T03 |
| Security/privacy | S15, S17-T10, S18-T08 |
| Usability/language | S14, S18-T03–S18-T07 |

## 17. Pilot report requirements

`docs/pilots/PILOT_001_REPORT.md` must include:

- dataset and tender complexity description;
- baseline method and limitations;
- per-tender and aggregate metric table;
- all critical/high misses;
- human corrections and manual interventions;
- AI model/prompt versions and cost;
- security/privacy incidents or near misses;
- decision on MVP readiness;
- residual risks, owners, and backlog changes.

## 18. Acceptance traceability

- **Metrics have calculation methods:** Sections 5–13.
- **Baseline and target values are recorded or marked for pilot measurement:** Sections 4–13.
- **Metrics link to later evaluation tasks:** Section 16.
