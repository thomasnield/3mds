from manim import *
import numpy as np
import os
import pathlib

config.quality = "fourk_quality"
config.preview = True
config.verbosity = "WARNING"
config.disable_caching = False

resources_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), "resource")
def get_resource(filename: str): return os.path.join(resources_folder, filename)

class LogoScene(Scene):

    def construct(self):
        circle = Circle(1.0, color=BLUE)
        rectangle = Rectangle(height=1.0, width=2.0, color=BLUE).move_to(circle, UP)

        handle = RoundedRectangle(corner_radius=.5, height=1.5, width=2.0, color=BLUE) \
            .move_to(circle).shift(LEFT * .8)

        handle_inner = Difference(handle, handle.copy().scale(.8), color=BLUE, fill_opacity=0.0)

        cup = VGroup(circle, rectangle, handle_inner)

        self.play(
            Create(cup)
        )

        self.play(
            cup.animate.set_fill(BLUE, opacity=1)
        )

        # create sin wave steam

        def get_sine_wave(dx=0):
            return FunctionGraph(
                lambda x: np.sin((x + dx)),
                x_range=[-3, 3]
            )

        sine_function = get_sine_wave()
        d_theta = ValueTracker(0)

        def update_wave(func):
            func.become(
                get_sine_wave(dx=d_theta.get_value())
            )
            return func

        sine_function.add_updater(update_wave)

        self.play(Create(sine_function))
        self.play(d_theta.animate.increment_value(4 * PI), run_time=2)

        # create steam functions
        steam_functions = []
        steam_waves = VGroup()
        for i in range(3):
            steam_function = get_sine_wave() \
                .rotate(PI / 2.0) \
                .scale(.2) \
                .next_to(cup, UP) \
                .shift([i * .5, 0, 0])

            steam_waves.add(steam_function)

            d_theta = ValueTracker(0)

            def update_wave(func, d=d_theta, i=i):
                func.become(
                    get_sine_wave(dx=d.get_value()) \
                        .rotate(PI / 2.0) \
                        .scale(.2) \
                        .next_to(cup, UP) \
                        .shift([i * .5, 0, 0])
                )
                return func

            steam_function.add_updater(update_wave)

            steam_functions += d_theta

            self.play(Create(steam_function), run_time=.3)

        text = Text("3-Minute Data Science").scale(.8).shift(DOWN * 1.5)
        self.play(Write(text), run_time=.5)
        #mobj_to_svg(VGroup(cup, steam_waves, sine_function), 'logo.svg', h_padding=1)
        self.play(*(d.animate.increment_value(4 * PI) for d in steam_functions), run_time=8, rate_func=linear)
        self.wait()


class PieChart(Scene):
    def construct(self):
        # create weights
        weights = np.array([.4, .3, .15, .10, .05])
        angles = 360 * DEGREES * weights
        rotate_angles = 360 * DEGREES * np.cumsum([0, .3, .15, .10, .05])
        colors = [RED, BLUE, PURPLE, GREEN, ORANGE]

        sectors = [Sector(outer_radius=3,
                          color=c,
                          angle=a).rotate(-r, about_point=ORIGIN)
                   for a, c, r in zip(angles, colors, rotate_angles)]

        self.add(*sectors)

        # add labels
        label_circle = Circle(radius=1.75)
        label_angles = rotate_angles - (angles / 2)
        labels = [MathTex(w, font_size=30) \
                      .move_to(label_circle.point_at_angle(-la))
                  for w, s, la in zip(weights, sectors, label_angles)]
        self.add(*labels)


class PieChartAnimated(Scene):
    def construct(self):
        # increment this up to 360 degrees later
        pie_vt = ValueTracker(.01)

        # create weights
        weights = np.array([.4, .3, .15, .10, .05])
        angles = 360 * DEGREES * weights
        rotate_angles = np.cumsum([0, .3, .15, .10, .05])
        colors = [RED, BLUE, PURPLE, GREEN, ORANGE]

        sectors = [always_redraw(lambda _w=w, _c=c, _r=r:
                                 Sector(outer_radius=3,
                                        color=_c,
                                        angle=pie_vt.get_value() * DEGREES * _w) \
                                 .rotate(-_r * pie_vt.get_value() * DEGREES, about_point=ORIGIN)
                                 )
                   for w, c, r in zip(weights, colors, rotate_angles)]

        self.add(*sectors)
        self.wait()
        self.play(pie_vt.animate.set_value(360), run_time=3)
        self.wait()

        # add labels
        label_circle = Circle(radius=1.75)
        label_angles = rotate_angles * 360 * DEGREES - (angles / 2)

        labels = [MathTex(w, font_size=30) \
                      .move_to(label_circle.point_at_angle(-la))
                  for w, s, la in zip(weights, sectors, label_angles)]

        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=.6))
        self.wait()

class JetBrainsPromo(Scene):
    def construct(self):
        jb_logo = ImageMobject(get_resource("jetbrains.png"))
        discount_txt = Tex(r"Use 3-month code ", r"3min\_datascience")
        discount_txt[1].set_color(BLUE)

        self.add(
            Group(jb_logo, discount_txt).arrange(DOWN)
        )


class ClosingCard(Scene):
  def construct(self):

    title = Text("Get 10-Day Free Access") \
        .set_color(BLUE).to_edge(UL)

    books = Group(
      ImageMobject(get_resource("book1.jpg")),
      ImageMobject(get_resource("book2.jpg"))
    ).scale(.33).arrange(RIGHT,buff=.8).next_to(title,DOWN,buff=.8,aligned_edge=LEFT)

    source_code = Tex("My books, live trainings, courses and more!", color=BLUE) \
        .next_to(books, DOWN, aligned_edge=LEFT,buff=1)

    email = Text(r"See link in the description") \
        .scale(.5) \
        .next_to(source_code, DOWN, aligned_edge=LEFT)

    self.play(*[FadeIn(mobj) for mobj in (title, books, source_code, email)])

    self.wait(29)


if __name__ == "__main__":
    os.system(r"manim pie_charts.py ClosingCard")
