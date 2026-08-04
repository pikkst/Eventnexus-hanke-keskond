# ADR-002 — Worker Queue Selection: Dramatiq

**Status:** Accepted for MVP  
**Date:** 2026-08-04  
**Decision owners:** Product and Engineering  
**Related task:** S1-T04

## Context

EventNexus needs a background job processing system for the worker application. The system must support:
- Redis-backed message queue
- Structured logging compatible with the existing API logging setup
- Health reporting
- Retries, timeouts, and dead-letter handling
- Type-safe, testable job definitions in Python 3.12

Two mature Python options were evaluated: Celery and Dramatiq.

## Decision

Dramatiq is selected for the worker queue framework.

## Consequences

### Positive

- **Smaller footprint and simpler API** — Dramatiq has less boilerplate than Celery, making it easier to bootstrap and maintain in a small team.
- **First-class type hint support** — Dramatiq actors are regular functions with decorators, which works well with Python 3.12 strict typing and mypy.
- **Cleaner middleware model** — Retries, time limits, age limits, and dead-letter routing are explicit middleware, making policy easy to audit.
- **Thread-based worker by default** — Matches the CPU-bound parsing/OCR and I/O-bound AI/document work well without requiring separate process management complexity at bootstrap.
- **Easier testing** — Actors are plain callables; jobs can be tested without a running broker by calling them directly or using Dramatiq's test helpers.

### Negative

- **Smaller ecosystem** — Fewer third extensions and less community tooling than Celery.
- **Less familiar to some teams** — Dramatiq is less widely known, so onboarding documentation matters.

## Alternatives considered

### Celery

Rejected for MVP because:
- Heavier boilerplate and configuration surface for a small team.
- Task definition and result backend patterns are less type-friendly.
- Monitoring extensions (Flower) add operational weight that is unnecessary at bootstrap.
- Dramatiq covers the required features with simpler primitives.

## Verification

- Worker starts via Docker with Redis broker.
- Sample job executes successfully end-to-end.
- Duplicate execution is handled safely via idempotency keys.
- Timeout and retry behavior are covered by unit tests.
- Dead-letter routing is configured and tested.
