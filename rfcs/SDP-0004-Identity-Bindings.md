# SDP-0004: Identity Bindings

Status: Draft Skeleton

Version: 0.1

Author: Paul Tucci

License: Apache 2.0

## Abstract

This RFC will define how SDP Decision Objects reference identity systems without becoming an identity protocol.

SDP is identity-agnostic.

## Purpose

The purpose of this RFC is to define how Decision Objects bind actors, approvers, agents, systems, and organizations to external identity providers.

## Scope

This RFC is expected to define:

- Identity reference format
- Human actor references
- AI agent references
- Application/system references
- Organization references
- Identity provider metadata
- Time-of-decision identity assertions
- Identity verification references

## Non-Goals

This RFC will not define:

- Authentication
- Identity proofing
- User directories
- SSO implementation
- OAuth/OIDC profiles
- PKI profiles
- Biometric identity

## Design Note

Identity systems answer who acted.

SDP records which identity assertion was relied upon at the time of decision.

Authority remains separate and is defined in SDP-0003.

## Open Questions

- What identity metadata is required for interoperability?
- How should AI agents be identified?
- How should service accounts and automated systems be represented?
- How should identity provider changes be handled over time?

## Status

Draft skeleton. Full specification pending.
