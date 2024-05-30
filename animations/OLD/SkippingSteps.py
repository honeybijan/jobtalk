from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class SkippingSteps(PresentationScene):

    def construct(self):
        title = Text("A Shortcut").to_edge(UP, buff=.5)

        Models = Ellipse(width = 3, height = 5, color=WHITE).move_to(DOWN)
        ModelsLabel = Text("Models", font_size = 28).next_to(Models, UP)
        ModsOval = VGroup(Models, ModelsLabel)

        Stats = Ellipse(width = 3, height = 5, color=WHITE).move_to(5 * RIGHT + DOWN)
        StatsLabel = Text("Observed Statistics", font_size = 28).next_to(Stats, UP)
        StatsOval = VGroup(Stats, StatsLabel)

        Results = Ellipse(width = 3, height = 5, color=WHITE).move_to(5 * LEFT + DOWN)
        ResultsLabel = Text("Causal Quantities", font_size = 28).next_to(Results, UP)
        ResultsOval = VGroup(Results, ResultsLabel)

        Start_Ovals = VGroup(ModsOval, StatsOval)
        
        self.add(title, Start_Ovals)


        Model1 = Dot(Models.get_center() + 2 * UP, radius = .15, color=BLUE)
        Model2 = Dot(Models.get_center(), color=RED, radius = .15)
        Model3 = Dot(Models.get_center() + 2 * DOWN, color=GREEN, radius = .15)
        Stat1 = Dot(Stats.get_center() + 1.2 * UP, radius = .5, color=BLUE).set_opacity(.3)
        Stat2 = Dot(Stats.get_center() + .8 * UP, radius = .5, color=RED).set_opacity(.3)
        Stat3 = Dot(Stats.get_center() + 2 * DOWN, radius = .5, color=GREEN).set_opacity(.3)
        Results1 = Dot(Results.get_center() + 1.2 * UP, radius = .15, color=BLUE)
        Results2 = Dot(Results.get_center() + .8 * UP, radius = .15, color=RED)
        Results3 = Dot(Results.get_center() + 2 * DOWN, radius = .15, color=GREEN)
        Models_And_Stats_Points = VGroup(Model1, Model2, Model3, Stat1, Stat2, Stat3)
        Results_Points = VGroup(Results1, Results2, Results3)

        Arrow1 = Arrow(start = Model1, end = Stat1, buff=.1, color = BLUE)
        Arrow2 = Arrow(start = Model2, end = Stat2, buff=.1, color = RED)
        Arrow3 = Arrow(start = Model3, end = Stat3, buff=.1, color = GREEN)
        Arrows = VGroup(Arrow1, Arrow2, Arrow3)

        lArrow1 = Arrow(start = Model1, end = Results1, buff=.1, color = BLUE)
        lArrow2 = Arrow(start = Model2, end = Results2, buff=.1, color = RED)
        lArrow3 = Arrow(start = Model3, end = Results3, buff=.1, color = GREEN)
        lArrows = VGroup(lArrow1, lArrow2, lArrow3)

        self.add(Models_And_Stats_Points, Arrows)

        self.play(Create(Results), Create(ResultsLabel), runtime = 1)
        self.play(Create(Results_Points), Create(lArrows), runtime = 1)
        self.end_fragment()

        Everything = VGroup(Start_Ovals, ResultsOval, Models_And_Stats_Points, Results_Points, Arrows, lArrows)
        Everything.generate_target()
        Everything.target.scale(.7).shift(UP)
        self.play(MoveToTarget(Everything))
        cite = Text('"Synthetic Potential Outcomes"').scale(.8).to_edge(DOWN, buff=1)
        self.play(Write(cite))
        self.end_fragment()

        