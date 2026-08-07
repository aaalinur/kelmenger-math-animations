from manim import *
import random

class PrimeOneConceptVertical(Scene):
    def construct(self):
        # 0. Баптаулар мен стильдер
        self.camera.background_color = "#0a0b16"
        
        # Шрифттер
        MAIN_FONT = "Pliant"
        CODE_FONT = "Fira Code"

        # ------------------------------------------------------------------
        # 1-БЛОК: "Сандардан үйшік құрау" (Арифметиканың Негізгі Теоремасы)
        # ------------------------------------------------------------------
        
        # Төменгі жақтағы жай сандар кірпіштері (2, 3, 5, 7) - Вертикаль форматта кішірейтілген
        prime_nums = [2, 3, 5, 7]
        prime_boxes = VGroup()
        for num in prime_nums:
            box = Square(side_length=0.9, stroke_color=WHITE, stroke_width=2)
            label = Text(str(num), font=CODE_FONT, color=WHITE, font_size=26)
            single_prime = VGroup(box, label)
            prime_boxes.add(single_prime)
        
        prime_boxes.arrange(RIGHT, buff=0.35)
        prime_boxes.move_to(DOWN * 2.8)

        # Төменгі панель тақырыбы
        primes_title = Text("Жай сандар (кірпіштер)", font=MAIN_FONT, color=WHITE, font_size=20)
        primes_title.next_to(prime_boxes, UP, buff=0.25)

        self.play(Write(primes_title), FadeIn(prime_boxes, shift=UP))
        self.wait(0.3)

        # "6" санының сұлбасы (жоғарыда)
        target_box_6 = RoundedRectangle(corner_radius=0.15, height=1.3, width=2.0, stroke_color=WHITE, stroke_width=2)
        target_box_6.move_to(UP * 2.0)
        label_6 = Text("6", font=MAIN_FONT, color=WHITE, font_size=36).next_to(target_box_6, UP, buff=0.2)
        
        self.play(Create(target_box_6), Write(label_6))

        # 2 және 3 кубиктерінің көшірмесін алып, 6-ның ішіне біріктіру
        b2_copy = prime_boxes[0].copy()
        b3_copy = prime_boxes[1].copy()

        target_pos_2 = target_box_6.get_center() + LEFT * 0.35
        target_pos_3 = target_box_6.get_center() + RIGHT * 0.35

        self.play(
            b2_copy.animate.move_to(target_pos_2).scale(0.75),
            b3_copy.animate.move_to(target_pos_3).scale(0.75),
            run_time=1.2
        )
        
        mult_sign = Text("×", font=CODE_FONT, color=WHITE, font_size=24).move_to(target_box_6.get_center())
        self.play(Write(mult_sign))
        self.wait(0.8)

        # 1-блокты тазалау
        block1_group = VGroup(primes_title, prime_boxes, target_box_6, label_6, b2_copy, b3_copy, mult_sign)
        self.play(FadeOut(block1_group))

        # ------------------------------------------------------------------
        # 2-БЛОК: "Жалғыздық принципі" (Unique Factorization)
        # ------------------------------------------------------------------

        # 30 = 2 × 3 × 5 формуласы (вертикальға лайық шрифт өлшемі)
        eq_30 = MathTex("30", "=", "2", "\\times", "3", "\\times", "5", font_size=44)
        eq_30.set_color(WHITE)
        eq_30.move_to(UP * 1.8)
        
        self.play(Write(eq_30))
        self.wait(0.4)

        # Басқа комбинацияның "кіргісі келуі" (2 × 13)
        wrong_combo = Text("2 × 13 ?", font=CODE_FONT, color=WHITE, font_size=32)
        wrong_combo.move_to(ORIGIN)

        self.play(FadeIn(wrong_combo, shift=UP))
        self.wait(0.3)
        
        # Кіре алмай, кейін серпіліп "жоқ" (X) болуы
        cross = Cross(wrong_combo, stroke_color=WHITE, stroke_width=3.5)
        self.play(Create(cross))
        self.play(
            wrong_combo.animate.shift(DOWN * 0.5),
            cross.animate.shift(DOWN * 0.5),
            rate_func=wiggle
        )
        self.wait(0.4)

        # Төменнен "Жалғыз жіктеу!" мәтіні
        unique_text = Text("ЖАЛҒЫЗ ҒАНА ЖІКТЕУ!", font=MAIN_FONT, color=WHITE, font_size=26)
        unique_text.move_to(DOWN * 2.2)
        
        self.play(Write(unique_text))
        self.wait(1.2)

        # 2-блокты тазалау
        block2_group = VGroup(eq_30, wrong_combo, cross, unique_text)
        self.play(FadeOut(block2_group))

        # ------------------------------------------------------------------
        # 3-БЛОК: "Хаос және Шексіздік" (Егер 1 жай сан болса...)
        # ------------------------------------------------------------------

        # Қайтадан 6 = 2 × 3
        base_6 = MathTex("6 =", "2", "\\times", "3", font_size=42).move_to(UP * 2.5)
        self.play(Write(base_6))
        self.wait(0.4)

        # 1-лердің қосылуымен формуланың ұзаруы (кішірек шрифт)
        eq_step1 = MathTex("6 =", "2", "\\times", "3", "\\times", "1", font_size=38).move_to(UP * 2.5)
        eq_step2 = MathTex("6 =", "2", "\\times", "3", "\\times", "1", "\\times", "1", font_size=34).move_to(UP * 2.5)
        eq_step3 = MathTex("6 =", "2", "\\times", "3", "\\times", "1", "\\times", "1", "\\times", "1", "\\dots", font_size=30).move_to(UP * 2.5)

        self.play(Transform(base_6, eq_step1))
        self.wait(0.25)
        self.play(Transform(base_6, eq_step2))
        self.wait(0.25)
        self.play(Transform(base_6, eq_step3))
        self.wait(0.4)

        # 9:16 тар экранында хаос жасау (координаталар X: [-2.2, 2.2], Y: [-3.5, 1.0])
        ones_chaos = VGroup()
        random.seed(42)

        for _ in range(22):
            x = random.uniform(-2.2, 2.2)
            y = random.uniform(-3.5, 1.0)
            
            box_1 = Square(side_length=0.55, stroke_color=WHITE, stroke_width=1.2)
            text_1 = Text("1", font=CODE_FONT, color=WHITE, font_size=16)
            unit = VGroup(box_1, text_1).move_to([x, y, 0])
            ones_chaos.add(unit)

        self.play(LaggedStartMap(FadeIn, ones_chaos, run_time=1.2, lag_ratio=0.04))
        self.wait(0.8)

        # Тәртіпке келтіру
        clean_6 = MathTex("6 =", "2", "\\times", "3", font_size=46).move_to(UP * 0.5)
        
        self.play(
            FadeOut(ones_chaos),
            FadeOut(base_6),
            run_time=0.8
        )
        
        self.play(Write(clean_6))
        
        # "1" санын бөлек "Бірлік" етіп көрсету
        unit_box = Square(side_length=0.85, stroke_color=WHITE, stroke_width=2).move_to(DOWN * 1.8)
        unit_label = Text("1", font=CODE_FONT, color=WHITE, font_size=24).move_to(unit_box.get_center())
        unit_text = Text("Бірлік сан (Unit)", font=MAIN_FONT, color=WHITE, font_size=20).next_to(unit_box, DOWN, buff=0.2)
        
        final_unit_group = VGroup(unit_box, unit_label, unit_text)
        self.play(FadeIn(final_unit_group, shift=UP))
        self.wait(1.5)

        # Тазалау
        self.play(FadeOut(clean_6), FadeOut(final_unit_group))
