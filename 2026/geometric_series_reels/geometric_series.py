from manim import *

# Рилс форматын баптау (1080x1920)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class GeometricSeriesReels(Scene):
    def construct(self): 
        # --- СТИЛЬ ЖӘНЕ ТҮСТЕР ---
        self.camera.background_color = "#0a0b16"
        
        primary_text = "#FFFFFF"
        accent_color = "#C5A059"  # Алтын түс
        font_name = "Cormorant Garamond"

        # 1. ТАСБАҚА СЕКІРУІ (SVG)
        line = Line(start=[-4, -3, 0], end=[4, -3, 0], color=primary_text)
        start_label = Text("Көлшік", font=font_name, font_size=30).next_to(line, LEFT, buff=0.2)
        end_label = Text("Құдық", font=font_name, font_size=30).next_to(line, RIGHT, buff=0.2)
        
        # SVG жүктеу
        try:
            turtle = SVGMobject("frog-svgrepo-com.svg")
            turtle.set_color(primary_text)
            turtle.scale(0.4)
            # Егер тасбақа солға қарап тұрса, төмендегіні активтендір:
            # turtle.flip(axis=UP) 
        except:
            turtle = Triangle(color=primary_text).scale(0.2).rotate(-90*DEGREES)
        
        turtle.move_to(line.get_start() + UP*0.5)

        self.play(Create(line), Write(start_label), Write(end_label))
        self.play(FadeIn(turtle))

        # Секіру анимациясы
        current_pos = line.get_start()
        step_size = 4.0 # Бірінші қадам
        
        for i in range(1, 6):
            # Секіру траекториясы (арка)
            arc = ArcBetweenPoints(
                current_pos + UP*0.5, 
                current_pos + RIGHT*step_size + UP*0.5, 
                radius=-step_size * 0.8
            )
            self.play(MoveAlongPath(turtle, arc), run_time=0.7, rate_func=smooth)
            current_pos += RIGHT*step_size
            step_size /= 2

        question_mark = Text("?", font=font_name, color=accent_color, font_size=72).next_to(turtle, UP, buff=0.5)
        self.play(Write(question_mark), turtle.animate.set_color(accent_color))
        self.wait(1.5)
        self.play(FadeOut(line, start_label, end_label, turtle, question_mark))

        # 2. МАТЕМАТИКАЛЫҚ ТЕҢДЕУ
        # MathTex-те Cormorant қаріпін қолдану үшін \text{} ішіне жазуға болады
        title = Text("Шексіз қосынды", font=font_name, font_size=40).shift(UP*4)
        self.play(Write(title))

        eq1 = MathTex("S", "=", "{1 \\over 2}", "+", "{1 \\over 4}", "+", "{1 \\over 8}", "+", "\\dots").scale(1.5)
        self.play(Write(eq1))
        self.wait(1)

        # Түрлендіру қадамдары
        eq2 = MathTex(
            "S", "=", "{1 \\over 2}", "+", "{1 \\over 2}", "(", "{1 \\over 2}", "+", "{1 \\over 4}", "+", "\\dots", ")"
        ).scale(1.5)
        
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        # Алтын түспен ерекшелеу (жақша ішіндегі бөлік - S)
        # Manim-де MathTex индекстері арқылы түс беру (6-дан 11-ге дейінгі символдар)
        self.play(eq2[6:11].animate.set_color(accent_color))
        
        brace = Brace(eq2[6:11], DOWN, color=accent_color)
        s_text = MathTex("S", color=accent_color).next_to(brace, DOWN)
        self.play(Create(brace), Write(s_text))
        self.wait(1.5)

        # Соңғы алгебра
        final_step = MathTex("S = {1 \\over 2} + {1 \\over 2} S").scale(1.5).shift(DOWN*2.5)
        result = MathTex("S = 1").scale(2).set_color(accent_color).shift(DOWN*4)

        self.play(Write(final_step))
        self.play(Write(result))
        self.wait(2)
        self.play(FadeOut(eq2, brace, s_text, final_step, result, title))

        # 3. ГЕОМЕТРИЯЛЫҚ ВИЗУАЛ (Шаршы)
        square_frame = Square(side_length=6, color=primary_text, stroke_width=2).move_to(ORIGIN)
        self.play(Create(square_frame))

        w, h = 6, 6
        anchor = square_frame.get_corner(DL)
        
        # 7 рет бөлу (рекурсия)
        for i in range(11):
            if i % 2 == 0: # Тігінен
                rect = Rectangle(width=w/2, height=h, fill_opacity=0.9, 
                                 fill_color=accent_color, stroke_color=primary_text, stroke_width=1)
                rect.move_to(anchor + RIGHT*(w/4) + UP*(h/2))
                anchor += RIGHT*(w/2)
                w /= 2
            else: # Көлденең
                rect = Rectangle(width=w, height=h/2, fill_opacity=0.9, 
                                 fill_color=accent_color, stroke_color=primary_text, stroke_width=1)
                rect.move_to(anchor + RIGHT*(w/2) + UP*(h/4))
                anchor += UP*(h/2)
                h /= 2
            self.play(FadeIn(rect), run_time=0.4)

        total_1 = Text("1", font=font_name, font_size=120).move_to(square_frame.get_center())
        self.play(Write(total_1))
        self.wait(2)
        self.play(FadeOut(total_1, square_frame), *[FadeOut(m) for m in self.mobjects])

        # 4. CALL TO ACTION
        cta_eq = MathTex("{1 \\over 3} + {1 \\over 9} + {1 \\over 27} + \\dots = ?").scale(1.8)
        cta_txt = Text("Жауабын комментарийге жаз", font=font_name, font_size=36).next_to(cta_eq, DOWN, buff=1.5)
        
        self.play(Write(cta_eq))
        self.play(FadeIn(cta_txt, shift=UP))
        self.wait(4)
