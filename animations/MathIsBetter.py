from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

class MathIsBetter(PresentationScene):

    def construct(self):
        title = Text("Causal Math Surpasses RCTs").to_edge(UP, buff=.5)
        self.add(title)
        
        math = Circle(radius = 1, color=BLUE, fill_color=BLUE, fill_opacity = .5).shift(.5 * DOWN)
        exp = Circle(radius = 2, color=RED, fill_color=RED, fill_opacity = .5).shift(.5 * DOWN)
        math_lab = always_redraw(lambda: Text("Math").scale(.7).next_to(math, UP))
        exp_lab = always_redraw(lambda: Text("RCTs").scale(.7).next_to(exp, UP))
        self.play(Write(exp), Write(exp_lab))
        self.end_fragment()

        self.play(Write(math), Write(math_lab))
        self.end_fragment()

        math.generate_target()
        exp.generate_target()
        math.target.scale(2).shift(RIGHT)
        exp.target.shift(LEFT)
        self.play(MoveToTarget(math), MoveToTarget(exp))
        self.end_fragment()

        what_else = Text("What else is possible?").scale(.5).to_edge(DOWN, buff=.5)
        self.play(Write(what_else))
        self.end_fragment()