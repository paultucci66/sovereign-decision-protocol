# SDP-0006: Exchange Format

Status: Draft Skeleton

Version: 0.1

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC will define the canonical exchange format for SDP Decision Objects.

The initial target format is expected to be JSON.

## Purpose

The purpose of this RFC is to allow independent systems to exchange Decision Objects consistently.

## Scope

This RFC is expected to define:

- Canonical serialization
- JSON representation
- Field naming conventions
- Required and optional sections
- Extension points
- Version metadata
- Encoding expectations
- Reference formats
- Validation expectations

## Non-Goals

This RFC will not define:

- Transport protocol
- API design
- Storage format
- Database schema
- Message broker implementation
- Product-specific import/export behavior

## Design Note

The exchange format should be simple enough for broad adoption and precise enough for audit, verification, and conformance.

## Open Questions

- Should JSON be the only canonical format for v0.1?
- How should extensions be namespaced?
- How should incompatible versions be handled?
- Should canonicalization be required for signatures?

## Status

Draft skeleton. Full specification pending.
