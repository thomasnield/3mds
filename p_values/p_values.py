import os, pathlib
from manim import *

config.quality = "low_quality"
config.preview = True
config.verbosity = "WARNING"
config.disable_caching = True

# where graphics are stored
resources_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources")

def get_svg(filename: str): return os.path.join(resources_folder, filename)

class Teacup(SVGMobject):
    def __init__(self, fill_color: str) -> None:
        super().__init__(file_name=get_svg("hot-tea-icon.svg"), fill_color=fill_color)

class Teakettle(SVGMobject):
    def __init__(self, fill_color: str) -> None:
        super().__init__(file_name=get_svg("coffee-tea-kettle-icon.svg"), fill_color=fill_color)


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

        for m in h_group:
            self.play(Write(m))
            self.wait()

        h0 = Tex("Null Hypothesis", color=BLUE, font_size=60) \
            .next_to(h_group, DOWN, aligned_edge=LEFT) \
            .to_edge(DOWN)

        h1 = Tex("Alternative Hypothesis", color=BLUE, font_size=60) \
            .next_to(h_group, DOWN, aligned_edge=LEFT) \
            .to_edge(DOWN)

        self.play(Circumscribe(h_group[:2]), FadeIn(h0))
        self.wait()
        self.play(FadeOut(h0))
        self.wait()
        self.play(Circumscribe(h_group[2:4]), FadeIn(h1))
        self.wait()
        self.play(FadeOut(h1))
        self.wait()

        # Highlight the alternative hypothesis and strike through null hypothesis
        strikethru = Line(start=h_group[0].get_left(), end=h_group[1].get_right(), color=YELLOW)
        self.play(Write(strikethru))
        self.wait()
        self.play(Indicate(h_group[2:4]))
        self.wait()



# Execute rendering
if __name__ == "__main__":
    #os.system(r"manim -qk -v WARNING -p --disable_caching -o TeacupScene.png p_values/p_values.py TeacupScene")
    os.system(r"manim p_values.py TeacupScene")
