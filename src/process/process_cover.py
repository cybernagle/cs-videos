from manim import *
import random

class Process(Scene):
    code = None

    def proc(self):
        self.code = Code(
            file_name="./process.c",
            tab_width=4, language="C", style="solarized-dark").scale(0.6)


    def construct(self):
        self.proc()
        self.add(self.code.shift(RIGHT*3))
        intro = Text("Porcess Struct", color=BLUE).scale(1.5).next_to(self.code, LEFT).shift(UP*0.5)
        intro2 = Text("Introduction", color=BLUE).scale(1.5).next_to(intro, DOWN)
        
        self.add(intro, intro2)
        

