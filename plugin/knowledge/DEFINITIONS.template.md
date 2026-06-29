# Definitions registry (template)

A single registry of every abbreviation and symbol, the point where each is first
defined, and its meaning. It enforces "define once, then use bare" and prevents
forward references and collisions. `pwa defs check` validates the document against
this discipline; `pwa defs build` can seed the abbreviation table from the text.

## Reading order

List the document files in reading order so first-use is well defined:

1. abstract
2. introduction
3. results
4. discussion
5. methods
6. supplementary

## Abbreviations

| Abbreviation | Long form | First defined in |
| --- | --- | --- |
| <ABBR> | <Long Form> | <section> |

## Symbols

| Symbol | Meaning | First defined in | Units |
| --- | --- | --- | --- |
| <symbol> | <meaning> | <section> | <units or -> |

## Rules

- Introduce each abbreviation as "Long Form (ABBR)" at first use, then use it
  bare. Do not redefine.
- Define every symbol at first use; do not reuse one symbol for two meanings.
- Keep this registry in sync with the text; it is the single source of truth for
  what each token means.
