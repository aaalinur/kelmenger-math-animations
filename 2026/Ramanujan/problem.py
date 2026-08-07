from manim import *

# 1. РИЛС (9:16) ПАРАМЕТРЛЕРІ
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920

class RamanujanReels(Scene):
    def construct(self):
        BG_COLOR = "#0a0b16"
        WHITE_COLOR = "#FFFFFF"
        ACCENT_COLOR = "#00FFCC"  # Түйінді жауаптар үшін ашық циан түсі
        GOLD_COLOR = "#FFD700"    # Алмастыруларға арналған алтын түс

        self.camera.background_color = BG_COLOR
        
        # --- 1-БӨЛІМ: АРИФМЕТИКАЛЫҚ МЫСАЛ ---
        title_text = Text(
                    "Өрнек:", 
                    font="Pliant", 
                    font_size=42, 
                    color=WHITE_COLOR
                )
        title_text.move_to([-2, 4.5, 0])
        self.play(Write(title_text), run_time=0.8)
        
        self.wait(1)
        
        f_infinity = MathTex("\\sqrt{1 + 2\\sqrt{1 + 3\\sqrt{1 + \\dots}}} = ?", font_size=46, color=WHITE_COLOR).move_to(UP * 3.3)
        self.play(Write(f_infinity), run_time=0.8)
        
        self.wait(4)
        
        step_1 = MathTex("9 = 1 + 2 \\cdot 4", font_size=42, color=WHITE_COLOR).next_to(f_infinity, DOWN * 1.3)
        step_2 = MathTex("3 = \\sqrt{1 + 2 \\cdot 4}", font_size=42, color=WHITE_COLOR).next_to(step_1, DOWN * 1.3)
        step_3 = MathTex("3 = \\sqrt{1 + 2\\sqrt{1 + 3 \\cdot 5}}", font_size=42, color=WHITE_COLOR).next_to(step_2, DOWN * 1.3)
        step_4 = MathTex("3 = \\sqrt{1 + 2\\sqrt{1 + 3\\sqrt{1 + 4 \\cdot 6}}}", font_size=42, color=WHITE_COLOR).next_to(step_3, DOWN * 1.3)
        
        self.play(Write(step_1), run_time=0.6)
        self.wait(3)
        self.play(Write(step_2), run_time=0.6)
        self.wait(3)
        self.play(Write(step_3), run_time=0.6)
        self.wait(3)
        self.play(Write(step_4), run_time=0.6)
        self.wait(3)
                
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(1)
        
        # --- 2-БӨЛІМ: ЖАЛПЫ АЛГЕБРАЛЫҚ ДӘЛЕЛДЕУ ---
        
        proof_title = Text("Жалпы дәлелдеу:", font="Pliant", font_size=40, color=WHITE_COLOR)
        proof_title.move_to(UP * 6)
        self.play(Write(proof_title), run_time=0.8)

        # 1. Негізгі теңбе-теңдік
        proof_1 = MathTex("(n+1)^2 = n^2 + 2n + 1", font_size=40, color=WHITE_COLOR).next_to(proof_title, DOWN * 1.2)
        proof_1_alt = MathTex("(n+1)^2 = 1 + n(n+2)", font_size=40, color=WHITE_COLOR).move_to(proof_1.get_center())
        
        self.play(Write(proof_1), run_time=0.8)
        self.wait(2)
        # Алгебралық түрге түрлендіру
        self.play(Transform(proof_1, proof_1_alt), run_time=0.8)
        self.wait(2)

        # 2. Екі жағынан түбір алу
        proof_2 = MathTex("n+1 = \\sqrt{1 + n(n+2)}", font_size=40, color=WHITE_COLOR).next_to(proof_1, DOWN * 1.2)
        self.play(Write(proof_2), run_time=0.8)
        self.wait(2.5)

        # 3. (n+2) өрнегін дәл осы ережемен ашу
        sub_text = Text("Дәл олай (n+2)-ні ашсақ:", font="Pliant", font_size=30, color="#A0A0A0")
        sub_text.next_to(proof_2, DOWN * 1.2)
        
        proof_3 = MathTex("n+2 = \\sqrt{1 + (n+1)(n+3)}", font_size=38, color=GOLD_COLOR)
        proof_3.next_to(sub_text, DOWN * 0.6)
        
        self.play(Write(sub_text), Write(proof_3), run_time=1)
        self.wait(3)

        # 4. (n+2)-ні орнына қою
        proof_4 = MathTex(
            "n+1 = \\sqrt{1 + n\\sqrt{1 + (n+1)(n+3)}}", 
            font_size=36, 
            color=WHITE_COLOR
        ).next_to(proof_3, DOWN * 1.2)
        self.play(Write(proof_4), run_time=1)
        self.wait(3)

        # Кадрды тазалау және түйінді сәтке өту
        self.play(
            FadeOut(proof_title),
            FadeOut(proof_1),
            FadeOut(sub_text),
            FadeOut(proof_3),
            proof_2.animate.move_to(UP * 5),
            proof_4.animate.move_to(UP * 3.3),
            run_time=1
        )
        self.wait(0.5)

        # 5. Шексіз рекурсиялық өрнек
        final_gen = MathTex(
            "n+1 = \\sqrt{1 + n\\sqrt{1 + (n+1)\\sqrt{1 + \\dots}}}",
            font_size=35,
            color=WHITE_COLOR
        ).next_to(proof_4, DOWN * 1.3)
        self.play(Write(final_gen), run_time=1.2)
        self.wait(3)

        # 6. n = 2 мәнін қою (ТҮЗЕТІЛДІ: MathTex + Text байланыстырылды)
        n_math = MathTex("n = 2", font_size=38, color=GOLD_COLOR)
        n_txt = Text("болса:", font="Pliant", font_size=30, color=GOLD_COLOR)
        n_sub = VGroup(n_math, n_txt).arrange(RIGHT, buff=0.25).next_to(final_gen, DOWN * 1.4)
        
        self.play(Write(n_sub), run_time=0.8)
        self.wait(1.5)

        final_res = MathTex(
            "3 = \\sqrt{1 + 2\\sqrt{1 + 3\\sqrt{1 + 4\\dots}}}",
            font_size=38,
            color=ACCENT_COLOR
        ).next_to(n_sub, DOWN * 1.0)
        
        # Қорапшамен рамкаға алу
        box = SurroundingRectangle(final_res, color=ACCENT_COLOR, buff=0.25)
        self.play(Write(final_res), Create(box), run_time=1.2)
        
        self.wait(4)