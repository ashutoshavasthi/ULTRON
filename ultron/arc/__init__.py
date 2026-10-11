"""Ultron on ARC-AGI: the Abstraction and Reasoning Corpus (Chollet, 2019), the public
benchmark for learning a new rule from a few examples.

Each task shows a few input → output grid pairs. Ultron must find the rule and apply it
to new inputs. It does this the way it finds every law: the shortest program that
explains every example, built from generic grid perception and operations (see
PRIMITIVES.md), found by size-ordered search.
"""
