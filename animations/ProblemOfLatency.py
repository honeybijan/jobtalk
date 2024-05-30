from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random

from GraphManim import *

class ProblemOfLatency(PresentationScene):

    def construct(self):
        title = Text("The Problem of Latency").to_edge(UP, buff=.5)
        self.add(title)
        
        # Draw DAG
        X  = Vertex(r'X').shift(LEFT)
        Y  = Vertex(r'Y').shift(RIGHT)
        C  = Vertex(r'C').shift(UP)
        XY = Edge(X, Y, redraw=False)
        CX = Edge(C, X, redraw=False)
        CY = Edge(C, Y, redraw=False)
        causal_dag = VGroup(X, Y, C, XY, CX, CY)
        causal_dag.move_to(ORIGIN).scale(2)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        causal_dag.generate_target()
        causal_dag.target.shift(UP)
        self.play(MoveToTarget(causal_dag))

        # Draw DAG
        uX  = Vertex(r'X', observed = False).shift(LEFT)
        uY  = Vertex(r'Y', observed = False).shift(RIGHT)
        uC  = Vertex(r'C', observed = False).shift(UP)
        uXY = Edge(uX, uY, observed = False)
        uCX = Edge(uC, uX, observed = False)
        uCY = Edge(uC, uY, observed = False)
        u_causal_dag = VGroup(uX, uY, uC, uXY, uCX, uCY).scale(2).move_to(causal_dag)
        self.play(TransformMatchingShapes(causal_dag, u_causal_dag))
        self.end_fragment()

        Vs = VGroup(*[Vertex(r"V_" + str(i)) for i in range (10)]).arrange(RIGHT).next_to(u_causal_dag, DOWN).shift(DOWN)
        tops = VGroup(X, Y, C)
        pair_list = [(0, 0), (0, 1), (0, 2), (2, 3), (2, 4), (0, 3), (1, 5), (1, 4), (1, 2), (1, 8), (2, 6), (2, 7), (2, 8), (1, 9) ]
        V_edges = VGroup(*[Edge(tops[i], Vs[j]) for i, j in pair_list])
        self.play(Write(Vs), Write(V_edges))
        self.end_fragment()



