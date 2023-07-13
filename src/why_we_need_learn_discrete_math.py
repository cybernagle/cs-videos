from manim import *
#from manim_voiceover import VoiceoverScene
#from manim_voiceover.services.recorder import RecorderService

class WhyDiscreteMath(Scene):
    def construct(self):
        code = """
        def why_discrete_math():
            if (x == true):
                do_something()
            else:
                do_other()
        """

        long_code = """
        def why_discrete_math():
            if(x==true && y==true && z==true):
                do_something()
            else if(x==true && y==true && z==false):
                do_something()
            ...
            else:
                do_other()
        """
        py_code = Code(code=code, tab_width=4, background="window",
                     language="Python", font="Monospace")
        long_py_code = Code(code=long_code, tab_width=4, background="window",
                     language="Python", font="Monospace")


        """
        define problem
        1. 2 * 2 * 2 = 8
        丑陋, 而且其中部分情况可能是服用的, 比如说如果 x 和 y 为真, 那么 z 的结果将不重要, 我们都是 do_something_xy()
        那么我就可以省去几行判断条件. 那么有什么工具可以帮助我们来分析这种情况, 并且确保我们的代码没有 bug 吗? 答案是肯定的, 就是真值表.
        """
        self.add(py_code)
        self.play(ApplyWave(py_code.code[1][7:16], run_time=2))
        self.play(FadeOut(py_code), FadeIn(long_py_code))

        self.play(ApplyWave(long_py_code.code[1][6:35], run_time=2))
        first_if = long_py_code.code[1][6:13].copy()
        second_if = long_py_code.code[1][17:24].copy()
        third_if = long_py_code.code[1][28:35].copy()

        self.play(first_if.animate.next_to(long_py_code, DOWN, 0.1).shift(LEFT*1.8))
        self.play(second_if.animate.next_to(first_if, RIGHT, buff = 0.5))
        self.play(third_if.animate.next_to(second_if, RIGHT, buff = 0.5))
        if_group = Group(first_if, second_if, third_if)
        self.play(FadeOut(long_py_code), if_group.animate.move_to(UP*0.5))

        """
        if !x & !y:
        if !x & y:
        if x & y & !z:
        else:
        """

        truth_table =Table(
            [["true", "true", "true", ""],
             ["false", "true", "true", ""],
             ["true", "false", "true", ""],
             ["true", "true", "false", ""],
             ["false", "false", "true", ""],
             ["false", "true", "false", ""],
             ["true", "false", "false", ""],
             ["false", "false", "false", ""],],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4)

        # 离散数学当中数论(counting)部分. 我们有多少的条件需要进行判断?
        self.play(
            truth_table.animate.move_to(LEFT*0.3).set_row_colors(YELLOW),
            if_group.animate.arrange(DOWN).next_to(truth_table, RIGHT, buff=0.1)
        )

        self.play(Indicate(truth_table.get_rows()[1:]))
        self.wait()


        """
        how discrete resolve problem
        """
        result_truth_table =Table(
            [["true", "true", "true", "do_a"],
             ["false", "true", "true", "do_c"],
             ["true", "false", "true", "do_a"],
             ["true", "true", "false", "do_b"],
             ["false", "false", "true", "do_d"],
             ["false", "true", "false", "do_c"],
             ["true", "false", "false", "do_a"],
             ["false", "false", "false", "do_d"],],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4).move_to(LEFT*0.3).set_row_colors(YELLOW)


        self.play(Create(result_truth_table),FadeOut(truth_table))
        self.play(result_truth_table.animate.set_row_colors(
            YELLOW,
            RED, PURPLE, RED,
            BLUE, GREEN, PURPLE,
            RED, GREEN
        ))


        ordered_truth_table =Table(
            [["true", "true", "true", "do_a"],
             ["true", "false", "true", "do_a"],
             ["true", "false", "false", "do_a"],
             ["true", "true", "false", "do_b"],
             ["false", "true", "false", "do_c"],
             ["false", "true", "true", "do_c"],
             ["false", "false", "true", "do_d"],
             ["false", "false", "false", "do_d"]],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4).move_to(LEFT*0.3).set_row_colors(YELLOW, RED, RED,
                                                      RED, BLUE, PURPLE,
                                                      PURPLE, GREEN, GREEN)

        self.play(Transform(result_truth_table, ordered_truth_table))#, FadeOut(result_truth_table))
        self.wait(1)

        result_code = """
        def why_discrete_math():
            if(x==false && y==false):
                do_d()
            else if(x==true && y==true && z==false):
                do_b()
            else if(x == false && y == true):
                do_c()
            else:
                do_a()
        """
        result_py_code = Code(code=result_code, tab_width=4, background="window",
                     language="Python", font="Monospace")
        tb_group = Group(result_truth_table ,ordered_truth_table)

        self.play(tb_group.animate.move_to(LEFT*3), FadeOut(ordered_truth_table))
        self.play(FadeIn(result_py_code.scale(0.5).move_to(RIGHT*2)))

        self.play(Indicate(result_py_code.code[3:5]))
        self.play(Indicate(result_truth_table.get_rows()[4:5]))

        self.play(Indicate(result_py_code.code[5:7]))
        self.play(Indicate(result_truth_table.get_rows()[5:7]))

        self.play(Indicate(result_py_code.code[1:3]))
        self.play(Indicate(result_truth_table.get_rows()[7:9]))

        self.play(Indicate(result_py_code.code[7:9]))
        self.play(Indicate(result_truth_table.get_rows()[1:4]))
