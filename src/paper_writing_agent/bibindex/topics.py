"""Topic vocabulary and a conservative keyword tagger.

The vocabulary is generic to computer science and software engineering. Tagging
is heuristic and intentionally cautious: it assigns a tag only on a clear keyword
match and falls back to ``other`` rather than guessing. Users can re-tag entries
by hand; the index is human-editable and merge-preserving.
"""

from __future__ import annotations

__all__ = ["TOPIC_TAGS", "tag_entry"]

# tag -> keywords that, if found in the title or venue, imply the tag.
_TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "machine_learning_general": ("learning", "neural", "gradient", "classifier", "regression"),
    "deep_learning_architecture": (
        "transformer",
        "attention",
        "convolutional",
        "cnn",
        "resnet",
        "architecture",
        "encoder",
        "decoder",
    ),
    "computer_vision": ("image", "vision", "segmentation", "detection", "object", "video"),
    "nlp": ("language model", "nlp", "translation", "text", "token", "embedding"),
    "systems_distributed": (
        "distributed",
        "parallel",
        "scalable",
        "cluster",
        "scheduling",
        "consensus",
        "fault",
    ),
    "compilers_pl": ("compiler", "programming language", "type system", "semantics", "runtime"),
    "databases": ("database", "query", "transaction", "index", "storage engine", "sql"),
    "security": ("security", "cryptograph", "attack", "vulnerab", "privacy", "adversarial"),
    "optimization_training": ("optimization", "optimizer", "training", "sgd", "adam", "scheduler"),
    "hardware_acceleration": ("gpu", "fpga", "accelerator", "cuda", "tpu", "simd", "kernel"),
    "software_engineering": (
        "software engineering",
        "testing",
        "refactoring",
        "code review",
        "bug",
        "maintenance",
    ),
    "theory_algorithms": ("algorithm", "complexity", "np-hard", "approximation", "graph theory"),
    "benchmarking_survey": ("benchmark", "survey", "comparison", "evaluation", "empirical study"),
    "datasets_benchmarks": ("dataset", "corpus", "benchmark suite", "collection"),
    "reproducibility_tools": (
        "reproducib",
        "framework",
        "library",
        "toolkit",
        "pytorch",
        "tensorflow",
        "open source",
    ),
}

TOPIC_TAGS: tuple[str, ...] = (*_TOPIC_KEYWORDS.keys(), "other")


def tag_entry(title: str, venue: str) -> list[str]:
    """Return one or more topic tags for an entry; ``["other"]`` if none match."""
    haystack = f"{title} {venue}".lower()
    tags = [tag for tag, keywords in _TOPIC_KEYWORDS.items() if any(k in haystack for k in keywords)]
    return tags or ["other"]
