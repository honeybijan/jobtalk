from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random

from GraphManim import *

class NeuralNetworks(PresentationScene):

    def construct(self):
        title = Text("Modern Methods for Latent Spaces").to_edge(UP, buff=.5)
        self.add(title)
        
        # Draw DAG
        Col1 = VGroup(*[Vertex("") for i in range(5)]).arrange(DOWN, buff=.5)
        Col2 = VGroup(*[Vertex("") for i in range(3)]).arrange(DOWN, buff=.5)
        latent_space = VGroup(*[Vertex("") for i in range(2)]).arrange(DOWN, buff=.5)
        Col3 = VGroup(*[Vertex("") for i in range(3)]).arrange(DOWN, buff=.5)
        Col4 = VGroup(*[Vertex("") for i in range(5)]).arrange(DOWN, buff=.5)
        NN_nodes = VGroup(Col1, Col2, latent_space, Col3, Col4).arrange(RIGHT, buff = 1).center().shift(.5 * UP)

        def dense_edges(c1, c2):
            edges = []
            for a in c1:
                for b in c2:
                    edges.append(Edge(a, b))
            return edges

        edges12 = dense_edges(Col1, Col2)
        edges2l = dense_edges(Col2, latent_space)
        edgesl3 = dense_edges(latent_space, Col3)
        edges34 = dense_edges(Col3, Col4)

        NN = VGroup(NN_nodes, *edges12, *edges2l, *edgesl3, *edges34)

        x = Tex(r"X").next_to(Col1, LEFT, buff=.5)
        y = Tex(r"Y").next_to(Col4, RIGHT, buff=.5)

        # Citations
        VAE = Text("Variational Auto Encoder").scale(.5)
        VAE_cite = Paragraph("Kingma, D. P., & Welling, M. (2013). Auto-encoding variational bayes. arXiv preprint arXiv:1312.6114.").scale(.25)

        Transformer = Text("Transformers/Foundation Models").scale(.5)
        Transformer_cite = Paragraph("Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017).\n Attention is all you need. Advances in neural information processing systems, 30.").scale(.25)

        citations = VGroup(VAE, VAE_cite, Transformer, Transformer_cite).arrange(DOWN).next_to(NN, DOWN, buff = .25)

        self.play(Write(NN))
        self.end_fragment()
        self.play(Write(x))
        self.end_fragment()
        self.play(Write(y))
        self.end_fragment()
        latent_space.generate_target()
        latent_space.target.set_color(YELLOW)
        self.play(MoveToTarget(latent_space))
        self.end_fragment()
        self.play(Write(VAE), FadeIn(VAE_cite))
        self.end_fragment()
        self.play(Write(Transformer), FadeIn(Transformer_cite))
        self.end_fragment()


        



