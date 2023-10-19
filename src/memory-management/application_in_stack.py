from manim import *

script = """
这是一块内存, 黄色区域是用户空间, 蓝色区域是内核空间.
它们的地址是从 60 - 2-3-0

在1-6-0 到1b0 的位置, 我们存放了应用程序的代码块.
分别为 main 函数
launch 函数
test 函数
getbuf 函数
gets 函数
IO 函数.

其中, main 函数会调用 launch 函数, launch 函数会调用 test 函数, test 会调用 getbuf, getbuf 会调用 gets
gets,会调用 IO

每个进程在完成其执行后,都会返回到上一个函数.那么它们是怎么继续执行前段函数的代码的呢?

答案是上个函数执行的地址,被存放在了栈当中.
我们假设 2-3-0 是我们用户栈空间.

当 main 执行到 callq 1-7-0 的时候,其当前执行的地址会被 push 到栈当中.
换句话说, csrip 所指向的地址, 会被push 到栈当中

这里我们假设 main 执行到了 1-6-5 的位置,跳转到launch函数.
而在 luanch 函数当中, sub 1-0, rsp 是申请栈空间用于存储参数.
紧接着 luanch 执行到 callq, test, 或者说, callq 1-8-0 这个地址.同样, 也将当前执行的地址, 我们假设是1-7-8 push 到栈中.随后跳转到
1-8-0 也就是 test 函数开始执行, test 的逻辑差不多.
sub 1-0, rsp , 申请栈空间, 然后跳转到 getbuf
getbuf 申请栈空间, 跳转到 
gets 再跳转到 IO
这里的 IO 我们会看到一个长跳转指令, 也就是 相对 rip + 50 的地址上面.
注意这里的跳转指令只是相对 rip ,而不是 cs rip ,所以它没有用进行用户态到内核态的切换.
用户态到内核态的切换是在 rip + 50 的这个地址的代码当中的系统调用来进行完成.
在执行 rip+5-0 的这个系统调用之后, cs rip 将陷入到内核态当中,执行系统调用 IO.
然后, 程序将按照原路径返回.
更具体一点, 用户程序从栈中获取到gets的需要继续执行的地址1-a-3, 并跳转过去, 执行完gets函数,从栈中获取到getbuf需要继续执行的地址 1-9-1然后返回到test 地址 183, 接下来都是一样的逻辑, test 再返回到launch地址 178, launch 执行完返回到 main 的 165 的位置.

这样, 我们就完整的完成了整个程序的执行过程.
最后留一个小问题, 我们在最初的地方提到6-0 到 230 这个地址空间, 是虚拟地址空间, 还是物理地址空间?

"""
class application_in_stack(Scene):

    memory = None
    address = None
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
        start_addr = 0x60
        for i in range(30):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=0.4, height=1,
                             grid_xstep=0.5, grid_ystep=1)
            rect.next_to(mem, RIGHT, buff=0)
            addr = Text(hex(start_addr), font_size = 10.5).next_to(rect, DOWN, buff=0.1)
            start_addr += 0x10
            addresses.add(addr)
            mem.add(rect)

        mem.shift(LEFT*6)
        addresses.shift(LEFT*6)
        self.memory = mem
        self.address = addresses

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
            self.memory.animate.shift(DOWN*3),
            self.address.animate.shift(DOWN*3),
        )

        self.play(
            self.memory[16:22].animate.set_color(PURPLE)
        )

        self.init_code()
        self.asm.shift(UP*2.5+LEFT)

        self.play(
            Transform(self.memory[16].copy(),self.main)
        )
        self.play(
            Transform(self.memory[17].copy(),self.launch)
        )
        self.play(
            Transform(self.memory[18].copy(),self.test)
        )
        self.play(
            Transform(self.memory[19].copy(),self.getbuf)
        )
        self.play(
            Transform(self.memory[20].copy(),self.gets)
        )
        self.play(
            Transform(self.memory[21].copy(),self.io)
        )

        indicator = SurroundingRectangle(self.main.code[2])
        self.play(
            Create(indicator),
            Indicate(self.main.code[2])
        )

        # this just a bunch of shit.
        reg = Text("cs:rip", color=BLUE).scale(0.5).next_to(self.memory[16],UP)
        #rbp = Text("rbp", color=BLUE).scale(0.5).next_to(self.stack[1][0],DOWN)
        #rsp = Text("rsp", color=BLUE).scale(0.5).next_to(self.stack[1][0],DOWN)
        self.play(Create(reg))
        self.wait()
        self.play(reg.animate.next_to(self.memory[17], UP))
        self.shift_code_indicator(3, indicator, self.launch)
        self.wait()
        self.play(reg.animate.next_to(self.memory[18], UP))
        self.shift_code_indicator(3, indicator, self.test)
        self.wait()
        self.play(reg.animate.next_to(self.memory[19], UP))
        self.shift_code_indicator(2, indicator, self.getbuf)
        self.wait()
        self.play(reg.animate.next_to(self.memory[20], UP))
        self.shift_code_indicator(2, indicator, self.gets)
        self.wait()
        self.play(reg.animate.next_to(self.memory[21], UP))
        self.shift_code_indicator(1, indicator, self.io)
        self.wait()

        self.play(reg.animate.next_to(self.memory[20], UP),run_time=0.3)
        self.shift_code_indicator(2, indicator, self.gets)
        self.play(reg.animate.next_to(self.memory[19], UP),run_time=0.3)
        self.shift_code_indicator(2, indicator, self.getbuf, size=1, run_time=0.3)
        self.play(reg.animate.next_to(self.memory[18], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.test, size=1, run_time=0.3)
        self.play(reg.animate.next_to(self.memory[17], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.launch, size=1, run_time=0.3)
        self.play(reg.animate.next_to(self.memory[16], UP),run_time=0.3)
        self.shift_code_indicator(2, indicator, self.main, size=1, run_time=0.3)

        # 返回的时候, 要怎么工作呢?
        # 是时候引入我们的栈空间
        self.play(
            self.memory[29].animate.set_color(RED),
        )

        self.create_stack()
        #kernel_stack = self.stack.copy().shift(UP*2+RIGHT*3).set_color(BLUE)
        self.play(self.stack.next_to(self.memory[29]).animate.shift(UP*4+LEFT*12))

        # 首先在栈底, 是我们的 main function 
        one = Text("0x165").scale(0.5).move_to(self.stack[0][-1])
        self.play(
            self.stack[0][-1].animate.set_color(PURPLE_A),
            Create(one)
        )

        # 然后, main callq launch
        # 紧接着执行指令, sub rsp 会在
        self.play(reg.animate.next_to(self.memory[17], UP))
        self.shift_code_indicator(1, indicator, self.launch)
        self.play(
            self.stack[0][-2].animate.set_color(PURPLE_A)
        )

        self.shift_code_indicator(3, indicator, self.launch)
        two  = Text("0x178").scale(0.5).move_to(self.stack[0][-3])
        self.play(
            self.stack[0][-3].animate.set_color(PURPLE_A),
            Create(two)
        )

        # execute test
        self.play(reg.animate.next_to(self.memory[18], UP))
        self.shift_code_indicator(1, indicator, self.test)
        self.play(
            self.stack[0][-4].animate.set_color(PURPLE_A)
        )
        self.shift_code_indicator(3, indicator, self.test)
        three = Text("0x183").scale(0.5).move_to(self.stack[0][-5])
        self.play(
            self.stack[0][-5].animate.set_color(PURPLE_A),
            Create(three)
        )
        self.wait()

        # execute getbuf
        self.play(reg.animate.next_to(self.memory[19], UP))
        self.shift_code_indicator(1, indicator, self.getbuf)
        self.play(
            self.stack[0][-6].animate.set_color(PURPLE_A)
        )

        self.shift_code_indicator(2, indicator, self.getbuf)
        four = Text("0x191").scale(0.5).move_to(self.stack[0][-7])
        self.play(
            self.stack[0][-7].animate.set_color(PURPLE_A),
            Create(four)
        )
        self.wait()

        # execute gets
        self.play(reg.animate.next_to(self.memory[20], UP))
        self.shift_code_indicator(2, indicator, self.gets)
        five = Text("0x1a3").scale(0.5).move_to(self.stack[0][-8])
        self.play(
            self.stack[0][-8].animate.set_color(PURPLE_A),
            Create(five)
        )
        self.wait()

        # execute IO
        self.play(reg.animate.next_to(self.memory[21], UP))
        self.shift_code_indicator(1, indicator, self.io)

        self.play(self.memory[26].animate.set_color(RED_C))
        self.play(reg.animate.next_to(self.memory[26], UP))

        # trap into kernel space
        self.play(self.memory[5].animate.set_color(RED_C))
        self.play(reg.animate.next_to(self.memory[5], UP))

        # return from kernel space
        self.wait()
        self.play(reg.animate.next_to(self.memory[26], UP),run_time=0.3)
        self.play(reg.animate.next_to(self.memory[21], UP),run_time=0.3)

        # return to gets
        self.play(
            self.stack[0][-8].animate.set_color(RED),
            FadeOut(five)
        )
        self.play(reg.animate.next_to(self.memory[20], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.gets, size=1, run_time=0.3)

        # return to getbuf
        self.play(
            self.stack[0][-7].animate.set_color(RED),
            FadeOut(four)
        )
        self.play(reg.animate.next_to(self.memory[19], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.getbuf, size=1, run_time=0.3)

        # return to test
        self.play(
            self.stack[0][-5].animate.set_color(RED),
            self.stack[0][-6].animate.set_color(RED),
            FadeOut(three)
        )
        self.play(reg.animate.next_to(self.memory[18], UP),run_time=0.3)
        self.shift_code_indicator(4, indicator, self.test, size=1, run_time=0.3)

        # return to launch
        self.play(
            self.stack[0][-3].animate.set_color(RED),
            self.stack[0][-4].animate.set_color(RED),
            FadeOut(two)
        )
        self.play(reg.animate.next_to(self.memory[17], UP),run_time=0.3)
        self.shift_code_indicator(4, indicator, self.launch, size=1, run_time=0.3)

        # return to main
        self.play(
            self.stack[0][-1].animate.set_color(RED),
            self.stack[0][-2].animate.set_color(RED),
            FadeOut(one)
        )
        self.play(reg.animate.next_to(self.memory[16], UP),run_time=0.3)
        self.shift_code_indicator(3, indicator, self.main, size=1, run_time=0.3)

        self.wait()

