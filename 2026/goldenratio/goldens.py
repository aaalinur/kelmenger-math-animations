import numpy as np
from manim import *
from background import SpaceBackground

# Вертикаль формат баптаулары (9:16)
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class GoldenShapesScene(Scene):
    def construct(self):
        # 1. Артқы фон
        bg = SpaceBackground(loop_time=4.0)
        self.add(bg)

        # Өзгертілген баптау параметрлері
        Golden = "#FFE600"
        ACCENT = "#FF007A"
        PHI = 1.618
        FONT = "Pliant"

        # =========================================================
        # 1. АЛТЫН ҮШБҰРЫШ (Golden Triangle)
        # =========================================================
        tri_title = Text("Алтын үшбұрыш", font_size=36, weight=BOLD, font=FONT).to_edge(UP, buff=2.0)
        
        tri_p1 = DOWN * 1.5 + LEFT * 1.0
        tri_p2 = DOWN * 1.5 + RIGHT * 1.0
        tri_p3 = UP * 1.736 + ORIGIN

        triangle = Polygon(tri_p1, tri_p2, tri_p3, color=WHITE, stroke_width=4)
        
        lbl_tri_base = MathTex("1", font_size=36, color=Golden).next_to(triangle, DOWN, buff=0.3)
        lbl_tri_side = MathTex("1.618", font_size=36, color=ACCENT).next_to(triangle, RIGHT, buff=0.1).shift(UP * 0.2)

        group_tri = VGroup(triangle, lbl_tri_base, lbl_tri_side)

        self.play(Write(tri_title), run_time=0.3)
        self.play(Create(triangle), Write(lbl_tri_base), Write(lbl_tri_side), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(group_tri), FadeOut(tri_title), run_time=0.3)

        # =========================================================
        # 2. АЛТЫН БЕСБҰРЫШ (Golden Pentagon)
        # =========================================================
        pent_title = Text("Алтын бесбұрыш", font_size=36, weight=BOLD, font=FONT).to_edge(UP, buff=2.0)
        
        pentagon = RegularPolygon(n=5, radius=2.2, color=WHITE, stroke_width=4).move_to(ORIGIN)
        pentagon.rotate(PI / 10)

        verts = pentagon.get_vertices()
        diagonal = Line(verts[1], verts[3], color=ACCENT, stroke_width=5)

        lbl_pent_side = MathTex("1", font_size=36, color=Golden).next_to(pentagon, DOWN, buff=0.3)
        lbl_pent_diag = MathTex("d = 1.618", font_size=36, color=ACCENT).next_to(diagonal, UP, buff=0.1)

        group_pent = VGroup(pentagon, diagonal, lbl_pent_side, lbl_pent_diag)

        self.play(Write(pent_title), run_time=0.3)
        self.play(Create(pentagon), run_time=0.5)
        self.play(Create(diagonal), Write(lbl_pent_side), Write(lbl_pent_diag), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(group_pent), FadeOut(pent_title), run_time=0.3)

        # =========================================================
        # 3. АЛТЫН СПИРАЛЬ (Үлкенірек әрі ұзынырақ)
        # =========================================================
        spiral_title = Text("Алтын спираль", font_size=36, weight=BOLD, font=FONT).to_edge(UP, buff=2.0)

        b = np.log(PHI) / (np.pi / 2)
        
        # t_range интервалын кеңейтіп, орамдарды көбейту (ұзынырақ)
        spiral = ParametricFunction(
            lambda t: np.array([
                0.05 * np.exp(b * t) * np.cos(t),
                0.05 * np.exp(b * t) * np.sin(t),
                0
            ]),
            t_range=[-4 * np.pi, 3.2 * np.pi],  # Тереңірек орамдар
            color=ACCENT,
            stroke_width=6
        )
        
        # Спиральді экранға сәйкестеп үлкейту (биіктігі 7.5 бірлік)
        spiral.scale_to_fit_height(7.5)
        spiral.move_to(ORIGIN)

        spiral_ratio = MathTex("\\phi = 1.618", font_size=54, color=Golden).next_to(spiral, DOWN, buff=0.6)

        # Анимация
        self.play(Write(spiral_title), run_time=0.3)
        self.play(Create(spiral), run_time=2.0)  # Ұзын спираль болғандықтан 2 сек созылады
        self.play(Write(spiral_ratio), run_time=0.5)

        self.wait(2.5)