# Sovereign Decision Protocol — Reference Prototype

A capture mechanism for the Decision Object. The schema was already defined; this
is the thing that **writes instances into it from live agent activity** and lets
you query the result.

Three parts:

1. **MCP server** — agents (Claude Code, Codex, etc.) point at it and emit /
   check authority. This is both the capture surface and the control point.
2. **Append-only, hash-chained ledger** — every event is immutable and carries
   the hash of the prior event. Tamper-evidence is what makes an Authority Record
   a *title instrument* instead of a log line.
3. **Grounded AI query** — ask the ledger questions; answers cite real event
   seq numbers and never invent records.

## The control loop (why this isn't just a logger)

The server is **bidirectional**, and that is the whole point:

- **Read side / `check_authority`** answers the **MAY** proof *before* the agent
  acts. The question itself is recorded.
- **Write side / `record_decision`** records the **DID / SHOULD / LEARNED** and
  re-verifies authority at record time.

A pure logger reproduces *Distributed Innocence* — everyone acted, nobody
checked, the record only proves it after the harm. A check-before-act loop makes
an over-reach **visible and attributable at the moment it is attempted**. That is
the missing control element.

## Five Proofs → ledger

| Proof   | Meaning                                  | Where it lives                     |
|---------|------------------------------------------|------------------------------------|
| WHO     | human principal the agent is bound to    | `principal` on every event         |
| MAY     | authority that permits the action        | `authority.granted` + `check`      |
| SHOULD  | policy / governance basis invoked        | `should` on the Decision Object    |
| DID     | the action actually taken                | `did` on the Decision Object       |
| LEARNED | the outcome observed                     | `learned` on the Decision Object   |

## Run it

```bash
pip install -r requirements.txt          # only needed for the MCP server + AI query

python demo.py                           # full control loop, zero deps, no API key
```

`demo.py` issues a grant, authorizes a legitimate review, denies a sign-attempt,
records an over-reach as unauthorized, and verifies the hash chain.

```bash
python demo_multiagent.py                # two agents, two principals, one ledger
```

`demo_multiagent.py` is the Interlateral picture: a reviewer agent bound to the
client and a signer agent bound to outside counsel share one ledger. Authority
stays partitioned across organizational walls, a **Trust Handoff** lets the signer
verify the reviewer's work on the shared record before acting, and a cross-agent
over-reach is denied and recorded. Every action stays attributable to its
principal.

### As an MCP server (point an agent at it)

```bash
python -m sdp.server                     # stdio transport
```

Tools exposed: `grant_authority`, `check_authority`, `record_decision`,
`revoke_authority`, `get_authority_record`, `list_ledger`, `verify_chain`.

### Grounded AI query

```bash
export ANTHROPIC_API_KEY=...
python -m sdp.query "Did any agent act outside its authority?"
```

## For AgentWeek

This is the showable artifact. In a shared Interlateral space, any participant's
agent can point at the server and the room gets a **live, queryable authority
ledger** of everything the agents did — a working instance of "visible delegated
agency." Lean on Interlateral's attested-principal binding for the WHO proof
rather than rebuilding identity.

## Production note

Storage is SQLite for the prototype. The `Ledger` surface is intentionally small;
swapping to Postgres / Neon is a single-file change. Add a per-event signature
(principal's key) on top of the hash chain when you need third-party
verifiability rather than just internal tamper-evidence.
