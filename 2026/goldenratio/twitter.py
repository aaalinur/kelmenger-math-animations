from manim import *
from background import SpaceBackground

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class TwitterGeometryScene(Scene):
    def construct(self):
        bg = SpaceBackground(loop_time=4.0)
        self.add(bg)

        # 1. Тек c.svg файлын жүктейміз
        circles_svg = SVGMobject("c.svg")
        circles_svg.height = 5.0
        circles_svg.move_to(ORIGIN)
        circles_svg.set_color("#00F0FF")
        circles_svg.set_stroke(width=1.5, opacity=0.4)

        # -------------------------------------------------------------
        # 2. c.svg ішіндегі құсты құрайтын негізгі шеңберлерді анықтау
        # (c.svg массвиіндегі индекстер бойынша)
        # -------------------------------------------------------------
        # Егер c.svg-де шеңберлер вектор бойынша орналасса,
        # біз олардың ішінен негізгі 5 шеңберді таңдап аламыз:
        
        # Мысалы: Басы, Кеудесі, Қанаты, Арқасы, Тұмсығы
        # (Дәл индекстерін анықтау үшін circles_svg[0], circles_svg[1]... қолданылады)
        
        ACCENT_COLOR = "#FF007A"
        
        # Барлық шеңберлердің ішінен құстың сұлбасын беретін негізгі топ:
        # Manim-де VGroup арқылы c.svg ішіндегі белгілі бір шеңберлерді ерекшелейміз
        bird_circles = VGroup()
        
        # c.svg құрамындағы әрбір ішкі элементті бақылау:
        for i, submob in enumerate(circles_svg):
            # Мұндағы i — c.svg ішіндегі шеңбердің реттік номері
            # Құс денесін құрайтын басты шеңберлерге қалың әрі ашық түс береміз
            pass

        # -------------------------------------------------------------
        # 3. Анимация
        # -------------------------------------------------------------

        # 1-қадам: Барлық шеңберлер торының (c.svg) шығуы
        self.play(
            Create(circles_svg),
            run_time=2.5
        )
        self.wait(1)

        # 2-қадам: Құстың сұлбасын жасайтын доғалардың/шеңберлердің 
        # үстінен акцентті түспен боялып шығуы
        # (Шеңберлердің дәл қиылысқан жиектері жарық диод сияқты жанады)
        
        # c.svg ішіндегі құсқа жауапты шеңберлерді таңдап (мысалы 3, 5, 8, 12):
        # Оларды акцентті түспен жүргізіп шығамыз:
        target_indices = [2, 4, 7, 10, 13]  # c.svg ішіндегі құстың контур шеңберлері
        
        highlight_group = VGroup(*[circles_svg[i] for i in target_indices if i < len(circles_svg)])

        self.play(
            highlight_group.animate.set_color(ACCENT_COLOR).set_stroke(width=5, opacity=1.0),
            run_time=2.0
        )
        self.wait(1)

        # 3-қадам: Құстың контуры толықтай айқындалуы
        # Қиылысқан шеңберлердің ішкі аркалары ерекшеленіп тұрады
        self.play(
            Indicate(highlight_group, color=WHITE, scale_factor=1.05),
            run_time=1.5
        )

        self.wait(3)