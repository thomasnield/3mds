from manim import *
import numpy as np
import os

config.quality = "low_quality"
config.preview = True
config.verbosity = "WARNING"
config.disable_caching = False

class PieChart(Scene):
    def construct(self):

        # create weights
        weights = np.array([.4, .3, .15, .10, .05])
        angles = 360*DEGREES*weights
        rotate_angles = 360*DEGREES*np.cumsum([0, .3, .15, .10, .05])
        colors = [RED, YELLOW, BLUE, GREEN, ORANGE, PURPLE]

        sectors = [Sector(outer_radius=3,
                          color=c,
                          angle=a).rotate(-r, about_point=ORIGIN)
                   for a,c,r in zip(angles, colors, rotate_angles)]

        self.add(*sectors)

        # add labels
        label_circle = Circle(radius=1.75)
        label_angles = rotate_angles - (angles/2)
        labels = [MathTex(w,font_size=30) \
                      .move_to(label_circle.point_at_angle(-la))
                  for w,s,la in zip(weights, sectors, label_angles)]
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
                                        angle=pie_vt.get_value()*DEGREES*_w) \
                                    .rotate(-_r * pie_vt.get_value()*DEGREES, about_point=ORIGIN)
                                 )
                   for w, c, r in zip(weights, colors, rotate_angles)]

        self.add(*sectors)
        self.wait()
        self.play(pie_vt.animate.set_value(360), run_time=3)
        self.wait()

        # add labels
        label_circle = Circle(radius=1.75)
        label_angles = rotate_angles*360*DEGREES - (angles / 2)

        labels = [MathTex(w, font_size=30) \
                      .move_to(label_circle.point_at_angle(-la))
                  for w, s, la in zip(weights, sectors, label_angles)]

        self.play(LaggedStart(*[Write(l) for l in labels], lag_ratio=.6))
        self.wait()

if __name__ == "__main__":
    os.system(r"manim pie_charts.py PieChartAnimated")