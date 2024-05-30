from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random


class AgeOfModels(PresentationScene):

    def construct(self):
        title1 = Text("Age of Data").to_edge(UP)
        title2 = Text("Age of Models").to_edge(UP)

        q1 = Text("How can we combine different data?")
        q2 = Text("How can we combine different models?")
        self.add(title1)
        self.play(Write(q1))
        self.end_fragment()

        self.play(TransformMatchingShapes(title1, title2), TransformMatchingShapes(q1, q2))
        self.end_fragment()