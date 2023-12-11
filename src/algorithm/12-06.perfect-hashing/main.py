import os
from manim import *

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

hash_u_to_m = Polygon(
    [-2.5, -2, 0],  # 左下角点
    [-2.5, 2, 0],   # 左上角点
    [-1, 1.3, 0],    # 右上角点
    [-1, -1.3, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5,
    stroke_opacity=0
)

univasal = Rectangle(height=4, width=0.4, color=OBJ_A, fill_opacity=0.5).next_to(hash_u_to_m, LEFT, buff=0.05)
tunivasal = Text("U", color=WORD_A).scale(0.5).move_to(univasal)
gunivasal = VGroup(univasal, tunivasal)

m = Rectangle(height=2.6, width=0.4, color=OBJ_B, fill_opacity=0.5).next_to(hash_u_to_m, RIGHT, buff=0.05)
tm = Text("M", color=WORD_B).scale(0.5).move_to(m)
gm = VGroup(m, tm)

perfect_m = univasal.copy().set_fill(OBJ_B).move_to(m)
hash_u_to_perfectm = Polygon(
    [-2.5, -2, 0],  # 左下角点
    [-2.5, 2, 0],   # 左上角点
    [-1, 2, 0],    # 右上角点
    [-1, -2, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5,
    stroke_opacity=0
)

ghash_u_to_m = VGroup(gunivasal, gm, hash_u_to_m)

birthdays = [
    '01-15',
    '02-14',
    '03-14',
    '04-07',
    '05-21',
    '06-30',
    '07-04',
    '08-16',
    '09-09',
    '10-31',
    '11-11',
    '12-25',
    '01-01',
    '02-14',
    '03-29',
    '04-22',
    '05-05',
    '06-18',
    '07-07',
    '08-08',
    '09-23',
    '10-10',
    '11-26',
]

# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic
class PerfectHashing(Scene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND

    def clear_obj_expect(self, mobject):
        self.mobjects=[mobject]
        self.foreground_mobjects=[mobject]

    def birthday_paradox(self):
# 第一节 生日悖论
        # 问你一个问题, 你们的班级现在有 23 个人，假设每个人的生日是随机的，那么有两个人生日一样的可能性是多少呢？
        kids = Group()
        for png in os.listdir("png"):
            if png.endswith(".png"):
                img = ImageMobject("png/"+png)
                img.scale(0.2)
                kids.add(img)

        kids.arrange_in_grid(buff=0.5)
        self.add(kids)

        birthday = VGroup()
        for i in enumerate(birthdays):
            text = Text(i[1]).scale(0.4).next_to(kids[i[0]], UP, buff=0.1)
            if i[0] < 5:
                self.play(FadeIn(text))
            birthday.add(text)

        self.wait()
        
        self.add(birthday)
        self.wait()
        self.play(
            birthday[1].animate.set_fill(RED),
            birthday[13].animate.set_fill(RED),
        )
        self.play(
            Indicate(birthday[1]),
            Indicate(birthday[13]),
        )

        guess1 = Text("10%").scale(2).next_to(kids, RIGHT, buff=1).shift(UP)
        guess2 = Text("23%").scale(2).next_to(guess1, DOWN, buff=0.2)
        guess3 = Text("50%").scale(2).next_to(guess2, DOWN, buff=0.2)

        # 是 18%
        self.play(
            FadeIn(guess1)
        )
        self.wait()
        # 23%
        self.play(FadeIn(guess2))
        self.wait()

        # 还是 50%?
        self.play(FadeIn(guess3))
        self.wait()

        # 答案可能超乎你的想象, 50.7%
        # 而当人数增加到 70 个人的时候, 这个数字就会变成 99.9%
        self.clear()
        fifty0 = MathTex(r"23").scale(2)
        fifty = MathTex(r"\rightarrow 50.7\%").scale(2)
        gfifty = VGroup(fifty0, fifty).arrange(buff=0.1)
        ninety_nine = MathTex(r"70 \rightarrow 99.9\%").scale(2).next_to(gfifty, DOWN, buff=0.5)
        self.play(Create(fifty0))
        self.wait()

        self.play(Create(fifty))
        self.wait()
        self.play(Create(ninety_nine))
        self.wait()

        # 换句话说, 如果你们的班级有 70 人的时候,你们班级里 99.9% 会有两个人生日相同
        # 〉 请注意, 这个和 70 个人的时候, 一定有一个人和你的生日相同不一样.
        self.play(FadeOut(gfifty))
        self.play(ninety_nine.animate.move_to(ORIGIN))

    ### 形式化证明 ###
        self.clear()
        # 为什么会这样呢？我们来看看这个问题的发现过程
        self.add(kids)
        prob = MathTex(r"p = \frac{1}{365}").next_to(kids, RIGHT, buff=1).align_on_border(UP)
        notprob = MathTex(r"p = \frac{364}{365}").next_to(kids, RIGHT, buff=1).align_on_border(UP)

        # 首先我们来看看只有两个人的情况
        self.play(FadeIn(birthday[0:2]))
        # 两个人的生日相同的概率是 1/365, 因为两个人同一天生日意味着只能是 365 中的一天. 
        self.play(FadeIn(prob))
        # 那么也就是说两个人的生日不同的概率是 364/365, 
        self.play(prob.animate.become(notprob))

        # 当达到 3 个人的时候, 就是 364/365 * 363/365
        self.play(FadeIn(birthday[2]))
        three_notprob = MathTex(r"\cdot \frac{363}{365}").next_to(notprob, DOWN, buff=0.3).shift(RIGHT*0.4)
        self.play(notprob.animate.become(three_notprob))

        # 四个人, 在乘以 362/365
        self.play(FadeIn(birthday[3]))
        four_notprob = MathTex(r"\cdot \frac{362}{365}").next_to(three_notprob, DOWN, buff=0.3)
        self.play(three_notprob.animate.become(four_notprob))

        # 而 23 个人, 则是 361/365 * 360/365 * 359/365 * ... * 343/365
        self.play(FadeIn(birthday[4:]))
        # 它的结果是, 是 49.3%
        rprob = MathTex("...").next_to(four_notprob, DOWN, buff=0.3)
        rprob_2 = MathTex(r"\frac{342}{365}").next_to(rprob, DOWN, buff=0.3)
        rprob_3 = MathTex("= 49.3%").set_color(OBJ_A).next_to(rprob_2, DOWN, buff=0.3)
        rnotprob = MathTex("= 50.7%").set_color(OBJ_A).next_to(rprob_2, DOWN, buff=0.3)
        self.play(
            FadeIn(rprob),
            FadeIn(rprob_2),
            FadeIn(rprob_3),
        )

        self.wait()
        minus1 = MathTex(r"1 - ").set_color(OBJ_A).next_to(prob, LEFT, buff=0.1)
        self.play(
            rprob_3.animate.become(rnotprob),
            FadeIn(minus1),
        )
        ## 那么至少有两个人生日相同的概率是多少呢？
        # 1 - 49.3% = 50.7%
        self.wait()
        self.clear()

    def construct(self):

        self.birthday_paradox()

        tbirthday = Text("生日悖论").shift(LEFT)
        tunivasal_desc = Text("通用哈希").next_to(tbirthday, LEFT, buff=0.9)
        plus = MathTex("+").next_to(tbirthday, LEFT, buff=0.3)
        equal = MathTex("=").next_to(tbirthday, RIGHT, buff=0.3)

        tperfect_hash = Text("完美哈希(perfect hashing)").next_to(equal, RIGHT, buff=0.3)

        tperfect_hash1 = Text("0碰撞").set_color(OBJ_A).next_to(tperfect_hash, RIGHT)
        tperfect_hash0 = Text("O(n)空间").set_color(WORD_A).next_to(tperfect_hash1, UP)
        tperfect_hash2 = Text("O(1)查找").set_color(WORD_B).next_to(tperfect_hash1,DOWN)

        gtperfect_hash = VGroup(
            tperfect_hash0,
            tperfect_hash1,
            tperfect_hash2,
        )

        bperfect_desc = Brace(gtperfect_hash, LEFT)
        perfect_hash_desc = VGroup(bperfect_desc, gtperfect_hash)

        # 这就是著名的生日悖论
        self.play(Create(tbirthday))
        # 而我们上一次提到的通用哈希, 
        self.play(Create(tunivasal_desc))
        # 在拥有了生日悖论的理论基础后, 
        self.play(Create(plus))
        # 就有了这个叫做完美哈希的算法
        self.play(Create(equal))
        self.play(Create(tperfect_hash))

        self.play(FadeOut(tbirthday),
                    FadeOut(tunivasal_desc),
                    FadeOut(plus),
                    FadeOut(equal),)
        self.play(tperfect_hash.animate.shift(LEFT*5))
        
        perfect_hash_desc.next_to(tperfect_hash, RIGHT, buff=0.5)

        # 完美哈希, 顾名思义, 就是完美的, 哈希算法, 它的特点是:
        # 1. 碰撞概率无限趋近于0
        # 2. 空间复杂度为 O(n)
        # 3. 时间复杂度为 O(1)
        self.play(FadeIn(bperfect_desc))
        self.play(FadeIn(tperfect_hash0))
        self.play(FadeIn(tperfect_hash1))
        self.play(FadeIn(tperfect_hash2))

        self.play(FadeOut(perfect_hash_desc),
                  FadeOut(tperfect_hash)) #perfect_hash_desc.animate.shift(UP*2.5))

        ### 完美哈希的实现

        # 其实我们再重新看生日悖论. 可以看到它和我们的哈希算法也是有共通之处的.
        # 我们来看看生日悖论的描述:
        # 在一个班级, 有23个人, 他们中有两个人同一天的生日的概率是50.7%
        # 也就是说, 23 个人, 它们被存储在 365 个位置当中, 有两个人存储在同一个位置的概率是50.7%
        tbirthday_desc = Text("在一个班级, 有 23 个人, 他们中有两个人 365 天的同一天的生日的概率是50.7%").scale(0.5)
        self.play(Create(tbirthday_desc))
        # 再抽象一点, n 个元素, 映射到 约等于 n 平方的位置当中, 存在碰撞的概率为 50.7%
        self.wait()
        self.play(tbirthday_desc.animate.shift(UP*1.5))
        tbirthday_desc2 = Text("n 个(人)元素, 映射到 约等于 n 平方的(生日)位置当中, 存!在!碰!撞!的概率约为 50%").scale(0.5)
        ttot = Arrow(start=tbirthday_desc.get_bottom(), end=tbirthday_desc2.get_top(), buff=0.1)
        self.play(GrowArrow(ttot))
        self.play(Create(tbirthday_desc2))
        # 即然是完美哈希,  一半的存在碰撞的可能性对于我们来说, 显然是不够的. 
        # 我们要做到更优秀, 让它无限接近于零. 
        self.wait()

        self.play(
            FadeOut(ttot),
            FadeOut(tbirthday_desc),
            FadeOut(tbirthday_desc2),
        )

        # 接下来, 我们来看, 完美哈希的具体实现.
        self.play(FadeIn(ghash_u_to_m))

        #self.play(FadeOut(gworld_to_class), FadeOut(tbirthday_desc))
        self.play(m.animate.become(perfect_m))
        self.play(hash_u_to_m.animate.become(hash_u_to_perfectm))

        # 我们有 U 个元素, 我们要把这 U 个元素映射到一个数组 m 当中. 
        # 而这里, 我们的 m 个位置, 需要和 U 的大小相同.
        ukeys = VGroup()
        factor = -1.5
        for i in range(9):
            ukeys.add(Circle(radius=0.02, color=BLUE).move_to(m).shift(UP * factor))
            factor += 0.4

        self.play(FadeIn(ukeys))


        l2_cycle = Circle(radius=0.08, color=BLUE).move_to(m).shift(UP * factor)
        l2 = [[[l2_cycle.copy()],[l2_cycle.copy()],[l2_cycle.copy()],],
              [[l2_cycle.copy()],[l2_cycle.copy()],[l2_cycle.copy()],[l2_cycle.copy()],[l2_cycle.copy()],[l2_cycle.copy()],],
              [[l2_cycle.copy()]]]
        ukeys_index = [7,5,2]

        l2_table = VGroup()
        for i in range(3):
             t = MobjectTable(
                l2[i],
                include_outer_lines=True,
             ).set_stroke(OBJ_C).scale(0.2).next_to(hash_u_to_m, RIGHT, buff=3).shift(UP*(1.5-2*i))

             for row in t.get_rows():
                for cell in row:
                    cell.set_opacity(0)

             pointer = CurvedArrow(start_point=ukeys[ukeys_index[i]].get_center(),end_point=t.get_left())
             t1 = VGroup(t,pointer)
             l2_table.add(t1)

        # 紧接着, 我们将使用二极哈希的方法, 将这个 m 的大小, 分成 l1, l2, l3 等等, 多个部分.

        self.play(FadeIn(l2_table[0]))
        self.wait()
        self.play(FadeIn(l2_table[1]))
        self.wait()
        self.play(FadeIn(l2_table[2]))
        self.wait()

        # 这样的情况下, 每个二极哈希表的大小都不会相同.
        # 有的表可能会为0 
        self.play(Indicate(l2_table[2]))

        bl1 = Brace(l2_table[0][0], RIGHT)
        btl1 = MathTex(r"l1^2").next_to(bl1, RIGHT, buff=0.1)

        bl2 = Brace(l2_table[1][0], RIGHT)
        btl2 = MathTex(r"l2^2").next_to(bl2, RIGHT, buff=0.1)

        bl3 = Brace(l2_table[2][0], RIGHT)
        btl3 = MathTex(r"l3^2").next_to(bl3, RIGHT, buff=0.1)

        # 当我们在创建这个哈希表的时候, 有三个细节需要注意: 
        # 细节一就是, 我们的二极哈希表的大小, 不是 l1, l2, l3 本身的大小. 而是它们的平方. 为什么? 理论依据就是, 生日悖论.
        self.play(FadeIn(bl1), FadeIn(btl1))
        self.play(FadeIn(bl2), FadeIn(btl2))
        self.play(FadeIn(bl3), FadeIn(btl3))

        # 细节二, 每个二极表我们都将重新从通用哈希中选择哈希函数, 这可以保证每个位置的碰撞概率一致, 且为 1/l1.
        f1 = MathTex("((a_1 \cdot k + b_1)\mod p) \mod m").scale(0.4).next_to(btl1, RIGHT, buff=0.1)
        f1_prime = MathTex("((a_1` \cdot k + b_1`)\mod p) \mod m").scale(0.4).next_to(f1, DOWN, buff=0.1)
        f2 = MathTex("((a_2 \cdot k + b_2)\mod p) \mod m").scale(0.4).next_to(btl2, RIGHT, buff=0.1)
        f3 = MathTex("((a_3 \cdot k + b_3)\mod p) \mod m").scale(0.4).next_to(btl3, RIGHT, buff=0.1)

        self.play(FadeIn(f1))
        self.play(FadeIn(f3))

        # 细节三, 当我们从通用哈希函数选取的函数发生了碰撞,我们将重新从通用哈希函数中随机再选择一个.
        self.play(FadeIn(f1_prime))

        # 接下来, 我们就用可视化 + 形式化的方法来证明这一点. 
        #self.clear_obj_expect(l2_table[2][0])
        self.clear()

        # 这个时候, 有人就说了, 你说构成就构成? 怎么证明 O(1) 的时间复杂度, O(n) 的空间复杂度, 以及 0 碰撞的概率呢?
        self.play(FadeIn(perfect_hash_desc),
                  FadeIn(tperfect_hash))
        self.wait()
        self.play(FadeOut(perfect_hash_desc),
                  FadeOut(tperfect_hash))


        ### 形式化证明 ###
        # 第一点, 接近 0 碰撞. 我们拿 table2 来看看效果.
        self.play(
            l2_table[1][0].animate.scale(2).align_on_border(LEFT),
        )
        bl2 = Brace(l2_table[1][0], RIGHT)
        btl2.next_to(bl2, RIGHT, buff=0.1),
        self.play(
            FadeIn(bl2),
            FadeIn(btl2),
        )


        # 首先, 我们选择的哈希函数是通用哈希; 
        # 所以当我们在 l1 当中的两个元素的碰撞概率可以表示为 H(l2_1) == H(l2_2) == 1/l2^2的概率
        self.play(
            l2_table[1][0].get_rows()[1][0].animate.set_opacity(1)
        )
        hash_l2_1 = MathTex(r"H(l2_1) = \frac{1}{l2^2}").scale(0.4).next_to(l2_table[1][0].get_rows()[1][0], RIGHT, buff=1.5)
        self.play(FadeIn(hash_l2_1))

        self.play(
            l2_table[1][0].get_rows()[5][0].animate.set_opacity(1)
        )
        hash_l2_2 = MathTex(r"H(l2_2) = \frac{1}{l2^2}").scale(0.4).next_to(hash_l2_1, RIGHT, buff=1.5)
        self.play(FadeIn(hash_l2_2))

        hash_l2 = VGroup(hash_l2_1, hash_l2_2)

        
        # 第三节, 空间大小.
                # 我们回到这个哈希表本身,  有人就会问, 你这样, 每一次都给 l1, l2, l3 进行平方, 那这样, 如果我要存储的大小是 1m, 岂不是要用掉 1m 平方的空间. 这是不可接受的呀.
                # 我们也同意这一点, 完美哈希如果说空间占用率达到如此之高, 也就称不上完美了. 
                # 所以, 实际上, 我们可以证明的是, 完美哈希的空间占用率, 仍然为 O(n) 

        ### 形式化证明 ###

        # 完美哈希的基本思想是使用两级哈希表，第一级哈希表将关键字集合分成若干个子集，每个子集对应一个槽，第二级哈希表则为每个子集构造一个没有冲突的哈希函数。
        # 这样，查找一个关键字时，只需要两次哈希计算和两次内存访问，即可保证在最坏情况下为 O (1) 的时间复杂度。

        #关于完美哈希的碰撞概率为 0 的证明，可以参考以下的定理和证明1：

        #定理：如果 N 个球被放入 M=N^2 个箱子中，那么没有箱子装有多余一个球的概率大于 1/2。

        #证明：显然，第 i, j 个球 (i, j \leq N) 发生冲突的概率为 1/M。故存在一对球发生冲突的概率为 \frac {C_N^2} {M}=\frac {N (N-1)} {2N^2}<\frac {1} {2}\\

        #关于完美哈希的空间复杂度为 O (n) 的证明，可以参考以下的定理和证明2：

        #定理：如果将 N 项放入包含 N 个箱子的主哈希表中，那么二级哈希表的总大小的期望值最多为 2N。

        #证明：与定理 5.2 的证明思路相似。成对冲突的期望数最多为 N (N-1)/2N。设散列到每一个“箱子”中元素为 b_i, 那么每个箱子中二级哈希表的大小为 b_i^2。每一个箱子中的成对冲突的期望数最多为 b_i (b_i-1)/2，记为 c_i。那么此时总的空位为 M=\sum b_i^2=2\sum c_i+\sum b_i\\ 成对冲突的期望数最多为 N (N-1)/2N，那么有 \sum c_i \le \frac {N-1} {2}\\ 故 M<2\cdot\frac {N-1} {2}+N<2N\\


        self.wait()
