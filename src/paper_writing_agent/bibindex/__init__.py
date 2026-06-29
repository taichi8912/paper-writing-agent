"""Bibliography context indexer and validator.

Builds a searchable, schema-validated context index from a BibTeX file so the
agent can select citation keys accurately, and validates the index against an
anti-hallucination schema. Supports merge-preserving regeneration and
author-grounded citation extraction from a prior manuscript.
"""
