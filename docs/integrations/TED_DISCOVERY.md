# TED API Discovery

**Task:** S0-T07  
**Status:** Complete  
**Research date:** 2026-08-04

## 1. Decision summary

Use the official **TED Search API v3** as the primary automated discovery source for EU-level procurement notices relevant to Eventnexus OÜ. The Search API is explicitly intended for published-notice search, analysis, bulk download, and commercial data reuse. It does not require authentication for published notices.

Production endpoint pattern:

```text
POST https://api.ted.europa.eu/v3/notices/search
```

Official documentation:

- `https://docs.ted.europa.eu/api/latest/search.html`
- `https://docs.ted.europa.eu/ODS/latest/reuse/search-api.html`
- `https://docs.ted.europa.eu/ODS/latest/reuse/field-list.html`
- `https://api.ted.europa.eu/swagger`

## 2. Search modes and limits

TED supports:

### Page-number mode

- maximum retrievable notices per query: 15,000;
- maximum notices per page: 250;
- maximum fields per page: 10,000.

### Iteration mode

- uses an `iterationNextToken`;
- no documented total-result ceiling;
- maximum notices per page: 250;
- maximum fields per page: 10,000.

Use page-number mode for normal incremental windows and iteration mode for controlled backfills. Queries must use `checkQuerySyntax: true` during configuration validation.

## 3. Query fields required by EventNexus

Official field aliases include:

| Meaning | Search field | Alias |
|---|---|---|
| Buyer country | `buyer-country` | `CY` |
| CPV classification | `classification-cpv` | `PC` |
| Publication date | `publication-date` | `PD` |
| Publication number | `publication-number` | `ND` |
| Notice title | `notice-title` | `TI` |
| Buyer name | `buyer-name` | `AU` |
| Notice type | `notice-type` | — |
| Notice identifier | `notice-identifier` | — |
| Notice version | `notice-version` | — |
| Procedure identifier | `procedure-identifier` | — |
| Place of performance | `place-of-performance` | `RC` |
| Tender deadline | `deadline-receipt-tender-date-lot` and time field | — |
| Main CPV | `main-classification-proc` / lot equivalent | — |
| Additional CPV | `additional-classification-proc` / lot equivalent | — |
| Change description | `change-description` | — |
| Previous/change version | `change-notice-version-identifier` | — |

The field list is versioned by TED and must be treated as an external contract.

## 4. Example Estonian IT queries

The following are configuration examples. Exact syntax must be sent with `checkQuerySyntax: true` against the current production API before enabling synchronization.

### 4.1 Broad Estonia IT services

```text
(CY = "EST" OR RC = "EST") AND PC = "72*"
```

### 4.2 Software and database packages

```text
(CY = "EST" OR RC = "EST") AND (PC = "48*" OR PC = "486*" OR PC = "722*")
```

### 4.3 Recent competition notices

```text
(CY = "EST" OR RC = "EST") AND PC = "72*" AND PD >= "${window_start}" AND PD < "${window_end}"
```

The adapter must not hard-code these strings in domain logic. Query templates, CPV groups, notice types, time windows, and language preferences are versioned configuration.

## 5. Recommended request body

```json
{
  "query": "(CY = \"EST\" OR RC = \"EST\") AND PC = \"72*\" AND PD >= \"2026-08-01\" AND PD < \"2026-08-02\"",
  "fields": [
    "publication-number",
    "notice-identifier",
    "notice-version",
    "publication-date",
    "notice-title",
    "notice-type",
    "procedure-identifier",
    "buyer-name",
    "buyer-country",
    "classification-cpv",
    "place-of-performance",
    "deadline-receipt-tender-date-lot",
    "deadline-receipt-tender-time-lot",
    "official-language",
    "change-description",
    "change-notice-version-identifier"
  ],
  "limit": 250,
  "paginationMode": "ITERATION",
  "checkQuerySyntax": true,
  "scope": "ACTIVE"
}
```

`scope` values and field availability must be validated against the current Swagger contract; configuration validation must fail visibly rather than silently removing unsupported fields.

## 6. Normalized opportunity mapping

| EventNexus field | TED source |
|---|---|
| source identity | publication number, notice identifier, version |
| publication time | publication date plus source metadata |
| title | notice title by language |
| buyer | buyer organization fields |
| country/location | buyer country and place-of-performance hierarchy |
| procedure | procedure identifier and type |
| notice type | eForms notice type/subtype |
| CPV | procedure, part, and lot classifications |
| lots | XML/eForms lot structures or selected result fields |
| deadline | lot deadline date/time; retain original timezone/source representation |
| languages | official-language and downloadable format/language URLs |
| values | estimated and result values with currencies |
| change | change reason, description, previous notice/version references |
| documents | URLs returned for available formats and languages |
| raw payload | complete API response plus downloaded official XML where selected |

Unknown fields are preserved in raw data and mapped to explicit unknown/null values.

## 7. Notice types

The adapter must distinguish at least:

- planning/prior information;
- competition/contract notice;
- change notice;
- result/contract award notice;
- contract modification;
- completion notice;
- cancellation/competition termination semantics.

Notice-type mappings are versioned because eForms code lists evolve.

## 8. Multilingual handling

- Preserve every source language and the official-language list.
- Prefer Estonian source material when available.
- Retain English and other official variants as separate immutable artifacts.
- Never overwrite original text with machine translation.
- A generated Estonian translation is a derived artifact with model/version/reviewer metadata.
- Search and deduplication use language-independent identifiers before title similarity.

## 9. Pagination and replay strategy

### Incremental synchronization

1. Query a closed publication-time window with overlap.
2. Store window start/end, query version, field set, pagination mode, and iteration token.
3. Upsert by immutable source notice identifier/version.
4. Repeat the last completed window after restart.
5. Deduplicate idempotently.
6. Advance the durable cursor only after every page in the window commits successfully.

### Overlap

Use an initial 24-hour overlap to tolerate delayed publication/indexing and clock differences. Deduplication by notice identity/version prevents duplicate business records.

### Backfill

Use iteration mode in bounded date partitions, never an unbounded single job. Store progress per partition and enforce cost/time/storage limits.

## 10. Change detection

- A new notice version creates a new immutable source version.
- Compare identifiers, version, lots, deadlines, CPV, values, documents, evaluation data, and change fields deterministically.
- Do not depend only on title/date similarity.
- Run AI change summary only after deterministic diff.
- Material changes trigger impact review and invalidate affected downstream analysis or approval.

## 11. Error and outage behavior

- `400`: mark query/configuration invalid; do not retry blindly.
- `429`: respect backoff and retry-after where provided.
- `5xx`/network failure: bounded retries with jitter; retain last successful data.
- malformed result: store safe diagnostic and raw response reference, stop affected page/window.
- missing optional fields: preserve unknown; do not reject the entire notice.
- API outage: manual import and existing opportunities remain available.

## 12. Rate and resource controls

- maximum page size 250;
- installation-level concurrency limit;
- configured requests/minute independent of theoretical service capacity;
- HTTP timeouts and response-size limits;
- daily backfill cap;
- no full XML download until notice passes configured relevance or retention rules, unless a fixture/backfill mode explicitly requires it;
- cache by notice/version and URL.

## 13. Fixture strategy

Fixtures under `fixtures/ted/` must include:

- Estonian competition notice;
- English/bilingual notice;
- multi-lot notice;
- amendment/change notice;
- result notice;
- search response with iteration token;
- malformed/missing-field response.

Fixtures are sanitized and tests do not require live TED access.

## 14. Security

- allowlist `api.ted.europa.eu` and documented TED download hosts;
- validate redirects and block private/reserved IP destinations;
- do not fetch arbitrary URLs supplied by model output;
- enforce response size and archive extraction limits;
- sanitize filenames and content types;
- treat XML as untrusted and disable external entities;
- no API key is needed for published notice search; do not add one unnecessarily.

## 15. Versioning

Record:

```text
api_version
query_template_version
field_set_version
cpv_profile_version
notice_codelist_version
eforms_sdk_version_if_known
parser_version
retrieved_at
raw_response_hash
```

TED API v3 is selected. API v2 compatibility is not used for new implementation unless a specific v3 blocker is documented.

## 16. Acceptance traceability

- **Example queries for Estonian IT tenders:** Section 4.
- **Normalized field mapping:** Section 6.
- **Pagination and replay strategy:** Section 9.
- **Sanitized fixtures:** `fixtures/ted/`.
