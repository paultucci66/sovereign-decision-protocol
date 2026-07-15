# SDP-0008: Conformance Requirements

Status: Draft

Version: 0.2

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC defines what it means for an implementation to conform to the Sovereign Decision Protocol. It establishes conformance levels — including a verifiable-scope level and an enforcing-deployment level — so that a claim of conformance carries a specific, testable meaning rather than a general endorsement.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used as defined in RFC 2119.

## 1. Purpose

Conformance ensures interoperability without forcing all implementations to behave identically. The protocol defines the common contract; products innovate above it. This RFC defines the contract's testable floor.

## 2. Conformance Levels

An implementation MAY claim one or more of the following levels. Levels are additive in rigor but independently claimable.

### 2.1 Level 0 — Structural

The implementation produces and/or consumes Decision Objects and Authority Records that validate against the SDP schemas, with all required fields present and correctly typed. This is the minimum for interoperable exchange.

### 2.2 Level 1 — Verifiable-Scope

The implementation's registry-facing grants validate against the Class A predicate schema (constraint.schema.json) and satisfy SDP-0003 §4: every registry-facing constraint is Class A, every category constraint pins a published taxonomy version, and no Class B or Class C constraint is presented as registry-facing without the disclosures §4 requires. A Level 1 implementation's published scope is deterministically checkable by an independent verifier.

### 2.3 Level 2 — Enforcing-Deployment

The implementation places authority evaluation in the execution path such that a denied decision cannot execute. See §3. This level is claimable only by deployments that gate a live executing agent, not by record-only or analysis-only implementations.

## 3. Enforcement in the Execution Path

Axiom 6.2 states that SDP, as a protocol, represents decisions and does not execute them. That is a statement about the *record format*, and it remains true. It is not a license to deploy a record-only gate against a live agent.

A record-only deployment that observes and logs boundary violations without preventing them produces the worst available posture: a contemporaneous, immutable, witnessed record that the organization knew a boundary and watched it be crossed. Enforced boundaries invert this — a denial on the record is exculpatory, evidence that the control worked. The evidentiary value the protocol exists to create depends on the boundary being enforced, not merely observed.

Therefore, for a Level 2 (Enforcing-Deployment) claim:

1. For every Class A constraint, the deployment MUST place the authority check in the execution path such that a `deny` verdict prevents the constrained action from executing. Failure MUST be closed: absent an authorized decision reference, a consequential action does not proceed. This costs liveness, never safety.
2. A conforming enforcing deployment MUST NOT rely on the agent voluntarily consulting an advisory endpoint. The check MUST sit between the agent and the executing tools — the proxy position — holding or mediating the credentials those tools require, so that a consequential call without an authorized decision reference fails closed.
3. A peer or sidecar component that an agent is merely invited to call, and that an agent holding its own credentials can bypass, does not satisfy this level. It MAY satisfy Level 0 or Level 1.
4. Class B constraints MAY gate execution and, where they do, escalate below threshold rather than fail closed. Class C constraints route to human disposition and do not gate at machine speed.

Record-only operation is a valid SDP use — for reconstruction, analysis, or exchange — and may claim Level 0 or Level 1. It MUST NOT claim Level 2, and an implementation MUST NOT describe record-only operation against a live executing agent as an enforcement control.

## 4. Producer, Consumer, Validator Requirements

- A **producer** MUST emit Decision Objects and Authority Records that meet Level 0. If it claims Level 1, its registry-facing grants MUST meet §2.2.
- A **consumer** MUST reject objects that fail schema validation and MUST treat any constraint it cannot deterministically evaluate as absent for reliance purposes (SDP-0003 §4.3).
- A **validator** MUST report the highest level an object or deployment satisfies and MUST NOT report a higher level than it can test.

## 5. Test Vectors

A conforming test suite SHOULD include, at minimum: paired vectors demonstrating that the same Decision Object yields the same verdict across two independent implementations (deterministic-semantics check for Class A constraints); registry-facing grants that must pass Level 1 and malformed ones that must fail; and an enforcement vector demonstrating that a `deny` prevents execution in a Level 2 deployment. Test vectors are REQUIRED for a Level 2 conformance claim and SHOULD accompany Level 1 claims.

## 6. Discovery Posture (Informative)

Implementers frequently ask whether a decision record creates litigation exposure — "a perfect record of every mistake my agents almost made." The honest answer shapes the deployment:

- Denied and escalated decisions in an *enforcing* deployment are exculpatory: they show the control functioning. This is why Level 2 matters beyond safety — it converts the record from liability into defense.
- Drift flags, variance events, and denied-then-overridden decisions are discoverable. Overrides in particular SHOULD themselves be recorded decisions with their own authority basis, so that an override is an accountable act rather than a silent gap.
- Retention and privilege posture is an implementer responsibility outside this RFC, but implementers SHOULD decide it deliberately rather than inherit it by default.

## 7. Extension and Version Handling

Implementations MUST ignore unknown fields they do not understand rather than reject objects carrying them, except where a field is required at the level being claimed. Version handling and the exchange envelope are specified in SDP-0006.

## 8. Open Questions

- Should Level 2 require a specific fail-closed latency bound, or only the fail-closed property?
- Should test vectors be normative artifacts in this repository or a separate conformance suite?
- How is a mixed deployment described — Level 2 for some tool surfaces, Level 0 for others?

## 9. Status

Draft. Conformance levels and the enforcement-in-path requirement are stable; test-vector artifacts are pending.
