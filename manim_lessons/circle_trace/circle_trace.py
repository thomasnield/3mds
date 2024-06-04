from manim import *
import os

config.quality = "fourk_quality"
config.preview = True
config.verbosity = "WARNING"
config.disable_caching = False

class CircleTraceProportion(Scene):
    def construct(self):
        circle = Circle(radius=2)
        self.add(circle)

        point = Dot()
        vt = DecimalNumber(0.0)

        point.add_updater(lambda m: m.move_to(circle.point_from_proportion(vt.get_value())), call_updater=True)
        vt.add_updater(lambda m: m.move_to(circle.point_from_proportion(vt.get_value()) * 1.3), call_updater=True)

        self.add(vt, point)
        self.wait()
        self.play(ChangeDecimalToValue(vt, 1.0), run_time=3)
        self.wait()
        self.play(ChangeDecimalToValue(vt, 0.0), run_time=3)
        self.wait()

class CircleTraceDegrees(Scene):
    def construct(self):
        circle = Circle(radius=2)
        self.add(circle)

        point = Dot()
        vt = DecimalNumber(0.0, unit=r"^{\circ}", num_decimal_places=0)

        point.add_updater(lambda m: m.move_to(circle.point_at_angle(vt.get_value()*DEGREES)), call_updater=True)
        vt.add_updater(lambda m: m.move_to(circle.point_at_angle(vt.get_value()*DEGREES) * 1.3), call_updater=True)

        self.add(vt, point)
        self.wait()
        self.play(ChangeDecimalToValue(vt, 359), run_time=3)
        self.wait()
        self.play(ChangeDecimalToValue(vt, 0), run_time=3)
        self.wait()



class CircleTraceRadians(Scene):
    def construct(self):
        circle = Circle(radius=2)
        self.add(circle)

        point = Dot()
        vt = DecimalNumber(0.0, unit=r"\pi")

        point.add_updater(lambda m: m.move_to(circle.point_at_angle(vt.get_value()*PI)), call_updater=True)
        vt.add_updater(lambda m: m.move_to(circle.point_at_angle(vt.get_value()*PI) * 1.4), call_updater=True)

        self.add(vt, point)
        self.wait()
        self.play(ChangeDecimalToValue(vt, 2), run_time=3)
        self.wait()
        self.play(ChangeDecimalToValue(vt, 0), run_time=3)
        self.wait()


if __name__ == "__main__":
    os.system(r"manim circle_trace.py CircleTraceProportion")
    os.system(r"manim circle_trace.py CircleTraceDegrees")
    os.system(r"manim circle_trace.py CircleTraceRadians")