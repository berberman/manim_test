from manimlib.imports import *
import itertools


class WTF(Scene):
    CONFIG = {
        "plane_kwargs": {
            "color": RED_B
        },
    }

    testE = None
    testEArrow = None
    testF = None

    D = 3.0
    FST = 5.0

    def construct(self):
        # Plane
        plane = NumberPlane(**self.plane_kwargs)
        plane.add(plane.get_axis_labels())
        self.add(plane)
        # Left E
        e_left = self.Positron("-")
        e_left_text = TexMobject("-4Q")
        e_left.move_to(self.D * LEFT)
        e_left_text.next_to(e_left, UP)
        # Origin E
        origin = self.Positron("+")
        # origin.scale(0.25)
        origin_text = TexMobject("Q")
        origin_text.next_to(origin, UP)
        # Brace
        left_group = VGroup(e_left, e_left_text, origin)
        left_brace = Brace(left_group)
        left_brace_text = left_brace.get_tex("L=-" + str(self.D))

        # Brace
        right = Dot(self.D * RIGHT, radius=0.2)
        right_group = VGroup(origin, right)
        right_brace = Brace(right_group)
        right_text = right_brace.get_tex("L=" + str(self.D))

        self.testE = self.Positron("+")
        self.testE.move_to(self.FST * LEFT)
        # self.testE.scale(0.25)
        self.testEArrow = Arrow(color=YELLOW, stroke_width=2)
        self.testEArrow.move_to(self.FST * LEFT)

        self.testF = TexMobject("0", color=RED)
        self.testF.move_to(self.FST * LEFT)

        self.play(
            FadeIn(e_left),
            Write(e_left_text),
            FadeIn(origin),
            Write(origin_text),
            Write(left_brace_text),
            GrowFromCenter(left_brace),
            Write(right_text),
            GrowFromCenter(right_brace),
            FadeIn(self.testE),
            FadeIn(self.testEArrow),
            FadeIn(self.testF))

        i = -self.FST
        while i < self.FST:
            f = self.calculate_f(i)
            new_f = TexMobject("E=" + format(f) + "N/c", color=YELLOW)
            new_f.move_to(X_AXIS * i + 1.3 * UP)
            new_f.scale(0.8)
            new_arrow = Arrow(color=YELLOW, stroke_width=2)
            new_arrow.move_to(X_AXIS * i + 0.5 * UP)
            new_arrow.set_length(sign(f) * 0.8)
            self.play(ApplyMethod(self.testE.move_to, i * X_AXIS),
                      Transform(self.testEArrow, new_arrow),
                      Transform(self.testF, new_f)
                      )
            i = i + 0.5

    def calculate_f(self, d):
        if d == .0 or d == -.0:
            d = 0.001
        r = d + self.D
        if r == .0 or r == -.0:
            r = 0.001
        f1 = -4.0 / (r ** 2) * sign(r)
        f2 = 1.0 / (d ** 2.0) * sign(d)
        return 9.0 * 1E9 * (f1 + f2)

    class Positron(Circle):
        CONFIG = {
            "radius": 0.2,
            "stroke_width": 2,
            "color": RED,
            "fill_color": RED,
            "fill_opacity": 0.8,
        }

        def __init__(self, text, **kwargs):
            Circle.__init__(self, **kwargs)
            plus = TexMobject(text)
            plus.scale(0.7)
            plus.move_to(self)
            self.add(plus)


def sign(n):
    if n == .0:
        return 1.0
    else:
        return n / abs(n)


def format(s):
    raw = "%e" % s
    r = raw.split('e')
    if float(s) == 0:
        return "0.0"
    return r[0] + "Q\\times10^{" + ''.join(list(itertools.dropwhile(lambda x: x == '0', r[1][1:]))) + "}"
