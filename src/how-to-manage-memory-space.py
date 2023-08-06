import math
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

construct_memory_structure = """
        <bookmark mark='A'/>
        考虑一个问题, 如果提供给你这么一片内存, 你会怎么管理它呢?
        <bookmark mark='B'/>
        我们首先将物理内存分成一个一个的小块, 每个小块的大小为 4KB, 被称为页
        <bookmark mark='C'/>
        为了管理这些页, 我们需要一个数据结构, 用来记录每个页的状态, 以及它的属性,
        <bookmark mark='D'/>
        这里, 我们选择使用链表, 将所有的物理页穿起来, 形成一个空闲内存链表
"""
generate_linked_list = """
        <bookmark mark='A'/>
        接下来我们仔细看看每一个页的结构, 本视频当中, 我们主要关注其中的一个属性,
        <bookmark mark='B'/>
        也就是 property
        <bookmark mark='C'/>
        它表示我管理了多少个页, 换句话说, 我管理了多大的内存.
        <bookmark mark='D'/>
        这里为了表示方便, 我们假设这个属性设置为 1000, 也就是说, 我检测到有 1000 个页, 4MB 的内存
        <bookmark mark='E'/>
        非头节点的页结构,我们将它们的 property 设置为 0
        <bookmark mark='F'/>
        这样, 我们就得到了一个空闲内存链表, 也就是我们的空闲物理内存
"""
allocate_memory_desc = """
        <bookmark mark='A'/>
        而空闲物理内存得到了以后, 接下来, 我们就需要考虑如何分配内存了
        <bookmark mark='B'/>
        这里我们演示的是最简单的分配方式, 也就是首次适应算法
        <bookmark mark='C'/>
        通俗来讲就是我找到第一个满足要求的内存块, 这内存就是我的了
        <bookmark mark='D'/>
        """
allocating_memory = """
        这里呢我们申请5个页的内存
        <bookmark mark='A'/>
        而在我获取到内存之后, 我需要将后面的内存的空闲内存链表进行更新
        <bookmark mark='B'/>
        也就是将 property 减去申请了的内存大小, 在这里, 我们假设申请的页数是6, 1000-6=994
        <bookmark mark='C'/>
        然后,我就需要将这个内存块从空闲内存链表中删除,
        <bookmark mark='D'/>
        也就是将这个内存块从链表中断开
        """
free_memory_desc = """
        <bookmark mark='A'/>
        接下来, 我们来到释放内存, 我们申请到的内存应该如何释放呢?
        <bookmark mark='B'/>
        诶,你可以说, 我们直接把链表接回去不就可以了吗?
        在我们的情况当中, 我们是第一次申请内存, 所以从内存的开始地址进行申请. 然而, 现实的情况是, 我们申请到的内存, 有很多可能是
        <bookmark mark='C'/>
        在中间. 并且是不连续的
        <bookmark mark='D'/>
        这个时候, 咱们就需要判定它在物理地址是否相邻,如果是,就需要让相邻的内存合并起来.所以问题变成了,我们怎么知道我们要释放的是连续的呢?
        """
freeing_memory = """
        <bookmark mark='A'/>
        基于这个问题, 我们要做的首先确定要释放的内存的基础地址,
        <bookmark mark='B'/>
        再加上要释放的大小
        <bookmark mark='C'/>
        这样就能够得出要释放的内存的最后一个地址
        <bookmark mark='D'/>
        然后, 我们将空闲链表当中的每一个地址进行遍历, 并且将其地址和要释放内存的最后一个地址比较,"""

freed_memory = """
        <bookmark mark='A'/>
        如果相等, 那么就说明这个 memory 是连续的, 那么就可以进行合并.
        <bookmark mark='B'/>
        但是, 如果不相等, 那么就说明这个 memory 不是连续的, 那么就不需要进行合并, 而是直接将链表接入到最接近的内存块的前面
        <bookmark mark='C'/>
        在我们的实例当中, 我们可以直接链接回去, 并且合并这些内存.
        这样, 我们就完成了内存的分配和释放
"""

class HowToManageMemSpace(MovingCameraScene, VoiceoverScene):
    memory = VGroup()
    quare_mem = VGroup()
    linked = VGroup()

    def create_memory(self) -> VGroup:
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0
        for i in range(9):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                      grid_xstep=2.0, grid_ystep=0.5)
            #for j in range(3):
            #    square = Square(color=BLUE,fill_opacity=0.5, width=0.5, height=0.5)
            #    rect.add(square)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, DOWN, buff=0)
            addr.next_to(rect, LEFT, buff=0.2)
            mem.add(rect)
            addresses.add(addr)
            if (start_addr == 0):
                start_addr += 0x1FFFFFFF
            else:
                start_addr += 0x20000000

        memory = VGroup(mem, addresses).shift(UP*2)
        self.memory = memory

    def square_mem(self) -> VGroup():
        squares = VGroup(*[
            Square(color=BLUE,side_length=0.5, fill_opacity=0.2).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(9)
            for j in range(4)
        ])
        self.square_mem = squares

    def linked(self) -> VGroup:
        arrows = VGroup(*[
            DoubleArrow(
                square.get_center() + 0.05*RIGHT,
                square.get_center() + 0.95*RIGHT,
                stroke_width=0.5,
            )
            for square in self.square_mem
        ])

        self.linked = arrows


    def construct(self):
        self.set_speech_service(RecorderService())
        self.main()

    def main(self):
        # 考虑一个问题, 如果提供给你这么一片内存, 你会怎么管理它呢?
        self.create_memory()
        with self.voiceover(text=construct_memory_structure) as tracker:
            self.play(FadeIn(self.memory))
            self.square_mem()
            self.square_mem.align_to(self.memory[0], UL)

            # 我们首先将物理内存分成一个一个的小块, 每个小块的大小为 4KB, 被称为页
            #self.wait_until_bookmark("C")
            self.wait_until_bookmark("B")
            self.play(
                FadeIn(self.square_mem),
                FadeOut(self.memory[0])
            )

            # 为了管理这些页, 我们需要一个数据结构, 用来记录每个页的状态, 以及它的属性,
            #self.wait_until_bookmark("D")
            self.wait_until_bookmark("C")
            self.play(
                self.square_mem.animate.arrange(RIGHT, buff = 0.5).to_edge(LEFT),
                FadeOut(self.memory),
                run_time=3
            )

            #这里, 我们选择使用链表, 将所有的物理页穿起来, 形成一个空闲内存链表
            self.wait_until_bookmark("D")
            self.linked()
            for i,j in enumerate(self.linked, start=1):
                self.play(Create(j), run_time=1.0/i)

            self.play(
                self.camera.frame.animate.move_to(self.square_mem[0].get_center()),
                self.square_mem[0].animate.set_color(RED),
            )
            self.play(
                self.camera.frame.animate.scale(0.1)
            )

        table = Table(
            [["REF", "FLAGS", "PROPERTY"],
             ["P_LINK", "PRE_P_LINK", "PRE_VADDR"]],
            include_outer_lines=True,
            include_background_rectangle=True,
            background_rectangle_color=BLUE,
        ).move_to(self.square_mem[0].get_center()).scale_to_fit_width(self.square_mem[0].get_width()*1.2).set_stroke(width=0.2)

        temp = table.copy()

        with self.voiceover(text=generate_linked_list) as tracker:
            # 接下来我们仔细看看每一个页的结构, 本视频当中, 我们主要关注其中的一个属性, 
            self.wait_until_bookmark("A")
            self.play(ReplacementTransform(self.square_mem[0], table))

            # 也就是 property
            self.wait_until_bookmark("B")
            self.play(
                Indicate(table.get_rows()[0][2]),
            )

            # 表示我管理了多少个页, 换句话说, 我有多大的内存.
            # 这里为了表示方便, 我们将这个属性设置为 1000, 也就是说, 我有 1000 个页, 4MB 的内存
            self.wait_until_bookmark("D")
            self.play(
                ReplacementTransform(
                    table.get_rows()[0][0],
                    Text("0").scale(0.06).set_stroke(width=0.2).move_to(table.get_rows()[0][0].get_center()),
                ),
                ReplacementTransform(
                    table.get_rows()[0][1],
                    Text("0").scale(0.06).set_stroke(width=0.2).move_to(table.get_rows()[0][1].get_center()),
                ),
                ReplacementTransform(
                    table.get_rows()[0][2],
                    Text("1000").scale(0.06).set_stroke(width=0.2).move_to(table.get_rows()[0][2].get_center()),
                )
            )

            # 而其他的页,因为不是头节点,我们将它们的 property 设置为 0
            self.wait_until_bookmark("E")
            for i, obj in enumerate(self.square_mem[1:], start=1):
                t = temp.copy().move_to(obj.get_center())\
                               .scale_to_fit_width(obj.get_width()*1.2)\
                               .set_stroke(width=0.2)
                self.play(
                    self.camera.frame.animate.move_to(obj.get_center()),
                    ReplacementTransform(obj, t),
                    ReplacementTransform(
                        mobject=t.get_rows()[0][0],
                        target_mobject=Text("0").scale(0.06).set_stroke(width=0.2).move_to(t.get_rows()[0][0].get_center()),
                    ),
                    ReplacementTransform(
                        mobject=t.get_rows()[0][1],
                        target_mobject=Text("0").scale(0.06).set_stroke(width=0.2).move_to(t.get_rows()[0][1].get_center()),
                    ),
                    ReplacementTransform(
                        t.get_rows()[0][2],
                        Text("0").scale(0.06).set_stroke(width=0.2).move_to(t.get_rows()[0][2].get_center()),
                    ),
                    run_time=1.5/i
                )


            # 这样, 我们就得到了一个空闲内存链表, 也就是我们的空闲物理内存
            self.wait_until_bookmark("F")
            self.play(
                self.camera.frame.animate.scale(30),
            )
            self.play(
                self.camera.frame.animate.move_to(self.square_mem[18])
            )


        free_group = VGroup()
        free_mem = SurroundingRectangle(self.square_mem, color=GREEN)
        surrand_free = Brace(free_mem, direction=DOWN, buff=SMALL_BUFF)
        text_free = surrand_free.get_text("Free Memory").set_color(GREEN)
        free_group.add(free_mem, surrand_free, text_free)

        # new free mem
        new_free_group = VGroup()
        new_free_mem = SurroundingRectangle(self.square_mem[6:], color=GREEN)
        new_surrand_free = Brace(new_free_mem, direction=DOWN, buff=SMALL_BUFF)
        new_text_free = new_surrand_free.get_text("Free Memory").set_color(GREEN)
        new_free_group.add(new_free_mem,new_surrand_free, new_text_free)

        # allocated mem
        allocated_group = VGroup()
        allocated_memory = SurroundingRectangle(self.square_mem[0:6], color=RED)
        allocated_brace = Brace(allocated_memory, direction=DOWN, buff=SMALL_BUFF)
        allocated_text = allocated_brace.get_text("Allocated Memory").set_color(RED)
        allocated_group.add(allocated_memory, allocated_brace, allocated_text)


        self.play(
            Create(free_mem),
            GrowFromCenter(surrand_free),
            Write(text_free)
        )

        # 而空闲物理内存得到了以后, 接下来, 我们就需要考虑如何分配内存了
        # 这里我们演示的是最简单的分配方式, 也就是首次适应算法
        with self.voiceover(text=allocate_memory_desc) as tracker:

            # 通俗来讲就是我找到第一个满足要求的内存块, 这内存就是我的了
            self.wait_until_bookmark("C")
            self.play(
                Indicate(self.square_mem[0:6]),
            )
            self.play(
                Indicate(self.square_mem[0:10]),
            )

        # 这里我们申请5个页的内存
        with self.voiceover(text=allocating_memory) as tracker:
            self.play(
                Create(allocated_group),
            )

            self.play(
                self.camera.frame.animate.move_to(self.linked[2]),
            )
            self.play(
                self.camera.frame.animate.scale(0.14)
            )


            # 而在我获取到内存之后, 我需要将后面的内存的空闲内存链表进行更新
            self.wait_until_bookmark("A")
            self.camera.frame.save_state()
            self.play(
                self.camera.frame.animate.move_to(self.square_mem[6]),
            )
            self.play(
                self.camera.frame.animate.scale(0.3)
            )
            # 也就是将 property 减去申请了的内存大小, 在这里, 我们假设申请的页数是6, 1000-6=994
            self.wait_until_bookmark("B")
            self.play(
                ReplacementTransform(
                    self.square_mem[6].get_rows()[0][2],
                    Text("994").scale(0.06).set_stroke(width=0.2).move_to(self.square_mem[6].get_rows()[0][2].get_center()),
                ),
            )

            self.wait_until_bookmark("C")
            self.play(Restore(self.camera.frame))
            self.wait()

            allocated_group.add(self.square_mem[0:6], self.linked[0:6])

            # 然后,我就需要将这个内存块从空闲内存链表中删除,
            self.play(
                ReplacementTransform(free_group[0], new_free_group[0]),
                ReplacementTransform(free_group[1], new_free_group[1]),
                ReplacementTransform(free_group[2], new_free_group[2]),
            )

            # 也就是将这个内存块从链表中断开
            self.wait_until_bookmark("D")
            self.play(
                self.camera.frame.animate.scale(2),
            )

            self.play(
                allocated_group.animate.next_to(self.square_mem[6], UP, buff=1),
            )

            self.play(
                allocated_group.animate.align_to(self.square_mem[6], LEFT),
                self.camera.frame.animate.move_to(self.square_mem[8]),
            )

        # 接下来, 我们来到 free memory , 上面的这个 memory 如何 free? 
        # 诶,你可以说, 我们直接把链表接回去不就可以了吗? 
        with self.voiceover(text=free_memory_desc) as tracker:
            self.wait_until_bookmark("A")
            self.play(Indicate(allocated_group))
            allocated_group.save_state()
            self.wait_until_bookmark("B")
            self.play(allocated_group.animate.next_to(self.square_mem[6],LEFT, buff=0.1).shift(DOWN*0.5))
            self.play(Restore(allocated_group))

            # 在我们的情况当中, 我们是第一次申请内存, 所以从内存的开始地址进行申请. 然而, 现实的情况是, 我们申请到的内存, 有很多可能是在中间. 并且是不连续的
            self.wait_until_bookmark("C")
            self.play(
                Indicate(self.square_mem[7:10]),
                Indicate(self.square_mem[11:12]),
                Indicate(self.square_mem[14:18]),
            )

            # 这个时候, 咱们就需要判定内存区域是否相邻,如果是,就需要让相邻的内存合并起来.所以问题变成了,我们怎么知道我们要释放的是连续的呢?
            self.wait_until_bookmark("D")
            self.play(
                ApplyWave(self.square_mem[7:10]),
                ApplyWave(self.square_mem[11:12]),
                ApplyWave(self.square_mem[14:18]),
            )

        # 基于这个问题, 我们要做的首先确定要释放的内存的基础地址,
        with self.voiceover(text=freeing_memory) as tracker:
            self.wait_until_bookmark("A")
            self.play(
                Indicate(self.square_mem[0]),run_time=2
            )
            # 再加上要释放的大小
            self.wait_until_bookmark("B")
            self.play(
                Indicate(allocated_brace),run_time = 2
            )
            # 这样就能够得出要释放的内存的最后一个地址
            self.wait_until_bookmark("C")
            self.play(
                Indicate(self.square_mem[5]),run_time=2.5
            )

            # 然后, 我们将空闲链表当中的每一个地址进行遍历, 并且将其地址和要释放内存的最后一个地址比较, 
            self.wait_until_bookmark("D")
            self.camera.frame.save_state()
            for i, obj in enumerate(self.square_mem[6:15]):
                self.play(
                    #self.camera.frame.animate.move_to(obj),
                    Indicate(obj),
                    run_time=1/(i+2)
                )
            self.play(Restore(self.camera.frame))
            self.square_mem.save_state()
            self.wait_until_bookmark("A")
            self.play(self.square_mem[5].animate.scale(2),
                      self.square_mem[6].animate.scale(2),)
            self.play(
                Indicate(self.square_mem[6]),
                Indicate(self.square_mem[5]),
            )
            self.play(Restore(self.square_mem))


        # 如果相等, 那么就说明这个 memory 是连续的, 那么就可以进行合并.
        with self.voiceover(text=freed_memory) as tracker:

            # 但是, 如果不相等, 那么就说明这个 memory 不是连续的, 那么就不需要进行合并, 而是直接将链表接入到最接近的内存块的前面
            self.wait_until_bookmark("B")
            self.square_mem.save_state()
            self.play(self.square_mem[5].animate.scale(2),
                      self.square_mem[6].animate.scale(2),)
            self.play(
                Wiggle(self.square_mem[6]),
                Wiggle(self.square_mem[5]),
            )
            self.play(Restore(self.square_mem))

            # 在我们的实例当中, 我们可以直接链接回去, 并且合并这些内存.
            self.wait_until_bookmark("C")
            self.play(allocated_group.animate.next_to(self.square_mem[6],LEFT, buff=0.1).shift(DOWN*0.5))
            self.play(
                self.camera.frame.animate.scale(4),
            )
            self.play(
                self.camera.frame.animate.move_to(self.square_mem[18])
            )
