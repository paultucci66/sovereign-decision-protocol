# Contributing

The Sovereign Decision Protocol (SDP) is intended to evolve as an open standards effort.

The goal is interoperability.

The goal is not to protect the first draft.

## How to Contribute

Use GitHub Issues to:

- Challenge assumptions
- Ask clarifying questions
- Propose changes to RFCs
- Suggest Decision Object fields
- Identify interoperability problems
- Raise implementation experience from real systems
- Point to legal, regulatory, technical, or operational requirements the protocol should consider

Use Pull Requests to:

- Improve wording
- Add examples
- Propose RFC changes
- Correct terminology
- Improve schemas
- Clarify design boundaries

## What Belongs Here

This repository is for the protocol.

Appropriate topics include:

- Decision Object structure
- Authority references
- Policy references
- Context and evidence references
- Materiality metadata
- Classification metadata
- Integrity and verification
- Versioning
- Exchange semantics
- Conformance

## What Does Not Belong Here

This repository is not for product implementation details.

The following generally belong in Decision Control Plane implementations or other product repositories:

- User interfaces
- Workflow engines
- AI model selection
- Prompt design
- Storage architecture
- Policy engine implementation
- Document retrieval implementation
- Vector databases
- Analytics dashboards
- Customer-specific business logic
- Pricing
- Sales material

If a proposal is required for two independent systems to exchange a consequential decision, it may belong in SDP.

If a proposal concerns how a product creates, governs, stores, analyzes, or learns from decisions, it probably belongs in a DCP implementation.

## Design Discipline

Before proposing a change, ask:

1. Is this required for interoperability?
2. Does this belong in the protocol or the product?
3. Will this still matter in ten years?
4. Does it make the protocol simpler or more complicated?
5. Does it preserve vendor neutrality?

## RFC Process

Major protocol changes should be proposed as RFC updates or new RFCs.

RFCs should include:

- Status
- Motivation
- Scope
- Non-goals
- Definitions
- Proposed structure or behavior
- Examples where useful
- Open questions

Drafts are expected to change.

That is the point.

## Tone

Be direct.

Be specific.

Challenge ideas, not people.

Prefer clear premises and concrete examples over abstract opinion.

The protocol should get stronger through scrutiny.

## Licensing

By contributing, you agree that your contribution may be included under the repository license.

This repository currently uses the Apache 2.0 license.
