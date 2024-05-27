from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

from icons import *


class FundamentalProblem(PresentationScene):
    
    def construct(self):
        title = Text("Fundamental Problem of Causal Inference").to_edge(UP, buff=.5)
        self.add(title)

        person_factual = StickFigure().to_edge(LEFT, buff=2).shift(.5 * DOWN)
        self.add(person_factual.body)
        self.end_fragment()

        person_treated = StickFigure(happy=True).to_edge(RIGHT, buff=6).shift(UP)

        treatment_arrow = Arrow(start = person_factual.get_center(), end=person_treated.get_center(), buff = 1)
        treated = Pill().scale(.5).next_to(treatment_arrow, .5 * UP)
        self.play(Write(treatment_arrow), FadeIn(treated), runtime = 1)
        self.play(FadeIn(person_treated), runtime = .5)
        self.end_fragment()

        person_counterfactual = StickFigure().to_edge(LEFT, buff=2).shift(.5 * DOWN)
        self.add(person_counterfactual.body)
        person_untreated = StickFigure(happy=False).to_edge(RIGHT, buff=6).shift(2 * DOWN)
        untreatment_arrow = Arrow(start = person_counterfactual.get_center(), end=person_untreated.get_center(), buff = 1)
        untreated = Pill(False).scale(.5).next_to(untreatment_arrow, .5 * DOWN)
        self.play(Write(untreatment_arrow), FadeIn(untreated), runtime = 1)
        self.play(FadeIn(person_untreated), runtime = .5)
        self.end_fragment()

        # Add ys
        po1 = MathTex(r'{{Y^{(1)}}}').next_to(person_treated, RIGHT, buff = 1)
        po0 = MathTex(r'{{Y^{(0)}}}').next_to(person_untreated, RIGHT, buff = 1)
        te = MathTex(r"{{\text{Treatment Effect}}}", r"=", r"{{Y^{(1)}}}", r"-", r"{{Y^{(0)}}}").to_edge(RIGHT, buff=1).scale(.7).shift(.5 * DOWN)
        self.play(Write(po1), Write(po0), runtime = 1)
        self.play(Write(te), runtime = 1)
        self.end_fragment()

        # Cant see both
        top = VGroup(po1, treatment_arrow, person_treated, te[2])
        bot = VGroup(po0, untreatment_arrow, person_untreated, te[4])
        top.generate_target()
        top.target.set_opacity(.3)
        self.play(MoveToTarget(top), runtime = .5)
        self.wait(1)
        top.generate_target()
        top.target.set_opacity(1)
        bot.generate_target()
        bot.target.set_opacity(.3)
        self.play(MoveToTarget(top), MoveToTarget(bot), runtime =.5)
        self.wait()
        bot.generate_target()
        bot.target.set_opacity(1)
        self.play(MoveToTarget(bot), runtime = .5)
        self.end_fragment()


        # Separate
        untreatment_arrow_2 = always_redraw(lambda: Arrow(start = person_counterfactual.get_center(), end=person_untreated.get_center(), buff = 1))
        treatment_arrow_2 = always_redraw(lambda: Arrow(start = person_factual.get_center(), end=person_treated.get_center(), buff = 1))
        self.add(untreatment_arrow_2, treatment_arrow_2)
        self.remove(untreatment_arrow, treatment_arrow)
        person_factual.remove(person_factual.head)
        person_factual.generate_target()
        person_factual.target.shift(1.5 * UP)
        person_counterfactual.remove(person_counterfactual.head)
        person_counterfactual.generate_target()
        person_counterfactual.target.shift(1.5 * DOWN)
        treated.generate_target()
        treated.target.shift(.2 * UP)
        untreated.generate_target()
        untreated.target.shift(.2 * DOWN)
        self.play(MoveToTarget(person_factual), MoveToTarget(person_counterfactual), MoveToTarget(treated), MoveToTarget(untreated), runtime = 1)
        self.end_fragment()

        # Groups
        group_of_sticks = StickFigure.group_of_sticks(n=9, width=3, scale=.3, v_sep=.7, h_sep=.5, happy_prob =.75)
        group_of_sticks2 = StickFigure.group_of_sticks(n=9, width=3, scale=.3, v_sep=.7, h_sep=.5, happy_prob = .25)
        group_of_sticks.move_to(person_factual)
        group_of_sticks_treated = group_of_sticks.copy().move_to(person_treated)
        group_of_sticks2.move_to(person_counterfactual)
        group_of_sticks.move_to(person_factual)
        group_of_sticks_untreated = group_of_sticks2.copy().move_to(person_untreated)
        apo1 = MathTex(r'\mathbb{E}[{{Y^{(1)}}}]').next_to(person_treated, RIGHT, buff = 1)
        apo0 = MathTex(r'\mathbb{E}[{{Y^{(0)}}}]').next_to(person_untreated, RIGHT, buff = 1)
        self.play(FadeOut(person_factual), FadeOut(person_counterfactual), FadeOut(person_treated), FadeOut(person_untreated))
        self.play(TransformMatchingTex(po1, apo1), TransformMatchingTex(po0, apo0),
                   *[FadeIn(stick.body) for stick in group_of_sticks], 
                   *[FadeIn(stick.body) for stick in group_of_sticks2], 
                   FadeIn(group_of_sticks_treated), FadeIn(group_of_sticks_untreated))
        self.end_fragment()

        ate = MathTex(r"{{\text{Avg Treatment Effect}}}", r"=", r"\mathbb{E}[{{Y^{(1)}}}]", r"-", r"\mathbb{E}[{{Y^{(0)}}}]").to_edge(RIGHT, buff=1).scale(.7).move_to(te)
        self.play(TransformMatchingTex(te, ate))
        self.end_fragment()

        