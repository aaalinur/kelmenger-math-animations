from manim import *

# Reels форматын баптау (1080x1920 / 9:16)
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 16.0
config.frame_width = 9.0

class SumOfOddNumbersReels(Scene):
    def construct(self):
        # --- СТИЛЬ ЖӘНЕ ТҮСТЕР ---
        self.camera.background_color = "#0a0b16"
        primary_text = "#FFFFFF"
        accent_color = "#59C571"     # Жасыл түс
        secondary_color = "#C5A059"  # Алтын түс
        font_name = "Pliant"         # Немесе жүктелген қаріп аты

        # ==========================================
        # 1-БӨЛІМ: ИНДУКЦИЯ ЖӘНЕ АЛГЕБРАЛЫҚ СҰРАҚ
        # ==========================================
        text1 = Text("Сіз тақ сандардың мына бір\nерекше қасиетін көріп пе едіңіз?", font=font_name, font_size=30)
        
        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))
        
        eq1 = MathTex("1", "+", "3", "+", "5", "+", "...", "+", "(", "2n", "-", "1", ")", "=")
        eq2 = MathTex(r"n^2").next_to(eq1, DOWN, buff=0.5) 
        
        self.play(Write(eq1))
        self.play(FadeIn(eq2))
        self.wait(0.9)
        self.play(FadeOut(eq1, eq2))
        
        # Мысалдар (n = 1..4)
        n1 = MathTex("n", "=", "1", ": ", "1", "=", "1")
        n2 = MathTex("n", "=", "2", ": ", "1", "+", "3", "=", r"2^2").next_to(n1, DOWN, buff=0.2)
        n22 = MathTex("n", "=", "2", ": ", "4", "=", r"2^2").next_to(n1, DOWN, buff=0.2)
        n3 = MathTex("n", "=", "3", ": ", "1", "+", "3", "+", "5", "=", r"3^2").next_to(n2, DOWN, buff=0.2)
        n33 = MathTex("n", "=", "3", ": ", "9", "=", r"3^2").next_to(n2, DOWN, buff=0.2)
        n4 = MathTex("n", "=", "4", ": ", "1", "+", "3", "+", "5", "+", "7", "=", r"4^2").next_to(n3, DOWN, buff=0.2)
        n44 = MathTex("n", "=", "4", ": ", "16", "=", r"4^2").next_to(n3, DOWN, buff=0.2)
        dots = Text("...", font_size=40).next_to(n4, DOWN, buff=0.2)
        
        self.play(Write(n1), Write(n2), Write(n3), Write(n4), Write(dots))
        self.wait(1.5)
        self.play(Transform(n2, n22), Transform(n3, n33), Transform(n4, n44))
        self.wait(1.5)
        self.play(FadeOut(n1), FadeOut(n2), FadeOut(n3), FadeOut(n4), FadeOut(dots))
        
        # Индукциялық дәлелге көшу
        text_induction = Text("Математикалық индукция әдісі:", font=font_name, font_size=35).shift(UP*5)
        self.play(Create(text_induction))
        self.wait(0.3)
        
        kaku1 = MathTex("1)", " ", "n = 1", ":", " ", "1 = 1", color="#C5A059").next_to(text_induction, DOWN, buff=1.5)
        self.play(Write(kaku1))
        self.wait(0.3)
        
        kaku2 = MathTex("2)", " ", "n = k", ":", " ", "1 + 3 + ... + (2k-1) = k^2", color="#C5A059").next_to(kaku1, DOWN, buff=0.3)
        self.play(Write(kaku2))
        self.wait(0.3)
        
        kaku3 = MathTex("3)", " ", "n = k+1", ":", " ", "k^2 + (2k+1) = (k+1)^2", color="#C5A059").next_to(kaku2, DOWN, buff=0.5)
        self.play(Write(kaku3))
        
        proved_alg = Text("Алгебралық түрде дәлелденді!", color=accent_color, font=font_name, font_size=29).next_to(kaku3, DOWN, buff=1)
        self.play(Write(proved_alg))
        self.wait(2)
        
        self.play(FadeOut(text_induction, kaku1, kaku2, kaku3, proved_alg))

        # ==========================================
        # 2-БӨЛІМ: ГЕОМЕТРИЯЛЫҚ ВИЗУАЛДЫ ДӘЛЕП
        # ==========================================
        text_geom = Text("Геометриялық дәлелдеу:", font=font_name, font_size=39).shift(UP*5)
        self.play(Create(text_geom))
        self.wait(0.5)

        # 1 - Жылтыр орталық шаршы
        ola1_1 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=accent_color, stroke_color=primary_text, stroke_width=1).move_to([-2, -2, 0])
        ola1_1t = MathTex("1", "+", color=accent_color).next_to(ola1_1, DOWN)
        self.play(Create(ola1_1), Write(ola1_1t))
        self.wait(0.4)

        # 3 - Екінші қабат
        ola1_2 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#B74040", stroke_color=primary_text, stroke_width=1).move_to([-1, -2, 0])
        ola2_2 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#B74040", stroke_color=primary_text, stroke_width=1).move_to([-1, -1, 0])
        ola2_1 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#B74040", stroke_color=primary_text, stroke_width=1).move_to([-2, -1, 0])
        ola1_2t = MathTex("3", "+", color="#B74040").next_to(ola1_2, DOWN)
        self.play(Create(ola1_2), Write(ola1_2t), Create(ola2_2), Create(ola2_1))
        self.wait(0.4)

        # 5 - Үшінші қабат
        ola1_3 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#4058B7", stroke_color=primary_text, stroke_width=1).move_to([0, -2, 0])
        ola2_3 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#4058B7", stroke_color=primary_text, stroke_width=1).move_to([0, -1, 0])
        ola3_3 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#4058B7", stroke_color=primary_text, stroke_width=1).move_to([0, 0, 0])
        ola3_2 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#4058B7", stroke_color=primary_text, stroke_width=1).move_to([-1, 0, 0])
        ola3_1 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#4058B7", stroke_color=primary_text, stroke_width=1).move_to([-2, 0, 0])
        ola1_3t = MathTex("5", "+", color="#4058B7").next_to(ola1_3, DOWN)
        self.play(Write(ola1_3t), Create(ola1_3), Create(ola2_3), Create(ola3_3), Create(ola3_1), Create(ola3_2))
        self.wait(0.4)

        # 7 - Төртінші қабат
        ola1_4 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([1, -2, 0])
        ola2_4 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([1, -1, 0])
        ola3_4 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([1, 0, 0])
        ola4_4 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([1, 1, 0])
        ola4_3 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([0, 1, 0])
        ola4_2 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([-1, 1, 0])
        ola4_1 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color="#F33FF0", stroke_color=primary_text, stroke_width=1).move_to([-2, 1, 0])
        ola1_4t = MathTex("7", "+", color="#F33FF0").next_to(ola1_4, DOWN)
        self.play(Write(ola1_4t), Create(ola1_4), Create(ola2_4), Create(ola3_4), Create(ola4_4), Create(ola4_3), Create(ola4_2), Create(ola4_1))
        self.wait(0.4)

        # 9 - Бесінші қабат
        ola1_5 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([2, -2, 0])
        ola2_5 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([2, -1, 0])
        ola3_5 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([2, 0, 0])
        ola4_5 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([2, 1, 0])
        ola5_5 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([2, 2, 0])
        ola5_4 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([1, 2, 0])
        ola5_3 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([0, 2, 0])
        ola5_2 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([-1, 2, 0])
        ola5_1 = Rectangle(width=1, height=1, fill_opacity=0.7, fill_color=secondary_color, stroke_color=primary_text, stroke_width=1).move_to([-2, 2, 0])
        ola1_5t = MathTex("9", color=secondary_color).next_to(ola1_5, DOWN)

        self.play(Write(ola1_5t), Create(ola1_5), Create(ola2_5), Create(ola3_5), Create(ola4_5), Create(ola5_5), Create(ola5_4), Create(ola5_3), Create(ola5_2), Create(ola5_1))
        self.wait(0.5)

        # Қорытынды сөз
        text_conclusion = Text("Әр тақ сан қосылған сайын,\nшаршы өз пішінін сақтайды!", font=font_name, font_size=28, color=secondary_color).next_to(ola1_3, DOWN, buff=2)
        self.play(Write(text_conclusion), run_time=0.8)
        self.wait(3.0)
