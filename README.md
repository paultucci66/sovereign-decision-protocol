# Sovereign Decision Protocol (SDP)

## An Open Standard for Representing Consequential Decisions

The Sovereign Decision Protocol (SDP) is an open, vendor-neutral protocol for representing consequential decisions.

SDP defines a common language for recording **who acted, what authority they possessed, which policies applied, what context and evidence were considered, what was decided, what was done, and what was learned.**

**SDP is not a product.**

It is a protocol.

Products implement the protocol.

Organizations own their decisions.

## Why SDP Exists

Organizations have standardized networking, identity, payments, encryption, storage, and application integration.

They have not standardized the decision itself.

That gap is becoming material as AI systems, automated workflows, human reviewers, and enterprise applications increasingly participate in consequential organizational decisions.

AI governance is the first urgent use case.

It is not the limit of the protocol.

SDP exists to make decisions portable, auditable, verifiable, and interoperable across systems, vendors, organizations, and time.

## Core Concept: The Decision Object

The Decision Object is the atomic unit of SDP.

It is the authoritative record of why a consequential action occurred.

Applications execute work.

The Decision Object preserves the authority, context, policy basis, evidence, decision, outcome, and organizational memory associated with that work.

## SDP, DCP, and Applications

SDP defines the protocol.

A Decision Control Plane (DCP) implements the orchestration layer for consequential decisions.

Applications produce and consume Decision Objects through SDP.

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

## The Five Proofs of Organizational Trust

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

## Repository Structure

- `rfcs/` — SDP RFC-style specification documents
- `docs/` — architecture, design principles, and explanatory material
- `schemas/` — JSON Schema definitions for core objects
- `examples/` — sample Decision Objects and decision flows
- `research/` — supporting papers and background research

## Status

Draft v0.1.

This repository is intended to evolve as an open standards effort.

Feedback, issues, and contributions are welcome under the Apache 2.0 license.

Maintained by Paul Tucci.
