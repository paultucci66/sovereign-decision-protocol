"""Two agents, two principals, one shared ledger — the Interlateral picture.

Agent A (reviewer) is bound to the CLIENT principal and may REVIEW contracts.
Agent B (signer)   is bound to OUTSIDE COUNSEL and may EXECUTE them.

Authority is partitioned across organizational walls; the shared ledger makes the
whole handoff attributable. We show:

  * each agent acting only within its own principal's grant
  * a Trust Handoff: B confirms A's review on the shared record before signing
  * a cross-agent over-reach (A tries to sign) denied and recorded
  * the chain verifying across both agents' activity

Run:  python demo_multiagent.py
"""
import os

from sdp.ledger import Ledger
from sdp.proofs import DECIDED

DB = "sdp_multiagent.db"


def authorized_review_seq(ledger: Ledger, contract: str):
    """Return the seq of an authorized review for `contract`, if one exists."""
    for e in ledger.events(types=[DECIDED]):
        do = e["payload"]
        action = do["did"]["action"]
        if (action.startswith("review:") and contract in action
                and do["authorized_at_record_time"]):
            return e["seq"]
    return None


def main():
    if os.path.exists(DB):
        os.remove(DB)
    L = Ledger(DB)

    CLIENT = "did:paul-tucci"
    COUNSEL = "did:outside-counsel"
    A = "agent:reviewer"   # bound to the client
    B = "agent:signer"     # bound to outside counsel
    CONTRACT = "contracts/NDA-2026"

    print("\n1) Two principals issue PARTITIONED authority on one SHARED ledger")
    L.grant_authority(CLIENT, A, scope=["review:contracts/*", "flag:risk"])
    L.grant_authority(COUNSEL, B, scope=["execute:contracts/*"])
    print(f"   {CLIENT:<22} -> {A:<16}: review")
    print(f"   {COUNSEL:<22} -> {B:<16}: execute")

    print("\n2) Agent A (client) reviews — inside its own grant")
    L.record_decision(
        CLIENT, A, f"review:{CONTRACT}",
        policy_basis="policy:contract-review-v1",
        outcome="2 risk clauses flagged; cleared to sign",
    )
    print("   review recorded")

    print("\n3) Trust Handoff — Agent B checks the SHARED record before signing")
    seq = authorized_review_seq(L, CONTRACT)
    if seq:
        print(f"   B sees A's authorized review at [seq {seq}] — handoff valid")
        chk = L.check_authority(B, f"execute:{CONTRACT}")
        print(f"   B check execute -> {chk['authorized']}  ({chk['reason']})")
        L.record_decision(
            COUNSEL, B, f"execute:{CONTRACT}",
            grant_id=chk["grant_id"],
            policy_basis=f"handoff: relies on review [seq {seq}]",
            outcome="NDA executed",
        )
        print("   execute recorded — chain attributable across BOTH orgs")
    else:
        print("   no authorized review on record — B must not sign")

    print("\n4) Cross-agent over-reach — Agent A (client) tries to SIGN")
    d = L.record_decision(
        CLIENT, A, f"execute:{CONTRACT}", outcome="attempted to self-sign"
    )
    print(f"   A execute -> authorized={d['decision']['authorized_at_record_time']}  "
          f"({d['decision']['authority_reason']})")

    print("\n5) Verify the shared chain")
    print(f"   {L.verify()}")

    print("\n6) Shared ledger — both principals, both agents, one record:")
    for e in L.events():
        print(f"   [seq {e['seq']}] {e['type']:<20} {(e['agent'] or '-'):<18} "
              f"who={e['principal'] or '-'}")

    print("\n   Two organizations' agents, one attributable record. Authority")
    print("   stayed partitioned; the over-reach is on the record. That is")
    print("   visible delegated agency across organizational walls.\n")


if __name__ == "__main__":
    main()
