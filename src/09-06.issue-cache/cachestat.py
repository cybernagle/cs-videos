from manim import *
import pickle
import random

class CacheStat(Scene):
    def construct(self):
        # 与人员沟通, 发现最近请求的数量并没有明显的增加.
        # 然后通过 df 命令查看文件系统的占用空间, 发现仅仅是 30%

        thirty = Text("30%").scale(2)

        self.play(FadeIn(thirty))
        self.play(FadeOut(thirty))

        # emmmm(背景音即可)
        # 难不成是 cache ? 
        # 我们来看看 cache 的使用情况.
        # 使用 cachestat.py , 获取 cache 的 hit, 发现其数值是 91%, 并不低. cache 的size 是500mi.
        cachestat = Text("python cachestat.py").scale(2)
        self.play(FadeIn(cachestat))
        self.play(FadeOut(cachestat))
        # 我们在另外一台机器取出一个进行对比, 发现其命中率是 97%. 而 cache 的 size 竟然是 300mi


        text = """
        HITS    MISSES  DIRTIES HITRATIO   BUFFERS_MB  CACHED_MB
        13804        0       67   91.00%          500        500
        13829        0       33   91.00%          500        500
        4708         0       29   91.00%          500        500
        """
        #r1 = Text(text).scale(0.3)
        vv = VGroup()
        r1 = ImageMobject("resource/91.png").scale(2)
        self.play(FadeIn(r1))
        self.play(r1.animate.shift(UP*1.5))

        text2 = """
        HITS    MISSES  DIRTIES HITRATIO   BUFFERS_MB  CACHED_MB
        3423         0       28   97.00%          500        300
        13646        0       141  97.00%          500        300
        23           0       91   97.00%          500        300
        """

        r2 = ImageMobject("resource/97.png").scale(2)
        r2.shift(DOWN*1.5)
        self.play(FadeIn(r2))

        r1r = Rectangle(width=1,height=1.2).move_to(r1)
        r2r = Rectangle(width=1,height=1.2).move_to(r2)
        vv.add(r1r, r2r)

        self.play(FadeIn(vv))
        self.wait()

        self.play(
            vv.animate.shift(RIGHT*2.4)
        )

        self.wait()
        self.play(
            FadeOut(r1),
            FadeOut(r2),
            FadeOut(vv)
        )

        # 当文件系统访问磁盘的时候, 为了因为磁盘的访问效率相对于内存更低. 所以文件系统会在内存当中使用cache.(manim 文件系统变化的动画)

        # 基本上可以断定就是 cache 的问题了.
        # 那么我们继续对比, 发现该机器某个该死的进程, 一直在消耗新的内存.而这部分内存, 消耗掉了本来文件系统cache可以占用的空间.
        # 从而导致 cache 命中率下降, 进而导致了 io 利用率的升高.

        # 于是 # kill $(pidof mihayo)
        self.play(FadeIn(Text("kill $(pidof mihayo)")))
    

        # 我们的问题消失了.

        self.wait()
