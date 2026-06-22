"""Grounded AI query over the SDP ledger.

The model answers ONLY from the Decision Object records it is handed, and cites
the event seq numbers it relied on. It never narrates the audit from imagination
-- the whole value of an authority ledger is that answers trace to real records.

Requires the `anthropic` SDK and ANTHROPIC_API_KEY. Imported lazily so the rest
of the engine runs with zero external dependencies.
"""
from __future__ import annotations

import json
import os

from .ledger import Ledger

MODEL = os.environ.get("SDP_QUERY_MODEL", "claude-sonnet-4-6")

SYSTEM = (
    "You are an audit query engine for an agent-authority ledger. "
    "Answer ONLY from the Decision Object records provided in the user message. "
    "Cite the seq number of every event you rely on, like [seq 4]. "
    "If the records do not support an answer, say so plainly. "
    "Never invent events, principals, or grants."
)


def ask(question: str, ledger: Ledger) -> str:
    import anthropic  # lazy: engine runs without the SDK installed

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    records = ledger.events()
    prompt = (
        f"Authority ledger ({len(records)} events):\n"
        f"{json.dumps(records, indent=2)}\n\n"
        f"Question: {question}"
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    import sys

    L = Ledger()
    q = " ".join(sys.argv[1:]) or "Did any agent act outside its authority?"
    print(ask(q, L))
