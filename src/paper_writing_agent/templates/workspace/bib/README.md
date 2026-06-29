# Bibliography

Put your BibTeX file here as `refs.bib`, then build the context index:

```bash
pwa bib build bib/refs.bib --output bib/bib_index.yaml
pwa bib validate bib/bib_index.yaml --bib bib/refs.bib
```

The index gives each key a topic, a citation role, suitable contexts, and sample
phrases so the agent can cite accurately. After editing the `.bib`, regenerate
with `--update` to preserve any curation you have added.

If you have a prior paper, anchor citations in real usage:

```bash
pwa bib ground bib/bib_index.yaml --from /path/to/prior/*.tex
```
