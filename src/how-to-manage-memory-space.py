from manim import *

class HowToManageMemSpace(MovingCameraScene):
    memory = VGroup()
    quare_mem = VGroup()
    linked = VGroup()

    def create_memory(self) -> VGroup:
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0
        for i in range(9):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                      grid_xstep=2.0, grid_ystep=0.5)
            #for j in range(3):
            #    square = Square(color=BLUE,fill_opacity=0.5, width=0.5, height=0.5)
            #    rect.add(square)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, DOWN, buff=0)
            addr.next_to(rect, LEFT, buff=0.2)
            mem.add(rect)
            addresses.add(addr)
            if (start_addr == 0):
                start_addr += 0x1FFFFFFF
            else:
                start_addr += 0x20000000

        memory = VGroup(mem, addresses).shift(UP*2)
        self.memory = memory

    def square_mem(self) -> VGroup():
        squares = VGroup(*[
            Square(color=BLUE,side_length=0.5, fill_opacity=0.2).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(9)
            for j in range(4)
        ])
        self.square_mem = squares

    def linked(self) -> VGroup:
        arrows = VGroup(*[
            Arrow(
                square.get_center()+0.05*RIGHT,
                square.get_center() + 0.95*RIGHT,
                stroke_width=0.5,
            )
            for square in self.square_mem
        ])

        self.linked = arrows

    def allcated(self) -> VGroup:
        pass

    def construct(self):
        self.create_memory()
        self.play(FadeIn(self.memory))
        self.square_mem()
        self.square_mem.align_to(self.memory[0], UL)
        self.play(
            FadeIn(self.square_mem),
            FadeOut(self.memory[0])
        )

        self.play(
            self.square_mem.animate.arrange(RIGHT, buff = 0.5).to_edge(LEFT),
            FadeOut(self.memory),
            run_time=3
        )

        self.linked()
        for i,j in enumerate(self.linked, start=1):
            self.play(Create(j), run_time=1.0/i)

        self.play(
            self.camera.frame.animate.move_to(self.square_mem[0].get_center()),
            self.square_mem[0].animate.set_color(RED),
        )
        self.play(
            self.camera.frame.animate.scale(0.1)
        )

        table = Table(
            [["REF", "FLAGS", "PROPERTY"],
             ["P_LINK", "PRE_P_LINK", "PRE_VADDR"]],
            include_outer_lines=True,
            include_background_rectangle=True,
            background_rectangle_color=BLUE,
        ).move_to(self.square_mem[0].get_center()).scale_to_fit_width(self.square_mem[0].get_width()*1.2).set_stroke(width=0.2)

        temp = table.copy()

        self.play(ReplacementTransform(self.square_mem[0], table))
        self.play(
            ReplacementTransform(
                table.get_rows()[0][0],
                Text("0").scale(0.06).set_stroke(width=0.2).move_to(table.get_rows()[0][0].get_center())
            ),
            ReplacementTransform(
                table.get_rows()[0][1],
                Text("0").scale(0.06).set_stroke(width=0.2).move_to(table.get_rows()[0][1].get_center())
            ),
            ReplacementTransform(
                table.get_rows()[0][2],
                Text("1000").scale(0.06).set_stroke(width=0.2).move_to(table.get_rows()[0][2].get_center())
            )
        )

        for i, obj in enumerate(self.square_mem[1:], start=1):
            t = temp.copy().move_to(obj.get_center())\
                               .scale_to_fit_width(obj.get_width()*1.2)\
                               .set_stroke(width=0.2)
            self.play(
                self.camera.frame.animate.move_to(obj.get_center()),
                ReplacementTransform(obj, t),
                ReplacementTransform(
                    t.get_rows()[0][0],
                    Text("0").scale(0.06).set_stroke(width=0.2).move_to(t.get_rows()[0][0].get_center())
                ),
                ReplacementTransform(
                    t.get_rows()[0][1],
                    Text("0").scale(0.06).set_stroke(width=0.2).move_to(t.get_rows()[0][1].get_center())
                ),
                ReplacementTransform(
                    t.get_rows()[0][2],
                    Text("0").scale(0.06).set_stroke(width=0.2).move_to(t.get_rows()[0][2].get_center())
                ),
                run_time=1/i
            )

        self.wait()

        self.play(
            self.camera.frame.animate.scale(40),
        )
        self.play(
            self.camera.frame.animate.move_to(self.square_mem[20])
        )

        # allocating memory

        all_mem = SurroundingRectangle(self.square_mem, color=RED)
        self.play(Create(all_mem))
        allocation_group = VGroup()
        length = 36
        for i in range(3):
            length /= 2
            s = SurroundingRectangle(self.square_mem[0:length], color=RED)
            allocation_group.add(s)

        allocated = always_redraw(lambda: Brace(self.square_mem, direction=DOWN, buff=SMALL_BUFF))
        text = allocated.get_text("Allocated Memory").set_color(RED)
        self.play(
            GrowFromCenter(allocated),
            Write(text))

        self.wait()
