from manim import *

class Mmap(Scene):

    def create_square_mem(self, color=BLUE) -> VGroup():
        squares = VGroup(*[
            Square(color=color,side_length=0.5, fill_opacity=0.2).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(9)
            for j in range(4)
        ])
        return squares

    def construct(self):
        self.square_mem = self.create_square_mem()

        # 这是我们的物理内存
        self.add(self.square_mem.shift(RIGHT))
        pgfault = Text("mmap &").scale(2).next_to(self.square_mem,LEFT).shift(UP*0.2)
        self.add(
            pgfault,
            Text("page fault").next_to(pgfault, DOWN),
        )
