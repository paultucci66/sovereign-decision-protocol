# SDP-0002: Decision Object Specification

Status: Draft Skeleton

Version: 0.1

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC will define the Decision Object, the atomic unit of the Sovereign Decision Protocol.

A Decision Object is the portable, auditable, verifiable representation of a consequential decision.

## Purpose

The purpose of this RFC is to specify the minimum structure required for independent systems to exchange consequential decisions.

## Scope

This RFC is expected to define:

- Required Decision Object fields
- Optional Decision Object fields
- Identity references
- Authority references
- Policy references
- Context references
- Evidence references
- Materiality metadata
- Classification metadata
- Decision disposition
- Outcome references
- Memory references
- Integrity metadata
- Versioning

## Non-Goals

This RFC will not define:

- Workflow execution
- User interfaces
- AI orchestration
- Storage implementation
- Policy engine implementation
- Document retrieval
- Analytics

## Open Questions

- Which fields are mandatory for conformance?
- Which fields are optional extensions?
- How should redacted Decision Objects reference originals?
- How should outcomes append without mutating the original decision?

## Annex A (Informative): Decision Type Reference Taxonomy

`decision_type` is an open string field, not a closed enum. Locking it to a fixed enum would force every implementation into one vendor's categories forever, which defeats the interoperability goal of a shared registry.

Instead, this annex offers a reference taxonomy that implementations SHOULD draw from, or extend, when populating `decision_type`. Comparability across independent SDP implementations depends on convergent, not identical, category use — the same logic that governs preferred code systems for registry-facing scope elsewhere in the protocol (see SDP-0003).

The taxonomy is effects-based: categories are defined by what a tool or action *does to the world*, not by department, system, or business process. This keeps classification decidable from the action itself, independent of organizational context.

| # | Category | Representative examples |
|---|---|---|
| 1 | Moves money | payments, credits, refunds, purchases, payroll |
| 2 | Creates obligations / binds the organization | contracts, quotes, acceptances, commitments — including promises made in prose |
| 3 | External communication | email/chat to customers, public posts, filings sent outward |
| 4 | Grants or changes access & authority | account provisioning, permission changes, key issuance — decisions *about* decision-power |
| 5 | Regulated data / regulated decisions | CPNI, PII, credit denials (FCRA/ECOA), health, housing, adverse actions |
| 6 | Writes to systems of record | billing master data, GL entries, CRM records, production config |
| 7 | Irreversible / destructive operations | deletes, cancellations, terminations |
| 8 | Government & regulatory filings | anything submitted to an agency |
| 9 | People decisions | hiring, firing, discipline, scheduling |
| 10 | Physical-world actuation | dispatch, shipping, device control |

This list is informative, not normative. It is not exhaustive, and it is not a conformance requirement. Implementations MAY define additional categories; implementations that wish to interoperate on `decision_type` comparisons SHOULD prefer a category from this list, or a published extension of it, over an ad hoc string.

Category alone does not determine whether an action rises to the level of a recorded Decision Object — that determination is a materiality question, addressed by the `materiality` field. Materiality *scoring methodology* is intentionally left to implementations (see SDP-0008 Conformance for the boundary between protocol-defined slots and implementation-defined judgment).

## Status

Draft skeleton. Full specification pending.
