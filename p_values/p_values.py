import os, pathlib
from manim import *

# where graphics are stored 
resources_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), "resources")

class Teacup(SVGMobject):
    def __init__(self, fill_color: str) -> None:
        super().__init__(file_name=os.path.join(resources_folder, "hot-tea-icon.svg"), fill_color=fill_color)

class Teakettle(SVGMobject):
    def __init__(self, fill_color: str) -> None:
        super().__init__(file_name=os.path.join(resources_folder, "coffee-tea-kettle-icon.svg"), fill_color=fill_color)


class TeacupScene(Scene):
    def construct(self):
        teacups = VGroup(*[Teacup(fill_color=WHITE) for i in range(8)]).arrange_in_grid(rows=2,cols=4)

        self.add(teacups)

        # select four of the cups with milk
        self.play(*[
            ReplacementTransform(teacups[i], teacups[i].copy().set_color(RED)) for i in (0,3,5,7)
        ])
        self.wait()

        # lady chooses them correctly 
        for i in (0,3,5,7):
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

# Execute rendering
if __name__ == "__main__":
    #os.system(r"manim -qk -v WARNING -p --disable_caching -o TeacupScene.png p_values/p_values.py TeacupScene")
    os.system(r"manim -ql -v WARNING -p --disable_caching -o TeacupScene.mp4 p_values/p_values.py TeacupScene")
