import math
import pandas as pd
from manim import *
import os 

class DataPoint(Dot):
    def __init__(self, point: list | np.ndarray, x: float, y: float, color, **kwargs):
        super().__init__(point=point, radius=.15, color=color, **kwargs)
        self.x = x
        self.y = y

def create_model(data: pd.DataFrame, initial_m: float, initial_b: float) -> tuple:

    m_tracker = ValueTracker(initial_m)
    b_tracker = ValueTracker(initial_b)

    ax = Axes(
        x_range=[-0.5, 10],
        y_range=[-0.2, 1.3],
        x_axis_config={"include_tip": False, "include_numbers": False},
        y_axis_config={"include_tip": False, "include_numbers": True}
    )

    # plot points
    false_points = [DataPoint(point=ax.c2p(p.x, p.y), x=p.x, y=p.y, color=RED) for p in data.itertuples() if p.y == 0.0]
    true_points = [DataPoint(point=ax.c2p(p.x, p.y), x=p.x, y=p.y, color=BLUE) for p in data.itertuples() if p.y == 1.0]
    points = [*true_points, *false_points]

    # plot function
    f = lambda x: 1.0 / (1.0 + math.exp(-(b_tracker.get_value() + m_tracker.get_value() * x)))
    plot = always_redraw(lambda: ax.plot(f, color=YELLOW))

    # max line
    max_line = DashedLine(start=ax.c2p(0, 1), end=ax.c2p(10, 1), color=WHITE)

    # likelihood_lines
    likelihood_lines = [
        always_redraw(
            lambda p=p: DashedLine(
                start=p.get_center(),
                end=ax.c2p(p.x, f(p.x)),
                color=p.get_color()
            )
        )
        for p in points
    ]

    return data, m_tracker, b_tracker, ax, points, true_points, false_points, plot, f, max_line, likelihood_lines

class LogisticRegressionScene(Scene):

    def construct(self):

        # build the logistic regression model
        url = r"https://raw.githubusercontent.com/thomasnield/machine-learning-demo-data/master/classification/simple_logistic_regression.csv"

        data, m_tracker, b_tracker, ax, points, true_points, false_points, \
            plot, f, max_line, likelihood_lines = create_model(data=pd.read_csv(url),
                                                               initial_m=0.69267212,
                                                               initial_b=-3.17576395
                                                               )

        # draw and initialize the objects
        self.play(LaggedStartMap(Write, ax),
                  Write(max_line),
                  Write(MathTex("0") \
                        .scale(.8) \
                        .next_to(ax.c2p(0, 0), DL, buff=.2)
                        )
                  )
        self.wait()

        self.play(LaggedStartMap(Write, VGroup(*true_points)))
        self.play(LaggedStartMap(Write, VGroup(*false_points)))
        self.play(Write(plot))
        self.wait()

        # draw axis labels
        x_label = ax.get_x_axis_label(
            Tex("Hours of Rain").scale(0.8), edge=DOWN, direction=DOWN, buff=0.5
        )
        y_label = ax.get_y_axis_label(
            Tex("Probability of Flood").scale(0.8).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.3,
        )

        # label x and y axes
        self.play(Write(x_label))
        self.wait()
        self.play(Write(y_label))
        self.wait()
        self.play(Unwrite(x_label), Unwrite(y_label), run_time=1/3)
        self.wait()

        # label true and false data
        true_data_label = Tex("TRUE", color=BLUE).next_to(VGroup(*true_points), UP)
        false_data_label = Tex("FALSE", color=RED).next_to(VGroup(*false_points), UP)

        self.play(Write(true_data_label), Circumscribe(VGroup(*true_points)))
        self.wait()
        self.play(Write(false_data_label), Circumscribe(VGroup(*false_points)))
        self.wait()
        self.play(Unwrite(true_data_label), Unwrite(false_data_label), run_time=1 / 3)
        self.wait()

        # Project likelihood lines
        self.play(LaggedStartMap(Write, VGroup(*likelihood_lines)))
        self.wait()
        self.play(m_tracker.animate.increment_value(-.3), b_tracker.animate.increment_value(-.3))
        self.play(m_tracker.animate.increment_value(.3), b_tracker.animate.increment_value(.3))
        self.play(m_tracker.animate.increment_value(.3), b_tracker.animate.increment_value(.3))
        self.play(m_tracker.animate.increment_value(-.3), b_tracker.animate.increment_value(-.3))
        self.wait()

        # Highlight middle
        self.play(
            Circumscribe(
                VGroup(*[p for p in points if 2.3 < ax.p2c(p.get_center())[0] < 7.5])
            ),
            run_time=3
        )

        # Remove likelihood lines
        self.play(*[Unwrite(mobj) for mobj in (*points, *likelihood_lines)])
        self.wait()

        # trace the curve
        alpha_tracker = ValueTracker(.65)

        # the trace dot that follows the curve
        class TraceDot(Dot):
            def __init__(self, alpha: float):
                self.point = plot.point_from_proportion(alpha)
                super().__init__(point=self.point, color=YELLOW)

                self.x = ax.p2c(self.point)[0]
                self.y = ax.p2c(self.point)[1]

        trace_dot: TraceDot = always_redraw(lambda: TraceDot(alpha_tracker.get_value()))

        # Have a label chase the trace
        trace_label = always_redraw(lambda: MathTex(round(TraceDot(alpha_tracker.get_value()).y, 2)) \
            .scale(.75) \
            .next_to(trace_dot, UL)
        )

        self.play(Write(trace_dot), Write(trace_label))
        self.wait()
        self.play(alpha_tracker.animate.set_value(0.0), run_time=3)
        self.play(alpha_tracker.animate.set_value(1.0), run_time=3)
        self.play(alpha_tracker.animate.set_value(0.65), run_time=3)
        self.wait()

        # demonstrate a prediction
        self.play(alpha_tracker.animate.set_value(.65), run_time=1)
        self.wait()

        predict_line_vert = DashedLine(color=YELLOW,
                                       dash_length=.3,
                                       start=trace_dot.get_center(),
                                       end=ax.c2p(trace_dot.x, 0)
                                       )

        predict_line_horz = DashedLine(color=YELLOW,
                                       dash_length=.3,
                                       start=trace_dot.get_center(),
                                       end=ax.c2p(0, trace_dot.y)
                                       )

        self.play(
            Write(predict_line_vert),
            Write(predict_line_horz)
        )

        predict_label_vert = MathTex(
            round(trace_dot.x, 2)
        ).scale(.8) \
        .next_to(predict_line_vert, DOWN, buff=.25)

        predict_label_horz = MathTex(
            round(trace_dot.y, 2)
        ).scale(.8) \
        .next_to(predict_line_horz, LEFT, buff=.25)

        self.play(Unwrite(trace_label))
        self.play(
            Write(predict_label_vert),
            Write(predict_label_horz)
        )
        self.wait()

        # demonstrate threshhold regions
        def generate_regions(threshold=0.5):
            false_region = Polygon(*[ax.c2p(x, y) for x, y in [(0, 0), (0, threshold), (10, threshold), (10, 0)]],
                                   color=RED, stroke_width=0, fill_opacity=.5) \
                .next_to(Point(ax.c2p(0, 0)), aligned_edge=DL, buff=0)

            true_region = Polygon(*[ax.c2p(x, y) for x, y in [(0, threshold), (0, 1), (10, 1), (10, threshold)]],
                                  color=BLUE, stroke_width=0, fill_opacity=.5) \
                .next_to(Point(ax.c2p(0, threshold)), aligned_edge=DL, buff=0)

            return true_region, false_region

        true_region, false_region = generate_regions()

        true_region.save_state()
        false_region.save_state()

        self.play(
            LaggedStartMap(FadeIn, true_region),
            LaggedStartMap(FadeIn, false_region)
        )

        self.wait()

        self.wait()
        true_text = Text("TRUE", color=WHITE) \
            .move_to(true_region, aligned_edge=RIGHT) \
            .shift(LEFT)

        false_text = Text("FALSE", color=WHITE) \
            .move_to(false_region, aligned_edge=RIGHT) \
            .shift(LEFT)

        self.play(Write(true_text), Write(false_text))
        self.wait()
        self.play(Wiggle(true_text), FocusOn(trace_dot))
        self.wait()
        self.play(FadeOut(true_text), FadeOut(false_text))
        self.wait()

        true_region1, false_region1 = generate_regions(.8)

        self.play(
            Transform(true_region, true_region1),
            Transform(false_region, false_region1)
        )
        self.wait()

        false_text.move_to(false_region1, aligned_edge=RIGHT).shift(LEFT)
        self.play(FadeIn(false_text))
        self.play(Wiggle(false_text), FocusOn(trace_dot))
        self.play(FadeOut(false_text))

        self.wait()

        self.play(
            Restore(true_region), Restore(false_region)
        )
        self.wait()
        true_region2, false_region2 = generate_regions(.2)

        self.play(
            Transform(true_region, true_region2),
            Transform(false_region, false_region2)
        )
        self.wait()

        self.play(
            Restore(true_region), Restore(false_region)
        )

if __name__ == "__main__":
    os.system( r"manim -qk -v WARNING -p --disable_caching -o NeuralNetworkScene.mp4 20220918_logistic_regression.py NeuralNetworkScene")
