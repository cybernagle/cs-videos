from manim import *

class Trap(Scene):

    memory = None
    cs = None
    gdt = None

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

        self.memory[0:15].set_color(BLUE),
        self.memory[15:30].set_color(YELLOW)

        user = Text("User Mode ").scale(1.5).next_to(self.memory[10], UP,buff=0.5)
        trap = Text("Trap").scale(2).set_color(RED).next_to(user, RIGHT, buff=0.5)
        kernel = Text("To Kernel Mode").scale(1.5).next_to(self.memory[-15], DOWN, buff=0.5)

        self.add(user, kernel, trap)
