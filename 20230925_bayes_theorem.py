
from manim import *
from threemds.utils import render_scenes

class BayesTheorem(Scene):
    def construct(self):
        title = Tex("Bayes Theorem", color=BLUE).scale(1.3).to_edge(UL)
        self.play(Write(title))
        self.wait()

        bt_tex = MathTex(r"P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}").scale(1.3)
        self.play(Write(bt_tex))
        self.wait()

class BayesTheoremTex(MathTex):
    def __init__(self, a:str, b: str,  **kwargs):

        tex_strings = []
        p_a = r"P(\text{" + a + r"})"
        p_b = r"P(\text{" + b + "})"
        p_a_b = r"P(\text{" + a + r"}|\text{" + b + r"})"
        p_b_a = r"P(\text{" + b + r"}|\text{" + a + r"})"

        tex =  p_a_b + r" = \frac{" + p_b_a  + r" \times " + p_a + "}{" + p_b + "}"
        print(tex)
        super().__init__(tex, **kwargs)

        global i
        i = 2

        def incr(j):
            global i
            if type(j) == str:
                i += len(j)
            else:
                i += j
            return i

        self.a1 = self[0][i:incr(a)] # capture A
        incr(1)
        self.b1 = self[0][i:incr(b)] # capture b
        self.a_given_b = self[0][0:i+1]
        incr(4)
        self.b2 = self[0][i:incr(b)] # capture b
        incr(1)
        self.a2 = self[0][i:incr(a)] # capture a
        self.b_given_a = self[0][i-len(a)-len(b)-3:i+1]
        incr(4)
        self.a3 = self[0][i:incr(a)] # capture a
        self.p_a = self[0][i-len(a)-2:i+1]
        incr(4)
        self.b3 = self[0][i:incr(b)] # capture b
        self.p_b = self[0][-len(b)-3:]

        VGroup(self.a1, self.a2, self.a3).set_color(RED)
        VGroup(self.b1, self.b2, self.b3).set_color(BLUE)


class VideoGameHomicidalExample1(Scene):
    def construct(self):
        self.add(Tex("Bayes Theorem", color=BLUE).scale(1.3).to_edge(UL))

        p_homicidal_gamer = MathTex(r"P(", r"\text{gamer}", r"|", r"\text{homicidal}", r")", "=", ".85").scale(1.3)
        p_homicidal_gamer[1].set_color(BLUE)
        p_homicidal_gamer[3].set_color(RED)

        self.play(Write(p_homicidal_gamer))
        self.wait()

        p_gamer_homicidal = MathTex(r"P(", r"\text{homicidal}", r"|", r"\text{gamer}", r")", "=", r"\text{ ? }").scale(1.3)
        p_gamer_homicidal[1].set_color(RED)
        p_gamer_homicidal[3].set_color(BLUE)

        VGroup(p_homicidal_gamer.generate_target(), p_gamer_homicidal).arrange(DOWN, buff=.75)

        self.play(MoveToTarget(p_homicidal_gamer), Write(p_gamer_homicidal))
        self.wait()

class VideoGameHomicidalExample2(Scene):
    def construct(self):

        stats = VGroup(
            MathTex(r"P(", r"\text{gamer}", r"|", r"\text{homicidal}", r")", "=", ".85"),
            MathTex(r"P(", r"\text{Gamer}", ") = .19"),
            MathTex(r"P(", r"\text{Homicidal}", ") = .0001"),
            MathTex(r"P(", r"\text{homicidal}", r"|", r"\text{gamer}", r")", "=", r"\text{ ? }")
        ).scale(1.3).arrange(DOWN, buff=.75)

        VGroup(stats[0][3], stats[2][1], stats[3][1]).set_color(RED)
        VGroup(stats[0][1], stats[1][1], stats[3][3]).set_color(BLUE)

        for m in stats:
            self.play(Write(m), lag_ratio=2)
            self.wait()



class VideoGameHomicidalExample3(Scene):
    def construct(self):

        self.add(Tex("Bayes Theorem", color=BLUE).scale(1.3).to_edge(UL))

        bt1 = BayesTheoremTex("A", "B")
        self.play(Write(bt1))
        self.wait()

        bt2 = BayesTheoremTex("Homicidal", "Gamer")
        self.play(ReplacementTransform(bt1, bt2))
        self.wait()

        p_solve = MathTex(r" = \frac{.85 \times .0001 }{.19}")
        p_solve[0][5:10].set_color(RED)
        p_solve[0][12:15].set_color(BLUE)

        a_given_b = bt2.a_given_b.copy()
        self.add(a_given_b)
        VGroup(a_given_b.generate_target(), p_solve).arrange(RIGHT)
        self.play(FadeOut(bt2))

        self.play(MoveToTarget(a_given_b), Write(p_solve))
        self.wait()

        p_solved = MathTex("= .0004").next_to(p_solve, DOWN, buff=.75, aligned_edge=LEFT)
        self.play(Write(p_solved))
        self.wait()
        self.play(Circumscribe(p_solved))
        self.wait()


class VennDiagramBayes(MovingCameraScene):
    def construct(self):

        # change line width behavior on camera zoom
        INITIAL_LINE_WIDTH_MULTIPLE = self.camera.cairo_line_width_multiple
        INITIAL_FRAME_WIDTH = config.frame_width

        def line_scale_down_updater(mobj):
            proportion = self.camera.frame.width / INITIAL_FRAME_WIDTH
            self.camera.cairo_line_width_multiple = INITIAL_LINE_WIDTH_MULTIPLE * proportion

        mobj = Mobject()
        mobj.add_updater(line_scale_down_updater)
        self.add(mobj)

        whole = Circle(radius=3.5,color=YELLOW)
        whole_txt = Tex("100K Population").move_to(whole)
        self.play(*[Write(m) for m in (whole, whole_txt)])
        self.wait()

        gamers = Circle(radius=1.5, color=BLUE).move_to([0,-2,0])
        gamers_txt = Tex("19K Gamers").scale(.75).move_to(gamers)
        self.play(*[Write(m) for m in (gamers, gamers_txt)])
        self.wait()

        homicidals = Circle(radius=.01, color=RED) \
            .move_to(gamers.get_top()) \
            .shift(.005 * DOWN) \
            .rotate(45*DEGREES, about_point=gamers.get_center())

        homicidals_txt = Tex("10 Homicidals") \
            .scale_to_fit_width(homicidals.width * .6) \
            .move_to(homicidals)

        self.play(*[Write(m) for m in (homicidals, homicidals_txt)])
        self.wait()

        self.wait()
        self.camera.frame.save_state()

        self.play(
            self.camera.frame.animate.set(height=homicidals.height * 1.2) \
                .move_to(homicidals),
            run_time=3
        )
        self.wait()

        homicidals_txt.save_state()
        homicidals_play_games_txt = Tex(r"8.5 homicidals","are gamers").arrange(DOWN) \
            .scale_to_fit_width(homicidals.width * .6) \
            .move_to(homicidals) \
            .rotate(45 * DEGREES)

        homicidals_dont_play_games_txt = Tex(r"1.5 homicidals","are not gamers").arrange(DOWN) \
            .scale_to_fit_width(homicidals.width * .4) \
            .move_to(homicidals.get_top()) \
            .next_to(gamers.get_top(), UP, buff=.001) \
            .rotate(45 * DEGREES, about_point=gamers.get_center())

        self.play(Transform(homicidals_txt,
                                       VGroup(homicidals_play_games_txt,
                                            homicidals_dont_play_games_txt)
                                       )
                  )

        self.wait()
        self.play(Restore(homicidals_txt))
        self.wait()
        self.play(Restore(self.camera.frame), run_time=3)
        self.wait()
        self.play(Wiggle(gamers))
        self.wait()
        self.play(Circumscribe(homicidals,color=RED))
        self.wait()

        self.play(
            self.camera.frame.animate.set(height=homicidals.height * 1.2) \
                .move_to(homicidals),
            run_time=3
        )

        intersect = Intersection(homicidals, gamers, color=PURPLE, fill_opacity=.6)
        diff1 = Difference(homicidals, gamers, color=RED, fill_opacity=.6)
        diff2 = Difference(gamers, homicidals, color=BLUE, fill_opacity=.6)

        homicidals_play_games_prop = Tex(r".85") \
            .scale_to_fit_width(homicidals.width * .2) \
            .move_to(homicidals) \
            .rotate(45 * DEGREES)

        homicidals_dont_play_games_prop = Tex(r".15") \
            .scale_to_fit_width(homicidals.width * .2) \
            .move_to(homicidals.get_top()) \
            .next_to(gamers.get_top(), UP, buff=.001) \
            .rotate(45 * DEGREES, about_point=gamers.get_center())

        self.play(*[Write(m) for m in (diff1,diff2,intersect)])

        self.wait()

        self.play(Transform(homicidals_txt,
                           VGroup(homicidals_play_games_prop,
                                homicidals_dont_play_games_prop)
                           )
                  )
        self.wait()
        self.play(
            Restore(self.camera.frame),
            *[FadeOut(m) for m in (diff1,diff2,intersect)],
            run_time=3
        )
        self.wait()


if __name__ == "__main__":
    render_scenes(q='k', scene_names=['VideoGameHomicidalExample2', 'VideoGameHomicidalExample1'])
