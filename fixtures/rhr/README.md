# Sanitized RHR Fixtures

**Task:** S0-T06  
**Captured and last audited:** 2026-08-04  
**Purpose:** Offline parser, normalization, lot, amendment, termination, and award tests

## Fixture policy

These fixtures are minimal, sanitized projections from publicly rendered notices on the official RHR domain. They are not claimed to be an official RHR JSON schema and must not be used to infer undocumented API contracts.

The fixtures preserve selected procurement identifiers, organizations, notice types, lot structure, CPV codes, deadlines, values, amendment semantics, and outcome fields needed for tests. Unnecessary natural-person contact names, direct phone numbers, and email addresses are omitted.

Each fixture contains:

- source URL;
- retrieval date;
- source notice ID and procedure identifiers where visible;
- capture type;
- a schema disclaimer;
- expected normalization assertions.

## Files

| File | Scenario | Public source |
|---|---|---|
| `it-multi-lot-notice.json` | Two-lot software development and maintenance contract notice | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/3772382/html` |
| `it-amendment-notice.json` | Multi-lot ICT framework amendment with changed-notice semantics | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/4283918/html` |
| `it-award-notice.json` | Software modernization award/result notice | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/4012336/html` |
| `it-cancelled-notice.json` | Technology-related result notice terminated without an awarded supplier | `https://riigihanked.riik.ee/rhr/api/public/v1/notice/4816678/html` |

## Critical outcome rule

A phrase equivalent to “publication ended” is not sufficient evidence of cancellation. Result notices may contain that text and still identify a successful supplier and signed contract.

The adapter must map a notice to a cancelled/terminated outcome only when explicit authoritative semantics are present, such as:

- no successful supplier was selected;
- the procedure or lot was terminated;
- an explicit termination/cancellation reason is provided; or
- another normalized official result code unambiguously represents termination.

Winner data, contract data, and result values take precedence over a generic publication-status phrase.

## Reuse status

The source notices are publicly rendered official procurement notices. The repository stores only a small sanitized factual projection for software testing and records exact provenance. Before redistributing full source documents or captures, implementation owners must confirm the applicable RHR terms and public-sector information reuse rules current at that time.

## Test rules

Tests must run without live RHR access. They must not assert that these field names are the official RHR response schema. Instead they test the EventNexus fixture contract:

- stable source identity and versions;
- lot parsing;
- date/timezone preservation;
- CPV normalization;
- amendment linkage and impact flags;
- award versus no-award/termination mapping;
- raw provenance retention;
- safe handling of missing fields;
- prevention of false cancellation classification.

When source structures change, add a new fixture version instead of rewriting historical fixtures silently. If a provenance error is found, correct it in a focused commit and increment `fixture_version`.
