from manim import *

class application_in_stack(Scene):
    stack = None
    def create_stack(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ["", "" ,"" ,'', '', '', '', "",""]
        for i in range(len(text)):
            r_color = RED
            height = 0.5
            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.stack = VGroup(chunk_group, text_group)

    def construct(self):
        self.create_stack()
        self.stack.shift(LEFT*3+UP*2.5)
        self.add(self.stack)
        # 首先在栈底, 是我们的 main function 
        one = Text("0x165").scale(0.5).move_to(self.stack[0][-1])
        two  = Text("0x178").scale(0.5).move_to(self.stack[0][-3])
        three = Text("0x183").scale(0.5).move_to(self.stack[0][-5])
        self.stack[0][-1].set_color(PURPLE_A),
        self.stack[0][-2].set_color(PURPLE_A),
        self.stack[0][-3].set_color(PURPLE_A),
        self.stack[0][-4].set_color(PURPLE_A),
        self.stack[0][-5].set_color(PURPLE_A),
        self.add(one, two, three)

        call = Text("How Call \nStack Works?").scale(2).next_to(self.stack, RIGHT)
        self.add(call)

