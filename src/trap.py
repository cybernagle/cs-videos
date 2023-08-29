from manim import *

class Trap(Scene):

    memory = None
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

        self.memory = mem

    def construct(self):
        self.create_memory()
        self.memory.shift(LEFT*6)
        self.add(self.memory)

        self.play(
            self.memory[0:15].animate.set_color(BLUE),
            self.memory[15:30].animate.set_color(YELLOW),
        )

        kernel_addr = Tex(r"$\texttt{0x1234}$", font_size = 36).next_to(self.memory[0], UP)
        user_addr = Tex(r"$\texttt{0x4567}$", font_size = 36).next_to(self.memory[15], UP)
        self.play(
            Create(kernel_addr),
            Create(user_addr),
        )
        self.wait()

