from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random

from GraphManim import *

class SPOsMulti(PresentationScene):

    def construct(self):
        title = Text("More Irrelevance...More Power").to_edge(UP, buff=.5)
        self.add(title)
        T = Vertex(label = r"T")
        Y = Vertex(label = r'Y')
        X1 = Vertex(label = r'X_1')
        X2 = Vertex(label = r'X_2')
        X = VGroup(X1, X2)
        Z1 = Vertex(label = r'Z_1')
        Z2 = Vertex(label = r'Z_2')
        Xref = VGroup(Z1, Z2)
        VisibleSubvertices = VGroup(T, Y, X1, X2, Z1, Z2).arrange(RIGHT, buff=1.4)
        U = Vertex(label=r'U', observed=False).next_to(VisibleSubvertices, 2.5 * UP)
        Upper_Edges = VGroup(*[Edge(T, Y)])
        Upper_U_Edges = VGroup(*[Edge(U, V, observed = False) for V in VisibleSubvertices])
        ArbitraryConnections = VGroup(*[Edge(X1, X2, observed=False), 
                                        Edge(X2, X1, observed=False), 
                                        Edge(Z1, Z2, observed=False), 
                                        Edge(Z2, Z1, observed=False)])
        simplified_graph = VGroup(VisibleSubvertices, U, Upper_U_Edges, Upper_Edges, ArbitraryConnections).next_to(title, DOWN).shift(DOWN)

        # Second SPO
        self.play(FadeIn(simplified_graph))
        Xp1 = Vertex(label = r"X'_1")
        Xp2 = Vertex(label = r"X'_2")
        new_vertices = VGroup(Xp1, Xp2)
        vertex_line = [T, Y, X1, X2, Xp1, Xp2, Z1, Z2]

        for vertex in VisibleSubvertices:
            vertex.generate_target()
        NewVisibleSubvertices = VGroup(*[v.target for v in VisibleSubvertices[:4]], Xp1, Xp2, Z1.target, Z2.target).arrange(RIGHT, buff=1.4).move_to(VisibleSubvertices)
        new_edges = VGroup(Edge(Xp1, Xp2, observed=False, redraw=False), Edge(Xp2, Xp1, observed=False, redraw=False), Edge(U, Xp1, observed=False, redraw=False), Edge(U, Xp2, observed=False, redraw=False))
        self.play(*[MoveToTarget(vertex) for vertex in VisibleSubvertices], Write(new_vertices), Write(new_edges))  
        self.end_fragment()


        U_vec = MobjectMatrix([[MathTex(r"\mathbb{P}(u^{(0)})").scale(.4), MathTex(r"\mathbb{P}(u^{(1)})").scale(.4)]], bracket_h_buff=0.05, bracket_v_buff=0.05, h_buff=1).next_to(U, UP)
        P_vec = lambda ob: MobjectMatrix([[MathTex(r"\mathbb{E}(" + ob.get_label_text() + r"|u^{(0)})").scale(.4)], [MathTex(r"\mathbb{E}(" + ob.get_label_text() + r"|u^{(1)})").scale(.4)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=1).next_to(ob, 2 * DOWN)
        
        col_vecs = VGroup(*[P_vec(v) for v in vertex_line])
        self.play(Write(U_vec), Write(col_vecs))
        self.end_fragment()

        # Add cond ts
        self.play(T.condition(), runtime = .5)
        U_vec2 = MobjectMatrix([[MathTex(r"\mathbb{P}(u^{(0)} | t)").scale(.4), MathTex(r"\mathbb{P}(u^{(1)}|t)").scale(.4)]], bracket_h_buff=0.05, bracket_v_buff=0.05, h_buff=1).move_to(U_vec)
        Y_vec2 = MobjectMatrix([[MathTex(r"\mathbb{E}(Y^{(t)} | u^{(0)})").scale(.4)], [MathTex(r"\mathbb{E}(Y^{(t)} | u^{(1)})").scale(.4)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=1).set_color(GREEN).move_to(col_vecs[1])
        self.play(TransformMatchingShapes(U_vec, U_vec2), TransformMatchingShapes(col_vecs[1], Y_vec2), FadeOut(col_vecs[0]))
        self.end_fragment()

        X_vecs = VGroup(col_vecs[2], col_vecs[3])
        Xp_vecs = VGroup(col_vecs[4], col_vecs[5])
        copy_y_X = Y_vec2.copy().move_to(X_vecs)
        copy_y_Xp = Y_vec2.copy().move_to(Xp_vecs)
        self.play(TransformMatchingShapes(X_vecs, copy_y_X))
        self.end_fragment()

        self.play(TransformMatchingShapes(Xp_vecs, copy_y_Xp))
        self.end_fragment()

        self.play(TransformMatchingShapes(copy_y_Xp, Xp_vecs))
        two_ys = VGroup(Y_vec2, copy_y_X)
        odot = MathTex(r"\odot", color=ORANGE).move_to(two_ys)
        Y_vec2.generate_target()
        copy_y_X.generate_target()
        Y_vec2.target.set_color(ORANGE)
        copy_y_X.target.set_color(ORANGE)
        self.play(Write(odot), MoveToTarget(Y_vec2), MoveToTarget(copy_y_X))
        self.end_fragment()

        copy_y2_Xp = MobjectMatrix([[MathTex(r"\mathbb{E}(Y^{(t)} | u^{(0)})^2").scale(.4)], [MathTex(r"\mathbb{E}(Y^{(t)} | u^{(1)})^2").scale(.4)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=1).set_color(ORANGE)
        copy_y2_Xp.move_to(Xp_vecs)
        self.play(TransformMatchingShapes(Xp_vecs, copy_y2_Xp))
        self.end_fragment()

        what_I_get = MathTex(r"\mathbb{M}[(Y^{(1)} - Y^{(0)})(Y^{(1)} - Y^{(0)})]", color=ORANGE).to_edge(DOWN, buff = 1)
        self.play(Write(what_I_get))
        self.end_fragment()



