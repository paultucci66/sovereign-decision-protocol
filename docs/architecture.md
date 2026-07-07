# Architecture

The Sovereign Decision Protocol (SDP) separates the protocol for representing decisions from the products and applications that orchestrate or execute them.

## Layers

```text
Applications
CloudBill | ERP | CRM | HR | Security | AI Agents | Custom Systems
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

## SDP: The Protocol

SDP defines the common representation for consequential decisions.

It includes:

- Decision Object structure
- Identity references
- Authority references
- Policy references
- Context references
- Evidence references
- Decision disposition
- Outcome references
- Integrity metadata
- Versioning
- Exchange semantics

SDP does not execute decisions.

It records them.

## DCP: The Decision Control Plane

A Decision Control Plane is an implementation layer that orchestrates consequential decisions.

A DCP may:

- Resolve identity references
- Evaluate delegated authority
- Retrieve context from documents, applications, files, APIs, or the internet
- Query prior Decision Objects
- Evaluate policy
- Coordinate AI recommendations
- Route human review
- Publish Decision Objects
- Store organizational decision memory
- Analyze outcomes and drift

These are product responsibilities.

They are not part of the core protocol.

## Applications

Applications execute domain-specific work.

Examples include billing platforms, ERPs, CRMs, HR systems, security tools, AI agents, and custom operational systems.

Applications may ask the Decision Control Plane to evaluate a decision.

Applications may receive a Decision Object and execute the resulting action.

Applications may publish outcomes back to the Decision Control Plane.

## Identity, Authority, and Policy

Identity, authority, and policy are separate concerns.

Identity answers:

> Who is the principal?

Authority answers:

> What may this principal decide?

Policy answers:

> What rules govern this decision?

SDP does not replace identity providers or policy engines.

It records references to them and preserves their role in the decision.

## Context and Evidence

The Decision Control Plane may use AI and connectors to retrieve supporting information from document repositories, file systems, enterprise applications, prior decisions, websites, or other sources.

SDP does not specify how that retrieval occurs.

The Decision Object records what context and evidence were considered, ideally by reference with integrity metadata.

## Material Decisions

Not every decision requires SDP.

The protocol is intended for consequential decisions.

Materiality is determined by organizational policy and domain context.

Once a decision is determined to be consequential, SDP provides the standard representation.

## Design Boundary

The protocol describes decisions.

The control plane discovers information and orchestrates decisions.

Applications execute work.

That boundary is intentional.
