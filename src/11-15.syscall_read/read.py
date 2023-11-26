from manim import *

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"
class Read(Scene):
    def construct(self):

        self.camera.background_color = BACKGROUND

        # 这是一个 read 操作
        # 它分别有三个参数, file, buffer, size
        # buffer的作用, 是在内存当中申请一块空间来存储需要读取的文件.
        # size 则限定了 buffer 的大小.

        # 我们来详细看一下 file 这个参数,
        read = Text("read(file, *buff, size)")
        read[0:4].move_to(ORIGIN)
        self.add(read[0:4])
        self.wait()
        self.play(read[0:4].animate.next_to(read[4:], LEFT))
        self.play(FadeIn(read[4:]))
        self.play(read.animate.shift(UP*3))

        gbuffer = VGroup()
        # buffer
        self.play(read[9:14].animate.set_fill(WORD_A))
        buffer = Rectangle(width=5, height=1, color=WORD_A)
        buffername = Text("buffer", color=WORD_A).move_to(buffer)
        self.play(FadeIn(buffer))
        self.play(FadeIn(buffername))
        gbuffer.add(buffer, buffername)

        # size
        self.play(read[15:-1].animate.set_fill(WORD_B))
        #left_line = Line(start=read[15], end=buffer.get_all_points()[0])
        left_line = Arrow(
            start=read[17].get_bottom(),
            end=buffer.get_all_points()[3]+LEFT+UP*0.21,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.02
        )
        right_line = Arrow(
            start=read[17].get_bottom(),
            end=buffer.get_all_points()[0]+RIGHT+UP*0.21,
            stroke_width=0.5,
            buff=0,
            max_tip_length_to_length_ratio=0.05
        )
        self.play(
            GrowArrow(left_line),
            GrowArrow(right_line)
        )

        self.play(buffer.animate.set(width=7))
        bsize = Brace(buffer).set_fill(WORD_B)
        bsize_text = bsize.get_text("size").set_fill(WORD_B)
        self.play(FadeIn(bsize), FadeIn(bsize_text))
        self.play(
            FadeOut(left_line),
            FadeOut(right_line),
        )

        gbuffer.add(bsize, bsize_text)
        self.play(gbuffer.animate.scale(0.5).align_on_border(LEFT).shift(UP*1.5+RIGHT))

        self.play(Indicate(read[5:8]))


        # file
        gfile = VGroup()
        afile = read[5:8].copy()
        file_struct = Rectangle(width=2, height=2, color=OBJ_A) 
        self.play(afile.animate.become(file_struct))
        file_name = Text("file").set_fill(OBJ_A).move_to(file_struct)
        gfile.add(afile, file_struct, file_name)

        # 它会包含文件状态, 比如说打开,被关闭.
        # 然后还有其权限, 包含可读,可写.
        # 最重要的就是 inode, 又称 index node.
        # 它包含了文件的元数据,在访问之前,它需要被添加锁,从而避免重复性的读写 ,
        # 而它的属性就包括了文件大小, 文件类型
        # 最关键的, 还是它所指向的 block 的位置.
        # 假设我们的 read 访问的, 是 4, 5 两个block.

        # 这是我们要访问的磁盘,
        # 文件系统初始化的过程中,它的起始位置会设置为超级块.
        # 然后, 我们的磁盘被分成一个一个的块并被编上号码.
        # 而 superblock 当中, 会记录上 inode 的数量, 以及 block 的数量
        # 在我们的视频当中, 假设一个小方格为一个块.
        # 而 inode ,则是包含了多个块的一个数据结构.

        # 回到我们 read 的操作, read, 它根据 inode 里面获取到了 4, 5 两个block
        # 剩下的, 就是将其内容读取到 buffer 当中即可.

        datas = ["状态", "权限"]
        for i in range(len(datas)):
            text = Text(datas[i]).scale(0.5).move_to(file_struct)
            self.play(FadeIn(text), run_time=0.2)
            self.wait()
            self.play(FadeOut(text), run_time=0.2)


        # inode
        ginode = VGroup()
        inode_struct =  Rectangle(width=1, height=1, color=OBJ_B, fill_opacity=0.3)
        inode = Text("inode", color=OBJ_B).scale(0.3).move_to(inode_struct)
        #self.play(FadeIn(lock))
        ginode.add(inode_struct, inode)

        self.play(FadeIn(inode))
        self.wait()
        self.play(FadeIn(inode_struct))
        self.wait()

        self.play(gfile.animate.scale(0.7).next_to(gbuffer, DOWN))
        self.play(ginode.animate.scale(2))

        self.play(FadeIn(file_name))

        lock = ImageMobject("./resources/lock.png").scale(0.2).move_to(inode_struct.get_all_points()[1])
        self.play(FadeIn(lock))
        inum = Text("4,5",color=OBJ_B).move_to(inode_struct)
        self.play(
            FadeOut(inode),
        )
        # inode 数据结构当中, 有一个很重要的信息, 就是 inode number
        self.play(
            FadeIn(inum)
        )

        #ginode.add(inum)

        self.play(
            FadeOut(inum)
        )
        
        self.play(ginode.animate.scale(0.7).next_to(gfile, DOWN, buff=0.6))
        self.play(lock.animate.scale(0.7).move_to(inode_struct.get_all_points()[1]))

        dgroup = VGroup()
        superblock_tt = Rectangle(width=0.5, height=1.5, grid_ystep=0.75, grid_xstep=0.5, color=OBJ_C, fill_opacity=0.3).shift(LEFT)
        sb_text = Text("superblock", color=OBJ_C).scale(0.3).next_to(superblock_tt, DOWN)
        dgroup.add(superblock_tt, sb_text)

        block_tt = Rectangle(height=1.5, width=3, grid_ystep=0.5, grid_xstep=0.5, color=OBJ_C).next_to(superblock_tt, RIGHT, buff=0.2)
        block_text = Text("blocks", color=OBJ_C).scale(0.3).next_to(block_tt, DOWN)
        dgroup.add(block_tt, block_text)

        ablock = Rectangle(height=0.5, width=0.5, color=OBJ_C, fill_opacity=0.8).move_to(block_tt).align_to(block_tt, UL)
        ablock_text = Text("block", color=OBJ_C).scale(0.2).next_to(ablock, DOWN, buff=0.1)
        dgroup.add(ablock, ablock_text)

        ainode = Rectangle(height=1, width=0.5, color=OBJ_B, fill_opacity=0.8).next_to(ablock, RIGHT, buff=0).align_to(ablock,UP)
        ainode_text = Text("inode", color=OBJ_B).scale(0.2).next_to(ainode, DOWN, buff=0.1)
        dgroup.add(ainode, ainode_text)

        block_count = Text("block\ncount", color=OBJ_C).scale(0.2).move_to(superblock_tt).shift(UP*0.3)
        inode_count = Text("inode\ncount", color=OBJ_B).scale(0.2).move_to(superblock_tt).shift(DOWN*0.3)
        dgroup.add(block_count, inode_count)

        self.play(FadeIn(dgroup))
        bnum4 = Text("4").scale(0.3).move_to(ainode).shift(UP*0.2)
        bnum5 = Text("5").scale(0.3).move_to(ainode).shift(DOWN*0.2)
        self.play(
            FadeIn(bnum4),
            FadeIn(bnum5),
        )

        self.play(ainode.copy().animate.become(buffer))
        
        self.play(buffer.animate.set_fill(WORD_A, opacity=0.8))

        self.wait()

class DiskOps(Scene):

    def generate_cycle(self, inner_radius=1, outer_radius=1.5,color=OBJ_A):
        cycle = VGroup()
        for i in range(8):
            a = AnnularSector(inner_radius=inner_radius, outer_radius=outer_radius, angle=44.5 * DEGREES,start_angle=i*45*DEGREES ,color=color)
            cycle.add(a)
        return cycle

    def generate_disk(self):
        disks = VGroup()
        prev_disk = AnnularSector(inner_radius=0.1, outer_radius=1.14, angle= 2*PI , color=OBJ_A)

        disks.add(prev_disk)

        disk = VGroup()
        init = 0.1
        for i in range(5):
            inner = init
            outer = init+0.2
            s = self.generate_cycle(inner_radius=inner, outer_radius=outer,color=OBJ_A)
            disk.add(s)
            s.move_to(disk)
            init+=0.21
        disks.add(disk)

        return disks

    def construct(self):
        self.camera.background_color = BACKGROUND
        disk = self.generate_disk()
        self.add(disk)
        #self.play(FadeIn(disk))
        self.play(FadeOut(disk[0]))

        self.play(disk[1].animate.shift(RIGHT*3))

        # init file system management
        dgroup = VGroup()
        self.play(Rotate(disk[1],angle=-45*DEGREES, run_time=0.1))

        self.play(Indicate(disk[1][4][0]))
        superblock_s = disk[1][4][0].copy()
        superblock_t = Rectangle(width=0.5, height=1.5, color=OBJ_C, fill_opacity=0.3).next_to(disk, LEFT*8)
        superblock_tt = Rectangle(width=0.5, height=1.5, grid_ystep=0.75, grid_xstep=0.5, color=OBJ_C, fill_opacity=0.3).next_to(disk, LEFT*8)
        self.play(superblock_s.animate.become(superblock_t))

        sb_text = Text("superblock", color=OBJ_C).scale(0.3).next_to(superblock_t, DOWN)
        self.play(FadeIn(sb_text))

        dgroup.add(superblock_tt, sb_text)

        #self.play(superblock_t.animate.become(superblock_tt))

        self.play(
            Indicate(disk[1][4][1:]),
            Indicate(disk[1][0:4])
        )

        block_s = disk[1].copy()
        block_t = Rectangle(height=1.5, width=3, color=OBJ_C).shift(LEFT*1.5)

        self.play(block_s.animate.become(block_t))
        block_tt = Rectangle(height=1.5, width=3, grid_ystep=0.5, grid_xstep=0.5, color=OBJ_C).shift(LEFT*1.5)

        self.play(
            FadeIn(block_tt),
            FadeOut(block_t)
        )


        block_text = Text("blocks", color=OBJ_C).scale(0.3).next_to(block_tt, DOWN)
        self.play(FadeIn(block_text))
        dgroup.add(block_tt, block_text)

        ablock = Rectangle(height=0.5, width=0.5, color=OBJ_C, fill_opacity=0.8).move_to(block_tt).align_to(block_tt, UL)
        ablock_text = Text("block", color=OBJ_C).scale(0.2).next_to(ablock, DOWN, buff=0.1)
        self.play(
            FadeIn(ablock),
            FadeIn(ablock_text)
        )
        self.play(
            Indicate(ablock)
        )
        dgroup.add(ablock, ablock_text)

        ainode = Rectangle(height=1, width=0.5, color=OBJ_B, fill_opacity=0.8).next_to(ablock, RIGHT, buff=0).align_to(ablock,UP)
        ainode_text = Text("inode", color=OBJ_B).scale(0.2).next_to(ainode, DOWN, buff=0.1)

        self.play(
            FadeIn(ainode),
            FadeIn(ainode_text)
        )
        self.play(
            Indicate(ainode)
        )

        dgroup.add(ainode, ainode_text)

        block_count = Text("block\ncount", color=OBJ_C).scale(0.2).move_to(superblock_tt).shift(UP*0.3)
        inode_count = Text("inode\ncount", color=OBJ_B).scale(0.2).move_to(superblock_tt).shift(DOWN*0.3)
        self.play(
            FadeIn(superblock_tt),
            FadeIn(block_count),
            FadeIn(inode_count),
        )

        dgroup.add(block_count)
        dgroup.add(inode_count)

        
        self.wait()
