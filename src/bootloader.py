from manim import *
from manim_data_structures import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class BootLoader(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService())
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
        with self.voiceover(text="这是一块内存区域") as tracker:
            self.play(Create(mem_group))
        bootloader_16_obj = Code(code=bootloader_16_code,
                    tab_width=4, background="window",
                     language="C").shift(LEFT*10)

        # 系统将启动代码放在了 0x7c00 的区域
        with self.voiceover(text="操作系统的启动代码会放在 0x7c00 开始的区域") as tracker:
            self.play(bootloader_16_obj.animate.scale(0.1).move_to(mem_group[1][1].get_center()))

        self.play(FadeOut(mem_group))

        with self.voiceover(text="接下来让我们详细看一下启动代码") as tracker:
            self.play(bootloader_16_obj.animate.scale(6).shift(DOWN*2+LEFT*2))

        self.play(FadeOut(bootloader_16_obj.code))


        self.play(FadeIn(bootloader_16_obj.code[0:4]))

        ax_reg = MathTable(
            [[0,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0]],
            include_outer_lines = True,
            include_background_rectangle= True,
            background_rectangle_color = BLUE,
            fill_opacity=1,
        ).scale(0.25).shift(RIGHT*3+UP)

        ax_reg_2 = ax_reg.copy()
        ax_txt = Text("ax", font_size = 20).next_to(ax_reg,LEFT)

        with self.voiceover(text="首先,代码用<bookmark mark='A'/>xor命令,<bookmark mark='B'/>将ax等寄存器值置为0") as tracker:
            self.play(Create(ax_reg), Create(ax_txt))
            self.play(ax_reg_2.animate.shift(DOWN))

            self.wait_until_bookmark("A")

            xor = bootloader_16_obj.code[3][4:8].copy()
            self.play(xor.animate.next_to(ax_reg, DOWN, buff=0.3))

            self.wait_until_bookmark("B")
            self.play(FadeOut(xor))

            self.play(ax_reg.animate.scale(2).shift(LEFT*2+DOWN*0.5))
            single_zero = MathTex("0", font_size = 25, color=RED)
            for i in ax_reg.get_entries():
                temp = single_zero.copy().move_to(i.get_center())
                self.play(Transform(i, temp), run_time=0.01)

            self.play(ax_reg.animate.shift(RIGHT*2+UP*0.5).scale(0.5))


        ds_reg, es_reg, ss_reg  = ax_reg.copy(), ax_reg.copy(), ax_reg.copy()
        with self.voiceover(text="随后的代码,将ax的值,用于初始化<bookmark mark='A'/>ds,es,ss等寄存器") as tracker:
            self.play(FadeIn(bootloader_16_obj.code[4:7]))

            self.wait_until_bookmark("A")
            self.play(
                FadeOut(xor),FadeOut(ax_reg_2),
                ds_reg.animate.shift(DOWN*0.5),
                es_reg.animate.shift(DOWN),
                ss_reg.animate.shift(DOWN*1.5)
            )

            ds_txt = Text("ds", font_size = 20).next_to(ds_reg,LEFT)
            es_txt = Text("es", font_size = 20).next_to(es_reg,LEFT)
            ss_txt = Text("ss", font_size = 20).next_to(ss_reg,LEFT)
            self.play(
                Create(ds_txt),
                Create(es_txt),
                Create(ss_txt)
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

        mem_start_addr = 0x8004
        mem_addresses = VGroup()

        for i in reversed(range(10)):
            addr = Text(hex(mem_start_addr), font_size = 15)
            addr.next_to(mem[i], LEFT, buff=0.2)
            mem_addresses.add(addr)
            mem_start_addr += 0x20

        whole_mem_group = VGroup()
        whole_mem_group.add(whole_mem, mem_addresses)

        with self.voiceover(text="紧接着,因为内存的大小不尽相同,所以启动代码需要探测内存的大小") as tracker:
            self.play(FadeIn(bootloader_16_obj.code[7:16]))
            self.play(whole_mem_group.animate.shift(RIGHT*4))

        # 
        bs = bootloader_16_obj.code[13][10:12].copy().scale(2)
        b = Brace(whole_mem, DOWN)
        with self.voiceover(text="要做到这一点,<bookmark mark='A'/>在经过一系列的初始化后,我们首先提供给调用 int 15 中断以<bookmark mark='B'/>必要的参数,比如说,我们一次检测的需要内容是<bookmark mark='C'/>20,然后,我们<bookmark mark='D'/>用int15中断来探测内存是否存在") as tracker:
            self.wait_until_bookmark("A")
            self.play(Indicate(bootloader_16_obj.code[8:11]))
            self.wait_until_bookmark("B")
            self.play(Indicate(bootloader_16_obj.code[12:15]))

            # 比如说, 我们一次检测的需要内容是 20
            self.wait_until_bookmark("C")
            self.play(Create(b), bs.animate.next_to(b, DOWN))


            self.wait_until_bookmark("C")
            self.play(Indicate(bootloader_16_obj.code[15]),Indicate(whole_mem[-1]))
            self.play(whole_mem[-1].animate.set_fill(YELLOW))


        self.play(FadeOut(b), FadeOut(bs))

        self.play(FadeIn(bootloader_16_obj.code[16:24]))
        init_value = 0
        size = Tex("$8000-8004: {}$".format(init_value),
                    font_size=25).next_to(whole_mem, DOWN)
        with self.voiceover(text="紧接着,我们通过<bookmark mark='A'/>jump指令进入循环,并将放在 <bookmark mark='B'/>0x8000 的位置上的变量进行自增,直到探测所有的的内存") as tracker:

            self.wait_until_bookmark('A')
            self.play(
                ApplyWave(bootloader_16_obj.code[11]),
                ApplyWave(bootloader_16_obj.code[23]),
            )

            self.wait_until_bookmark('B')
            for i in reversed(range(9)):
                tmp_size_str = "$8000-8004: {}$".format(init_value)
                tmp_size = Tex(tmp_size_str, font_size=25).next_to(whole_mem, DOWN)
                init_value += 1
                self.play(Indicate(whole_mem[i], run_time=0.5), Transform(size, tmp_size, run_time=0.5))

            self.play(whole_mem[:9].animate.set_fill(YELLOW))

            e820struct = Tex("$e820map.nr\_map$", font_size=30, color=RED)
        with self.voiceover(text="最后,我们将这个值,存放在了<bookmark mark='A'/>e820map的nr_map这个变量当中.在后期的内存管理中备用.") as tracker:
            self.play(size.animate.next_to(bootloader_16_obj, RIGHT, buff=0.5))
            self.wait_until_bookmark("A")
            self.play(e820struct.animate.next_to(size, UP))

