# Source Freshness and Synchronization Policy

**Task:** S0-T08  
**Status:** Complete  
**Last updated:** 2026-08-04

## 1. Scope

This policy governs TED, user-imported public RHR notices, manual imports, documents, amendments, and source outage behavior.

## 2. Freshness classes

| Class | Examples | Target refresh latency |
|---|---|---|
| `CRITICAL_ACTIVE` | active bid with deadline within 7 days; known clarification/amendment period | source check every 2 hours where permitted; visible alert within 4 hours |
| `ACTIVE` | active opportunity/workspace with deadline over 7 days | every 6 hours where permitted |
| `WATCHING` | shortlisted or watched opportunity | every 24 hours |
| `REFERENCE` | historical award/outcome/research | weekly or manual |
| `MANUAL_ONLY` | authenticated/restricted source or unsupported integration | user refresh/import only |

These are maximum product frequencies, not permission to exceed source rules. A stricter official limit always wins.

## 3. Source-specific defaults

### TED Search API

- incremental windows every 6 hours;
- 24-hour overlap to tolerate delayed indexing;
- daily reconciliation of the last 7 days;
- iteration mode only for bounded backfills;
- max page size 250;
- bounded concurrency and backoff.

### RHR public imported notice

- no bulk crawl;
- refresh only explicitly imported notice URLs;
- default 6 hours for active workspaces, 24 hours for watching, manual for reference;
- one concurrent request per installation initially;
- conditional requests and content-hash caching where supported;
- stop/reduce frequency on `403`, `429`, repeated `5xx`, structural change, or support/terms concern.

### Manual imports

- freshness is user-declared;
- UI displays import time, source date, source URL/reference, and `manual` status;
- users can mark replaced/superseded files;
- final readiness requires a manual source-freshness confirmation within 24 hours of package approval for active tenders.

## 4. Durable cursor and transaction rules

A sync window is complete only after every page and item is committed or deliberately quarantined under a documented partial-page policy.

Store:

```text
source
query_version
window_start
window_end
pagination_mode
next_token_or_page
started_at
completed_at
last_success_at
last_error_code
last_error_at
items_seen
items_created
items_versioned
items_quarantined
raw_response_hashes
```

Cursor advancement must be atomic with the completed page/window state. Restart repeats the last incomplete unit idempotently.

## 5. Amendment urgency

The following changes are `CRITICAL`:

- submission deadline or timezone;
- cancellation/termination;
- required document added/replaced;
- eligibility/exclusion criteria;
- selected lot structure or scope;
- evaluation criteria/weights;
- binding contract/pricing terms;
- clarification response affecting requirements.

Target: visible event within 4 hours of source detection and immediate invalidation of affected readiness/approvals.

Other changes target visibility within 24 hours.

## 6. Manual refresh

Authorized users may request refresh. The system must:

- deduplicate simultaneous requests;
- show current job and last successful result;
- enforce source limits;
- never imply that clicking refresh guarantees current source data;
- preserve previous data on failure.

## 7. Backoff and retries

- network timeout: configurable, initial 20 seconds connect/read bound;
- transient retries: maximum 3 attempts;
- exponential backoff with jitter;
- honor `Retry-After`;
- no retry storm across workers;
- circuit breaker after repeated source failure;
- manual reset/health check available to administrators.

Permanent validation/configuration errors do not retry automatically.

## 8. Source outage behavior

- existing opportunities and documents remain available;
- no record is deleted because a source is unavailable;
- UI shows last successful synchronization and staleness;
- final package approval warns or blocks according to configured maximum age;
- manual import remains available;
- outage notifications contain no tender text or secrets;
- recovery replays missed windows with overlap.

## 9. Retention

- immutable raw source versions retained through the tender lifecycle and audit retention period;
- normalized superseded versions retained for traceability;
- temporary download files deleted promptly after hashing/storage;
- source sync operational logs follow configured shorter retention;
- deletion never breaks package, approval, citation, or submission evidence integrity.

Exact retention durations are finalized in S15-T07; this policy requires relationship-preserving retention.

## 10. User-visible freshness

Every source-backed screen must expose:

- source system;
- authoritative URL/reference;
- source publication/version time when available;
- last successful retrieval;
- next scheduled check;
- freshness state: `CURRENT`, `AGING`, `STALE`, `ERROR`, `MANUAL_ONLY`, `UNKNOWN`;
- last error summary;
- amendment/change count;
- whether analysis/approval is stale.

Suggested default thresholds:

| Context | Current | Aging | Stale |
|---|---:|---:|---:|
| deadline within 7 days | <= 4h | >4h to 8h | >8h |
| other active tender | <= 8h | >8h to 24h | >24h |
| watched opportunity | <= 24h | >24h to 48h | >48h |
| historical/reference | <= 7d | >7d to 30d | >30d |

## 11. Final approval freshness gate

Before final package approval:

1. every active authoritative source has a successful check within the configured bound;
2. manual-only sources are explicitly reconfirmed by the Bid Lead;
3. no unreviewed amendment exists;
4. all document versions used by citations and approvals are current;
5. deadline and timezone are reconfirmed;
6. any source outage exception is accepted by an authorized decision-maker with rationale.

AI cannot override this gate.

## 12. Acceptance traceability

- **No source polled more aggressively than permitted:** source rule precedence and conservative defaults in Sections 2–3.
- **Deadline/amendment target latency:** Sections 2 and 5.
- **Failed sync does not delete existing opportunities:** Section 8.
- **Freshness visible to users:** Section 10.
