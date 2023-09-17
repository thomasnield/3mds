from manim import *
from scipy.stats import norm
import os

class ProjectedAreaScene(Scene):
    def construct(self):

        # declare mean and standard deviation
        mean, std = 0, 1
        x_lower, x_upper = mean-std*3, mean+std*3

        # declare ValueTracker to draw both graphs
        # start it at lower tail
        vt = ValueTracker(x_lower)

        # declare x and y axes for PDF and CDF
        pdf_ax = Axes(x_range=[x_lower, x_upper, 1],
                      y_range=[-.05, .75, .25],
                      tips=False,
                      axis_config = {'include_numbers': True })

        cdf_ax = Axes(x_range=[x_lower, x_upper, 1],
                      y_range=[-.25, 1.0, .25],
                      tips=False,
                      axis_config = {'include_numbers': True, 'numbers_to_exclude' : [-.25] })

        # stack the axes vertically and fit to screen
        VGroup(pdf_ax, cdf_ax) \
            .arrange(UP,buff=1) \
            .scale_to_fit_height(6)

        # declare PDF function plot and its area
        pdf_partial_plot = always_redraw(lambda: pdf_ax.plot(lambda x: norm.pdf(x, mean, std),
                                                  x_range=[x_lower, vt.get_value()],
                                                  color=BLUE)
                                 )

        pdf_full_plot = pdf_ax.plot(lambda x: norm.pdf(x, mean, std))

        pdf_partial_area = always_redraw(lambda: pdf_ax.get_area(pdf_full_plot,
                                                      color=BLUE,
                                                      x_range=[x_lower, vt.get_value()])
                                 )


        cdf_partial_plot = always_redraw(lambda: cdf_ax.plot(lambda x: norm.cdf(x, mean, std),
                                                  x_range=[x_lower, vt.get_value()],
                                                  color=RED)
                                 )

        # create the line that connects the PDF and CDF
        projecting_line = always_redraw(lambda: DashedLine(color=YELLOW,
                                                           start=pdf_ax.c2p(vt.get_value(), 0),
                                                           end=cdf_ax.c2p(vt.get_value(),
                                                                          norm.cdf(vt.get_value(), mean, std)
                                                                          )
                                                           )
                                        )

        # add the axes and plots to the scene
        self.add(pdf_ax, cdf_ax, pdf_partial_area, cdf_partial_plot, projecting_line)
        self.wait()

        # animate the value tracker to upper x bound for 7 seconds
        self.play(vt.animate.set_value(x_upper), run_time=7)
        self.wait()



# Execute rendering
if __name__ == "__main__":
    os.system(r"manim -qk -v WARNING -p --disable_caching -o ProjectedAreaScene.mp4 20230829_multiple_plots.py ProjectedAreaScene")
