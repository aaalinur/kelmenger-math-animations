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


class ConstellationSpaceBackground(VGroup):
    """
    4-фон: Шоқжұлдыздар сызығы мен қалқымалы математикалық символдары бар
    концептуалды ғарыш фоны.
    """
    def __init__(self, num_nodes=25, max_distance=2.8, **kwargs):
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

        # 2. Шоқжұлдыз түйіндері (Nodes) мен сызықтар
        random.seed(404)
        self.nodes_data = []
        nodes_group = VGroup()
        lines_group = VGroup()

        # Түйіндерді орналастыру
        for _ in range(num_nodes):
            x = random.uniform(-config.frame_width / 2 + 0.5, config.frame_width / 2 - 0.5)
            y = random.uniform(-config.frame_height / 2 + 0.5, config.frame_height / 2 - 0.5)
            
            radius = random.uniform(0.02, 0.035)
            base_opacity = random.uniform(0.3, 0.7)
            
            node = Dot(point=[x, y, 0], radius=radius, color=COLOR_WHITE)
            node.set_opacity(base_opacity)
            nodes_group.add(node)
            
            self.nodes_data.append({
                "mob": node,
                "pos": np.array([x, y, 0]),
                "base_opacity": base_opacity,
                "phase": random.uniform(0, 2 * np.pi)
            })

        # Түйіндер арасындағы арақашықтық бойынша сызықтар жүргізу
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                p1 = self.nodes_data[i]["pos"]
                p2 = self.nodes_data[j]["pos"]
                dist = np.linalg.norm(p1 - p2)

                if dist < max_distance:
                    # Қашықтыққа байланысты мөлдірлік
                    line_opacity = (1.0 - (dist / max_distance)) * 0.18
                    line = Line(
                        start=p1,
                        end=p2,
                        stroke_color=COLOR_WHITE,
                        stroke_width=0.8,
                        stroke_opacity=line_opacity
                    )
                    lines_group.add(line)

        self.add(lines_group)
        self.add(nodes_group)

        # 3. Фонда баяу қалқитын математикалық символдар
        symbols_list = [r"\pi", r"\theta", r"\infty", r"\sum", r"\int", r"\alpha", r"\Delta"]
        self.floating_symbols = []
        symbols_group = VGroup()

        for i in range(10):
            sym_tex = random.choice(symbols_list)
            sym = MathTex(sym_tex, color=COLOR_WHITE, font_size=28)
            
            x = random.uniform(-3.5, 3.5)
            y = random.uniform(-7.0, 7.0)
            base_opacity = random.uniform(0.08, 0.18)  # Негізгі фонға кедергі жасамайтындай өте мөлдір
            
            sym.move_to([x, y, 0])
            sym.set_opacity(base_opacity)
            symbols_group.add(sym)

            self.floating_symbols.append({
                "mob": sym,
                "start_y": y,
                "speed": random.uniform(0.05, 0.12),
                "phase": random.uniform(0, 2 * np.pi)
            })

        self.add(symbols_group)
        self.add_updater(self.update_background)

    def update_background(self, mob, dt):
        self.time += dt
        
        # 1. Түйіндердің нәзік пульсациясы
        for node in self.nodes_data:
            val = np.sin(1.5 * self.time + node["phase"])
            op = node["base_opacity"] + 0.15 * val
            node["mob"].set_opacity(max(0.1, min(1.0, op)))

        # 2. Математикалық символдардың баяу қалқуы
        h = config.frame_height
        half_h = h / 2.0
        for sym in self.floating_symbols:
            current_y = sym["start_y"] + np.sin(0.5 * self.time + sym["phase"]) * 0.3
            sym["mob"].set_y(current_y)


class ConstellationSceneDemo(Scene):
    def construct(self):
        bg = ConstellationSpaceBackground(num_nodes=28)
        self.add(bg)

        title = Text("Концептуалды Фон", font="Pliant", font_size=36, color=COLOR_WHITE)
        title.to_edge(UP, buff=2.0)

        formula = MathTex(r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}", font_size=42, color=COLOR_WHITE)
        formula.center()

        self.play(Write(title))
        self.play(Write(formula))
        self.wait(4.0)