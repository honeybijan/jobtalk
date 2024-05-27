from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *


class InformationEngineering(PresentationScene):

    def construct(self):
        title = Text("Carving up Information").to_edge(UP, buff=.5)
        self.add(title)

        # Draw DAG
        X  = Vertex(r'X').shift(LEFT)
        Y  = Vertex(r'Y').shift(RIGHT)
        A  = Vertex(r'A', observed=False).shift(UP + LEFT)
        B  = Vertex(r'B', observed=False).shift(UP + RIGHT)
        XY = Edge(X, Y)
        AX = Edge(A, X, observed=False)
        AY = Edge(A, Y, observed=False)
        BY = Edge(B, Y, observed=False)
        causal_dag = VGroup(X, Y, A, B, XY, AX, AY, BY)
        causal_dag.move_to(ORIGIN).scale(2)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        PartialBlue = VGroup(X, Y, A, XY, AX, AY)
        PartialRed = VGroup(B, BY)
        PartialBlue.generate_target()
        PartialBlue.target.set_color(BLUE)
        PartialRed.generate_target()
        PartialRed.target.set_color(RED)
        self.play(MoveToTarget(PartialRed), MoveToTarget(PartialBlue), runtime=1)
        self.end_fragment()

        Cite = Text('Mazaheri, et. al. "Causal Information Splitting." (UAI 2023).', font_size = 24).next_to(causal_dag, 2 * DOWN)
        self.play(Create(Cite), runtime = 1)
        self.end_fragment()
