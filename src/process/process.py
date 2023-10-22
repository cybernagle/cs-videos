from manim import *

class Process(Scene):
    memory = None
    cpu = None

    def create_virtual_memory(self, length=30,width=1.5, height=0.5, color=YELLOW) -> VGroup:
        mem = VGroup()
        width = width
        height = height
        for i in range(length):
            buff = 0
            rect = Rectangle(color=color, fill_opacity=0.5, width=width, height=height,
                             grid_xstep=width, grid_ystep=height)
            rect.next_to(mem, RIGHT, buff=buff)
            mem.add(rect)

        mem.move_to(ORIGIN)
        return mem

    def create_physical_mem(self, color=BLUE) -> VGroup():
        squares = VGroup(*[
            Square(color=color,side_length=0.5, fill_opacity=0.2).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(9)
            for j in range(4)
        ])
        return squares

    def linked(self, memory) -> VGroup:
        arrows = VGroup(*[
            DoubleArrow(
                square.get_center() + 0.05*RIGHT,
                square.get_center() + 0.95*RIGHT,
                stroke_width=0.5,
            )
            for square in memory
        ])

        return linked

    def init_cpu(self):
        self.cpu = VGroup(
            *[Square(side_length=0.8, fill_opacity=0.5).set_color(BLUE) for _ in range(4)]
        )
        self.cpu.arrange_in_grid(2,2,buff=0)

    def shift_asm(self,obj, index):
        binarys = obj
        self.play(
            binarys[index].animate.shift(RIGHT*5)
        )

    def decode(self,obj, target, index):
        binarys = obj
        asm = target
        asm_line = Text(asm[index]).scale(0.3).move_to(binarys[index])
        self.play(Transform(binarys[index], asm_line), run_time=1)

    def construct(self):

        elfhdr = self.create_virtual_memory(length=2, color=GREEN)
        text = self.create_virtual_memory(length=3, color=YELLOW)
        stack = self.create_virtual_memory(length=1, color=RED)

        elfhdr.shift(LEFT*5)
        text.next_to(elfhdr, RIGHT)
        stack.next_to(text, RIGHT)

        elfhdr_desc = Text("elfheader").scale(0.5).next_to(elfhdr[0], DOWN)
        text_desc = Text(".text").scale(0.5).next_to(text[0], DOWN)
        stack_desc = Text("stack").scale(0.5).next_to(stack[0], DOWN)

        self.add(
            elfhdr, text, stack,
            elfhdr_desc, text_desc, stack_desc
        )

        virtual_memory = VGroup(
            elfhdr, text, stack,
            elfhdr_desc, text_desc, stack_desc
        )
        self.play(
            virtual_memory.animate.shift(UP*3)
        )
