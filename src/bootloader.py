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

    lgdt gdtdesc
    movl %cr0, %eax
    orl $CR0_PE_ON, %eax
    movl %eax, %cr0

    ljmp $PROT_MODE_CSEG, $protcseg
        """
        bootloader_32_code = """
.code32
protcseg:
    # $PROT_MODE_DESG = 0x10
    movw $PROT_MODE_DSEG, %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %fs
    movw %ax, %gs
    movw %ax, %ss

    movl $0x0, %ebp
    movl $start, %esp
    call bootmain
spin:
    jmp spin

# Bootstrap GDT
.p2align 2                                          # force 4 byte alignment
gdt:
    SEG_NULLASM                                     # null seg
    SEG_ASM(STA_X|STA_R, 0x0, 0xffffffff)           # code seg for bootloader and kernel
    SEG_ASM(STA_W, 0x0, 0xffffffff)                 # data seg for bootloader and kernel

gdtdesc:
    .word 0x17                                      # sizeof(gdt) - 1
    .long gdt                                       # address gdt
"""
        bootloader_16_obj = Code(code=bootloader_16_code,
                    tab_width=4, background="window",
                     language="C").scale(0.5).shift(LEFT*3)

        bootloader_32_obj = Code(code=bootloader_32_code,
                    tab_width=4, background="window",
                     language="C").scale(0.5)
        self.play(Create(bootloader_16_obj))

        ax_reg = MathTable(
            [[0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0]],
            include_outer_lines = True,
            include_background_rectangle= True,
            background_rectangle_color = BLUE,
            fill_opacity=1,
        ).scale(0.25).shift(RIGHT*3+UP)

        #ax_reg = MArray([0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0]).scale(0.3).shift(LEFT*4)
        ax_txt = Text("ax", font_size = 15).next_to(ax_reg,LEFT)

        self.play(Create(ax_reg), Create(ax_txt))
        ax_reg_2 = ax_reg.copy()
        self.play(ax_reg_2.animate.shift(DOWN))

        xor = Text("xor", font_size = 20).next_to(ax_reg, DOWN, buff=0.3)
        self.play(Create(xor))

        self.play(ax_reg.animate.scale(2).shift(LEFT*2+DOWN*0.5))

        #for i in range(len(ax_reg.get_rows[0].get_entries())):
        #    print(i)

        for i in ax_reg.get_entries():
            self.play(Write(i,"0"))


        #self.play(Write(ax_reg))
        self.play(ax_reg.animate.shift(RIGHT*2+UP*0.5).scale(0.5))

        #ds_reg, es_reg, ss_reg  = ax_reg.copy(), ax_reg.copy(), ax_reg.copy()

        #self.play(
        #    FadeOut(xor),FadeOut(ax_reg_2),
        #    ds_reg.animate.shift(DOWN*0.5),
        #    es_reg.animate.shift(DOWN),
        #    ss_reg.animate.shift(DOWN*1.5),
        #)

        #ds_txt = Text("ds", font_size = 15).next_to(ds_reg,LEFT)
        #es_txt = Text("es", font_size = 15).next_to(es_reg,LEFT)
        #ss_txt = Text("ss", font_size = 15).next_to(ss_reg,LEFT)

        #self.play(
        #    Create(ds_txt),
        #    Create(es_txt),
        #    Create(ss_txt),
        #)

        self.wait()


