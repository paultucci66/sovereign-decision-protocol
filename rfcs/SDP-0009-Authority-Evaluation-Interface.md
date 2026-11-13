# SDP-0009: Authority Evaluation Interface

Status: Draft

Version: 0.1

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC defines the Authority Evaluation Interface: the call an enforcement point makes, before a consequential action executes, to ask whether an actor may take that action under its current authority, and the response that call returns. It also defines the outcome report that closes the loop after execution.

The interface is specified as a profile of the OpenID AuthZEN Authorization API 1.0. An implementation that already speaks AuthZEN can adopt this profile by adding the SDP members defined here; it does not need a second wire protocol.

AuthZEN answers *may this subject perform this action on this resource*. This profile adds what SDP requires on top of that answer: a Decision Object identifier issued for every evaluation, the authority snapshot the verdict was computed against, the constraints the caller must honor, a verdict set that includes escalation and simulation, and a mandatory report of what actually happened.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are used as defined in RFC 2119.

## 1. Purpose

SDP-0008 §3 requires a Level 2 (Enforcing-Deployment) implementation to place the authority check in the execution path, in the proxy position, failing closed. It does not say what that check looks like on the wire. Without a common interface, every enforcement point is bound to one evaluator, and conformance cannot be tested across vendors.

### 1.1 Why this belongs in the protocol

SDP-0001 §4 excludes policy engines and control-plane orchestration from the protocol. This RFC does not specify either. It specifies only the exchange between two independent systems: the component that holds the credentials and gates execution, and the component that evaluates authority. Applying the RFC index Design Test:

- **Required for two independent systems to exchange a consequential decision?** Yes. The enforcement point (a gateway, workflow engine, SOAR platform, MCP server, payment rail) and the evaluator are routinely built by different parties.
- **Protocol or product?** The request and response shapes are protocol. How the evaluator reaches its verdict, scores materiality, stores records, or presents them to humans is product.
- **Will this still matter in ten years?** The enforcement-point/decision-point split has been stable since XACML. What is new is that the actor is increasingly an AI agent and the record must survive scrutiny.

## 2. Terminology

**Enforcement Point (EP).** The component that sits between an actor and the executing tools, holds or mediates the credentials those tools require, and permits or blocks execution. Corresponds to the AuthZEN Policy Enforcement Point (PEP).

**Authority Evaluator (AE).** The component that evaluates a proposed act against Authority Records (SDP-0003) and returns a verdict. Corresponds to the AuthZEN Policy Decision Point (PDP). A Decision Control Plane typically contains an AE; this RFC does not require that it does.

**Evaluation.** One request/response exchange for one proposed act.

**Authorized Decision Reference.** The `decision_id` from a `permit` response, presented by the EP to the executing tool or recorded alongside the execution. This is the reference SDP-0008 §3 requires before a consequential action proceeds.

**Act.** The tuple of subject, action, and resource (with the SDP members of each) that an evaluation is about.

**Act Digest.** A hash over the canonical form of the act (§6.6), binding a verdict to exactly the act evaluated.

## 3. Relationship to AuthZEN

This RFC is a profile of the AuthZEN Authorization API 1.0 (OpenID Final Specification, January 2026).

1. Requests and responses MUST be valid AuthZEN Access Evaluation requests and responses.
2. All SDP-specific members are carried in a single `sdp` object inside the `properties` of `subject`, `action`, and `resource`, and inside the request and response `context`. Implementations MUST NOT place SDP members elsewhere.
3. The AuthZEN `decision` boolean MUST be `true` if and only if the SDP verdict is `permit`. Every other verdict MUST produce `decision: false`. An AuthZEN-only client that ignores the `sdp` members therefore fails closed by construction.
4. An AE conforming to this profile MUST also be a conforming AuthZEN PDP for the evaluation endpoint.

AuthZEN working-group drafts for obligations and for access-request-and-approval address adjacent needs (§5.4 and §5.2 respectively). This profile defines its own members for those needs so that it does not depend on non-final drafts. Alignment with those profiles once final is an open question (§12).

## 4. Evaluation Request

### 4.1 Structure

```json
{
  "subject": {
    "type": "agent",
    "id": "agt_01HZX4Q8",
    "properties": {
      "sdp": {
        "principal_assertion": "<signed assertion; profile per SDP-0004 / SDP-0007>",
        "acting_for": "prn_01HZW9TT"
      }
    }
  },
  "action": {
    "name": "isolate_host",
    "properties": {
      "sdp": {
        "effect_category": "operational.containment",
        "codes": [
          { "system": "UNSPSC", "version": "v26.0801", "code": "81111800" }
        ],
        "amount": null
      }
    }
  },
  "resource": {
    "type": "endpoint",
    "id": "host-4471",
    "properties": {
      "sdp": { "owner": "org_acme", "jurisdiction": "US-SC" }
    }
  },
  "context": {
    "sdp": {
      "profile": "SDP-0009/0.1",
      "mode": "evaluate",
      "request_id": "req_7F3K2",
      "idempotency_key": "soc-playbook-88:run-2291:step-4",
      "requested_at": "2026-11-13T20:14:05Z",
      "parent_decision_id": "dec_01HZX4M2",
      "authority_hint": "auth_01HZV0AA",
      "materiality": {
        "hard_to_undo": false,
        "leaves_org": false,
        "changes_legal_or_financial_position": false
      }
    }
  }
}
```

### 4.2 Required and optional members

The request `context.sdp` object:

- `profile` — MUST be present; the profile identifier and version.
- `mode` — MUST be `evaluate` or `simulate` (§5.3).
- `request_id` — MUST be present; unique per transmission.
- `idempotency_key` — MUST be present; stable across retries of the same intended act (§6.4).
- `requested_at` — MUST be present; the EP's timestamp for the proposed act.
- `parent_decision_id` — MUST be present when the act is performed under a parent decision's envelope (§8).
- `authority_hint` — MAY identify the Authority Record the EP believes applies. The AE MUST NOT treat the hint as establishing authority; it MUST resolve authority independently.
- `materiality` — MAY carry the EP's materiality signals. The AE MAY use or override them; how materiality affects a verdict is implementation-defined.

The `subject.properties.sdp` object MUST carry `principal_assertion`. `acting_for` MUST be present when the subject acts on behalf of another principal.

The `action.properties.sdp` object SHOULD carry `effect_category` (SDP-0002 Annex A) and MUST carry every value a Class A constraint in the applicable grant needs in order to be evaluated deterministically: codes pinned to a code-system version per SDP-0003 §5, monetary `amount` with ISO 4217 currency, counterparty identifiers, and so on. An act missing a value that a Class A constraint requires MUST NOT receive `permit` (§6.1).

Monetary amounts MUST be encoded as decimal strings, not floating-point numbers.

## 5. Evaluation Response

### 5.1 Structure

```json
{
  "decision": false,
  "context": {
    "sdp": {
      "profile": "SDP-0009/0.1",
      "verdict": "escalate",
      "decision_id": "dec_01HZX4R9",
      "request_id": "req_7F3K2",
      "act_digest": "sha256:9c1e...",
      "evaluated_at": "2026-11-13T20:14:05.412Z",
      "authority_snapshot": {
        "authority_id": "auth_01HZV0AA",
        "valid_time": "2026-11-13T20:14:05Z",
        "recorded_time": "2026-11-13T20:14:05.401Z",
        "digest": "sha256:44ab..."
      },
      "constraints": [
        { "constraint_id": "c-01", "class": "A", "result": "satisfied" },
        { "constraint_id": "c-07", "class": "C", "result": "requires_human" }
      ],
      "obligations": [],
      "valid_until": null,
      "evidence_required": [],
      "escalation": {
        "reason": "class_c_constraint",
        "route": "approver:role/soc-lead",
        "approval_decision_id": null
      },
      "reasons": [
        { "code": "requires_human_disposition", "constraint_id": "c-07" }
      ]
    }
  }
}
```

### 5.2 Verdicts

`verdict` MUST be one of:

- **`permit`** — The act is authorized as evaluated. `decision` is `true`. The response MUST carry `valid_until` and MAY carry `obligations` and `evidence_required`.
- **`deny`** — The act is not authorized. The EP MUST NOT execute it.
- **`escalate`** — The act cannot be decided at machine speed: a Class B constraint returned below threshold, a Class C constraint applies, or the AE's policy requires human approval. The response MUST carry `escalation.route`. The human ruling is itself a recorded decision (SDP-0003 §3.3). Once that ruling exists, the EP obtains a `permit` or `deny` by re-evaluating with the same `idempotency_key`; the resulting response MUST reference the ruling in `escalation.approval_decision_id`.
- **`simulate_required`** — The AE requires a simulation of the act (§5.3) before it will issue a verdict. The EP SHOULD submit a `simulate` request and then re-evaluate.

An EP that receives a verdict it does not recognize MUST treat it as `deny`.

### 5.3 Simulation

A request with `mode: "simulate"` asks what the verdict would be without authorizing anything. The AE MUST evaluate it exactly as an `evaluate` request and MUST record the result, but:

1. `decision` MUST be `false` regardless of the would-be verdict.
2. The would-be verdict is returned in `context.sdp.simulated_verdict`; `verdict` MUST be `simulated`.
3. The issued `decision_id` MUST be marked as simulation evidence and MUST NOT be accepted as an Authorized Decision Reference.

Simulation is a distinct pre-decision evidence class. It records what the organization knew before it acted, and it is never confused with an outcome.

### 5.4 Constraints, obligations, and evidence

`constraints` reports the result of each constraint in the applicable grant: `satisfied`, `violated`, `unevaluable`, `below_threshold`, or `requires_human`. For Class B constraints the entry MUST carry the classifier identity, version, threshold, and score (SDP-0003 §3.2).

`obligations` lists machine-readable conditions the EP MUST honor when executing a `permit` — for example, a narrower amount than requested, a required co-signer, a notification, or a maximum batch size. An EP that cannot honor an obligation MUST NOT execute and SHOULD report `not_executed` (§7).

`evidence_required` lists what the outcome report (§7) MUST contain for this decision.

## 6. Normative Processing Rules

### 6.1 Default deny

The AE MUST return `deny` unless every Class A constraint in the applicable grant is `satisfied`. A constraint that is `unevaluable` because the request lacks a required value is a failure, not a pass. If no Authority Record applies, the verdict MUST be `deny`.

### 6.2 Every evaluation is a decision

The AE MUST issue a `decision_id` and record a Decision Object for every evaluation, including `deny`, `escalate`, `simulate_required`, and simulated evaluations. An AE MUST NOT record only permits. A denial on the record is evidence that the control worked (SDP-0008 §6); a record of permits alone is evidence of nothing.

`decision_id` values MUST be stable, globally unique, and carry the `dec_` prefix. Their full specification belongs to SDP-0002.

### 6.3 Authority snapshot

The AE MUST evaluate against the authority in force at the act's valid time and MUST return an `authority_snapshot` that identifies the Authority Record, the valid time and recorded time at which it was evaluated, and a digest of the record's canonical form as evaluated. A later change to the Authority Record MUST NOT alter the snapshot of a prior decision. This lets a verifier answer, years later, *what authority existed at the moment of decision* rather than *what authority exists now*.

If the Authority Record's status (SDP-0003 §6) cannot be resolved at evaluation time, the AE MUST return `deny`.

### 6.4 Idempotency

For a given `idempotency_key`:

1. A repeated request whose act digest matches the original MUST return the same verdict and the same `decision_id`, unless the original was `escalate` or `simulate_required` and the condition has since been resolved, in which case the AE returns the resolved verdict and a new `decision_id` linked to the original.
2. A repeated request whose act digest differs from the original MUST receive `deny` with reason `idempotency_conflict`.
3. A `permit` MUST authorize at most one execution of the act. Retries of a single execution reuse the same key and decision; a second execution requires a new key and a new evaluation.

### 6.5 Validity window

A `permit` MUST carry `valid_until`. An EP MUST NOT begin execution after `valid_until`. The AE SHOULD keep the window short relative to the rate at which the relevant authority can change.

### 6.6 Act digest and binding

The AE MUST compute `act_digest` over the JSON Canonicalization Scheme (RFC 8785) form of the request's `subject`, `action`, and `resource` objects, excluding `principal_assertion`. An executing tool that receives an Authorized Decision Reference SHOULD verify that the act it is about to perform matches the digest. A `permit` authorizes the evaluated act and nothing else.

### 6.7 Fail closed

A Level 2 EP MUST treat each of the following as `deny`:

- no response before the EP's timeout;
- a transport error;
- a response that is not a valid AuthZEN evaluation response or lacks a valid `context.sdp`;
- an unrecognized verdict;
- a response whose integrity cannot be verified, once SDP-0007 defines response signing;
- a `permit` whose `valid_until` has passed or whose `act_digest` does not match.

This costs liveness, never safety (SDP-0008 §3).

## 7. Outcome Report

Every `permit` MUST be followed by an outcome report from the EP. This closes the loop between what was authorized and what happened.

```json
{
  "profile": "SDP-0009/0.1",
  "decision_id": "dec_01HZX4T0",
  "idempotency_key": "soc-playbook-88:run-2291:step-4",
  "act_digest": "sha256:9c1e...",
  "result": "succeeded",
  "executed_at": "2026-11-13T20:14:06.020Z",
  "completed_at": "2026-11-13T20:14:07.880Z",
  "effects": [
    { "type": "transaction", "ref": "txn_88412" }
  ],
  "evidence": [
    { "type": "tool_response_digest", "value": "sha256:aa17..." }
  ]
}
```

1. `result` MUST be `succeeded`, `failed`, `partial`, or `not_executed`.
2. The report MUST carry every item listed in the permit's `evidence_required`.
3. `effects` SHOULD link the decision to the transaction, ticket, or record the action produced, so that a verifier can traverse from the outcome back to the authorizing decision and forward again.
4. The AE MUST accept the report against the matching `decision_id` and `act_digest` and MUST reject a report whose digest does not match.
5. A `permit` with no outcome report after `valid_until` plus an implementation-defined grace period MUST be flagged by the AE as an unreported execution. Unreported executions are drift events and are discoverable (SDP-0008 §6).

The outcome is recorded as part of, or linked to, the Decision Object. It MUST NOT overwrite the verdict or the authority snapshot.

## 8. Decision Envelopes and Hierarchies

Some decisions authorize a bounded set of subsequent acts: an incident-response playbook run, a bill run that produces line items, a procurement approval that produces purchase orders.

1. A `permit` MAY carry an `envelope`: a set of Class A constraints that bounds child acts performed under it.
2. A child evaluation MUST carry `parent_decision_id`. The AE MUST evaluate the child against both the parent's envelope and the child actor's own authority. The child is permitted only if both permit it.
3. An envelope MUST NOT be broader than the authority under which the parent was permitted. This mirrors the delegation rule of SDP-0003 §7.
4. Aggregate constraints in an envelope (for example, a total amount across all children) MUST be evaluated against the cumulative children recorded so far.
5. A child Decision Object MUST reference its parent. A parent's outcome report SHOULD reference its children.

Envelopes prevent an actor from splitting one unauthorized act into many small ones that each pass on their own.

## 9. Bindings

### 9.1 HTTPS (normative)

- Evaluation: the AuthZEN Access Evaluation endpoint, `POST /access/v1/evaluation`.
- Batch evaluation: the AuthZEN `POST /access/v1/evaluations` endpoint MAY be used. Each item is a separate evaluation with its own `decision_id` and `idempotency_key`.
- Outcome report: `POST /sdp/v1/outcome`.
- Discovery: the AE's AuthZEN metadata document MUST list `"sdp_profiles": ["SDP-0009/0.1"]` and the outcome endpoint URI.

Transport security, client authentication, and response signing follow AuthZEN and SDP-0007 respectively.

### 9.2 MCP (informative)

An MCP gateway in the proxy position is a natural EP. On each `tools/call`, the gateway maps the call to an evaluation request — the tool name to `action.name`, the arguments the grant's Class A constraints require into `action.properties.sdp`, the target into `resource` — and forwards the call only on `permit`, attaching the `decision_id`. The AuthZEN COAZ-MCP binding draft describes the general mapping of MCP messages into AuthZEN requests and SHOULD be followed where it applies.

### 9.3 Workflow and orchestration engines (informative)

Workflow engines, SOAR platforms, and RPA tools that execute consequential steps on behalf of AI or human operators can act as EPs by placing an evaluation step immediately before each consequential action and an outcome-report step immediately after it. Such an engine satisfies Level 2 only if it holds the credentials for the gated action, so that the action cannot run without passing through the evaluation step.

## 10. Security Considerations

This section maps the interface to the Kinsana threat model.

- **Authority Spoofing.** The AE MUST verify `principal_assertion` and MUST NOT accept identity or authority asserted only in unsigned request members. `authority_hint` is never authoritative (§4.2).
- **Decision Laundering.** Envelope bounds (§8) and act-digest binding (§6.6) prevent an authorization for one act from being reused for another, or split across many.
- **Selective Memory.** Recording every evaluation including denials (§6.2), and flagging permits with no outcome (§7.5), means the record cannot be curated after the fact.
- **Drift Exploitation.** Authority snapshots (§6.3) and short validity windows (§6.5) prevent a stale grant from authorizing new acts, and fix the evaluated authority so it cannot be revised later.
- **Compliance Theater.** An advisory call the actor may skip is not enforcement. Level 2 requires the EP to hold the credentials (SDP-0008 §3.2); this interface does not change that.
- **Replay.** Idempotency (§6.4), validity windows (§6.5), and single-execution permits prevent a captured `permit` from authorizing repeat execution.
- **Availability.** Fail closed (§6.7) means an AE outage halts consequential actions. Deployments SHOULD plan AE availability accordingly; they MUST NOT fail open to preserve availability. Break-glass authority remains an open question in SDP-0003 §9.

## 11. Conformance

- An EP or AE claiming Level 0 against this RFC MUST produce and accept messages that validate against the request, response, and outcome-report schemas.
- An EP claiming Level 2 MUST implement §6.7 and §7 in full and MUST sit in the proxy position per SDP-0008 §3.
- An AE claiming conformance MUST implement §6.1 through §6.6, §7.4, §7.5, and §8.
- The SDP-0008 §5 test suite SHOULD add vectors for: default deny on a missing Class A value; a recorded `deny`; idempotency replay and conflict; an expired `permit`; act-digest mismatch; a child act exceeding its parent envelope; and an unreported execution.

JSON Schemas for the request, response, and outcome-report members are to be published as `sdp-evaluation.schema.json` and `sdp-outcome.schema.json`.

## 12. Open Questions

- Should this profile adopt the AuthZEN Obligations and Access Request profiles once they are final, replacing `obligations` and `escalate` with their members?
- Should Level 2 require a maximum evaluation latency, consistent with the open question in SDP-0008 §8?
- May an EP cache a `permit` for a class of identical acts, and if so, how is each execution still recorded?
- How are evaluations performed when the EP is disconnected from the AE (edge, offline), short of failing closed?
- Is `escalate` a single verdict, or should Class B below-threshold and Class C human disposition be distinguished at the verdict level?
- Should response signing be required at Level 2 before SDP-0007 is complete?

## 13. Acknowledgments

The authority snapshot, simulation evidence class, idempotent decision-to-outcome linkage, and prefixed decision identifiers draw on RFC input from CloudBill engineering to SDP v0.1. The wire shape follows the OpenID AuthZEN Authorization API 1.0.

## 14. Status

Draft. Request, response, verdict set, and fail-closed rules are open for review and implementation feedback. Schemas and test vectors are pending.
