from manim import *
from moonbg import MoonSpaceBackground

# Vertical 9:16 configuration
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0a0b16"

class Conclusion(Scene):
    def construct(self):
        # 1. Фонды 1 жолмен шақыру
        bg = MoonSpaceBackground(loop_time=4.0)
        self.add(bg)

      
        self.wait(0.9)
      

        quote = Text("Пропорциясында сәл де болса \n оғаштығы жоқ бірде-бір \n мінсіз сұлулық болмайды.", font="Pliant", font_size=26.7, color="#FFFFFF")
        au = Text("Фрэнсис Бэкон", font="Pliant", font_size=17, color="#FFFFFF").move_to([2.3, -1.79, 0])

        self.play(Write(quote), run_time = 1.74)
        self.play(Write(au))          
        self.wait(4.3)
