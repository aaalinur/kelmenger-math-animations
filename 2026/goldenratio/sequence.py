from manim import *
from background import SpaceBackground

# Вертикаль формат баптаулары (9:16)
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class FibonacciRhythmScene(Scene):
    def construct(self):
        # 1. Артқы фон
        bg = SpaceBackground(loop_time=4.0)
        self.add(bg)

        # -------------------------------------------------------------
        # 2. Сандар қатарын құрастыру (Фибоначчи)
        # -------------------------------------------------------------
        # Сандарды ырғақпен жеке-жеке шығару үшін бөлек элемент ретінде береміз
        sequence = MathTex(
            "1,", "1,", "2,", "3,", "5,", "8,", "13,", "\\dots",
            font_size=56
        )
        sequence.move_to(UP * 1.5)

        # -------------------------------------------------------------
        # 3. Анимация: Сандардың ырғақпен (екпінмен) шығуы
        # -------------------------------------------------------------
        # Әр сан сәл үлкейіп (scale=1.4), ырғақты түрде пайда болады
        for item in sequence:
            self.play(
                FadeIn(item, scale=1.4),
                run_time=0.25
            )
            self.wait(0.1)  # Ырғақ арасындағы қысқа пауза

        self.wait(1.0)

        # -------------------------------------------------------------
        # 4. Формула / Алтын қатыс (1 : 1.618)
        # -------------------------------------------------------------
        ACCENT_COLOR = "#FFE600"

        # 1:1.618 формуласы
        ratio_formula = MathTex("1 : 1.618", font_size=80, color=ACCENT_COLOR)
        ratio_formula.next_to(sequence, DOWN, buff=1.5)

        # Формула айналасындағы акцентті рамка
        box = SurroundingRectangle(
            ratio_formula, 
            color=ACCENT_COLOR, 
            buff=0.3, 
            corner_radius=0.2,
            stroke_width=6
        )

        # Формуланың жазылуы және рамканың пайда болуы
        self.play(
            Write(ratio_formula),
            run_time=1.0
        )
        self.play(
            Create(box),
            run_time=0.8
        )

        # Нәтижені көрсетіп тұру үшін соңында 3 секунд күту
        self.wait(3)