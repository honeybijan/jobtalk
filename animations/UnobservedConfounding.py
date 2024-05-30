from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random

from GraphManim import *

class UnobservedConfounding(PresentationScene):

    def construct(self):
        title = Text("Unobverved Confounding").to_edge(UP, buff=.5)
        C = Vertex("C", observed = True)
        U = Vertex("U", observed = False).next_to(C, 4 * RIGHT)
        T = Vertex("T", observed = True).next_to(C, 3 * DOWN)
        Y = Vertex("Y", observed = True).next_to(U, 3 * DOWN)
        CT = Edge(C, T)
        CY = Edge(C, Y)
        TY = Edge(T, Y)
        UT = Edge(U, T, observed = False)
        UY = Edge(U, Y, observed = False)
        graph = Graph(V = [C, U, T, Y], E = [CT, CY, TY, UT, UY])
        graph.move_to(ORIGIN)

        self.add(C, T, Y, CT, CY, TY, title)
        self.play(Create(UT), Create(UY), Create(U), runtime=.5)
        self.end_fragment()
        graph.generate_target()
        graph.target.to_edge(UP, buff = 1.5)
        self.play(MoveToTarget(graph))

        Allman = Text('Allman, et al. "Identifiability of parameters in structure models with many observed variables." 2009.', font_size=24)
        Anandkumar = Text('Anandkumar, et al. "Tensor decompositions for learning latent variable models." 2014.', font_size=24)
        Blessing = Text('Wang and Blei. "The Blessing of Multiple Causes." 2019.', font_size=24)
        Ogburn = Text('Ogburn, et. al. "Comment on the blessing of multiple causes." 2019.', font_size=24)
        citations = VGroup(Allman, Anandkumar, Blessing, Ogburn)
        citations.arrange(DOWN, center=False, aligned_edge=LEFT)

        for cit in citations:
            self.play(Create(cit), runtime = .5)
            self.end_fragment()
