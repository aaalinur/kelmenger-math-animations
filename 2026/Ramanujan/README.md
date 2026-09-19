# Ramanujan

This folder contains experiments and visualizations related to Ramanujan-style nested radicals and recursive algebraic identities.

## Main scripts

- `ramanujan_nested_radical.py` — the main nested-radical explanation scene
- `ramanujan_infinity.py` — an infinite-form visual scroll animation
- `ramanujan3num.py` — a three-number variant of the idea
- `problem.py` — legacy file kept for compatibility

## Concept

The animations center on expressions such as:

\[
3 = \sqrt{1 + 2\sqrt{1 + 3\sqrt{1 + 4\sqrt{\dots}}}}
\]

## Render

From this directory, run:

```bash
manim ramanujan_nested_radical.py
```

## Notes

The earlier generic file name `problem.py` was renamed to `ramanujan_nested_radical.py` for clarity; the original is retained temporarily for compatibility.
