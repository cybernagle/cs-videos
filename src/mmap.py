from manim import *

class Trap(Scene):

    memory = None
    linked = None
    square_mem = None

    def create_memory(self) -> VGroup:
        mem = VGroup()
        for i in range(3):
            rect = Rectangle(color=YELLOW, fill_opacity=0.5, width=0.4, height=1,
                             grid_xstep=0.5, grid_ystep=1)
            rect.next_to(mem, RIGHT, buff=0)
            mem.add(rect)
        self.memory = mem

    def create_square_mem(self, color=BLUE) -> VGroup():
        squares = VGroup(*[
            Square(color=color,side_length=0.5, fill_opacity=0.2).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(9)
            for j in range(4)
        ])
        #self.square_mem = squares
        return squares

    def linked(self) -> VGroup:
        arrows = VGroup(*[
            DoubleArrow(
                square.get_center() + 0.05*RIGHT,
                square.get_center() + 0.95*RIGHT,
                stroke_width=0.5,
            )
            for square in self.square_mem
        ])

        self.linked = arrows

    def construct(self):
        self.square_mem = self.create_square_mem()

        self.add(self.square_mem)
        self.wait()
        self.play(
            self.square_mem.animate.arrange(RIGHT, buff = 0.5).to_edge(LEFT),
        )
        self.linked()
        self.add(self.linked)

        physical = VGroup(self.square_mem, self.linked)

        self.play(physical.animate.shift(DOWN*3))

        disk = self.create_square_mem(color=PURPLE)
        disk.arrange(RIGHT, buff = 0.5).to_edge(LEFT)
        self.add(disk)
        self.play(disk.animate.shift(UP*3))

        self.wait()
        self.create_memory()
        self.memory.shift(LEFT*6)
        self.play(Create(self.memory))
        self.wait()
