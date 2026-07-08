# SDP-0003: Authority Model

Status: Draft Skeleton

Version: 0.1

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC will define how SDP represents authority for consequential decisions.

SDP separates identity from authority.

Authentication proves who a principal is.

Authority determines what that principal may decide.

## Purpose

The purpose of this RFC is to define a vendor-neutral authority model that can be referenced by Decision Objects.

## Scope

This RFC is expected to define:

- Authority references
- Delegated authority
- Authority scope
- Authority conditions
- Authority expiration
- Authority revocation
- Chain of authority
- Decision signatures
- Trust anchors
- Authority verification metadata

## Non-Goals

This RFC will not define:

- A specific identity provider
- A specific PKI implementation
- A specific access-control product
- A specific policy engine
- Organizational approval workflows

## Design Note

The authority model may use concepts similar to public key infrastructure, including trust anchors, delegated authority, revocation, signatures, and time-bound credentials.

SDP should support those patterns without requiring any specific PKI stack.

## Open Questions

- What minimum authority metadata is required for conformance?
- How should temporary authority be represented?
- How should emergency authority be represented?
- How should revoked authority be validated after the fact?

## Status

Draft skeleton. Full specification pending.
