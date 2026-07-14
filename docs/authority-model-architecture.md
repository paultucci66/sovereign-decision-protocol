# Design Note: Authority Model Architecture

**Status:** Working note. Input to SDP-0003 (Authority Model), which is not yet drafted.  
**Date:** July 2026  
**Author:** Paul Tucci

---

## Purpose

SDP-0001 § 9 states that the authority model "may use concepts similar to public key infrastructure" and lists trust anchors, delegated authority, authority credentials, decision signatures, revocation, time-bound authority, and chain of authority — without specifying the design. This note records the architectural reasoning behind that direction, the prior art it must answer to, and the specific problems SDP-0003 will need to solve.

---

## 1. Why the prior art failed — and why that is instructive

There have been serious attempts to bind *authorization* rather than *identity* to a cryptographic credential:

- **SPKI/SDSI** (RFC 2693)
- **X.509 Attribute Certificates** (RFC 5755) — an Attribute Authority binding privileges to an identity. Standardized. Almost entirely unused.
- **X.509 Proxy Certificates** (RFC 3820) — delegation of a subset of rights. Deployed in grid computing, nowhere else.
- **Macaroons** (contextual caveats), **Biscuit** (decentralized authorization tokens)
- **W3C Verifiable Credentials / DIDs**

Every one of these built a **credential**. None built a **record**.

A credential looks forward: *this agent may do X.* It is checked before the act, then discarded. But nobody needed cryptography for that, because **access control can be done with a database lookup.** An ACL is cheaper, simpler, and sufficient. The prior art solved a problem that already had a free solution — which is why it saw so little adoption.

A record looks backward: *this decision was made, under this authority, at this moment.* And a record has requirements a database lookup cannot satisfy:

- Verifiable by an adversary
- Verifiable years later
- Verifiable when the issuer is hostile, uncooperative, bankrupt, or gone
- Verifiable by a court with no access to the issuer's systems and no reason to trust their logs

**That is the requirement that makes cryptography necessary rather than merely possible.**

The prior art was not wrong. It was aimed at the wrong artifact, and the artifact it aimed at did not need it.

SDP is not a revival of SPKI. It is the record SPKI never was.

**Corollary for the spec:** the authority credential (AAR) is scaffolding. The Decision Object is the artifact.

---

## 2. The trust root is a legal person

This is the simplification that makes the model clean where the prior art was not.

**WebPKI needs a third-party CA** because the relying party has never met the server and needs a stranger to vouch that a name belongs to a key. That necessity created the CA industry, and most of the friction in WebPKI comes from it — root stores, cross-signing, the politics of trust.

**Authority has no such problem.** A counterparty transacting with an agent is not dealing with a stranger. It is dealing with a company it already knows. It does not need a third party to vouch that Acme Corp exists.

It needs to verify that **this agent speaks for Acme.**

And Acme can attest to that itself.

**Acme is its own root.**

- No CA industry
- No root store
- No third party in the trust path between two parties who already know each other

The authority root is the **legal person** — and the legal person is the party who bears the liability.

**In PKI the root is a trust anchor. In an authority chain the root is a liability anchor.** The chain a counterparty validates in order to transact is the same chain a court follows afterward to locate the responsible principal. Revoke at the root and every downstream grant dies — technically and legally, in the same instant.

The trust chain is the liability chain. Not by analogy. By construction.

### Distributing the root key

The remaining question: how does a counterparty learn Acme's root key?

**A registry of legal persons.** Corporate registries already establish that an entity exists, who its officers are, and what its legal identity is. The **LEI/vLEI** system (GLEIF) already binds legal entities and official organizational roles to cryptographic credentials and is recognized in financial regulation.

**The certificate authority for agentic authority is the corporate registry.**

The authority chain terminates in a *legal* title system, not a technical one. That is precisely why it can carry liability. (This is the "authority registries as title systems" argument of Agentic Law II, arrived at from the technical side.)

---

## 3. Credential and record are different objects

| | Agent Authority Record | Decision Object |
|---|---|---|
| Direction | Forward-looking | Backward-looking |
| Lifetime | Long-lived, revocable | Minted once, sealed, immutable |
| Checked | Before the act — by the enforcement layer and by the counterparty | After the fact — by auditors, courts, counterparties |
| Purpose | Authorize | Prove |

### The Decision Object staples the authority proof

**Critical design decision.** The Decision Object must not contain a *pointer* to a live registry. It must contain a **snapshot**: the authority chain, plus cryptographic evidence that the chain was valid at that moment.

This is OCSP stapling, applied to authority.

It is what makes the record usable, because the record must survive:

- Revocation of the grant (a later revocation must not invalidate a decision made under a then-valid grant)
- The issuer's bankruptcy or dissolution
- An uncooperative party in discovery
- The registry going offline

**A record that requires calling the issuer to verify is worthless in precisely the moment it is needed — when the issuer is the opposing party.**

The Decision Object must be **self-contained and offline-verifiable.**

---

## 4. Three problems SDP-0003 must solve

### 4.1 Backdating (the most important attack)

If a principal can forge a grant after the fact, the entire model collapses. An organization sued over an agent's action could simply mint a grant showing the action was outside scope — or inside it, whichever helps.

**Proposed answer: a transparency log.** Certificate Transparency's model — append-only, publicly verifiable, Merkle-structured. **A grant that is not logged is not valid.**

This kills backdating and provides **non-repudiation of time**, which is what a court actually needs.

### 4.2 Privacy (cuts directly against transparency)

An organization cannot publish every authority grant. Doing so leaks its org structure, its commercial posture, its risk appetite, and its internal limits.

**Proposed answer: log commitments, not contents.** Publish hashes to the transparency log; disclose the grant itself only to counterparties who need it; prove inclusion with Merkle paths.

**And for scope disclosure: selective disclosure.** A counterparty who only needs to know "this agent may commit up to $50,000" should not receive the entire grant. BBS+ / VC-style selective disclosure is materially better here than X.509's all-or-nothing certificate model.

**Design tension to record honestly:** X.509 has the more proven chain and revocation machinery; the Verifiable Credentials world has the better privacy cryptography. SDP likely needs elements of both, and should say so rather than pretending one stack is sufficient.

### 4.3 Revocation is prospective, not retroactive

**This must be stated explicitly in the spec, or readers will assume the opposite and conclude the model is unsound.**

If a principal revokes a grant today, decisions made yesterday under a then-valid grant **still stand**. The Decision Object captured validity at time T. Revocation changes what an agent may do *going forward*. It does not unwind history.

This is correct, it is consistent with how PKI revocation and recording systems work, and it is essential to the model's coherence — but it is counterintuitive enough that it needs saying.

---

## 5. What to borrow from where

| Source | What it contributes |
|---|---|
| **X.509 / PKI** | Chain construction, delegation, revocation and status-checking (OCSP), the proven machinery |
| **Certificate Transparency** | Append-only log, non-repudiation of time, defeat of backdating |
| **Verifiable Credentials (W3C)** | Selective disclosure, holder-presented credentials, no mandatory central IdP |
| **LEI / vLEI (GLEIF)** | Binding of legal entities and organizational roles — the trust root distribution problem |
| **SPKI / Macaroons / Biscuit** | Prior art on authorization-as-payload; instructive failures |

**What none of them provide, and what SDP adds:** the decision record, and the legal semantics that make the chain a liability chain.

---

## 6. Framing discipline (for the spec and for public writing)

**Do not claim the credential mechanics are novel.** They are not. Claiming a new credential scheme buries SDP in twenty-five years of prior art and invites a technical reviewer to dismiss it.

**Claim the unoccupied layer:** the decision record, the liability semantics, and the neutral cross-domain representation. The crowded credential field is then supporting cast, not competition — every scheme above becomes a signed *input* to an authority record.

They authenticate the actor. SDP represents the decision and locates the liability.
