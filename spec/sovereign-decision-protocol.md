# Sovereign Decision Protocol (SDP)

**Version:** 0.1  
**Status:** Draft  
**Maintained by:** Tempismo LLC  
**License:** Apache 2.0

---

## Purpose

The Sovereign Decision Protocol (SDP) defines a standard structure for
representing, governing, preserving, and learning from consequential
organizational decisions.

SDP is intended to provide a common language for humans, AI systems,
workflows, governance platforms, security systems, and enterprise
applications to communicate decision information in a consistent and
auditable manner.

The protocol does not execute actions.

The protocol records decisions, authority, evidence, outcomes, and
organizational learning.

---

## Foundational Principles

### Principle 1: A Decision Object Creates a Decision Record

A Decision Object is the authoritative representation of a decision.

A Decision Record is the complete historical record generated throughout
the lifecycle of that decision.

Every Decision Object SHALL generate a corresponding Decision Record.

Every Decision Record SHALL be immutable.

---

### Principle 2: Decisions and Actions Remain Separate

A decision is not an action.

The protocol records:

- What was decided
- Why it was decided
- Who authorized it
- What evidence was considered

Execution systems perform actions.

SDP records actions but does not perform them.

This separation preserves accountability and interoperability.

---

### Principle 3: Separation of Powers

Organizations operate through three governance functions:

**Legislative** — Defines policies, authority, rules, and constraints.

**Executive** — Executes workflows, deployments, provisioning, and
operational actions.

**Judicial** — Evaluates outcomes, compliance, effectiveness, and
lessons learned.

SDP preserves the authoritative record connecting all three.

---

### Principle 4: Consequential Decisions Only

Not all decisions warrant preservation.

SDP is intended for material decisions. Examples include:

- AI deployment approvals
- Capital expenditures
- Vendor approvals
- Regulatory decisions
- Security exceptions
- Policy changes
- Hiring decisions
- Mergers and acquisitions

Organizations SHOULD establish materiality thresholds.

---

### Principle 5: Governance Should Minimize Friction

Governance exists to create confidence.

Governance that does not improve outcomes should be simplified or removed.

That which governs least governs best.

---

### Principle 6: Emergent Risk

Risk may emerge from the interaction of individually authorized components.

An authorized action plus an authorized action does not necessarily produce
an authorized aggregate outcome.

SDP implementations SHOULD evaluate the aggregate intent of linked decision
chains — not only the authorization status of each individual decision.

The `aggregate_intent` field on a Decision Object enables this evaluation.

---

### Principle 7: The Enterprise Remains the Finder of Fact

SDP provides evidence, governance, lineage, and traceability.

The enterprise determines conclusions.

AI systems may participate in decision making.

AI systems SHALL NOT be the source of authority.

---

## Relationship to Transaction-Layer Protocols

SDP operates at the decision layer. It sits above transaction-layer
protocols such as the Agent Payments Protocol (AP2) and x402.

Transaction-layer protocols answer a bounded question: is this specific
transaction authorized, by a verifiable mandate, and executed correctly
between parties? Their primitive is the mandate — a signed, scoped grant
authorizing a single transaction. They make an individual agent-to-agent
exchange trustworthy.

SDP does not authorize or execute transactions. It records the decision
that a transaction implements: who decided, under what authority, against
which policy, with what expected outcome, and what was learned. A mandate
at the transaction layer is one input to a Decision Object — it is captured
as evidence or as an Action Object linked to the governing decision.

The two layers are complementary, not competing:

| Layer | Question | Primitive |
|---|---|---|
| Transaction (AP2, x402) | Is this transaction authorized and correctly executed? | Mandate |
| Decision (SDP) | Was the decision this transaction carries out actually sanctioned? | Decision Object |

A mandate may be perfectly valid at the transaction layer and still
implement a decision that no principal actually sanctioned. This is the
gap SDP addresses. It is most acute where individually valid transactions
aggregate into an outcome no one authorized — the condition described in
Principle 6. Transaction-layer protocols validate each mandate in isolation
and have no view of the aggregate. The Decision Object, with its
`aggregate_intent` field and linked decision chain, does.

SDP therefore complements transaction-layer infrastructure. Where AP2 and
x402 establish that a transaction is trustworthy, SDP establishes that the
decision behind it was authorized, recorded, and accountable.

---

## The Six Pillars

SDP is organized around six governance pillars. Each pillar contributes
to the Decision Object. The Decision Object is the nexus of all six.

```
Identity
Authority
Governance
Memory
Context
Drift
    ↓
Decision Object
    ↓
Decision Record
    ↓
Organizational Learning
```

**Identity** — Know who or what is participating in a decision.

**Authority** — Know who has the right to decide.

**Governance** — Know the policies, rules, and constraints that apply.

**Memory** — Preserve institutional knowledge and prior decisions.

**Context** — Capture the circumstances surrounding the decision.

**Drift** — Detect and respond when assumptions, policies, models,
or outcomes diverge from expectations.

---

## Core Objects

### Decision Object

Represents a material organizational decision.

**Attributes:**

| Field | Type | Description |
|---|---|---|
| `decision_id` | string | Globally unique identifier |
| `decision_type` | string | Classification of decision |
| `title` | string | Human-readable description |
| `description` | string | Full description and rationale |
| `status` | enum | Current lifecycle status |
| `authority` | Authority Object | Who authorized this decision |
| `risk_level` | enum | low \| medium \| high \| critical |
| `materiality` | enum | low \| medium \| high \| critical |
| `owner` | string | Decision owner identity |
| `requestor` | string | Requesting party identity |
| `context` | object | Circumstances at decision time |
| `aggregate_intent` | string | Intent of the full workflow chain |
| `evidence_ids` | array | References to Evidence Objects |
| `expected_outcomes` | array | What the decision is intended to produce |
| `actual_outcomes` | array | What the decision actually produced |
| `conditions` | array | Conditions attached to authorization |
| `dependencies` | array | Decision IDs this decision depends on |
| `workflow_id` | string | Groups decisions in a workflow chain |
| `created_at` | ISO8601 | Creation timestamp |
| `effective_from` | ISO8601 | When decision takes effect |
| `expires_at` | ISO8601 | When authorization expires |
| `supersedes` | string | Decision ID this supersedes |
| `superseded_by` | string | Decision ID that supersedes this |
| `learning_summary` | string | Lessons captured from this decision |

**Example:**

```json
{
  "decision_id": "DEC-12345",
  "decision_type": "AI_DEPLOYMENT",
  "title": "Deploy Customer Service Agent",
  "status": "APPROVED",
  "risk_level": "HIGH",
  "materiality": "HIGH",
  "aggregate_intent": "Automate tier-1 customer support to reduce response time",
  "workflow_id": "WF-891"
}
```

---

### Authority Object

Represents delegated decision authority.

**Attributes:**

| Field | Type | Description |
|---|---|---|
| `authority_id` | string | Unique identifier |
| `role` | string | Organizational role |
| `scope` | array | Decision types within authority |
| `limits` | object | Constraints on authority |
| `delegation_chain` | array | Chain of delegated authority |
| `granted_by` | string | Who granted this authority |
| `granted_at` | ISO8601 | When authority was granted |
| `expires_at` | ISO8601 | When authority expires |

**Example:**

```json
{
  "authority_id": "AUTH-100",
  "role": "CISO",
  "scope": ["AI_DEPLOYMENT", "SECURITY_EXCEPTION"],
  "limits": {
    "max_risk_level": "HIGH",
    "requires_co_authorization_above": "CRITICAL"
  }
}
```

---

### Evidence Object

Represents information considered during decision making.

Examples: risk assessments, policy documents, security reviews,
financial analyses, legal opinions, system state snapshots,
prior Decision Objects.

Evidence may be stored externally and referenced by SDP.

**Attributes:**

| Field | Type | Description |
|---|---|---|
| `evidence_id` | string | Unique identifier |
| `evidence_type` | enum | data \| document \| signal \| prior_decision \| system_state \| external \| human_attestation |
| `title` | string | Description of evidence |
| `source` | string | Originating system or person |
| `content_uri` | string | External reference if applicable |
| `integrity_hash` | string | SHA256 for tamper detection |
| `captured_at` | ISO8601 | When evidence was captured |
| `captured_by` | string | Who or what captured it |

---

### Action Object

Represents an executed activity linked to a decision.

Examples: agent deployed, access granted, account created, policy applied,
infrastructure provisioned, configuration changed.

**Actions SHALL reference a Decision Object.**

**Actions SHALL NOT replace a Decision Object.**

**Attributes:**

| Field | Type | Description |
|---|---|---|
| `action_id` | string | Unique identifier in executing system |
| `decision_id` | string | Decision Object this action is linked to |
| `action_type` | string | Classification of action |
| `description` | string | What was done |
| `target_system` | string | System where action was executed |
| `target_resource` | string | Specific resource acted upon |
| `executed_by` | string | Identity of executing system or person |
| `executed_at` | ISO8601 | Execution timestamp |
| `parameters` | object | Action parameters at execution time |

---

### Outcome Object

Represents measured results of an executed decision.

Examples: success metrics, compliance findings, risk events,
cost savings, operational impact, variance from expected.

Outcomes enable organizational learning.

**Attributes:**

| Field | Type | Description |
|---|---|---|
| `outcome_id` | string | Unique identifier |
| `decision_id` | string | Decision Object this outcome belongs to |
| `description` | string | What was observed |
| `metric` | string | How outcome was measured |
| `expected_value` | string | What was predicted |
| `actual_value` | string | What occurred |
| `variance` | string | Delta between expected and actual |
| `variance_significance` | enum | none \| minor \| moderate \| material \| critical |
| `measured_at` | ISO8601 | When outcome was measured |
| `measured_by` | string | Who or what measured it |

---

## Decision Record

A Decision Record is an immutable event stream.

The Decision Record represents organizational memory.

**Example Event Stream:**

```
DecisionCreated
EvidenceAdded
RiskAssessmentCompleted
PolicyEvaluated
ApprovalGranted
ConditionsAdded
ActionExecuted
OutcomeMeasured
VarianceDetected
ReviewConducted
LearningCaptured
```

The Decision Record SHALL preserve chronology.

Events SHALL NOT be modified after creation.

Corrections SHALL be recorded as additional events.

---

## Materiality Classification

Organizations MAY classify decisions as:

| Level | Examples |
|---|---|
| Low | Routine operational decisions within policy |
| Medium | Decisions with moderate risk or cost impact |
| High | Decisions with significant risk, cost, or regulatory exposure |
| Critical | Board-level, M&A, major regulatory, existential risk decisions |

Materiality influences approval requirements, retention requirements,
review requirements, and evidence requirements.

---

## Decision Lifecycle

```
Proposed → Under Review → Approved → Executed → Monitored → Completed → Archived
                        ↘ Rejected
                                         ↘ Revoked (at any post-approval stage)
```

| Status | Description |
|---|---|
| Proposed | Decision Object created, not yet evaluated |
| Under Review | Under authority evaluation |
| Approved | Authorized to proceed |
| Rejected | Denied — do not proceed |
| Executed | Action has been taken |
| Monitored | Outcome tracking in progress |
| Completed | Outcome recorded, learning captured |
| Archived | Retained per policy, no active monitoring |
| Revoked | Authorization withdrawn post-approval |

---

## MCP Interface

The SDP MCP Interface provides a standard way for systems to interact
with Decision Objects programmatically.

### `decision.create()`
Creates a Decision Object in `Proposed` status.

### `decision.get()`
Retrieves the current state of a Decision Object.

### `decision.add_evidence()`
Associates an Evidence Object with a Decision Object.

### `decision.request_authority()`
Submits a Decision Object for authority evaluation.
Returns disposition: `allow | deny | escalate | require_approval | require_evidence`

### `decision.record_action()`
Associates an executed Action Object with a Decision Object.
Confirms authorization before recording.

### `decision.record_outcome()`
Associates measured Outcome Objects with a Decision Object.
Triggers variance and drift evaluation.

### `decision.search()`
Searches Decision Objects and Decision Records by structured query
or natural language.

### `decision.record()`
Returns the complete, immutable Decision Record event stream for
a Decision Object.

---

## Retention

Recommended retention guidance:

| Type | Retention |
|---|---|
| Operational Decisions | 7 years |
| Governance Decisions | 10 years |
| Strategic Decisions | Permanent |
| Board / Legal / Regulatory | Permanent or legal hold |

Organizations shall apply applicable jurisdictional requirements.

---

## Institutional Memory

The Decision Record constitutes organizational memory.

The purpose of preserving decisions is not merely auditability.

The purpose is learning.

Organizations that preserve decisions, evidence, outcomes, and lessons
learned create a compounding knowledge asset. This institutional memory
becomes increasingly valuable over time.

```
Decision → Action → Outcome → Measurement → Investigation → Learning → Better Future Decisions
```

---

## Compatibility

Implementations of SDP are classified as:

**Core Compatible**
Implements: `decision.create()`, `decision.request_authority()`,
`decision.record_action()`

**Full Compatible**
Implements all eight MCP operations plus Evidence integrity hashing,
aggregate intent evaluation, and outcome recording.

**Protocol Compatible**
Full Compatible plus open specification schemas, tenant isolation,
and AI self-authorization prevention.

---

## Vision

The Sovereign Decision Protocol seeks to establish the Decision Object as
a first-class enterprise data structure.

Just as enterprises maintain systems of record for customers, employees,
and financial transactions — organizations will maintain systems of record
for consequential decisions.

The Decision Object becomes the foundation.

The Decision Record becomes the memory.

The Learning Enterprise becomes the outcome.

---

*Sovereign Decision Protocol v0.1 — Tempismo LLC*  
*This specification is published as an open standard.*  
*Feedback and contributions welcome.*
