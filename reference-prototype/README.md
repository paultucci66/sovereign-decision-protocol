# Sovereign Decision Protocol — Reference Prototype

> **Conformance: SDP-0008 Level 0 (Structural).** This prototype demonstrates the
> Decision Object model, the Five Proofs, the hash-chained ledger, and the
> check-before-act *pattern*. It is **not an enforcing deployment.** It is a peer
> MCP server an agent is invited to call; an agent holding its own credentials can
> act without ever consulting it. Enforcement — a `deny` that actually prevents
> execution — requires the **proxy position** described in SDP-0008 §3 (the SDP
> component sits between the agent and its tools, holds their credentials, and
> fails closed). That is Level 2 and is future work. Read the control-loop section
> below with that distinction in mind: this makes over-reach **visible and
> attributable**, not **prevented**.

A capture mechanism for the Decision Object. The schema was already defined; this
is the thing that **writes instances into it from live agent activity** and lets
you query the result.

Three parts:

1. **MCP server** — agents (Claude Code, Codex, etc.) point at it and emit /
   check authority. This is the **capture surface** and an **advisory
   check-before-act loop** — not an enforcement gate (see the banner above).
2. **Append-only, hash-chained ledger** — every event is immutable and carries
   the hash of the prior event. Tamper-evidence is what makes an Authority Record
   a *title instrument* instead of a log line.
3. **Grounded AI query** — ask the ledger questions; answers cite real event
   seq numbers and never invent records.

## The control loop (why this isn't just a logger — and what it still isn't)

The server is **bidirectional**, and that buys something real over a pure logger:

- **Read side / `check_authority`** answers the **MAY** proof *before* the agent
  acts. The question itself is recorded.
- **Write side / `record_decision`** records the **DID / SHOULD / LEARNED** and
  re-verifies authority at record time.

A pure logger reproduces *Distributed Innocence* — everyone acted, nobody
checked, the record only proves it after the harm. A check-before-act loop makes
an over-reach **visible and attributable at the moment it is attempted**.

Be precise about the limit. Visible and attributable is not the same as
prevented. Because this is a peer server the agent chooses to call, a compromised
or non-cooperating agent can skip the check and act on its own credentials. The
loop records honestly what was asked and done; it does not stand in the execution
path. Turning this from an advisory loop into an enforcing gate is the proxy-position
work in SDP-0008 §3, and it is the single most important step from Level 0 to
Level 2. Until then, the *control point* is a design target, not a property of
this artifact.

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
records an over-reach as unauthorized, and verifies the hash chain. Note the denial
is *recorded*, not *enforced* — the demo shows the agent's own restraint, not a gate
that stopped it.

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
rather than rebuilding identity. (Showable and honest: it demonstrates capture and
attribution, not enforcement — say so if asked.)

## Production note

Storage is SQLite for the prototype. The `Ledger` surface is intentionally small;
swapping to Postgres / Neon is a single-file change. Two things stand between this
and a conformant enforcing deployment: add a per-event signature (principal's key)
on top of the hash chain for third-party verifiability rather than just internal
tamper-evidence (toward SDP-0007), and move the check into the execution path via
the proxy position so `deny` fails closed (toward SDP-0008 Level 2).
