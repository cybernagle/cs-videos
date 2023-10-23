from manim import *
import random

# https://github.com/mit-pdos/xv6-public/blob/eeb7b415dbcb12cc362d0783e41c3d1f44066b17/proc.h#L35

class Process(Scene):
    memory = None
    cpu = None
    code = None
    page_table = None

    def proc(self):
        self.code = Code(
            file_name="./process.c",
            tab_width=4, language="C", style="solarized-dark").scale(0.5)

    def create_virtual_memory(self, length=30,width=1.5, height=0.5, color=YELLOW) -> VGroup:
        mem = VGroup()
        width = width
        height = height
        for i in range(length):
            buff = 0
            rect = Rectangle(color=color, fill_opacity=0.5, width=width, height=height,
                             grid_xstep=width, grid_ystep=height)
            rect.next_to(mem, RIGHT, buff=buff)
            mem.add(rect)

        mem.move_to(ORIGIN)
        return mem

    def construct(self):

        elfhdr = self.create_virtual_memory(length=2, color=GREEN)
        text = self.create_virtual_memory(length=3, color=YELLOW)
        stack = self.create_virtual_memory(length=1, color=RED)

        elfhdr.shift(LEFT*5)
        text.next_to(elfhdr, RIGHT)
        stack.next_to(text, RIGHT)

        elfhdr_desc = Text("elfheader").scale(0.5).next_to(elfhdr[0], DOWN)
        text_desc = Text(".text").scale(0.5).next_to(text[0], DOWN)
        stack_desc = Text("stack").scale(0.5).next_to(stack[0], DOWN)

        virtual_memory = VGroup(
            elfhdr, text, stack,
            elfhdr_desc, text_desc, stack_desc
        )
        virtual_memory.move_to(ORIGIN)

        # 这是我们的一个程序.其中的代码存放在 .text 段当中.
        self.add(
            virtual_memory
        )

        self.wait()

        self.play(
            virtual_memory.animate.shift(UP*3)
        )

        code = self.create_virtual_memory(length=13,height=0.5, width=0.5, color=YELLOW).align_to(text,LEFT)
        temp = text.copy()
        # 程序被执行后, 在内存当中就变成了进程.
        self.play(
            temp.animate.become(code, copy_submobjects=False)
        )

        self.wait()

        # 表达一下
        # enum procstate { UNUSED, EMBRYO, SLEEPING, RUNNABLE, RUNNING, ZOMBIE };
        
        # 我们的 cpu 会执行 cs ip 所指向的指令.
        reg = Text("cs:ip", color=BLUE).scale(0.5).next_to(temp[0], DOWN)
        reg_pointer = Arrow(start=reg.get_edge_center(UP), end=temp[0].get_edge_center(DOWN))
        reg_group = VGroup(reg, reg_pointer)

        run_state = Text("RUNNING").scale(0.4).next_to(temp, LEFT,buff=0.1)
        self.play(reg_group.animate.shift(RIGHT*1), run_time=1)

        # 当 CPU 在执行该程序的指令的时候,它就进入了 RUNNING 的状态.
        # 程序不断的向前执行, 遇到循环等分支,会重复执行部分代码.
        steps = [3, 2]
        for i in range(len(steps)):
            n = steps[i]
            reg_group.save_state()
            self.play(reg_group.animate.shift(RIGHT*n), run_time=n/2)
            self.play(Restore(reg_group))
        self.play(FadeIn(run_state))

        temp2 = temp.copy()
        self.play(
            temp2.animate.shift(DOWN*2)
        )

        reg_group.save_state()
        # 进程之间也会发生切换的情况.
        self.play(reg_group.animate.next_to(temp2[0], DOWN))
        self.play(reg_group.animate.shift(RIGHT*4), run_time=1)
        self.wait()

        self.play(Wiggle(temp))
        # runnable
        # 在我们的实例当中,进程切换到另外一个进程后, 原有进程的状态就变成了 RUNNABLE
        runnable_state = Text("RUNABLE").scale(0.4).move_to(run_state)
        self.play(run_state.animate.become(runnable_state))

        # process regs: cs, ip, eip
        # 接下来, 如果需要将进程切换回来,我们需要做哪些事情?
        self.proc()
        self.code.align_on_border(LEFT).shift(DOWN*0.2)
        # 我们看一下  xv6 的实现.
        self.play(Write(self.code.background_mobject))
        # 进程状态被枚举为 procstate
        self.play(
            FadeIn(self.code.code[0:8]),
        )
        self.wait()
        # 进程本身, 由 proc 这个结构来进行管理
        self.play(
            FadeIn(self.code.code[15:17]),
            FadeIn(self.code.code[28]),
        )

        # 首先我们将进程切换回来, 首先需要知道我们切换的是谁, 于是我们需要进程的 ID
        # 这里, 我们假设原进程是0 , 
        p1 = Text("0", color=GREEN).scale(0.5).next_to(temp, DOWN)
        p2 = Text("1", color=GREEN).scale(0.5).next_to(temp2, DOWN)
        self.play(
            Create(p1),
        )

        self.wait(0.5)
        #切换后的进程是 1
        self.play(
            Create(p2),
        )
        # 在proc这个结构当中, 用 pid 来表示. sz 则代表的是 process 的大小.
        self.play(
            FadeIn(self.code.code[17:19]),
        )
        self.play(
            Indicate(self.code.code[17:19]),
        )

        self.page_table = Table(
            [["0", ""],
             ["1", ""],
             ["2", ""],
             ["3", ""],
             ["4", ""]],
            col_labels=[Text("VPN"), Text("PFN")],
            include_outer_lines=True
        ).set_column_colors(YELLOW).scale(0.3).align_on_border(RIGHT)

        p2_page_table = self.page_table.copy().set_column_colors(YELLOW_B).next_to(self.page_table, DOWN)

        # 而进程0和进程1都有自己的页表.
        # 我们需要从页表1切换到页表0, 这个被结构体当中的 pgdir 管理.
        self.play(FadeIn(self.page_table))
        self.play(FadeIn(p2_page_table))
        self.play(FadeIn(self.code.code[19]))
        self.play(Indicate(self.code.code[19]))

        # context
        # 接下来, 进程在切换过程当中,有一些上下文环境,比如说当前指令位置ip寄存器.
        self.wait()
        self.play(Indicate(reg))
        # 栈的地址, sp 
        self.play(Indicate(stack))
        # 这个信息会存储在 context 这个结构当中.
        self.play(
            FadeIn(self.code.code[8:15]),
        )

        i = 20
        self.play(
            FadeIn(self.code.code[i]),
        )
        self.play(
            Indicate(self.code.code[i]),
            Indicate(self.code.code[8:15]),
        )
        # trapframe: 还有中断信息,在进程被被切换一般都是会发生系统调用从而陷入内核态,并且发生切换.具体的系统调用如何分发,
        #            以及分发后的上下文切换.
        #            这个,就需要 trapfram 来进行管理.
        # 细节可以看中断一章.
        i+=1
        self.play(
            FadeIn(self.code.code[i]), # 20
        )
        self.play(
            Indicate(self.code.code[i]), # 20
        )

        # kstack
        # 而在切换到内核态以后,内核本身也需要对该进程的内核态上下文保存, 所以我们需要一个栈, 也就是 kstack 来保存其上下文信息.
        # 问题: kstack 是在用户空间还是在内核空间?
        i+=1
        self.play(
            FadeIn(self.code.code[i]), # 21
        )
        self.play(
            Indicate(self.code.code[i]), # 21
        )

        # 当然了, 我们程序的文件地址也需要被修改, 它们被 inode, 和 cwd, cwd也就是当前文件路径两个字段来进行管理.
        i+=1
        self.play(
            FadeIn(self.code.code[i:25]),
        )
        self.play(
            Indicate(self.code.code[i:25])
        )

        # 最后还有进程管理链表本身需要的: 父进程,是否被杀死等等辅助信息.
        self.play(
            FadeIn(self.code.code[25:28]),
        )
        self.play(
            Indicate(self.code.code[25:28])
        )
        self.wait()

        # 这样,我们就完成了从进程1回到进程0的切换, 于是进程 0 变成了 running 的状态.
        self.play(Restore(reg_group))
        runagain_state = Text("RUNNING").scale(0.4).move_to(run_state)
        self.play(run_state.animate.become(runagain_state))

        self.wait()
