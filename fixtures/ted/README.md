# Sanitized TED API Fixtures

**Task:** S0-T07  
**Captured/design date:** 2026-08-04  
**Last audited:** 2026-08-04

These fixtures implement an offline EventNexus test contract derived from the official TED Search API v3 documentation. They are intentionally small and sanitized. They do not replace the official OpenAPI schema or prove current live response behavior.

## Files

- `search-estonia-it-page-1.json` — iteration-mode search page containing Estonian IT notices, Estonian/English language variants, multi-lot fields, and a next token;
- `search-estonia-it-page-2-change.json` — following page containing a changed notice version and the end-of-iteration condition;
- `search-result-notices.json` — synthetic documentation-derived result notices covering both an awarded result and termination without award;
- `search-malformed-item.json` — valid envelope with one malformed item to test validation, quarantine, and partial-failure handling.

## Official references

- `https://docs.ted.europa.eu/api/latest/search.html`
- `https://docs.ted.europa.eu/ODS/latest/reuse/search-api.html`
- `https://docs.ted.europa.eu/ODS/latest/reuse/field-list.html`

## Test rules

Tests must validate the internal adapter contract without live network access, including:

- iteration and durable cursor handling;
- replay and immutable notice versions;
- missing-field behavior;
- multilingual fields;
- lot normalization;
- amendment/change impact;
- awarded versus terminated-without-award outcomes;
- decimal monetary values;
- invalid-item quarantine;
- preservation of raw response references.

Synthetic fixture identifiers, organizations, values, and URLs must never be treated as real procurement or Eventnexus OÜ facts. Before production enablement, validate configured queries and selected fields against the current TED production contract.
