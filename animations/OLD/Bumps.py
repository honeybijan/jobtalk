from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP
import math
from GraphManim import *

config.video_dir = "./videos"

import random

def PDF_normal(x, mu, sigma):
    '''
    General form of probability density function of univariate normal distribution
    '''
    return math.exp(-((x-mu)**2)/(2*sigma**2))/(sigma*math.sqrt(2*math.pi))

class Bumps(PresentationScene):

    def construct(self):
        title = Text("Parametric Assumptions").to_edge(UP, buff=.5)
        ax = Axes(
            x_range = [-5, 5, 1],
            y_range = [0, 0.5, 0.1],
            axis_config = {'include_numbers':True}
        )
        self.add(title)

        # Draw graph
        curve1 = ax.plot(lambda x: PDF_normal(x, 2, 1), color=BLUE)
        curve2 = ax.plot(lambda x: PDF_normal(x, -2, 1), color=RED)
        graph = VGroup(ax, curve1, curve2).scale(.8)
        self.add(ax)
        self.play(Create(curve1), runtime=1)
        self.play(Create(curve2), runtime=1)
        self.end_fragment()

        # Draw DAG
        graph.generate_target()
        graph.target.to_edge(LEFT, buff = .5)
        self.play(MoveToTarget(graph), runtime = 1)
        U = Vertex(r'U', observed=False, radius=.5)
        V = Vertex(r'V', radius=.5).next_to(U, 3 * DOWN)
        E = Edge(U, V, tip_size=.2)
        G = Graph([U, V], [E], unobserved=U).move_to(ORIGIN).to_edge(RIGHT, buff=1)
        self.play(Create(G), runtime = .5)

        def AnimateRandomSample(red):
            if red:
                col = RED
                rand_value = random.gauss(-2, 1)
            else:
                col = BLUE
                rand_value = random.gauss(2, 1)
            new_dot = Dot(U.get_center(), radius = .5, color=col)
            num_dot = LabeledDot(Tex("{0:.1f}".format(round(rand_value, 1)), color = BLACK), color = col, radius=.5).move_to(V)
            self.play(Create(new_dot), runtime=.5)
            self.play(Create(num_dot), runtime=.5)
            num_dot.generate_target()
            num_dot.target.scale(.2).move_to(ax.coords_to_point(rand_value, 0, 0))
            self.play(FadeOut(new_dot), MoveToTarget(num_dot), runtime = 1)
            self.end_fragment()
        for r in [True, False]:
            AnimateRandomSample(r)

        def CreateRandomSample():
            red = random.random() > .5
            if red:
                col = RED
                rand_value = random.gauss(-2, 1)
            else:
                col = BLUE
                rand_value = random.gauss(2, 1)
            num_dot = LabeledDot(Tex("{0:.1f}".format(round(rand_value, 1)), color = BLACK), color = col, radius=.5).move_to(V)
            num_dot.generate_target()
            num_dot.target.scale(.2).move_to(ax.coords_to_point(rand_value, 0, 0))
            return num_dot
        
        dots = [CreateRandomSample() for i in range(50)]
        self.add(*dots)
        self.play(LaggedStart(*[MoveToTarget(dot) for dot in dots], lag_ratio=.05), runtime = 3)
        two_bumps = ax.plot(lambda x: (PDF_normal(x, 2, 1) + PDF_normal(x, -2, 1))/2, color=PURPLE)
        self.play(Create(two_bumps), runtime = 1)
        self.end_fragment()