from manim import *

class VonNeomann(Scene):
    memory = None
    cpu = None
    def create_memory(self):
        mem = VGroup()
        for i in range(5):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                             grid_xstep=2, grid_ystep=0.5)
            rect.next_to(mem, DOWN, buff=0)
            mem.add(rect)
        mem.move_to(ORIGIN)
        self.memory = mem

    def init_cpu(self):
        self.cpu = VGroup(
            *[Square(side_length=0.8, fill_opacity=0.5).set_color(BLUE) for _ in range(9)]
        )
        self.cpu.arrange_in_grid(3,3,buff=0)


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
        self.play(self.cpu.animate.shift(RIGHT*3))
        self.wait()

        # 内存当中的指令,首先会被取到 cpu 当中.
        # 然后二进制的内容会被译码,二进制对应的指令开始具有语义(将二进制向右移动,转换成汇编指令)

        #1010111111110000 -> mov ax, 0AFFh
        #1010111000001111 -> mov bx, 0AEFh
        #1110101011111111 -> mov cx, 0EBFFh
        #1010100011111111 -> mov dx, 0A3FFh
        #0000001101100000 -> mov si, 03B0h

        asm = [
            "mov ax, 0AFFh",
            "mov bx, 0AEFh",
            "mov cx, 0EBFFh",
            "mov dx, 0A3FFh",
            "mov si, 03B0h"
        ]
        for i in range(len(asm)):
            self.play(
                binarys[i].animate.shift(RIGHT*5)
            )
            a = Text(asm[i]).scale(0.3).move_to(binarys[i])
            self.play(Transform(binarys[i], a), run_time=1)

        # try to do operation
        self.play(self.cpu.animate.arrange_in_grid(3,3,0.5))
        
        self.wait()
