# Design Principles

These principles guide the Sovereign Decision Protocol.

They are intended to keep the protocol small, durable, vendor-neutral, and useful across many implementations.

## 1. Identity Is Not Authority

Authentication proves who a principal is.

Authority determines what that principal may decide.

SDP SHALL NOT define identity providers.

SDP MAY reference identities issued by existing systems such as PKI, OpenID Connect, OAuth-based providers, enterprise identity platforms, government identity systems, or future identity mechanisms.

The protocol concerns decision authority, not authentication.

## 2. Representation Is Not Execution

SDP records decisions.

It does not execute workflows.

Applications, agents, and Decision Control Plane implementations MAY execute actions, route approvals, evaluate policies, retrieve evidence, and coordinate human review.

SDP standardizes the resulting Decision Object.

## 3. The Decision Is the Source

Operational systems own operational state.

The Decision Object preserves the intent, authority, rationale, context, evidence, and outcome behind consequential actions.

A customer system may record that a customer was suspended.

A billing system may execute the suspension.

The Decision Object records why the suspension was authorized.

## 4. Protocol Minimalism

SDP SHOULD define only what is required for interoperable decision representation.

It SHOULD NOT define user interfaces, dashboards, storage engines, workflow engines, AI orchestration, document retrieval, internet search, vector databases, or model behavior.

Those are implementation concerns.

## 5. Vendor Neutrality

No vendor should own the language by which organizations preserve authority, accountability, and decision history.

SDP SHALL be implementable by multiple products, platforms, organizations, and open-source projects.

## 6. Identity Agnostic

SDP SHALL NOT require a specific identity provider.

Implementations MAY bind Decision Objects to Entra ID, Okta, WorkOS, Google, Ping, PKI, decentralized identity systems, national identity systems, or future mechanisms.

## 7. Policy Agnostic

SDP SHALL NOT require a specific policy engine.

A Decision Object MAY reference policies held in GRC systems, policy-as-code systems, legal documents, board resolutions, internal controls, contracts, or other authoritative sources.

## 8. Context by Reference

Context and evidence may be large, distributed, confidential, or externally controlled.

SDP SHOULD record verifiable references to context and evidence rather than embedding full payloads by default.

References SHOULD support integrity checks, versioning, timestamps, and source attribution where practical.

## 9. Materiality Is Contextual

Not every decision requires a Decision Object.

A lunch choice is not material for most organizations.

A lunch supplier decision may be material for a restaurant chain, hospital, school district, or regulated food service provider.

Organizations define materiality through policy.

SDP represents decisions once they are determined to be consequential.

## 10. Immutability of Record

A Decision Object SHOULD be immutable once published.

Later events MAY append outcomes, corrections, reversals, lessons learned, or superseding decisions.

The original decision history SHOULD remain preserved.

## 11. Cryptographic Integrity

Decision Objects SHOULD support cryptographic integrity mechanisms such as hashes, signatures, timestamps, and authority-chain verification.

The authority model may draw from PKI concepts without requiring SDP to become an identity system.

## 12. Extensibility Without Fragmentation

SDP SHOULD allow extensions for domain-specific decision types.

Extensions SHOULD NOT break core interoperability.

The core Decision Object should remain small and stable.
