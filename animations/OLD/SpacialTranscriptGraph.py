from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math

from GraphManim import *


class SpacialTranscriptGraph(PresentationScene):

    def construct(self):
        title = Text("Spacial Transcriptomics").to_edge(UP, buff=.5)
        self.add(title)

        # Draw DAG
        Cell  = RectVertex("Cell")
        Close  = RectVertex("Close Cells").shift(3 * LEFT)
        Far  = RectVertex("Far Cells").shift(6 * LEFT)
        Structure  = RectVertex("Structure", color=WHITE, observed=False).shift(2 * UP + 3 * LEFT)

        StructEdge1 = DashedLine(start=Structure.get_edge_center(DOWN) + .2 * RIGHT, end = Cell.get_edge_center(UP), buff=0)
        StructEdge1.add_tip(tip_length = .1, tip_width=.1)
        StructEdge2 = DashedLine(start=Structure.get_edge_center(DOWN), end = Close.get_edge_center(UP), buff=0)
        StructEdge2.add_tip(tip_length = .1, tip_width=.1)
        StructEdge3 = DashedLine(start=Structure.get_edge_center(DOWN) + .2 * LEFT, end = Far.get_edge_center(UP), buff=0)
        StructEdge3.add_tip(tip_length = .1, tip_width=.1)

        FarToClose = Line(start=Far.get_edge_center(RIGHT), end = Close.get_edge_center(LEFT), buff=0)
        FarToClose.add_tip(tip_length = .1, tip_width=.1)
        CloseToCell = Line(start=Close.get_edge_center(RIGHT), end = Cell.get_edge_center(LEFT), buff=0)
        CloseToCell.add_tip(tip_length = .1, tip_width=.1)
        
        causal_dag = VGroup(Cell, Close, Far, Structure, StructEdge1, StructEdge2, StructEdge3, FarToClose, CloseToCell)
        causal_dag.scale(1.5).move_to(ORIGIN).shift(DOWN)
        self.play(Write(causal_dag), run_time = 1)
        self.end_fragment()

        CloseToCell.generate_target()
        CloseToCell.target.set_color(GREEN)
        self.play(MoveToTarget(CloseToCell), runtime=.5)
        self.end_fragment()