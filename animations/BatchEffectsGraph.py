from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *

def fade_to_gray(list_of_edges):
    for edge in list_of_edges:
        edge.generate_target()
        edge.target.set_opacity(.3)
    return [MoveToTarget(edge) for edge in list_of_edges]

def fade_back(list_of_edges):
    for edge in list_of_edges:
        edge.generate_target()
        edge.target.set_opacity(1)
    return [MoveToTarget(edge) for edge in list_of_edges]

class BatchEffectsGraph(PresentationScene):

    def construct(self):
        title = Text("Shared Signals").to_edge(UP, buff=.5)
        self.add(title)


         # Draw DAG
        def dag_generator(clab, xlab, ylab):
            c  = RectVertex(clab).shift(1.5 * UP)
            x  = RectVertex(xlab).shift(1.5 * LEFT)
            y  = RectVertex(ylab).shift(1.5 * RIGHT)

            cx = Line(start=c.get_edge_center(DOWN) + .2 * LEFT, end = x.get_edge_center(UP), buff=0)
            cx.add_tip(tip_length = .1, tip_width=.1)
            cy = Line(start=c.get_edge_center(DOWN) + .2 * RIGHT, end = y.get_edge_center(UP), buff=0)
            cy.add_tip(tip_length = .1, tip_width=.1)
            xy = Line(start=x.get_edge_center(RIGHT), end = y.get_edge_center(LEFT), buff=0)
            xy.add_tip(tip_length = .1, tip_width=.1)

            cd = VGroup(c, x, y, cx, cy, xy)
            cd.scale(1.5).move_to(ORIGIN)
            return cd, cx, cy, xy

        causal_dag, cx, cy, xy = dag_generator("Batch", "Drug", "scRNA")
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        # Remove both
        self.play(*fade_to_gray([cx, cy]), runtime = 1)
        self.end_fragment()

        causal_dag.generate_target()
        causal_dag.target.to_edge(LEFT, buff=1)
        self.play(MoveToTarget(causal_dag))

        ten_batches = VGroup(*[Dot(radius = .15, color=random_bright_color()) for i in range(10)]).arrange(DOWN, buff = .25)
        ten_drugs = VGroup(*[Dot(radius = .15, color=random_bright_color()) for i in range(10)]).arrange(DOWN, buff = .25)
        diag = VGroup(ten_batches, ten_drugs).arrange(RIGHT, buff = 2)
        drug_to_batches = dict()
        for drug in ten_drugs:
            drug_to_batches[drug] = [[], []]
        lines = []
        for batch in ten_batches:
            for i in np.random.choice(10, 4):
                lines.append(Line(batch, ten_drugs[i]))
                drug_to_batches[ten_drugs[i]][0].append(batch)
                drug_to_batches[ten_drugs[i]][1].append(lines[-1])
        connections = VGroup(*lines)
        batches_label = Text("Batches").scale(.5).next_to(ten_batches, LEFT)
        drugs_label = Text("Drugs").scale(.5).next_to(ten_drugs, RIGHT)
        diagram = VGroup(ten_batches, ten_drugs, connections, batches_label, drugs_label).to_edge(RIGHT, buff = .5)
        self.play(Write(diagram))
        self.end_fragment()

        # fade all but drug 1 and its batches
        selected_drug = ten_drugs[4]
        for drug in ten_drugs:
            drug.generate_target()
            if drug != selected_drug:
                drug.target.set_opacity(.3)
        for batch in ten_batches:
            batch.generate_target()
            if batch not in drug_to_batches[selected_drug][0]:
                batch.target.set_opacity(.3)
        for con in connections:
            con.generate_target()
            if con not in drug_to_batches[selected_drug][1]:
                con.target.set_opacity(.3)
        self.play(*[MoveToTarget(d) for d in ten_drugs], *[MoveToTarget(b) for b in ten_batches], *[MoveToTarget(c) for c in connections])
        self.end_fragment()

        self.play(*fade_to_gray([xy]))
        self.end_fragment()

        self.play(FadeOut(diagram))
        causal_dag.generate_target()
        causal_dag.target.center()
        self.play(MoveToTarget(causal_dag))

        # Remove Incoming X
        self.play(*fade_back([cx, cy, xy]), runtime = 1)
        self.end_fragment()
        self.play(*fade_to_gray([cx]))
        self.end_fragment()
        
        self.play(*fade_back([cx]))
        indep = Tex("Outcome " + r"$\perp \!\!\!\! \perp$" +  " Batch " + r"$\; | \;$" + " Drug").next_to(causal_dag, DOWN)
        self.play(Write(indep))
        self.play(*fade_to_gray([cy]), runtime = 1)
        self.end_fragment()

        def dag_and_eq(clab, xlab, ylab):
            causal_dag, cx, cy, xy = dag_generator(clab=clab, xlab=xlab, ylab=ylab)
            cy.set_opacity(.3)
            indep = Tex(ylab + " " + r"$\perp \!\!\!\! \perp$" +  " " + xlab + " " + r"$\; | \;$" + " " + clab).next_to(causal_dag, DOWN)
            return VGroup(causal_dag, indep)
        
        current_dag_and_eq = VGroup(causal_dag, indep)
        fairness = dag_and_eq("Protected", "Ability", "Performance")
        self.play(TransformMatchingShapes(current_dag_and_eq, fairness))
        self.end_fragment()

        sports = dag_and_eq("Game", "Participants", "Results")
        self.play(TransformMatchingShapes(fairness, sports))
        self.end_fragment()

        self.play(Write(Text("https://www.lacctic.com/", color=BLUE).scale(.5).to_edge(DOWN, buff=1)))
        self.end_fragment()
