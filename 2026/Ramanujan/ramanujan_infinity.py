from manim import *
import numpy as np

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920

class RamanujanWaveScroll(Scene):
    def construct(self):
        BG_COLOR = "#0A0B16"
        WHITE_COLOR = "#FFFFFF"
        ACCENT_COLOR = "#00FFCC"
        GOLD_COLOR = "#FFD700"

        self.camera.background_color = BG_COLOR

        terms_count = 21
        latex_str = "3 = "
        open_braces = 0

        for i in range(2, terms_count + 1):
            latex_str += f"\\sqrt{{1 + {i}"
            open_braces += 1

        latex_str += "\\sqrt{1 + \\dots}"
        open_braces += 1
        latex_str += "}" * open_braces

        long_expr = MathTex(latex_str, font_size=44, color=WHITE_COLOR)
        long_expr.move_to(ORIGIN)

        focus_box = RoundedRectangle(
            corner_radius=0.2, 
            height=2.8, 
            width=8.0, 
            color=ACCENT_COLOR, 
            stroke_width=3
        ).move_to(ORIGIN)

        long_expr.align_to(focus_box, LEFT)
        long_expr.shift(RIGHT * 0.5)

        self.play(FadeIn(long_expr, shift=RIGHT * 0.5), run_time=0.8)
        self.wait(0.5)

        start_x = long_expr.get_x()
        start_y = long_expr.get_y()
        shift_total = long_expr.width - 3.5

        amplitude = 0.45
        frequency = 6 * TAU

        def wave_update(mob, alpha):
            cur_x = start_x - alpha * shift_total
            cur_y = start_y + amplitude * np.sin(alpha * frequency)
            mob.move_to([cur_x, cur_y, 0])

        self.play(
            UpdateFromAlphaFunc(long_expr, wave_update),
            run_time=15,
            rate_func=linear
        )
        self.wait(1.0)

        self.play(
            FadeOut(long_expr),
            FadeOut(focus_box),
            run_time=0.8
        )

        final_formula = MathTex(
            "\\lim_{n \\to \\infty} \\sqrt{1 + 2\\sqrt{1 + 3\\sqrt{\\dots + n\\sqrt{1 + (n+1)}}}} = 3",
            font_size=38,
            color=ACCENT_COLOR
        ).move_to(ORIGIN)

        final_box = SurroundingRectangle(final_formula, color=GOLD_COLOR, buff=0.3, stroke_width=2.5)

        self.play(Write(final_formula), Create(final_box), run_time=1.2)
        self.wait(3.0)