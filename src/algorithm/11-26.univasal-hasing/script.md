# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic
        # 世界上任何一种类型的对象, 我们将其定义为 U 集合.
        # hash 的作用, 是将这个集合的内容
        # 映射到一个更小的区间, 以便于程序使用
        # 取在 U 集合当中的任意一个对象
        # 执行 mod p, 将其映射到 p 的范围内.
        # 然后再执行 mod m, 将其映射到 m 的范围内.
        # 接下来的事情会是: 
        # 将 k * a 并加上 b
        # 其中 a 和 b 都在质数当中. a != 0
        # 这样, 我们就可以得到多个hash 函数.
        # 譬如说, 
        # 1乘以 k + 0 mod p 再 mod m
        # 2乘以 k + 1 mod p 再 mod m
        # 3 乘以 k + 2 mod p 再 mod m
        # 以此类推
        # 直到 (p-1)乘以k+(p-1) mod p 再 mod m
        # 如此,我们就能够得出这些 hash 函数的定义
        # H p, m = h(a,b) 其中 a 属于 p 的非零整数集, 而 b 属于 p 的整数集合.
        # 而它们的数量为: p*(p-1)
        # 我们的 univasal hashing 函数,就是每次随机的从中抽取一个函数进行 hash.
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
        # 在选择了 prime 了之后, 我们需要看一看 prime number 在 执行 (a*k + b) mod p 的时候, 
        # 会碰撞吗?
        # 答案是不会!
        # 我们
        # 首先我们假设他们会碰撞, 那么就会有
        # a*x1 + b == a*x2 + b 
        # a(x1 - x2) = 0 mod p
        # 从而我们可以得出
        #而我们知道的是 x1 != x2, 而 p 是质数, 所以不可能存在 0 mod p, 所以我们可以说. x1, x2 hash 后不会碰撞.
        # use manim create a table with 7 rows and 7 columns
            #include_background_rectangle=True,
            #background_rectangle_color=BLUE,
        # 换另外一个角度来看,
        # 如果我们把一个质数5范围内所有的数都 按照 (key * a)mod b 的方法 hash 一遍, 我们得出下面的表格.
        # 我们说横轴是 P
        # 纵轴是 A
        # 也就意味着, key * a mod p 的结果, 是不会为 0 的. 或者说, 没有与 p 整除的数(废话)
        # 而且, 可以看到我们的 mod 的结果分布, 是均匀的. 分布均匀的意思是, 它们在横轴以及纵轴上, 都不会相交.
        #self.play(Indicate(fivebyfive.get_cell((1,1))))
        # 我们再来看一个反例, prime number 为 6 的情况
        # 当我们的 a 为 3 的时候
        # 可以看到 key = 1, 3, 5 的时候, hash 的结果都是 3 
        # 从上面的例子我们可以看到, 质数作为 模数,
        # 有以下几个作用
        # 1. hash 在 mod 到 p 的时候, 是不会发生碰撞的.
        # 2. hash 的分布比较均匀, 换句话说, 保证每个位置的概率都是一样的.
        # sec 3
        #self.play(FadeIn(hash_func2),FadeIn(thash2))
        #self.play(FadeIn(ghashing))
        # 在经过 hash function (a*k + b) mod p 以后.
        # 我们来看看 p mod m ,
        #因为它是从一个大的范围
        # 进入一个小的范围.
        # 所以碰撞是必然的.
        # 那么, 什么情况下会发生碰撞呢?碰撞的概率会有多少呢?
        # 假设我们 ku = (a*k+b) mod p 
        # 那么与 ku mod n 的情况下, 能够与 ku 产生碰撞的就是: ku + n , ku + 2n , ku -n ...
        # generate a line with thin stroke
        # 产生碰撞的数量就会是: p/m - 1
        # 所以发生碰撞的概率我们可以表示为
        # (p/m - 1) / (p-1)
        # 而整个
        # p/m 
        # 我们接下来要证明的是: ((a*k+b) mod p) mod m 
        # prob(h(a,b)(x1) == h(a,b)(x2)) <= ([p/m] - 1) / (p-1) <= ((p-1)/m) / (p-1) = 1/m
