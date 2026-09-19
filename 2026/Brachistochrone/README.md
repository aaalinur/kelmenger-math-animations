# Brachistochrone

This folder contains a Manim animation exploring the classic brachistochrone problem: among all possible paths between two points, which one minimizes travel time under gravity?

## Included files

- `background.py` — custom space-styled background used in the scene
- `f.py` — main brachistochrone animation
- `ball.png` — asset used in the render

## Render

From this directory, run:

```bash
manim f.py
```

If you want to render a specific scene class, check the class names defined in `f.py` and use:

```bash
manim f.py <SceneName>
```

## Notes

This visual is designed for a vertical 9:16 short-form format and uses a cinematic space aesthetic to highlight the physics of the fastest path.
