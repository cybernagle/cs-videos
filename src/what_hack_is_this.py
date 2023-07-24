from manim import *

class WhatHackIsThisCode(Scene):
    def construct(self):
        code = """
#define SEG_ASM(type,base,lim)                                  \\
    .word (((lim) >> 12) & 0xffff), ((base) & 0xffff);          \\
    .byte (((base) >> 16) & 0xff), (0x90 | (type)),             \\
        (0xC0 | (((lim) >> 28) & 0xf)), (((base) >> 24) & 0xff)
"""

        code_obj = Code(code=code,
                        #tab_width=4, language="C", style="fruity")
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
            word_group.animate.arrange(DOWN,aligned_edge=LEFT).shift(LEFT*3.7+UP),
            byte_group.animate.arrange(DOWN,aligned_edge=LEFT).shift(LEFT*3+DOWN)
        )

        self.play(
            Circumscribe(word_group,time_width=2)
        )
        self.play(
            Circumscribe(byte_group,time_width=2)
        )

        lim = "$type = \mathtt{0x10}$"
        base = "$base = \mathtt{0x0}$"
        t = "$lim = \mathtt{0xffffffff}$"

        type_param = Tex(t).next_to(base_param)
        lim_param = Tex(lim)
        base_param = Tex(base).next_to(lim_param)


