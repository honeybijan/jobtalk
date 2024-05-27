from manim import *
import random

class StickFigure(VGroup):
    def __init__(self, happy = True, color=WHITE, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.happy = happy
        self.body = SVGMobject(file_name = "svgs/person.svg", color = color, fill_color = color)
        self.add(self.body)
        self.eye1 = Circle(radius=.1, color=BLACK, fill_opacity=1).center().shift(.5 * LEFT)
        self.eye2 = Circle(radius=.1, color=BLACK, fill_opacity=1).center().shift(.5 * RIGHT)
        self.mouth = Arc(radius=1.0, start_angle= PI / 6, angle=2 * PI / 3, num_components=9, arc_center=self.body.get_center() + UP, color = BLACK, stroke_width=4).set_opacity(1).center().shift(DOWN)
        if self.happy:
            self.mouth.rotate(PI)
        self.head = VGroup(self.eye1, self.eye2, self.mouth).scale(.2).shift(1.3 * UP)
        self.add(self.head)
    
    # p is prob of same, i.e. p is prob of happy if starting happy
    def fade_in_random_emotion(self, p):
        if (random.random() > p):
            self.mouth.rotate(PI)
            self.happy = not self.happy
        return FadeIn(self.head)
    
    def random_emotion(self, p):
        if (random.random() > p):
            self.mouth.rotate(PI)
            self.happy = not self.happy

    def group_of_sticks(n, width, scale, h_sep, v_sep, happy_prob=.5, red_prob = None):
        g = VGroup()
        for i in range(n):
            if not red_prob:
                col = random_bright_color()
            else:
                if random.random() < red_prob:
                    col = RED
                else:
                    col = BLUE
            stick = StickFigure(color = col).scale(scale).shift(int(i / width) * v_sep * DOWN + int(i % width) * h_sep * RIGHT)
            if not red_prob:
                stick.random_emotion(happy_prob)
            else:
                if col == RED:
                    stick.random_emotion(.25)
                else:
                    stick.random_emotion(.75)
            g.add(stick)
        return g

class Pill(VGroup):
    def __init__(self, treated = True, color=WHITE, **kwargs):
        VGroup.__init__(self, **kwargs)
        body = SVGMobject(file_name = "svgs/pill.svg", color = color, fill_color = color).scale(.25)
        self.add(body)
        if not treated:
            prohibit = SVGMobject(file_name = "svgs/prohibit.svg", color = RED, fill_color = RED)
            self.add(prohibit)