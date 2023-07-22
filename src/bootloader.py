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
    do_something_inappropriate
    jmp finish_probe
cont:
    addw $20, %di
    incl 0x8000
    cmpl $0, %ebx
    jnz start_probe
"""
        finish_probe = """
finish_probe:
    lgdt gdtdesc
    movl %cr0, %eax
    orl $CR0_PE_ON, %eax
    movl %eax, %cr0
    ljmp $PROT_MODE_CSEG, $protcseg
"""
        gdt = """
gdt:
    SEG_NULLASM
    SEG_ASM(STA_X|STA_R, 0x0, 0xffffffff)
    SEG_ASM(STA_W, 0x0, 0xffffffff)
gdtdesc
    .word 0x17
    .long gdt
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
        bootloader_16_obj = Code(code=bootloader_16_code,
                    tab_width=4, background="window",
                     language="C").shift(LEFT*10)

        self.play(bootloader_16_obj.animate.scale(0.1).move_to(mem_group[1][1].get_center()))

        self.play(FadeOut(mem_group))

        self.play(bootloader_16_obj.animate.scale(6).shift(DOWN*2+LEFT*2))

        self.play(FadeOut(bootloader_16_obj.code))

        self.play(FadeIn(bootloader_16_obj.code[0:7]))

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

        ds_txt = Text("ds", font_size = 20).next_to(ds_reg,LEFT)
        es_txt = Text("es", font_size = 20).next_to(es_reg,LEFT)
        ss_txt = Text("ss", font_size = 20).next_to(ss_reg,LEFT)

        self.play(
            Create(ds_txt),
            Create(es_txt),
            Create(ss_txt),
        )

        reg_group = VGroup()
        reg_group.add(
            ds_reg, es_reg, ss_reg, ax_reg,
            ax_txt, ds_txt, es_txt, ss_txt
        )

        self.play(FadeOut(reg_group))
        # start probe memory
        # why 0x8000 , because ucore only manage memory start with 0x8000.
        # it's defined by a structure called e820map
        whole_mem = mem.copy()

        mem_start_addr = 0x0
        mem_addresses = VGroup()

        for i in reversed(range(10)):
            addr = Text(hex(mem_start_addr), font_size = 15)
            addr.next_to(mem[i], LEFT, buff=0.2)
            mem_addresses.add(addr)
            mem_start_addr += 0x20

        whole_mem_group = VGroup()
        whole_mem_group.add(whole_mem, mem_addresses)

        self.play(FadeIn(bootloader_16_obj.code[7:16]))
        self.play(whole_mem_group.animate.shift(RIGHT*3))

        # but from start, Operating system do not know how big your memory is.
        # thus , we need to probe your size of memory.
        self.play(Indicate(bootloader_16_obj.code[15]))
        self.play(Indicate(whole_mem[-2]))
        self.play(whole_mem[-2].animate.set_fill(YELLOW))

        self.play(FadeIn(bootloader_16_obj.code[16:24]))

        self.play(
            ApplyWave(bootloader_16_obj.code[11]),
            ApplyWave(bootloader_16_obj.code[23]),
        )

        for i in reversed(range(8)):
            self.play(Indicate(whole_mem[i], run_time=0.1))
            self.play()
        self.play(whole_mem[:8].animate.set_fill(YELLOW))

        self.wait()
