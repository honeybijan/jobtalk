from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class LatentFactorModels(PresentationScene):

    def construct(self):
        title = Text("Latent Heterogeneity").to_edge(UP, buff=.5)
        self.add(title)

        LFMs = VGroup(Text("Principal Component Analysis").scale(.7), Text("Clustering").scale(.7), Text("Mixture Models").scale(.7)).arrange(RIGHT, buff = 1.5)
        Allman = Text('Allman, et al. "Identifiability of parameters in structure models with many observed variables." 2009.', font_size=28)
        Anandkumar = Text('Anandkumar, et al. "Tensor decompositions for learning latent variable models." 2014.', font_size=28)
        Blessing = Text('Wang and Blei. "The Blessing of Multiple Causes." 2019.', font_size=28)
        Ogburn = Text('Ogburn, et. al. "Comment on the blessing of multiple causes." 2019.', font_size=28)
        citations = VGroup(LFMs, Blessing, Ogburn)
        citations.arrange(DOWN, center=False, aligned_edge=LEFT)
        citations.scale(.7).next_to(title, DOWN)
        for cit in citations:
            self.play(Create(cit), runtime = .5)
            self.end_fragment()


        Results = Ellipse(width = 2, height = 3, color=WHITE).move_to(5 * LEFT)
        ResultsLabel = Text("Causal Quantities", font_size = 24).next_to(Results, UP)
        ResultsOval = VGroup(Results, ResultsLabel)

        Models = Ellipse(width = 2, height = 3, color=WHITE)
        ModelsLabel = Text("Latent Factor Models", font_size = 24).next_to(Models, UP)
        ModsOval = VGroup(Models, ModelsLabel)

        Stats = Ellipse(width = 2, height = 3, color=WHITE).move_to(5 * RIGHT)
        StatsLabel = Text("Observed Statistics", font_size = 24).next_to(Stats, UP)
        StatsOval = VGroup(Stats, StatsLabel)


        Causal1 = Dot(5 * LEFT + 1 * UP, radius = .2, color=BLUE)
        Causal2 = Dot(5 * LEFT + 1 * DOWN, radius = .2, color=RED)
        Model1 = Dot(1 * UP, radius = .2, color=BLUE)
        Model2 = Dot(1 * DOWN, radius = .2, color=RED)
        Stat1 = Dot(5 * RIGHT, radius = .2, color=PURPLE)
        Stat2 = Dot(5 * RIGHT, radius = .2, color=PURPLE)
        Arrow1_M_to_S = always_redraw(lambda: Arrow(start = Model1, end = Stat1, buff=.2, color=BLUE))
        Arrow2_M_to_S = always_redraw(lambda: Arrow(start = Model2, end = Stat2, buff=.2, color=RED))
        Arrow1_M_to_C = always_redraw(lambda: Arrow(start = Model1, end = Causal1, buff=.2, color=BLUE))
        Arrow2_M_to_C = always_redraw(lambda: Arrow(start = Model2, end = Causal2, buff=.2, color=RED))
        Arrows = VGroup(Arrow1_M_to_C, Arrow2_M_to_C, Arrow1_M_to_S, Arrow2_M_to_S)

        whole_diagram = VGroup(ResultsOval, ModsOval, StatsOval, Causal1, Causal2, Model1, Model2, Stat1, Stat2, Arrows)
        whole_diagram.to_edge(DOWN, buff = .5)

        self.play(*[Create(item) for item in [ResultsOval, ModsOval, StatsOval]], runtime=.5)
        self.play(*[Create(item) for item in [Causal1, Causal2, Model1, Model2, Stat1, Stat2]], runtime=.5)
        self.end_fragment()

        self.play(Create(Arrow1_M_to_S), Create(Arrow2_M_to_S), runtime=1)
        self.play(Create(Arrow1_M_to_C), Create(Arrow2_M_to_C), runtime=1)
        self.end_fragment()

        Stat1.generate_target()
        Stat1.target.set_color(BLUE).shift(.3 * UP)
        Stat2.generate_target()
        Stat2.target.set_color(RED).shift(.3 * DOWN)
        self.play(*[MoveToTarget(t) for t in [Stat1, Stat2]], runtime = 1)
        self.end_fragment()

        Stat1.generate_target()
        Stat1.target.set_opacity(.5).scale(2.5)
        Stat2.generate_target()
        Stat2.target.set_opacity(.5).scale(2.5)
        self.play(*[MoveToTarget(t) for t in [Stat1, Stat2]], runtime = 1)
        self.end_fragment()

        self.play(FadeOut(citations))
        whole_diagram.generate_target()
        whole_diagram.target.next_to(title, .5 * DOWN)
        self.play(MoveToTarget(whole_diagram))
        iid = Text('Mazaheri et. al. "The sparse Hausdorff moment problem, with application to topic models." (arxiv, 2019)', t2w={'Mazaheri':BOLD}, font_size=28)
        prod1 = Text('Mazaheri et. al. "Source Identification for Mixtures of Product Distributions." (COLT, 2021)', t2w={'Mazaheri':BOLD}, font_size=28)
        bnd = Text('Mazaheri et. al. "Causal Inference Despite Limited Global Confounding via Mixture Models." (CleaR, 2023)', t2w={'Mazaheri':BOLD}, font_size=28)
        prod2 = Text('Mazaheri et. al.  "Identification of Mixtures of Discrete Product Distributions in Near-Optimal Sample \n \t and Time Complexity" (COLT, 2024)', t2w={'Mazaheri':BOLD}, font_size=28)
        discovery = Text('Mazaheri et. al.  "Discrete Nonparametric Causal Discovery under Latent Class Confounding." (arxiv, 2023)', t2w={'Mazaheri':BOLD}, font_size=28)
        citations = VGroup(iid, prod1, bnd, prod2, discovery)
        citations.arrange(DOWN, center=False, aligned_edge=LEFT).scale(.7).to_edge(DOWN, buff = .5)
        self.play(LaggedStart(*[Write(cite) for cite in citations]), runtime = 3)
        self.end_fragment()

        # Takeaways
        identifiability_conditions = Text("Identifiability:")
        prove = Text("1. Hard to prove")
        state = Text("2. Hard to state")
        verify = Text("3. Hard to verify")
        sample_complexity = Text("Stability:")
        unstable = Text("- Pretty bad")
        main_points = VGroup(identifiability_conditions, prove, state, verify, sample_complexity, unstable)
        main_points.arrange(DOWN, center=False, aligned_edge = LEFT)
        identifiability_conditions.shift(LEFT)
        sample_complexity.shift(LEFT)
        main_points.set_color(YELLOW).center()
        main_highlight = BackgroundRectangle(main_points, color = YELLOW, stroke_width=8, stroke_opacity=1, fill_opacity=1, fill_color = BLACK, buff=.3)

        self.play(FadeIn(main_highlight), runtime = .5)
        self.play(Write(identifiability_conditions), runtime = 1)
        self.play(LaggedStart(*[Write(t) for t in [prove, state, verify]]), runtime = 2)
        self.end_fragment()
        self.play(Write(sample_complexity), runtime = 1)
        self.play(FadeIn(unstable), runtime = .5)
        self.end_fragment()

        # Reset
        trash = VGroup(main_points, main_highlight, citations)
        whole_diagram.generate_target()
        whole_diagram.target.center()
        self.play(FadeOut(trash))
        self.play(MoveToTarget(whole_diagram))
        Stat1.generate_target()
        Stat2.generate_target()
        Stat1.target.set_color(PURPLE).set_opacity(1).scale(1/2.5).shift(.3 * DOWN)
        Stat2.target.set_color(PURPLE).set_opacity(1).scale(1/2.5).shift(.3 * UP)
        self.play(MoveToTarget(Stat1), MoveToTarget(Stat2))
        self.end_fragment()

        Causal1.generate_target()
        Causal2.generate_target()
        Causal1.target.set_color(PURPLE).shift(DOWN)
        Causal2.target.set_color(PURPLE).shift(UP)
        self.play(MoveToTarget(Causal1), MoveToTarget(Causal2))
        self.end_fragment()

        Stat1.generate_target()
        Stat2.generate_target()
        Stat1.target.set_color(BLUE).set_opacity(1).shift(UP)
        Stat2.target.set_color(RED).set_opacity(1).shift(DOWN)
        Causal1.generate_target()
        Causal2.generate_target()
        Causal1.target.set_color(BLUE).shift(UP)
        Causal2.target.set_color(RED).shift(DOWN)
        self.play(MoveToTarget(Stat1), MoveToTarget(Stat2), MoveToTarget(Causal1), MoveToTarget(Causal2))
        self.end_fragment()