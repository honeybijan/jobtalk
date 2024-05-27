from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *
from icons import *


class ApproachesToCausality(PresentationScene):

    def construct(self):
        title = Text("Approaches to Causlaity").to_edge(UP, buff=.5)
        self.add(title)

        # Three techniques (add later)
        RCTs = Text("Gold Standard: Randomized Controled Trials")
        Instruments = Text("Instrumental Variables")
        CovAdjustments = Text("Covariate Adjustments / Reweighting")
        all_techniques = VGroup(RCTs, Instruments, CovAdjustments)
        all_techniques.arrange(DOWN, center=False, aligned_edge=LEFT)


        # People to sort
        num_participants = 40
        starting_pool = StickFigure.group_of_sticks(n=num_participants, width=20, scale=.5, v_sep=1, h_sep=.5, red_prob=.5).next_to(title, DOWN)
        self.add(starting_pool)
        treated_group_placeholder = StickFigure.group_of_sticks(n=int(num_participants/2), width=10, scale=.5, v_sep=1, h_sep=.5).to_corner(DL, buff = 1)
        control_group_placeholder = StickFigure.group_of_sticks(n=int(num_participants/2), width=10, scale=.5, v_sep=1, h_sep=.5).to_edge(DR, buff = 1)
        treated_rect = SurroundingRectangle(treated_group_placeholder, color=WHITE, buff=0.1, corner_radius=0.1)
        treated_label = Pill().scale(.7).next_to(treated_rect, UP)#Text("Treated", font_size=18).next_to(treated_rect, UP)
        treated_section = VGroup(treated_rect, treated_label)
        control_rect = SurroundingRectangle(control_group_placeholder, color=WHITE, buff=0.1, corner_radius=0.1)
        control_label = Pill(treated = False).scale(.5).next_to(control_rect, UP)
        control_section = VGroup(control_rect, control_label)
        self.play(Write(treated_section), Write(control_section))
        treated_group = VGroup()
        control_group = VGroup()
        for r, i in enumerate(np.random.permutation(num_participants)):
            stick = starting_pool[r]
            stick.generate_target()
            if i % 2 == 0:
                stick.target.move_to(treated_group_placeholder[int(i/2)])
                treated_group.add(stick)
            else:
                stick.target.move_to(control_group_placeholder[int(i/2)])
                control_group.add(stick)
        self.play(LaggedStart(*[MoveToTarget(stick) for stick in starting_pool]), runtime = 2)
        self.end_fragment()

        # Draw DAG
        severity  = RectVertex("Severity").scale(1.5).shift(UP)
        treatment  = RectVertex("Treatment").scale(1.5).shift(LEFT)
        outcome  = RectVertex("Outcome").scale(1.5).shift(RIGHT)
        severity_treatment = Line(start=severity.get_edge_center(DOWN) + .2 * LEFT, end = treatment.get_edge_center(UP))
        severity_treatment.add_tip(tip_length = .15, tip_width=.15)
        severity_outcome = Line(start=severity.get_edge_center(DOWN) + .2 * RIGHT, end = outcome.get_edge_center(UP))
        severity_outcome.add_tip(tip_length = .15, tip_width=.15)
        treatment_outcome = Line(start=treatment.get_edge_center(RIGHT), end = outcome.get_edge_center(LEFT), buff=0)
        treatment_outcome.add_tip(tip_length = .15, tip_width=.15)
        causal_dag = VGroup(severity, treatment, outcome, severity_outcome, severity_treatment, treatment_outcome)
        causal_dag.next_to(title, 1.5 * DOWN, buff=.5)
        self.play(Write(causal_dag))
        self.end_fragment()

        self.play(Unwrite(severity_treatment))
        self.end_fragment()

        self.play(Write(RCTs))