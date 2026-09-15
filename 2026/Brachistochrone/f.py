import numpy as np
from manim import *
from background import SpaceBackground


# =============================================================
# CONFIG
# =============================================================

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60


class Problem(Scene):

    def construct(self):

        # =============================================================
        # 1. БАСТАПҚЫ НҮКТЕЛЕР
        # =============================================================

        point_a_pos = np.array([-2.5, 4.0, 0.0])
        point_b_pos = np.array([2.5, 1.0, 0.0])

        dot_a = Dot(
            point=point_a_pos,
            radius=0.15,
            color=RED
        )

        dot_b = Dot(
            point=point_b_pos,
            radius=0.15,
            color=BLUE
        )

        label_a = MathTex(
            "A",
            font_size=48
        ).next_to(dot_a, LEFT)

        label_b = MathTex(
            "B",
            font_size=48
        ).next_to(dot_b, RIGHT)

        for mob in [dot_a, dot_b, label_a, label_b]:
            mob.set_z_index(20)

        self.play(
            FadeIn(dot_a, scale=0.5),
            Write(label_a),
            run_time=0.6
        )

        self.play(
            FadeIn(dot_b, scale=0.5),
            Write(label_b),
            run_time=0.6
        )


        # =============================================================
        # 2. ТҮЗУ СЫЗЫҚ
        # =============================================================

        line_path = Line(
            point_a_pos,
            point_b_pos,
            stroke_width=4,
            color=WHITE
        )

        self.play(
            Create(line_path),
            run_time=0.8
        )


        # =============================================================
        # 3. ДОП
        # =============================================================

        ball = ImageMobject("ball.png")

        ball.height = 1.4
        ball.set_z_index(30)

        radius = ball.height / 2


        def reset_ball_to_start(path_mobject):

            start_pos = path_mobject.point_from_proportion(0)

            tangent = (
                path_mobject.point_from_proportion(0.001)
                - start_pos
            )

            if np.linalg.norm(tangent) > 0:

                tangent /= np.linalg.norm(tangent)

                normal = np.array([
                    -tangent[1],
                    tangent[0],
                    0
                ])

            else:
                normal = UP

            ball.move_to(
                start_pos + normal * radius
            )


        def roll_ball_on_path(path_mobject):

            sim_dt = 1 / 60
            num_samples = 1000

            alphas = np.linspace(
                0,
                1,
                num_samples
            )

            points = [
                path_mobject.point_from_proportion(a)
                for a in alphas
            ]

            y_start = points[0][1]

            s_vals = [0.0]

            for i in range(1, num_samples):

                ds = np.linalg.norm(
                    points[i] - points[i - 1]
                )

                s_vals.append(
                    s_vals[-1] + ds
                )

            s_vals = np.array(s_vals)

            y_vals = np.array([
                p[1]
                for p in points
            ])

            current_s = 0.0

            s_history = [0.0]

            while current_s < s_vals[-1]:

                current_y = np.interp(
                    current_s,
                    s_vals,
                    y_vals
                )

                delta_h = max(
                    0,
                    y_start - current_y
                )

                # Домалау үшін:
                # v² = 10/7 * g * Δh
                v = np.sqrt(
                    (10.0 / 7.0)
                    * 9.81
                    * delta_h
                )

                v = max(v, 0.1)

                current_s += v * sim_dt

                s_history.append(
                    min(
                        current_s,
                        s_vals[-1]
                    )
                )

            total_length = s_vals[-1]

            sim_time = (
                len(s_history) - 1
            ) * sim_dt

            state = {
                "time": 0.0,
                "prev_s": 0.0
            }


            def updater(m, dt):

                state["time"] += dt

                idx = int(
                    state["time"] / sim_dt
                )

                s_curr = s_history[
                    min(
                        idx,
                        len(s_history) - 1
                    )
                ]

                alpha = (
                    s_curr / total_length
                    if total_length > 0
                    else 0
                )

                alpha = min(
                    1.0,
                    max(0.0, alpha)
                )

                center_pos = (
                    path_mobject
                    .point_from_proportion(alpha)
                )

                tangent = (
                    path_mobject
                    .point_from_proportion(
                        min(
                            1.0,
                            alpha + 0.001
                        )
                    )
                    - center_pos
                )

                if np.linalg.norm(tangent) > 0:

                    tangent /= np.linalg.norm(
                        tangent
                    )

                    normal = np.array([
                        -tangent[1],
                        tangent[0],
                        0
                    ])

                else:
                    normal = UP

                m.move_to(
                    center_pos
                    + normal * radius
                )

                ds = (
                    s_curr
                    - state["prev_s"]
                )

                m.rotate(
                    -ds / radius
                )

                state["prev_s"] = s_curr


            ball.add_updater(updater)

            self.wait(sim_time)

            ball.remove_updater(updater)


        # =============================================================
        # 4. ТҮЗУ БОЙЫМЕН ДОП
        # =============================================================

        reset_ball_to_start(
            line_path
        )

        self.play(
            FadeIn(ball, scale=0.5),
            run_time=0.5
        )

        roll_ball_on_path(
            line_path
        )

        self.play(
            FadeOut(ball, scale=0.5),
            run_time=0.5
        )

        self.wait(0.3)


        # =============================================================
        # 5. ШЕҢБЕР ДОҒАСЫ
        # =============================================================

        arc_path = ArcBetweenPoints(
            start=point_a_pos,
            end=point_b_pos,
            angle=TAU / 6,
            stroke_width=4,
            color=WHITE
        )

        self.play(
            Transform(
                line_path,
                arc_path
            ),
            run_time=1.2
        )

        self.wait(0.5)

        reset_ball_to_start(
            arc_path
        )

        self.play(
            FadeIn(ball, scale=0.5),
            run_time=0.5
        )

        roll_ball_on_path(
            arc_path
        )

        self.play(
            FadeOut(ball, scale=0.5),
            run_time=0.5
        )

        self.wait(0.3)


        # =============================================================
        # 6. ҮШ ОРТА
        # =============================================================

        self.play(
            Uncreate(line_path),
            run_time=0.8
        )

        y_top = point_a_pos[1]
        y_bottom = point_b_pos[1]

        rect_width = config.frame_width

        total_height = (
            y_top - y_bottom
        )

        layer_height = (
            total_height / 3.0
        )

        y_center_top = (
            y_top
            - layer_height / 2.0
        )

        y_center_mid = (
            y_top
            - 1.5 * layer_height
        )

        y_center_bot = (
            y_bottom
            + layer_height / 2.0
        )


        top_medium = Rectangle(
            width=rect_width,
            height=layer_height,
            fill_color="#0033aa",
            fill_opacity=0.45,
            stroke_width=0
        )

        top_medium.move_to([
            0,
            y_center_top,
            0
        ])

        top_medium.set_z_index(1)


        middle_medium = Rectangle(
            width=rect_width,
            height=layer_height,
            fill_color="#0066cc",
            fill_opacity=0.45,
            stroke_width=0
        )

        middle_medium.move_to([
            0,
            y_center_mid,
            0
        ])

        middle_medium.set_z_index(1)


        bottom_medium = Rectangle(
            width=rect_width,
            height=layer_height,
            fill_color="#44aaff",
            fill_opacity=0.45,
            stroke_width=0
        )

        bottom_medium.move_to([
            0,
            y_center_bot,
            0
        ])

        bottom_medium.set_z_index(1)


        self.play(

            FadeIn(
                bottom_medium,
                shift=UP * 0.3
            ),

            FadeIn(
                middle_medium,
                shift=UP * 0.3
            ),

            FadeIn(
                top_medium,
                shift=UP * 0.3
            ),

            run_time=1.2,
            lag_ratio=0.25
        )


        # =============================================================
        # 7. СИНУСОИДАЛЫҚ ТОЛҚЫНДАР
        # =============================================================

        wave_state = {
            "time": -3.0
        }


        def create_bullet_wave(
            y_center,
            speed_factor
        ):

            bullet_length = 1.8

            wave = always_redraw(
                lambda: ParametricFunction(

                    lambda t: np.array([
                        t,

                        y_center
                        + 0.22
                        * np.sin(
                            16
                            * (
                                t
                                - wave_state["time"]
                                * speed_factor
                            )
                        ),

                        0
                    ]),

                    t_range=[
                        wave_state["time"]
                        * speed_factor
                        - bullet_length / 2,

                        wave_state["time"]
                        * speed_factor
                        + bullet_length / 2,

                        0.01
                    ],

                    color=YELLOW,
                    stroke_width=5

                ).set_z_index(8)
            )

            return wave


        bullet_top = create_bullet_wave(
            y_center_top,
            speed_factor=2.0
        )

        bullet_mid = create_bullet_wave(
            y_center_mid,
            speed_factor=3.0
        )

        bullet_bot = create_bullet_wave(
            y_center_bot,
            speed_factor=4.2
        )


        self.add(
            bullet_top,
            bullet_mid,
            bullet_bot
        )


        def update_wave_time(
            mob,
            dt
        ):
            wave_state["time"] += dt


        tracker = Mobject()

        tracker.add_updater(
            update_wave_time
        )

        self.add(tracker)

        self.wait(2.8)

        tracker.remove_updater(
            update_wave_time
        )

        self.remove(
            bullet_top,
            bullet_mid,
            bullet_bot
        )


        # =============================================================
        # 8. ЭНЕРГИЯ
        # =============================================================

        bar_width = 0.8
        max_bar_height = 2.5
        base_y = -2.0

        progress = ValueTracker(0.0)

        x_ep = -1.2
        x_ek = 1.2


        ep_label = MathTex(
            "E_p",
            font_size=42,
            color=RED
        )

        ep_label.move_to([
            x_ep,
            base_y - 0.5,
            0
        ])

        ep_label.set_z_index(15)


        ep_bar = always_redraw(
            lambda: Rectangle(

                width=bar_width,

                height=max(
                    0.01,
                    (
                        1.0
                        - progress.get_value()
                    )
                    * max_bar_height
                ),

                fill_color=RED,
                fill_opacity=0.85,

                stroke_color=WHITE,
                stroke_width=2

            ).move_to([

                x_ep,

                base_y
                + (
                    (
                        1.0
                        - progress.get_value()
                    )
                    * max_bar_height
                )
                / 2.0,

                0

            ]).set_z_index(15)
        )


        ek_label = MathTex(
            "E_k",
            font_size=42,
            color=GREEN
        )

        ek_label.move_to([
            x_ek,
            base_y - 0.5,
            0
        ])

        ek_label.set_z_index(15)


        ek_bar = always_redraw(
            lambda: Rectangle(

                width=bar_width,

                height=max(
                    0.01,
                    progress.get_value()
                    * max_bar_height
                ),

                fill_color=GREEN,
                fill_opacity=0.85,

                stroke_color=WHITE,
                stroke_width=2

            ).move_to([

                x_ek,

                base_y
                + (
                    progress.get_value()
                    * max_bar_height
                )
                / 2.0,

                0

            ]).set_z_index(15)
        )


        base_line = Line(
            [
                x_ep - 0.8,
                base_y,
                0
            ],

            [
                x_ek + 0.8,
                base_y,
                0
            ],

            stroke_width=3,
            color=WHITE
        ).set_z_index(15)


        energy_group = Group(
            ep_bar,
            ek_bar,
            ep_label,
            ek_label,
            base_line
        )


        self.play(

            FadeIn(
                ep_label,
                shift=UP * 0.2
            ),

            FadeIn(
                ek_label,
                shift=UP * 0.2
            ),

            Create(base_line),

            FadeIn(
                ep_bar,
                scale=0.5
            ),

            FadeIn(
                ek_bar,
                scale=0.5
            ),

            run_time=0.8
        )

        self.wait(0.3)


        self.play(
            progress.animate.set_value(1.0),
            run_time=2.2,
            rate_func=smooth
        )

        self.wait(0.5)


        self.play(
            FadeOut(
                energy_group,
                scale=0.9
            ),
            run_time=0.8
        )


        # =============================================================
        # 9. ҮШ ОРТА — СЫНУ
        # =============================================================

        y_boundary_1 = 3.0
        y_boundary_2 = 2.0


        p0 = point_a_pos

        p1 = np.array([
            -1.2,
            y_boundary_1,
            0
        ])

        p2 = np.array([
            0.4,
            y_boundary_2,
            0
        ])

        p3 = point_b_pos


        ray_points = [
            p0,
            p1,
            p2,
            p3
        ]


        outer_ray = VMobject(
            stroke_width=10,
            stroke_color=YELLOW,
            stroke_opacity=0.35
        )

        outer_ray.set_points_as_corners(
            ray_points
        )

        outer_ray.set_z_index(11)


        inner_ray = VMobject(
            stroke_width=4,
            stroke_color="#FFFFAA"
        )

        inner_ray.set_points_as_corners(
            ray_points
        )

        inner_ray.set_z_index(12)


        normal1 = DashedLine(
            start=p1 + UP * 0.45,
            end=p1 + DOWN * 0.45,
            dash_length=0.06,
            stroke_width=1.5,
            stroke_opacity=0.7,
            color=WHITE
        ).set_z_index(10)


        normal2 = DashedLine(
            start=p2 + UP * 0.45,
            end=p2 + DOWN * 0.45,
            dash_length=0.06,
            stroke_width=1.5,
            stroke_opacity=0.7,
            color=WHITE
        ).set_z_index(10)


        self.play(
            Create(outer_ray),
            Create(inner_ray),
            run_time=1.8,
            rate_func=linear
        )

        self.play(
            FadeIn(
                normal1,
                scale=0.5
            ),

            FadeIn(
                normal2,
                scale=0.5
            ),

            run_time=0.5
        )

        self.wait(2)


        # =============================================================
        # 10. ГРАДИЕНТТІ ОРТА
        # =============================================================

        self.play(

            FadeOut(outer_ray),
            FadeOut(inner_ray),

            FadeOut(normal1),
            FadeOut(normal2),

            FadeOut(top_medium),
            FadeOut(middle_medium),
            FadeOut(bottom_medium),

            run_time=0.8
        )


        # -------------------------------------------------------------
        # ГРАДИЕНТ
        #
        # Маңызды:
        # Градиент енді СОЛДАН ОҢҒА емес,
        # ЖОҒАРЫДАН ТӨМЕН қарай өзгереді.
        # -------------------------------------------------------------

        gradient_rect = Rectangle(
            width=rect_width,
            height=total_height,
            stroke_width=0
        )

        gradient_rect.move_to([
            0,
            (y_top + y_bottom) / 2.0,
            0
        ])

        gradient_rect.set_z_index(1)


        # Жоғарыдан төмен бірнеше жұқа қабат.
        # Осылайша градиент бағыты анық түрде вертикаль болады.

        gradient_layers = []

        gradient_steps = 40

        for i in range(gradient_steps):

            ratio = i / (gradient_steps - 1)

            # Жоғарыда ашығырақ,
            # төменде қоюырақ.

            top_color = np.array(
                color_to_rgb("#0066cc")
            )

            bottom_color = np.array(
                color_to_rgb("#002266")
            )

            rgb = (
                top_color * (1 - ratio)
                + bottom_color * ratio
            )

            layer_color = rgb_to_color(rgb)


            layer = Rectangle(

                width=rect_width,

                height=total_height
                / gradient_steps
                + 0.01,

                stroke_width=0,

                fill_color=layer_color,

                fill_opacity=0.72

            )


            y = (
                y_top
                - (
                    i + 0.5
                )
                * total_height
                / gradient_steps
            )


            layer.move_to([
                0,
                y,
                0
            ])

            layer.set_z_index(1)

            gradient_layers.append(
                layer
            )


        self.play(
            LaggedStart(
                *[
                    FadeIn(layer)
                    for layer in gradient_layers
                ],

                lag_ratio=0.01
            ),

            run_time=1.2
        )

        self.wait(0.3)


        # =============================================================
        # 11. НАҚТЫ БРАХИСТОХРОНА / ЦИКЛОИДА
        # =============================================================

        #
        # Циклоиданың параметрлік теңдеуі:
        #
        # x = x0 + R(θ - sin θ)
        #
        # y = y0 - R(1 - cos θ)
        #
        #
        # Біз R және θ_end мәндерін A -> B
        # геометриялық шарттарынан есептейміз.
        #


        dx = (
            point_b_pos[0]
            - point_a_pos[0]
        )

        dy = (
            point_a_pos[1]
            - point_b_pos[1]
        )


        # Циклоиданың төңкерілген түрі үшін:
        #
        # dx = R(θ - sinθ)
        # dy = R(1 - cosθ)
        #
        # Сондықтан:
        #
        # dx / dy =
        # (θ - sinθ)/(1-cosθ)
        #
        # Осы теңдеуден θ табылады.


        from scipy.optimize import brentq


        def theta_equation(theta):

            return (
                (
                    theta
                    - np.sin(theta)
                )
                / (
                    1
                    - np.cos(theta)
                )
                - dx / dy
            )


        theta_end = brentq(
            theta_equation,
            1e-6,
            2 * np.pi - 1e-6
        )


        R_val = (
            dy
            / (
                1
                - np.cos(theta_end)
            )
        )


        # Тексеру үшін:

        final_dx = (
            R_val
            * (
                theta_end
                - np.sin(theta_end)
            )
        )

        final_dy = (
            R_val
            * (
                1
                - np.cos(theta_end)
            )
        )


        print(
            "Cycloid parameters:"
        )

        print(
            "R =",
            R_val
        )

        print(
            "theta_end =",
            theta_end
        )

        print(
            "Calculated dx =",
            final_dx
        )

        print(
            "Required dx =",
            dx
        )

        print(
            "Calculated dy =",
            final_dy
        )

        print(
            "Required dy =",
            dy
        )


        # =============================================================
        # 12. ЦИКЛОИДА ФУНКЦИЯСЫ
        # =============================================================

        def cycloid_func(t):

            theta = (
                t
                * theta_end
            )


            x = (
                point_a_pos[0]
                + R_val
                * (
                    theta
                    - np.sin(theta)
                )
            )


            y = (
                point_a_pos[1]
                - R_val
                * (
                    1
                    - np.cos(theta)
                )
            )


            return np.array([
                x,
                y,
                0
            ])


        # =============================================================
        # 13. ЦИКЛОИДАНЫ САЛУ
        # =============================================================

        cycloid_outer = ParametricFunction(

            cycloid_func,

            t_range=[
                0,
                1,
                0.002
            ],

            stroke_width=10,

            color=YELLOW,

            stroke_opacity=0.35

        ).set_z_index(11)


        cycloid_inner = ParametricFunction(

            cycloid_func,

            t_range=[
                0,
                1,
                0.002
            ],

            stroke_width=4,

            color="#FFFFAA"

        ).set_z_index(12)


        self.play(

            Create(
                cycloid_outer
            ),

            Create(
                cycloid_inner
            ),

            run_time=2.5,

            rate_func=linear
        )


        self.wait(2)
        
                # =============================================================
        
# =============================================================
        # 14. ФИНАЛ — ҮШ ТРАЕКТОРИЯНЫ ФИЗИКАЛЫҚ САЛЫСТЫРУ
        # =============================================================
        
        # Градиентті алып тастаймыз.
        self.play(
            *[FadeOut(layer) for layer in gradient_layers],
            FadeOut(cycloid_outer),
            FadeOut(cycloid_inner),
            run_time=0.8
        )
        
        # -------------------------------------------------------------
        # ҮШ ЖОЛ
        # -------------------------------------------------------------
        
        straight_path = Line(
            point_a_pos,
            point_b_pos,
            stroke_width=4,
            color=WHITE
        )
        
        arc_path_final = ArcBetweenPoints(
            start=point_a_pos,
            end=point_b_pos,
            angle=TAU / 6,
            stroke_width=4,
            color=WHITE
        )
        
        final_cycloid = ParametricFunction(
            cycloid_func,
            t_range=[0, 1, 0.002],
            stroke_width=4,
            color=WHITE
        )
        
        # Үш траекторияны бірге көрсетеміз.
        self.play(
            Create(straight_path),
            Create(arc_path_final),
            Create(final_cycloid),
            run_time=1.5,
            rate_func=linear
        )
        
        self.wait(0.4)
        
        # -------------------------------------------------------------
        # ҮШ ДОП
        # -------------------------------------------------------------
        
        ball_straight = ImageMobject("ball.png")
        ball_arc = ImageMobject("ball.png")
        ball_cycloid = ImageMobject("ball.png")
        
        for b in [ball_straight, ball_arc, ball_cycloid]:
            b.height = 0.72
            b.set_z_index(30)
        
        # -------------------------------------------------------------
        # ЖОЛДЫҢ ГЕОМЕТРИЯСЫ
        # -------------------------------------------------------------
        
        def get_path_data(path_mob, samples=1600):
            """
            Параметрлік alpha -> нақты доға ұзындығы s.
            Бұл барлық үш жол үшін бірдей физикалық есептеуді
            қолдануға мүмкіндік береді.
            """
            alphas = np.linspace(0.0, 1.0, samples)
        
            points = np.array([
                path_mob.point_from_proportion(a)
                for a in alphas
            ])
        
            ds = np.linalg.norm(
                points[1:] - points[:-1],
                axis=1
            )
        
            s_values = np.concatenate([
                [0.0],
                np.cumsum(ds)
            ])
        
            y_values = points[:, 1]
        
            return alphas, s_values, y_values
        
        
        # -------------------------------------------------------------
        # ФИЗИКАЛЫҚ СИМУЛЯЦИЯ
        # -------------------------------------------------------------
        
        def simulate_rolling(path_mob, gravity=9.81, sim_dt=1 / 60):
            """
            Доп A нүктесінен тыныштыққа жақын бастап,
            ауырлық әсерінен жол бойымен қозғалады.
        
            Домалайтын тұтас шар үшін:
                v² = (10/7) g Δh
        
            Одан кейін:
                ds = v dt
        
            Яғни әр траектория өзінің нақты ұзындығы мен
            биіктік өзгерісіне байланысты өз уақытында B-ге жетеді.
            """
        
            alphas, s_values, y_values = get_path_data(path_mob)
        
            total_length = s_values[-1]
            y_start = y_values[0]
        
            current_s = 0.0
            history = [0.0]
        
            while current_s < total_length:
                current_y = np.interp(
                    current_s,
                    s_values,
                    y_values
                )
        
                delta_h = max(
                    0.0,
                    y_start - current_y
                )
        
                # Тұтас шардың домалау энергиясы:
                # mgh = 1/2 mv² + 1/2 Iω²
                # I = 2/5 mr²
                # => v² = 10/7 g h
                v = np.sqrt(
                    (10.0 / 7.0)
                    * gravity
                    * delta_h
                )
        
                # A нүктесінде v = 0 болуы мүмкін.
                # Симуляцияның басталуын тоқтатпау үшін өте кіші
                # бастапқы жылдамдық береміз.
                v = max(v, 0.08)
        
                current_s += v * sim_dt
        
                history.append(
                    min(current_s, total_length)
                )
        
            total_time = (
                len(history) - 1
            ) * sim_dt
        
            return {
                "alphas": alphas,
                "s_values": s_values,
                "history": np.array(history),
                "total_length": total_length,
                "total_time": total_time,
            }
        
        
        # Үш траекторияны жеке-жеке физикалық есептейміз.
        straight_data = simulate_rolling(straight_path)
        arc_data = simulate_rolling(arc_path_final)
        cycloid_data = simulate_rolling(final_cycloid)
        
        print("\n==============================")
        print("ROLLING SIMULATION")
        print("==============================")
        print(
            f"Straight : {straight_data['total_time']:.3f} s"
        )
        print(
            f"Arc      : {arc_data['total_time']:.3f} s"
        )
        print(
            f"Cycloid  : {cycloid_data['total_time']:.3f} s"
        )
        print("==============================\n")
        
        
        # -------------------------------------------------------------
        # ДОПТЫ БАСТАПҚЫ НҮКТЕГЕ ОРНАЛАСТЫРУ
        # -------------------------------------------------------------
        
        def place_ball_at_s(
            ball_mob,
            path_mob,
            data,
            s,
        ):
            """
            Доптың центрін жолдан ball_radius қашықтықта ұстайды.
            """
        
            s = np.clip(
                s,
                0.0,
                data["total_length"]
            )
        
            alpha = np.interp(
                s,
                data["s_values"],
                data["alphas"]
            )
        
            pos = path_mob.point_from_proportion(alpha)
        
            # Жанама бағыт.
            eps = 0.001
            next_alpha = min(
                1.0,
                alpha + eps
            )
        
            tangent = (
                path_mob.point_from_proportion(next_alpha)
                - pos
            )
        
            norm = np.linalg.norm(tangent)
        
            if norm > 1e-9:
                tangent /= norm
        
                normal = np.array([
                    -tangent[1],
                    tangent[0],
                    0.0
                ])
            else:
                normal = UP
        
            radius = ball_mob.height / 2.0
        
            ball_mob.move_to(
                pos + normal * radius
            )
        
        
        place_ball_at_s(
            ball_straight,
            straight_path,
            straight_data,
            0.0
        )
        
        place_ball_at_s(
            ball_arc,
            arc_path_final,
            arc_data,
            0.0
        )
        
        place_ball_at_s(
            ball_cycloid,
            final_cycloid,
            cycloid_data,
            0.0
        )
        
        # Үшеуі де дәл бір уақытта көрінеді.
        self.play(
            FadeIn(ball_straight, scale=0.5),
            FadeIn(ball_arc, scale=0.5),
            FadeIn(ball_cycloid, scale=0.5),
            run_time=0.5
        )
        
        
        # -------------------------------------------------------------
        # ФИЗИКАЛЫҚ UPDATER
        # -------------------------------------------------------------
        
        def make_physics_updater(
            ball_mob,
            path_mob,
            data,
        ):
            state = {
                "time": 0.0,
                "prev_s": 0.0,
            }
        
            sim_dt = 1 / 60
        
            def updater(mob, dt):
                state["time"] += dt
        
                index = int(
                    state["time"] / sim_dt
                )
        
                index = min(
                    index,
                    len(data["history"]) - 1
                )
        
                s_curr = data["history"][index]
        
                place_ball_at_s(
                    mob,
                    path_mob,
                    data,
                    s_curr
                )
        
                # Домалау:
                # s = rθ  =>  Δθ = Δs/r
                ds = s_curr - state["prev_s"]
        
                radius = mob.height / 2.0
        
                if radius > 1e-9:
                    mob.rotate(
                        -ds / radius
                    )
        
                state["prev_s"] = s_curr
        
            return updater
        
        
        # Үш допқа да БІРДЕЙ физикалық механизм беріледі.
        ball_straight.add_updater(
            make_physics_updater(
                ball_straight,
                straight_path,
                straight_data
            )
        )
        
        ball_arc.add_updater(
            make_physics_updater(
                ball_arc,
                arc_path_final,
                arc_data
            )
        )
        
        ball_cycloid.add_updater(
            make_physics_updater(
                ball_cycloid,
                final_cycloid,
                cycloid_data
            )
        )
        
        
        # -------------------------------------------------------------
        # ҮШЕУІ ДЕ БІР МЕЗЕТТЕ БАСТАЙДЫ
        # БІРАҚ ӘРҚАЙСЫСЫНЫҢ УАҚЫТЫ ӘРТҮРЛІ.
        # -------------------------------------------------------------
        
        max_time = max(
            straight_data["total_time"],
            arc_data["total_time"],
            cycloid_data["total_time"],
        )
        
        self.wait(max_time)
        
        
        # -------------------------------------------------------------
        # UPDATER-ДЕРДІ ӨШІРУ
        # -------------------------------------------------------------
        
        ball_straight.clear_updaters()
        ball_arc.clear_updaters()
        ball_cycloid.clear_updaters()
        
        self.wait(2)
        
        