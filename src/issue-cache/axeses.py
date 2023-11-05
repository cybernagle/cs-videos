from manim import *
import numpy as np
import os
import random

class PercentageUsage(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1, 10, 1], y_range=[-0.1, 1, 0.1], color=BLUE,
            y_axis_config={
                "unit_size": 20,
                "font_size": 30,
                "include_numbers": True,
                "label_direction": LEFT,
                "include_tip": False,
                "label_direction": LEFT,
            },
        )
        ax_labels = ax.get_axis_labels(x_label="Time", y_label="Percentage")

        cpu = ax.plot(
            lambda x: np.random.uniform(0.50, 0.60),
            color=RED, x_range=[0, 10], use_smoothing=False)

        memory = ax.plot(
            lambda x: np.random.uniform(0.70, 0.75) if x < 5 else np.random.uniform(0.70, 0.75)*1.05,
            color=YELLOW, x_range=[0, 10], use_smoothing=False)

        disks = ax.plot(
            lambda x: np.random.uniform(0.40, 0.50) if x < 5 else np.random.uniform(0.40, 0.50)*1.5,
            color=ORANGE, x_range=[0, 10], use_smoothing=False)

        errors = ax.plot(
            lambda x: 0 if x < 5 else np.random.uniform(0.0,0.1 ),
            color=ORANGE, x_range=[0, 10], use_smoothing=False)

        self.add(ax, cpu, memory, disks, ax_labels)
        self.wait()
        self.add(errors)

        self.wait()

        self.remove(ax, cpu, memory, disks, ax_labels,errors)

        bx = Axes(
            x_range=[-1, 10, 1], y_range=[-0.1, 1, 0.1], color=GREEN,
            y_axis_config={
                "unit_size": 20,
                "font_size": 30,
                "include_numbers": True,
                "label_direction": LEFT,
                "include_tip": False,
                "label_direction": LEFT,
            },

        )
        bx_labels = ax.get_axis_labels(x_label="Time", y_label="Percentage")

        disks_detail = ax.plot(
            lambda x: np.random.uniform(0.60, 1),
            color=ORANGE, x_range=[0, 10], use_smoothing=False)

        self.add(bx, disks_detail, bx_labels)

        self.wait()
        self.remove(disks_detail, bx_labels)

        self.add(memory, errors)

        indicator = Circle(radius=0.1).move_to(memory)
        self.play(FadeIn(indicator))

        self.wait()
