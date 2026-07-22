# 🐸 Infinite Geometric Series Visual Proof (Reels Edition)

An interactive, vertical (9:16) **Manim animation** visualising the sum of an infinite geometric series through Zeno's Paradox and geometric square sub-division:

$$\sum_{n=1}^{\infty} \left(\frac{1}{2}\right)^n = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \dots = 1$$

Designed specifically for Instagram Reels, TikTok, and YouTube Shorts (`1080x1920`).


---

## 🎬 Watch the Final Reel

- 📲 **Instagram Reel:** [Watch on Instagram](https://www.instagram.com/p/DYSgtIXI5sa/)

---

## 📐 Content Highlights

1. **Zeno's Paradox (Frog Jump):** A visual animation of a frog hopping across half of the remaining distance at each step toward its destination.
2. **Algebraic Substitution:** Transforming $S = \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \dots$ into $S = \frac{1}{2} + \frac{1}{2}S$ to effortlessly solve for $S = 1$.
3. **Geometric Visual Proof:** Recursively splitting a unit square into halved sub-rectangles, demonstrating spatial convergence to $1$.
4. **Call To Action (CTA):** Encouraging audience interaction with a follow-up puzzle:
   $$\frac{1}{3} + \frac{1}{9} + \frac{1}{27} + \dots = ?$$

---

## 📂 File Requirements

Make sure the required SVG asset is present in the same directory before rendering:

- `geometric_series.py` (Main Manim code)
- `frog-svgrepo-com.svg` (Frog icon; falls back to a vector triangle if missing)

---

## 🎥 How to Render

To render the scene in standard vertical preview quality:

```bash
manim -pql geometric_series.py GeometricSeriesReels
```

For high-quality production export (1080x1920 @ 60 FPS):


```bash
manim -pqh geometric_series.py GeometricSeriesReels
```

