from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class WhyDiscreteMath(VoiceoverScene):
    def construct(self):

        self.set_speech_service(RecorderService())

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
        # 脚本:
        # 这是一段 python 的代码, 需要判断一个条件,用一个语句就可以了.
        with self.voiceover(text="这段代码有判断一个条件.") as tracker:
            self.add(py_code)
            self.play(ApplyWave(py_code.code[1][7:16], run_time=2))

        # 当判断条件达到三个的时候, 我们将面临 2^3 八个分支.
        # 那么我们可以做什么以简化这些分支吗?

        with self.voiceover(text="当判断条件达到三个的时候, 我们将面临 2^3, 八个分支.") as tracker:
            self.play(FadeOut(py_code), FadeIn(long_py_code))
            self.play(ApplyWave(long_py_code.code[1][6:35], run_time=2))

        first_if = long_py_code.code[1][6:13].copy()
        second_if = long_py_code.code[1][17:24].copy()
        third_if = long_py_code.code[1][28:35].copy()

        with self.voiceover(text="我们可以做什么来简化分支吗 ?") as tracker:
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
            [["T", "T", "T", ""],
             ["F", "F", "T", ""],
             ["T", "F", "T", ""],
             ["T", "T", "F", ""],
             ["F", "F", "T", ""],
             ["F", "T", "F", ""],
             ["T", "F", "F", ""],
             ["F", "F", "F", ""],],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4)

        # 离散数学当中数论(counting)部分. 我们有多少的条件需要进行判断?
        # 让我们引入一个离散数学当中最基础的真值表.
        with self.voiceover(text="让我们引入一个离散数学当中最基础的真值表") as tracker:
            self.play(
                truth_table.animate.move_to(LEFT*0.3).set_row_colors(YELLOW),
                if_group.animate.arrange(DOWN).next_to(truth_table, RIGHT, buff=0.1)
            )

        # 并把所有的情况遍历在真值表当中.
        with self.voiceover(text="并把所有的情况遍历在真值表当中") as tracker:
            self.play(Indicate(truth_table.get_rows()[1:]))


        """
        how discrete resolve problem
        """
        result_truth_table =Table(
            [["T", "T", "T", "do_a"],
             ["F", "T", "T", "do_c"],
             ["T", "F", "T", "do_a"],
             ["T", "T", "F", "do_b"],
             ["F", "F", "T", "do_d"],
             ["F", "T", "F", "do_c"],
             ["T", "F", "F", "do_a"],
             ["F", "F", "F", "do_d"],],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4).move_to(LEFT*0.3).set_row_colors(YELLOW)
        ordered_truth_table =Table(
            [["T", "T", "T", "do_a"],
             ["T", "F", "T", "do_a"],
             ["T", "F", "F", "do_a"],
             ["T", "T", "F", "do_b"],
             ["F", "T", "F", "do_c"],
             ["F", "T", "T", "do_c"],
             ["F", "F", "T", "do_d"],
             ["F", "F", "F", "do_d"]],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4).move_to(LEFT*0.3).set_row_colors(YELLOW, RED, RED,
                                                      RED, BLUE, PURPLE,
                                                      PURPLE, GREEN, GREEN)

        # 接着, 我们给所有的情况所要做的事情列出来.与条件一一对应, 并做好排序.
        with self.voiceover(text="接着, 我们给所有的情况所要做的事情列出来.与条件一一对应, 并做好排序.") as tracker:
            self.play(Create(result_truth_table),FadeOut(truth_table))
            self.play(result_truth_table.animate.set_row_colors(
                YELLOW,
                RED, PURPLE, RED,
                BLUE, GREEN, PURPLE,
                RED, GREEN
            ))
            self.wait(3.5)
            self.play(Transform(result_truth_table, ordered_truth_table))

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

        # 根据真值表, 我们就可以写出这种程序.
        self.play(tb_group.animate.move_to(LEFT*4), FadeOut(ordered_truth_table))
        with self.voiceover(text="让我们把真值表转换成程序") as tracker:
            pass
        self.play(
            FadeIn(result_py_code.scale(0.8).next_to(result_truth_table, RIGHT, buff=0.2)),
        )

        self.play(FadeOut(result_py_code.code))
        with self.voiceover(text="从真值表我们可以看到,如果x与y为假,不论z的真假.都是do_d") as tracker:
            c1 = result_truth_table.get_cell((8,1))
            c2 = result_truth_table.get_cell((8,2))
            c3 = result_truth_table.get_cell((9,1))
            c4 = result_truth_table.get_cell((9,2))
            indicated_group = VGroup(c1,c2,c3,c4)
            self.play(Indicate(indicated_group,run_time=tracker.get_remaining_duration() ))
            self.play(
                FadeOut(indicated_group),
            )

        self.play(FadeIn(result_py_code.code[:3]))
        with self.voiceover(text="而x与y为真,z为假的情况下.do_b") as tracker:
            c1 = result_truth_table.get_cell((5,1))
            c2 = result_truth_table.get_cell((5,2))
            c3 = result_truth_table.get_cell((5,3))
            indicated_group = VGroup(c1,c2,c3)
            self.play(Indicate(indicated_group,run_time=tracker.get_remaining_duration() ))
            self.play(
                FadeOut(indicated_group),
            )
        self.play(
            FadeIn(result_py_code.code[3:5])
        )

        with self.voiceover(text="而x为假,y为真的情况下,不论z的真假,都是do_c") as tracker:
            c1 = result_truth_table.get_cell((6,1))
            c2 = result_truth_table.get_cell((6,2))
            c3 = result_truth_table.get_cell((7,1))
            c4 = result_truth_table.get_cell((7,2))
            indicated_group = VGroup(c1,c2,c3,c4)
            self.play(Indicate(indicated_group,run_time=tracker.get_remaining_duration() ))
            self.play(
                FadeOut(indicated_group),
            )
        self.play(
            FadeIn(result_py_code.code[5:7]),
        )

        with self.voiceover(text="最后剩余的所有情况都是do_a") as tracker:
            indicated_group = VGroup()
            list = [
                (2,1), (2,2), (2,3),
                (3,1), (3,2), (3,3),
                (4,1), (4,2), (4,3),
            ]
            for item in list:
                result_truth_table.get_cell(item)
            self.play(Indicate(indicated_group,run_time=tracker.get_remaining_duration() ))
            self.play(
                FadeOut(indicated_group),
            )
        self.play(
            FadeIn(result_py_code.code[7:9]),
        )


        # 可以看到, 每个分支条件与真值表中的同颜色区域进行一一对应.
        # 这样, 我们就可以很自信的说, 我们简化了分支, 并且从数学上证明了它不会遗漏任何情况.

        with self.voiceover(text="可以看到, 每个分支条件与真值表中的同颜色区域进行一一对应.") as tracker:
            self.play(Indicate(result_py_code.code[3:5]))
            self.play(Indicate(result_truth_table.get_rows()[4:5]))

            self.play(Indicate(result_py_code.code[5:7]))
            self.play(Indicate(result_truth_table.get_rows()[5:7]))

            self.play(Indicate(result_py_code.code[1:3]))
            self.play(Indicate(result_truth_table.get_rows()[7:9]))

            self.play(Indicate(result_py_code.code[7:9]))
            self.play(Indicate(result_truth_table.get_rows()[1:4]))

        with self.voiceover(text="这样, 我们就可以很自信的说, 我们简化了分支, 并且从数学上证明了它不会遗漏任何情况.") as tracker:
            pass
