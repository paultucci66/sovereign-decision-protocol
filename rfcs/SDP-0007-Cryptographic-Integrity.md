# SDP-0007: Cryptographic Integrity

Status: Draft Skeleton

Version: 0.1

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC will define how SDP Decision Objects support integrity, verification, signatures, timestamps, and tamper evidence.

## Purpose

The purpose of this RFC is to ensure Decision Objects can be trusted, verified, and audited across time and systems.

## Scope

This RFC is expected to define:

- Object hashes
- Signature metadata
- Timestamp metadata
- Canonicalization requirements
- Integrity references
- Redaction integrity patterns
- Supersession integrity patterns
- Verification expectations

## Non-Goals

This RFC will not define:

- A required PKI vendor
- Certificate issuance
- Key management products
- Hardware security modules
- Blockchain requirements
- Storage immutability products

## Design Note

SDP should support cryptographic integrity without mandating any specific trust infrastructure.

The protocol records integrity metadata.

Implementations perform verification.

## Open Questions

- Which fields are covered by object hashes?
- How are appended outcomes linked to original decisions?
- How should redacted derivatives prove relationship to originals?
- What minimum signature metadata is required?

## Status

Draft skeleton. Full specification pending.
