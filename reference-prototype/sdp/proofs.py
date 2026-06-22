"""Five Proofs vocabulary for the Sovereign Decision Protocol prototype.

Every consequential agent action is anchored by five proofs:

  WHO     - the human principal the agent is bound to
  MAY     - the authority (grant) that permits the action
  SHOULD  - the policy / governance basis invoked
  DID     - the action actually taken
  LEARNED - the outcome / what was observed

The ledger stores these as append-only, hash-chained events.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# Ledger event types
GRANTED = "authority.granted"   # WHO + MAY  : an Authority Record is issued
REVOKED = "authority.revoked"   # MAY pulled : a grant is withdrawn
CHECKED = "authority.checked"   # MAY tested : "may I?" asked before acting
DECIDED = "decision.recorded"   # DID + SHOULD + LEARNED : what the agent did
