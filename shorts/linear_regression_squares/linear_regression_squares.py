from manim import *
import os
import numpy as np
from sklearn.linear_model import LinearRegression

config.preview = True
config.verbosity = "WARNING"
config.disable_caching = False

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

class LinearRegressionSquares(Scene):
    def construct(self):

        ax = Axes(x_range=(-1,10,1),
                  y_range=(-1,20,1),
                  x_length= config.frame_width*.8,
                  y_length=config.frame_height*.5)

        x = np.arange(1,10,1,dtype=float)
        y = np.array([1.52246106, 6.2760993, 3.80538691, 6.19722876,
                      7.21630459, 11.43284789, 11.8475795, 10.04278697, 16.15779999])

        points = VGroup(*[Dot(ax.c2p(_x,_y), color=BLUE) for _x,_y in zip(x,y)])
        print(y)

        fit = LinearRegression().fit(x.reshape(-1, 1), y)
        m = fit.coef_.flatten()[0]
        b = fit.intercept_.flatten()[0]

        line = Line(start=ax.c2p(0,b), end=ax.c2p(10, 10*m+b), color=YELLOW)

        residuals = VGroup(*[Line(start=ax.c2p(_x,_y),
                                  end=ax.c2p(_x, _x*m+b), color=RED)
                             for _x,_y in zip(x,y)])

        squares = VGroup(*[Square(side_length=r.get_length(), color=RED, fill_color=RED, fill_opacity=.6) \
                         .next_to(r, aligned_edge=LEFT, buff=0)
                           for r in residuals])

        self.add(ax, points, line, residuals, squares)

if __name__ == "__main__":
    os.system(r"manim linear_regression_squares.py LinearRegressionSquares")
