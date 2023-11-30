from manim import *

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

"""
class 1
"""
# 首先定义什么是 hashing function?
hash_func = Polygon(
    [-0.5, -1, 0],  # 左下角点
    [-0.5, 1, 0],   # 左上角点
    [0.5, 0.3, 0],    # 右上角点
    [0.5, -0.3, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5
)

hash_func.set_stroke(color=SHADOW, opacity=0)
thash_func = Text("Hash", color=SHADOW).scale(0.5).move_to(hash_func)
ghash = VGroup(hash_func, thash_func)

univasal = Rectangle(height=2, width=0.4, color=OBJ_A, fill_opacity=0.5).next_to(hash_func, LEFT, buff=0.05)
tunivasal = Text("U", color=WORD_A).scale(0.5).move_to(univasal)
ugroup = VGroup(univasal, tunivasal)

ukeys = VGroup()
factor = -0.8
for i in range(9):
    ukeys.add(Circle(radius=0.02, color=BLUE).move_to(univasal).shift(UP * factor))
    factor += 0.2

m = Rectangle(height=0.6, width=0.4, color=OBJ_B, fill_opacity=0.5).next_to(hash_func, RIGHT, buff=0.05)
tm = Text("M", color=WORD_B).scale(0.5).move_to(m)
gm = VGroup(m, tm)

hash_func1 = Polygon(
    [-0.5, -1.3, 0],  # 左下角点
    [-0.5, 1.3, 0],   # 左上角点
    [0.5, 0.3, 0],    # 右上角点
    [0.5, -0.3, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5,
    stroke_opacity=0
)
# 我们定义一个大于U集合的prime p
prime = Rectangle(height=2.6, width=0.4, color=OBJ_C, fill_opacity=0.5).next_to(univasal, UP, buff=0.05)
tprime = Text("P", color=OBJ_C).scale(0.5).move_to(prime)
gprime = VGroup(prime, tprime)

hash_func2 = Polygon(
    [-2.5, -1, 0],  # 左下角点
    [-2.5, 1, 0],   # 左上角点
    [-1, 1.3, 0],    # 右上角点
    [-1, -1.3, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5,
    stroke_opacity=0
)

#ghashing = VGroup(ugroup, gm, hash_func1, hash_func2,gprime, thash_func)

"""
class 2
"""
matrix5 = [[(x*y)%5 for x in range(0, 5)] for y in range(0, 5)]
fivebyfive = IntegerTable(
    matrix5,
    row_labels=[ Text(str(i)) for i in range(0, 5)],
    col_labels=[ Text(str(i)) for i in range(0, 5)],
    include_outer_lines=True,
    #include_background_rectangle=True,
    #background_rectangle_color=BLUE,
).scale(0.5).set_column_colors(BLUE).set_row_colors(BLUE)

# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic
class UnivasalHash(Scene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND

    def construct(self):

        # 世界上任何一种类型的对象, 我们将其定义为 U 集合.
        self.play(FadeIn(univasal))#, FadeIn(tunivasal))
        self.add(ukeys)
        self.wait()
        self.remove(ukeys)
        self.play(FadeIn(tunivasal))
        # hash 的作用, 是将这个集合的内容
        self.play(FadeIn(hash_func), FadeIn(thash_func))
        # 映射到一个更小的区间, 以便于程序使用
        self.play(FadeIn(m), FadeIn(tm))

        self.play(FadeIn(prime), FadeIn(tprime))

        self.play(
            gprime.animate.next_to(ghash, LEFT, buff=0.05),
            ugroup.animate.shift(LEFT*2)
        )

        self.play(
            hash_func.animate.become(hash_func1)
        )

        thash2 = thash_func.copy().move_to(hash_func2)
        self.play(FadeIn(hash_func2),FadeIn(thash2))

        # 取在 U 集合当中的任意一个对象
        key1 = Circle(radius=0.02, color=BLUE).move_to(univasal).shift(UP*0.5)
        tkey1 = Tex("k", color=BLUE).scale(0.5).next_to(key1, LEFT)
        pkey1 = Circle(radius=0.02, color=BLUE).move_to(prime).shift(UP*0.7)
        mkey1 = Circle(radius=0.02, color=BLUE).move_to(m).shift(UP*0.2)
        utop = Arrow(
            start=key1,
            end=pkey1,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.02
        )
        ptom = Arrow(
            start=pkey1,
            end=mkey1,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.02
        )
        pformular0 = MathTex("(k\mod p) ").scale(0.8).next_to(m, RIGHT)
        pformular1 = MathTex("\mod m").scale(0.8).next_to(pformular0, RIGHT, buff=0)

        formular = MathTex("((a \cdot k + b)\mod p) \mod m").scale(0.8).next_to(m)
        formulardetail = MathTex("a \cdot k + b").scale(0.8).next_to(pformular0, DOWN)
        
        ta = MathTex("a = \\{1, 2, 3, ..., p-1\\}").scale(0.5).next_to(formular, DOWN)
        tb = MathTex("b = \\{0, 1, 2, ..., p-1\\}").scale(0.5).next_to(ta, DOWN)

        f1 = MathTex("((1 \cdot k + 0)\mod p) \mod m").scale(0.8).next_to(ORIGIN, RIGHT).shift(UP)
        f2 = MathTex("((2 \cdot k + 1)\mod p) \mod m").scale(0.8).next_to(f1, DOWN)
        f3 = MathTex("((3 \cdot k + 2)\mod p) \mod m").scale(0.8).next_to(f2, DOWN)
        f4 = MathTex("...").scale(0.8).next_to(f3, DOWN)
        f5 = MathTex("(((p-1) \cdot k + (p-1))\mod p) \mod m").scale(0.8).next_to(f4,DOWN)
        gformulars = VGroup(f1, f2, f3, f4, f5)

        hashformular = MathTex("H_{p,m} = \\{h_{ab} : a \\in Z_p \\text{ and } b \\in Z_p\\}", color=WORD_A).scale(0.8).next_to(gformulars, DOWN)
        hashformular_count = MathTex("count(H_{p,m}) = p\cdot (p-1)", color=WORD_A).scale(0.8).next_to(hashformular, DOWN)

        gmapping = VGroup(
            key1,  tkey1, pkey1, mkey1,utop, ptom, ugroup, ghash,gm, hash_func, hash_func1, hash_func2,
            thash2, thash_func,gprime
        )

        # 执行 mod p, 将其映射到 p 的范围内.
        self.play(FadeIn(key1))
        self.play(FadeIn(tkey1))
        self.play(GrowArrow(utop))
        self.play(FadeIn(pkey1))
        self.wait()
        self.play(FadeIn(pformular0))

        # 然后再执行 mod m, 将其映射到 m 的范围内.
        self.play(GrowArrow(ptom))
        self.play(FadeIn(mkey1))
        self.wait()
        self.play(FadeIn(pformular1))


        # 接下来的事情会是: 
        # 将 k * a 并加上 b
        self.play(FadeIn(formulardetail))
        self.play(
            FadeOut(formulardetail),
            FadeOut(pformular0),
            pformular1.animate.become(formular)
        )

        # 其中 a 和 b 都在质数当中. a != 0
        self.play(
            FadeIn(ta),
            FadeIn(tb),
        )
        self.play(
            FadeOut(ta),
            FadeOut(tb),
        )

        # 这样, 我们就可以得到多个hash 函数.
        # 譬如说, 
        self.play(gmapping.animate.shift(LEFT*3))
        # 1乘以 k + 0 mod p 再 mod m
        # 2乘以 k + 1 mod p 再 mod m
        # 3 乘以 k + 2 mod p 再 mod m
        # 以此类推
        # 直到 (p-1)乘以k+(p-1) mod p 再 mod m
        self.play(FadeIn(f1))
        self.play(FadeIn(f2))
        self.play(FadeOut(pformular1))
        self.play(FadeIn(f3))
        self.play(FadeIn(f4))
        self.play(FadeIn(f5))

        self.wait()
        # 如此,我们就能够得出这些 hash 函数的定义
        # H p, m = h(a,b) 其中 a 属于 p 的非零整数集, 而 b 属于 p 的整数集合.
        self.play(
            FadeIn(hashformular),
        )
        # 而它们的数量为: p*(p-1)
        self.play(
            FadeIn(hashformular_count),
        )

        self.play(
            FadeOut(hashformular),
            FadeOut(hashformular_count),
            FadeOut(gformulars)
        )
        self.play(
            gmapping.animate.move_to(ORIGIN)
        )
        
        # 我们的 univasal hashing 函数,就是每次随机的从中抽取一个函数进行 hash.


        #self.play(
        #    FadeIn(formular),
        #    FadeIn(ta),
        #    FadeIn(tb),
        #)
        # `((a x k + b) mod p ) mod m`
        # 其中 a = { 1, 2, 3 ... p-1} 
        # 其中 b = { 0, 1, 2, 3 ... p-1} 
        # 所以上面的 hash function 就存在有
        # H = {h(a,b)}, 其中 a = { 1, 2, 3 ... p-1} , b = { 0, 1, 2, 3 ... p-1}
        # count(H) = p(p-1)

        # 首先回答的第一个问题会是, 为什么中间是一个 prime number ?
        # 在我们的 hash function 当中, 会涉及到两个 point, 第一个是 a*k 然后是 +b
        # 涉及到 + 和 * 两个运算.
        # 其中乘法, 是对称的, 也就是说 a*k 或者 k*a , +b, 或者 b+ 都是不影响这个公式的结果的.
        # 质数的性质是: 不能被除了 1 以外所有的数整除.

        # prime number 第一个性质: 除了 0 以外的数, 在进行对 p 取余的时候,都会有一个 1.
        # 这保证了, 我们在执行 hash function 的时候, 是可逆的. 我给你执行了一个 hash, 你肯定要通过 hash function 再返回回来.
        # 否则也就白 hash 了

        # 而非质数则不然, 
        # 我们可以看一个反面例子 p == 6
        # F6

        # sec 2
        # 在选择了 prime 了之后, 我们需要看一看 prime number 在 执行 (a*k + b) mod p 的时候, 

        self.play(
            FadeOut(ptom)
        )
        # 会碰撞吗?
        key2 = key1.copy().next_to(key1, DOWN)
        utop2 = Arrow(
            start=key2,
            end=pkey1,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.02
        )
        self.play(FadeIn(key2))
        self.play(GrowArrow(utop2))

        # 答案是不会!
        # 我们
        # 首先我们假设他们会碰撞, 那么就会有
        # a*x1 + b == a*x2 + b 
        akey = MathTex("a \cdot key_1 + b = a \cdot key_2 + b").scale(0.8).next_to(ORIGIN, RIGHT).shift(UP*2)
        self.play(FadeIn(akey))
        # a(x1 - x2) = 0 mod p
        # 从而我们可以得出
        bkey = MathTex("a \cdot (key_1 - key_2) = 0 \mod p").scale(0.8).next_to(ORIGIN, RIGHT).shift(UP*1.5)
        self.play(FadeIn(bkey))
        #而我们知道的是 x1 != x2, 而 p 是质数, 所以不可能存在 0 mod p, 所以我们可以说. x1, x2 hash 后不会碰撞.

        


        self.wait()

class WhyOneOverM(Scene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND
    def construct(self):
        positions5 = [[(i+2, j+2) for i , row in enumerate(matrix5) for j, val in enumerate(row) if val==num] for num in range(1,5)]
        matrix6 = [[(x*y)%6 for x in range(0, 6)] for y in range(0, 6)]
        positions6 = [[(i+2, j+2) for i , row in enumerate(matrix6) for j, val in enumerate(row) if val==num] for num in range(1,6)]

        # use manim create a table with 7 rows and 7 columns
        fivebyfive.get_columns()[0].set_fill(WORD_B, opacity=0.5)
        fivebyfive.get_rows()[0].set_fill(WORD_B, opacity=0.5)

        sixbysix = IntegerTable(
            matrix6,
            row_labels=[ Text(str(i)) for i in range(0, 6)],
            col_labels=[ Text(str(i)) for i in range(0, 6)],
            include_outer_lines=True,
            #include_background_rectangle=True,
            #background_rectangle_color=BLUE,
        ).scale(0.5)


        # 换另外一个角度来看,
        # 如果我们把一个质数5范围内所有的数都 按照 (key * a)mod b 的方法 hash 一遍, 我们得出下面的表格.
        self.play(FadeIn(fivebyfive))

        # 我们说横轴是 P
        self.play(Indicate(fivebyfive.get_rows()[0]))
        # 纵轴是 A
        self.play(Indicate(fivebyfive.get_columns()[0]))
        # 也就意味着, key * a mod p 的结果, 是不会为 0 的. 或者说, 没有与 p 整除的数(废话)
        # 而且, 可以看到我们的 mod 的结果分布, 是均匀的. 分布均匀的意思是, 它们在横轴以及纵轴上, 都不会相交.
        #self.play(Indicate(fivebyfive.get_cell((1,1))))

        positions = []
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]

        index = 0
        for i in positions5:
            color=colors[index]
            for j in i:
                fivebyfive.add_highlighted_cell(j, color=color)
            index += 1


        surrand_columnfive = SurroundingRectangle(
            fivebyfive.get_columns()[2],
            color=RED,
            buff=0.05
        )
        
        self.play(Wiggle(fivebyfive))
        self.play(FadeIn(surrand_columnfive))
        self.wait(2)
        self.play(
            FadeOut(fivebyfive),
            FadeOut(surrand_columnfive)
        )

        # 我们再来看一个反例, prime number 为 6 的情况
        self.play(FadeIn(sixbysix))

        index = 0
        for i in positions6:
            color=colors[index]
            for j in i:
                sixbysix.add_highlighted_cell(j, color=color)
            index += 1

        
        gsurranding = VGroup()
        for i in [2,4,6]:
            temp = SurroundingRectangle(
                sixbysix.get_rows()[i],
                color=RED,
                buff=0.05
            )
            key = Text("k={}".format(str(i-1)), color=RED).scale(0.8).next_to(temp, LEFT, buff=1)
            gsurranding.add(temp, key)

        surrand_column = SurroundingRectangle(
            sixbysix.get_columns()[4],
            color=RED,
            buff=0.05
        )
        # 当我们的 a 为 3 的时候
        a1 = Text("a=3", color=WORD_A).scale(0.8).next_to(surrand_column,UP)
        self.play(
            FadeIn(surrand_column),
            FadeIn(a1)
        )
        self.wait()
        # 可以看到 key = 1, 3, 5 的时候, hash 的结果都是 3 
        self.play(
            FadeIn(gsurranding)
        )
        self.wait()
        self.play(
            FadeOut(gsurranding),
            FadeOut(surrand_column),
            FadeOut(a1)
        )
        self.wait()

        gsurrandingsix = VGroup()
        for i in [2,5]:
            temp = SurroundingRectangle(
                sixbysix.get_rows()[i],
                color=RED,
                buff=0.05
            )
            key = Text("k={}".format(str(i-1)), color=RED).scale(0.8).next_to(temp, LEFT, buff=1)
            gsurrandingsix.add(temp,key)
        surrand_columnsix = SurroundingRectangle(
            sixbysix.get_columns()[3],
            color=RED,
            buff=0.05
        )
        a2 = Text("a=2", color=WORD_A).scale(0.8).next_to(surrand_columnsix, UP)
        self.play(
            FadeIn(surrand_columnsix),
            FadeIn(a2)
        )
        self.wait()
        self.play(
            FadeIn(gsurrandingsix)
        )
        self.wait()
        self.play(
            FadeOut(gsurrandingsix),
            FadeOut(surrand_columnsix),
            FadeOut(a2)
        )

        self.wait()

        self.play(FadeOut(sixbysix))

        self.wait()

        # 从上面的例子我们可以看到, 质数作为 模数,
        # 有以下几个作用
        # 1. hash 在 mod 到 p 的时候, 是不会发生碰撞的.
        # 2. hash 的分布比较均匀, 换句话说, 保证每个位置的概率都是一样的.

        uprime = Text("1. hash 在 mod 到 p 的时候, 是不会发生碰撞的.", color=WORD_A).scale(0.8).to_edge(UP).shift(DOWN*2)
        uprime2 = Text("2. hash 的分布比较均匀, 换句话说, 保证每个位置\n    的概率都是一样的.", color=WORD_A).scale(0.8).next_to(uprime, DOWN)
        self.play(Create(uprime))
        self.play(Create(uprime2))

        self.play(
            FadeOut(uprime),
            FadeOut(uprime2),
        )
        # sec 3
        gprime.next_to(ghash, LEFT, buff=0.05),
        ugroup.shift(LEFT*2)

        thash2 = thash_func.copy().move_to(hash_func2)
        #self.play(FadeIn(hash_func2),FadeIn(thash2))

        ghashing = VGroup(ugroup, gm, hash_func1, hash_func2,gprime, thash_func )
        ghashing.add(thash2)
        #self.play(FadeIn(ghashing))
        hash_u_p = VGroup(ugroup, hash_func2, thash2)
        hash_p_m = VGroup(gm, hash_func1, gprime, thash_func)
        self.play(
            FadeIn(hash_u_p),
            FadeIn(hash_p_m),
        )

        self.play(FadeOut(hash_u_p))

        pkey1 = Circle(radius=0.02, color=BLUE).move_to(prime).shift(UP)
        pkey2 = Circle(radius=0.02, color=BLUE).move_to(prime).shift(DOWN*0.3)
        mkey = Circle(radius=0.02, color=BLUE).move_to(m).shift(UP*0.2)

        ptom1 = Arrow(
            start=pkey1,
            end=mkey,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.02
        )
        ptom2 = Arrow(
            start=pkey2,
            end=mkey,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.02
        )

        pformular0 = MathTex("(p\mod m) ").scale(0.8).next_to(m, RIGHT)
        # 在经过 hash function (a*k + b) mod p 以后.
        # 我们来看看 p mod m ,
        self.play(FadeIn(pkey1))
        self.play(FadeIn(pkey2))
        self.play(GrowArrow(ptom1))
        self.play(FadeIn(mkey))
        self.play(FadeIn(pformular0))

        #因为它是从一个大的范围
        self.play(Indicate(prime))
        # 进入一个小的范围.
        self.play(Indicate(m))

        # 所以碰撞是必然的.
        self.play(GrowArrow(ptom2))
        self.wait()
        # 那么, 什么情况下会发生碰撞呢?碰撞的概率会有多少呢?
        self.play(FadeOut(ptom2), FadeOut(pkey2))
        ku = MathTex("u").scale(0.3).next_to(pkey1, LEFT)

        pkeys = VGroup()
        factor = 1
        for i in range(7):
            pkeys.add(Circle(radius=0.02, color=BLUE).next_to(pkey1,DOWN*factor))
            factor += 1

        # 假设我们 ku = (a*k+b) mod p 
        self.play(FadeIn(ku))
        # 那么与 ku mod n 的情况下, 能够与 ku 产生碰撞的就是: ku + n , ku + 2n , ku -n ...
        self.play(Indicate(pformular0))
        poverm = VGroup()
        for i in range(len(pkeys)):
            self.play(FadeIn(pkeys[i]), run_time=0.3)
            index = "u + {index} \cdot m".format(index=i+1)
            text = MathTex(index).scale(0.5).next_to(pkeys[i], LEFT)
            poverm.add(text)
            self.play(FadeIn(text),run_time=0.3)

        surrand_poverm = SurroundingRectangle(
            poverm,
            color=RED,
            buff=0.05
        )

        fpoverm = MathTex("p/m -1").scale(0.5).next_to(surrand_poverm, LEFT).shift(UP)
        self.play(FadeIn(surrand_poverm))
        self.play(FadeIn(fpoverm))

        # generate a line with thin stroke

        over = Line(start=fpoverm.get_left(), end=fpoverm.get_right(),).set_stroke(width=1).next_to(fpoverm, DOWN, buff=0)
        fp = MathTex("p-1").scale(0.5).next_to(over, DOWN, buff=0)

        self.play(
            FadeIn(over),
            FadeIn(fp)
        )

        fpoverm2 = MathTex("\\frac{(p-1)/m}{p-1}").scale(0.5).next_to(fp, DOWN, buff=0.5)
        self.play(FadeIn(fpoverm2))

        fpoverm3 = MathTex("\\frac{1}{m}").scale(0.5).next_to(fpoverm2, DOWN, buff=0.5)
        self.play(FadeIn(fpoverm3))

        self.mobjects=[fpoverm3]
        self.foreground_mobjects=[fpoverm3]

        self.play(
            fpoverm3.animate.scale(5).move_to(ORIGIN)
        )
        self.remove(fpoverm3)
        
        # 产生碰撞的数量就会是: p/m - 1
        # 所以发生碰撞的概率我们可以表示为
        # (p/m - 1) / (p-1)
        # 而整个
        # p/m 
        # 我们接下来要证明的是: ((a*k+b) mod p) mod m 
        # prob(h(a,b)(x1) == h(a,b)(x2)) <= ([p/m] - 1) / (p-1) <= ((p-1)/m) / (p-1) = 1/m

        # 接下来我们看一个实际的例子
        p11 = MathTex("p = 11").scale(0.8).to_edge(UP).shift(LEFT)
        m4 = MathTex("m = 4").scale(0.8).next_to(p11, RIGHT)
        # 假设我们选取的质数是 11
        self.play(FadeIn(p11))
        # 然后我们的哈希表的大小 m 是 4
        self.play(FadeIn(m4))
        # 那么, 我们的碰撞情况会是如何呢?
        # 让我们看看 
        # 11*11 matrix
       
        #self.play(ApplyWave(ebye))

        #self.play(FadeIn(ebye))
        #self.play(FadeOut(ebye))
        # 最后, prime number 以及 hasing funcion 如何证明说可以让碰撞的几率变成 1/m
        self.wait()

class Ebye(Scene):
    def construct(self):
        ebye = IntegerTable(
            [[(x)%4 for x in range(0, 11)] for y in range(0, 11)],
            row_labels=[ Text(str(i)) for i in range(0, 11)],
            col_labels=[ Text(str(i)) for i in range(0, 11)],
            include_outer_lines=True,
        ).scale(0.4)

        self.add(ebye)
        # 当 p = 11 的时候, 最多 121 个结果, 需要存放到容量为4的hash表当中.
        # 那么, 这会产生多少冲突呢? 
        for row in ebye.get_rows()[1:]:
            for cell in row[1:]:
                cell.set_opacity(0)

        for row in ebye.get_rows()[1:]:
            for cell in row[1:]:
                #cell.set_opacity(1)
                self.play(FadeIn(cell), run_time=0.5)
 
                #ebye.add_highlighted_cell(j, color=color)

