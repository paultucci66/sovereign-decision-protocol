# What SDP Does Not Protect Against

SDP governs the **scope** of a decision — who was authorized to make it, within what bounds, and whether those bounds were enforced. It does not govern the **quality** of a decision. These are different problems, and conflating them is the fastest way to lose the audience that matters the first time a governed agent does something wrong inside its envelope.

This document states the boundary plainly, so that it is stated by the project rather than about it.

## An agent can be fully in scope and fully wrong

A within-cap purchase of a defective product is authorized. A credit issued to the wrong account, for a permitted amount, is authorized. A message that is perfectly compliant and commercially disastrous is authorized. A scope gate evaluates whether an action falls inside a granted boundary; it has, by construction, no view of whether the action was correct.

The following are invisible to an authority model and remain the deployer's responsibility:

- **In-scope error.** Correct authority, wrong judgment. The gate passes it.
- **Prompt injection inside the envelope.** A compromised agent acting within its granted scope produces authorized harm. Authority scope does not detect compromise; it bounds blast radius.
- **Model regression or drift within scope.** A model that degrades while staying inside its bounds produces worse decisions the gate still admits.
- **Aggregate harm from individually valid actions.** Addressed only to the extent typed aggregate constraints (SDP-0003) are configured; the residual, especially across organizations, is an open design problem.

## What scope *does* do about these

The honest claim is narrower and still valuable:

- **Caps bound blast radius.** They do not prevent error; they limit its magnitude. A wrong decision under a $5,000 cap is wrong by at most $5,000.
- **Enforcement makes the boundary real.** An enforced deny (SDP-0008 Level 2) prevents out-of-scope action and produces an exculpatory record. It does nothing about in-scope error.
- **The record enables review.** Recorded decisions make sampling, audit, and post-hoc analysis possible. Detecting in-scope error is a review and evaluation function that operates *on* the record; it is not performed *by* the scope gate.
- **Residual risk is a portfolio problem.** In-scope error is managed the way other operational risk is managed — review sampling, human-in-the-loop on high-materiality classes, and insurance — not eliminated by authority infrastructure.

## The one-sentence version

Authority is not alignment. SDP makes it verifiable that an agent acted within granted bounds and that the bounds were enforced; it does not make the agent correct, uncompromised, or wise.

Governance is orthogonal to safety — a category apart, the way jurisdiction is orthogonal to whether a verdict is correct. A court can hold unquestioned authority to rule and rule wrongly; the authority was never the thing carrying the safety load. So it is here. No more than human government is safe. Bad governance is unsafe but no less governed. A perfectly governed agent can do real harm inside its envelope, and nothing in this protocol claims otherwise. Governed is not safe. We are saying so plainly, so that no one can say they were not warned.
