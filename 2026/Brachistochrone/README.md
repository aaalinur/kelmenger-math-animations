# Brachistochrone

This folder contains the brachistochrone animation, showing how a ball travels along different paths between two points and why the cycloid is the fastest under gravity.

## Main script

- `brachistochrone.py` — main Manim scene entry point
- `f.py` — legacy script kept for compatibility
- `background.py` — space-themed background used by the animation
- `ball.png` — image asset for the moving ball

## Render

From this directory, run:

```bash
manim brachistochrone.py
```

## Notes

The original generic filename `f.py` was renamed to `brachistochrone.py` to make the animation purpose clearer, while the old file remains as a compatibility alias.
