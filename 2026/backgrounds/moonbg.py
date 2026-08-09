from manim import *
import random
import numpy as np
import os

# Vertical 9:16 configuration
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0a0b16"

COLOR_WHITE = "#FFFFFF"


class MoonSpaceBackground(Group):  # VGroup орнына Group қолданамыз
    """
    2-фон: AI суреті (Ай беті) + Жылтылдайтын жұлдыздар + Аққан жұлдыз.
    """
    def __init__(self, image_path="moon_surface.png", num_stars=40, loop_time=4.0, **kwargs):
        super().__init__(**kwargs)
        self.loop_time = loop_time
        self.time = 0

        # 1. Суреттің бар-жоғын тексеру
        if os.path.exists(image_path):
            print(f"[SUCCESS] Сурет табылды: {image_path}")
            bg_image = ImageMobject(image_path)
            bg_image.height = config.frame_height
            bg_image.width = config.frame_width
            self.add(bg_image)
        else:
            print(f"[WARNING] Файл табылмады: {image_path}")
            print(f"Ағымдағы жұмыс папкасы: {os.getcwd()}")
            bg_rect = Rectangle(
                width=config.frame_width,
                height=config.frame_height,
                fill_color="#0a0b16",
                fill_opacity=1.0,
                stroke_width=0
            )
            self.add(bg_rect)

        # 2. Мәтін жақсы оқылуы үшін ортасын сәл күңгірттеу (Vignette layer)
        center_overlay = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color="#0a0b16",
            fill_opacity=0.35,
            stroke_width=0
        )
        self.add(center_overlay)

        # 3. Жылтылдайтын жұлдыздар
        random.seed(202)
        self.stars_data = []
        stars_group = VGroup()

        for _ in range(num_stars):
            x = random.uniform(-config.frame_width / 2 + 0.3, config.frame_width / 2 - 0.3)
            y = random.uniform(-2.0, config.frame_height / 2 - 0.3)
            
            radius = random.uniform(0.012, 0.025)
            base_opacity = random.uniform(0.15, 0.45)
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

        # 4. Аққан жұлдыз (Shooting Star)
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

        # Жұлдыздардың жұмсақ жылтылдауы
        for data in self.stars_data:
            val = np.sin(data["freq"] * tau + data["phase"])
            current_opacity = data["base_opacity"] + 0.20 * (val * 0.5 + 0.5)
            data["mob"].set_opacity(current_opacity)

        # Аққан жұлдыз анимациясы
        start_t = 1.0
        duration = 1.2
        
        if start_t <= t_cycle <= (start_t + duration):
            progress = (t_cycle - start_t) / duration
            
            cycle_count = int(self.time // self.loop_time)
            np.random.seed(cycle_count + 88)
            
            start_x = np.random.uniform(-3.5, 1.5)
            start_y = np.random.uniform(2.0, 6.5)
            angle = np.random.uniform(np.pi / 6, np.pi / 3)
            length = np.random.uniform(6.0, 8.0)
            
            direction = np.array([np.cos(angle), -np.sin(angle), 0])
            
            start_pos = np.array([start_x, start_y, 0]) + progress * direction * length
            end_pos = start_pos + direction * 0.8
            
            alpha = np.sin(np.pi * progress)
            
            self.shooting_star.put_start_and_end_on(start_pos, end_pos)
            self.shooting_star.set_stroke(opacity=alpha * 0.85)
        else:
            self.shooting_star.set_stroke(opacity=0)


class MoonSceneDemo(Scene):
    def construct(self):
        image_full_path = r"C:\Users\Azamat\Desktop\Ramanujan\moon_surface.png"
        
        bg = MoonSpaceBackground(image_path=image_full_path, loop_time=4.0)
        self.add(bg)

        title = Text("Nox Мекені", font="Pliant", font_size=36, color=COLOR_WHITE)
        title.to_edge(UP, buff=2.0)

        self.play(Write(title))
        self.wait(3.0)