from manim import *

class application_in_stack(Scene):

    memory = None
    cs = None
    gdt = None
    stack = None

    def create_stack(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ["", "" ,"" ,'', '', '', '']
        for i in range(len(text)):
            r_color = BLUE
            height = 0.5
            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.stack = VGroup(chunk_group, text_group)

    def create_gdt(self):
        table = Table(
            [["0", "kernel code 0x0"], 
             ["1", "kernel data"], 
             ["2", "user code 0x123"], 
             ["3", "user data"]],
            include_outer_lines=True,
            h_buff=1.5,
            v_buff=0.7,
            line_config={"stroke_color": WHITE, "stroke_width": 1},
            background_stroke_color=WHITE
        )
        self.gdt = table
        
    def create_memory(self) -> VGroup:
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0
        for i in range(30):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=0.4, height=1,
                             grid_xstep=0.5, grid_ystep=1)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, RIGHT, buff=0)
            mem.add(rect)

        mem.shift(LEFT*6)
        self.memory = mem

    def create_cs(self):
        keys = VGroup(*[Rectangle(height=0.5, width=0.5).set_fill(WHITE, opacity=0.2) for i in range(4)]).arrange(RIGHT, buff=0)
        labels = VGroup(*[Text(char).scale(0.5).move_to(keys[i]) for i, char in enumerate("1011")])
        self.cs = VGroup(keys, labels)

    def construct(self):

        self.create_memory()
        self.memory[0:15].set_color(BLUE)
        self.memory[15:30].set_color(YELLOW)
        self.memory.shift(DOWN*3)

        self.create_stack()
        stack2 = self.stack.copy().shift(UP*2+RIGHT*3).set_color(YELLOW)
        self.stack.shift(UP*2+LEFT*3).set_COLOR(BLUE)

        self.play(Create(self.memory))
        self.play(Create(self.stack))
        self.play(Create(stack2))
        self.wait()
