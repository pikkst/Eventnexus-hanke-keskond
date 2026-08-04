# Sanitized RHR Fixtures

**Task:** S0-T06  
**Captured:** 2026-08-04  
**Purpose:** Offline parser, normalization, lot, amendment, cancellation, and award tests

## Fixture policy

These fixtures are minimal, sanitized projections from publicly rendered notices on the official RHR domain. They are not claimed to be an official RHR JSON schema and must not be used to infer undocumented API contracts.

The fixtures preserve procurement identifiers, organizations, notice types, lot structure, CPV codes, deadlines, values, amendment semantics, and outcome fields needed for tests. Unnecessary natural-person contact names, direct phone numbers, and email addresses are omitted or replaced with placeholders.

Each fixture contains:

- source URL;
- retrieval date;
- source notice ID and notice UUID/version where visible;
- capture type;
- sanitization notes;
- expected normalization assertions.

## Files

| File | Scenario | Public source |
|---|---|---|
| `it-multi-lot-notice.json` | Multi-lot software development framework notice | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/4821118/html` |
| `it-amendment-notice.json` | IKT framework amendment with changed notice semantics | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/4283918/html` |
| `it-award-notice.json` | Software development award/result notice | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/4012336/html` |
| `it-cancelled-notice.json` | Software development procedure marked ended/cancelled | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/3774462/html` |

## Reuse status

The source notices are publicly rendered official procurement notices. The repository stores only a small sanitized factual projection for software testing and records exact provenance. Before redistributing full source documents or captures, implementation owners must confirm the applicable RHR terms and public-sector information reuse rules current at that time.

## Test rules

Tests must run without live RHR access. They must not assert that these field names are the official RHR response schema. Instead they test the EventNexus fixture contract:

- stable source identity and versions;
- lot parsing;
- date/timezone preservation;
- CPV normalization;
- amendment linkage and impact flags;
- cancellation/outcome mapping;
- raw provenance retention;
- safe handling of missing fields.

When source structures change, add a new fixture version instead of rewriting historical fixtures silently.
