from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP
from GraphManim import *

config.video_dir = "./videos"

import random

class AnimListStartError(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(self, message)

class Pocket(VGroup):
    def __init__(self, **kwargs):
        position_list = [
            [-1.5, 1, 0],  # top left
            [-1.5, -1.2, 0],  # bottom left
            [0, -1.8, 0],  #  bottom
            [1.5, -1.2, 0],  # bottom right
            [1.5, 1, 0],  # top right
        ]
        VGroup.__init__(self, **kwargs)
        Outline = Polygon(*position_list, color=WHITE)
        Inner = Outline.copy().scale(.9)
        self.add(Outline)
        self.add(DashedVMobject(Inner, num_dashes=40))

class AnimationList:
    def __init__(self, times = None, animations = None, re_orderings = None, removes = None, adds = None):
        if times == None:
            times = []
        if animations == None:
            animations = []
        if re_orderings == None:
            re_orderings = []
        if removes == None:
            removes = []
        if adds == None:
            adds = []
        self.times = times
        self.animations = animations
        self.re_orderings = re_orderings
        self.adds = adds
        self.removes = removes

    def __str__(self):
        result = "\n".join([str(t) + "\t" + str(len(a)) for t,a  in zip(self.times, self.animations)])
        return result

    def length(self):
        return len(self.times)

    # Adds a new time step
    def time_step(self, time=.2):
        self.times.append(time)
        self.animations.append([])
        self.re_orderings.append([])
        self.removes.append([])
        self.adds.append([])

    def re_order(self, manim_objects):
        self.re_orderings[-1] = manim_objects

    def add_objects(self, manim_objects):
        self.adds[-1] += manim_objects

    def remove_objects(self, manim_objects):
        self.removes[-1] += manim_objects

    # Adds a new animation simultaneiously
    def add_animation(self, anim):
        if len(self.animations) == 0:
            raise AnimListStartError("Need to define time step first")
        self.animations[-1].append(anim)
    
    # Adds other after self
    def append(self, other):
        new_times = self.times + other.times
        new_anims = self.animations + other.animations
        new_adds = self.adds + other.adds
        new_removes = self.removes + other.removes
        new_reords = self.re_orderings + other.re_orderings
        return AnimationList(animations = new_anims, times = new_times, adds = new_adds, removes = new_removes, re_orderings=new_reords)
    
    # Adds other after self
    def simul(self, other):
        new_times = []
        new_anims = []
        new_reords = []
        new_adds = []
        new_removes = []
        min_length = min(len(self.times),len(other.times))
        for i in range(min_length):
            new_times.append(max(self.times[i], other.times[i]))
            new_anims.append(self.animations[i] + other.animations[i])
            new_reords.append(self.re_orderings[i] + other.re_orderings[i])
            new_adds.append(self.adds[i] + other.adds[i])
            new_removes.append(self.removes[i] + other.removes[i])
        
        if len(self.times) <= len(other.times):
            for time in other.times[min_length:] :
                new_times.append(time)
            for anim in other.animations[min_length:]:
                new_anims.append(anim)
        else:
            for time in self.times[min_length:] :
                new_times.append(time)
            for anim in self.animations[min_length:]:
                new_anims.append(anim)
        return AnimationList(animations = new_anims, times = new_times, adds = new_adds, removes = new_removes, re_orderings=new_reords)

    def play_animation(self, scene):
        for anims, time, reord, ads, rem in zip(self.animations, self.times, self.re_orderings, self.adds, self.removes):
            # Add
            for moj in ads:
                scene.add(moj)

            # Reorder
            for i, moj in enumerate(reord):
                moj.z_index = i

            # Animate
            scene.play(*anims, run_time = time)

            # Remove
            for moj in rem:
                scene.remove(moj)

class Coin(VGroup):
    def __init__(self, radius = .4, bias = .5, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.bias = bias
        heads_angle = bias * 2 * PI
        self.red_slice = AnnularSector(inner_radius=0, outer_radius=radius, angle=heads_angle, start_angle= PI / 2 - heads_angle/2, color=RED)
        self.blue_slice = AnnularSector(inner_radius=0, outer_radius=radius, angle=2 * PI - heads_angle, start_angle= PI / 2 + heads_angle/2, color=BLUE)
        self.add(self.red_slice)
        self.add(self.blue_slice)
        H = Text("H", font_size = 16, color=BLACK)
        H.move_to(self.get_center() + .2 * UP)
        T = Text("T", font_size = 16, color=BLACK)
        T.move_to(self.get_center() + .2 * DOWN)
        self.add(H)
        self.add(T)
        self.original = self.copy()
        self.flip_outcomes = []

    def randomize_bias(self):
        new_bias = random.random()
        heads_angle = new_bias * 2 * PI
        #self.target = Coin(bias=new_bias).move_to(self.get_center())
        self.red_slice.target = AnnularSector(inner_radius=0, outer_radius=.4, angle=heads_angle, start_angle= PI / 2 - heads_angle/2, color=RED)
        self.blue_slice.target = AnnularSector(inner_radius=0, outer_radius=.4, angle=2 * PI - heads_angle, start_angle= PI / 2 + heads_angle/2, color=BLUE)
        self.red_slice.target.shift(self.get_center())
        self.blue_slice.target.shift(self.get_center())
        return [MoveToTarget(self.red_slice), MoveToTarget(self.blue_slice)]

    def reset_original(self):
        self.original = self.copy()

    def select(self, pocket):
        anim_list = AnimationList()
        anim_list.time_step(.5)
        self.generate_target()
        self.target.move_to(pocket.get_center() + 2 * UP)
        self.target.scale(1.2)
        anim_list.add_animation(MoveToTarget(self))
        return anim_list
    
    def deselect(self):
        anim_list = AnimationList()
        anim_list.time_step(.5)
        self.target = self.original.copy()
        anim_list.add_animation(MoveToTarget(self))
        for flip_outcome in self.flip_outcomes:
            anim_list.add_animation(FadeOut(flip_outcome, shift = UP))
        self.flip_outcomes = []
        return anim_list

    # Create H and T sides
    def pre_flip(self):
        heads = VGroup()
        heads.add(Circle(radius=self.width/2, color=RED, fill_opacity=1))
        #heads.add(AnnularSector(inner_radius=0, outer_radius=self.width/2, angle=2 * PI, start_angle= PI / 2, color=RED))
        heads.add(Text("H", font_size=28, color=BLACK).move_to(heads.get_center()))
        heads.move_to(self.get_center())

        tails = VGroup()
        tails.add(Circle(radius=self.width/2, color=BLUE, fill_opacity=1))
        #tails.add(AnnularSector(inner_radius=0, outer_radius=self.width/2, angle=2 * PI, start_angle= 3 *PI / 2, color=BLUE))
        tails.add(Text("T", font_size=28, color=BLACK).move_to(tails.get_center()))
        tails.move_to(self.get_center())
        return heads, tails


    def flip(self, final='H',n_flips=1):
        heads, tails = self.pre_flip()
        anim_list = AnimationList()

        if final=="H":
            HT = [tails, heads]
        else:
            HT = [heads, tails]

        def collapse(c):
            c.generate_target()
            c.target.stretch(.01, dim=1)
            anim_list.add_animation(MoveToTarget(c))

        def relapse(c):
            c.generate_target()
            c.target.stretch(1, dim=1)
            anim_list.add_animation(MoveToTarget(c))

        # Collapse All

        anim_list.time_step(.2)
        anim_list.add_objects([heads, tails])
        collapse(self)
        collapse(tails)
        collapse(heads)

        for i in range(n_flips * 2):
            # Relapse HT[0], and collapse again
            anim_list.time_step(.2)
            index_mod = i % 2
            anim_list.re_order([self, HT[index_mod - 1], HT[index_mod]])
            relapse(HT[index_mod])
            anim_list.time_step(.2)
            if i < n_flips * 2 - 1:
                collapse(HT[index_mod])
        self.flip_outcomes += [HT[index_mod]]
        anim_list.remove_objects([HT[index_mod - 1]])
        relapse(self)
        return anim_list
    
    def second_flip_split(self, n_flips=1):
        anim_list = AnimationList()

        anim_list.time_step(.5)
        self.generate_target()
        self.target.shift(.7 * RIGHT)
        anim_list.add_animation(MoveToTarget(self))

        for f_o in self.flip_outcomes:
            f_o.generate_target()
            f_o.target.shift(.7 * LEFT)
            anim_list.add_animation(MoveToTarget(f_o))
        return anim_list

    def get_outcome_components(self, end_y_coord):
        outcome_text = self.flip_outcomes[0][1]
        outcome_background = self.flip_outcomes[0][0]
        self.flip_outcomes = []
        outcome_text.generate_target()
        if outcome_text.text == "H":
            outcome_text.target.color = RED
        else:
            outcome_text.target.color = BLUE
        end_location = outcome_text.get_center()
        end_location[1] = end_y_coord
        outcome_text.target.move_to(end_location)
        return outcome_text, FadeOut(outcome_background)


class CoinFlipping(PresentationScene):

    def construct(self):

        # Pockets
        Left_Pocket = Pocket().shift(3 * LEFT + 1.8 * DOWN)
        Right_Pocket = Pocket().shift(3 * RIGHT + 1.8 * DOWN)

        # Coins
        H_biased = Coin(bias=3/4)
        T_biased = Coin(bias=1/4)
        T_biased.move_to(H_biased.get_center() + DOWN)
        Biased_Coins = VGroup(H_biased, T_biased)
        Biased_Coins.move_to(Left_Pocket.get_center())

        Fair1 = Coin()
        Fair2 = Coin()
        Fair2.move_to(Fair1.get_center() + DOWN)
        Fair_Coins = VGroup(Fair1, Fair2)
        Fair_Coins.move_to(Right_Pocket.get_center())

        # Remember current location
        for coin in [H_biased, T_biased, Fair1, Fair2]:
            coin.reset_original()
        Coins = VGroup(Biased_Coins, Fair_Coins)

        # Coin Labels
        #H_biased_label = Text("Coin #1", font_size = 18)
        #H_biased_label.next_to(H_biased, DOWN)
        #T_biased_label = Text("Coin #2", font_size = 18)
        #T_biased_label.next_to(T_biased, DOWN)
        #Fair1_label = Text("Coin #1", font_size = 18)
        #Fair1_label.next_to(Fair1, DOWN)
        #Fair2_label = Text("Coin #2", font_size = 18)
        #Fair2_label.next_to(Fair2, DOWN)
        #Coin_Labels = VGroup(H_biased_label, T_biased_label, Fair1_label, Fair2_label)

        # Bar charts
        def get_bar_percentages(trackers):
            total = 0
            for tracker in trackers:
                total += tracker.get_value()
            if total > 0:
                return [tracker.get_value()/total for tracker in trackers]
            else:
                return [0 for tracker in trackers]
            
        left_trackers = {"H": ValueTracker(0), 
                         "T": ValueTracker(0), 
                         "HH": ValueTracker(0), 
                         "HT": ValueTracker(0), 
                         "TH": ValueTracker(0), 
                         "TT": ValueTracker(0)}
        BC_Left = BarChart(
            values=[0, 0],
            bar_names=["H", "T"],
            y_range=[0, 1, .5],
            y_length=2,
            x_length=3,
            x_axis_config={"font_size": 24},
            bar_colors=[RED, BLUE]
        )
        BC_Left.shift(3 * LEFT + 2.2 * UP)
        BC_Left.add_updater(
            lambda mob: mob.change_bar_values(get_bar_percentages([left_trackers["H"], left_trackers["T"]])))
        
        BC_Left2 = BarChart(
            values=[0, 0, 0, 0],
            bar_names=["HH", "HT", "TH", "TT"],
            y_range=[0, 1, .5],
            y_length=2,
            x_length=3,
            x_axis_config={"font_size": 24},
            bar_colors=[RED, PURPLE, PURPLE, BLUE]
        )
        BC_Left2.shift(3 * LEFT + 2.2 * UP)
        BC_Left2.add_updater(
            lambda mob: mob.change_bar_values(get_bar_percentages([left_trackers[ht] for ht in BC_Left2.bar_names])))

        right_trackers = {"H": ValueTracker(0), 
                         "T": ValueTracker(0), 
                         "HH": ValueTracker(0), 
                         "HT": ValueTracker(0), 
                         "TH": ValueTracker(0), 
                         "TT": ValueTracker(0)}
        BC_Right = BarChart(
            values=[0, 0],
            bar_names=["H", "T"],
            y_range=[0, 1, .5],
            y_length=2,
            x_length=3,
            x_axis_config={"font_size": 24},
            bar_colors=[RED, BLUE]
        )
        BC_Right.shift(3 * RIGHT + 2.2 * UP)
        BC_Right.add_updater(
            lambda mob: mob.change_bar_values(get_bar_percentages([right_trackers["H"], right_trackers["T"]]))
        )

        BC_Right2 = BarChart(
            values=[0, 0, 0, 0],
            bar_names=["HH", "HT", "TH", "TT"],
            y_range=[0, 1, .5],
            y_length=2,
            x_length=3,
            x_axis_config={"font_size": 24},
            bar_colors=[RED, PURPLE, PURPLE, BLUE]
        )
        BC_Right2.shift(3 * RIGHT + 2.2 * UP)
        BC_Right2.add_updater(
            lambda mob: mob.change_bar_values(get_bar_percentages([right_trackers[ht] for ht in BC_Right2.bar_names]))
        )


        # ~~~~~~~~~~~~~~~ANIMATION~~~~~~~~~~~~~~~~~~~
        # Subroutines
        def flip_step(left_coin, right_coin, left_final, right_final):
            left_coin.select(Left_Pocket).simul(right_coin.select(Right_Pocket)).play_animation(self)
            left_coin.flip(final=left_final).simul(right_coin.flip(final=right_final)).play_animation(self)
            #self.play(left_trackers[left_final].animate.set_value(left_trackers[left_final].get_value() + 1), 
            #          right_trackers[right_final].animate.set_value(right_trackers[right_final].get_value() + 1))
            deselecting = left_coin.deselect().simul(right_coin.deselect())
            deselecting.add_animation(left_trackers[left_final].animate.set_value(left_trackers[left_final].get_value() + 1))
            deselecting.add_animation(right_trackers[right_final].animate.set_value(right_trackers[right_final].get_value() + 1))
            deselecting.play_animation(self)
            self.end_fragment()

        def two_flip_step(left_coin, right_coin, left_finals, right_finals):
            left_coin.select(Left_Pocket).simul(right_coin.select(Right_Pocket)).play_animation(self)
            left_coin.flip(final=left_finals[0]).simul(right_coin.flip(final=right_finals[0])).play_animation(self)
            left_coin.second_flip_split().simul(right_coin.second_flip_split()).play_animation(self)
            left_coin.flip(final=left_finals[1]).simul(right_coin.flip(final=right_finals[1])).play_animation(self)
            #self.play(left_trackers[left_final].animate.set_value(left_trackers[left_final].get_value() + 1), 
            #          right_trackers[right_final].animate.set_value(right_trackers[right_final].get_value() + 1))
            deselecting = left_coin.deselect().simul(right_coin.deselect())
            deselecting.add_animation(left_trackers[left_finals].animate.set_value(left_trackers[left_finals].get_value() + 1))
            deselecting.add_animation(right_trackers[right_finals].animate.set_value(right_trackers[right_finals].get_value() + 1))
            deselecting.play_animation(self)
            self.end_fragment()

        # Create
        self.play(FadeIn(Coins, shift=DOWN), Create(Left_Pocket), Create(Right_Pocket), run_time=1)
        self.end_fragment()
        self.play(Create(BC_Left), Create(BC_Right), run_time = .5)
        self.end_fragment()

        # Flip Single Coins
        flip_step(H_biased, Fair2, "H", "T")
        flip_step(T_biased, Fair2, "T", "H")
        flip_step(T_biased, Fair1, "T", "H")
        flip_step(H_biased, Fair1, "H", "T")
        flip_step(T_biased, Fair2, "H", "T")

        # Distribution that we converge to
        self.play(left_trackers["H"].animate.set_value(1),
                  left_trackers["T"].animate.set_value(1),
                  right_trackers["H"].animate.set_value(1),
                  right_trackers["T"].animate.set_value(1), run_time = 1)
        self.end_fragment()

        # Flip Two Coins
        # Morph the charts
        self.play(FadeOut(BC_Left), FadeOut(BC_Right), run_time = .5)
        self.play(Create(BC_Left2), Create(BC_Right2), run_time = .5)
        self.end_fragment()
        
        two_flip_step(H_biased, Fair1, "HH", "TH")
        two_flip_step(T_biased, Fair2, "TT", "HH")
        two_flip_step(H_biased, Fair2, "HH", "HT")
        two_flip_step(T_biased, Fair1, "TH", "TT")

        # Distribution that we converge to
        self.play(left_trackers["HH"].animate.set_value(5),
                  left_trackers["HT"].animate.set_value(3),
                  left_trackers["TH"].animate.set_value(3),
                  left_trackers["TT"].animate.set_value(5), run_time = 1)
        self.end_fragment()

        # Many flips -> Many identical coins
        Biased_Coins.generate_target()
        Biased_Coins.target.move_to([0, 1.5, 0]) 
        self.play(FadeOut(BC_Left2), FadeOut(BC_Right2), FadeOut(Right_Pocket), FadeOut(Left_Pocket), FadeOut(Fair_Coins), MoveToTarget(Biased_Coins), run_time=1)
        self.end_fragment()
        coin_list = [[H_biased], [T_biased]]

        # Set Up Slide With Stacks of Coins
        for i in range(6):
            new_Hb = H_biased.copy()
            new_Tb = T_biased.copy()
            coin_list[0].append(new_Hb)
            coin_list[1].append(new_Tb)
        shift_anim_list = []
        for i, (Hb, Tb) in enumerate(zip(*coin_list)):
            Hb.generate_target()
            Tb.generate_target()
            Hb.target.shift((3 * LEFT) + (i * RIGHT))
            Tb.target.shift((3 * LEFT) + (i * RIGHT))
            shift_anim_list += [MoveToTarget(Hb), MoveToTarget(Tb)]
        self.play(*shift_anim_list, run_time=1)
        self.end_fragment()
        upper_coins = VGroup(*coin_list[0])
        lower_coins = VGroup(*coin_list[1])
        all_coins = VGroup(upper_coins, lower_coins)

        # Label with U
        u0 = MathTex(r"u^{(0)}").next_to(upper_coins[0], LEFT)
        u0.add_updater(lambda o: o.set_color)
        u1 = MathTex(r"u^{(1)}").next_to(lower_coins[0], LEFT)
        U_values = VGroup(u0, u1)
        self.play(Write(u0), Write(u1), run_time = 1)
        self.end_fragment()

        # Flipping
        Data_Label_Line = Line(start = [-3.5, -.5, 0], end = [3.5, -.5, 0])
        Data_Label = Text("Data", font_size=28).next_to(Data_Label_Line, .5 * UP)
        self.play(Create(Data_Label_Line), Create(Data_Label), run_time = .5)
        self.end_fragment()

        def row_flip_step(row, sequence):
            Select_Rect = SurroundingRectangle(all_coins[row])
            self.play(Write(Select_Rect), U_values[row].animate.set_color(YELLOW), run_time = .2)
            self.pause()
            flip_anim_list = all_coins[row][0].flip(sequence[0])
            for i, coin in enumerate(all_coins[row][1:]):
                flip_anim_list = flip_anim_list.simul(coin.flip(sequence[i+1]))
            flip_anim_list.add_animation(FadeOut(Select_Rect))
            flip_anim_list.add_animation(U_values[row].animate.set_color(WHITE))
            flip_anim_list.play_animation(self)

        data = []
        def row_deposit_data(row, step):
            move_to_targets = []
            background_fadeouts = []
            for coin in all_coins[row]:
                text_obj, background_fadeout = coin.get_outcome_components(-1 - step * (.5))
                data.append(text_obj)
                text_to_target = MoveToTarget(text_obj)
                move_to_targets.append(text_to_target)
                background_fadeouts.append(background_fadeout)
            self.play(*background_fadeouts,
                      *move_to_targets, run_time = 1)
            
        row_seqs = [
            (0, "HHHHHTH"),
            (0, "HTHTHHH"),
            (1, "TTTTHTH"),
            (0, "THTHHHH"),
            (1, "HTTTTHT")
        ]
        for step, (row, seq) in enumerate(row_seqs):
            row_flip_step(row, seq)
            row_deposit_data(row, step)
            self.end_fragment()
        
        # Label n
        Data_Group = VGroup(*data)
        Data_Brace = Brace(Data_Group, direction = [-1, 0, 0])
        Data_Brace_Label = MathTex("n").next_to(Data_Brace, LEFT)
        self.play(Write(Data_Brace), Write(Data_Brace_Label), run_time=.5)
        self.end_fragment()

        # Label k
        Source_Brace = Brace(VGroup(all_coins, U_values), direction = [-1, 0, 0])
        Source_Brace_Label = MathTex("k").next_to(Source_Brace, LEFT)
        self.play(Write(Source_Brace), Write(Source_Brace_Label), run_time=.5)
        self.end_fragment()

        # Label d
        Variables_Brace = Brace(all_coins, direction = [0, 1, 0])
        Variables_Brace_Label = MathTex("d").next_to(Variables_Brace, UP)
        self.play(Write(Variables_Brace), Write(Variables_Brace_Label), run_time=.5)
        self.end_fragment()

        Variable_Labels_and_Braces = VGroup(Data_Brace, 
                                            Data_Brace_Label, 
                                            Source_Brace, 
                                            Source_Brace_Label, 
                                            Variables_Brace, 
                                            Variables_Brace_Label)
        Coins_and_Data = VGroup(Data_Group, all_coins, Data_Label, Data_Label_Line, Variable_Labels_and_Braces, U_values)

        # Identifiability
        Coins_and_Data.generate_target()
        old_center = Coins_and_Data.get_center()
        Coins_and_Data.target.scale(.7)
        Coins_and_Data.target.to_edge(LEFT)
        self.play(MoveToTarget(Coins_and_Data), run_time=.5)

        Moments = MathTex(r"\mu^i := \sum_{u} P(u) P(H \; | \: u)^i").shift(UP)
        Identifiability = MathTex(r"d \geq 2k - 1, n \in \frac{1}{\zeta}^{\Omega(k)}").next_to(Moments, DOWN)
        #Improvement = MathTex(r'd \in O(k^2), n \in O \left(\frac{1}{\zeta^2}\right)').next_to(Identifiability, DOWN)
        Citation = MarkupText("Gordon, <b>Mazaheri</b>, Rabani, Schulman (2020)", font_size = 18).next_to(Identifiability, DOWN)
        MathStuff = VGroup(Identifiability, Moments, Citation).center()
        MathStuff.to_edge(RIGHT)
        self.play(Write(Moments), run_time = 1)
        self.end_fragment()
        self.play(Write(Identifiability), run_time = 1)
        self.end_fragment()
        self.play(FadeIn(Citation), run_time = 1)
        self.end_fragment()

        # Mixture of Products
        self.play(FadeOut(MathStuff), run_time = .5)
        Coins_and_Data.generate_target()
        Coins_and_Data.target.scale(1/.7)
        Coins_and_Data.target.move_to(old_center)
        self.play(MoveToTarget(Coins_and_Data), run_time=.5)
        self.end_fragment()
        new_bias_anim_list = []
        
        for coin in coin_list[0] + coin_list[1]:
            new_bias_anim_list += coin.randomize_bias()
        self.play(*new_bias_anim_list, run_time = 1)
        self.end_fragment()

        Coins_and_Data.generate_target()
        Coins_and_Data.target.scale(.7)
        Coins_and_Data.target.to_edge(DOWN)
        self.play(MoveToTarget(Coins_and_Data), run_time=.5)
        self.end_fragment()

        Vertices = [Vertex(label = r'V_' + str(i+1)).next_to(coin_list[0][i], UP).shift(UP) for i in range(7)]
        Mixture_U = Vertex(label=r"U", observed=False).next_to(Vertices[3], UP).shift(UP)
        Edges = [Edge(Mixture_U, V) for V in Vertices]
        MixProdGraph = Graph(Vertices, Edges, unobserved = Mixture_U)
        self.play(Write(MixProdGraph), run_time=2)
        self.end_fragment()

        Coins_Data_Graph = VGroup(Coins_and_Data, MixProdGraph)
        Coins_Data_Graph.generate_target()
        Coins_Data_Graph.target.to_edge(LEFT)
        self.play(MoveToTarget(Coins_Data_Graph), run_time = .5)
        self.end_fragment()

        Moments2 = MathTex(r"\forall \mathbf{S} \subseteq \mathbf{V}, \mu^{\mathbf{S}} := \sum_{u} P(u) \prod_{V_i \in \mathbf{S}} P(v_i = 1 \; | \: u)")
        MomentsWant = MathTex(r"\mu^{V_1, V_1} :", "=", r"\sum_{u} P(u) P(v_1 = 1 \; | \: u)",
                               r"P(v_1 = 1 \; | \: u)")
        MomentsWant2 = MathTex("=", r"\sum_{u} P(u) P(v_1 = 1 \; | \: u)", r"\left(a_i P(v_i = 1 \; | \: u) + a_j P(v_j = 1 \; | \: u) \right)")
        MomentsWant3 = MathTex("=", "a_i", r"\mu^{V_1 V_i}", "+", "a_j", r"\mu^{V_1, V_j}")
        Citation2 = MarkupText("Gordon, <b>Mazaheri</b>, Rabani, Schulman (COLT, 2021)", font_size = 24)
        Citation3 = MarkupText("Gordon, <b>Mazaheri</b>, Rabani, Schulman (CLeaR, 2023)", font_size = 18)

        lines = VGroup(Moments2, MomentsWant, MomentsWant2, MomentsWant3, Citation2)
        lines.scale(.45)
        lines.arrange(DOWN)
        lines.to_edge(RIGHT)
        self.play(Write(lines[0]), run_time = 2)
        self.end_fragment()
        self.play(Write(lines[1]), run_time = 2)
        self.end_fragment()
        self.play(
            TransformMatchingTex(
                lines[1].copy(), lines[2],
                key_map={
                    r'\sum_{u} P(u) P(v_1 = 1 \; | \: u)^2': r'\mu^{V_1 V_1} := \sum_{u} P(u) P(v_1 = 1 \; | \: u)',
                    r"P(v_1 = 1 \; | \: u)" : r"\left(a_i P(v_i = 1 \; | \: u) + a_j P(v_j = 1 \; | \: u) \right)"
                }
            ),
            run_time = 2
        )
        self.end_fragment()
        self.play(
            TransformMatchingTex(
                lines[2].copy(), lines[3],
            ),
            run_time = 2
        )
        self.end_fragment()
        self.play(FadeIn(Citation2), run_time = .2)
        self.end_fragment()




        # K Mix BND Proceedure
        Steps = VGroup(*[
            MarkupText("1. Learn DAG (<b>Mazaheri</b> et. al., ArXiV 2023)", font_size = 24),
            MarkupText("2. Induce Mixtures of Products (<b>Mazaheri</b> et. al., CLeaR 2022)", font_size = 24),
            MarkupText("3. Solve Mixture of Products (<b>Mazaheri</b> et. al., COLT 2021, ArXiV 2023)", font_size = 24),
        ])
        MixProdGraph.generate_target()
        MixProdGraph.target.center().to_edge(UP)
        self.play(MoveToTarget(MixProdGraph), FadeOut(Coins_and_Data), FadeOut(lines), run_time=1)
        self.end_fragment()

        Steps.arrange(DOWN).next_to(MixProdGraph, DOWN)
        vs = MixProdGraph.get_vertices()
        New_Edges = VGroup(*[Edge(vs[i], vs[i+1]) for i in range(6)])
        MixProdGraph.get_edges().add(*New_Edges)
        self.play(Write(New_Edges), Write(Steps[0]), run_time = 1)
        self.end_fragment()

        self.play(*[vs[2 * i+1].condition() for i in range(3)], Write(Steps[1]), run_time = 1)
        self.end_fragment()
        surrounding_rects = [SurroundingRectangle(Vertices[2 * i], color=YELLOW) for i in range(3)]
        self.play(*[Write(SR) for SR in surrounding_rects], runtime = 1)
        self.end_fragment()
        self.play(*[Unwrite(SR) for SR in surrounding_rects], run_time = 1)
        self.end_fragment()
        self.play(*[vs[2 * i +1].uncondition() for i in range(3)],
                  *[vs[2 * i].condition() for i in range(3)], run_time = 1)
        self.end_fragment()
        surrounding_rects_odd = [SurroundingRectangle(Vertices[2 * i + 1], color=YELLOW) for i in range(3)]
        self.play(*[Write(SR) for SR in surrounding_rects_odd], runtime = 1)
        self.end_fragment()
        self.play(Write(Steps[2]), run_time = 1)
        self.end_fragment()
        self.play(*[vs[2 * i].uncondition() for i in range(3)],
                  *[Unwrite(SR) for SR in surrounding_rects_odd], run_time = 1)
        self.end_fragment()

        # New Idea
        vs[0].generate_target()
        vs[1].generate_target()
        vs[0].target.reset_text("T")
        vs[1].target.reset_text("Y")
        self.play(MoveToTarget(vs[0]), MoveToTarget(vs[1]), run_time = .5)
        self.end_fragment()

