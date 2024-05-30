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
        title = Text("Approaches to Causal Inference").to_edge(UP, buff=.5)
        self.add(title)

        # Three techniques (add later)
        RCTs = Text("Randomized Controled Trials").scale(.5)
        RCT_cite = Paragraph("Fisher, R. A. (1931). The technique of field experiments.\nHarpenden: Rothamsted Experimental Station, 11-13.").scale(.25)
        Instruments = Text("Instrumental Variables").scale(.5)
        Instrument_cite = Paragraph("Angrist, J., & Imbens, G. (1995). Identification and estimation of\n local average treatment effects. Econometrica. 62 (2): 467–476.").scale(.25)
        ipw = Text("Inverse Probability Weighting").scale(.5)
        IPW_cite = Paragraph("Hernán, M. A., & Robins, J. M. (2010). Causal inference.").scale(.25)
        CovAdjustments = Text("Covariate Adjustments").scale(.5)
        CovAdjustments_cite = Paragraph("Pearl, J. (2009). Causality. Cambridge university press.").scale(.25)
        all_techniques = VGroup(RCTs, RCT_cite, Instruments, Instrument_cite, ipw, IPW_cite, CovAdjustments, CovAdjustments_cite)
        all_techniques.arrange(DOWN, center=True)


        # People to sort
        num_participants = 40
        starting_pool = StickFigure.group_of_sticks(n=num_participants, width=10, scale=.5, v_sep=1, h_sep=.5, red_prob=.5).center().to_edge(LEFT, buff=.5).shift(.5 * DOWN)
        self.add(starting_pool)
        treated_group_placeholder = StickFigure.group_of_sticks(n=int(num_participants/2), width=10, scale=.5, v_sep=1.2, h_sep=.5)
        control_group_placeholder = StickFigure.group_of_sticks(n=int(num_participants/2), width=10, scale=.5, v_sep=1.2, h_sep=.5)
        treated_rect = SurroundingRectangle(treated_group_placeholder, color=WHITE, buff=0.3, corner_radius=0.1)
        treated_label = Pill().scale(.7).next_to(treated_rect, LEFT)#Text("Treated", font_size=18).next_to(treated_rect, UP)
        treated_box = VGroup(treated_rect, treated_label)
        treated_section = VGroup(treated_box, treated_group_placeholder)
        control_rect = SurroundingRectangle(control_group_placeholder, color=WHITE, buff=0.3, corner_radius=0.1)
        control_label = Pill(treated = False).scale(.4).next_to(control_rect, LEFT)
        control_box = VGroup(control_rect, control_label)
        control_section = VGroup(control_box, control_group_placeholder)
        two_sections = VGroup(treated_section, control_section).arrange(DOWN).center().to_edge(RIGHT, buff = .5).shift(.5 * DOWN)
        self.play(Write(treated_box), Write(control_box))
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

        rand  = RectVertex("Random").scale(1.5).next_to(treatment, 2 * LEFT).set_color(YELLOW)
        rand_treatment = Line(start=rand.get_edge_center(RIGHT), end=treatment.get_edge_center(LEFT), buff=0)
        rand_treatment.add_tip(tip_length = .15, tip_width=.15)
        rand_and_edge = VGroup(rand, rand_treatment)

        instrument  = RectVertex("Instrument").scale(1.5).next_to(treatment, 2 * LEFT)
        instrument_treatment = Line(start=instrument.get_edge_center(RIGHT), end = treatment.get_edge_center(LEFT))
        instrument_treatment.add_tip(tip_length = .15, tip_width=.15)
        instrument_and_edge = VGroup(instrument, instrument_treatment).set_color(YELLOW)

        causal_dag = VGroup(severity, treatment, outcome, severity_outcome, severity_treatment, treatment_outcome)
        fullcausal_dag = VGroup(causal_dag, rand_and_edge, instrument_and_edge)
        fullcausal_dag.next_to(title, DOWN, buff=.5).to_edge(LEFT)
        self.play(Write(causal_dag))
        all_techniques.next_to(causal_dag, DOWN, buff=.5)
        self.end_fragment()

        self.play(Unwrite(severity_treatment))
        self.end_fragment()
        self.play(Write(rand_and_edge))

        self.play(Write(RCTs), FadeIn(RCT_cite))
        self.end_fragment()

        # Re-shuffle
        people_to_shift = list()
        bot_row_treated_y_coord = treated_group_placeholder[-1].get_center()[1]
        bot_row_control_y_coord = control_group_placeholder[-1].get_center()[1]
        for stick in treated_group:
            if stick.color == BLUE and stick.get_center()[1] == bot_row_treated_y_coord:
                stick.generate_target()
                stick.change_color(RED)
                stick.target.change_color(RED)
                people_to_shift.append(stick)
        for stick in control_group:
            if stick.color == RED and stick.get_center()[1] == bot_row_control_y_coord:
                stick.generate_target()
                stick.change_color(BLUE)
                stick.target.change_color(BLUE)
                people_to_shift.append(stick)
        severity_treatment = Line(start=severity.get_edge_center(DOWN) + .2 * LEFT, end = treatment.get_edge_center(UP))
        severity_treatment.add_tip(tip_length = .15, tip_width=.15)
        self.play(Unwrite(rand_and_edge), Write(severity_treatment), *[MoveToTarget(stick) for stick in people_to_shift])
        self.end_fragment()

        self.play(Write(instrument_and_edge), Write(severity_treatment))
        top_row_treated = SurroundingRectangle(treated_group_placeholder[:10], color=YELLOW, buff=0.1, corner_radius=0.1)
        top_row_control = SurroundingRectangle(control_group_placeholder[:10], color=YELLOW, buff=0.1, corner_radius=0.1)
        self.play(Write(top_row_control), Write(top_row_treated))
        self.end_fragment()

        self.play(Write(Instruments), FadeIn(Instrument_cite))
        self.end_fragment()

        self.play(Unwrite(top_row_control), Unwrite(top_row_treated), Unwrite(instrument_and_edge))
        self.end_fragment()

        # Covariate Adjustment
        for stick in treated_group:
            if stick.color == RED:
                stick.generate_target()
                stick.target.scale(.5)
            else:
                stick.generate_target()
                stick.target.scale(1.2)
        for stick in control_group:
            if stick.color == BLUE:
                stick.generate_target()
                stick.target.scale(.5)
            else:
                stick.generate_target()
                stick.target.scale(1.2)
        self.play(*[MoveToTarget(stick) for stick in treated_group], *[MoveToTarget(stick) for stick in control_group])
        self.end_fragment()

        self.play(Write(ipw), FadeIn(IPW_cite))
        self.play(Write(CovAdjustments), FadeIn(CovAdjustments_cite))
        CovAdjustments.generate_target()
        CovAdjustments.target.set_color(YELLOW)
        self.play(MoveToTarget(CovAdjustments), runtime = .5)
        self.end_fragment()

        # Color blind
        for stick in treated_group:
            stick.generate_target()
            stick.change_color(GRAY)
            stick.target.change_color(GRAY)
        for stick in control_group:
            stick.generate_target()
            stick.change_color(GRAY)
            stick.target.change_color(GRAY)
        severity_and_edges = VGroup(severity, severity_treatment, severity_outcome)
        severity_and_edges.generate_target()
        severity_and_edges.target.set_opacity(.3)
        self.play(MoveToTarget(severity_and_edges), 
                  *[MoveToTarget(stick) for stick in treated_group],
                  *[MoveToTarget(stick) for stick in control_group])
        self.end_fragment()

