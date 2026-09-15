from manim import *
from background import SpaceBackground

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class Scene1Matchstick(MovingCameraScene):
    def construct(self):


        bg = SpaceBackground(loop_time=4.0)
        self.add(bg)


        MATCH_SCALE = 0.2435
        MATCH_POSITION = [-0.04, 0, 0]
        COLOR_PINK = "#FF007A"
        COLOR_YELLOW = "#FFE600"

        line_spacing = 1.2
        line_height = 10
        lines = VGroup(*[
            Line(
                start=[(i - 2.5) * line_spacing, -line_height / 2, 0],
                end=[(i - 2.5) * line_spacing, line_height / 2, 0],
                stroke_width=4,
                color=WHITE
            )
            for i in range(6)
        ])

        self.play(Create(lines), run_time=1.5)
        self.wait(0.5) 

        self.play(
            self.camera.frame.animate.set(width=2.5).move_to(ORIGIN),
            run_time=2
        )
        self.wait(0.5)

        matchstick = ImageMobject("match.png")
        matchstick.scale(MATCH_SCALE)
        matchstick.move_to(MATCH_POSITION)

        self.play(FadeIn(matchstick, scale=0.9), run_time=1)
        self.wait(0.5)

        left_line_x = -line_spacing / 2
        right_line_x = line_spacing / 2

        gap_arrow = DoubleArrow(
            start=[left_line_x, 1.2, 0],
            end=[right_line_x, 1.2, 0],
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
            color=COLOR_PINK
        )
        gap_label = MathTex("1", color=COLOR_PINK).scale(0.5)
        gap_label.next_to(gap_arrow, UP, buff=0.08)

        match_top = matchstick.get_top()[1]
        match_bottom = matchstick.get_bottom()[1]

        match_arrow = DoubleArrow(
            start=[right_line_x - 0.2, match_bottom, 0],
            end=[right_line_x - 0.2, match_top, 0],
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08,
            color=COLOR_PINK
        )
        match_label = MathTex("1", color=COLOR_PINK).scale(0.5)
        match_label.next_to(match_arrow, RIGHT, buff=0.08)

        arrows_group = VGroup(gap_arrow, gap_label, match_arrow, match_label)

        self.play(
            GrowFromCenter(gap_arrow),
            Write(gap_label),
            GrowFromCenter(match_arrow),
            Write(match_label),
            run_time=1.2
        )
        self.wait(1)

        self.play(FadeOut(arrows_group), run_time=0.8)

        center_dot = Dot(point=matchstick.get_center(), radius=0.04, color=COLOR_PINK)
        self.play(Create(center_dot), run_time=0.5)
        self.wait(0.3)

        match_with_dot = Group(matchstick, center_dot)

        self.play(
            match_with_dot.animate.shift(RIGHT * 0.3),
            run_time=1,
            rate_func=there_and_back
        )
        self.play(
            match_with_dot.animate.shift(LEFT * 0.3),
            run_time=1,
            rate_func=there_and_back
        )
        self.wait(0.5)

        dot_pos = center_dot.get_center()
        ref_line = Line(dot_pos, dot_pos + UP * 0.6, stroke_width=0)
        rot_line = Line(dot_pos, dot_pos + UP * 0.6, stroke_width=0)

        angle_arc = always_redraw(
            lambda: Arc(
                radius=0.25,
                start_angle=ref_line.get_angle(),
                angle=rot_line.get_angle() - ref_line.get_angle(),
                arc_center=dot_pos,
                color=COLOR_PINK,
                stroke_width=2.5
            )
        )

        self.add(angle_arc)
        self.play(
            Rotate(matchstick, angle=-35 * DEGREES, about_point=dot_pos),
            Rotate(rot_line, angle=-35 * DEGREES, about_point=dot_pos),
            run_time=1.2
        )
        self.wait(0.3)

        self.play(
            Rotate(matchstick, angle=35 * DEGREES, about_point=dot_pos),
            Rotate(rot_line, angle=35 * DEGREES, about_point=dot_pos),
            run_time=1.2
        )
        self.remove(angle_arc)
        self.wait(0.3)

        middle_x = (left_line_x + right_line_x) / 2
        dashed_mid_line = DashedLine(
            start=[middle_x, -line_height / 2, 0],
            end=[middle_x, line_height / 2, 0],
            dash_length=0.1,
            dashed_ratio=0.6,
            stroke_width=3,
            color=COLOR_PINK
        ).set_opacity(0.4)

        self.play(Create(dashed_mid_line), run_time=1)
        self.wait(0.5)

        self.play(
            Rotate(matchstick, angle=90 * DEGREES, about_point=dot_pos),
            run_time=1.5
        )
        self.wait(0.2)

        hit_point = np.array([left_line_x, dot_pos[1], 0])

        flash_spark = Flash(
            hit_point,
            color=COLOR_YELLOW,
            line_length=0.15,
            num_lines=8,
            flash_radius=0.1,
            run_time=0.8
        )
        hit_dot = Dot(point=hit_point, radius=0.06, color=COLOR_YELLOW)
        
        self.play(
            flash_spark,
            Create(hit_dot),
            run_time=0.8
        )
        self.wait(1)

        # Жоғары жылжыту
        top_shift = UP * 0.55
        all_scene_mobjects = Group(
            lines, matchstick, center_dot, dashed_mid_line
        )

        self.play(
            all_scene_mobjects.animate.shift(top_shift),
            hit_dot.animate.shift(top_shift),
            run_time=1.2
        )
        self.wait(0.3)

        # Төменгі панель мен өстер
        panel_bg = Rectangle(
            width=2.2,
            height=1.1,
            fill_color="#0a0b16",
            fill_opacity=1,
            stroke_color="#2a2c3d",
            stroke_width=1.5
        ).move_to([0, -0.65, 0]).set_z_index(0)

        axes = Axes(
            x_range=[0, PI, PI / 2],
            y_range=[0, 0.5, 0.25],
            x_length=1.5,
            y_length=0.6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_ticks": True,
                "tick_size": 0.03,
            },
            tips=False
        ).move_to(panel_bg.get_center() + DOWN * 0.05 + LEFT * 0.05).set_z_index(1)

        # X өсінің белгілері
        x_label_0 = MathTex("0", font_size=10).next_to(axes.c2p(0, 0), DOWN, buff=0.05)
        x_label_pi2 = MathTex(r"\frac{\pi}{2}", font_size=10).next_to(axes.c2p(PI / 2, 0), DOWN, buff=0.05)
        x_label_pi = MathTex(r"\pi", font_size=10).next_to(axes.c2p(PI, 0), DOWN, buff=0.05)

        # Y өсінің белгілері
        y_label_025 = MathTex("0.25", font_size=10).next_to(axes.c2p(0, 0.25), LEFT, buff=0.05)
        y_label_05 = MathTex("0.5", font_size=10).next_to(axes.c2p(0, 0.5), LEFT, buff=0.05)

        axis_labels = VGroup(x_label_0, x_label_pi2, x_label_pi, y_label_025, y_label_05).set_z_index(1)

        x_axis_title = MathTex(r"\theta", font_size=12, color=COLOR_PINK).set_z_index(1)
        x_axis_title.next_to(axes.x_axis.get_end(), RIGHT, buff=0.04)

        y_axis_title = MathTex(r"d", font_size=12, color=COLOR_PINK).set_z_index(1)
        y_axis_title.next_to(axes.y_axis.get_top(), UP, buff=0.04)

        self.play(FadeIn(panel_bg), run_time=0.6)
        self.play(
            Create(axes),
            Write(axis_labels),
            Write(x_axis_title),
            Write(y_axis_title),
            run_time=1.2
        )
        self.wait(0.5)

        # 1. d = 0.5 нүктесі (pi/2, 0.5)
        target_point = axes.c2p(PI / 2, 0.5)

        self.play(
            hit_dot.animate.move_to(target_point).scale(0.6).set_z_index(10),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        self.play(FadeOut(dashed_mid_line), run_time=0.5)

        self.current_match_angle = 90.0

        # Барлық кесінділер мен нүктелерді топтастыру
        all_graph_elements = VGroup(hit_dot)

        def process_distance(d_val, angle1_deg, angle2_deg):
            curr_center = center_dot.get_center()
            target_x = left_line_x + d_val
            shift_vector = np.array([target_x - curr_center[0], 0, 0])

            self.play(
                Rotate(matchstick, angle=-self.current_match_angle * DEGREES, about_point=curr_center),
                run_time=0.6
            )
            self.current_match_angle = 0.0

            self.play(
                matchstick.animate.shift(shift_vector),
                center_dot.animate.shift(shift_vector),
                run_time=0.8
            )

            new_dot_pos = center_dot.get_center()

            new_dashed_line = DashedLine(
                start=[new_dot_pos[0], -line_height / 2, 0],
                end=[new_dot_pos[0], line_height / 2, 0],
                dash_length=0.1,
                dashed_ratio=0.6,
                stroke_width=3,
                color=COLOR_PINK
            ).set_opacity(0.4)

            self.play(Create(new_dashed_line), run_time=0.5)

            self.play(
                Rotate(matchstick, angle=angle1_deg * DEGREES, about_point=new_dot_pos),
                run_time=0.8
            )
            self.current_match_angle = angle1_deg

            hit_pt_1 = np.array([left_line_x, new_dot_pos[1] + (0.5 * np.cos(angle1_deg * DEGREES)), 0])
            flash_1 = Flash(hit_pt_1, color=COLOR_YELLOW, line_length=0.15, num_lines=8, flash_radius=0.1, run_time=0.5)
            dot_1 = Dot(point=hit_pt_1, radius=0.06, color=COLOR_YELLOW)
            self.play(flash_1, Create(dot_1), run_time=0.5)

            self.play(
                Rotate(matchstick, angle=-angle1_deg * DEGREES, about_point=new_dot_pos),
                run_time=0.6
            )
            self.current_match_angle = 0.0

            self.play(
                Rotate(matchstick, angle=angle2_deg * DEGREES, about_point=new_dot_pos),
                run_time=0.8
            )
            self.current_match_angle = angle2_deg

            hit_pt_2 = np.array([left_line_x, new_dot_pos[1] - (0.5 * np.cos((180 - angle2_deg) * DEGREES)), 0])
            flash_2 = Flash(hit_pt_2, color=COLOR_YELLOW, line_length=0.15, num_lines=8, flash_radius=0.1, run_time=0.5)
            dot_2 = Dot(point=hit_pt_2, radius=0.06, color=COLOR_YELLOW)
            self.play(flash_2, Create(dot_2), run_time=0.5)

            t1 = axes.c2p(angle1_deg * DEGREES, d_val)
            t2 = axes.c2p(angle2_deg * DEGREES, d_val)

            self.play(
                dot_1.animate.move_to(t1).scale(0.6).set_z_index(10),
                dot_2.animate.move_to(t2).scale(0.6).set_z_index(10),
                run_time=1.2,
                rate_func=smooth
            )

            conn_line = Line(
                start=t1,
                end=t2,
                color=COLOR_YELLOW,
                stroke_width=2.5
            ).set_z_index(5)

            self.play(Create(conn_line), FadeOut(new_dashed_line), run_time=0.8)
            all_graph_elements.add(dot_1, dot_2, conn_line)

        # 2. d = 0.25 (30° және 150°)
        process_distance(0.25, 30, 150)

        # 3. d = sqrt(3)/4 ≈ 0.433 (60° және 120°)
        process_distance(np.sqrt(3) / 4, 60, 120)

        # 4. d = 0.1 (11.5° және 168.5°)
        process_distance(0.1, 11.53, 168.47)

        # 5. d = 0 (тура сызықтың үстінде, 0° және 180°)
        process_distance(0.001, 0.1, 179.9)

        self.wait(1)

# --- ЖАҢАРТЫЛҒАН СОҢҒЫ БӨЛІМ ---

        # 1. Артқы объектілерді жоғалту
        background_objects = Group(lines, matchstick, center_dot)
        graph_group = Group(panel_bg, axes, axis_labels, x_axis_title, y_axis_title, all_graph_elements)

        self.play(
            FadeOut(background_objects),
            run_time=0.8
        )
        self.wait(0.2)

        # 2. Графикті ЕҢ ЖОҒАРЫ ЫСЫРУ (UP * 2.2 - 9:16 форматы үшін оңтайлы)
        self.play(
            graph_group.animate.shift(UP * 2.2),
            run_time=1.2
        )
        self.wait(0.3)

        # 3. d = 0.25 ақ үзік сызығы (жаңа позициясымен)
        d025_start = axes.c2p(0, 0.25)
        d025_end = axes.c2p(PI, 0.25)
        
        white_line = DashedLine(
            start=d025_start,
            end=d025_end,
            dash_length=0.04,
            dashed_ratio=0.5,
            stroke_width=2,
            color=WHITE
        ).set_z_index(6)

        self.play(Create(white_line), run_time=0.8)
        self.wait(0.2)

        # 4. Қызғылт (#FF007A) индикатор сызық
        highlight_line = Line(
            start=d025_start,
            end=d025_start + RIGHT * 0.25,
            stroke_width=4,
            color=COLOR_PINK
        ).set_z_index(7)

        self.play(Create(highlight_line), run_time=0.4)

        shift_distance = (d025_end[0] - d025_start[0]) - 0.25
        self.play(
            highlight_line.animate.shift(RIGHT * shift_distance),
            run_time=1.0,
            rate_func=there_and_back
        )
        self.wait(0.2)

        # 5. Индикатор мен ақ сызықты жоғалту
        self.play(
            FadeOut(highlight_line),
            FadeOut(white_line),
            run_time=0.5
        )

        # 6. Синусоида және оның астындағы сары аудан
        sin_curve = axes.plot(
            lambda x: 0.5 * np.sin(x),
            x_range=[0, PI],
            color=COLOR_YELLOW
        ).set_z_index(4)

        region_under_curve = axes.get_area(
            sin_curve,
            x_range=[0, PI],
            color=COLOR_YELLOW,
            opacity=0.35
        ).set_z_index(3)

        self.play(
            Create(sin_curve),
            FadeIn(region_under_curve),
            run_time=1.2
        )
        self.wait(0.5)

        # 7. Формулаларды графиканың ТӨМЕНІНДЕГІ АШЫҚ ЖЕРГЕ орналастыру (Y = -0.50)
        FORMULA_POS = [0, -0.50, 0]

        # Негізгі формула: P = S1 / S2
        formula = MathTex(
            r"P = \frac{S_1}{S_2}",
            font_size=16,
            color=WHITE
        ).move_to(FORMULA_POS)

        self.play(Write(formula), run_time=0.8)
        self.wait(0.6)

        # Ашылған түрі
        formula_expanded = MathTex(
            r"P = \frac{\int_{0}^{\pi} \frac{1}{2}\sin\theta \, d\theta}{0.5 \cdot \pi}",
            font_size=13,
            color=WHITE
        ).move_to(FORMULA_POS)

        self.play(Transform(formula, formula_expanded), run_time=1.0)
        self.wait(0.8)

        # Тез-тез есептеу 1-қадам
        formula_step2 = MathTex(
            r"P = \frac{1}{\frac{\pi}{2}}",
            font_size=16,
            color=WHITE
        ).move_to(FORMULA_POS)

        self.play(Transform(formula, formula_step2), run_time=0.6)
        self.wait(0.3)

        # Тез-тез есептеу 2-қадам
        formula_step3 = MathTex(
            r"P = \frac{2}{\pi}",
            font_size=16,
            color=WHITE
        ).move_to(FORMULA_POS)

        self.play(Transform(formula, formula_step3), run_time=0.6)
        self.wait(0.5)

        # Соңғы Алтын Жазу: pi = 2 / P
        pi_formula = MathTex(
            r"\pi = \frac{2}{P}",
            font_size=22,
            color="#FFD700"
        ).move_to(FORMULA_POS)

        self.play(
            Transform(formula, pi_formula),
            run_time=1.0
        )
        self.wait(2.5)