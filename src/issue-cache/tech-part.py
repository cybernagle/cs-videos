from manim import *
import pickle
import random

class TechPart(Scene):

    def generate_cycle(self, inner_radius=1, outer_radius=1.5,color=GREEN):
        cycle = VGroup()
        for i in range(8):
            a = AnnularSector(inner_radius=inner_radius, outer_radius=outer_radius, angle=44.5 * DEGREES,start_angle=i*45*DEGREES ,color=color)
            cycle.add(a)
        return cycle


    def generate_tree(self):
        vertices = [ 1,2,3,4,5,6,7]
        edges = [
            (1,2), (1,3),(2,4), (2,5), (3, 6),(3,7)
        ]
        layout = {
            1: [0, 0, 0],
            2: [1, -1, 0],
            3: [-1, -1, 0],
            4: [2, -2, 0],
            5: [0.5, -2, 0],
            6: [-2, -2, 0],
            7: [-0.5, -2, 0],
        }

        tree = Graph(vertices, edges,labels=True, label_fill_color=GREEN,layout_scale=2,
                     layout=layout)#.set_color(YELLOW)
        return tree
        

    def generate_disk(self):
        disks = VGroup()
        prev_disk = AnnularSector(inner_radius=0.1, outer_radius=1.14, angle= 2*PI , color=GREEN)

        disks.add(prev_disk)

        disk = VGroup()
        init = 0.1
        for i in range(5):
            inner = init
            outer = init+0.2
            s = self.generate_cycle(inner_radius=inner, outer_radius=outer,color=GREEN)
            disk.add(s)
            s.move_to(disk)
            init+=0.21
        disks.add(disk)

        return disks


    def create_memory(
            self,
            length=30, color=YELLOW, width=1.5, height=0.5,
            x_grid = 1.5, y_grid = 0.5
    ) -> VGroup:
        mem = VGroup()
        width = width
        height = height
        for i in range(length):
            buff = 0

            rect = Rectangle(color=color, fill_opacity=0.5, width=width, height=height,
                             grid_xstep=x_grid, grid_ystep=y_grid)
            rect.next_to(mem, RIGHT, buff=buff)
            mem.add(rect)
        mem.move_to(ORIGIN)
        return mem


    def construct(self):
        ##************ 问题描述

        # 事情是这样的, 今天一上班, 同事就给我发了一条消息如下:
        # 收到很多用户投诉, 进程发生系统卡死的情况.
        # 我们发现是数据库似乎存在问题.
        # 因为我们的 log 里面发现, 数据库当中, 查询超过 1000ms 的请求增加了很多.
        # 而在以前, 这是从来没有发生过的事情.
        # 从监控系统来看, 目前判断是磁盘的原因.

        # 然后他给了我如下的几张监控截图.
        # 截图显示, cpu 基本上稳定在 50% 左右,
        # 内存的利用率有所增加, 但是并没有很高, 从原有的 70%, 上升到 75% 左右.并保持稳定
        # 而磁盘的 IO 利用率, 则有明显的升高, 从 50% , 增加到 85%
        # 从这些条件来看, 确实是磁盘 IO 有所增加.
        # 但是, 从这些条件来看, 锅还不能明显断定就是我们的.
        # 所以, 我需要进一步的断定.
        # 于是, 我登陆到了机器上面, 以秒为单位来计算IO的利用率.
        # 当我到机器上执行更细粒度的数据查询的时候,
        # 其表现变成了如下所示(一张 60% - 100% 的变化图):
        # 事情可以看的再细一点,当以更细粒度的在电脑上看一个利用率的时候, 我们发现利用率平均在 80% 的运算结果, 是因为磁盘的IO的利用率
        # 从图标当中可以看到, 利用率之所以是在 80% 的运算结果, 是因为我们监控系统当中聚合的时间是 5s, 而这中间, 
        # 有的时候达到了 100%, 而有的时候下降到 60% , 被平均了以后, 就变成了 80%
        # 所以,系统当中出现的个别情况,就是正好磁盘IO利用率达到了100%的时候导致的,
        # 并且数据库在发生查询的时候发生的.
        
        ##************ 问题结论

        # 所有问题有了结论(开始背锅图片),接下来的问题是,
        # 为什么会发生磁盘利用率 100% 的情况?

        # 这里,首先我们来了解一下我们的文件系统基本结构.
        # 左边是我们的内存, 它被分为了一个一个的页面被进行操作.
        # 内存之上运行的是我们的文件系统,可以拥有路径, 文件, 然后用目录的形式来管理
        # 每一个文件, 都会拥有它的 inode 结构. 它用于存储文件与实际数据的比如说大小,权限等等相关信息.

        ram = self.create_memory(
            5, color=YELLOW, width=0.6, height=1.6,x_grid=0.2, y_grid=0.2
        )
        self.add(ram)
        self.play(ram.animate.shift(LEFT*4))

        file_manager = self.generate_tree()

        file_manager.shift(LEFT*4)
        self.wait()
        self.play(file_manager.animate.next_to(ram, UP))
        
        # disks
        disks = self.generate_disk()

        # 右侧是我们的磁盘, 它拥有一个又一个的扇区.
        # 这些扇区被组织成了其上面的一种形式, 在地址的最开始会 inode map,
        # 当程序根据 inode 来访问数据的时候, 首先会根据 inode 来获取其在磁盘当中的具体位置.
        # 然后在进行数据传输. 每一次的传输都是以 block 为单位.
        # 一般的, 会有 512k
        # 传输的过程, 在传统的银盘当中, 是依靠旋转.

        self.wait()
        self.play(disks.animate.shift(RIGHT*4))
        self.play(FadeOut(disks[0]))

        disk_arrangement = Rectangle(width=4.0, height=2.0, grid_xstep=0.5, grid_ystep=0.5,fill_opacity=0.5, color=GREEN).set_fill(color=GREEN)

        disk_arrangement.shift(RIGHT*4)


        self.wait()
        self.play(disk_arrangement.animate.next_to(disks, UP))

        inodes = Rectangle(width=1.0, height=2.0, fill_opacity=0.5, grid_ystep=1.0, grid_xstep=1.0, color=GREEN_A).move_to(disk_arrangement).align_to(disk_arrangement, LEFT)
        self.add(inodes)


        # 我们所说的这个问题当中, 就是在内存和磁盘之间的通道利用率, 在瞬时达到了 100%.
        tunnel = RoundedRectangle(corner_radius=0.1, height=0.5, color=RED, fill_opacity=0.1)
        self.play(FadeIn(tunnel))

        #  被文件系统托管的block
        temp = Rectangle(width=0.5, height=0.5).move_to(disks)
        self.play(Rotate(disks[1],angle=-45*DEGREES, run_time=0.1))
        self.play(temp.animate.move_to(disk_arrangement))
        self.play(temp.animate.move_to(file_manager))
        self.play(temp.animate.move_to(ram))
        self.play(tunnel.animate.set_fill(RED, opacity=0.2))
        self.remove(temp)

        for i in range(2, 10):
            temp.move_to(disks)
            self.play(Rotate(disks[1],angle=-45*DEGREES, run_time=0.1))
            self.play(temp.animate.move_to(disk_arrangement), run_time=0.1)
            self.play(temp.animate.move_to(file_manager), run_time=0.1)
            self.play(temp.animate.move_to(ram), run_time=0.1)
            self.play(tunnel.animate.set_fill(RED, opacity=i*0.1), run_time=0.1)
            self.remove(temp)

        full = Text("100%", color=RED).scale(0.5).next_to(tunnel, DOWN)
        self.play(FadeIn(full))
        self.wait()
        self.play(FadeOut(full))
        self.play(tunnel.animate.set_fill(RED, opacity=0.1))

        # 一般来说, 磁盘IO大了, 要么是系统请求增加
        # 要么就是磁盘容量不够,从而以碎片的形式存储,进而导致寻址增加.从而增加 IO,提高了利用率.
        self.play(Indicate(disks[1]))

        fragment_place = [0, 3, 1, 6]
        fragments = VGroup()
        for i in range(len(fragment_place)):
            x = fragment_place[i]
            circle = Circle(radius=0.05).move_to(disks[1][i][x])
            fragments.add(circle)

        self.play(FadeIn(fragments))

        self.play(Rotate(disks[1],angle=-45*DEGREES, run_time=0.5))
        
        # 与人员沟通, 发现最近请求的数量并没有明显的增加.
        # 然后通过 df 命令查看文件系统的占用空间, 发现仅仅是 30%

        # emmmm(背景音即可)
        # 难不成是 cache ? 
        # 我们来看看 cache 的使用情况.
        # 使用 cachestat.py , 获取 cache 的 hit, 发现其数值是 91%, 并不低. cache 的size 是500mi.
        # 我们在另外一台机器取出一个进行对比, 发现其命中率是 97%. 而 cache 的 size 竟然是 300mi

        # 当文件系统访问磁盘的时候, 为了因为磁盘的访问效率相对于内存更低. 所以文件系统会在内存当中使用cache.(manim 文件系统变化的动画)
        self.play(Indicate(ram[0]))

        cache = Rectangle(color=ORANGE, fill_opacity=0.6, width=0.6, height=0.6, grid_xstep=0.2, grid_ystep=0.2).move_to(ram[0]).align_to(ram[0], UP)

        self.play(FadeIn(cache))
        self.wait()
        # 而如果 cache 被占满, 则文件系统获取数据的时候, 无法从系统cache中获取, 就只能去磁盘当中拿. 这样就会导致io利用率升高.
        self.play(cache.animate.set_fill(ORANGE, opacity=1))
        pick = Rectangle(width=0.5, height=0.5).move_to(ram[0]).align_to(ram[0], UP)
        self.play(pick.animate.move_to(file_manager))
        self.play(Wiggle(pick))
        self.remove(pick)
        self.wait()
        pick.move_to(disks)
        self.play(pick.animate.move_to(disk_arrangement))
        self.play(pick.animate.move_to(file_manager))
        self.play(tunnel.animate.set_fill(RED, opacity=1))
        self.play(FadeIn(full))
        self.remove(temp)
       
        # 基本上可以断定就是 cache 的问题了.
        # 那么我们继续对比, 发现该机器某个的进程, 一直在持续消耗新的内存.而这部分内存, 消耗掉了本来文件系统cache可以占用的空间.
        # 从而导致 cache 命中率下降, 进而导致了 io 利用率的升高.

        # 于是 # kill $(pidof mihayo)

        # 我们的问题消失了.

        self.wait()
