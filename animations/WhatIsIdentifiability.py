from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class WhatIsIdentifiability(PresentationScene):

    def construct(self):
        title = Text("What is Identifiability?").to_edge(UP, buff=.5)
        Models = Ellipse(width = 3, height = 5, color=WHITE).move_to(3 * LEFT + DOWN)
        ModelsLabel = Text("Models", font_size = 28).next_to(Models, UP)
        Stats = Ellipse(width = 3, height = 5, color=WHITE).move_to(3 * RIGHT + DOWN)
        StatsLabel = Text("Observed Statistics", font_size = 28).next_to(Stats, UP)
        self.add(title, Models, ModelsLabel, Stats, StatsLabel)


        Model1 = Dot(3 * LEFT + 1 * UP, radius = .3, color=BLUE)
        Model2 = Dot(3 * LEFT + 3 * DOWN, radius = .3, color=RED)
        Stat1 = Dot(3 * RIGHT + 1 * UP, radius = .3, color=BLUE)
        Stat2 = Dot(3 * RIGHT + 3 * DOWN, radius = .3, color=RED)
        Arrow1 = Arrow(start = Model1, end = Stat1, buff=.2, color=BLUE)
        Arrow2 = Arrow(start = Model2, end = Stat2, buff=.2, color=RED)
        self.play(Create(Model1), Create(Model2), Create(Stat1), Create(Stat2), runtime=1)
        self.play(Create(Arrow1), Create(Arrow2), runtime=1)
        self.end_fragment()

        Stat1.generate_target()
        Stat1.target.set_color(PURPLE).move_to(3 * RIGHT + DOWN)
        Stat2.generate_target()
        Stat2.target.set_color(PURPLE).move_to(3 * RIGHT + DOWN)
        Arrow1.generate_target()
        Arrow1.target.put_start_and_end_on(Arrow1.get_start(), 3 * RIGHT + DOWN)
        Arrow2.generate_target()
        Arrow2.target.put_start_and_end_on(Arrow2.get_start(), 3 * RIGHT + DOWN)
        self.play(*[MoveToTarget(t) for t in [Stat1, Stat2, Arrow1, Arrow2]], runtime = 1)
        self.end_fragment()