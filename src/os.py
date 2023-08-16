from manim import *
from manim_physics import *

class OS(SpaceScene):

    keys = None
    labels = None
    keyboard = None

    def keyboard(self):
        self.keys = VGroup(*[Rectangle(height=0.6, width=1).set_fill(WHITE, opacity=0.2) for i in range(10)]).arrange(RIGHT, buff=0.1)
        self.labels = VGroup(*[Text(char).scale(0.5).move_to(self.keys[i]) for i, char in enumerate("QWERTYUIOP")])
        self.keyboard = VGroup(self.keys, self.labels)
    def construct(self):
        self.keyboard()
        text1 = Text("关于键盘中断了").set_color("#FE5C2B").scale(2).next_to(self.keyboard, UP)
        text2 = Text("操作系统的故事").set_color("#FE5C2B").scale(2).next_to(self.keyboard, DOWN)
        self.add(self.keyboard, text1, text2)
