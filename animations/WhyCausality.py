from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
from GraphManim import *

class WhyCausality(PresentationScene):

    def construct(self):
        title1 = Text("Causation and Extrapolation").to_edge(UP)

        self.add(title1)

        season  = RectVertex("Month").shift(UP)
        co2  = RectVertex(r"$\text{CO}_2$").shift(LEFT)
        temp  = RectVertex("Temperature").shift(RIGHT)
        beach = RectVertex("Beach").shift(3 * RIGHT)
        temp_beach = Line(start=temp.get_edge_center(RIGHT), end = beach.get_edge_center(LEFT), buff=0)
        temp_beach.add_tip(tip_length = .1, tip_width=.1)
        season_co2 = Line(start=season.get_edge_center(DOWN) + .2 * LEFT, end = co2.get_edge_center(UP), buff=0)
        season_co2.add_tip(tip_length = .1, tip_width=.1)
        season_temp = Line(start=season.get_edge_center(DOWN) + .2 * RIGHT, end = temp.get_edge_center(UP), buff=0)
        season_temp.add_tip(tip_length = .1, tip_width=.1)
        co2_temp = Line(start=co2.get_edge_center(RIGHT), end = temp.get_edge_center(LEFT), buff=0)
        co2_temp.add_tip(tip_length = .1, tip_width=.1)

        causal_dag = VGroup(season, co2, temp, beach, season_co2, season_temp, co2_temp, temp_beach)
        causal_dag.scale(1.5).next_to(title1, DOWN)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        interpolation = Tex("Interpolation: Temperature model with good accuracy.", color=YELLOW).scale(.7)
        extrapolation = Tex(r"Causal Extrapolation: What would have or will happen if $\text{CO}_2$ changes?", color=YELLOW).scale(.7)
        interp_extrap = VGroup(interpolation, extrapolation).arrange(DOWN, aligned_edge=LEFT, buff=.5).next_to(causal_dag, DOWN, buff=.5)

        interpolators = VGroup(season, co2, beach, temp_beach, co2_temp, season_temp)
        for inter in interpolators:
            inter.generate_target()
            inter.target.set_color(YELLOW)
        self.play(Write(interpolation), *[MoveToTarget(inter) for inter in interpolators])
        not_causal = [beach, season, temp_beach, season_temp, interpolation]
        for inter in not_causal:
            inter.generate_target()
            inter.target.set_color(WHITE)
        self.end_fragment()
        self.play(Write(extrapolation), *[MoveToTarget(n_cause) for n_cause in not_causal])
        self.end_fragment()

        for obj in [co2, co2_temp, extrapolation]:
            obj.generate_target()
            obj.target.set_color(WHITE)
        self.play(*[MoveToTarget(obj) for obj in [co2, co2_temp, extrapolation]], runtime = .5)
        key1 = Text("1. Causality is key whenever we act on a system.", color=YELLOW).scale(.9)
        key2 = Text("2. Causality cannot be verified in a validation set.", color=YELLOW).scale(.9)
        keys = VGroup(key1, key2).arrange(DOWN, center=False, aligned_edge=LEFT, buff = .5).next_to(interp_extrap, DOWN, buff = .5)
        highlight_rect = SurroundingRectangle(keys, buff=.2, corner_radius=.1, color=YELLOW)
        self.play(Write(key1))
        self.end_fragment()
        self.play(Write(key2))
        self.play(Write(highlight_rect))
        self.end_fragment()