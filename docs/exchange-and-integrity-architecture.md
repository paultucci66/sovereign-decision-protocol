# Design Note: Exchange, Integrity, and the Bilateral Record

**Status:** Working note. Input to SDP-0006 (Exchange Format) and SDP-0007 (Cryptographic Integrity), neither yet drafted.  
**Date:** July 2026  
**Author:** Paul Tucci

---

## Purpose

This note records two related architectural findings:

1. **The exchange of Decision Objects between two parties is itself the evidentiary event.** It supplies the manifestation of assent and — more importantly — the attribution that US statute already requires for machine-formed contracts.
2. **Immutability does not require a blockchain.** It requires a ledger discipline, and an integrity anchor that the record-holder does not control. For bilateral decisions, the counterparty *is* the anchor.

---

## 1. The Bilateral Exchange

### Structure

Two objects, cryptographically linked. Not two independent records passing each other.

**Party A's Decision Object:**
- Agent identity
- Stapled authority chain (valid at time T)
- Terms offered
- Signature

**Party B's Decision Object:**
- Agent identity
- Stapled authority chain (valid at time T)
- **Hash reference to A's object**
- Acceptance
- Signature

**The hash reference is the acceptance.** Offer and acceptance, cryptographically linked, each carrying proof that its agent was authorized to make it.

### What the exchange establishes

Be precise here. The exchange does **not** by itself create a contract — consideration, definiteness, and legality live in the payload and in the underlying deal. What it supplies is exactly the two things that were in doubt for machine-formed agreements:

**Manifestation of mutual assent.** Restatement (Second) of Contracts § 17 requires a *manifestation*, not a subjective meeting of minds. A signed, exchanged Decision Object carrying a verified authority chain is a manifestation — and a stronger one than a click, a wet signature, or an email, because none of those prove the signer's authority.

**Attribution under E-SIGN § 7001(h).** This is the load-bearing part. The statute conditions the validity of an agent-formed contract on the agent's action being *legally attributable to the person to be bound.* An exchanged Decision Object carries the authority chain from the acting agent up to the legal person, stapled and provably valid at the moment of the act.

**Attribution therefore stops being something litigated afterward. It is answered in the artifact, at formation.**

### Constructive notice falls out of the mechanism

Because B could have verified A's authority scope *before* accepting, B had the means of knowing the boundary.

If A's agent exceeded its recorded scope and B accepted anyway, B was not reasonably relying on anything. The apparent-authority claim collapses — not because A disclaimed it, but because B declined to look.

This is the constructive-notice argument of Agentic Law II § 11, arriving as a mechanism rather than a legal theory. Recording systems defeat the claim of innocent reliance. The exchange *is* the recording event, as between the two parties.

### What each party walks away holding

- What was offered
- What was accepted
- That both agents were authorized to make those manifestations
- When it happened

Verifiable without either party's cooperation. Indefinitely.

**This is stronger than a signed paper contract. A paper contract does not prove the signer had authority to sign it.**

---

## 2. The Precedent: Carrier Interconnect Settlement

This mechanism is not novel. It is the settlement architecture of telecom, and the author operated it for twenty-five years.

Two carriers exchange Call Detail Records. Each holds its own record of the call. Neither can unilaterally rewrite it, because the other side holds a matching record. Disputes resolve by comparing the two. **The exchange of records is the settlement mechanism.** No trusted third party sits in the middle.

Two organizations exchange Decision Objects. Each holds its own record of what was agreed. Neither can unilaterally rewrite it. Disputes resolve by comparing the two.

**Same mechanism. Same structure. Different record.**

The Decision Object is the CDR of the agentic economy, and the exchange is the interconnect.

### The gap EDI left open

Exchanged machine records forming binding contracts is not a stretch of UETA — **UETA was written for EDI.** Trading-partner agreements have worked this way for decades. This is the case the statute was drafted to cover.

What EDI never had was the **authority chain**. EDI proved the message came from the trading partner's system. It never proved that the system was authorized to commit the trading partner to that obligation.

That is the gap SDP fills.

---

## 3. Immutability: It Is a Ledger, Not a Blockchain

Decision Objects are never edited and never deleted. A decision is revised by **superseding** it — issuing a new object that references the prior one. The prior object remains.

The correct mental model is not distributed ledger technology. It is **double-entry bookkeeping**, which has worked for five centuries and which courts already trust.

You do not erase a posted journal entry. You post a correcting entry. The audit trail *is* the sequence of entries.

**The decision ledger is a general ledger.** Append-only, supersession by reference, no deletion.

### Why a *local* blockchain fails

A hash chain held entirely by one organization provides **detection of tampering only if some other party holds an independent copy of a later hash.**

If a single organization holds the entire chain and every hash in it, that organization can recompute the chain from any point. Nothing prevents it.

And in litigation, **that organization is the defendant.** The plaintiff's allegation is precisely that the records were altered or backdated. A chain the defendant built, holds, and could regenerate proves nothing to a court.

A private blockchain solves the **insider** problem: a rogue employee cannot quietly alter one record without breaking the chain. That is genuinely useful.

It does not solve the **institutional** problem, which is the one that matters in a dispute.

---

## 4. Local Ledger, Public Anchor

Keep the local hash chain — it is cheap and gives internal integrity. Then **periodically publish the Merkle root somewhere the organization cannot rewrite.**

That is anchoring, and it is the entire mechanism.

**Batching is what makes it economically viable.** One anchor per hour covers millions of decisions. Cost does not scale with decision volume — which is essential, given that SDP-based products are expected to meter at sub-penny per decision. Writing each decision individually to a public chain is economically absurd at that volume. Anchoring is nearly free.

### Anchor targets, in rough order of legal defensibility

| Target | Notes |
|---|---|
| **RFC 3161 timestamping authority** | Legally recognized. Qualified timestamps under eIDAS carry a presumption of accuracy in the EU. A court knows what to do with this. |
| **Transparency log** (Certificate Transparency model) | Append-only, independently monitored, inclusion and consistency proofs. Proven at internet scale. |
| **Public chain via OpenTimestamps** | The legitimate use of a blockchain here: as a **notary**, not a database. |
| **The counterparty** | See below — the elegant case. |

### The counterparty is the anchor

For a **bilateral** decision, no external anchor is required.

Both parties hold a signed co-original. Neither can unilaterally alter it, because the other side holds the matching copy. Mutual signature plus dual custody yields non-repudiation for free.

**Anchoring is only necessary for *unilateral* decisions** — internal decisions with no counterparty to serve as witness.

This also gives the co-original principle a second justification. It is not only a rights argument (the party whose judgment produced the decision is entitled to hold the record). It is the **integrity mechanism**.

---

## 5. Privacy: Never Put the Payload in the Immutable Structure

**This is the failure mode that would be fatal, and it must be designed against explicitly.**

Consequential decisions — lending, hiring, customer actions — contain personal data. An immutable structure containing personal data **cannot comply with GDPR Article 17 or CCPA deletion rights.** It would be a system structurally incapable of erasure, built that way on purpose.

### SDP already solved this

**Design Axiom 5: context is referenced, not embedded.**

That axiom is what makes erasure possible. Only hashes and verifiable references enter the immutable structure. The payload lives in ordinary storage, where it can be deleted.

**Axiom 5 is not a storage optimization. It is the privacy architecture.** The spec should say so explicitly.

### Crypto-shredding for the payload

Encrypt the payload, store the ciphertext, and satisfy an erasure request by **destroying the key**. The ledger entry persists structurally; the content becomes unrecoverable.

The record still proves *that* a decision was made, under a given authority, at a given time — which is what the legal record requires — without retaining data the organization is obligated to delete.

---

## 6. Courts Already Have the Admissibility Mechanism

**Federal Rules of Evidence 902(13) and 902(14)**, effective December 1, 2017.

- **902(13)** permits self-authentication of *"a record generated by an electronic process or system that produces an accurate result,"* on certification by a qualified person. A Decision Object is precisely such a record.
- **902(14)** permits self-authentication of data *"authenticated by a process of digital identification."* The Advisory Committee Note explicitly names **hash values** as that process.

These rules eliminate the need for a foundation witness. A hash-authenticated Decision Object fits the existing rule as written.

**This is a significant advantage over a blockchain-based story**, because it requires no judicial familiarity with distributed ledgers. The mechanism is already in the rules.

### State the limits honestly

- Both rules require a **certification by a qualified person**. Self-authentication is not automatic.
- Self-authentication addresses **authenticity only**. Hearsay and other grounds for exclusion still apply.
- Commentators note that most parties will not themselves meet the "qualified person" standard.

Do not overclaim this. It removes one obstacle. It does not make a Decision Object automatically admissible.

---

## 7. Honest Limits

**Both sides must implement.** The bilateral exchange requires the counterparty to speak SDP. This is the classic protocol chicken-and-egg. It was true of TCP/IP as well, but it should not be papered over.

**Compromise is not cured.** If a party's agent was prompt-injected, or its signing key stolen, the exchange does not fix that. What it does is establish that the grant was valid and that the agent acted within recorded scope — which shifts the burden to the party *claiming* compromise to prove it. That is the correct allocation of the burden, and it is all that should be claimed.

**Not every exchange is a contract.** Two agents may exchange Decision Objects for notification, filing, or coordination with no agreement intended. The exchange proves manifestation. It does not manufacture agreement where none was offered.

**Anchoring introduces an external dependency.** For unilateral decisions, the integrity guarantee is only as good as the anchor. A timestamping authority can fail; a transparency log can be abandoned. The design should permit multiple simultaneous anchors.

---

## Summary

**Local ledger. Public anchor. Bilateral exchange where a counterparty exists.**

The organization's decisions remain in its own control — its data, its jurisdiction, its storage. Only proof-of-existence leaves the boundary. The organization publishes *that* a decision existed at a moment in time, and nothing about what it said.

That is decision sovereignty, expressed as an architecture.
