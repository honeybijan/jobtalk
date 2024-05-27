from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random

from GraphManim import *

class IdentifiabilityReduction(PresentationScene):

    def construct(self):
        title = Text("Results on Identifiability").to_edge(UP, buff=.5)
        self.add(title)

        Vertices = [Vertex(label = r'V')]
        for i in range(6):
            Vertices.append(Vertex(label = r'V').next_to(Vertices[-1], RIGHT))
        Mixture_U = Vertex(label=r"U", observed=False).next_to(Vertices[3], UP).shift(UP)
        Upper_Edges = [Edge(Mixture_U, V, observed = False) for V in Vertices]
        MixProdGraph = Graph(Vertices, Upper_Edges, unobserved = Mixture_U)
        KMixIID = MarkupText('"The sparse Hausdorff moment problem, with application to topic models." (arxiv, 2019)', font_size=22).next_to(MixProdGraph, DOWN)
        KmixProd = MarkupText('"Source Identification for Mixtures of Product Distributions." (COLT, 2021)', font_size=22).next_to(KMixIID, DOWN)
        KmixBND = MarkupText('"Causal Inference Despite Limited Global Confounding via Mixture Models." (CleaR, 2023)', font_size=22).next_to(KmixProd, DOWN)
        Discovery = MarkupText('"Discrete Nonparametric Causal Discovery under Latent Class Confounding." (Hopefully UAI, 2024)', font_size=22).next_to(KmixBND, DOWN)
        
        slide = VGroup(MixProdGraph, Discovery, KmixBND, KmixProd, KMixIID).move_to(ORIGIN)
        Low_Edges = [Edge(Vertices[i], Vertices[i+1], observed=False) for i in range(len(Vertices) - 1)]
        Obs_Lower_Edges = [Edge(Vertices[i], Vertices[i+1], observed=True) for i in range(len(Vertices) - 1)]
        
        # KMix IID
        self.add(MixProdGraph)
        self.play(Create(KMixIID), runtime = .5)
        self.end_fragment()

        # K Mix Prod
        New_Vertices = [Vertex(label=r"V_" + str(i+1), color=random_bright_color()).move_to(v) for i, v in enumerate(Vertices)]
        v_changes = []
        for v, new_v in zip(Vertices, New_Vertices):
            v_changes.append(TransformMatchingShapes(v, new_v))
        self.play(Create(KmixProd), runtime = 1)
        self.play(*v_changes, runtime = 1)
        self.end_fragment()

        # K MixBND
        self.play(*[Create(edge) for edge in Obs_Lower_Edges], runtime = 1)
        self.play(Create(KmixBND), runtime=1)
        self.end_fragment()

        move_to_targets = []
        for obs_edge, unobs_edge in zip(Obs_Lower_Edges, Low_Edges):
            move_to_targets.append(TransformMatchingShapes(obs_edge, unobs_edge))
        self.play(*move_to_targets, runtime = 1)
        self.play(Create(Discovery), runtime=1)
        self.end_fragment()

        self.end_fragment()
