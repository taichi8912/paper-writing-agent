"""Symbol and abbreviation registry with a no-forward-reference linter.

Maintains a single registry of every symbol and abbreviation, the reading-order
point where it is first defined, and checks that nothing is used before it is
defined and that nothing is defined twice.
"""
