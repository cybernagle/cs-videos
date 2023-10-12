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

        self.init_cpu()
        # 这是我们的 CPU
        self.add(self.cpu)
        self.play(self.cpu.animate.shift(RIGHT*4.5))
        self.wait()

        # 内存当中的指令,首先会被取到 cpu 当中.
        # 然后二进制的内容会被译码,二进制对应的指令开始具有语义(将二进制向右移动,转换成汇编指令)

        #1111111111100000 -> jmpq *%rax
        asm = [
            "mov ax, 0AFFh",
            "mov bx, 0AEFh",
            "mov cx, 0EBFFh",
            "mov dx, 0A3FFh",
            "mov si, 03B0h"
        ]

        # try to do operation
        self.play(self.cpu.animate.arrange_in_grid(2,2,0.5))
        registers = ["ax", "bs", "ss","sp"]
        reg_group = VGroup()
        for i in range(len(registers)):
            t = Text(registers[i], color=WHITE).scale(0.5).next_to(self.cpu[i], DOWN, buff=0.15)
            reg_group.add(t)
        self.play(
            FadeIn(reg_group)
        )

        process = Text("取指令", color=YELLOW).shift(UP*2.5)
        self.add(process)

        #self.play(
        #    binarys[0].animate.shift(RIGHT*5)
        #)
        #asm_line = Text(asm[0]).scale(0.3).move_to(binarys[0])
        #self.play(Transform(binarys[0], asm_line), run_time=1)
        self.shift_asm(binarys, 0)

        self.play(
            process.animate.become(Text("指令译码", color=YELLOW).shift(UP*2.5))
        )
        self.decode(binarys,asm,0)

        self.play(
            process.animate.become(Text("执行指令", color=YELLOW).shift(UP*2.5))
        )
        self.play(self.memory[6].animate.set_color(RED_A))
        self.play(Text("keyboard").scale(0.5).animate.move_to(self.memory[6]))

        self.play(
            process.animate.become(Text("访存取数", color=YELLOW).shift(UP*2.5))
        )

        numbers = Text("0").scale(0.5).move_to(self.memory[6])
        self.play(numbers.animate.next_to(self.memory[6],RIGHT))

        self.play(
            process.animate.become(Text("结果写回", color=YELLOW).shift(UP*2.5))
        )
        self.play(
            numbers.animate.move_to(self.cpu[0])
        )

        self.play(FadeOut(process))

        #for i in range(len(asm)):
        #    self.play(
        #        binarys[i].animate.shift(RIGHT*5)
        #    )
        #    a = Text(asm[i]).scale(0.3).move_to(binarys[i])
        #    self.play(Transform(binarys[i], a), run_time=1)

        self.wait()
