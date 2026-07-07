# Classification Model

Decision Objects may be public, private, shared, restricted, or subject to other disclosure rules.

SDP SHOULD support the classification pattern without adopting any single government, military, legal, or enterprise classification regime as the protocol standard.

## Purpose

Classification answers a different question than materiality.

Materiality asks:

> How consequential is this decision?

Classification asks:

> Who may know about this decision?

A decision may be highly material and public.

A decision may be low materiality but highly restricted.

The two dimensions SHOULD remain separate.

## Pattern Support

Many organizations already understand classification models.

Government and defense organizations may think in terms of public, controlled, confidential, secret, top secret, compartmented, or eyes-only patterns.

Enterprises may think in terms of public, internal, confidential, restricted, legal privileged, executive-only, customer-shared, or regulator-shared records.

SDP SHOULD support these patterns by defining classification metadata, not by mandating one universal label set.

## Baseline Classification Concepts

Implementations MAY support baseline classifications such as:

| Classification | Meaning |
|----------------|---------|
| Public | May be disclosed publicly |
| Internal | Limited to the owning organization |
| Confidential | Limited to authorized internal parties |
| Restricted | Limited to specific roles, groups, or purposes |
| Shared | Disclosable to named external parties under policy |
| Compartmented | Limited to a defined compartment or need-to-know group |

These labels are illustrative.

Organizations MAY map SDP classification metadata to their own classification schemes.

## Decision Object Metadata

A Decision Object SHOULD be able to carry classification metadata such as:

```json
{
  "classification": {
    "level": "restricted",
    "scheme": "organization-defined",
    "owner": "acme-corp",
    "accessPolicy": "POLICY-SEC-17",
    "compartments": ["legal", "executive"],
    "externalDisclosure": {
      "allowed": true,
      "allowedParties": ["auditor", "regulator"],
      "basis": "AUDIT-REQUEST-2026-04"
    }
  }
}
```

The DCP enforces access.

SDP records the classification and disclosure intent.

## Redaction

Some Decision Objects may need to be shared in redacted form.

SDP SHOULD allow a published object to reference a redacted derivative while preserving the integrity relationship to the original object.

The protocol should support the pattern.

The DCP should implement the policy, redaction, approval, and audit mechanics.

## Design Boundary

SDP classifies the Decision Object.

The DCP enforces access, disclosure, redaction, compartmentalization, and audit.

Applications consume only what they are authorized to see.
