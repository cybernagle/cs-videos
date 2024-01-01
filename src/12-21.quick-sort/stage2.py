from manim  import *
from manim.typing import Vector3

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

# quick sort 
import random

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

class quicksortStage2(VoiceoverScene):

    stack = VGroup()

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND
    
    def clear_except(self,obj):
        self.mobjects = [obj]
        self.foreground_mobjects = [obj]

    def computer_voice(self):
        self.set_speech_service(
            AzureService(
                voice="zh-CN-YunhaoNeural",
                style="newscast-casual",
            )
        )
    def human_voice(self):
        self.set_speech_service(
            AzureService(
                voice="zh-CN-XiaomengNeural",
                style="newscast-casual",
            )
        )

    def construct(self):
        self.computer_voice()

        # 为什么呢? 
        why = Text("为什么会退化成 O(n^2) 呢?")
        with self.voiceover(text="为什么呢?") as tracker:
            self.play(Write(why))
        self.wait()
        self.play(FadeOut(why))

        data = [99, 98, 97, 96, 95, 94]
        squares = VGroup()

        # . 
        for i in data:
            square = Square(side_length=0.5, color=OBJ_A, fill_opacity=1)
            text = Text(str(i)).scale(0.5).move_to(square.get_center())
            s = VGroup(square, text)
            squares.add(s)
        squares.arrange(RIGHT).move_to(ORIGIN)
        with self.voiceover(text="答案是,我们选择的中间数") as tracker:
            self.play(FadeIn(squares))

        why_happen = """
        在最坏的情况当中, 我们可以看到, 因为数字是逆序的
        之前的算法选择的是第一个数字作为中间数
        这样导致了每次排序第一个都是最大的数字.而剩余的都是 smaller 
        这样, 我们的算法就会因为没有二分, 而退化成 O n 平方
        那么怎么解决呢?
        """

        with self.voiceover(text=why_happen) as tracker:
            for k,v in enumerate(squares):
                self.play(
                    v[0].animate.set_color(OBJ_C).set_z_index(2),
                    v[1].animate.set_z_index(3)
                )
                self.play(Wiggle(squares[k:]))

        self.clear()

        #   随机数
        randomiaze = Text("随机数")
        with self.voiceover(text="随机数") as tracker:
            self.play(Write(randomiaze))
            self.play(FadeOut(randomiaze))

        # 我们来证明这一点,
        # 1. 我们来计算, 在排序过程中, 我们需要进行多少次比较.
        # 2. 每次排序中, 每次比较的成本是多少? 
        # 3. 汇总每次排序的成本, 就是我们总的算法复杂度.

        proof_text = """
             1. 我们来计算, 在排序过程中, 我们需要进行多少次比较.
             2. 每次排序中, 每次比较的成本是多少? 
             3. 汇总每次排序的成本, 就是我们总的算法复杂度.
            """
        vproof_text = "我们的证明步骤如下: "  + proof_text
        tproof = Text(proof_text).scale(0.8)
        with self.voiceover(text=vproof_text) as tracker:
            self.play(Write(tproof), run_time=tracker.get_remaining_duration())

        self.clear()

        data = [20, 84, 41, 73, 27, 5, 96, 98, 46, 64]
        demo = VGroup()
        for i in data:
            square = Square(side_length=0.5, color=OBJ_A, fill_opacity=1)
            demo.add(square)
        demo.arrange(RIGHT).move_to(ORIGIN)
        self.play(FadeIn(demo))
        
        # 快速排序是每次将这堆内容分为两个部分.
        with self.voiceover(text="快速排序是每次将这堆内容分为两个部分") as tracker:
            self.play(
                demo[0:5].animate.shift(LEFT),
                demo[5:0].animate.shift(RIGHT)
            )

            self.play(demo.animate.shift(UP*2))
        # 大堆和小堆的每个对象之间都只会比较一次. 
        # 如果每次交换我们将其定义为 X,i,j.每两个元素之间都会有比较发生的可能性.
        tcompare = """
        如果每次交换我们将其定义为 X,i,j. 每两个元素之间都会有比较发生的可能性.
        因为每一次的递归选择的中间数都不一样, 所以大堆和小堆的每个对象之间都只会比较一次.
        """

        zero = MathTex('i').scale(0.5).next_to(demo[0], DOWN)
        j = MathTex('j').scale(0.5).next_to(demo[4], DOWN)
        jplus = MathTex('j+1').scale(0.5).next_to(demo[5], DOWN)
        n = MathTex('n').scale(0.5).next_to(demo[-1], DOWN)
        compare = MathTex("X_{i,j} = I\{Z_i\ compare\ to\ Z_j\}").move_to(ORIGIN)
        with self.voiceover(text=tcompare) as tracker:
            self.play(FadeIn(compare))
            self.play(FadeIn(j), FadeIn(n), FadeIn(zero), FadeIn(jplus))


            for k, v in enumerate(demo):
                p1 = v.get_center()
                if k == 4: continue
                if k+1 < len(demo):
                    p2 = demo[k+1].get_center()
                    self.play(
                        v.copy().set_fill(color=OBJ_B).animate.move_to(p2),
                        demo[k+1].copy().set_fill(color=OBJ_B).animate.move_to(p1),
                    )

            demo2 = demo[6:]
            for k, v in enumerate(demo2):
                p1 = v.get_center()
                if k == 4: continue
                if k+1 < len(demo2):
                    p2 = demo2[k+1].get_center()
                    self.play(
                        v.copy().set_fill(color=OBJ_C).animate.move_to(p2),
                        demo2[k+1].copy().set_fill(color=OBJ_C).animate.move_to(p1))

            demo3 = demo[7:]
            for k, v in enumerate(demo3):
                p1 = v.get_center()
                if k == 4: continue
                if k+1 < len(demo3):
                    p2 = demo3[k+1].get_center()
                    self.play(
                        v.copy().set_fill(color=WORD_A).animate.move_to(p2),
                        demo3[k+1].copy().set_fill(color=WORD_A).animate.move_to(p1))

            demo4 = demo[8:]
            for k, v in enumerate(demo4):
                p1 = v.get_center()
                if k == 4: continue
                if k+1 < len(demo4):
                    p2 = demo4[k+1].get_center()
                    self.play(
                        v.copy().set_fill(color=WORD_B).animate.move_to(p2),
                        demo4[k+1].copy().set_fill(color=WORD_B).animate.move_to(p1))
        sum = MathTex(r"\sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{i,j}").next_to(compare, DOWN)
        with self.voiceover(text="要计算所有的比较次数可能性, 就可以得到以下的公式") as tracker:
            self.play(Write(sum))
        
        # 然而, 并不是所有的比较都会发生的, 比如说, 小堆里面选择的中间数, 和大堆就不会再比较了.
        with self.voiceover(text="然而, 并不是所有的比较都会发生的, 比如说, 小堆里面选择的中间数, 和大堆就不会再比较了.所以说, 一部分的比较是不会发生的.") as tracker:
            self.play(Indicate(demo[0]))
            self.play(Indicate(demo[5:]))
        self.clear_except(compare)

        compare0 = MathTex("=\ Prob\{Z_i\ compare\ to\ Z_j\}").next_to(compare, RIGHT)
        compare1 = MathTex("=\ Prob\{Z_i\ or Z_j\ is\ pivot\}").next_to(compare0, DOWN)
        compare2 = MathTex("=\ Prob\{Z_i\ is\ pivot\}+Prob\{Z_j\ is\ pivot\}").next_to(compare1, DOWN)
        #1/(j-i+1)
        compare3 = MathTex("=\ \\frac{1}{j-i+1} + \\frac{1}{j-i+1}").next_to(compare2, DOWN)
        compare4 = MathTex("=\ \\frac{2}{j-i+1}").next_to(compare3, DOWN)
        # 这样, 我们只要计算出在随机中间数的情况下发生次数的可能性, 我们就能够得到我们算法的复杂度了.
        with self.voiceover(text="这样, 我们只要计算出在随机中间数的情况下发生次数的可能性, 我们就能够得到我们算法的复杂度了.") as tracker:
            self.play(compare.animate.shift(LEFT*4+UP*2))

        # Z_i 和 Z_j 之间发生了比较.
        # 可以被表达为我们在数组当中Z i 被选为中间数,或者 Z j 被选为中间数.
        # 这样, 我们就可以得出, 发生比较的可能性, 就是 Z i 被选为中间数的可能性, 加上 Z j 被选为中间数的可能性.
        # 然后我们就能够得出一个比较的时间复杂度.
        single_compare = """
        Z_i 和 Z_j 之间发生了<bookmark mark='A'/>比较.
        可以被表达为我们在数组当中<bookmark mark='B'/>Z i 被选为中间数,或者 Z j 被选为中间数.
        这样, 我们就可以得出, 发生比较的可能性, 就是<bookmark mark='C'/> Z i 被选为中间数的可能性, 加上 Z j 被选为中间数的可能性.
        <bookmark mark='D'/>
        然后我们就能够得出一个比较的时间复杂度.
        """

        with self.voiceover(text=single_compare) as tracker:
            self.wait_until_bookmark("A")
            self.play(Create(compare0))
            self.wait_until_bookmark("B")
            self.play(Create(compare1))
            self.wait_until_bookmark("C")
            self.play(Create(compare2))
            self.wait_until_bookmark("D")
            self.play(Create(compare3))
            self.play(Create(compare4))

        self.clear()

        sum0 = MathTex(r"=\ \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \frac{2}{j-i+1}").next_to(sum, RIGHT)
        sum1 = MathTex(r"=\ \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k+1}").next_to(sum0, DOWN)
        sum2 = MathTex(r"=\ \sum_{i=1}^{n-1} \sum_{k=1}^{n} \frac{2}{k}").next_to(sum1, DOWN)
        sum3 = MathTex(r"=\ \sum_{i=1}^{n-1} O(\lg(n))").next_to(sum2, DOWN)
        sum4 = MathTex(r"=\ O(n\lg(n))").next_to(sum3, RIGHT)
        # 把这个结果, 代入到我们的求和公式, 进行进一步的演算, 就可以得到我们的算法复杂度为 O(n*logn) 了
        with self.voiceover(text="把这个结果, 代入到我们的求和公式, 进行进一步的演算, 就可以得到我们的算法复杂度为 O(n*logn) 了") as tracker:
            self.play(Create(sum))
            self.play(sum.animate.shift(LEFT*4+UP*3.5))
            self.play(Create(sum0))
            self.play(Create(sum1))
            self.play(Create(sum2))
            self.play(Create(sum3))
            self.play(Create(sum4))
