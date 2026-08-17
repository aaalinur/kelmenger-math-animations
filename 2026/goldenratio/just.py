from manim import *
from background import SpaceBackground

# Вертикаль формат баптаулары (9:16)
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class JustScene(Scene):
    def construct(self):
        
        bg = SpaceBackground(loop_time=4.0)
        self.add(bg)
        
        self.wait(12.0)  