from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP
from random import shuffle

config.video_dir = "./videos"
from GraphManim import *
import random


class Vertex(VGroup):
    def __init__(self, label, observed=True, radius = .2, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.label_text = label
        self.Outer_Circle = Circle(radius = radius, color = WHITE)
        if not observed:
            self.Outer_Circle = DashedVMobject(self.Outer_Circle, num_dashes = 20)
        self.add(self.Outer_Circle)
        self.Label = MathTex(label, font_size = 18, color=WHITE)
        self.Label.move_to(self.get_center())
        #self.Label.add_updater(lambda mob: mob.become(MathTex(self.label_text, font_size=18, color=mob.color)))
        self.add(self.Label)
        Cond_Circle = Circle(radius = radius, color = WHITE, fill_opacity=1)
        Cond_Label = MathTex(label, font_size = 18, color=BLACK)
        self.DarkMode = VGroup(Cond_Circle, Cond_Label)

    def reset_text(self, label):
        self.label_text = label
    
    def highlight(self, color):
        return self.set_color(color) #[self.Label.animate.set_color(color), self.Outer_Circle.animate.set_color(color)]
    
    def unhighlight(self):
        return self.highlight(WHITE)
    
    def condition(self):
        self.DarkMode.move_to(self.get_center())
        return Create(self.DarkMode)
    
    def uncondition(self):
        return Uncreate(self.DarkMode)
    
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
        Edge_Arrow.add_tip(tip_width = .1, tip_length=.1)
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
    
class Edge(VGroup):
    def __init__(self, Vertex1, Vertex2, observed=True, label=None, label_loc = UP, curve=None, **kwargs):
        VGroup.__init__(self, **kwargs)
        radius = Vertex1.get_width() / 2
        if not curve:
            if observed:
                Edge_Arrow = Line(start=Vertex1.get_center(), end=Vertex2.get_center(), buff=radius)
            else:
                Edge_Arrow = DashedLine(start=Vertex1.get_center(), end=Vertex2.get_center(), buff=radius)
        else:
            Edge_Arrow = ArcBetweenPoints(start=Vertex1.get_center(), end=Vertex2.get_center(), buff=radius, angle=curve)
        Edge_Arrow.add_tip(tip_width = .1, tip_length = .1)
        self.add(Edge_Arrow)
        if label:
            self.Label = MathTex(label, font_size = 18, color=WHITE).next_to(Edge_Arrow, label_loc)
            self.add(self.Label)
    
    def highlight(self, color):
        return [self.Label.animate.set_color(color), self.Outer_Circle.animate.set_color(color)]
    
    def unhighlight(self):
        return self.highlight(WHITE)
    
    def condition(self):
        return [self.Outer_Circle.animate.set_fill_opacity(1), self.Label.animate.set_color(BLACK)]
    
    def uncondition(self):
        return [self.Outer_Circle.animate.set_fill_opacity(0), self.Label.animate.set_color(WHITE)]


class Weather(PresentationScene):

    def construct(self):
        Burn = Text("Sun Burn", font_size=24)
        IceCream = Text("Ice Cream", font_size=24).next_to(Burn, RIGHT)
        labels = VGroup(Burn, IceCream).center().to_edge(UP)
        labels_and_underline = VGroup(labels, Underline(labels))
        self.play(Write(labels_and_underline), run_time=1)
        self.end_fragment()
        datas = ["11", "11", "10", "11", "11", "11", "11", "01"]
        Summer_Datas = VGroup()
        for step, data in enumerate(datas):
            colors = [BLUE, RED]
            burn_data = Text(str(data[0]), font_size=20, color = colors[int(data[0])]).next_to(Burn, DOWN).shift(.4 * step * DOWN)
            IceCream_data = Text(str(data[1]), font_size=20, color = colors[int(data[1])]).next_to(IceCream, DOWN).shift(.4 * step * DOWN)
            Summer_Datas.add(burn_data, IceCream_data)
            self.play(FadeIn(burn_data), FadeIn(IceCream_data), run_time=.5)
        self.end_fragment()
        datas = ["10", "01", "00", "00", "00", "00", "00", "00"]
        Winter_Datas = VGroup()
        for step, data in enumerate(datas):
            colors = [BLUE, RED]
            burn_data = Text(str(data[0]), font_size=20, color = colors[int(data[0])]).next_to(Burn, DOWN).shift(.4 * (8 + step) * DOWN)
            IceCream_data = Text(str(data[1]), font_size=20, color = colors[int(data[1])]).next_to(IceCream, DOWN).shift(.4 * (8 + step) * DOWN)
            Winter_Datas.add(burn_data, IceCream_data)
            self.play(FadeIn(burn_data), FadeIn(IceCream_data), run_time=.5)
        self.end_fragment()

        SummerBrace = Brace(Summer_Datas, direction = LEFT, color=RED)
        Summer = Text("Summer", font_size=24, color=RED).next_to(SummerBrace, LEFT)
        WinterBrace = Brace(Winter_Datas, direction = LEFT, color=BLUE)
        Winter = Text("Winter", font_size=24, color=BLUE).next_to(WinterBrace, LEFT)
        Braces = VGroup(Summer, SummerBrace, Winter, WinterBrace)
        self.play(Write(Braces), run_time = 1)
        self.end_fragment()

        # Move over to clear some space
        DataTable = VGroup(labels_and_underline, Summer_Datas, Winter_Datas, Braces)
        self.play(DataTable.animate.to_edge(LEFT), run_time=.5)

        # DAG
        burnV  = RectVertex("Sun Burn").shift(LEFT)
        iceV  = RectVertex("Ice Cream").shift(RIGHT)
        weatherV  = RectVertex("Season").shift(UP)
        edge1 = Line(start=weatherV.get_edge_center(DOWN) + .2 * LEFT, end=burnV.get_edge_center(UP), buff=0)
        edge1.add_tip(tip_length = .1, tip_width=.1)
        edge2 = Line(start=weatherV.get_edge_center(DOWN) + .2 * RIGHT, end=iceV.get_edge_center(UP), buff=0)
        edge2.add_tip(tip_length = .1, tip_width=.1)
        causal_dag = VGroup(burnV, iceV, weatherV, edge1, edge2)
        causal_dag.to_edge(UP).shift(3 * RIGHT).shift(DOWN)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        bd1 = MathTex(r'P(\text{Sun Burn} \;|\; do(\text{Ice Cream})) :=', font_size=28)
        bd2 = MathTex(r'P(\text{Summer})P(\text{Sun Burn} \;|\; \text{Summer, Ice Cream})', color=RED, font_size=28)
        bd3 = MathTex(r'+ P(\text{Winter})P(\text{Sun Burn} \;|\; \text{Winter, Ice Cream})', color=BLUE, font_size=28).next_to(bd2, DOWN)
        expansion = VGroup(bd2, bd3).next_to(bd1, DOWN)
        all_backdoor = VGroup(bd1, expansion)
        all_backdoor.next_to(causal_dag, DOWN)
        self.play(Write(bd1), run_time = 1, buff=.2)
        self.end_fragment()
        rect_summer = SurroundingRectangle(Summer_Datas, color = RED)
        self.play(Write(bd2), Write(rect_summer), run_time = 1)
        self.end_fragment()
        rect_winter = SurroundingRectangle(Winter_Datas, color = BLUE)
        self.play(Write(bd3), Write(rect_winter), run_time = 1)
        

        self.end_fragment()
