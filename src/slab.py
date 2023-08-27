from manim import *


class Slab(Scene):
    memory = VGroup()
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
        self.memory.save_state()
        self.play(
            self.memory[0:5].animate.set_color(RED),
            self.memory[5:10].animate.set_color(ORANGE),
            self.memory[10:15].animate.set_color(YELLOW),
            self.memory[15:20].animate.set_color(GREEN),
        )

        self.wait()
        self.play(self.memory[5:10].animate.set_color(BLUE))
        self.wait()
        self.play(self.memory[20:27].animate.set_color(PURPLE))

        # 碎片
        self.play(
            Indicate(self.memory[5:10]),
            Indicate(self.memory[27:]),
        )

        self.play(Restore(self.memory))

        # 当访问的对象越小的时候, 我们的碎片也就越多.
        self.play(
            self.memory[0:2].animate.set_color(RED_A),
            self.memory[3:6].animate.set_color(YELLOW),
            self.memory[7:11].animate.set_color(RED_B),
            self.memory[11:13].animate.set_color(GREEN),
            self.memory[15:19].animate.set_color(RED_C),
            self.memory[20:25].animate.set_color(PURPLE),
            self.memory[26:].animate.set_color(ORANGE),
        )

        self.play(
            Indicate(self.memory[2]),
            Indicate(self.memory[6]),
            Indicate(self.memory[13:15]),
            Indicate(self.memory[19]),
            Indicate(self.memory[25]),
        )
        self.wait()

        # 如何解决这些碎片呢?
        # 引入 buddy system
