from manim import *

class WhatHackIsThisCode(Scene):
    def construct(self):
        code = """
#define SEG_ASM(type,base,lim)                                  \\
    .word (((lim) >> 12) & 0xffff), ((base) & 0xffff);          \\
    .byte (((base) >> 16) & 0xff), (0x90 | (type)),             \\
        (0xC0 | (((lim) >> 28) & 0xf)), (((base) >> 24) & 0xff)
"""

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

        self.add(code_obj)
        self.play(Indicate(word, run_time=1))
        self.play(Indicate(byte, run_time=1))

        word_group = VGroup()
        word_group.add(word_lim, word_base)

        byte_group = VGroup()
        byte_group.add(
            byte_lim, byte_type,
            byte_third, byte_fourth
        )

        self.play(
            FadeOut(code_obj),
            word_group.animate.arrange(DOWN,aligned_edge=LEFT).shift(LEFT*4.7+UP),
            byte_group.animate.arrange(DOWN,aligned_edge=LEFT).shift(LEFT*4+DOWN)
        )

        self.play(
            Circumscribe(word_group,time_width=2)
        )
        self.play(
            Circumscribe(byte_group,time_width=2)
        )

        t = "$type = \mathtt{0x10}$"
        base = "$base = \mathtt{0x0}$"
        lim = "$lim = \mathtt{0xffffffff}$"

        lim_param = Tex(lim)
        base_param = Tex(base).next_to(lim_param)
        type_param = Tex(t).next_to(base_param)

        #第一个值是 (lim >> 12) & 0xffff，表示将 lim 右移12位，然后取低16位；
        binary_table = VGroup()

        for i in range(32):
            binary_digit = Tex("$1$", font_size=30)
            binary_digit.move_to(2 * LEFT + i * 0.2 * RIGHT)
            binary_table.add(binary_digit)

        surrand_pre = always_redraw(
            lambda: SurroundingRectangle(binary_table)
        ) 

        binary = VGroup(binary_table, surrand_pre)
        self.play(Create(binary))

        self.wait()

        for i in reversed(range(20,32)):
            binary_table -= binary_table[i]

        self.wait()

        self.play(Indicate(binary_table[4:]))

        lim_last_binary = binary_table[4:].copy()
        lim_last_rect = SurroundingRectangle(lim_last_binary)
        lim_last = VGroup(lim_last_binary, lim_last_rect)

        self.play(Transform(binary, lim_last))

        self.wait()
        self.play(binary.animate.to_edge(UP))      


        # 第二个值是 (base & 0xffff)，表示将 base 的低16位保留。
        base_value = Tex("$0$", font_size=30)
        base_group = VGroup(base_value)
        base_surrand = SurroundingRectangle(base_group)
        base = VGroup(base_group, base_surrand)
        self.add(base)
        self.wait()
        for i in range(16):
            base_temp = Tex("$0$", font_size=30)
            base_temp.move_to(i*0.2*RIGHT)
            base_group.add(base_temp)

        base_surrand_2 = SurroundingRectangle(base_group)
        self.play(Transform(base_surrand, base_surrand_2))

        self.wait()
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
        self.add(base_third)

        self.wait()

        for i in range(16):
            base_temp_third = Tex("$0$", font_size=30)
            base_temp_third.move_to(i*0.2*RIGHT)
            base_third_group.add(base_temp_third)

        base_third_surrand_2 = SurroundingRectangle(base_third_group).set_stroke(color=RED)
        self.play(Transform(base_third_surrand, base_third_surrand_2))

        self.wait()
        #self.play(base_third.animate.next_to(binary, DOWN, buff=0.2))

        self.play(Indicate(base_third_group[9:]))

        thrid_last_value = base_third_group[9:].copy()
        third_surrander = SurroundingRectangle(thrid_last_value).set_stroke(color=RED)
        third_last = VGroup(thrid_last_value, third_surrander)

        self.play(Transform(base_third, third_last))

        self.play(base_third.animate.next_to(binary, DOWN, buff=0.2).align_to(binary, LEFT))

        # 第二个值是 (0x90 | type)，表示将 type 的值与 0x90 进行按位或运算；
        ninety = byte_type[0:4].copy()
        ninety_group = VGroup(ninety)
        self.play(ninety.animate.next_to(byte_type , RIGHT, buff=5).shift(UP))
        self.wait()
        ninety_binary = Tex("$1001$", font_size=30).move_to(ninety.get_center())
        self.play(Transform(ninety_group, ninety_binary))
        ninety_group.add(ninety_binary)

        type_value = Tex("$\mathtt{0x10}$", font_size=30).next_to(ninety_binary, DOWN, buff=0.1)
        self.play(Create(type_value))
        self.wait()
        type_binary = Tex("$00010000$", font_size=30).move_to(type_value.get_center()).align_to(ninety_binary, RIGHT)
        type_group = VGroup(type_value, type_binary)
        self.play(Transform(type_value, type_binary))

        forth_final_binary = Tex("$00011001$", font_size=30).move_to(ninety_group.get_center()).align_to(ninety_group, RIGHT)

        self.play(type_group.animate.shift(UP*0.3))
        forth = VGroup(type_group, ninety_group)
        self.play(
            FadeOut(forth),
            FadeIn(forth_final_binary))

        surrand_forth = SurroundingRectangle(forth_final_binary).set_stroke(color=RED)
        self.play(Create(surrand_forth))

        base_forth = VGroup(forth_final_binary, surrand_forth) 
        self.play(base_forth.animate.next_to(base_third, RIGHT, buff=0.2))

        self.wait()

        # 第三个值是 (0xC0 | ((lim >> 28) & 0xf))，表示将 lim 右移28位，然后取低4位，并与 0xC0 进行按位或运算；

        fifth_binary_table = VGroup()

        for i in range(32):
            fifth_tmp = Tex("$1$", font_size=30)
            fifth_tmp.move_to(2 * LEFT + i * 0.15 * RIGHT)
            fifth_binary_table.add(fifth_tmp)

        fifth_surrand = SurroundingRectangle(fifth_binary_table).set_stroke(color=RED)
        fifth_group = VGroup(fifth_binary_table, fifth_surrand)
        self.play(Create(fifth_group))
        self.wait()

        fifth_surrand_1 = SurroundingRectangle(fifth_binary_table[0:8]).set_stroke(color=RED)
        self.play(Transform(fifth_surrand, fifth_surrand_1))
        for i in reversed(range(8,32)):
            fifth_binary_table.remove(fifth_binary_table[i])

        self.wait()
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
            sixth_tmp = Tex("$0$", font_size=30)
            sixth_tmp.move_to(2 * LEFT + i * 0.2 * RIGHT)
            sixth_binary_table.add(sixth_tmp)

        sixth_surrand = SurroundingRectangle(sixth_binary_table).set_stroke(color=RED)
        sixth_group = VGroup(sixth_binary_table, sixth_surrand)
        self.play(Create(sixth_group))

        sixth_surrand_1 = SurroundingRectangle(sixth_binary_table[0:8]).set_stroke(color=RED)
        self.play(Transform(sixth_surrand, sixth_surrand_1))
        for i in reversed(range(8,32)):
            sixth_binary_table.remove(sixth_binary_table[i])

        base_sixth = VGroup(sixth_group, sixth_surrand)
        self.play(base_sixth.animate.next_to(base_fifth, RIGHT, buff=0.2).align_to(base, RIGHT))

        self.wait()
