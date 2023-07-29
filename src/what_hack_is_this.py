from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class WhatHackIsThisCode(VoiceoverScene):
    def construct(self):
        code = """
#define SEG_ASM(type,base,lim)                                  \\
    .word (((lim) >> 12) & 0xffff), ((base) & 0xffff);          \\
    .byte (((base) >> 16) & 0xff), (0x90 | (type)),             \\
        (0xC0 | (((lim) >> 28) & 0xf)), (((base) >> 24) & 0xff)
"""


        self.set_speech_service(RecorderService())
        """
        这段代码是一个宏定义，用于生成一条特定格式的x86汇编指令。让我来解释一下每个部分的含义：
        SEG_ASM(type, base, lim): 这是一个宏定义，定义了一个带有三个参数的宏。
            在使用时，需要提供类型（type）、基地址（base）和限制（lim）。
        .word (((lim) >> 12) & 0xffff), ((base) & 0xffff): 这一行使用 .word 指令将两个16位的值写入到内存中。
        """
        code_obj = Code(code=code,
                        tab_width=4, language="C", style="solarized-dark")

        word = code_obj.code[1][4:9]
        byte = code_obj.code[2][4:9]

        word_lim = code_obj.code[1][12:33].copy()
        word_base = code_obj.code[1][37:52].copy()

        byte_lim = code_obj.code[2][12:32].copy()
        byte_type = code_obj.code[2][36:49].copy()
        byte_third = code_obj.code[3][9:37].copy()
        byte_fourth = code_obj.code[3][41:62].copy()

        with self.voiceover(text="这行代码在做什么事情?<bookmark mark='A'/>首先.word将两个16位的值写入内存.<bookmark mark='B'/>.byte将4个8位的值写入到内存") as tracker:
            self.add(code_obj)
            self.wait_until_bookmark("A")
            self.play(Indicate(word, run_time=1))
            self.wait_until_bookmark("B")
            self.play(Indicate(byte, run_time=1))

        word_group = VGroup()
        word_group.add(word_lim, word_base)

        byte_group = VGroup()
        byte_group.add(
            byte_lim, byte_type,
            byte_third, byte_fourth
        )

        t = "$type = \mathtt{0x10}$"
        base = "$base = \mathtt{0x0}$"
        lim = "$lim = \mathtt{0xffffffff}$"
        with self.voiceover(text="接下来我们分别来看看他们各自要写的<bookmark mark='A'/>内容,以及他们需要的<bookmark mark='B'/>三个参数,<bookmark mark='C'/>limit,<bookmark mark='D'/>base,以及<bookmark mark='E'/>type") as tracker:
            self.wait_until_bookmark("A")
            self.play(
                FadeOut(code_obj),
                word_group.animate.arrange(DOWN,aligned_edge=LEFT).shift(LEFT*4.7+UP),
                byte_group.animate.arrange(DOWN,aligned_edge=LEFT).shift(LEFT*4+DOWN)
            )

            indicate_word_group = SurroundingRectangle(word_group).set_stroke(PURPLE)
            indicate_byte_group = SurroundingRectangle(byte_group).set_stroke(PURPLE)
            self.play(Create(indicate_word_group), Create(indicate_byte_group))

            word = VGroup(word_group, indicate_word_group)
            byte = VGroup(byte_group, indicate_byte_group)

            self.play(word.animate.align_to(byte, RIGHT))


            param_lim = Tex(lim, font_size = 30).next_to(word, UP, buff=1.5).align_to(word, LEFT)
            param_base = Tex(base, font_size=30).next_to(param_lim, DOWN)
            param_type = Tex(t, font_size=30).next_to(param_base, DOWN)

            param_group = VGroup(param_lim, param_base, param_type)

            self.wait_until_bookmark("B")
            self.play(Create(param_group))
            self.wait_until_bookmark("C")
            self.play(Indicate(param_lim))
            self.wait_until_bookmark("D")
            self.play(Indicate(param_base))
            self.wait_until_bookmark("E")
            self.play(Indicate(param_type))

        #第一个值是 (lim >> 12) & 0xffff，表示将 lim 右移12位，然后取低16位；
        lim_first = param_lim.copy()
        binary_table = VGroup()

        for i in range(32):
            binary_digit = Tex("$1$", font_size=30).next_to(word, RIGHT)
            binary_digit.move_to(i * 0.2 * RIGHT)
            binary_table.add(binary_digit)

        surrand_pre = SurroundingRectangle(binary_table)

        binary = VGroup(binary_table, surrand_pre)

        binary_tmp = binary.copy()

        with self.voiceover(text="第一个内容首先是将参数<bookmark mark='C'/>limit进行<bookmark mark='A'/>右移,并取其后<bookmark mark='B'/>16位") as tracker:
            self.play(ApplyWave(word_lim))
            self.wait_until_bookmark("C")
            self.play(Transform(lim_first, binary_tmp))
            self.play(
                FadeOut(binary_tmp), 
                FadeOut(lim_first),
                FadeIn(binary)
            )

            surrand_pre_2 = SurroundingRectangle(binary_table[0:20])
            self.wait_until_bookmark("A")
            self.play(Transform(surrand_pre, surrand_pre_2))
            for i in reversed(range(20,32)):
                binary_table -= binary_table[i]

            self.play(Indicate(binary_table[4:]))

            lim_last_binary = binary_table[4:].copy()
            lim_last_rect = SurroundingRectangle(lim_last_binary)
            lim_last = VGroup(lim_last_binary, lim_last_rect)

            self.wait_until_bookmark("B")
            self.play(Transform(binary, lim_last))

            self.play(binary.animate.shift(UP*3+LEFT))

        # 第二个值是 (base & 0xffff)，表示将 base 的低16位保留。
        param_base_2 = param_base.copy()
        base_group = VGroup()

        with self.voiceover(text="第二个内容是取base值的后十六位") as tracker:

            self.play(ApplyWave(word_base))
            for i in range(16):
                base_temp = Tex("$0$", font_size=30).next_to(word, RIGHT)
                base_temp.move_to(i*0.2*RIGHT)
                base_group.add(base_temp)

            base_surrand = SurroundingRectangle(base_group)
            base = VGroup(base_group, base_surrand)

            base_tmp = base.copy()
            self.play(Transform(param_base_2, base_tmp))

            self.play(
                FadeOut(param_base_2),
                FadeOut(base_tmp),
                FadeIn(base)
            )

            self.play(base.animate.next_to(binary, RIGHT, buff=0.2))

        """
        .byte (((base) >> 16) & 0xff), (0x90 | (type)), (0xC0 | (((lim) >> 28) & 0xf)), (((base) >> 24) & 0xff): 这一行使用 .byte 
            指令将四个8位的值写入到内存中。
        这段代码的作用是生成了一条x86汇编指令，用于设置一个段描述符（Segment Descriptor），其中包含了段的类型、基地址和限制。
            具体的含义和用途还需要根据上下文进一步分析。
        """
        # 第一个值是 ((base >> 16) & 0xff)，表示将 base 右移16位，然后取低8位；


        base_third_value = Tex("$0$", font_size=30)
        base_third_group = VGroup(base_third_value)
        base_third_surrand = SurroundingRectangle(base_third_group).set_stroke(color=RED)
        base_third = VGroup(base_third_group, base_third_surrand)
        base_temp_thrid = param_base.copy()
        base_third_copy = base_third.copy()

        for i in range(16):
            base_temp_third = Tex("$0$", font_size=30)
            base_temp_third.move_to(i*0.2*RIGHT)
            base_third_group.add(base_temp_third)

        base_third_surrand_2 = SurroundingRectangle(base_third_group).set_stroke(color=RED)

        thrid_last_value = base_third_group[9:].copy()
        third_surrander = SurroundingRectangle(thrid_last_value).set_stroke(color=RED)
        third_last = VGroup(thrid_last_value, third_surrander)

        with self.voiceover(text="byte的第一个值是取<bookmark mark='A'/>base的前<bookmark mark='B'/>十六位,然后再取其<bookmark mark='C'/>低八位") as tracker:
            self.play(ApplyWave(byte_lim))
            self.wait_until_bookmark('A')
            self.play(Transform(base_temp_thrid, base_third_copy))

            self.play(
                FadeOut(base_third_copy),
                FadeOut(base_temp_thrid),
                FadeIn(base_third)
            )

            self.wait_until_bookmark('B')
            self.play(Transform(base_third_surrand, base_third_surrand_2))

            self.wait_until_bookmark('C')
            self.play(Indicate(base_third_group[9:]))
            self.play(Transform(base_third, third_last))
            self.play(base_third.animate.next_to(binary, DOWN, buff=0.2).align_to(binary, LEFT))

        # 第二个值是 (0x90 | type)，表示将 type 的值与 0x90 进行按位或运算；

        with self.voiceover(text="第二个值是将<bookmark mark='A'/>type的第一位<bookmark mark='B'/>和第四位<bookmark mark='C'/>置为1") as tracker:
            self.play(ApplyWave(byte_type))
            ninety = byte_type[0:4].copy()
            ninety_group = VGroup(ninety)
            self.play(ninety.animate.next_to(byte_type, RIGHT, buff=5).shift(UP))
            ninety_binary = Tex("$10010000$", font_size=30).move_to(ninety.get_center())
            self.play(Transform(ninety_group, ninety_binary))
            ninety_group.add(ninety_binary)

            type_value = param_type.copy()
            self.wait_until_bookmark('A')
            self.play(type_value.animate.next_to(ninety_binary, DOWN, buff=0.1).align_to(ninety_binary, RIGHT))
            type_binary = Tex("$00010000$", font_size=30).move_to(type_value.get_center()).align_to(ninety_binary, RIGHT)
            type_group = VGroup(type_value, type_binary)
            self.wait_until_bookmark('B')
            self.play(Transform(type_value, type_binary))

            forth_final_binary = Tex("$10010000$", font_size=30).move_to(ninety_group.get_center()).align_to(ninety_group, RIGHT)

            self.play(type_group.animate.shift(UP*0.3))
            forth = VGroup(type_group, ninety_group)
            self.wait_until_bookmark('C')
            self.play(
                FadeOut(forth),
                FadeIn(forth_final_binary))

            surrand_forth = SurroundingRectangle(forth_final_binary).set_stroke(color=RED)
            self.play(Create(surrand_forth))

            base_forth = VGroup(forth_final_binary, surrand_forth) 
            self.play(base_forth.animate.next_to(base_third, RIGHT, buff=0.2))


        # 第三个值是 (0xC0 | ((lim >> 28) & 0xf))，表示将 lim 右移28位，然后取低4位，并与 0xC0 进行按位或运算；

        fifth_binary_table = VGroup()
        for i in range(32):
            fifth_tmp = Tex("$1$", font_size=30).next_to(word,RIGHT)
            fifth_tmp.move_to(i * 0.15 * RIGHT)
            fifth_binary_table.add(fifth_tmp)

        fifth_surrand = SurroundingRectangle(fifth_binary_table).set_stroke(color=RED)
        fifth_group = VGroup(fifth_binary_table, fifth_surrand)
        param_lim_fifth = param_lim.copy()
        fifth_group_copy = fifth_group.copy()
        with self.voiceover(text="第三个值相对复杂一些,limit<bookmark mark='A'/>先向右<bookmark mark='B'/>移动28位,取其<bookmark mark='C'/>低四位后,与0xc0按位<bookmark mark='D'/>或运算") as tracker:
            self.play(ApplyWave(byte_third))
            self.wait_until_bookmark('A')
            self.play(Transform(param_lim_fifth, fifth_group_copy))
            self.play(
                FadeOut(fifth_group_copy),
                FadeOut(param_lim_fifth),
                FadeIn(fifth_group)
            )

            fifth_surrand_1 = SurroundingRectangle(fifth_binary_table[0:8]).set_stroke(color=RED)
            self.wait_until_bookmark('B')
            self.play(Transform(fifth_surrand, fifth_surrand_1))
            for i in reversed(range(8,32)):
                fifth_binary_table.remove(fifth_binary_table[i])

            for i in fifth_binary_table[0:4]:
                tmp = Tex("$0$", font_size=30).move_to(i.get_center())
                i.become(tmp)

            fifth_hex = Tex("$\mathtt{0xc0}$", font_size=30).next_to(fifth_binary_table, DOWN, buff=0.2).align_to(LEFT)
            fifth_binary = Tex("$11000000$", font_size=30).next_to(fifth_binary_table, DOWN, buff=0.2).align_to(LEFT)
            self.play(Create(fifth_hex))

            self.play(Transform(fifth_hex, fifth_binary))

            self.play(fifth_hex.animate.shift(UP*0.4))
            fifth_final = Tex("$11001111$", font_size=30).move_to(fifth_hex.get_center()).align_to(fifth_hex, RIGHT)

            self.play(
                FadeOut(fifth_binary_table),
                FadeOut(fifth_hex),
                FadeIn(fifth_final)
            )
            base_fifth = VGroup(fifth_final, fifth_surrand)
            self.play(base_fifth.animate.next_to(base_forth, RIGHT, buff=0.2))

        # 第四个值是 ((base >> 24) & 0xff)，表示将 base 右移24位，然后取低8位。
        sixth_binary_table = VGroup()
        for i in range(32):
            sixth_tmp = Tex("$0$", font_size=30).next_to(word,RIGHT)
            sixth_tmp.move_to(i * 0.2 * RIGHT)
            sixth_binary_table.add(sixth_tmp)

        sixth_surrand = SurroundingRectangle(sixth_binary_table).set_stroke(color=RED)
        sixth_group = VGroup(sixth_binary_table, sixth_surrand)

        param_base_3 = param_base.copy()
        sixth_group_copy = sixth_group.copy()
        with self.voiceover(text="最后一个值是将<bookmark mark='A'/>base右移<bookmark mark='B'/>24位,然后取其低八位") as tracker:

            self.play(ApplyWave(byte_fourth))
            self.wait_until_bookmark('A')
            self.play(Transform(param_base_3, sixth_group_copy))
            self.play(
                FadeOut(sixth_group_copy),
                FadeOut(param_base_3),
                FadeIn(sixth_group)
            )

            sixth_surrand_1 = SurroundingRectangle(sixth_binary_table[0:8]).set_stroke(color=RED)
            self.wait_until_bookmark('B')
            self.play(Transform(sixth_surrand, sixth_surrand_1))
            for i in reversed(range(8,32)):
                sixth_binary_table.remove(sixth_binary_table[i])

            base_sixth = VGroup(sixth_group, sixth_surrand)
            self.play(base_sixth.animate.next_to(base_fifth, RIGHT, buff=0.2).align_to(base, RIGHT))

        segment_descriptor = VGroup(
            base_sixth,
            base_fifth,
            base,
            binary,
            base_third,
            base_forth
        )
        ## 那么你要问了, 这些二进制都在干什么?

        b = Brace(segment_descriptor, DOWN)
        sg = b.get_text("Segment descriptor")
        with self.voiceover(text="这样,我们就构建了一个段描述符") as tracker:
            self.play(Create(b), Create(sg))

        all_seg = VGroup(segment_descriptor, b, sg)
        # 当我们在执行 cs:ip 的时候, cs 的段选择子

        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0
        for i in range(10):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                      grid_xstep=2.0, grid_ystep=0.5)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, DOWN, buff=0)
            addr.next_to(rect, LEFT, buff=0.2)
            mem.add(rect)
            addresses.add(addr)
            start_addr += 0x1000

        memory = VGroup(mem, addresses)
        with self.voiceover(text="描述符将存放在内存中,等候cs,ss等段寄存器来使用") as tracker:
            self.play(memory.animate.scale(0.7).move_to(ORIGIN).shift(RIGHT*3+DOWN))

            self.play(
                all_seg.animate.scale(0.1).move_to(ORIGIN).shift(RIGHT*3+DOWN),
            )
            self.play(
                FadeOut(all_seg)
            )
            self.play(
                Indicate(mem[5])
            )

        #self.wait()
