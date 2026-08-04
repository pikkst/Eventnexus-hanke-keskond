# RHR Integration Discovery

**Task:** S0-T05  
**Status:** Complete for MVP ingestion decision; automated RHR-wide search remains deferred  
**Research date:** 2026-08-04

## 1. Objective

Determine a permitted, supportable MVP method for bringing Estonian procurement information from the Riigihangete register (RHR) into EventNexus without building an unsupported authenticated scraper or assuming a supplier submission API exists.

## 2. Official systems and sources reviewed

1. RHR public web application: `https://riigihanked.riik.ee/rhr-web/`
2. Public rendered-notice endpoint observed on official RHR host, for example: `https://riigihanked.riik.ee/rhr/api/public/v1/notice/{noticeId}/html`
3. RHR user-guide index maintained by Riigi Tugiteenuste Keskus: `https://rtk.ee/riigihangete-korraldamine/registri-haldamine/rhr-kasutusjuhendid`
4. RHR system record and data dictionary reference in RIHA: `https://www.riha.ee/Infos%C3%BCsteemid/Vaata/RHR`
5. Current Riigihangete seadus in Riigi Teataja: `https://www.riigiteataja.ee/akt/112072025026`
6. TED Search API documentation for published notices: `https://docs.ted.europa.eu/api/latest/search.html`

The RHR support contact published by RTK is `register@riigihanked.riik.ee`, with support hours and phone shown on the guide page. No support contact is required to use the selected manual/public MVP path. Support confirmation is required before implementing undocumented bulk polling or supplier-side submission automation.

## 3. Confirmed public capabilities

### 3.1 Public notice rendering

RHR exposes publicly accessible rendered notice pages on its official domain using a stable observed pattern:

```text
GET /rhr/api/public/v1/notice/{noticeId}/html
```

Observed public rendered notices expose eForms-style information including:

- buyer organizations;
- procedure title and identifier;
- notice identifier and version;
- notice/form type;
- CPV classifications;
- lots;
- values and currencies where present;
- locations;
- procedure type;
- qualification categories;
- evaluation criteria;
- tender language;
- submission deadline and timezone;
- document and tender portal links;
- award information for result notices;
- prior notice reference and change description for amendment notices.

These pages are useful as immutable research fixtures and as a user-directed import source when the notice ID or URL is known.

### 3.2 Public RHR web search

RHR provides a public browser search interface. During this discovery, no current official machine-readable documentation was found that authorizes or specifies automated bulk use of the web application's internal search requests.

Therefore the MVP must not reverse engineer or continuously scrape private/internal web application endpoints.

### 3.3 Public documents

Published notices can link to RHR procurement pages and document sections. Access conditions differ by procedure and document. The product must:

- use only public or user-authorized documents;
- preserve the source URL and access time;
- never bypass authentication, confidentiality gates, CAPTCHA, access controls, or technical restrictions;
- allow manual upload when automated public download is unavailable;
- treat portal links as references, not proof that every linked file is publicly retrievable.

### 3.4 Version and amendment information

Rendered notices can expose:

- notice UUID and version;
- prior notice version being changed;
- change reason;
- changed section identifier;
- human-readable change description;
- notice sending/publication timestamps.

The raw notice identity and version must be retained. A changed notice creates a new source version; it must not overwrite the previous record.

## 4. Data model mapping

| EventNexus field | RHR rendered notice source |
|---|---|
| `source_system` | constant `RHR` |
| `source_notice_id` | numeric notice ID from URL plus notice UUID where exposed |
| `source_version` | notice version suffix and immutable capture hash |
| `procedure_reference` | RHR internal reference / procedure identifier |
| `title` | procedure and/or lot title |
| `buyer` | organization section |
| `notice_type` | form type and notice type |
| `procedure_type` | procedure description/type |
| `cpv_codes` | main and additional classifications |
| `lots` | `LOT-*` sections |
| `value` | estimated/result value where present |
| `submission_deadline` | original text, parsed timestamp, timezone, confidence |
| `languages` | official notice and tender submission languages |
| `evaluation` | criteria name/type/weight/description |
| `documents_url` | document address exactly as published |
| `submission_url` | submission address exactly as published |
| `amendment_of` | previous notice/version reference |
| `change_summary` | deterministic fields plus source description |
| `raw_capture` | stored rendered HTML or approved fixture, hash, retrieval metadata |

Unknown or absent fields must remain `UNKNOWN`/null; they must not be inferred as negative values.

## 5. Selected MVP ingestion strategy

### Decision

The initial RHR strategy is:

1. **Primary automated opportunity discovery:** TED Search API for notices published to TED, including Estonian IT opportunities within the configured query scope.
2. **RHR user-directed import:** accept an RHR procurement URL or public notice URL/ID and capture the public rendered notice plus user-provided files.
3. **Manual import fallback:** allow users to create a source record and upload procurement documents when no supported public machine path exists.
4. **RHR source enrichment:** preserve RHR links and identifiers, and optionally retrieve explicitly public rendered notice content with bounded rate, host allowlisting, caching, and user/audit visibility.
5. **No undocumented bulk RHR search or authenticated scraping in MVP.**

This gives the MVP a permitted and testable RHR path without depending on undocumented internal endpoints.

## 6. Update detection strategy

For a user-imported RHR notice:

- store notice URL, numeric ID, notice UUID/version, retrieval time, HTTP validators if supplied, and content hash;
- poll only when enabled by the source freshness policy or when the user requests refresh;
- use conditional requests where supported;
- compare captured content and parsed identity/version;
- store a new immutable source version on change;
- run deterministic diff before AI summarization;
- raise high-priority impact review for deadline, document, scope, evaluation, eligibility, lot, value, or cancellation changes;
- never delete the previous version after a failed refresh.

For opportunities discovered through TED, use TED as the synchronization cursor and link back to RHR when the Estonian source URL is present.

## 7. Authentication and secrets

The selected MVP ingestion path requires no RHR credentials for public notices.

The system must not store:

- RHR passwords;
- ID-card PINs;
- Smart-ID or Mobile-ID secrets;
- signing keys;
- reusable browser sessions;
- procurement portal authentication cookies.

User-authenticated file acquisition is manual unless a later officially supported interface is approved.

## 8. Rate limits and polite access

No official rate-limit contract for the observed public rendered-notice endpoint was located during this discovery. Therefore:

- default to manual refresh and low-frequency checks;
- cache by source version/content hash;
- never crawl sequential notice IDs;
- cap concurrency to one RHR request per installation initially;
- use bounded retries with exponential backoff and jitter;
- stop on `403`, `429`, repeated `5xx`, changed robots/terms, or structural incompatibility;
- expose last successful refresh and last error;
- obtain support confirmation before increasing automation.

## 9. Raw payload retention

For every import retain:

```text
source_url
retrieved_at
http_status
content_type
content_length
etag_if_present
last_modified_if_present
sha256
notice_id
notice_uuid
notice_version
parser_version
raw_storage_key
```

The normalized model must always link to the raw captured version.

## 10. Reuse and privacy guidance

Public procurement notices are public records, but the product must still minimize unnecessary personal contact details in fixtures, analytics, prompts, and exports. Public availability does not justify sending all content to external AI.

Fixtures in the repository must:

- contain only data necessary for parser and normalization tests;
- replace unnecessary personal names, direct phone numbers, and email addresses with deterministic placeholders where they are not the subject of the test;
- preserve public organization names, procurement identifiers, notice types, dates, CPV codes, lot structure, and change semantics;
- document provenance and retrieval date.

## 11. Unsupported assumptions

The following are not established and must not be implemented as facts:

- that RHR provides a documented public bulk search API equivalent to TED Search API;
- that all RHR procurement documents are anonymously downloadable;
- that internal web application endpoints are stable or permitted for automated reuse;
- that public notice IDs are sequentially crawlable;
- that RHR supports supplier draft creation or tender submission through a public API;
- that browser automation is permitted;
- that a published portal link can be accessed without user authentication;
- that RHR and TED fields are always identical or synchronized at the same time.

## 12. Failure and fallback behavior

- RHR outage must not remove existing opportunities.
- Refresh failure leaves the last successful source version visible and marked stale.
- Manual import and local document analysis remain usable.
- A parser incompatibility stores the raw capture and creates a review task.
- Missing public documents become visible gaps.
- No failed import may be treated as “no requirements” or “no amendment.”

## 13. Implementation prerequisites

Before production code:

- approve this ADR and source freshness policy;
- freeze sanitized fixtures;
- implement host allowlisting and SSRF protection;
- add parser contract tests;
- confirm current RHR terms/robots/support guidance at implementation time;
- contact RHR support before any bulk search, authenticated integration, or increased polling is proposed.

## 14. Acceptance traceability

- **At least one permitted MVP ingestion path selected:** user-directed public notice import plus manual document import, with TED for automated discovery.
- **Unsupported assumptions listed:** Section 11.
- **Update detection documented:** Section 6.
- **No production scraper created:** this task contains research and fixtures only.
- **ADR selects initial strategy:** `docs/adr/ADR-001-rhr-ingestion-strategy.md`.
