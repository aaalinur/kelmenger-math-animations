from manim import *

# 1. РИЛС (9:16) ПАРАМЕТРЛЕРІ
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920

TexTemplateLibrary.default = TexTemplate(
    preamble=r"""
    \usepackage[english]{babel}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \usepackage{fontspec}
    \setmonofont{Fira Code}
    \usepackage[none]{hyphenat}
    """
)

class RamanujanReels(Scene):
    def construct(self):
        BG_COLOR = "#0a0b16"
        WHITE_COLOR = "#FFFFFF"

        self.camera.background_color = BG_COLOR

        # ----------------------------------------------------
        # 1. HOOK: Тақырып пен Басталғыш 3
        # ----------------------------------------------------
        title_text = Text(
            "Рамануджан жұмбағы", 
            font="Pliant", 
            font_size=42, 
            color=WHITE_COLOR
        )
        title_text.move_to(UP * 4.5)

        three_math = MathTex("3", font_size=120, color=WHITE_COLOR)
        three_math.move_to(UP * 1.5)

        self.play(Write(title_text), run_time=0.8)
        self.play(Write(three_math), run_time=0.6)
        self.wait(0.3)

        # ----------------------------------------------------
        # 2. ДӘЛЕЛДЕУ ҚАДАМДАРЫ (ДИНАМИКАЛЫҚ)
        # ----------------------------------------------------
        step1 = MathTex("n^2 = 1 + (n^2 - 1)", font_size=46, color=WHITE_COLOR)
        step1.move_to(DOWN * 0.5)

        step2 = MathTex("n^2 - 1 = (n - 1)(n + 1)", font_size=42, color=WHITE_COLOR)
        step2.next_to(step1, DOWN, buff=0.6)

        step3 = MathTex("n = \\sqrt{1 + (n - 1)(n + 1)}", font_size=44, color=WHITE_COLOR)
        step3.next_to(step2, DOWN, buff=0.6)

        self.play(Write(step1), run_time=0.7)
        self.play(Write(step2), run_time=0.7)
        self.play(
            ReplacementTransform(step1.copy(), step3),
            ReplacementTransform(step2.copy(), step3),
            run_time=0.9
        )
        self.wait(0.5)

        # Формулаларды тазалау
        self.play(
            FadeOut(step1),
            FadeOut(step2),
            step3.animate.move_to(UP * 1.5),
            FadeOut(three_math)
        )

        # ----------------------------------------------------
        # 3. ШЕКСІЗ ТЕРЕҢДЕУ АНИМАЦИЯСЫ (Climax)
        # ----------------------------------------------------
        # Қадам 1: 3 = sqrt(1 + 2 * 4)
        f1 = MathTex("3 = \\sqrt{1 + 2 \\cdot 4}", font_size=48, color=WHITE_COLOR)
        f1.move_to(DOWN * 0.5)
        self.play(Transform(step3, f1), run_time=0.8)
        self.wait(0.4)

        # Қадам 2: 4-ті ашу -> sqrt(1 + 3 * 5)
        f2 = MathTex("3 = \\sqrt{1 + 2\\sqrt{1 + 3 \\cdot 5}}", font_size=44, color=WHITE_COLOR)
        f2.move_to(DOWN * 0.5)
        self.play(
            Transform(step3, f2),
            Flash(f2, color=WHITE_COLOR, line_length=0.2, num_lines=10),
            run_time=0.8
        )
        self.wait(0.4)

        # Қадам 3: 5-ті ашу -> sqrt(1 + 4 * 6)
        f3 = MathTex("3 = \\sqrt{1 + 2\\sqrt{1 + 3\\sqrt{1 + 4 \\cdot 6}}}", font_size=40, color=WHITE_COLOR)
        f3.move_to(DOWN * 0.5)
        self.play(
            Transform(step3, f3),
            Flash(f3, color=WHITE_COLOR, line_length=0.2, num_lines=12),
            run_time=0.8
        )
        self.wait(0.4)

        # Қадам 4: Шексіздікке кететін Толық Өрнек
        f_infinity = MathTex("3 = \\sqrt{1 + 2\\sqrt{1 + 3\\sqrt{1 + \\dots}}}", font_size=46, color=WHITE_COLOR)
        f_infinity.move_to(DOWN * 0.5)

        self.play(
            Transform(step3, f_infinity),
            run_time=1.0
        )

        # ----------------------------------------------------
        # 4. СОҢҒЫ ЖАРҚЫРАҒАН ЭФФЕКТ (Loop-қа дайын)
        # ----------------------------------------------------
        # Барлық зарттарды ортаға жинап, үлкейтіп пульсация жасау
        self.play(
            FadeOut(title_text),
            step3.animate.scale(1.2).move_to(ORIGIN),
            run_time=1.0
        )
        
        # Энергия толқыны (Шексіздік сиқыры)
        self.play(
            Indicate(step3, scale_factor=1.1, color=WHITE_COLOR),
            Flash(step3, color=WHITE_COLOR, flash_radius=1.8, num_lines=20),
            run_time=1.5
        )
        self.wait(1.5)