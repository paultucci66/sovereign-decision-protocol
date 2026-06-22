"""MCP server exposing the Sovereign Decision Protocol control loop.

Point any MCP-capable agent (Claude Code, Codex, etc.) at this server.

  Agent-facing:
    check_authority   -- ask "may I?" BEFORE acting (the control point)
    record_decision   -- record what it did, anchored to its authority

  Operator-facing:
    grant_authority   -- issue an Authority Record (the title instrument)
    revoke_authority  -- pull a grant

  Read / audit:
    get_authority_record, list_ledger, verify_chain

Run:  python -m sdp.server     (stdio transport, the default MCP client expects)
"""
from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from .ledger import Ledger

ledger = Ledger()
mcp = FastMCP("sovereign-decision-protocol")


@mcp.tool()
def grant_authority(principal: str, agent: str, scope: list[str],
                    constraints: Optional[dict] = None) -> dict:
    """Issue an Authority Record (MAY) binding an agent to a human principal (WHO).

    scope: list of action patterns, e.g. ["review:contracts/*", "flag:risk"].
    constraints: optional, e.g. {"expires_at": "2026-12-31T00:00:00+00:00",
    "max_amount": 100000}.
    """
    return ledger.grant_authority(principal, agent, scope, constraints)


@mcp.tool()
def check_authority(agent: str, action: str,
                    context: Optional[dict] = None) -> dict:
    """The control point. Ask whether `agent` MAY take `action` before doing it.

    Returns {authorized, grant_id, reason}. The question is recorded either way,
    so an action later taken without a valid MAY is visible and attributable.
    """
    return ledger.check_authority(agent, action, context or {})


@mcp.tool()
def record_decision(principal: str, agent: str, action: str,
                    grant_id: Optional[str] = None,
                    policy_basis: Optional[str] = None,
                    outcome: Optional[str] = None,
                    context: Optional[dict] = None) -> dict:
    """Record a Decision Object (DID + SHOULD + LEARNED).

    Authority is re-verified at record time. Actions without a valid MAY are
    still recorded -- flagged as unauthorized rather than silently dropped.
    """
    return ledger.record_decision(principal, agent, action, grant_id,
                                  policy_basis, outcome, context)


@mcp.tool()
def revoke_authority(principal: str, grant_id: str, reason: str = "") -> dict:
    """Revoke a previously issued Authority Record."""
    return ledger.revoke_authority(principal, grant_id, reason)


@mcp.tool()
def get_authority_record(grant_id: str) -> Optional[dict]:
    """Fetch a single Authority Record (the title instrument) by id."""
    return ledger.authority_record(grant_id)


@mcp.tool()
def list_ledger(agent: Optional[str] = None) -> list[dict]:
    """Return the append-only ledger, optionally filtered to one agent."""
    return ledger.events(agent=agent)


@mcp.tool()
def verify_chain() -> dict:
    """Verify the tamper-evident hash chain over the entire ledger."""
    return ledger.verify()


if __name__ == "__main__":
    mcp.run()
