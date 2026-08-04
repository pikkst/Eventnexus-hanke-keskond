# ADR-001 — Initial RHR Ingestion Strategy

**Status:** Accepted for MVP  
**Date:** 2026-08-04  
**Decision owners:** Product and Engineering  
**Related task:** S0-T05

## Context

EventNexus must find Estonian IT procurements and preserve authoritative RHR references. Research confirmed public RHR rendered-notice pages and the public browser application, but did not identify a current officially documented bulk RHR search contract suitable for unrestricted automated polling. TED provides an officially documented Search API for published notices.

Using undocumented RHR application endpoints as a production crawler would create stability, permission, support, and compliance risk. Supplier-side authenticated automation would also introduce identity-secret and submission risks.

## Decision

The MVP will use:

1. TED Search API v3 as the primary automated source for notices within TED scope.
2. User-directed RHR import from a known public RHR procurement/notice URL or notice ID.
3. Manual notice and document import as the guaranteed fallback.
4. Low-frequency, bounded refresh of explicitly imported public RHR notice URLs only.
5. Immutable raw captures, source versions, hashes, and deterministic change detection.
6. No crawling of sequential IDs, no reverse-engineered bulk RHR search, no authenticated portal scraping, and no supplier submission automation.

## Consequences

### Positive

- Uses a documented open API for scalable discovery.
- Preserves RHR as the Estonian authoritative portal reference.
- Keeps MVP functional when RHR automation is unavailable.
- Avoids storing portal credentials and identity secrets.
- Makes source behavior testable with fixtures.

### Negative

- Some below-threshold or non-TED Estonian opportunities may require manual RHR import.
- RHR freshness for imported notices depends on conservative polling or user refresh.
- Coverage cannot be claimed as complete until an approved RHR-wide source is available.

## Alternatives rejected

### Scrape the RHR web search application

Rejected for MVP because no stable, officially documented contract or reuse/rate-limit guidance was established.

### Browser automation with user credentials

Rejected because it creates authentication, legal, security, support, and reliability risks and is unnecessary for MVP discovery.

### RHR-only discovery

Rejected because a supported bulk source was not established, while TED Search API is officially documented and open for published notices.

### TED-only with no RHR import

Rejected because Eventnexus needs Estonian source links, below-threshold/manual cases, and RHR-specific document workflows.

## Revisit triggers

Reassess this ADR when:

- RHR publishes an official documented public search/open-data API;
- RHR support confirms a permitted machine integration;
- the product demonstrates material missed opportunities outside TED scope;
- official supplier-side integration becomes available;
- source terms, architecture, or public endpoints change.

Any revised strategy requires a new ADR, updated fixtures, threat model, and source policy review.
