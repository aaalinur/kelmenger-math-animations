from manim import *
import random
import numpy as np

# Vertical 9:16 configuration
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0a0b16"

COLOR_BG = "#0a0b16"
COLOR_WHITE = "#FFFFFF"


class ParallaxSpaceBackground(VGroup):
    """
    3-фон: Параллакс эффектісі бар динамикалық қозғалатын ғарыш фоны.
    3 түрлі қабаттағы жұлдыздар әртүрлі жылдамдықпен баяу төмен жылжиды.
    """
    def __init__(self, num_stars=80, **kwargs):
        super().__init__(**kwargs)
        self.time = 0

        # 1. Тұтас қою-көк фон
        bg_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=COLOR_BG,
            fill_opacity=1.0,
            stroke_width=0
        )
        self.add(bg_rect)

        # 2. Параллакс жұлдыздары (3 қабат)
        random.seed(303)
        self.stars_data = []
        stars_group = VGroup()

        for _ in range(num_stars):
            x = random.uniform(-config.frame_width / 2 + 0.2, config.frame_width / 2 - 0.2)
            y = random.uniform(-config.frame_height / 2, config.frame_height / 2)
            
            # Қабат таңдау: 1 (алыс/баяу), 2 (орташа), 3 (жақын/жылдам)
            layer = random.choice([1, 1, 2, 2, 3])
            
            if layer == 1:
                radius = random.uniform(0.010, 0.018)
                speed = random.uniform(0.2, 0.35)
                opacity = random.uniform(0.15, 0.35)
            elif layer == 2:
                radius = random.uniform(0.020, 0.032)
                speed = random.uniform(0.5, 0.8)
                opacity = random.uniform(0.40, 0.65)
            else:  # layer 3
                radius = random.uniform(0.035, 0.048)
                speed = random.uniform(1.0, 1.4)
                opacity = random.uniform(0.70, 0.90)

            star = Dot(point=[x, y, 0], radius=radius, color=COLOR_WHITE)
            star.set_opacity(opacity)
            stars_group.add(star)

            self.stars_data.append({
                "mob": star,
                "x": x,
                "start_y": y,
                "speed": speed
            })

        self.add(stars_group)
        self.add_updater(self.update_background)

    def update_background(self, mob, dt):
        self.time += dt
        h = config.frame_height
        half_h = h / 2.0

        # Жұлдыздардың үздіксіз төмен жылжуы (Шексіз loop)
        for data in self.stars_data:
            current_y = data["start_y"] - data["speed"] * self.time
            # Экранның төменгі шегінен асса, жоғарыдан қайта шығару
            wrapped_y = (current_y + half_h) % h - half_h
            data["mob"].move_to([data["x"], wrapped_y, 0])


class ParallaxSceneDemo(Scene):
    def construct(self):
        bg = ParallaxSpaceBackground(num_stars=80)
        self.add(bg)

        title = Text("Динамикалық Фон", font="Pliant", font_size=36, color=COLOR_WHITE)
        title.to_edge(UP, buff=2.0)
        
        subtitle = Text("Hook / Motion Effect", font="Fira Code", font_size=20, color="#00F0FF")
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(4.0)
        