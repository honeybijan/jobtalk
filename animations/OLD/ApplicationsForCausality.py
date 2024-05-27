from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class ApplicationsForCausality(PresentationScene):

    def construct(self):
        title = Text("Application Areas").to_edge(UP, buff=.5)
        Causality = Text("Causal Inference", font_size = 28)
        Science = Text("Science", font_size = 28).move_to(3 * LEFT + 2 * UP)
        Economics = Text("Economics", font_size = 28).move_to(3 * RIGHT + 2 * UP)
        Medicine = Text("Medicine", font_size = 28).move_to(3 * RIGHT + 2 * DOWN)
        CompSci = Text("CS and ML", font_size = 28).move_to(3 * LEFT + 2 * DOWN)

        Arrow1 = Arrow(start = 3 * LEFT + 2 * UP, end = ORIGIN, buff=.5)
        Arrow2 = Arrow(start = 3 * RIGHT + 2 * UP, end = ORIGIN, buff=.5)
        Arrow3 = Arrow(start = 3 * LEFT + 2 * DOWN, end = ORIGIN, buff=.5)
        Arrow4 = Arrow(start = 3 * RIGHT + 2 * DOWN, end = ORIGIN, buff=.5)

        self.add(title)
        self.play(Write(Science))
        self.end_fragment()
        self.play(Write(Economics))
        self.end_fragment()
        self.play(Write(Medicine))
        self.end_fragment()
        self.play(Write(CompSci))
        self.end_fragment()
        self.play(Write(Arrow1), Write(Arrow2), Write(Arrow3), Write(Arrow4))
        self.play(Create(Causality), runtime = 1)
        self.end_fragment()