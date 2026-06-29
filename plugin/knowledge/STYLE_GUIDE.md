# High-impact manuscript style guide

This is the single source of truth for writing and typesetting a manuscript with
this tool. It is journal-agnostic: venue-specific choices are configuration
(`paper-writing-agent.toml`), noted inline as **[configurable]**. The forbidden-
vocabulary values are owned by the linter, not duplicated here; run `pwa lint`
and `pwa check` for the authoritative, enforced lists.

Quality hierarchy: **Accuracy > Clarity > Conciseness > Professionalism.**

## 1. Conceptual standards

- **Lead with the advance.** State the conceptual or technical contribution
  early. A reader should know what is new and why it matters within the first
  paragraph of the abstract and the introduction.
- **One message per paragraph.** Open each paragraph with its claim; the rest of
  the paragraph supports that claim. No naked paragraphs outside a section.
- **Claim-based Results headings.** A Results subsection heading states a finding
  ("Method X halves training time at equal accuracy"), not a topic ("Training
  time"). Reading the headings in order should give the take-home messages.
  Methods headings stay neutral and descriptive.
- **Prose, not bullet lists.** The body is connected prose. Reserve lists for
  genuine enumerations.
- **Captions are self-contained.** A reader who sees only the figure and its
  caption understands what was done. Caption order: a title sentence, the design,
  the sample size and what the error bars mean, and the statistical test (named
  once per figure). Captions describe what is shown; they do not state results or
  interpretation. Describe only what the artwork shows; if a fact is essential
  and missing, fix the artwork rather than narrate around it.

## 2. Typography

- **Non-breaking spaces** between a label and its number and before references:
  `Figure~1`, `Table~2`, `Section~3`, `16~bp`.
- **Ranges** use an en-dash: `10--20`, `0.48--0.77`.
- **Figure/table references** **[configurable]** `style.figure_ref`: `full`
  ("Figure 1", "Table 2") or `abbreviated` ("Fig. 1", "Tab. 2"). Be consistent.
- **No em dashes.** Use commas, parentheses, or a period. The linter enforces
  this by default (`slop.em_dash = "zero"`).

## 3. Statistics

- **Every P-value carries a verdict.** A sentence that gives a P-value must also
  say, in words, whether the comparison is significant. A bare P-value is a
  defect (`pwa stats` flags it).
- **Earn "significant".** Permitted only with a test, a P-value below threshold,
  and the verdict in the same or an adjacent sentence.
- **Name a test once,** at first occurrence ("Welch's *t*-test"); afterwards give
  the P-value alone.
- **P-value notation [configurable]** `stats.pvalue_notation`: `P-italic-sci`
  (italic capital *P*, `2.6 x 10^{-5}`), `p-lower-sci`, or `p-lower-e`.
- **Italic** statistical symbols: *n*, *r*, *P*, Spearman *p*.
- **Equivalence is not non-significance.** To claim two methods are equivalent,
  use an equivalence test (for example TOST) or a confidence interval; do not
  infer equivalence from a non-significant difference.

## 4. Numbers and units

- **Thousands separators [configurable]** `stats.thousands_separator`: write
  `4,093` and `300,000,000`.
- **Leading zero [configurable]** `stats.leading_zero`: write `0.70`, not `.70`.
- **Significant figures [configurable]** `stats.significant_figures` (default 2):
  round from the full-precision value in the statistics store, never from a
  figure image.
- **Number and unit** take a space: `16 bp`, `40 GB`, `500 ms`. The percent sign
  is closed up: `45.6%`. Write multipliers as `22.5 times` or `22.5-fold`.

## 5. Punctuation

- **Oxford comma** in lists: `A, B, and C`.
- **Semicolons** separate complex list items that contain commas, and join two
  closely related independent clauses.
- **Colons** introduce a list or an explanation after a complete clause.

## 6. Nomenclature and spelling

- **Define once, then use bare.** Introduce an abbreviation at first use as
  "Long Form (ABBR)"; afterwards use the abbreviation alone. Do not redefine.
  `pwa defs check` enforces this in reading order.
- **No undefined symbols.** Define every symbol at first use; keep a registry
  (see `DEFINITIONS.template.md`).
- **Spelling [configurable]** `style.spelling`: `US` or `UK`. Be consistent
  (`optimization`/`optimisation`, `behavior`/`behaviour`).
- **No implementation identifiers in prose.** Write "the attention layer", not
  `MultiHeadAttention`; name the concept, not the class.

## 7. Language quality (anti-AI-slop)

The linter owns the enforced lists; this section states the intent.

- **Forbidden (Tier 1).** Strong AI markers and self-praise: words like `delve`,
  `underscore`, `pivotal`, `tapestry`, and claims like `novel`, `remarkable`,
  `prove`. The reader judges merit; the author reports facts.
- **Replace (Tier 2).** Prefer precise alternatives: `use` over `leverage`,
  `improve` over `enhance`, `reliable` over `robust`, `through` over `via`.
- **Forbidden phrases (Tier 3).** Filler such as `due to the fact that`,
  `it is important to note that`, and `in the ever-evolving landscape of`.
- **Structure.** Avoid copula avoidance (`serves as`), participle padding
  (`..., highlighting ...`), negative parallelism (`not only ... but also`), and
  forced rules of three.

## 8. Hedging

Calibrate confidence to evidence:

- High: `demonstrate`, `establish`, `show` (for a result with a significant test).
- Moderate: `suggest`, `indicate`, `support`.
- Low: `may`, `might`, `could`, `appears to`.
- Speculation: `hypothesize`, `propose`, `we speculate`.
- Avoid: `prove`, `definitely`, `obviously`, `clearly`, `of course`.

## 9. Discussion and Conclusion

A Discussion has, in order: a direct answer to the research question; the key
findings with data; comparison to three to five prior works; the mechanism or
rationale; broader implications; an honest limitations paragraph; and concrete
future directions. A Conclusion integrates (does not merely summarize), states
the contribution, looks forward, and introduces no new data.

## 10. Section architecture **[configurable]**

`style.section_structure`: `methods-supplementary` ("Materials and Methods" plus
a Supplementary section), `methods-extended` (Methods plus Extended Data), or
plain `imrad`. Fixed reading order: Abstract, Introduction, Results, Discussion,
Methods, Supplementary. Never use a concept before the section that defines it.

## 11. Pre-submission checklist

- [ ] `pwa check` is clean (no errors).
- [ ] Every P-value has a verdict; each test is named once.
- [ ] Every abbreviation and symbol is defined before first use.
- [ ] Every citation key exists; no `% TODO: cite` remains.
- [ ] Captions are self-contained and free of results/interpretation.
- [ ] Numbers, units, and spelling follow the configured house style.
- [ ] If LaTeX: the document compiles with no new errors or undefined references.
