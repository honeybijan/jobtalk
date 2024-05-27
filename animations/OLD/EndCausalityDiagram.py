from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class EndCausalityDiagram(PresentationScene):

    def construct(self):
        title2 = Text("Application-driven Theory").to_edge(UP, buff=.5)
        title1 = Text("Theory-driven Application").to_edge(UP, buff=.5)
        Causality = Text("Causal Inference", font_size = 28)
        Science = Text("Science", font_size = 28).move_to(3 * LEFT + 2 * UP)
        Economics = Text("Economics", font_size = 28).move_to(3 * RIGHT + 2 * UP)
        Medicine = Text("Medicine", font_size = 28).move_to(3 * RIGHT + 2 * DOWN)
        CompSci = Text("CS and ML", font_size = 28).move_to(3 * LEFT + 2 * DOWN)

        Arrow1 = Arrow(start = 3 * LEFT + 2 * UP, end = ORIGIN, buff=.5)
        Arrow2 = Arrow(start = 3 * RIGHT + 2 * UP, end = ORIGIN, buff=.5)
        Arrow3 = Arrow(start = 3 * LEFT + 2 * DOWN, end = ORIGIN, buff=.5)
        Arrow4 = Arrow(start = 3 * RIGHT + 2 * DOWN, end = ORIGIN, buff=.5)
        Arrows = [Arrow1, Arrow2, Arrow3, Arrow4]

        everything = VGroup(Causality, Science, Economics, Medicine, CompSci, Arrow1, Arrow2, Arrow3, Arrow4).scale(1.2)
        Targets = [DoubleArrow(start = a.get_start(), end=a.get_end()) for a in Arrows]

        self.add(everything, title2)
        self.play(*[TransformMatchingShapes(A, T) for A,T in zip(Arrows, Targets)], TransformMatchingShapes(title2, title1), runtime = 1)
        self.end_fragment()