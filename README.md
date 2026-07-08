# Sovereign Decision Protocol (SDP)

## A Medium of Exchange for Consequential Decisions

The Sovereign Decision Protocol (SDP) is an open, vendor-neutral protocol for representing consequential decisions.

It is intentionally small.

It defines the Decision Object.

It defines how decisions can be exchanged.

It does not define the product that creates, governs, stores, or analyzes them.

**SDP is not a product.**

It is a protocol.

Products implement the protocol.

Organizations own their decisions.

## Why SDP Exists

Organizations have standardized networks, identity, payments, messaging, APIs, and now AI.

They have not standardized the decision itself.

That gap matters because organizational judgment is increasingly fragmented across people, applications, documents, AI systems, workflows, and informal channels.

Transactions preserve what happened.

Decisions explain why it happened.

Authority explains who was allowed to make it happen.

SDP exists to make those decisions portable, auditable, verifiable, and interoperable across systems, vendors, organizations, and time.

## What SDP Defines

At the core of SDP is the **Decision Object**.

A Decision Object is the portable record of a consequential decision.

It may reference:

- Identity
- Authority
- Policy
- Context
- Evidence
- Materiality
- Classification
- Disposition
- Outcome
- Memory
- Integrity metadata

The Decision Object is the medium of exchange.

The value built around it belongs in implementations.

## Protocol vs. Product

SDP defines the protocol.

A Decision Control Plane (DCP) is the product category that implements it.

A DCP may orchestrate identity, authority, policy, context, evidence, AI, human review, publication, audit, memory, analytics, and learning.

Those are product responsibilities.

They are not protocol requirements.

```text
Applications
CloudBill, ERP, CRM, AI agents, HR, Security, Custom Systems
        |
        | SDP Decision Requests / Decision Objects
        v
Decision Control Plane
Authority | Policy | Context | Evidence | AI | Human Review | Memory
        |
        | SDP
        v
Decision Objects
Portable, auditable, verifiable records of consequential decisions
```

Kinsana is intended to be a Decision Control Plane implementation.

Kinsana is not the protocol.

## The Five Proofs

| Proof | Question Answered |
|-------|-------------------|
| Identity | Who acted? |
| Authority | Were they authorized? |
| Governance | Which rules applied? |
| Decision | What was decided and done? |
| Memory | What was learned? |

## Design Axioms

1. **Identity is not authority.** Authentication proves who someone is. Authority determines what they may decide.
2. **Representation is not execution.** SDP records decisions. Products and applications execute workflows.
3. **The decision is the source.** Enterprise systems own operational state. Decision Objects preserve the intent, authority, and rationale behind consequential actions.
4. **Context is referenced, not embedded.** SDP records verifiable references to context and evidence. The DCP may retrieve documents, files, web resources, prior decisions, or application data.
5. **Materiality is contextual.** Organizations define which decisions are consequential through policy. SDP represents decisions once they are material.
6. **Simplicity is the adoption strategy.** The protocol should remain small enough to implement and stable enough to trust.

## Repository Structure

- `rfcs/` — RFC-style protocol documents
- `docs/` — architecture, design principles, classification, and explanatory material
- `schemas/` — JSON Schema definitions for core objects
- `examples/` — sample Decision Objects and decision flows
- `articles/` — public-facing articles and drafts
- `research/` — supporting papers and background research

## Status

Draft v0.1.

This repository is intended to evolve as an open standards effort.

Feedback, issues, and contributions are welcome under the Apache 2.0 license.

Maintained by Paul Tucci.
