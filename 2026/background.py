from manim import *
import random
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0a0b16"

COLOR_BG = "#0a0b16"
COLOR_WHITE = "#FFFFFF"


class SpaceBackground(VGroup):

    def __init__(self, num_stars=65, loop_time=4.0, **kwargs):
        super().__init__(**kwargs)
        self.loop_time = loop_time
        self.time = 0

        bg_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=COLOR_BG,
            fill_opacity=1.0,
            stroke_width=0
        )
        self.add(bg_rect)

        grid = NumberPlane(
            x_range=[-5, 5, 0.5],
            y_range=[-9, 9, 0.5],
            background_line_style={
                "stroke_color": COLOR_WHITE,
                "stroke_width": 0.6,
                "stroke_opacity": 0.08,
            },
            axis_config={
                "stroke_color": COLOR_WHITE,
                "stroke_width": 0.6,
                "stroke_opacity": 0.08,
                "include_ticks": False,
            }
        )
        self.add(grid)

        random.seed(101) 
        self.stars_data = []
        stars_group = VGroup()

        for _ in range(num_stars):
            x = random.uniform(-config.frame_width / 2 + 0.2, config.frame_width / 2 - 0.2)
            y = random.uniform(-config.frame_height / 2 + 0.2, config.frame_height / 2 - 0.2)
            radius = random.uniform(0.012, 0.028)
            base_opacity = random.uniform(0.10, 0.30)
            freq = random.choice([1, 2, 3])
            phase = random.uniform(0, 2 * np.pi)

            star = Dot(point=[x, y, 0], radius=radius, color=COLOR_WHITE)
            star.set_opacity(base_opacity)
            stars_group.add(star)
            
            self.stars_data.append({
                "mob": star,
                "base_opacity": base_opacity,
                "freq": freq,
                "phase": phase
            })

        self.add(stars_group)

        self.shooting_star = Line(
            start=ORIGIN,
            end=RIGHT * 0.7 + DOWN * 0.7,
            stroke_color=COLOR_WHITE,
            stroke_width=1.5,
            stroke_opacity=0
        )
        self.add(self.shooting_star)

        self.add_updater(self.update_background)

    def update_background(self, mob, dt):
        self.time += dt
        t_cycle = self.time % self.loop_time
        tau = 2 * np.pi * t_cycle / self.loop_time

        for data in self.stars_data:
            val = np.sin(data["freq"] * tau + data["phase"])
            current_opacity = data["base_opacity"] + 0.25 * (val * 0.5 + 0.5)
            data["mob"].set_opacity(current_opacity)

        start_t = 1.0
        duration = 1.2
        
        if start_t <= t_cycle <= (start_t + duration):
            progress = (t_cycle - start_t) / duration
            cycle_count = int(self.time // self.loop_time)
            np.random.seed(cycle_count + 42)
            start_x = np.random.uniform(-4.0, 2.0)
            start_y = np.random.uniform(3.0, 7.0)
            angle = np.random.uniform(np.pi / 6, np.pi / 3)  
            length = np.random.uniform(7.0, 10.0)
            direction = np.array([np.cos(angle), -np.sin(angle), 0])
            start_pos = np.array([start_x, start_y, 0]) + progress * direction * length
            end_pos = start_pos + direction * 0.8
            alpha = np.sin(np.pi * progress)
            self.shooting_star.put_start_and_end_on(start_pos, end_pos)
            self.shooting_star.set_stroke(opacity=alpha * 0.8)
        else:
            self.shooting_star.set_stroke(opacity=0)

       # bg = SpaceBackground(loop_time=4.0)
       # self.add(bg)
       

'''
from manim import *
from background import SpaceBackground  # background.py файлынан класты импорттау

# Vertical 9:16 configuration
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0a0b16"

class MainScene(Scene):
    def construct(self):
        # 1. Фонды 1 жолмен шақыру
        bg = SpaceBackground(loop_time=4.0)
        self.add(bg)

        # 2. Сенің негізгі контентің
        title = Text("Жаңа Видео", font="Pliant", font_size=40, color="#FFFFFF")
        self.play(Write(title))
        self.wait(2)
        '''
