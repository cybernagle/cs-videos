from manim import *
import random
import pickle

class FontSize(Scene):
    def construct(self):

        # Pango stuff
        styles = [
            BOLD,
            # Only for Pango from below
            SEMIBOLD,
            ULTRABOLD,
            HEAVY,
            ULTRAHEAVY,
        ]

        group = VGroup()
        for i in styles:
            t = Text(str(1),font_size=100,color="#008000",weight=i).next_to(group)
            group.add(t)

        group.shift(LEFT*3)
        self.add(group)
            
