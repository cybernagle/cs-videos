from manim import *

class Trap(Scene):

    memory = None
    cs = None
    gdt = None

    def create_gdt(self):
        table = Table(
            [["0:", "kernel code 0x0"], 
             ["1:", "kernel data"], 
             ["2:", "user code 0x123"], 
             ["3:", "user data"]],
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

        self.memory = mem

    def create_cs(self):
        keys = VGroup(*[Rectangle(height=0.5, width=0.5).set_fill(WHITE, opacity=0.2) for i in range(4)]).arrange(RIGHT, buff=0)
        labels = VGroup(*[Text(char).scale(0.5).move_to(keys[i]) for i, char in enumerate("1011")])
        self.cs = VGroup(keys, labels)

    def construct(self):
        reg = Text("cs:rip")
        self.play(Create(reg))

        self.create_memory()
        self.memory.shift(LEFT*6)
        self.play(
            reg.animate.next_to(self.memory, UP, buff=1.5),
            Create(self.memory)
        )

        reg.save_state()
        self.wait()
        self.play(
            reg.animate.next_to(self.memory[0],UP)
        )
        self.wait()
        self.play(
            reg.animate.next_to(self.memory[29],UP)
        )
        self.wait()
        self.play(Restore(reg))

        self.wait()
        self.play(
            self.memory[0:15].animate.set_color(BLUE),
            self.memory[15:30].animate.set_color(YELLOW)
        )

        self.wait()
        kernel_addr = Tex(r"$\texttt{0x0}$", font_size = 36).next_to(self.memory[0], UP)
        user_addr = Tex(r"$\texttt{0x123}$", font_size = 36).next_to(self.memory[15], UP)
        self.play(
            Create(kernel_addr),
            Create(user_addr),
        )

        reg.save_state()
        self.wait()
        self.play(
            reg.animate.next_to(self.memory[15], DOWN)
        )

        self.wait()
        self.play(
            reg.animate.next_to(self.memory[0], DOWN)
        )
        self.wait()
        self.play(Restore(reg))

        self.create_cs()
        self.cs.move_to(reg)

        self.wait()
        value = Tex(r"$\texttt{0xB}$", font_size = 36).move_to(reg)
        self.play(ReplacementTransform(reg, value))
        self.wait()
        self.play(
            ReplacementTransform(value, self.cs)
        )

        self.play(Indicate(
            self.cs[0][2:]
        ))
        self.wait()

        self.create_gdt()
        self.gdt.scale(0.5).next_to(self.memory[25], UP, buff=0.5)
        self.play(Create(self.gdt))

        self.play(Indicate(
            self.gdt.get_cell((3,1))
        ))

        self.wait()
        self.play(Indicate(
            self.gdt.get_cell((3,0))
        ))

        self.play(
            self.cs.animate.next_to(self.memory[15], DOWN)
        )

        labels_final = VGroup(*[Text(char).scale(0.5).move_to(self.cs[0][i]) for i, char in enumerate("00")])
        self.play(
            Transform(self.cs[1][0:2], labels_final)
        )

        self.wait()
        self.play(
            Indicate(self.gdt.get_cell((1,1)))
        )

        self.wait()
        self.play(
            self.cs.animate.next_to(self.memory[0], DOWN)
        )

        labels_final = VGroup(*[Text(char).scale(0.5).move_to(self.cs[0][i+2]) for i, char in enumerate("00")])
        self.play(
            Transform(self.cs[1][2:], labels_final)
        )
        self.wait()
