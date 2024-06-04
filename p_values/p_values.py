import os, pathlib
from manim import *
from scipy.stats import norm
import os
import urllib.request

config.quality = "fourk_quality"
config.preview = True
config.verbosity = "WARNING"
config.disable_caching = False

# where graphics are stored
resources_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources")

def get_svg(filename: str): return os.path.join(resources_folder, filename)

class Teacup(SVGMobject):
    def __init__(self, fill_color: str) -> None:
        super().__init__(file_name=get_svg("hot-tea-icon.svg"), fill_color=fill_color)

class Teakettle(SVGMobject):
    def __init__(self, fill_color: str) -> None:
        super().__init__(file_name=get_svg("coffee-tea-kettle-icon.svg"), fill_color=fill_color)

class TitleScene(Scene):

    def construct(self):
        title = Text("P-values")
        subtitle = Text("in 3 Minutes",color=BLUE).scale(.75).next_to(title, DOWN)

        self.play(FadeIn(title), FadeIn(subtitle), run_time=2)
        self.wait()
        self.play(FadeOut(title), FadeOut(subtitle), run_time=2)

class TeacupScene(Scene):
    def construct(self):
        teacups = VGroup(*[Teacup(fill_color=WHITE) for _ in range(8)]) \
            .arrange_in_grid(rows=2,cols=4)

        self.add(teacups)

        # select four of the cups with milk
        selected_cups = (0,3,5,7)

        self.play(*[
            ReplacementTransform(teacups[i], teacups[i].copy().set_color(RED)) for i in selected_cups
        ])
        self.wait()

        # lady chooses them correctly 
        for i in selected_cups:
            self.play(
                ReplacementTransform(teacups[i], teacups[i].copy().set_color(BLUE))
            )
            self.wait()

        self.wait()

        # move the tea to the bottom left corner
        teacups.generate_target()
        teacups.target.scale(.6).arrange_in_grid(rows=4,cols=2).to_edge(DL)

        # fade in tea kettle 
        kettle = Teakettle(fill_color=RED).scale(.6).next_to(teacups.target, aligned_edge=DR, buff=1)
        self.play(MoveToTarget(teacups), FadeIn(kettle))

        # animate the teacups moving and the kettle 
        self.wait()

        # show p-value as ratio
        tex1 = MathTex(r"p =", r"\frac{1}{70}", color=YELLOW, font_size=60)

        self.play(Write(tex1))
        self.wait()

        # show p-value as floating point
        tex2 = MathTex(r"p = ", r"0.01428571", color=YELLOW, font_size=60) \
            .move_to(tex1, aligned_edge=LEFT)

        self.play(ReplacementTransform(tex1[1], tex2[1]),
                  ReplacementTransform(tex1[0], tex2[0])
                  )

        self.wait()

        # show p-value as percentage
        tex3 = MathTex(r"p = ", r"1.4\%", color=YELLOW, font_size=60) \
            .move_to(tex2, aligned_edge=LEFT)

        self.play(*[FadeOut(t) for i,t in enumerate(tex2[1]) if i not in (1,3,4)],
                  ReplacementTransform(tex2[1][3], tex3[1][0]),
                  ReplacementTransform(tex2[1][1], tex3[1][1]),
                  ReplacementTransform(tex2[1][4], tex3[1][2]),
                  FadeIn(tex3[1][-1])
                  )

        self.wait()

        # Coincidence?
        coincidence = Tex("Coincidence?", color=RED, font_size=60)  \
            .rotate(45 * DEGREES) \
            .next_to(tex3, direction=DR, buff=0)

        self.play(Write(coincidence))
        self.wait()
        self.play(Unwrite(coincidence))
        self.wait()

        # go back to rounded floating point value
        tex4 = MathTex(r"p = ", r".014", color=YELLOW, font_size=60) \
            .move_to(tex3, aligned_edge=LEFT)

        self.play(
            ReplacementTransform(tex3[0], tex4[0]),
            FadeIn(tex4[1][1]),
            ReplacementTransform(tex3[1][1], tex4[1][0]),
            ReplacementTransform(tex3[1][0], tex4[1][2]),
            ReplacementTransform(tex3[1][2], tex4[1][3]),
            FadeOut(tex3[1][-1])
        )
        self.wait()

        # Define null hypothesis and alternative hypothesis
        h_group = VGroup(
            MathTex(r"H_0 = \text{She was guessing! }"), MathTex(r"P \ge .05"),
            MathTex(r"H_1 = \text{She has a talent! }"), MathTex(r"P < .05")
        ).arrange_in_grid(rows=2,cols=2, col_alignments=['l','l']) \
        .next_to(tex3, DOWN, aligned_edge=LEFT)

        h0 = Tex("Null Hypothesis", color=PURPLE, font_size=60) \
            .next_to(h_group, DOWN, aligned_edge=LEFT) \
            .to_edge(DOWN)

        h1 = Tex("Alternative Hypothesis", color=PURPLE, font_size=60) \
            .next_to(h_group, DOWN, aligned_edge=LEFT) \
            .to_edge(DOWN)

        hypothesis_texs = VGroup(h0, h1)

        for m,h in zip((h_group[:2], h_group[2:4]), (h0, h1)):
            self.play(Write(m))
            self.wait()
            self.play(Circumscribe(m), FadeIn(h))
            self.wait()
            self.play(FadeOut(h))


        # Highlight the alternative hypothesis and strike through null hypothesis
        strikethru = Line(start=h_group[0].get_left(), end=h_group[1].get_right(), color=YELLOW)
        self.play(Write(strikethru))
        self.wait()
        self.play(Indicate(h_group[2:4]))
        self.wait()

class Pill(SVGMobject):
    def __init__(self) -> None:
        super().__init__(file_name=get_svg("pill.svg"))


class ColdTestScene(MovingCameraScene):
    def construct(self):
        # declare normal distribution
        mean = 18
        std = 1.5
        f = lambda x: norm.pdf(x, mean, std)

        # declare axis
        ax = Axes(x_range=[mean-4*std, mean+4*std, std],
                    tips=False,
                    y_range=[0, f(mean) + .1, (f(mean) + .1) / 4],
                    x_axis_config={"include_numbers": True,
                                   "numbers_to_exclude": [mean - 4 * std]
                                   },
                    y_axis_config={"include_numbers": True,
                                   "decimal_number_config": {
                                       "num_decimal_places": 2
                                   }
                                   }
                    )
        self.play(Write(ax))
        self.wait()

        # declare plot
        plt = ax.plot(f, color=BLUE)
        self.play(Write(plt))
        self.wait()

        z_tracker = ValueTracker(.001)

        # shade area
        def area_for_z(z: float): return 1 - 2*norm.cdf(-z)
        area = always_redraw(lambda: ax.get_area(plt,x_range=(mean-z_tracker.get_value()*std, mean+z_tracker.get_value()*std)))
        self.add(area)

        self.play(z_tracker.animate.set_value(4))
        self.wait()
        a_txt = always_redraw(lambda: MathTex("A =", round(area_for_z(z_tracker.get_value()), 2))
                              .move_to(plt.get_center())
                              )
        self.play(Write(a_txt))
        self.wait()

        # transform area to .95
        self.play(z_tracker.animate.set_value(2))
        self.wait()

        # transform area to .68
        self.play(z_tracker.animate.set_value(1) )
        self.wait()

        # transform area to .95
        self.play(z_tracker.animate.set_value(2))
        self.wait()

        # draw dashed line and pill
        pill_x_vt = ValueTracker(16)
        line = always_redraw(lambda:
                             DashedLine(start=ax.c2p(pill_x_vt.get_value(),0), end=ax.c2p(pill_x_vt.get_value(), f(pill_x_vt.get_value())))
                             )

        pill = Pill().rotate(45*DEGREES).scale(.5)
        pill.add_updater(lambda mobj: mobj.next_to(line, UL))
        area.clear_updaters()
        self.play(Write(line))
        self.wait()
        self.play(FadeIn(pill))
        self.wait()

        # H0 and H1
        h_group = VGroup(
            MathTex(r"H_0 : \mu = 18 }"), MathTex(r"P \ge .05", color=YELLOW),
            MathTex(r"H_1 : \mu \ne 18"), MathTex(r"P < .05", color=YELLOW)
        ).arrange_in_grid(rows=2, cols=2, col_alignments=['l', 'l']) \
        .scale(.8) \
        .to_corner(UR)

        self.play(Write(h_group[0]), Write(h_group[1]))
        self.wait()
        self.play(Write(h_group[2]), Write(h_group[3]))
        self.wait()

        # trace pill to successful test
        self.play(area.animate.set_color(RED))
        self.wait()
        self.play(pill_x_vt.animate.set_value(14.9), area.animate.set_color(BLUE))
        self.wait()

        # zoom in on area
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(.5).move_to(pill))
        self.wait()
        diff_area = ax.get_area(plt, x_range=(pill_x_vt.get_value(), mean-2*std), color=YELLOW)
        self.play(FadeIn(diff_area))
        self.play(FadeOut(diff_area))
        self.wait()
        self.play(Restore(self.camera.frame))
        self.wait()

        # show p-value area
        self.play(FadeOut(area, a_txt))
        self.wait()


        # draw left tail
        lower_vt = ValueTracker(pill_x_vt.get_value())
        upper_vt = ValueTracker(pill_x_vt.get_value())

        left_tail = always_redraw(lambda:
                                  ax.get_area(plt, x_range=(lower_vt.get_value(), upper_vt.get_value()), color=RED)
                                  )
        self.add(left_tail)
        self.play(lower_vt.animate.set_value(mean-4*std), run_time=3)
        self.wait()

        # show area
        tail_label = MathTex(round(norm.cdf(pill_x_vt.get_value(),loc=mean, scale=std), 4)) \
                                        .move_to(plt.get_center())


        left_tail_line = Line(start=left_tail.get_right()+.25*LEFT+.125*DOWN, end=tail_label.get_left()+.25*DL)

        self.play(Write(left_tail_line), run_time=3)
        self.wait()
        self.play(Write(tail_label))
        self.wait()

        # copy right tail
        right_tail = left_tail.copy()

        self.play(FadeIn(right_tail))
        self.play(Rotate(right_tail, angle=-180*DEGREES, axis=Y_AXIS, about_point=ORIGIN), run_time=2)
        self.wait()

        # label p-value areas
        self.play(Rotate(left_tail_line.copy(), angle=-180*DEGREES, axis=Y_AXIS, about_point=ORIGIN),
                  tail_label.animate.become(MathTex(round(norm.cdf(pill_x_vt.get_value(),loc=mean, scale=std)*2, 4)) \
                                        .move_to(plt.get_center())),
                  run_time=2)
        self.wait()

        p_value_label = Tex("p-value", color=YELLOW).scale(.6).next_to(tail_label, DOWN)
        self.play(Circumscribe(tail_label), FadeIn(p_value_label))
        self.wait()

        # Highlight the alternative hypothesis and strike through null hypothesis

        strikethru = Line(start=h_group[0].get_left(), end=h_group[1].get_right(), color=YELLOW)
        self.play(Write(strikethru))
        self.wait()

        self.play(Indicate(tail_label), Indicate(VGroup(h_group[2], h_group[3])))
        self.wait()


class ClosingCard(Scene):
  def construct(self):
    urllib.request.urlretrieve(r"https://images-na.ssl-images-amazon.com/images/I/51yHtuQ9wAL._SX379_BO1,204,203,200_.jpg", "image1.jpg")
    urllib.request.urlretrieve(r"https://images-na.ssl-images-amazon.com/images/I/41khDop3M4L._SX379_BO1,204,203,200_.jpg", "image2.jpg")

    title = Text("Get 10-Day Free Access") \
        .set_color(BLUE).to_edge(UL)

    books = Group(
      ImageMobject(r"image1.jpg"),
      ImageMobject(r"image2.jpg")
    ).scale(.9).arrange(RIGHT,buff=.8).next_to(title,DOWN,buff=.8,aligned_edge=LEFT)

    source_code = Tex("My books, live trainings, courses and more!", color=BLUE) \
        .next_to(books, DOWN, aligned_edge=LEFT,buff=1)

    email = Text(r"See link in the description") \
        .scale(.5) \
        .next_to(source_code, DOWN, aligned_edge=LEFT)

    self.play(*[FadeIn(mobj) for mobj in (title, books, source_code, email)])

    self.wait(29)

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


# Execute rendering
if __name__ == "__main__":
    #os.system(r"manim p_values.py TitleScene")
    #os.system(r"manim p_values.py TeacupScene")
    #os.system(r"manim p_values.py ColdTestScene")
    #os.system(r"manim p_values.py LogoScene")
    os.system(r"manim p_values.py ClosingCard")

