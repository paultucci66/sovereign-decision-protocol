"""End-to-end demo of the SDP control loop. No MCP client or API key required.

Scenario
--------
A contract-review agent is bound to principal "Paul Tucci" and granted authority
to REVIEW contracts and FLAG risk -- but NOT to execute / sign them. We watch the
control loop:

  * authorize a legitimate action (review)
  * deny an over-reach (execute/sign) BEFORE it happens
  * make an unauthorized attempt visible and attributable on the record
  * prove the whole ledger is tamper-evident

Run:  python demo.py
"""
import os

from sdp.ledger import Ledger

DB = "sdp_ledger.db"


def main():
    if os.path.exists(DB):
        os.remove(DB)
    L = Ledger(DB)

    PRINCIPAL = "did:paul-tucci"
    AGENT = "agent:contract-reviewer"

    print("\n1) Issue an Authority Record  (WHO + MAY)")
    g = L.grant_authority(
        PRINCIPAL, AGENT,
        scope=["review:contracts/*", "flag:risk"],
        constraints={"max_amount": 100000},
    )
    grant_id = g["grant_id"]
    print(f"   {grant_id}  ->  scope: review:contracts/*, flag:risk")

    print("\n2) Agent checks authority BEFORE acting  (the control point)")
    a1 = L.check_authority(AGENT, "review:contracts/NDA-2026", {"amount": 0})
    print(f"   review:contracts/NDA-2026   -> {a1['authorized']}  ({a1['reason']})")
    a2 = L.check_authority(AGENT, "execute:contracts/NDA-2026")
    print(f"   execute:contracts/NDA-2026  -> {a2['authorized']}  ({a2['reason']})")

    print("\n3) Agent records the authorized decision  (DID + SHOULD + LEARNED)")
    d = L.record_decision(
        PRINCIPAL, AGENT, "review:contracts/NDA-2026",
        grant_id=grant_id,
        policy_basis="policy:contract-review-v1",
        outcome="2 risk clauses flagged; no authority to sign",
        context={"amount": 0},
    )
    print(f"   {d['decision']['decision_id']}  "
          f"authorized={d['decision']['authorized_at_record_time']}")

    print("\n4) Agent attempts an action it was NEVER authorized for")
    d2 = L.record_decision(
        PRINCIPAL, AGENT, "execute:contracts/NDA-2026",
        policy_basis="(none cited)",
        outcome="attempted to sign the NDA",
    )
    print(f"   {d2['decision']['decision_id']}  "
          f"authorized={d2['decision']['authorized_at_record_time']}  "
          f"reason={d2['decision']['authority_reason']}")

    print("\n5) Verify the tamper-evident chain")
    print(f"   {L.verify()}")

    print("\n6) The ledger -- every WHO / MAY / CHECK / DID on the record:")
    for e in L.events():
        who = e["principal"] or "-"
        print(f"   [seq {e['seq']}] {e['type']:<20} agent={e['agent']}  who={who}")

    print("\n   The over-reach at step 4 is on the record as UNAUTHORIZED --")
    print("   visible and attributable. That is the missing control element.\n")


if __name__ == "__main__":
    main()
