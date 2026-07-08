# SDP RFC Index

This directory contains RFC-style documents for the Sovereign Decision Protocol.

## Current RFCs

| RFC | Title | Status |
|-----|-------|--------|
| [SDP-0001](SDP-0001.md) | Sovereign Decision Protocol Overview | Draft |
| [SDP-0002](SDP-0002-Decision-Object.md) | Decision Object Specification | Draft Skeleton |
| [SDP-0003](SDP-0003-Authority-Model.md) | Authority Model | Draft Skeleton |
| [SDP-0004](SDP-0004-Identity-Bindings.md) | Identity Bindings | Draft Skeleton |
| [SDP-0005](SDP-0005-Policy-References.md) | Policy References | Draft Skeleton |
| [SDP-0006](SDP-0006-Exchange-Format.md) | Exchange Format | Draft Skeleton |
| [SDP-0007](SDP-0007-Cryptographic-Integrity.md) | Cryptographic Integrity | Draft Skeleton |
| [SDP-0008](SDP-0008-Conformance.md) | Conformance Requirements | Draft Skeleton |

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
