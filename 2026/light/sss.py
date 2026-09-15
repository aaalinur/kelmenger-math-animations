from manim import *
import numpy as np
import random

# Вертикаль формат (1080x1920)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class Light(Scene):
    def construct(self):
        # 1. Фон (Сары/құм түс)
        self.camera.background_color = "#E4D49E"

        # Палитра (айқын көрінетін түстер)
        COLOR_ARROW_1 = "#FF5252"    # 1-бөлімдегі жебелерге арналған қанық қызыл-сары
        COLOR_LINE_AB = "#6C5CE7"     # A-B кесіндісіне арналған қанық күлгін/индиго
        COLOR_HIGHLIGHT = "#00CEC9"   # Акценттік ашық лазурь түс
        COLOR_SEA = "#1E88E5"         # Теңіз түсі
        COLOR_PATH = "#FF5252"        # 5-бөлімдегі A-B түзуі

        # ==========================================
        # 1-БӨЛІМ: АСАН ЖӘНЕ ҮСЕН (ТАС ЛАҚТЫРУ)
        # ==========================================
        asan = ImageMobject("asan.walk.png")
        usen = ImageMobject("usen.walk.png")

        asan.height = 1.2
        usen.height = 1.2

        characters = Group(asan, usen).arrange(RIGHT, buff=0.5)
        characters.rotate(90 * DEGREES)
        characters.move_to(LEFT * 2.2 + UP * 3.5)

        self.play(FadeIn(characters), run_time=1.0)

        # SVG Тас (Оригинал түсі сақталады)
        rock = SVGMobject("rock-svgrepo-com.svg")
        rock.height = 0.35
        
        start_pos = asan.get_center() + RIGHT * 0.4 + DOWN * 0.1
        flight_distance = 4.5
        end_pos = start_pos + RIGHT * flight_distance

        rock.move_to(start_pos)
        self.play(FadeIn(rock), run_time=0.3)

        # Тастың ұшу анимациясы
        base_scale = rock.height

        def update_rock_flight(mob, alpha):
            current_pos = interpolate(start_pos, end_pos, alpha)
            mob.move_to(current_pos)
            scale_factor = 1.0 + 0.8 * np.sin(np.pi * alpha)
            mob.set_height(base_scale * scale_factor)

        self.play(
            UpdateFromAlphaFunc(rock, update_rock_flight),
            run_time=1.2,
            rate_func=linear
        )

        arrow_asan = Arrow(
            start=asan.get_right(),
            end=rock.get_center(),
            color=COLOR_ARROW_1,
            buff=0.15,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15
        )

        arrow_usen = Arrow(
            start=usen.get_right(),
            end=rock.get_center(),
            color=COLOR_ARROW_1,
            buff=0.15,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15
        )

        self.play(
            Create(arrow_asan),
            Create(arrow_usen),
            run_time=1.2
        )

        tmin_1 = MathTex("t = \\min", color=BLACK)
        tmin_1.scale(1.2)
        tmin_1.next_to(Group(arrow_asan, arrow_usen, rock), DOWN, buff=0.6)

        self.play(Write(tmin_1), run_time=0.8)
        self.wait(1)

        self.play(
            FadeOut(Group(characters, rock, arrow_asan, arrow_usen, tmin_1)),
            run_time=1.0
        )
        self.wait(0.5)

        # ==========================================
        # 2-БӨЛІМ: A ЖӘНЕ B НҮКТЕЛЕРІ
        # ==========================================
        point_A = Dot(point=LEFT * 2.5, color=BLACK, radius=0.12)
        label_A = MathTex("A", color=BLACK).next_to(point_A, LEFT, buff=0.2)

        point_B = Dot(point=RIGHT * 2.5, color=BLACK, radius=0.12)
        label_B = MathTex("B", color=BLACK).next_to(point_B, RIGHT, buff=0.2)

        node_A = VGroup(point_A, label_A)
        node_B = VGroup(point_B, label_B)

        self.play(
            FadeIn(node_A),
            FadeIn(node_B),
            run_time=0.8
        )

        arrow_AB = Arrow(
            start=point_A.get_center(),
            end=point_B.get_center(),
            color=COLOR_LINE_AB,
            buff=0.15,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )

        self.play(Create(arrow_AB), run_time=1.0)

        tmin_2 = MathTex("t = \\min", color=BLACK)
        tmin_2.scale(1.2)
        tmin_2.next_to(arrow_AB, DOWN, buff=0.5)

        self.play(Write(tmin_2), run_time=0.8)

        self.wait(1.5)
        self.play(
            FadeOut(Group(node_A, node_B, arrow_AB, tmin_2)),
            run_time=1.0
        )
        self.wait(0.5)

        # ==========================================
        # 3-БӨЛІМ: ТЕҢІЗ ЖӘНЕ АСАН-ҮСЕНДІ ОРНАЛАСТЫРУ
        # ==========================================
        def get_sea_polygon(time_val):
            points = [np.array([-config.frame_width/2 - 0.5, -config.frame_height/2 - 0.5, 0])]
            x_range = np.linspace(-config.frame_width/2 - 0.5, config.frame_width/2 + 0.5, 80)
            
            for x in x_range:
                y = 0.12 * np.sin(2.0 * x + time_val * 2.0) + 0.08 * np.cos(3.0 * x - time_val * 1.5)
                points.append(np.array([x, y, 0]))

            points.append(np.array([config.frame_width/2 + 0.5, -config.frame_height/2 - 0.5, 0]))

            return Polygon(
                *points,
                fill_color=COLOR_SEA,
                fill_opacity=0.88,
                stroke_color=COLOR_SEA,
                stroke_width=1
            )

        num_foam_waves = 6
        random.seed(42)
        foam_data = [
            {"phase": i * (1.0 / num_foam_waves), "speed": 0.20 + random.uniform(-0.02, 0.02)}
            for i in range(num_foam_waves)
        ]

        def get_foam_wave(y_pos, opacity):
            x_range = np.linspace(-config.frame_width/2 - 0.5, config.frame_width/2 + 0.5, 80)
            points = [np.array([x, y_pos + 0.04 * np.sin(7.0 * x), 0]) for x in x_range]
            
            wave_line = VMobject()
            wave_line.set_points_smoothly(points)
            wave_line.set_stroke(color=WHITE, width=1.8, opacity=opacity)
            return wave_line

        sea = get_sea_polygon(0.0)
        foam_group = VGroup(*[get_foam_wave(-8.0, 0) for _ in range(num_foam_waves)])

        full_sea_group = VGroup(sea, foam_group)
        
        shift_amount = config.frame_height / 2 + 1.0
        full_sea_group.shift(DOWN * shift_amount)

        self.play(
            full_sea_group.animate.shift(UP * shift_amount),
            run_time=1.8,
            rate_func=rate_functions.ease_out_cubic
        )

        def global_sea_update(mob, dt):
            mob.time += dt

            new_sea = get_sea_polygon(mob.time)
            sea.become(new_sea)

            y_start = -config.frame_height / 2
            y_end = 0.0

            for i, data in enumerate(foam_data):
                progress = (mob.time * data["speed"] + data["phase"]) % 1.0
                current_y = interpolate(y_start, y_end, progress)

                if progress < 0.7:
                    opacity = interpolate(0.1, 0.6, progress / 0.7)
                else:
                    opacity = interpolate(0.6, 0.0, (progress - 0.7) / 0.3)

                updated_foam = get_foam_wave(current_y, opacity)
                foam_group[i].become(updated_foam)

        sea.time = 0
        sea.add_updater(global_sea_update)

        # ------------------------------------------
        # АСАН МЕН ҮСЕНДІ ЖАҒАЛАУҒА ҚОЙУ
        # ------------------------------------------
        asan_shore = ImageMobject("asan.walk.png")
        usen_shore = ImageMobject("usen.walk.png")

        asan_shore.height = 1.1
        usen_shore.height = 1.1

        shore_characters = Group(asan_shore, usen_shore).arrange(RIGHT, buff=0.4)
        shore_characters.rotate(35 * DEGREES)
        shore_characters.move_to(LEFT * 2.0 + UP * 2.2)

        self.play(
            FadeIn(shore_characters, shift=DOWN * 0.2),
            run_time=1.0
        )

        self.wait(1)
        
        # ==========================================
        # 4-БӨЛІМ: ТАС ЛАҚТЫРУ, A/B НҮКТЕЛЕРІЖӘНЕ ҚОЗҒАЛЫС
        # ==========================================
        usen_pos = usen_shore.get_center() + RIGHT * 0.2 + UP * 0.1
        start_pos_sea = usen_pos
        end_pos_sea = RIGHT * 2.2 + DOWN * 2.5 

        # SVG Тас (Оригинал түсі сақталады)
        sea_rock = SVGMobject("rock-svgrepo-com.svg")
        sea_rock.height = 0.3
        sea_rock.move_to(start_pos_sea)

        self.play(FadeIn(sea_rock), run_time=0.3)

        rock_base_scale = sea_rock.height

        def update_sea_rock_flight(mob, alpha):
            current_pos = interpolate(start_pos_sea, end_pos_sea, alpha)
            arc_height = 1.2 * np.sin(np.pi * alpha)
            mob.move_to(current_pos + UP * arc_height)
            
            scale_factor = 1.0 + 0.6 * np.sin(np.pi * alpha)
            mob.set_height(rock_base_scale * scale_factor)

        self.play(
            UpdateFromAlphaFunc(sea_rock, update_sea_rock_flight),
            run_time=1.3,
            rate_func=linear
        )

        self.play(
            sea_rock.animate.scale(0.1).set_opacity(0),
            run_time=0.2
        )

        # ДӨҢГЕЛЕК ТОЛҚЫНДАР
        num_ripples = 3
        ripples = VGroup(*[
            Circle(radius=0.1, color=WHITE, stroke_width=2.5, stroke_opacity=0.9)
            .move_to(end_pos_sea)
            for _ in range(num_ripples)
        ])

        self.add(ripples)

        def animate_ripple(circle, delay):
            return AnimationGroup(
                Wait(delay),
                circle.animate(run_time=1.0, rate_func=rate_functions.ease_out_cubic)
                .scale(6.0)
                .set_stroke(width=0.5, opacity=0),
            )

        self.play(
            animate_ripple(ripples[0], 0.0),
            animate_ripple(ripples[1], 0.25),
            animate_ripple(ripples[2], 0.5),
        )

        # A ЖӘНЕ B НҮКТЕЛЕРІН БЕЛГІЛЕУ
        pointA_sea = Dot(point=start_pos_sea, color=BLACK, radius=0.12)
        labelA_sea = MathTex("A", color=BLACK).next_to(pointA_sea, LEFT * 0.8 + UP * 0.8, buff=0.1)

        pointB_sea = Dot(point=end_pos_sea, color=WHITE, radius=0.12)
        labelB_sea = MathTex("B", color=WHITE).next_to(pointB_sea, RIGHT * 0.8 + DOWN * 0.8, buff=0.1)

        nodeA_sea = VGroup(pointA_sea, labelA_sea)
        nodeB_sea = VGroup(pointB_sea, labelB_sea)

        self.play(
            FadeIn(nodeA_sea),
            FadeIn(nodeB_sea),
            run_time=0.8
        )

        # ------------------------------------------
        # ҮСЕНДІ ЖОҒАЛТУ ЖӘНЕ АСАНДЫ А НҮКТЕСІНЕ ЖЫЛЖЫТУ
        # ------------------------------------------
        target_asan_pos = pointA_sea.get_center() + UP * 0.45 + LEFT * 0.1

        self.play(
            FadeOut(usen_shore),
            asan_shore.animate.move_to(target_asan_pos),
            run_time=1.2
        )

        self.wait(1)

# ==========================================
        # 5-БӨЛІМ: ТРАЕКТОРЯЛАР, ОПТИМИЗАЦИЯ ЖӘНЕ ҮСЕННІҢ ҚОЗҒАЛЫСЫ
        # ==========================================
        # 1. A ЖӘНЕ B НҮКТЕЛЕРІН ТҮЗУМЕН ҚОСУ (#FF5252) — 1-ші ТРАЕКТОРИЯ
        line_AB_1 = Line(
            start=pointA_sea.get_center(),
            end=pointB_sea.get_center(),
            color=COLOR_PATH,
            stroke_width=4
        )
        self.play(Create(line_AB_1), run_time=1.0)

        # 2. ЖОҒАРҒЫ ЖАҚТАҒЫ ТАЙМЕР (t1)
        timer_val1 = ValueTracker(0.0)
        timer_tex1 = always_redraw(lambda: 
            MathTex(
                f"t_1 = {timer_val1.get_value():.2f}\\text{{ s}}", 
                color=BLACK
            ).scale(1.1).to_corner(UR, buff=0.8)
        )
        self.play(Write(timer_tex1), run_time=0.5)

        # Асанның қозғалысы (2 * DEGREES бұрышымен)
        pos_A = pointA_sea.get_center()
        pos_B = pointB_sea.get_center()

        t_intersect1 = (0.0 - pos_A[1]) / (pos_B[1] - pos_A[1])
        pos_beach1 = interpolate(pos_A, pos_B, t_intersect1)

        d_land1 = np.linalg.norm(pos_beach1 - pos_A)
        d_sea1 = np.linalg.norm(pos_B - pos_beach1)

        # ЖЫЛДАМДЫҚТАР (Құмда 3 есе жылдам)
        v_land = 1.8
        v_sea = 0.6

        time_land1 = d_land1 / v_land
        time_sea1 = d_sea1 / v_sea
        total_time1 = time_land1 + time_sea1

        asan_shore.generate_target()
        asan_shore.target.rotate(2 * DEGREES)
        asan_shore.target.move_to(pos_A)
        self.play(MoveToTarget(asan_shore), run_time=0.5)

        # Асан жүріп өтеді
        self.play(
            asan_shore.animate.move_to(pos_beach1),
            timer_val1.animate.set_value(time_land1),
            run_time=time_land1,
            rate_func=linear
        )

        asan_swim = ImageMobject("asan.swim.png")
        asan_swim.height = 1.1
        asan_swim.rotate(np.arctan2((pos_B - pos_A)[1], (pos_B - pos_A)[0]) + 90 * DEGREES)
        asan_swim.move_to(pos_beach1)
        
        self.remove(asan_shore)
        self.add(asan_swim)

        self.play(
            asan_swim.animate.move_to(pos_B),
            timer_val1.animate.set_value(total_time1),
            run_time=time_sea1,
            rate_func=linear
        )

        # ------------------------------------------
        # АСАН ЖОҒАЛЫП, ҮСЕН А НҮКТЕСІНДЕ ШЫҒАДЫ
        # ------------------------------------------
        # Жазу қара түске (color=BLACK) ауыстырылды
        text_long_sea = Text("Судағы жол ұзын", font_size=24, color=BLACK)
        text_long_sea.next_to(line_AB_1.get_center(), RIGHT, buff=0.2)

        usen_A = ImageMobject("usen.walk.png")
        usen_A.height = 1.1
        usen_A.move_to(pos_A)

        self.play(
            FadeOut(asan_swim),
            FadeIn(usen_A),
            Write(text_long_sea),
            run_time=1.0
        )
        self.wait(1)

        # ------------------------------------------
        # 2-ШІ ТРАЕКТОРИЯ (Жалпы жол тым ұзын)
        # ------------------------------------------
        pos_beach2 = np.array([pos_B[0], 0.0, 0.0])

        line_AB_2_land = Line(start=pos_A, end=pos_beach2, color=ORANGE, stroke_width=4)
        line_AB_2_sea = Line(start=pos_beach2, end=pos_B, color=ORANGE, stroke_width=4)
        line_AB_2 = VGroup(line_AB_2_land, line_AB_2_sea)

        # Жазу қара түске (color=BLACK) ауыстырылды
        text_long_total = Text("Жалпы жол тым ұзын", font_size=24, color=BLACK)
        text_long_total.next_to(line_AB_2_land.get_center(), LEFT, buff=0.2)

        self.play(
            Create(line_AB_2),
            Write(text_long_total),
            run_time=1.2
        )

        self.wait(2.5)

        # ------------------------------------------
        # ЕКЕУІНІҢ ОРТАСЫН БОЯУ
        # ------------------------------------------
        region_between = Polygon(
            pos_A, pos_beach1, pos_B, pos_beach2,
            fill_color=YELLOW,
            fill_opacity=0.25,
            stroke_width=0
        )
        self.play(FadeIn(region_between), run_time=1.2)
        self.wait(1.5)

        # ------------------------------------------
        # ОРТАСЫНАН ОҢТАЙЛЫ (БАЛАНС) 3-ШІ СЫЗЫҚ
        # ------------------------------------------
        pos_beach3 = interpolate(pos_beach1, pos_beach2, 0.7)

        line_opt_land = Line(start=pos_A, end=pos_beach3, color=GREEN, stroke_width=5)
        line_opt_sea = Line(start=pos_beach3, end=pos_B, color=GREEN, stroke_width=5)
        line_optimal = VGroup(line_opt_land, line_opt_sea)

        self.play(Create(line_optimal), run_time=1.2)

        self.play(
            FadeOut(line_AB_1),
            FadeOut(line_AB_2),
            FadeOut(text_long_sea),
            FadeOut(text_long_total),
            FadeOut(region_between),
            run_time=1.0
        )

        # "Баланс" сөзі де қара түске (color=BLACK) ауыстырылды
        text_balance = Text("Баланс", font_size=32, color=BLACK, weight=BOLD)
        text_balance.next_to(line_optimal.get_center(), RIGHT, buff=0.4)
        self.play(Write(text_balance), run_time=0.8)
        self.wait(1)

        # ------------------------------------------
        # ҮСЕННІҢ $t_2$ ТАЙМЕРІМЕН ҚОЗҒАЛЫСЫ
        # ------------------------------------------
        timer_val2 = ValueTracker(0.0)
        timer_tex2 = always_redraw(lambda: 
            MathTex(
                f"t_2 = {timer_val2.get_value():.2f}\\text{{ s}}", 
                color=BLACK
            ).scale(1.1).next_to(timer_tex1, DOWN, buff=0.3, aligned_edge=RIGHT)
        )
        self.play(Write(timer_tex2), run_time=0.5)

        d_land3 = np.linalg.norm(pos_beach3 - pos_A)
        d_sea3 = np.linalg.norm(pos_B - pos_beach3)

        time_land3 = d_land3 / v_land
        time_sea3 = d_sea3 / v_sea
        total_time3 = time_land3 + time_sea3

        usen_angle_land = np.arctan2((pos_beach3 - pos_A)[1], (pos_beach3 - pos_A)[0]) + 90 * DEGREES
        usen_A.rotate(usen_angle_land)

        self.play(
            usen_A.animate.move_to(pos_beach3),
            timer_val2.animate.set_value(time_land3),
            run_time=time_land3,
            rate_func=linear
        )

        usen_swim = ImageMobject("usen.swim.png")
        usen_swim.height = 1.1
        usen_angle_sea = np.arctan2((pos_B - pos_beach3)[1], (pos_B - pos_beach3)[0]) + 90 * DEGREES
        usen_swim.rotate(usen_angle_sea)
        usen_swim.move_to(pos_beach3)

        self.remove(usen_A)
        self.add(usen_swim)

        self.play(
            usen_swim.animate.move_to(pos_B),
            timer_val2.animate.set_value(total_time3),
            run_time=time_sea3,
            rate_func=linear
        )

        self.wait(3)