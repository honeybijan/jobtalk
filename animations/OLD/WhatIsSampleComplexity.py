from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class WhatIsSampleComplexity(PresentationScene):

    def construct(self):
        title = Text("What is Sample Complexity?").to_edge(UP, buff=.5)
        Models = Ellipse(width = 3, height = 5, color=WHITE).move_to(3 * LEFT + DOWN)
        ModelsLabel = Text("Models", font_size = 28).next_to(Models, UP)
        Stats = Ellipse(width = 3, height = 5, color=WHITE).move_to(3 * RIGHT + DOWN)
        StatsLabel = Text("Observed Statistics", font_size = 28).next_to(Stats, UP)
        self.add(title, Models, ModelsLabel, Stats, StatsLabel)


        Model1 = Dot(3 * LEFT + 1 * UP, radius = .3, color=BLUE)
        Model2 = Dot(3 * LEFT + 3 * DOWN, radius = .3, color=RED)
        Stat1 = Dot(3 * RIGHT + .5 * DOWN, radius = .3, color=BLUE)
        Stat2 = Dot(3 * RIGHT + 1.5 * DOWN, radius = .3, color=RED)
        Arrow1 = Arrow(start = Model1, end = Stat1, buff=.2, color = BLUE)
        Arrow2 = Arrow(start = Model2, end = Stat2, buff=.2, color = RED)
        self.add(Model1, Model2, Stat1, Stat2, Arrow1, Arrow2)

        Stat1.generate_target()
        Stat1.target.set_opacity(.3)
        Stat1.target.scale(3)

        Stat2.generate_target()
        Stat2.target.set_opacity(.3)
        Stat2.target.scale(3)

        Arrow1.generate_target()
        Arrow1.target.put_start_and_end_on(Arrow1.get_start(), Stat1.target.get_edge_center(LEFT))
        Arrow2.generate_target()
        Arrow2.target.put_start_and_end_on(Arrow2.get_start(), Stat2.target.get_edge_center(LEFT))
        self.play(*[MoveToTarget(t) for t in [Stat1, Stat2, Arrow1, Arrow2]], runtime = 1)
        self.end_fragment()