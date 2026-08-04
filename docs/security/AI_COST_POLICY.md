# AI Cost, Quota, and Emergency-Stop Policy

**Task:** S0-T12  
**Status:** Complete  
**Policy owner:** Eventnexus OÜ Managing Director / designated Financial Owner  
**Technical owner:** EventNexus System Administrator  
**Last updated:** 2026-08-04

## 1. Purpose

This policy prevents unbounded Gemini spending, denial-of-wallet, uncontrolled retries, and hidden AI operating cost. Application-level limits are mandatory even when provider quotas and billing alerts exist.

No production configuration may represent unlimited spending.

## 2. Initial MVP limits

The following conservative limits apply to the pilot unless an authorized owner changes them through audited configuration.

| Scope | Warning threshold | Hard limit | Behavior at hard limit |
|---|---:|---:|---|
| Single provider request | €0.25 estimated | €0.50 estimated | Reject before send |
| One AI workflow/job | €1.00 estimated/actual | €2.00 | Stop safely before next step |
| One workspace per rolling day | €4.00 | €5.00 | Block new calls for workspace |
| Entire installation per calendar day, Europe/Tallinn | €8.00 | €10.00 | Global AI block until reset/day change |
| Entire installation per calendar month | €80.00 | €100.00 | Global AI block until authorized budget change/new month |
| One user per rolling hour | 80% of configured request/token quota | configured quota | Throttle/block and show reason |

A call or job estimated above €1.00 is an **unusually large job** and requires explicit approval from an authorized role before execution, even if other budgets are available.

All values are configuration with safe defaults. The product owner may later revise them using measured pilot cost, but may not set an empty, negative, infinite, or effectively unbounded value.

## 3. Currency and price source

- Store internal budget values in EUR using decimal arithmetic.
- Provider prices may be denominated in another currency; use a configured exchange-rate source and store the rate, source, and timestamp used for estimation.
- Record the provider price-table version or effective date.
- Estimates are advisory before execution; provider billing reconciliation is authoritative for actual cost.
- A pricing-table change triggers administrator review and may reduce available budget until confirmed.

## 4. Estimation

Before a call, estimate:

```text
input_tokens
expected_output_tokens
cached_or_special_feature_tokens_if_applicable
provider_input_price
provider_output_price
other_feature_price
currency_rate
estimated_total_eur
```

For workflows, reserve expected cost before the first step and update the reservation after each response.

If reliable token estimation is unavailable:

- use a conservative byte/token approximation;
- apply a configurable safety multiplier, initial `1.5`;
- reject requests that cannot be bounded;
- never assume zero cost for unknown pricing.

## 5. Enforcement order

Before every AI call:

1. verify AI feature and policy eligibility;
2. verify provider/model price configuration;
3. estimate input/output and total cost;
4. check single-call limit;
5. check workflow reservation and spent amount;
6. check workspace daily budget;
7. check installation daily and monthly budgets;
8. check user and provider quotas;
9. atomically reserve budget;
10. send request;
11. record actual usage and reconcile reservation.

If any check fails, no provider request is made.

## 6. Budget ledger

Record:

```text
budget_event_id
invocation_or_job_id
workspace_id
actor_id
provider
model
purpose
price_version
currency
exchange_rate
estimated_input_tokens
estimated_output_tokens
actual_input_tokens
actual_output_tokens
estimated_cost_eur
actual_or_reconciled_cost_eur
reservation_amount_eur
reservation_status
budget_scope_snapshots
created_at
reconciled_at
```

The ledger must not contain full prompts, responses, secrets, or tender text.

## 7. Atomicity and concurrency

Budget checks and reservations must be concurrency-safe. Two workers must not both spend the same remaining budget.

Required behavior:

- atomic transaction or distributed lock around reservation;
- idempotency key per call/step;
- retry uses the original reservation where appropriate;
- abandoned reservations expire through a reconciled cleanup process;
- reconciliation cannot silently make a negative remaining budget disappear;
- race-condition tests cover parallel jobs.

## 8. Retry and loop limits

Default maximums:

| Control | Initial limit |
|---|---:|
| Provider request attempts per step | 3 total |
| Schema-repair retries | 1 additional bounded attempt |
| Agent/workflow AI steps | 8 |
| Tool calls per workflow | 12 |
| Consecutive identical failure retries | 0 after classified permanent error |
| Workflow wall-clock duration | 30 minutes unless a lower purpose limit applies |
| Concurrent AI calls per installation | 2 |
| Concurrent AI calls per workspace | 1 |

Retries count toward budgets. A retry is not free because the first response failed.

## 9. Safe-stop behavior

When a workflow reaches a hard budget or quota limit:

1. finish processing the already received response locally if safe;
2. do not start another paid step;
3. persist completed step results and source/version metadata;
4. release unused reservations;
5. mark the workflow `BUDGET_EXHAUSTED` or `QUOTA_EXHAUSTED`;
6. show the user completed work, missing steps, and safe next action;
7. avoid partial approval or misleading “complete” status;
8. create a safe audit and metric event.

The worker must not corrupt or delete previous reviewed content.

## 10. Warnings and approvals

Warnings appear at 80% of each scope’s hard limit.

An unusually large job approval stores:

```text
approver
role
workspace
purpose
estimated_cost
maximum_approved_cost
source_count
model
expires_at
approved_at
reason
```

Approval is for one exact job configuration and does not increase general budgets. If input size/model/purpose changes materially, new approval is required.

## 11. Administrative changes

Budget changes require:

- authorized financial/admin role;
- old/new values;
- reason;
- effective time;
- optional expiry/reversion time;
- impact preview;
- audit event.

The UI must not offer an “unlimited” option. Emergency increases should be time-limited where possible.

## 12. Emergency kill switch

The system must support a local global kill switch that blocks new external AI requests immediately without disabling local document access, manual analysis, deterministic checks, or exports from already reviewed content.

Automatic kill-switch triggers include:

- installation hard daily/monthly limit reached;
- provider usage cannot be reconciled for a configured period;
- detected credential leakage;
- unexpected provider/project/model;
- repeated policy-gate bypass attempt;
- anomalous cost velocity;
- provider pricing unknown or changed without review;
- incident response activation.

Re-enable requires an authorized user, resolved cause, audit record, and—where security/privacy related—incident-owner approval.

## 13. Anomaly detection

Generate alerts for:

- cost rate above configured hourly baseline;
- unusual token size or repeated near-limit calls;
- many schema failures/retries;
- one user/workspace consuming disproportionate budget;
- provider-reported usage not matching ledger within tolerance;
- calls outside expected operating hours when configured;
- a model or feature not in allowlist;
- repeated blocked requests.

Alerts must not include prompt content.

## 14. Caching and reuse

Safe cost reduction:

- cache deterministic analysis by input content hash, prompt version, schema version, model version, and policy context;
- reuse local parsed text and retrieval results;
- avoid sending entire documents when excerpts suffice;
- batch only when classification, permissions, traceability, and size limits remain clear;
- invalidate cache on source/evidence/policy/prompt/model changes.

Provider-side explicit caching remains prohibited by the Gemini data policy unless separately approved.

## 15. Provider quota behavior

Rate limits are treated separately from financial budgets.

- handle `429` with bounded backoff;
- do not increase application concurrency merely because provider quota rises;
- queue lower-priority work rather than retrying aggressively;
- show whether a failure is local budget, local rate, or provider quota;
- provider outage/limit does not justify bypassing policy through an unapproved account or model.

## 16. Testing

Automated tests must use a deterministic mock provider by default and must not incur paid calls.

Required tests:

- call rejected before send over each limit;
- warning at 80%;
- workflow stops cleanly mid-plan;
- reservations are atomic under concurrency;
- retries consume budget;
- failed/cancelled jobs reconcile reservations;
- currency/price version stored;
- unknown pricing fails closed;
- kill switch blocks every AI workflow including embeddings;
- budget increase requires authorization/audit;
- no unlimited/negative/NaN configuration accepted;
- provider usage reconciliation detects mismatch.

Live billing smoke tests require explicit opt-in, dedicated budget, synthetic data, and cleanup.

## 17. Reporting

Administrators see:

- today/month spend and remaining budget;
- spend by workspace, user, purpose, model, and job status;
- estimated versus reconciled cost;
- retries and failed-call cost;
- warnings, blocks, anomalies, and kill-switch state;
- provider price version and last reconciliation.

Bid users see workspace cost and safe, non-sensitive explanations for blocked work.

## 18. Pilot review

During pilot, record median and p95 cost for:

- opportunity classification;
- tender summary;
- requirement extraction;
- public research;
- translation;
- section drafting;
- consistency/unsupported-claim review;
- embeddings if enabled.

After at least five representative tenders, review limits based on actual value and risk. A higher budget is not accepted merely because calls are possible; it must map to measurable workflow benefit.

## 19. Acceptance traceability

- **Deterministic enforcement:** Sections 5, 7, and 9.
- **Worker stops safely at limits:** Section 9.
- **Production defaults cannot be unlimited:** Sections 2, 11, and 16.
