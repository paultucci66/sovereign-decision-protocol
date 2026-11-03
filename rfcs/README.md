# SDP RFC Index

This directory contains RFC-style documents for the Sovereign Decision Protocol.

## Current RFCs

| RFC | Title | Status | Version | Notes |
|-----|-------|--------|---------|-------|
| [SDP-0001](SDP-0001.md) | Sovereign Decision Protocol Overview | Draft | 0.1 | Scope, definitions, design axioms, Five Proofs, layered architecture |
| [SDP-0002](SDP-0002-Decision-Object.md) | Decision Object Specification | Draft Skeleton | 0.1 | Field specification pending; includes informative Annex A (effects-based decision type taxonomy) |
| [SDP-0003](SDP-0003-Authority-Model.md) | Authority Model | Draft | 0.2 | Normative. Authority Record, Class A/B/C constraint model, registry-facing scope rule, code-system pinning, delegation. Constraint model stable for implementation; verification metadata awaits SDP-0007 |
| [SDP-0004](SDP-0004-Identity-Bindings.md) | Identity Bindings | Draft Skeleton | 0.1 | |
| [SDP-0005](SDP-0005-Policy-References.md) | Policy References | Draft Skeleton | 0.1 | |
| [SDP-0006](SDP-0006-Exchange-Format.md) | Exchange Format | Draft Skeleton | 0.1 | |
| [SDP-0007](SDP-0007-Cryptographic-Integrity.md) | Cryptographic Integrity | Draft Skeleton | 0.1 | Will specify the attestation, status, and log-inclusion profile referenced by SDP-0003 §6 |
| [SDP-0008](SDP-0008-Conformance.md) | Conformance Requirements | Draft | 0.2 | Normative. Level 0 Structural, Level 1 Verifiable-Scope, Level 2 Enforcing-Deployment (proxy position, fail closed). Levels stable; test-vector artifacts pending |

### Status definitions

- **Draft Skeleton** — scope and open questions only; no normative content yet.
- **Draft** — contains normative requirements (RFC 2119 keywords) and is open for review and implementation feedback.

## RFC Intent

The RFC series separates the protocol from implementations.

SDP defines the common representation and exchange of consequential decisions.

Decision Control Plane products create value around that protocol.

## Proposed Process

1. Open an issue describing the problem or proposed change.
2. Discuss whether the issue belongs in the protocol or an implementation.
3. If it belongs in the protocol, update an existing RFC or propose a new one.
4. Keep the core protocol small unless interoperability requires expansion.

## Design Test

Before adding anything to SDP, ask:

- Is this required for two independent systems to exchange a consequential decision?
- Does this belong in the protocol or the product?
- Will this still matter in ten years?
