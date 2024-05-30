from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *
from icons import *


class CausalModels(PresentationScene):

    def construct(self):
        title = Text("Causal Modeling and Interventions").to_edge(UP, buff=.5)
        self.add(title)

        # New DAG
        severity  = RectVertex("Severity").scale(1.5).shift(2* UP)
        treatment  = RectVertex("Treatment").scale(1.5).shift(2* LEFT)
        outcome  = RectVertex("Outcome").scale(1.5).shift(2* RIGHT)

        #season_temp._set_start_and_end_attrs(start=severity.get_edge_center(DOWN) + .2 * LEFT, end = treatment.get_edge_center(UP))
        severity_treatment = Line(start=severity.get_edge_center(DOWN) + .2 * LEFT, end = treatment.get_edge_center(UP))
        severity_treatment.add_tip(tip_length = .15, tip_width=.15)
        severity_outcome = Line(start=severity.get_edge_center(DOWN) + .2 * RIGHT, end = outcome.get_edge_center(UP))
        severity_outcome.add_tip(tip_length = .15, tip_width=.15)
        treatment_outcome = Line(start=treatment.get_edge_center(RIGHT), end = outcome.get_edge_center(LEFT), buff=0)
        treatment_outcome.add_tip(tip_length = .15, tip_width=.15)
        causal_dag = VGroup(severity, treatment, outcome, severity_outcome, severity_treatment, treatment_outcome).next_to(title, DOWN, buff = .7)
        self.play(Write(causal_dag), runtime = 1)
        self.end_fragment()

        # Move it over
        # Draw some people
        group_of_sticks_Treated = StickFigure.group_of_sticks(n=16, width=8, scale=.5, v_sep=1, h_sep=.5, red_prob=.75)
        group_of_sticks_Untreated = StickFigure.group_of_sticks(n=16, width=8, scale=.5, v_sep=1, h_sep=.5, red_prob=.25)
        group_of_sticks_Treated.to_corner(DL, buff = 1)
        group_of_sticks_Untreated.to_corner(DR, buff = 1)
        treated_rect = SurroundingRectangle(group_of_sticks_Treated, color=WHITE, buff=0.1, corner_radius=0.1)
        treated_label = Pill().scale(.7).next_to(treated_rect, UP)#Text("Treated", font_size=18).next_to(treated_rect, UP)
        treated_section = VGroup(treated_rect, treated_label)
        untreated_rect = SurroundingRectangle(group_of_sticks_Untreated, color=WHITE, buff=0.1, corner_radius=0.1)
        untreated_label = Pill(treated = False).scale(.5).next_to(untreated_rect, UP)#Text("Untreated", font_size=18).next_to(untreated_rect, UP)
        untreated_section = VGroup(untreated_rect, untreated_label)
        self.play(FadeIn(group_of_sticks_Treated), 
                  FadeIn(group_of_sticks_Untreated), 
                  FadeIn(treated_section), 
                  FadeIn(untreated_section))
        self.end_fragment()

        # Backdoor path
        treatment.generate_target()
        treatment.target.set_color(YELLOW)
        severity_treatment.generate_target()
        severity_treatment.target.set_color(YELLOW)
        treated_section.generate_target()
        treated_section.target.set_color(YELLOW)
        self.play(MoveToTarget(treatment), runtime=.5)
        self.play(*treatment.condition(), MoveToTarget(treated_section), runtime = .5)
        self.end_fragment()

        severity.generate_target()
        severity.target.set_color(YELLOW)
        bayes = Tex(r'Severity $|$ Treatment $\neq^d$ Severity', color=YELLOW).scale(.5).next_to(causal_dag, UP, buff=.25)
        self.play(MoveToTarget(severity_treatment), MoveToTarget(severity), Write(bayes), runtime=.5)
        self.end_fragment()

        severity_outcome.generate_target()
        severity_outcome.target.set_color(YELLOW)
        outcome.generate_target()
        outcome.target.set_color(YELLOW)
        print([stick.happy for stick in group_of_sticks_Treated])
        highlights = VGroup(*[BackgroundRectangle(stick, color=RED, fill_opacity = .4) for stick in group_of_sticks_Treated if not stick.happy])
        self.play(MoveToTarget(severity_outcome), MoveToTarget(outcome), FadeIn(highlights), runtime=.5)
        self.end_fragment()

        everything = VGroup(causal_dag, group_of_sticks_Treated, group_of_sticks_Untreated, treated_section, untreated_section, bayes, highlights)
        everything.generate_target()
        everything.target.scale(.8).shift(.5 * UP)
        self.play(MoveToTarget(everything), FadeOut(treatment.Cond_Label), FadeOut(treatment.Cond_Rect))
        backdoor_path = Text('"Backdoor Path"', color=YELLOW).scale(.5).next_to(everything, DOWN, buff = .5)
        cite = Paragraph("Pearl, J. (2009). Causality. Cambridge university press.").scale(.25).next_to(backdoor_path, DOWN)
        self.play(Write(backdoor_path), FadeIn(cite), runtime=1)
        self.end_fragment()

        #severity_treatment.generate_target()
        #severity_treatment.target.set_opacity(.3)
        #self.play(MoveToTarget(severity_treatment), runtime=.5)
        #self.end_fragment()