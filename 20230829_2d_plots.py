from manim import *
import os

class MyPlotScene(Scene):
    def construct(self):

        # declare x and y axes
        ax = Axes(x_range=[-5,5,1], y_range=[-1,5,1])

        # declare 2 functions and plot them
        f1 = ax.plot(lambda x: (1/5)*x**2, color=BLUE)
        f2 = ax.plot(lambda x: (1/2)*x + 1, color=YELLOW)

        # add the axes and plots to the scene
        self.add(ax, f1, f2)


class MyPlotSceneAnimated(Scene):
    def construct(self):

        # create a value tracker that updates the scene with an x-value
        vt = ValueTracker(-5)

        # declare x and y axes
        ax = Axes(x_range=[-5, 5, 1], y_range=[-1, 5, 1])

        # declare the two functions but always update their upper end to the ValueTracker
        f1 = always_redraw(lambda: ax.plot(lambda x: (1/5) * x ** 2, color=BLUE, x_range=[-5,vt.get_value()]))
        f2 = always_redraw(lambda: ax.plot(lambda x: (1/2) * x + 1, color=YELLOW, x_range=[-5,vt.get_value()]))

        # declare two dots to trace the two functions, also pointed to the ValueTracker
        f1_dot = always_redraw(lambda: Dot(
                    point=ax.c2p(vt.get_value(), f1.underlying_function(vt.get_value())),
                    color=BLUE
                )
            )

        f2_dot = always_redraw(lambda: Dot(
                    point=ax.c2p(vt.get_value(), f2.underlying_function(vt.get_value())),
                    color=YELLOW
                )
            )

        # Animate the axis being drawn
        self.play(Write(ax))
        self.wait()

        # Add the functions and trace dots
        self.add(f1, f2, f1_dot, f2_dot)

        # Animate the ValueTracker across 6 seconds, updating the plots and tracing dots
        self.play(vt.animate.set_value(5), run_time=6)

        # Fade out the dots
        self.play(FadeOut(f1_dot), FadeOut(f2_dot))
        self.wait()


# Execute rendering
if __name__ == "__main__":
    # os.system( r"manim -qk -v WARNING -p --disable_caching -o MyPlotScene.png scratch_pad.py MyPlotScene")
    os.system( r"manim -qk -v WARNING -p --disable_caching -o MyPlotScene.mp4 20230829_2d_plots.py MyPlotSceneAnimated")
