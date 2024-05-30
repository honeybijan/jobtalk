from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random

from GraphManim import *

class SPOsSingle(PresentationScene):

    def construct(self):
        title = Text("Synthetic Potential Outcomes").to_edge(UP, buff=.5)
        self.add(title)

        T = Vertex(label = r"T")
        Y = Vertex(label = r'Y')
        X1 = Vertex(label = r'X_1')
        X2 = Vertex(label = r'X_2')
        X = VGroup(X1, X2)
        Z1 = Vertex(label = r'Z_1')
        Z2 = Vertex(label = r'Z_2')
        Xref = VGroup(Z1, Z2)
        VisibleSubvertices = VGroup(T, Y, X1, X2, Z1, Z2).arrange(RIGHT, buff=1.5)
        U = Vertex(label=r'U', observed=False).next_to(VisibleSubvertices, 2.5 * UP)

        A = Vertex(label=r"A")
        C = Vertex(label=r"C")
        V1 = Vertex(label=r"V_1")
        V2 = Vertex(label=r"V_2")
        V3 = Vertex(label=r"V_3")
        Extras = VGroup(A, C, V1, V2, V3).arrange(RIGHT, buff=1.5)
        Extras.next_to(VisibleSubvertices, 2 * DOWN)

        Upper_Edges = VGroup(*[Edge(T, Y)])
        Lower_Edges = VGroup(*[Edge(A, T), Edge(A, Y), Edge(Y, C), Edge(C, X1), Edge(V1, X1), Edge(X2, V1), Edge(X2, V2), Edge(Z1, V2), Edge(V3, Z1), Edge(V3, Z2)])
        FullGraph = VGroup(VisibleSubvertices, U, Extras, Upper_Edges, Lower_Edges)
        FullGraph.next_to(title, 3 * DOWN)
        BoxAround = SurroundingRectangle(VGroup(VisibleSubvertices, Extras), buff = .2, corner_radius=.1, color=WHITE)
        U_Edges = VGroup(*[DashedLine(start=U, end=BoxAround.get_edge_center(UP) + (2.5 * LEFT) + i * (RIGHT), buff = .1) for i in range(6)])
        for edge in U_Edges:
            edge.add_tip(tip_length = .1, tip_width=.1)
        self.add(FullGraph, BoxAround, U_Edges)

        self.play(A.condition(), C.condition())
        Upper_U_Edges = VGroup(*[Edge(U, V, observed = False) for V in VisibleSubvertices])
        ArbitraryConnections = VGroup(*[Edge(X1, X2, observed=False), 
                                        Edge(X2, X1, observed=False), 
                                        Edge(Z1, Z2, observed=False), 
                                        Edge(Z2, Z1, observed=False)])
        simplified_graph = VGroup(VisibleSubvertices, U, Upper_U_Edges, Upper_Edges, ArbitraryConnections)
        self.play(FadeOut(Lower_Edges), FadeOut(Extras), A.uncondition(), C.uncondition(), FadeOut(BoxAround), FadeOut(U_Edges), Write(Upper_U_Edges), Write(ArbitraryConnections), runtime=1)
        self.end_fragment()
        # Sit irrelevant
        BoxAroundX = SurroundingRectangle(X, buff = .2, corner_radius=.1)
        BoxAroundXref = SurroundingRectangle(Xref, buff = .2, corner_radius=.1)
        BoxAroundXTY = SurroundingRectangle(VGroup(T, Y), buff = .2, corner_radius=.1)
        self.play(Write(BoxAroundX), Write(BoxAroundXref), Write(BoxAroundXTY))
        sit_irrelevant = Text('"Situationally Irrelevant"', color = YELLOW).scale(.5).next_to(BoxAroundX, DOWN)
        self.play(Write(sit_irrelevant))
        self.end_fragment()

        # Vectorize
        self.play(FadeOut(BoxAroundX), FadeOut(BoxAroundXref), FadeOut(BoxAroundXTY), FadeOut(sit_irrelevant))
        U_vec = MobjectMatrix([[MathTex(r"\mathbb{P}(u^{(0)})").scale(.3), MathTex(r"\mathbb{P}(u^{(1)})").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, h_buff=0.7).next_to(U, UP)
        P_vec = lambda ob: MobjectMatrix([[MathTex(r"\mathbb{E}(" + ob.get_label_text() + r"|u^{(0)})").scale(.3)], [MathTex(r"\mathbb{E}(" + ob.get_label_text() + r"|u^{(1)})").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5).next_to(ob, DOWN)
        def E_vec(lb, cond=""):
            return MobjectMatrix([[MathTex(r"\mathbb{E}(" + lb + r"|" + cond + r" u^{(0)})").scale(.3)], [MathTex(r"\mathbb{E}(" + lb + r"|" + cond + r" u^{(1)})").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5)
        
        col_vecs = VGroup(*[P_vec(v) for v in VisibleSubvertices])
        self.play(Write(U_vec), Write(col_vecs))
        self.end_fragment()

        # Observed Moments
        first_order_eq = VGroup(
            Text("First Order Moments: ").scale(.5),
            MathTex(r"\mathbb{M}(Y) = "),
            U_vec.copy(),
            E_vec("Y")
        ).arrange(RIGHT)
        second_order_eq = VGroup(
            Text("Second Order Moments: ").scale(.5),
            MathTex(r"\mathbb{M}(YX) = "),
            U_vec.copy(),
            E_vec("Y"),
            MathTex(r"\odot"),
            E_vec("X")
        ).arrange(RIGHT)
        wanted_eq = VGroup(
            Text("Wanted: ").scale(.5),
            MathTex(r"\mathbb{M}(Y^{(t)}) = "),
            U_vec.copy(),
            E_vec("Y", cond = " t,")
        ).arrange(RIGHT).set_color(GREEN)
        eqs = VGroup(first_order_eq, second_order_eq, wanted_eq).arrange(DOWN, center=True).to_corner(DOWN, buff = .5)
        for eq in eqs:
            self.play(Write(eq))
            self.end_fragment()

        self.play(Unwrite(first_order_eq), Unwrite(second_order_eq))
        # Add cond ts
        self.play(T.condition(), runtime = .5)
        U_vec2 = MobjectMatrix([[MathTex(r"\mathbb{P}(u^{(0)} | t)").scale(.3), MathTex(r"\mathbb{P}(u^{(1)}|t)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, h_buff=0.7).move_to(U_vec)
        Y_vec2 = E_vec("Y", cond = " t,").set_color(GREEN).move_to(col_vecs[1])
        Y.generate_target()
        Y.target.set_color(GREEN)
        self.play(TransformMatchingShapes(U_vec, U_vec2), TransformMatchingShapes(col_vecs[1], Y_vec2), FadeOut(col_vecs[0]))
        self.end_fragment()

        # Linear Combination
        X1.generate_target()
        X1.target.set_color(YELLOW)
        X2.generate_target()
        X2.target.set_color(BLUE)
        col_vecs[2].generate_target()
        col_vecs[2].target.set_color(YELLOW)
        col_vecs[3].generate_target()
        col_vecs[3].target.set_color(BLUE)
        self.play(*[MoveToTarget(t) for t in [X1, X2, col_vecs[2], col_vecs[3]]])

        copyY = Y_vec2.copy()
        copyY.generate_target()
        copyX1 = col_vecs[2].copy()
        copyX1.generate_target()
        copyX2 = col_vecs[3].copy()
        copyX2.generate_target()
        want_alphas = VGroup(
            copyY.target,
            MathTex(r"= \alpha_1"),
            copyX1.target,
            MathTex(r"+ \alpha_2"),
            copyX2.target
        ).arrange(RIGHT)
        want_alpha_eq_structure = VGroup(want_alphas[1], want_alphas[3])
        moment_matching_1 = MathTex(r"\mathbb{M}(Y Z_1|t) = \alpha_1 \mathbb{M}(X_1 Z_1|t) + \alpha_2 \mathbb{M}(X_2 Z_1|t)").scale(.8)
        moment_matching_2 = MathTex(r"\mathbb{M}(Y Z_2|t) = \alpha_1 \mathbb{M}(X_1 Z_2|t) + \alpha_2 \mathbb{M}(X_2 Z_2|t)").scale(.8)
        moment_matching = VGroup(moment_matching_1, moment_matching_2).arrange(DOWN, center=True)
        alpha_derive = VGroup(want_alphas, moment_matching).arrange(DOWN, center=True).next_to(col_vecs, DOWN)
        self.play(Write(want_alpha_eq_structure), MoveToTarget(copyY), MoveToTarget(copyX1), MoveToTarget(copyX2))
        self.end_fragment()

        # Moment matching
        self.play(Write(moment_matching))
        self.end_fragment()

        # Rearrange as matrix equations
        moment_matching_matrix = VGroup(
            MobjectMatrix([[MathTex(r"\alpha_1").scale(.3)], [MathTex(r"\alpha_2").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = .7),
            MathTex("="),
            MobjectMatrix([[MathTex(r"\mathbb{M}(X_1 Z_1|t)").scale(.3), MathTex(r"\mathbb{M}(X_2 Z_1|t)").scale(.3)], [MathTex(r"\mathbb{M}(X_1 Z_2|t)").scale(.3), MathTex(r"\mathbb{M}(X_2 Z_2|t)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1),
            MobjectMatrix([[MathTex(r"\mathbb{M}(Y Z_1|t)").scale(.3)], [MathTex(r"\mathbb{M}(Y Z_2|t)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1)
        ).arrange(RIGHT)
        new_wanted = VGroup(
            MathTex(r"\mathbb{M}(Y^{(t)})", color = GREEN),
            MathTex(r"= \alpha_1"),
            MathTex(r"\mathbb{M}(X_1)", color=YELLOW),
            MathTex(r"+ \alpha_2"),
            MathTex(r"\mathbb{M}(X_2)", color = BLUE),
        ).arrange(RIGHT)
        final_eqs = VGroup(moment_matching_matrix, new_wanted).arrange(DOWN, center=True).center().to_edge(DOWN, buff = 1)
        inverse = MathTex(r"-1").scale(.3).next_to(moment_matching_matrix[2], RIGHT, buff=0.05).shift(.3 * UP)
        self.play(FadeOut(want_alphas), FadeOut(VGroup(copyX1, copyX2, copyY)), FadeIn(inverse), TransformMatchingShapes(moment_matching, moment_matching_matrix), TransformMatchingShapes(wanted_eq, new_wanted))
        self.end_fragment()


        moment_matching_matrix_a = VGroup(
            MobjectMatrix([[MathTex(r"\alpha_1").scale(.3)], [MathTex(r"\alpha_2").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1.4),
            MathTex("="),
            MobjectMatrix([[MathTex(r"\mathbb{M}(X_1 Z_1|T=1)").scale(.3), MathTex(r"\mathbb{M}(X_2 Z_1|T=1)").scale(.3)], [MathTex(r"\mathbb{M}(X_1 Z_2|T=1)").scale(.3), MathTex(r"\mathbb{M}(X_2 Z_2|T=1)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1.4),
            MobjectMatrix([[MathTex(r"\mathbb{M}(Y Z_1|T=1)").scale(.3)], [MathTex(r"\mathbb{M}(Y Z_2|T=1)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1.4)
        ).arrange(RIGHT)
        moment_matching_matrix_b = VGroup(
            MobjectMatrix([[MathTex(r"\beta_1").scale(.3)], [MathTex(r"\beta_2").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1.4),
            MathTex("="),
            MobjectMatrix([[MathTex(r"\mathbb{M}(X_1 Z_1|T=0)").scale(.3), MathTex(r"\mathbb{M}(X_2 Z_1|T=0)").scale(.3)], [MathTex(r"\mathbb{M}(X_1 Z_2|T=0)").scale(.3), MathTex(r"\mathbb{M}(X_2 Z_2|T=0)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1.4),
            MobjectMatrix([[MathTex(r"\mathbb{M}(Y Z_1|T=0)").scale(.3)], [MathTex(r"\mathbb{M}(Y Z_2|T=0)").scale(.3)]], bracket_h_buff=0.05, bracket_v_buff=0.05, v_buff=0.5, h_buff = 1.4)
        ).arrange(RIGHT)
        ATE_eq = VGroup(
            MathTex(r"\mathbb{M}(Y^{(1)}) - \mathbb{M}(Y^{(0)})"),
            MathTex(r"= (\alpha_1 - \beta_1)"),
            MathTex(r"\mathbb{M}(X_1)", color=YELLOW),
            MathTex(r"+ (\alpha_2 - \beta_2)"),
            MathTex(r"\mathbb{M}(X_2)", color = BLUE),
        ).arrange(RIGHT)
        final_calc = VGroup(ATE_eq, moment_matching_matrix_a, moment_matching_matrix_b).arrange(DOWN, center=True).center()
        inverse_a = MathTex(r"-1").scale(.3).next_to(moment_matching_matrix_a[2], RIGHT, buff=0.05).shift(.3 * UP)
        inverse_b = MathTex(r"-1").scale(.3).next_to(moment_matching_matrix_b[2], RIGHT, buff=0.05).shift(.3 * UP)
        main_highlight = BackgroundRectangle(final_calc, color = WHITE, stroke_width=8, stroke_opacity=1, fill_opacity=1, fill_color = BLACK, buff=.3)
        moment_matching_copy = moment_matching_matrix.copy()
        self.play(FadeIn(main_highlight),
                  TransformMatchingShapes(moment_matching_matrix, moment_matching_matrix_a),
                  TransformMatchingShapes(moment_matching_copy, moment_matching_matrix_b),
                  FadeIn(inverse_a),
                  FadeIn(inverse_b),
                  FadeIn(ATE_eq),
                  FadeOut(VGroup(simplified_graph, U_vec2, new_wanted, inverse)),
                  T.uncondition())
        self.end_fragment()

        proceedure = VGroup(main_highlight, moment_matching_matrix_a, moment_matching_matrix_b, inverse_a, inverse_b, ATE_eq)
        identifiability = Tex(r"Identifiability $\rightarrow$ Matrix Singularity").scale(.8)
        stability = Tex(r"Stability $\rightarrow$ Matrix Condition Number").scale(.8)
        main_points = VGroup(identifiability, stability)
        main_points.arrange(DOWN, center=False, aligned_edge = LEFT)
        main_points.set_color(YELLOW)
        proceedure.generate_target()
        proceedure.target.next_to(title, DOWN, buff = .5)
        main_points.next_to(proceedure, DOWN, buff = .5)
        self.play(MoveToTarget(proceedure))
        self.play(Write(identifiability))
        self.end_fragment()
        self.play(Write(stability))
        self.end_fragment()
        




