from manim import *
import numpy as np
import random

# Вертикаль формат (1080x1920)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class Loo(Scene):
    def construct(self):
        # Экран өңін ақ (немесе қалаған фоныңызға) орнату
        self.camera.background_color = "#E4D49E"

        # ------------------------------------------
        # 1. ТІКТӨРТБҰРЫШ (Ортаны бөлу) ЖӘНЕ А ЖӘНЕ B НҮКТЕЛЕРІ
        # ------------------------------------------
        medium_box = Rectangle(
            width=12, 
            height=3.5, 
            fill_color=BLUE_A, 
            fill_opacity=0.3, 
            stroke_color=BLUE_C
        ).move_to(DOWN * 1.75)

        # Жарық түсетін нүктелер
        pos_A = np.array([-3.5, 2.5, 0])
        pos_C = np.array([0, 0, 0])  # Сыну нүктесі
        pos_B = np.array([2.0, -3.0, 0])

        dot_A = Dot(pos_A, color=BLACK)
        dot_B = Dot(pos_B, color=BLACK)
        label_A = MathTex("A", color=BLACK).next_to(dot_A, UP)
        label_B = MathTex("B", color=BLACK).next_to(dot_B, DOWN)

        self.play(
            Create(medium_box),
            FadeIn(dot_A, label_A),
            FadeIn(dot_B, label_B),
            run_time=1.0
        )

        # ------------------------------------------
        # 2. A -> B ЖАРЫҚ ЖОЛЫ (СЫНУЫ)
        # ------------------------------------------
        ray_1 = Line(start=pos_A, end=pos_C, color=YELLOW_E, stroke_width=5)
        ray_2 = Line(start=pos_C, end=pos_B, color=YELLOW_E, stroke_width=5)
        light_path = VGroup(ray_1, ray_2)

        self.play(Create(light_path), run_time=1.2)

        # ------------------------------------------
        # 3. V1 > V2 ЖЫЛДАМДЫҚ САТЫСЫ
        # ------------------------------------------
        v_relation = MathTex("v_1 > v_2", color=BLACK).scale(1.2)
        v_text = Text("(Ауадағы жылдамдық жоғары)", font_size=20, color=BLACK)
        v_group = VGroup(v_relation, v_text).arrange(DOWN, buff=0.15)
        v_group.to_corner(UR, buff=0.8)

        self.play(Write(v_group), run_time=1.0)
        self.wait(1)

        # ------------------------------------------
        # 4. СНЕЛЛ ЗАҢЫ
        # ------------------------------------------
        snell_law = MathTex(
            "n_1 \\sin(\\theta_1) = n_2 \\sin(\\theta_2)", 
            color=BLACK
        ).scale(1.3)
        snell_law.move_to(UP * 0.5)

        self.play(Write(snell_law), run_time=1.2)
        self.wait(2)

        # ------------------------------------------
        # 5. БӘРІН ЖОЮ (FadeOut)
        # ------------------------------------------
        self.play(
            * [FadeOut(mob) for mob in self.mobjects],
            run_time=1.0
        )
        self.wait(0.5)

        # ------------------------------------------
        # 6. КІШІРЕЙТІЛГЕН FERMAT.JPG ЖӘНЕ ФЕРМА ПРИНЦИПІ
        # ------------------------------------------
        # Ферма суреті кішірейтілді (height = 3.2)
        fermat_img = ImageMobject("Fermat.jpg")
        fermat_img.height = 3.2
        fermat_img.to_edge(LEFT, buff=0.5)

        # Экран ортасында, сәл оң жақта Ферма принципінің жазылуы
        fermat_title = Text("Ферма принципі:", font_size=28, color=BLACK, weight=BOLD)
        
        # Қаріп өлшемі кішірейтілді (font_size = 20)
        fermat_text = Text(
            "Жарық бір нүктеден екінші нүктеге\n"
            "арақашықтығы ең қысқа емес,\n"
            "уақыты ең аз (ең жылдам) траекториямен таралады.",
            font_size=20,
            color=BLACK,
            line_spacing=0.8
        )
        
        text_group = VGroup(fermat_title, fermat_text).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        text_group.next_to(fermat_img, RIGHT, buff=0.4)

        self.play(
            FadeIn(fermat_img),
            Write(text_group),
            run_time=1.5
        )

        self.wait(3)