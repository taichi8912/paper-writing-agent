# Design philosophy

This document is the top-level contract for the project. Every feature, default,
and contribution is judged against it. It is the generic, public form of a
manuscript-writing discipline developed while writing high-impact papers.

## Objective function

**Maximize the probability that a manuscript is accepted at a high-impact
venue.** Everything else is subordinate to this objective.

## Quality hierarchy

When two goals conflict, the earlier one wins:

1. **Accuracy**: every claim is factual and backed by data.
2. **Clarity**: an expert understands it on the first read.
3. **Conciseness**: no redundant words or expressions.
4. **Professionalism**: an appropriate academic register throughout.

Accuracy is never traded for brevity; clarity is never traded for polish.

## The eight pillars

1. **Evidence grounding and traceability.** Every claim resolves to a concrete
   source: a number in the statistics store, a figure's provenance chain, a
   citation key with recorded context, or a symbol in the definitions registry.
   Nothing is asserted from memory.

2. **Anti-AI-slop.** AI-generated prose has recognizable fingerprints:
   inflated significance, copula avoidance, present-participle padding, synonym
   cycling, the rule of three, em dashes, and a fixed vocabulary
   (`delve`, `underscore`, `pivotal`, `tapestry`, ...). The tool detects these
   and proposes precise academic replacements.

3. **Statistical honesty.** The words *significant* and *significantly* are
   earned, not asserted. A significance claim requires a statistical test, a
   P-value below threshold, and an explicit verdict in the same or an adjacent
   sentence. A bare P-value with no verdict is a defect.

4. **Single source of truth.** Each rule and each piece of state is owned by
   exactly one canonical file. The style guide owns conventions; the section
   tracker owns completion state; the bibliography index owns citation context;
   the definitions registry owns symbols. No value is duplicated.

5. **Plan, confirm, execute, verify.** The agent reports its plan, waits for the
   user to approve, executes only the approved plan, then verifies the result
   before reporting completion. Decision authority rests with the user.

6. **Reproducibility and audit trail.** Statistics are re-runnable, never
   transcribed from an image. Completion-state changes are timestamped and
   justified. A reader can reconstruct how every number was produced.

7. **Configurable, not rigid.** The original agent was tuned to one author and
   one venue. The public tool exposes every such choice (target venue,
   citation style, spelling variant, P-value notation, section structure,
   strictness, operating language) as a friendly default that the user
   overrides. Sensible out of the box; never a straitjacket.

8. **Dogfooding.** The project applies its own rules to its own prose. The
   anti-slop linter runs on this repository's documentation in pre-commit and
   in CI. How we build the tool demonstrates what the tool enforces.

## What is always on

Independent of configuration, the tool will not:

- let a significance claim stand without a test, a P-value, and a verdict;
- invent a citation key or fabricate a reference;
- make speculative edits to a file it has not read;
- override the user's decision authority;
- demote accuracy below any other quality.

## What the user controls

Target field and venue tier, citation style, spelling variant (US/UK), P-value
notation, significant figures, section structure, figure-reference style,
hedging strictness, operating language, principle verbosity, and project-local
extensions to the forbidden-word lists.
