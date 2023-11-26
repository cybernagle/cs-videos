from manim import *

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

class UnivasalHash(Scene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND

    def construct(self):

        # 首先定义 hashing
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

        univasal = Rectangle(height=2, width=0.4, color=OBJ_A, fill_opacity=0.5).next_to(hash_func, LEFT, buff=0.05)
        tunivasal = Text("U", color=WORD_A).scale(0.5).move_to(univasal)

        m = Rectangle(height=0.6, width=0.4, color=OBJ_B, fill_opacity=0.5).next_to(hash_func, RIGHT, buff=0.05)
        tm = Text("M", color=WORD_B).scale(0.5).move_to(m)

        self.play(FadeIn(univasal), FadeIn(tunivasal))
        self.play(FadeIn(hash_func), FadeIn(thash_func))
        self.play(FadeIn(m), FadeIn(tm))

        # 有了 hasing funciton 之后
        # 我们开始定义说, univasal hasing 是什么?
        # 定一个 prime  p
        # `((a*k + b) mod p ) mod m`
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
        # 选择了 prime 了之后, 我们需要看一看 prime number 在 执行 (a*k + b) mod p 的时候, 会碰撞吗?
        # a*x1 + b == a*x2 + b
        # a(x1 - x2) = 0 mod p
        # x != x2, 而 p 不能被任何数整除, 所以我们可以说. x1, x2 hash 后不会碰撞.


        # sec 3
        # 在经过 hash function (a*k + b) mod p 以后.
        # 我们来看看 (a*k + b) mod p ,因为它是从一个大的范围进入一个小的范围.
        # 所以碰撞是必然的.
        # 即然我们在选择这个数, 所以我们能够做到的就是, 减少碰撞的概率.
        # 那么, 什么情况下会发生碰撞呢?碰撞的概率会有多少呢?
        # 假设我们 ku = (a*k+b) mod p 
        # 那么与 ku mod n 的情况下, 能够与 ku 产生碰撞的就是: ku + n , ku + 2n , ku -n ...
        # 我们来看一张图
        # 11*11 matrix
        
        # 我们接下来要证明的是: ((a*k+b) mod p) mod m 
        # prob(h(a,b)(x1) == h(a,b)(x2)) <= ([p/m] - 1) / (p-1) <= ((p-1)/m) / (p-1) = 1/m

        # 最后, prime number 以及 hasing funcion 如何证明说可以让碰撞的几率变成 1/n

        self.wait()
