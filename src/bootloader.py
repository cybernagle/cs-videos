from manim import *
from manim_data_structures import *

class BootLoader(Scene):
    def construct(self):
        bootloader_16_code = """
.code16
    cli
    cld
    xorw %ax, %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %ss
probe_memory:
    movl $0, 0x8000
    xorl %ebx, %ebx
    movw $0x8004, %di
start_probe:
    movl $0xE820, %eax
    movl $20, %ecx
    movl $SMAP, %edx
    int $0x15
    jnc cont
    movw $12345, 0x8000
    jmp finish_probe
cont:
    addw $20, %di
    incl 0x8000
    cmpl $0, %ebx
    jnz start_probe
finish_probe:
    lgdt gdtdesc
    movl %cr0, %eax
    orl $CR0_PE_ON, %eax
    movl %eax, %cr0
    ljmp $PROT_MODE_CSEG, $protcseg
"""
        # boot loader load into mem(at 0x7c00) from disk, then start from 0x7c00
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x7c00
        for i in range(10):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                      grid_xstep=2.0, grid_ystep=0.5)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, DOWN, buff=0)
            addr.next_to(rect, LEFT, buff=0.2)
            mem.add(rect)
            addresses.add(addr)
            start_addr += 8
        mem_group = VGroup(mem, addresses)
        mem_group.shift(UP*2.5)

        # cpu will start execute code at 0x7c00
        self.play(Create(mem_group))
        self.play(FadeOut(mem_group))

        bootloader_16_obj = Code(code=bootloader_16_code,
                    tab_width=4, background="window",
                     language="C").scale(0.5).shift(LEFT*3)

        self.play(Create(bootloader_16_obj))

        ax_reg = MathTable(
            [[0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0]],
            include_outer_lines = True,
            include_background_rectangle= True,
            background_rectangle_color = BLUE,
            fill_opacity=1,
        ).scale(0.25).shift(RIGHT*3+UP)

        ax_txt = Text("ax", font_size = 20).next_to(ax_reg,LEFT)

        self.play(Create(ax_reg), Create(ax_txt))
        ax_reg_2 = ax_reg.copy()
        self.play(ax_reg_2.animate.shift(DOWN))

        xor = Text("xor", font_size = 20).next_to(ax_reg, DOWN, buff=0.3)
        self.play(Create(xor))

        self.play(ax_reg.animate.scale(2).shift(LEFT*2+DOWN*0.5))

        single_zero = MathTex("0", font_size = 25, color=RED)
        for i in ax_reg.get_entries():
            temp = single_zero.copy().move_to(i.get_center())
            self.play(Transform(i, temp), run_time=0.01)

        self.play(ax_reg.animate.shift(RIGHT*2+UP*0.5).scale(0.5))

        ds_reg, es_reg, ss_reg  = ax_reg.copy(), ax_reg.copy(), ax_reg.copy()

        self.play(
            FadeOut(xor),FadeOut(ax_reg_2),
            ds_reg.animate.shift(DOWN*0.5),
            es_reg.animate.shift(DOWN),
            ss_reg.animate.shift(DOWN*1.5),
        )

        ds_txt = Text("ds", font_size = 15).next_to(ds_reg,LEFT)
        es_txt = Text("es", font_size = 15).next_to(es_reg,LEFT)
        ss_txt = Text("ss", font_size = 15).next_to(ss_reg,LEFT)

        self.play(
            Create(ds_txt),
            Create(es_txt),
            Create(ss_txt),
        )

        self.wait()


def generate_mem():
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0fc0
        for i in range(10):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                      grid_xstep=2.0, grid_ystep=0.5)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, DOWN, buff=0)
            addr.next_to(rect, LEFT, buff=0.2)
            mem.add(rect)
            addresses.add(addr)
            start_addr += 8
        mem_group = VGroup(mem, addresses)
        mem_group.shift(RIGHT*3+UP*2.5)


