from manim import *

class application_in_stack(Scene):

    memory = None
    cs = None
    gdt = None
    stack = None

    main = None
    io = None
    test = None
    getbuf = None
    gets = None
    launch = None

    def init_code(self):
        # 0x21
        self.main = Code(
            file_name="./code/application_in_stack_main.S",
            tab_width=4, language="C", style="solarized-dark").scale(0.5)
        # 0x20
        self.launch = Code(
            file_name="./code/application_in_stack_launch.S",
            tab_width=4, language="C", style="solarized-dark").scale(0.5).next_to(self.main,direction=DOWN,aligned_edge=LEFT)
        # 0x19
        self.test = Code(
            file_name="./code/application_in_stack_test.S",
            tab_width=4, language="C", style="solarized-dark").scale(0.5).next_to(self.launch,direction=DOWN,aligned_edge=LEFT)

        # 0x18
        self.getbuf = Code(
            file_name="./code/application_in_stack_getbuf.S",
            tab_width=4, language="C", style="solarized-dark").scale(0.5).next_to(self.main,direction=RIGHT,aligned_edge=UP)
        # 0x17
        self.gets = Code(
            file_name="./code/application_in_stack_gets.S",
            tab_width=4, language="C", style="solarized-dark").scale(0.5).next_to(self.getbuf,direction=DOWN,aligned_edge=LEFT)
        # 0x16
        self.io = Code(
            file_name="./code/application_in_stack_IO.S",
            tab_width=4, language="C", style="solarized-dark").scale(0.5).next_to(self.gets,direction=DOWN,aligned_edge=LEFT)

        self.asm = VGroup(
            self.main,
            self.io,
            self.test,
            self.getbuf,
            self.gets,
            self.launch,
        )


    def shift_code_indicator(self, index, source,target , size=1, run_time=1):
        if size <= 1:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index])),
                Indicate(target.code[index])
            )
        else:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index:index+size])),
                Indicate(target.code[index:index+size]),
                run_time=run_time
            )

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
        self.add(self.memory)
        self.play(
            self.memory[0:15].animate.set_color(BLUE),
            self.memory[15:30].animate.set_color(YELLOW)
        )
        self.wait()
        self.play(
            self.memory.animate.shift(DOWN*3)
        )



        self.play(
            self.memory[16:22].animate.set_color(PURPLE)
        )

        self.init_code()
        self.asm.shift(UP*2.5+LEFT)

        self.play(
            Transform(self.memory[21].copy(),self.main)
        )
        self.play(
            Transform(self.memory[20].copy(),self.launch)
        )
        self.play(
            Transform(self.memory[19].copy(),self.test)
        )
        self.play(
            Transform(self.memory[18].copy(),self.getbuf)
        )
        self.play(
            Transform(self.memory[17].copy(),self.gets)
        )
        self.play(
            Transform(self.memory[16].copy(),self.io)
        )

        indicator = SurroundingRectangle(self.main.code[2])
        self.play(
            Create(indicator),
            Indicate(self.main.code[2])
        )

        # this just a bunch of shit.
        reg = Text("cs:rip", color=BLUE).scale(0.5).next_to(self.memory[21],UP)
        #rbp = Text("rbp", color=BLUE).scale(0.5).next_to(self.stack[1][0],DOWN)
        #rsp = Text("rsp", color=BLUE).scale(0.5).next_to(self.stack[1][0],DOWN)
        self.play(Create(reg))
        self.wait()
        self.play(reg.animate.next_to(self.memory[20], UP))
        self.shift_code_indicator(4, indicator, self.launch)
        self.wait()
        self.play(reg.animate.next_to(self.memory[19], UP))
        self.shift_code_indicator(4, indicator, self.test)
        self.wait()
        self.play(reg.animate.next_to(self.memory[18], UP))
        self.shift_code_indicator(3, indicator, self.getbuf)
        self.wait()
        self.play(reg.animate.next_to(self.memory[17], UP))
        self.shift_code_indicator(3, indicator, self.gets)
        self.wait()
        self.play(reg.animate.next_to(self.memory[16], UP))
        self.shift_code_indicator(1, indicator, self.io)
        self.wait()

        self.play(reg.animate.next_to(self.memory[17], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.gets)
        self.play(reg.animate.next_to(self.memory[18], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.getbuf, size=1, run_time=0.3)
        self.play(reg.animate.next_to(self.memory[19], UP),run_time=0.3)
        self.shift_code_indicator(4, indicator, self.test, size=1, run_time=0.3)
        self.play(reg.animate.next_to(self.memory[20], UP),run_time=0.3)
        self.shift_code_indicator(4, indicator, self.launch, size=1, run_time=0.3)
        self.play(reg.animate.next_to(self.memory[21], UP),run_time=0.3)
        self.shift_code_indicator(2, indicator, self.main, size=1, run_time=0.3)

        # 返回的时候, 要怎么工作呢?
        # 是时候引入我们的栈空间
        self.play(
            self.memory[29].animate.set_color(RED),
        )

        self.create_stack()
        #kernel_stack = self.stack.copy().shift(UP*2+RIGHT*3).set_color(BLUE)
        self.play(self.stack.next_to(self.memory[29]).animate.shift(UP*4+LEFT*12))

        # 首先我们在栈底记

        self.play(reg.animate.next_to(self.memory[20], UP))
        self.shift_code_indicator(4, indicator, self.launch)
        self.wait()
        self.play(reg.animate.next_to(self.memory[19], UP))
        self.shift_code_indicator(4, indicator, self.test)
        self.wait()
        self.play(reg.animate.next_to(self.memory[18], UP))
        self.shift_code_indicator(3, indicator, self.getbuf)
        self.wait()
        self.play(reg.animate.next_to(self.memory[17], UP))
        self.shift_code_indicator(3, indicator, self.gets)
        self.wait()
        self.play(reg.animate.next_to(self.memory[16], UP))
        self.shift_code_indicator(1, indicator, self.io)
        self.wait()

        self.wait()
