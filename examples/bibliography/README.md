# Bibliography example

A small, synthetic `refs.bib` with three computer-science references. Use it to
see the citation pipeline end to end.

```bash
# Build a context index (topics, roles, sample phrases, cite_as).
pwa bib build examples/bibliography/refs.bib --output /tmp/bib_index.yaml

# Validate it against the schema and the anti-hallucination gates.
pwa bib validate /tmp/bib_index.yaml --bib examples/bibliography/refs.bib

# Ground citations in how a prior paper used them (marks entries verified).
pwa bib ground /tmp/bib_index.yaml --from examples/latex/abstract.tex examples/latex/introduction.tex
```

The index seeds each entry's `key_findings` from its title and leaves the
semantic fields for you (or the agent) to curate. Re-run `build --update` after
editing the `.bib` to add new keys without losing curation.
