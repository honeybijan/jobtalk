from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP
import math
from GraphManim import *

config.video_dir = "./videos"

import random

class KvsData(PresentationScene):

    def construct(self):
        title = Text("More Data, More Problems?").to_edge(UP, buff=.5)
        self.add_foreground_mobject(title)

        ax = Axes(x_range=[-5, 100, 5], y_range=[-5, 100, 10]).scale(.8).shift(.5 * DOWN)
        labels = MathTex(r'k = \text{Number of Latent Components}').set_color(WHITE).scale(.5).to_edge(DOWN, buff = .5)
        self.add(ax, labels)

        # Draw graph
        curve1 = ax.plot(lambda x: x, color=BLUE)
        curve2 = ax.plot(lambda x: math.exp(x/10)/50, color=RED)
        data_we_get = Text("Data we get", color = BLUE).scale(.5).move_to(5 * RIGHT + 1.2 * UP)
        data_we_need = Text("Data we need", color = RED).scale(.5).move_to(5 * RIGHT + 3 * UP)
        self.play(Create(curve1), runtime=1)
        self.play(Write(data_we_get), runtime = 1)
        self.play(Create(curve2), runtime=1)
        self.play(Write(data_we_need), runtime = 1)
        self.end_fragment()