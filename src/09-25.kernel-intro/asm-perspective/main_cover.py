from manim import *

class VonNeomannCover(Scene):
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

        self.memory.shift(LEFT*5),
        binarys.shift(LEFT*5)
        self.add(self.memory)
        self.add(binarys)

        addr = ['0x1', '0x2', '0x3', '0x4', '0x5']
        addr_group = VGroup()
        for a in range(len(addr)):
            addr_group.add(Text(addr[a]).scale(0.3).next_to(self.memory[a], LEFT))

        self.add(addr_group)

        self.init_cpu()
        self.cpu.shift(RIGHT*4.5)
        self.cpu.arrange_in_grid(2,2,0.5)
        self.add(self.cpu)

        registers = ["ax", "bs", "ss","sp"]
        reg_group = VGroup()
        for i in range(len(registers)):
            t = Text(registers[i], color=WHITE).scale(0.5).next_to(self.cpu[i], DOWN, buff=0.15)
            reg_group.add(t)
        self.add(reg_group)

        a = Text("一个CPU指令", color=RED_B).shift(UP*0.5).scale(1.8).shift(LEFT*0.25)
        self.add(a)
        self.add(Text("的生命周期", color=RED_B).next_to(a, DOWN))

