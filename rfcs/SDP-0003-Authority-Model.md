# SDP-0003: Authority Model

Status: Draft

Version: 0.2

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC defines how SDP represents authority for consequential decisions. SDP separates identity from authority: authentication proves who a principal is; authority determines what that principal may decide. This RFC specifies the structure of an Authority Record, the classification of the constraints that bound a grant, and the rule that governs which constraints may be published for third-party verification.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used as defined in RFC 2119.

## 1. Purpose

SDP records the authority basis for a decision and enables independent verification of it. This RFC defines a vendor-neutral authority model that Decision Objects reference via `authority_record_id`. It does not mandate a specific PKI, identity provider, or policy engine.

## 2. The Authority Record

An Authority Record is the representation of a grant: a principal's authorization to make a bounded class of decisions. It is referenced by, and outlives, the individual Decision Objects made under it.

An Authority Record MUST carry, at minimum:

- `authority_id` — stable identifier for the grant
- `role` — the granted role or capacity
- `granted_by` — the principal issuing the grant
- `granted_at` — issuance timestamp
- `constraints` — the bounds on the grant (see §3)

An Authority Record SHOULD additionally carry attestation, status, and log-inclusion metadata sufficient for a verifier to establish that the grant is authentic, current, and was recorded before the decisions made under it (see §6). A grant that cannot be shown to have existed at decision time confers no evidentiary benefit; per the witnessing architecture, a grant that is not logged is not valid.

## 3. Constraint Classes

Every constraint in an Authority Record MUST declare its class. The class determines how the constraint is enforced and whether it may be published for third-party verification.

### 3.1 Class A — Deterministic

A constraint is Class A if and only if two independent compliant implementations, given the same grant and the same proposed act, MUST return the same in-or-out verdict with no probabilistic inference and no human discretion. This is Axiom 6.3 (deterministic semantics) applied to scope.

Class A constraints are enforced by a policy engine at machine speed and are reproducible from `(grant, act)` alone. Examples: per-action monetary cap, aggregate cap over a window, code-set membership, allow/deny lists, time windows, expiry, jurisdiction codes, rate limits, n-of-m co-authorization, action-pattern exclusions.

### 3.2 Class B — Classifier-mediated

A Class B constraint reduces a semantic judgment to a versioned model's verdict against a confidence threshold — for example, "is this invoice line within category X." A Class B constraint MUST record, on each decision it gates, the classifier's identity, version, threshold, and verdict as evidence. A below-threshold result MUST escalate.

### 3.3 Class C — Human judgment

A Class C constraint expresses a standard, not a rule — "commercially reasonable," "best interests," fiduciary duties, novel situations. A Class C constraint MUST route to human disposition, and the human ruling is itself a recorded decision. Implementations MUST NOT represent a Class C constraint as machine-enforced.

## 4. Registry-Facing Scope

Registry-facing scope is any portion of a grant published for third-party verification.

**Registry-facing scope MUST consist solely of Class A constraints.**

The reason is a fairness condition, not a preference. Constructive notice — the doctrine that lets a counterparty be deemed to know a published boundary — can only fairly attach to a boundary that is machine-decidable. A published scope that requires judgment to interpret gives the checker no knowledge, so no knowledge can be imputed, and the loss-shifting the registry exists to produce never engages. Worse, an ambiguous published scope is construed against the drafter. Prose scope in a registry recreates, at the registry layer, the exact problem the registry exists to solve.

Accordingly:

1. A Class B constraint presented to any external party MUST disclose the classifier's identity, version, and threshold; absent that disclosure it is not registry-facing.
2. A Class C constraint MUST NOT appear in registry-facing scope in any form.
3. A verifier that cannot deterministically evaluate a constraint MUST treat that constraint as absent for reliance purposes; it confers no constructive-notice effect.

The registry-facing grant is the financing statement of authority: like a UCC-1, it is a *notice* of the decidable envelope, not the underlying agreement. Full grant details remain private, disclosed selectively to counterparties who need them.

## 5. Category Constraints and Code Systems

A Class A category constraint MUST be expressed against a published, versioned code system rather than a description. Grants MUST pin the taxonomy version they reference; an unpinned taxonomy reference is not Class A.

Established taxonomies SHOULD be preferred over private code systems. A private code system MUST be published at a stable, versioned URI to qualify as Class A. Where more than one taxonomy could express a scope, selection SHOULD follow: fitness for the constraint at the required granularity (gate); recognition by the courts, regulators, and counterparties where the grant will be read (gate); stewardship and longevity of the maintaining institution; open access; then adoption breadth and technical quality as tiebreakers. A new standard SHOULD be adopted only to fill a capability gap an established one genuinely cannot.

Reference taxonomies by domain (informative):

| Domain | Preferred (reach) | Regional / adjacent |
|---|---|---|
| Products and services | UNSPSC | CPV, ECLASS, GS1 GPC, HS/WCO |
| Merchant / spend categories | MCC (ISO 18245) | network supersets |
| Industries | ISIC | NAICS, NACE, UK SIC |
| Jurisdictions | ISO 3166-1 / -2 | UN M49, UN/LOCODE |
| Currencies | ISO 4217 | ISO 24165 DTI (digital assets) |
| Payment purpose | ISO 20022 external code sets | network reason codes |
| Counterparty identity | LEI (ISO 17442), vLEI | UEI, DUNS, national registry numbers |

Two precision requirements. A merchant category code (MCC) classifies the *merchant*, not the purchased item; a grant using MCC MUST NOT be read as constraining commodity type, and vice versa. Industry scope intended to travel across borders SHOULD anchor on ISIC and treat NAICS/NACE as regional profiles.

## 6. Verification Metadata

To support the evidentiary role of a grant, an Authority Record SHOULD carry:

- `attestation` — signature(s) binding the grant to its issuer and, where applicable, the agent identity it authorizes
- `status` — current validity (active, suspended, revoked, expired) resolvable at or after decision time
- `log_inclusion` — proof that the grant was recorded in a witnessing log prior to decisions made under it

The normative cryptographic profile for these fields is deferred to SDP-0007. This RFC requires their presence in the model; SDP-0007 specifies their construction. Implementations MAY satisfy these requirements by adopting an external verifiable-credential profile and inheriting its attestation, status, and inclusion semantics.

## 7. Delegation

An Authority Record MAY carry a `delegation_chain` recording the path by which authority reached the granting principal. Each link in a registry-facing delegation chain MUST itself satisfy §4 — a delegated grant cannot publish a broader or less decidable scope than it holds.

## 8. What This Model Does Not Establish

This RFC defines the representation and verification of authority scope. It does not, by itself, create constructive notice against the world; that effect depends on adoption, custom, or statute that this protocol cannot conjure. The near-term, unilateral value of a conforming Authority Record is evidentiary: a contemporaneous, witnessed record of the scope a principal granted and the enforcement applied to it. See SDP-0008 for the enforcement posture required to realize that value, and the corpus limitations note for what authority scope does not govern.

## 9. Open Questions

- Should `status` resolution be pull (verifier queries) or push (short-lived signed status), and at what freshness requirement?
- What is the minimum `log_inclusion` proof for conformance, and how does grant validity behave when a witnessing log becomes unavailable?
- How should emergency or break-glass authority be represented within the Class A discipline?

## 10. Status

Draft. Constraint-class model and registry-facing rule are stable enough for implementation; verification metadata (§6) awaits the SDP-0007 cryptographic profile.
