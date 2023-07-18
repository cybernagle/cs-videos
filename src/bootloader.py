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

        ax_reg = MArray([0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0]).scale(0.3).shift(LEFT*4)

        self.play(Create(ax_reg))
        ax_reg_2 = ax_reg.copy()
        self.play(ax_reg_2.animate.shift(DOWN))

        xor = Text("xor", font_size = 20).next_to(ax_reg, DOWN, buff=0.25)
        self.play(Create(xor))
        for i in ax_reg:
            i.update_mob_value(mob_value_args={"0":0})

        self.wait()


