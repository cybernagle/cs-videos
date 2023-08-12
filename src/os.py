from manim import *
from manim_physics import *



class OS(SpaceScene):
    def construct(self):
        text = Text(":-)").set_color("#00FFFF").scale(2)
        line = Line(start=5*LEFT+3*DOWN, end=5*RIGHT+3*DOWN,buff=1)
        self.add(text, line)
        self.make_rigid_body(text)  # Mobjects will move with gravity
        self.make_static_body(line)

        self.wait(5)
