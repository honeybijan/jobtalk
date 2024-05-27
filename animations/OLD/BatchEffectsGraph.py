from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *


class BatchEffectsGraph(PresentationScene):

    def construct(self):
        title = Text("Batch Effects").to_edge(UP, buff=.5)
        self.add(title)

        # Draw DAG
        X  = Vertex(r'X').shift(LEFT)
        Y  = Vertex(r'Y').shift(RIGHT)
        Batch  = RectVertex("Batch", color=WHITE).shift(UP)
        edge1 = Line(start=Batch.get_edge_center(DOWN) + .2 * LEFT, end=X, buff=0)
        edge1.add_tip(tip_length = .1, tip_width=.1)
        edge2 = Line(start=Batch.get_edge_center(DOWN) + .2 * RIGHT, end=Y, buff=0)
        edge2.add_tip(tip_length = .1, tip_width=.1)
        edge3 = Edge(X, Y)
        causal_dag = VGroup(X, Y, Batch, edge1, edge2, edge3)
        causal_dag.shift(DOWN).scale(2)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        # Remove both
        edge1.generate_target()
        edge2.generate_target()
        edge1.target.set_opacity(.3)
        edge2.target.set_opacity(.3)
        self.play(MoveToTarget(edge1), MoveToTarget(edge2), runtime = 1)
        self.end_fragment()

        # Remove Incoming X
        edge2.generate_target()
        edge2.target.set_opacity(1)
        self.play(MoveToTarget(edge2), runtime = 1)
        self.end_fragment()

        # Remove Incoming Y
        # Remove Incoming X
        indep = MathTex(r'Y \perp \!\!\!\! \perp \text{Batch} \; | \; X').next_to(causal_dag, DOWN)
        edge1.generate_target()
        edge2.generate_target()
        edge1.target.set_opacity(1)
        edge2.target.set_opacity(.3)
        self.play(Write(indep))
        self.play(MoveToTarget(edge1), MoveToTarget(edge2), runtime = 1)
        self.end_fragment()