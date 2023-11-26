from manim import *

class Trap(Scene):

    memory = None
    cs = None
    gdt = None

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

        self.memory = mem

    def create_cs(self):
        keys = VGroup(*[Rectangle(height=0.5, width=0.5).set_fill(WHITE, opacity=0.2) for i in range(4)]).arrange(RIGHT, buff=0)
        labels = VGroup(*[Text(char).scale(0.5).move_to(keys[i]) for i, char in enumerate("1011")])
        self.cs = VGroup(keys, labels)

    def construct(self):
        reg = Text("cs:rip", color=BLUE)
        # 这是CS和RIP寄存器
        self.add(reg)

        self.create_memory()
        self.memory.shift(LEFT*6)
        self.play(
            reg.animate.next_to(self.memory, UP, buff=1.5),
            Create(self.memory)
        )

        reg.save_state()
        self.wait()
        # 它负责呢保存内存当前执行指令的地址
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
        # 现在咱们的内存有两块区域.
        self.play(
            self.memory[0:15].animate.set_color(BLUE),
            self.memory[15:30].animate.set_color(YELLOW)
        )

        self.wait()
        kernel_addr = Tex(r"$\texttt{0x0}$", font_size = 36).next_to(self.memory[0], UP)
        user_addr = Tex(r"$\texttt{0x123}$", font_size = 36).next_to(self.memory[15], UP)
        # 0-123 是内核代码,123向后是用户代码
        self.play(
            Create(kernel_addr),
            Create(user_addr),
        )

        reg.save_state()
        self.wait()
        # 当 cs rip 指向 123 时,就是用户态执行
        self.play(
            reg.animate.next_to(self.memory[15], DOWN)
        )

        self.wait()
        # 指向 0 时, 就是在内核态执行.
        self.play(
            reg.animate.next_to(self.memory[0], DOWN)
        )
        self.wait()
        self.play(Restore(reg))

        self.create_cs()
        self.cs.move_to(reg)

        self.wait()
        # 那么这种切换是如何工作的呢? 
        value = Tex(r"$\texttt{0xB}$", font_size = 36).move_to(reg)
        # 我们假设 cs 的值是 B
        self.play(ReplacementTransform(reg, value))
        self.wait()
        # 它转换成二进制后, 就是 1011
        self.play(
            ReplacementTransform(value, self.cs)
        )

        # 这里分为两个部分,前两个比特位负责找到代码的地址
        self.play(Indicate(
            self.cs[0][2:]
        ))
        # 后两个比特负责权限.
        self.play(Indicate(
            self.cs[0][:2]
        ))
        self.wait()

        # 前两个比特会在一个叫做gdt 的表格当中,找到其实际的内存位置.
        self.create_gdt()
        self.gdt.scale(0.5).next_to(self.memory[25], UP, buff=0.5)
        self.play(Create(self.gdt))

        # 在我们这里, 前两位是 10, 也就是在我们表格当中2的位置.
        self.play(Indicate(
            self.gdt.get_cell((3,1))
        ))

        self.wait()
        # 所以我们可以得到它指向用户代码段, 也就是 0x123
        self.play(Indicate(
            self.gdt.get_cell((3,0))
        ))

        self.play(
            self.cs.animate.next_to(self.memory[15], DOWN)
        )

        # 而所谓的用户态陷入到内核态,也就是将 cs 的值, 从 10 ,改位00
        labels_final = VGroup(*[Text(char).scale(0.5).move_to(self.cs[0][i]) for i, char in enumerate("00")])
        self.play(
            Transform(self.cs[1][0:2], labels_final)
        )

        self.wait()
        # 从 gdt 当中, 我们也就切换到了 0 的地址
        self.play(
            Indicate(self.gdt.get_cell((1,1)))
        )

        self.wait()
        # 也就是从用户段代码切换到了内核段的代码.
        self.play(
            self.cs.animate.next_to(self.memory[0], DOWN)
        )

        # 别忘记, 还需要将权限位, 从11, 改成00 
        labels_final = VGroup(*[Text(char).scale(0.5).move_to(self.cs[0][i+2]) for i, char in enumerate("00")])
        self.play(
            Transform(self.cs[1][2:], labels_final)
        )
        # 这样,就完成了从用户态切换到内核态.
        self.play(
            Indicate(self.memory[0:15])
        )
        self.wait()
