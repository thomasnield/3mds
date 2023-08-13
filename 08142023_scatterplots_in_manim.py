from manim import *
import pandas as pd
import os


class ScatterPlotScene(Scene):

    def construct(self):
        # Download data and put in DataFrame
        data_url = "https://raw.githubusercontent.com/thomasnield/machine-learning-demo-data/master/regression/linear_normal.csv"

        df = pd.read_csv(data_url)

        # Add the Axes
        ax = Axes(x_range=[0, 100, 5], y_range=[-20, 200, 10])
        self.add(ax)

        # Add the dots
        for x, y in df.values:
            dot = Dot(ax.c2p(x, y), color=BLUE)
            self.add(dot)


class ScatterPlotAnimatedScene(Scene):

    def construct(self):
        # Download data and put in DataFrame
        data_url = "https://raw.githubusercontent.com/thomasnield/machine-learning-demo-data/master/regression/linear_normal.csv"

        df = pd.read_csv(data_url)

        # Animate the creation of Axes
        ax = Axes(x_range=[0, 100, 5], y_range=[-20, 200, 10])
        self.play(Write(ax))

        self.wait()  # wait for 1 second

        # Animate the creation of dots
        dots = [Dot(ax.c2p(x, y), color=BLUE) for x, y in df.values]
        self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=.05))

        self.wait()  # wait for 1 second


# Execute rendering
if __name__ == "__main__":
    # os.system(r"manim -qk -v WARNING -p --disable_caching -o ScatterPlotScene.png 08142023_scatterplots_in_manim.py ScatterPlotScene")
    os.system(r"manim -qk -v WARNING -p --disable_caching -o ScatterPlotScene.mp4 08142023_scatterplots_in_manim.py ScatterPlotAnimatedScene")
