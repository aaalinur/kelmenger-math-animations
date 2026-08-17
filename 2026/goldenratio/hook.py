from manim import *
from dynbg import ParallaxSpaceBackground

# Вертикаль формат баптаулары (9:16)
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class AspectRatioScene(Scene):
    def construct(self):
        
        bg = ParallaxSpaceBackground()
        self.add(bg)

        # -------------------------------------------------------------
        # 1. Төртбұрыштар мен әріптерді құрастыру (Кішірейтілген & Көлденең)
        # -------------------------------------------------------------
        
        # А нұсқасы: Квадратқа жақын (Көлденең: 1.8 x 1.6)
        rect_a = Rectangle(width=1.8, height=1.6, color=WHITE, stroke_width=4)
        
        # B нұсқасы: Көлденең Алтын пропорция (1.618 : 1 -> 2.2 x 1.36)
        rect_b = Rectangle(width=2.2, height=1.36, color=WHITE, stroke_width=4)
        
        # C нұсқасы: Ені қысқалау / жіңішке (1.1 x 2.2)
        rect_c = Rectangle(width=1.1, height=2.2, color=WHITE, stroke_width=4)

        # Төртбұрыштарды ортасы бойынша түзу қатарға тиімді орналастыру
        rects = VGroup(rect_a, rect_b, rect_c).arrange(RIGHT, buff=0.5)

        # Әріптерді әр төртбұрыштың астына белгіленген қашықтықта қою
        label_a = Text("A", font_size=32, weight=BOLD).next_to(rect_a, DOWN, buff=0.3)
        label_b = Text("B", font_size=32, weight=BOLD).next_to(rect_b, DOWN, buff=0.3)
        label_c = Text("C", font_size=32, weight=BOLD).next_to(rect_c, DOWN, buff=0.3)

        group_a = VGroup(rect_a, label_a)
        group_b = VGroup(rect_b, label_b)
        group_c = VGroup(rect_c, label_c)

        # Барлық топты экранның дәл ортасына жылжыту
        all_options = VGroup(group_a, group_b, group_c).move_to(ORIGIN)

        # -------------------------------------------------------------
        # 2. Анимациялар
        # -------------------------------------------------------------
        
        # 1-қадам: Үш нұсқаның экранға шығуы
        self.play(
            FadeIn(group_a, shift=UP * 0.5),
            FadeIn(group_b, shift=UP * 0.5),
            FadeIn(group_c, shift=UP * 0.5),
            run_time=1.5
        )

        # 2-қадам: 3 секунд күту (Self wait 3)
        self.wait(3)

        # 3-қадам: Ортадағы (B) төртбұрышты акцентті түспен қоршау
        ACCENT_COLOR = "#FFE600"

        highlight_box = rect_b.copy()
        highlight_box.set_stroke(color=ACCENT_COLOR, width=8)

        # Анимация: Контур сызылады және әріп түсі өзгереді
        self.play(
            Create(highlight_box),
            label_b.animate.set_color(ACCENT_COLOR),
            run_time=1.0
        )
        
        # Нәтижені көрсетіп тұру
        self.wait(2)