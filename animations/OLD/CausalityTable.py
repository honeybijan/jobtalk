from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
from GraphManim import *

def MultiCellCover(left, right, top, bottom, fill, label=None):
    center_x = (left.get_x() + right.get_x())/2
    center_y = (top.get_y() + bottom.get_y())/2
    w = abs(left.get_x() - right.get_x())
    h = abs(top.get_y() - bottom.get_y())
    Rect = Rectangle(width=w, height=h, color=WHITE)

    Rect.move_to([center_x, center_y, 0])
    Rect.set_fill(color=BLACK, opacity=1)
    Label=Text(label, color=fill).move_to([center_x, center_y, 1])
    return VGroup(Rect, Label)

class CausalityTable(PresentationScene):

    def construct(self):
        title = Text("An Example").to_edge(UP, buff=.5)

        expanded_entries = [[70, 30],[1, 9],
                            [9, 1],[30, 70]]
        data_table = IntegerTable(
            expanded_entries, 
            row_labels=[Text("Mild"), Text("Severe"), Text("Mild"), Text("Severe")],
            col_labels=[Text("Better"), Text("Worse")],
            include_outer_lines=True)

        h_lines = data_table.get_horizontal_lines()
        v_lines = data_table.get_vertical_lines()

        cover_rect_control = MultiCellCover(v_lines[0], v_lines[2], h_lines[2], h_lines[4], BLUE, label="Control")
        cover_rect_treat = MultiCellCover(v_lines[0], v_lines[2], h_lines[4], h_lines[1], YELLOW, label="Treatment")
        cover_rect_control_better = MultiCellCover(v_lines[2], v_lines[3], h_lines[2], h_lines[4], GREEN, label="71")
        cover_rect_treat_better = MultiCellCover(v_lines[2], v_lines[3], h_lines[4], h_lines[1], GREEN, label="39")
        cover_rect_control_worse = MultiCellCover(v_lines[3], v_lines[1], h_lines[2], h_lines[4], RED, label="39")
        cover_rect_treat_worse = MultiCellCover(v_lines[3], v_lines[1], h_lines[4], h_lines[1], RED, label="71")
        cover_rects = VGroup(cover_rect_control, 
                              cover_rect_treat, 
                              cover_rect_control_better, 
                              cover_rect_control_worse, 
                              cover_rect_treat_better, 
                              cover_rect_treat_worse)
        data_table.get_rows()[1].set_color(BLUE)
        data_table.get_rows()[2].set_color(BLUE)
        data_table.get_rows()[3].set_color(YELLOW)
        data_table.get_rows()[4].set_color(YELLOW)
        data_table.get_columns()[1].set_color(GREEN)
        data_table.get_columns()[2].set_color(RED)

        full_table = VGroup(data_table, cover_rects)
        full_table.scale(.7).to_edge(LEFT, buff=.5)

        # Add Table
        self.add(data_table, title)
        self.add(cover_rects)
        
        # Reveal Confounder
        self.play(FadeOut(cover_rects), runtime=.5)
        self.end_fragment()


        # Focus on rows
        data_table.generate_target()
        data_table.target.get_rows()[2].set_opacity(.3)
        data_table.target.get_rows()[4].set_opacity(.3)
        self.play(MoveToTarget(data_table), runtime=.5)
        self.end_fragment()
        data_table.generate_target()
        data_table.target.get_rows()[2].set_opacity(1)
        data_table.target.get_rows()[4].set_opacity(1)
        data_table.target.get_rows()[1].set_opacity(.3)
        data_table.target.get_rows()[3].set_opacity(.3)
        self.play(MoveToTarget(data_table), runtime=.5)
        self.end_fragment()

        data_table.generate_target()
        data_table.target.get_rows()[1].set_opacity(1)
        data_table.target.get_rows()[3].set_opacity(1)

        self.play(MoveToTarget(data_table), run_time = 1)
        self.end_fragment()

        # Draw DAG
        TreatV  = RectVertex("Treatment").shift(LEFT)
        OutcomeV  = RectVertex("Outcome").shift(RIGHT)
        ConditionV  = RectVertex("Condition").shift(UP)
        edge1 = Line(start=ConditionV.get_edge_center(DOWN) + .2 * LEFT, end=TreatV.get_edge_center(UP), buff=0)
        edge1.add_tip(tip_length = .1, tip_width=.1)
        edge2 = Line(start=ConditionV.get_edge_center(DOWN) + .2 * RIGHT, end=OutcomeV.get_edge_center(UP), buff=0)
        edge2.add_tip(tip_length = .1, tip_width=.1)
        edge3 = Line(start=TreatV.get_edge_center(RIGHT), end=OutcomeV.get_edge_center(LEFT), buff=0)
        edge3.add_tip(tip_length = .1, tip_width=.1)
        causal_dag = VGroup(TreatV, OutcomeV, ConditionV, edge1, edge2, edge3)
        causal_dag.to_edge(RIGHT, buff=2).shift(UP)

        # Fade out rows and give do-intervention
        bd1 = MathTex(r'P(\text{Better} \;|\; do(\text{Treatment})) :=', color=YELLOW, font_size=28)
        bd2 = MathTex(r'P(\text{Mild})(9/10)', color=YELLOW, font_size=28)
        bd3 = MathTex(r'+ P(\text{Severe})(3/10)', color=YELLOW, font_size=28).next_to(bd2, RIGHT)
        bd4 = MathTex(r' = 6/10', color=YELLOW, font_size=28).next_to(bd3, RIGHT)
        expansion = VGroup(bd2, bd3, bd4).next_to(bd1, DOWN)
        all_backdoor = VGroup(bd1, expansion)
        all_backdoor.next_to(causal_dag, DOWN, buff=1)
        self.play(Write(bd1), run_time = 1, buff=.2)
        self.end_fragment()

        data_table.generate_target()
        data_table.target.get_rows()[1].set_opacity(.3)
        data_table.target.get_rows()[2].set_opacity(.3)
        data_table.target.get_rows()[4].set_opacity(.3)
        row = data_table.get_rows()[3][1:].copy()
        self.play(MoveToTarget(data_table), runtime=.5)
        self.play(TransformMatchingShapes(row, bd2), runtime=1)
        self.end_fragment()


        data_table.generate_target()
        data_table.target.get_rows()[4].set_opacity(1)
        data_table.target.get_rows()[3].set_opacity(.3)
        row = data_table.get_rows()[4][1:].copy()
        self.play(MoveToTarget(data_table), runtime=.5)
        self.play(TransformMatchingShapes(row, bd3), runtime=1)
        self.end_fragment()

        data_table.generate_target()
        data_table.target.get_rows()[1].set_opacity(1)
        data_table.target.get_rows()[2].set_opacity(1)
        data_table.target.get_rows()[4].set_opacity(1)
        data_table.target.get_rows()[3].set_opacity(1)
        self.play(Write(bd4), MoveToTarget(data_table), runtime = .5)
        self.end_fragment()

        # Control Do Intervention
        row1 = data_table.get_rows()[1][1:].copy()
        row2 = data_table.get_rows()[2][1:].copy()
        rows = VGroup(row1, row2)
        bd5 = MathTex(r'P(\text{Better} \;|\; do(\text{Control})) = 4/10', color=BLUE, font_size=28).next_to(expansion, DOWN)
        self.play(MoveToTarget(data_table), TransformMatchingShapes(rows, bd5), runtime=1)
        self.end_fragment()

        self.play(Create(causal_dag), runtime = 1)
        self.end_fragment()

        edge1.generate_target()
        edge1.target.set_opacity(.1)
        self.play(MoveToTarget(edge1), runtime=.5)
        self.end_fragment()