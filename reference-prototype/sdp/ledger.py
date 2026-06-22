"""Append-only, hash-chained ledger for the Sovereign Decision Protocol.

Design choices that matter:

  * Events are immutable. Current authority is a *projection* over events,
    never a mutable row. You don't edit a decision; you supersede it.
  * Each event carries the hash of the previous event -> a tamper-evident
    chain. This is what makes an Authority Record a *title instrument*
    rather than a log entry.
  * check_authority() records the question itself. Asking is on the record,
    so an action taken without a valid MAY is visible and attributable --
    the opposite of "Distributed Innocence."

Storage is SQLite for the prototype. The surface is small enough that swapping
in Postgres / Neon later is a single-file change (replace the Ledger backend).
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from typing import Any, Optional

from .proofs import CHECKED, DECIDED, GRANTED, REVOKED, new_id, now_iso

GENESIS = "0" * 64


def _canonical(obj: Any) -> str:
    """Deterministic JSON: sorted keys, no whitespace. Stable across reloads."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _hash(prev_hash: str, body: dict) -> str:
    return hashlib.sha256((prev_hash + _canonical(body)).encode()).hexdigest()


def _match(pattern: str, action: str) -> bool:
    """Exact match, or trailing-* wildcard prefix match.

    'review:contracts/*' matches 'review:contracts/NDA-2026'.
    """
    if pattern == action:
        return True
    if pattern.endswith("*") and action.startswith(pattern[:-1]):
        return True
    return False


class Ledger:
    def __init__(self, path: str = "sdp_ledger.db"):
        self.db = sqlite3.connect(path)
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                seq       INTEGER PRIMARY KEY AUTOINCREMENT,
                id        TEXT NOT NULL,
                type      TEXT NOT NULL,
                ts        TEXT NOT NULL,
                principal TEXT,
                agent     TEXT,
                payload   TEXT NOT NULL,
                prev_hash TEXT NOT NULL,
                hash      TEXT NOT NULL
            )
            """
        )
        self.db.commit()

    # ------------------------------------------------------------------ #
    # core append (the only writer)
    # ------------------------------------------------------------------ #
    def _append(self, type_: str, principal: Optional[str],
                agent: Optional[str], payload: dict) -> dict:
        prev = self.db.execute(
            "SELECT hash FROM events ORDER BY seq DESC LIMIT 1"
        ).fetchone()
        prev_hash = prev[0] if prev else GENESIS
        body = {
            "id": new_id("evt"),
            "type": type_,
            "ts": now_iso(),
            "principal": principal,
            "agent": agent,
            "payload": payload,
        }
        h = _hash(prev_hash, body)
        self.db.execute(
            "INSERT INTO events "
            "(id,type,ts,principal,agent,payload,prev_hash,hash) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (body["id"], type_, body["ts"], principal, agent,
             _canonical(payload), prev_hash, h),
        )
        self.db.commit()
        return {**body, "prev_hash": prev_hash, "hash": h}

    # ------------------------------------------------------------------ #
    # WHO + MAY : issue / revoke an Authority Record (the title instrument)
    # ------------------------------------------------------------------ #
    def grant_authority(self, principal: str, agent: str, scope: list[str],
                        constraints: Optional[dict] = None) -> dict:
        grant_id = new_id("grant")
        payload = {
            "grant_id": grant_id,
            "scope": scope,                    # list of action patterns
            "constraints": constraints or {},  # {"expires_at": ISO, "max_amount": n}
        }
        evt = self._append(GRANTED, principal, agent, payload)
        return {"grant_id": grant_id, "event": evt}

    def revoke_authority(self, principal: str, grant_id: str,
                        reason: str = "") -> dict:
        return self._append(REVOKED, principal, None,
                            {"grant_id": grant_id, "reason": reason})

    # ------------------------------------------------------------------ #
    # projection : active grants for an agent
    # ------------------------------------------------------------------ #
    def _active_grants(self, agent: str) -> list[dict]:
        revoked: set[str] = set()
        for row in self.db.execute(
            "SELECT payload FROM events WHERE type=? ORDER BY seq", (REVOKED,)
        ):
            revoked.add(json.loads(row[0])["grant_id"])

        grants: dict[str, dict] = {}
        for row in self.db.execute(
            "SELECT principal,agent,payload FROM events WHERE type=? ORDER BY seq",
            (GRANTED,),
        ):
            p, a, payload = row[0], row[1], json.loads(row[2])
            if a == agent and payload["grant_id"] not in revoked:
                grants[payload["grant_id"]] = {"principal": p, "agent": a, **payload}
        return list(grants.values())

    @staticmethod
    def _constraints_ok(constraints: dict, context: dict) -> tuple[bool, str]:
        exp = constraints.get("expires_at")
        if exp and now_iso() > exp:
            return False, "grant expired"
        cap = constraints.get("max_amount")
        if cap is not None and context.get("amount", 0) > cap:
            return False, f"amount {context.get('amount')} exceeds cap {cap}"
        return True, "within constraints"

    # ------------------------------------------------------------------ #
    # MAY at decision time : THE control point
    # ------------------------------------------------------------------ #
    def check_authority(self, agent: str, action: str,
                        context: Optional[dict] = None) -> dict:
        context = context or {}
        decision = {"authorized": False, "grant_id": None,
                    "reason": "no grant covers this action"}
        principal = None
        for g in self._active_grants(agent):
            if not any(_match(p, action) for p in g["scope"]):
                continue
            ok, why = self._constraints_ok(g["constraints"], context)
            if not ok:
                decision = {"authorized": False, "grant_id": g["grant_id"],
                            "reason": why}
                principal = g["principal"]
                continue
            decision = {"authorized": True, "grant_id": g["grant_id"],
                        "reason": "within granted scope"}
            principal = g["principal"]
            break
        # the question itself goes on the record -- this is the key move
        self._append(CHECKED, principal, agent,
                     {"action": action, "context": context, "result": decision})
        return decision

    # ------------------------------------------------------------------ #
    # DID + SHOULD + LEARNED : record what the agent actually did
    # ------------------------------------------------------------------ #
    def record_decision(self, principal: str, agent: str, action: str,
                        grant_id: Optional[str] = None,
                        policy_basis: Optional[str] = None,
                        outcome: Optional[str] = None,
                        context: Optional[dict] = None) -> dict:
        # re-verify authority at record time; the check is itself recorded
        authz = self.check_authority(agent, action, context or {})
        decision_object = {
            "decision_id": new_id("do"),
            "who": principal,                          # WHO
            "may": grant_id or authz["grant_id"],      # MAY
            "should": policy_basis,                    # SHOULD
            "did": {"action": action, "context": context or {}},  # DID
            "learned": outcome,                        # LEARNED
            "authorized_at_record_time": authz["authorized"],
            "authority_reason": authz["reason"],
        }
        evt = self._append(DECIDED, principal, agent, decision_object)
        return {"decision": decision_object, "event": evt}

    # ------------------------------------------------------------------ #
    # read side
    # ------------------------------------------------------------------ #
    def events(self, types: Optional[list[str]] = None,
               agent: Optional[str] = None) -> list[dict]:
        q = ("SELECT seq,id,type,ts,principal,agent,payload,prev_hash,hash "
             "FROM events")
        clauses, args = [], []
        if types:
            clauses.append("type IN (%s)" % ",".join("?" * len(types)))
            args += list(types)
        if agent:
            clauses.append("agent = ?")
            args.append(agent)
        if clauses:
            q += " WHERE " + " AND ".join(clauses)
        q += " ORDER BY seq"
        out = []
        for r in self.db.execute(q, args):
            out.append({
                "seq": r[0], "id": r[1], "type": r[2], "ts": r[3],
                "principal": r[4], "agent": r[5], "payload": json.loads(r[6]),
                "prev_hash": r[7], "hash": r[8],
            })
        return out

    def authority_record(self, grant_id: str) -> Optional[dict]:
        for e in self.events(types=[GRANTED]):
            if e["payload"]["grant_id"] == grant_id:
                return e
        return None

    def count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    # ------------------------------------------------------------------ #
    # integrity : verify the tamper-evident chain
    # ------------------------------------------------------------------ #
    def verify(self) -> dict:
        prev_hash = GENESIS
        for e in self.events():
            body = {"id": e["id"], "type": e["type"], "ts": e["ts"],
                    "principal": e["principal"], "agent": e["agent"],
                    "payload": e["payload"]}
            if _hash(prev_hash, body) != e["hash"] or e["prev_hash"] != prev_hash:
                return {"ok": False, "broken_at_seq": e["seq"]}
            prev_hash = e["hash"]
        return {"ok": True, "events": self.count()}
