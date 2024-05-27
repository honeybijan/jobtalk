from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *

class RectVertex(VGroup):
    def __init__(self, label, observed=True, **kwargs):
        VGroup.__init__(self, **kwargs)
        Label = Text(label, font_size = 18, color=WHITE)
        Outer_Rect = SurroundingRectangle(Label, buff = .1, color=WHITE)
        if not observed:
            Outer_Rect = DashedVMobject(Outer_Rect, num_dashes = 10)
        self.add(Label)
        self.add(Outer_Rect)
    
    def highlight(self, color):
        return self.set_color(color) #[self.Label.animate.set_color(color), self.Outer_Circle.animate.set_color(color)]
    
    def unhighlight(self):
        return self.highlight(WHITE)
    
    def condition(self):
        return [self.Outer_Rect.animate.set_fill_opacity(1), self.Label.animate.set_color(BLACK)]
    
    def uncondition(self):
        return [self.Outer_Rect.animate.set_fill_opacity(0), self.Label.animate.set_color(WHITE)]
    
def dist_sq(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

class RectEdge(VGroup):
    def __init__(self, Vertex1, Vertex2, observed=True, label=None, label_loc = UP, curve=None, **kwargs):
        VGroup.__init__(self, **kwargs)
        dist_points = [(dist_sq(Vertex1.get_center(), p2), p2) for p2 in [Vertex2.get_edge(UP), Vertex2.get_edge(DOWN), Vertex2.get_edge(LEFT), Vertex2.get_edge(RIGHT)]]
        end_point = min(dist_points)[1]
        dist_points = [(dist_sq(Vertex2.get_center(), p2), p2) for p2 in [Vertex1.get_edge(UP), Vertex1.get_edge(DOWN), Vertex1.get_edge(LEFT), Vertex1.get_edge(RIGHT)]]
        start_point = min(dist_points)[1]
        if not curve:
            if observed:
                Edge_Arrow = Line(start=start_point, end=end_point, buff=0)
            else:
                Edge_Arrow = DashedLine(start=start_point, end=end_point, buff=0)
        else:
            Edge_Arrow = ArcBetweenPoints(start=start_point, end=end_point, buff=0, angle=curve)
        Edge_Arrow.add_tip(tip_width = .1, tip_length=.05)
        self.add(Edge_Arrow)
        if label:
            self.Label = Text(label, font_size = 18, color=WHITE).next_to(Edge_Arrow, label_loc)
            self.Label.next_to(Edge_Arrow, label_loc)
            self.add(self.Label)
    
    def highlight(self, color):
        return [self.Label.animate.set_color(color), self.Outer_Circle.animate.set_color(color)]
    
    def unhighlight(self):
        return self.highlight(WHITE)
    
    def condition(self):
        return [self.Outer_Circle.animate.set_fill_opacity(1), self.Label.animate.set_color(BLACK)]
    
    def uncondition(self):
        return [self.Outer_Circle.animate.set_fill_opacity(0), self.Label.animate.set_color(WHITE)]

class EmergenceOfConfounding(PresentationScene):

    def construct(self):
        title = Text("Confounding Emergence").to_edge(UP, buff=.5)
        self.add(title)

        values = []
        for value_set in range(3):
            values.append([])
            for i in range(100):
                values[value_set].append((10 * np.random.normal() + 70 - (20 * value_set), 10 * np.random.normal() + 70 - (20 * value_set)))
        print(values)
        # Animate the creation of Axes
        ax = Axes(x_range=[-5, 100, 5], y_range=[-5, 100, 10]).scale(.8).to_edge(DOWN, buff = 1)
        icecream_label = Text("Ice Cream Sales").scale(.5).to_edge(DOWN, buff = .5)
        sunblock_label = Text("Sunblock Sales").scale(.5).rotate(math.pi/2).to_edge(LEFT, buff = 2).shift(.5 * DOWN)
        labels = VGroup(icecream_label, sunblock_label)
        self.play(Write(ax), Write(labels))
        self.end_fragment()

        # Animate the creation of dots
        dots_list = []
        for vset in values:
            dots = [Dot(ax.c2p(x, y), color=BLUE) for x, y in vset]
            dots_list += dots
            self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=.05))
            self.end_fragment()
        FullGraph = VGroup(*dots_list, ax, labels)
        FullGraph.generate_target()
        FullGraph.target.scale(.5).to_edge(LEFT, buff = .5)
        self.play(MoveToTarget(FullGraph))

        # Draw DAG
        TreatV  = RectVertex("Ice Cream").shift(LEFT)
        OutcomeV  = RectVertex("Sunblock").shift(RIGHT)
        ConditionV  = RectVertex("Season").shift(UP)
        edge1 = Line(start=ConditionV.get_edge_center(DOWN) + .2 * LEFT, end=TreatV.get_edge_center(UP), buff=0)
        edge1.add_tip(tip_length = .1, tip_width=.1)
        edge2 = Line(start=ConditionV.get_edge_center(DOWN) + .2 * RIGHT, end=OutcomeV.get_edge_center(UP), buff=0)
        edge2.add_tip(tip_length = .1, tip_width=.1)
        causal_dag = VGroup(TreatV, OutcomeV, ConditionV, edge1, edge2)
        causal_dag.to_edge(RIGHT, buff=2).shift(DOWN)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()