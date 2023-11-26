from manim import *

class VonNeomann(Scene):
    memory = None
    cpu = None
    def create_memory(self):
        mem = VGroup()
        for i in range(8):
            color = BLUE
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                             grid_xstep=2, grid_ystep=0.5)
            rect.next_to(mem, DOWN, buff=0)
            mem.add(rect)
        mem.move_to(ORIGIN)
        self.memory = mem

    def init_cpu(self):
        self.cpu = VGroup(
            *[Square(side_length=0.8, fill_opacity=0.5).set_color(BLUE) for _ in range(4)]
        )
        self.cpu.arrange_in_grid(2,2,buff=0)

    def shift_asm(self,obj, index):
        binarys = obj
        self.play(
            binarys[index].animate.shift(RIGHT*5)
        )

    def decode(self,obj, target, index):
        binarys = obj
        asm = target
        asm_line = Text(asm[index]).scale(0.3).move_to(binarys[index])
        self.play(Transform(binarys[index], asm_line), run_time=1)

    def construct(self):
        # 这是一小块在代码段的内存
        self.create_memory()

        binary = [
            "1010111111110000",
            "1010111000001111",
            "1110101011111111",
            "1010100011111111",
            "0000001101100000",
        ]
        binarys = VGroup()
        for i in range(len(binary)):
            t = Text(binary[i]).scale(0.3).move_to(self.memory[i])
            binarys.add(t)

        # 它存放了一堆二进制数据
        self.add(self.memory)
        self.wait()
        self.add(binarys)
        self.wait()

        self.play(
            self.memory.animate.shift(LEFT*5),
            binarys.animate.shift(LEFT*5)
        )
        self.wait()

        addr = ['0x1', '0x2', '0x3', '0x4', '0x5']
        addr_group = VGroup()
        for a in range(len(addr)):
            addr_group.add(Text(addr[a]).scale(0.3).next_to(self.memory[a], LEFT))

        self.add(addr_group)

        self.init_cpu()
        # 这是我们的 CPU
        self.add(self.cpu)
        self.play(self.cpu.animate.shift(RIGHT*4.5))
        self.wait()


        asm = [
            "mov 0xKEYBOARD, ax",
            "INC ax",
            "mov ax, 0xMONITOR",
            "jmp 0x1",
        ]

        # cpu 上面会有很多的速度很快的寄存器
        self.play(self.cpu.animate.arrange_in_grid(2,2,0.5))
        registers = ["ax", "bs", "ss","sp"]
        reg_group = VGroup()
        for i in range(len(registers)):
            t = Text(registers[i], color=WHITE).scale(0.5).next_to(self.cpu[i], DOWN, buff=0.15)
            reg_group.add(t)
        self.play(
            FadeIn(reg_group)
        )

        # 首先指令将从内存中取出来.
        process = Text("取指令", color=YELLOW).shift(UP*2.5)
        self.add(process)

        self.shift_asm(binarys, 0)

        self.wait()

        self.play(
            process.animate.become(Text("译码", color=YELLOW).scale(0.8).shift(UP*2.5))
        )
        # 取出来之后, 一堆二进制将会被译码, CPU 就知道要执行什么任务
        self.decode(binarys,asm,0)

        self.wait()
        # 接下来,通过地址计算,我们知道指令要操作的地址是什么
        self.play(
            process.animate.become(Text("地址计算", color=YELLOW).scale(0.8).shift(UP*2.5))
        )
        self.wait()
        self.play(self.memory[6].animate.set_color(RED_A))
        keyboard = Text("keyboard").scale(0.5).move_to(self.memory[6])
        self.play(FadeIn(keyboard))
        self.wait()

        # 然后去到相应的地址拿到数据
        self.play(
            process.animate.become(Text("访存取数", color=YELLOW).scale(0.8).shift(UP*2.5))
        )
        self.wait()

        numbers = Text("0").scale(0.5).move_to(self.memory[6])
        self.play(numbers.animate.next_to(self.memory[6],RIGHT))
        self.wait()

        # 如果有计算的任务,比如说自增,那么将执行计算,这里我们只是搬迁,所以不涉及到计算
        self.play(
            process.animate.become(Text("执行", color=YELLOW).scale(0.8).shift(UP*2.5))
        )
        self.wait()

        # 最后将结果存放起来.
        self.play(
            process.animate.become(Text("存放结果", color=YELLOW).scale(0.8).shift(UP*2.5))
        )
        self.wait()
        self.play(
            numbers.animate.move_to(self.cpu[0])
        )
        self.wait()

        self.play(FadeOut(process))


        # 我们所看到的这一系列操作, 被称之为一个指令周期. 每一个简单的指令,都会经过这个周期.
        # 接下来,计算机重复上面的过程, 紧接着取后面一条指令
        self.shift_asm(binarys, 1)
        self.decode(binarys, asm, 1)
        # INC 1 的意思是, 将该存储位置的数据,自增1
        self.play(numbers.animate.become(Text("1").scale(0.5).move_to(self.cpu[0])))

        self.wait()
        # 紧接着我们执行又一个指令周期将内容搬运到显示器缓冲区.
        self.shift_asm(binarys, 2)
        self.decode(binarys, asm, 2)
        self.play(self.memory[7].animate.set_color(RED_B))
        monitor = Text("monitor").scale(0.5).move_to(self.memory[7])
        self.play(FadeIn(monitor))
        self.play(numbers.animate.next_to(self.memory[7], RIGHT))
        self.wait()

        # 继续执行
        # 这个时候, 本来应该按照顺序执行下一条指令.
        # 但是我们这个指令本身修改了指令的执行顺序.
        # 也就是 jmp 指令, 回到 0x1 的地址重新开始执行上面的数据搬迁的操作.
        # 从而构成了一个循环.
        self.shift_asm(binarys, 3)
        self.decode(binarys, asm, 3)
        self.wait()

        self.remove(binarys[4])
        self.play(
            FadeOut(self.memory),
            FadeOut(self.cpu),
            FadeOut(keyboard),
            FadeOut(monitor),
            FadeOut(reg_group),
            FadeOut(numbers),
            FadeOut(addr_group)
        )

        # 重点看一下我们目前的指令, 它几乎包含了所有目前我们会用到的指令类型:

        move_cmd = Text("数据搬迁指令", color=RED).shift(UP*2.5+LEFT*4).scale(0.6)
        calc_cmd = Text("运算指令",color=RED).shift(UP*2.5).scale(0.6)
        ctrl_cmd = Text("控制指令", color=RED).shift(UP*2.5+RIGHT*4).scale(0.6)

        # 数据搬迁指令
        self.play(FadeIn(move_cmd))
        self.play(
            binarys[0].animate.next_to(move_cmd, DOWN*4),
            binarys[2].animate.next_to(move_cmd, DOWN*5)
        )
        self.wait()

        # 控制指令
        self.play(FadeIn(ctrl_cmd))
        self.play(
            binarys[3].animate.next_to(ctrl_cmd, DOWN*4),
        )
        self.wait()

        # 运算指令
        self.play(FadeIn(calc_cmd))
        vonNeomann = ["存储", "IO", "运算", "控制"]

        v_group = VGroup()
        for i in range(len(vonNeomann)):
            v_group.add(Text(vonNeomann[i], color=GREEN).scale(0.5))

        # 而这些指令与冯诺伊曼又形成了对应关系
        v_group[0:2].arrange().next_to(move_cmd, DOWN*10)
        # 数据搬迁指令,对应存储与 IO
        self.play(FadeIn(v_group[0:2]))

        v_group[2].next_to(calc_cmd, DOWN*10)

        # 运算指令, 执行运算
        self.play(FadeIn(v_group[2]))

        v_group[3].next_to(ctrl_cmd, DOWN*10)
        # 运算指令,  控制指令流
        self.play(FadeIn(v_group[3]))

        self.wait()
