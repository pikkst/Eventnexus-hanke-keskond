# Sanitized TED API Fixtures

**Task:** S0-T07  
**Captured/design date:** 2026-08-04

These fixtures implement an offline EventNexus test contract derived from the official TED Search API v3 documentation. They are intentionally small and sanitized. They do not replace the official OpenAPI schema.

Files:

- `search-estonia-it-page-1.json` — iteration-mode search page with Estonian IT notice, multi-lot fields, and next token;
- `search-estonia-it-page-2-change.json` — following page containing a change notice and end-of-iteration condition;
- `search-malformed-item.json` — valid envelope with one malformed item to test partial failure handling.

Official references:

- `https://docs.ted.europa.eu/api/latest/search.html`
- `https://docs.ted.europa.eu/ODS/latest/reuse/search-api.html`
- `https://docs.ted.europa.eu/ODS/latest/reuse/field-list.html`

Tests must validate the internal adapter contract, pagination/replay, missing-field behavior, and immutable version handling without live network access.
