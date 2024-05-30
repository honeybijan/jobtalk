from manim import *
from manim_revealjs import PresentationScene, COMPLETE_LOOP

config.video_dir = "./videos"

import random
import numpy as np
import math
import pandas as pd

from GraphManim import *

class GlobalWarming(PresentationScene):

    def construct(self):
        # Real Data
        title = Text("Heterogeneous Data").to_edge(UP, buff=.5)
        self.add(title)
        real_data_ax = Axes(x_range=[2015, 2021, 1], 
                            y_range=[-15, 15, 5], 
                            x_length=12, y_length=8, 
                            x_axis_config={"include_numbers": True, 
                                           "decimal_number_config": {"group_with_commas": False, "num_decimal_places": 0}}).scale(.8).center()
        #time_label = real_data_ax.get_axis_labels(x_label=r'\text{Year}')
        citation = Text("Data from Copernicus Climate Change Service (processing by Our World in Data) and NOAA", font_size=14).next_to(real_data_ax, DOWN)
        time_label = Text("Year").scale(.5).next_to(real_data_ax, RIGHT)
        df = pd.read_csv("data/co2_and_temp.csv")
        dots = []
        adjusted_co2 = df['CO2'] - np.average(df['CO2'])
        adjusted_temp = df['Temperature'] - np.average(df['Temperature'])
        for (y, t, c) in zip(df['Year_Decimal'], adjusted_temp, adjusted_co2):
            temp_dot = Dot(real_data_ax.c2p(y, t), color=RED, radius=.05)
            co2_dot = Dot(real_data_ax.c2p(y, c), color=BLUE, radius=.05)
            dots.append(VGroup(temp_dot, co2_dot))
        self.add_foreground_mobject(real_data_ax)
        self.add(time_label, citation)
        co2_label = Tex(r"$\text{CO}_2$ in PPM (from avg)", color=BLUE).scale(.5).next_to(co2_dot, UP).shift(.5, RIGHT)
        temp_label = Text(u'Temperature \N{DEGREE SIGN}C (from avg)', color=RED).scale(.5).next_to(temp_dot, DOWN).shift(.5, RIGHT + DOWN)

        self.play(LaggedStart(*[Create(dot) for dot in dots], lag_ratio=.05))
        self.play(Write(co2_label), Write(temp_label), runtime=.5)
        self.end_fragment()

        # Cheating Data
        self.remove(real_data_ax, time_label, *dots, temp_label, co2_label, citation)
        temperatures = []
        co2s = []
        times = []
        ss_temperatures = []
        ss_co2s = []
        ss_times = []
        period = 20
        for i in range(100):
            x = i
            if x % 20 == 0:
                ss_times.append(x)
                ss_temperatures.append(33 + (.3 * x) + 20 * np.sin(x * (2 * math.pi)/period))
                ss_co2s.append(37 + (.3 * x)  - 20 * np.sin(x * (2 * math.pi)/period))
            times.append(x)
            temperatures.append(33 + (.3 * x) + 20 * np.sin(x * (2 * math.pi)/period))
            co2s.append(37 + (.3 * x) - 20 * np.sin(x * (2 * math.pi)/period))

        # Animate the creation of Axes
        left_ax = Axes(x_range=[-5, 100, 10], y_range=[-5, 100, 10], x_length=12, y_length=10).scale(.4).to_edge(LEFT, buff = 1)
        year_label = Tex("Time").scale(.5).next_to(left_ax, DOWN, buff = .25)

        right_ax = Axes(x_range=[-5, 100, 10], y_range=[-5, 100, 10], x_length=12, y_length=10).scale(.4).to_edge(RIGHT, buff = 1)
        temp_label = Tex("Temperature").scale(.5).rotate(math.pi/2).next_to(right_ax, LEFT, buff = .25)
        CO2_label = MathTex(r"\text{CO}_2").scale(.5).next_to(right_ax, DOWN, buff = .25)

        labels = VGroup(year_label, temp_label, CO2_label)
        self.play(Write(left_ax), Write(labels), Write(right_ax))
        self.end_fragment()

        # Animate the creation of dots
        def dot_set(time, temp, co2):
            temp_dot = Dot(left_ax.c2p(time, temp), color=RED, radius=.05)
            co2_dot = Dot(left_ax.c2p(time, co2), color=BLUE, radius=.05)
            both_dot = Dot(right_ax.c2p(co2, temp), color=PURPLE, radius=.05)
            return VGroup(temp_dot, co2_dot, both_dot)
        partial_dots = [dot_set(time, temp, co2) for time, temp, co2 in zip(ss_times, ss_temperatures, ss_co2s)]
        full_dots = [dot_set(time, temp, co2) for time, temp, co2 in zip(times, temperatures, co2s)]
        self.play(LaggedStart(*[Create(partial_dot) for partial_dot in partial_dots], lag_ratio=.05))
        self.end_fragment()
        self.play(LaggedStart(*[Create(full_dot) for full_dot in full_dots], lag_ratio=.05))
        self.end_fragment()
        
        both_graphs = VGroup(*full_dots, *partial_dots, right_ax, left_ax, temp_label, CO2_label, year_label)
        both_graphs.generate_target()
        both_graphs.target.scale(.8).next_to(title, DOWN, buff=.5)
        simpson=Text("Simpson's Paradox").scale(.5).next_to(both_graphs, DOWN, buff=.2).shift(.75 * UP)
        simpson_cite = Paragraph('Simpson, Edward H. (1951). "The Interpretation of Interaction in Contingency Tables".\n\tJournal of the Royal Statistical Society, Series B. 13: 238–241', alignment=True).scale(.25).next_to(simpson, DOWN)
        self.play(MoveToTarget(both_graphs))
        self.play(Write(simpson), FadeIn(simpson_cite))
        self.end_fragment()