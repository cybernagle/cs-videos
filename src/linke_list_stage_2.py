import math
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

s_intro = """
我们现在有四个链表. 三个链表分别属于进程<bookmark mark='A'/> 1, 2, 3,还有<bookmark mark='B'/>空闲链表, 它们一共 12<bookmark mark='C'/>个页
被进程使用的链表应该如何进行释放呢?
"""
s_free_first = """
假设现在我们进程一的内存<bookmark mark='A'/>使用完了. 我们需要释放内存
这里为了演示方便,我们首先讨论进程1与<bookmark mark='B'/>空闲内存的地址不相邻的情况.
"""
s_free_first_act = """
在不相邻的情况下, 我们只能用链表将其串接起来.
因为被释放的进程1占用来两个页的内存, 所以我们将 property 设置<bookmark mark='A'/>为 2
而因为它们不相邻,所以我们不需要更新两个链表头节点的值,然后我们直接用链表将其链接<bookmark mark='B'/>起来.
"""

s_free_first_done = """
所以这个时候这个空闲链表中就包含了两个链表.
一个是进从进程1回收的链表<bookmark mark='A'/>,
另外一个是原来的空闲链表<bookmark mark='B'/>.
"""

s_free_second = """
接下来,假设进程2<bookmark mark='A'/>执行完毕, 我们需要将其回收.
这里,因为我们没有办法控制进程结束的顺序,所以我们不确定该进程的页链表是在什么位置.
它有可能在空闲链表的前面<bookmark mark='B'/>,也有可能在空闲链表的<bookmark mark='C'/>中间.也有可能在后面<bookmark mark='D'/>.内存地址有可能相邻, 也有可能不相邻.
"""
s_free_second_judge = """
而这是我们需要判断的地方,咱们按照进程的基础地址以及要释放的长度,得到其<bookmark mark='A'/>起始位置
以及<bookmark mark='B'/>结束位置
拿着这两个值,遍历当前的<bookmark mark='C'/>空闲链表.
"""
s_free_second_merge = """
经过遍历以后,我们会发现图中第三个页表的位置<bookmark mark='A'/>和我的起始位置相邻.这个时候,咱们就开始合并这两个链表.
"""
s_free_second_act = """
所谓合并,就是将两个链表当中后一个链表的property<bookmark mark='A'/>置为零,
然后将前一个链表的property设为<bookmark mark='B'/>两者之和,也就是4.
然后将两者链接<bookmark mark='C'/>在一起.
并且和后面的链表重新<bookmark mark='D'/>链接
"""
s_free_second_done = """
这一次, 我们还是有两个链表. 第一个是前面被释放的两个合并后链表<bookmark mark='A'/>. 另外一个是最初的<bookmark mark='B'/>空闲列表.
"""
s_free_third = """
process 3 的释放也是同样的流程.
判定与进程2的进程相邻后, 与合并后的1,2进行再一次<bookmark mark='A'/>合并,
后判定与空闲内存仍然相邻,继续<bookmark mark='B'/>合并.
最后把它们链接<bookmark mark='C'/>起来
"""
s_free_third_done = """
这样,我们就释放了三个进程的内存空间,并<bookmark mark='A'/>恢复了所有的空闲内存空间.
"""


class PageLinkedListManagement(MovingCameraScene, VoiceoverScene):
    page_link = VGroup()
    pages = VGroup()
    braces = VGroup()
    point_to_free = DoubleArrow()
    point_to_prev = DoubleArrow()

    def init_pages(self) -> VGroup:
        tables = VGroup(*[
            Table(
                [["0"],
                 ["0"],
                 ["pre-next"]],
                row_labels=[Text("flag"), Text("property"), Text("page_link")],
                include_outer_lines=True,
                include_background_rectangle=True,
                background_rectangle_color=BLUE,
                arrange_in_grid_config={"cell_alignment": RIGHT})
                for _ in range(8)
        ])
        self.pages = tables

    def set_link(self) -> VGroup:
        arrows = VGroup(*[
            DoubleArrow(
                obj.get_rows()[2][0].get_center() + 5.4 * RIGHT,
                obj.get_rows()[2][0].get_center() + 7.7 * RIGHT,
            )
            for obj in self.pages
        ])
        self.page_link = arrows

    def construct(self):
        self.set_speech_service(RecorderService())
        self.camera.frame.scale(5.7)
        self.init_pages()
        self.pages.arrange(buff=2)
        #self.set_table_value(self.pages[0], 1, 1, Text("").scale(3).set_color(YELLOW))

        self.pages[0].get_rows()[1][1].become(
            Text("8").scale(3).set_color(YELLOW).move_to(self.pages[0].get_rows()[1][1].get_center())
        )
        self.set_link()

        self.add(self.pages)
        self.add(self.page_link)
        self.camera.frame.move_to(self.page_link[3].get_center())
        index = 0
        allocations = VGroup()
        for i in range(0, 8, 2):
            allocations.add(self.pages[i:i + 2])
            allocations[index].add(self.page_link[i:i + 2])
            index += 1

        for i in range(3):
            desc = Text("Proces {}".format(i+1)).scale(4).next_to(allocations[i].get_center(), UP, buff=3)
            self.add(desc)
            allocations[i].add(desc)
            allocations[i].save_state()
            allocations[i].move_to(allocations[i].get_center() + 6 * UP + i * 2* RIGHT)
            #allocations[i+1][0].get_rows()[1][1].scale(3)
            allocations[i+1][0].get_rows()[1][1].become(
                Text(str(8 - (i+1)*2)).scale(3).set_color(YELLOW).move_to(allocations[i+1][0].get_rows()[1][1].get_center())
            )

        self.set_speech_service(RecorderService())
        with self.voiceover(text=s_intro) as tracker:
            # 我们现在有四个链表. 三个链表分别属于进程<bookmark mark='A'/> 1, 2, 3,它们如何进行释放呢?
            self.wait_until_bookmark('A')
            for i in range(3):
                self.play(Indicate(allocations[i]))
            # 还有一个<bookmark mark='B'/>空闲链表
            self.wait_until_bookmark('B')
            self.play(Indicate(allocations[3]))

            # 一共 12<bookmark mark='C'/> 个页
            self.wait_until_bookmark('C')
            self.play(
                Indicate(allocations),
                Indicate(self.pages)
            )

        with self.voiceover(text=s_free_first) as tracker:
            # 这个时候, 我们进程一的内存<bookmark mark='A'/>使用完了. 我们需要释放内存
            self.wait_until_bookmark('A')
            self.play(Restore(allocations[0]), run_time=1)

            # 这里为了演示方便,我们先假设已知其与<bookmark mark='B'/>空闲内存不相邻.
            self.wait_until_bookmark('B')
            self.play(
                Indicate(allocations[0][-3]),
                Indicate(allocations[3][0]),
            )

        with self.voiceover(text=s_free_first_act) as tracker:
            # 这样, 我们只能用链表将其串接起来. 
            # 我们释放的这个内存的两个页, 所以我们将 property 设置<bookmark mark='A'/>为 2
            self.wait_until_bookmark('A')
            self.play(
                allocations[0][0].get_rows()[1][1].animate.become(
                    Text(str("2")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
            ))
            # 
            self.point_to_free = DoubleArrow(allocations[0][-3].get_center() + 4 * RIGHT,
                                        allocations[3][0].get_center() + 4 * LEFT)
            # 因为它们不相邻,所以我们不需要更新两个链表头节点的值,后面我们会讲到需要修改的情况.然后我们直接用链表将其链接<bookmark mark='B'/>起来.
            self.wait_until_bookmark('B')
            self.play(GrowArrow(self.point_to_free))

        with self.voiceover(text=s_free_first_done) as tracker:
            # 所以这个时候这个空闲链表中就包含了两个链表.
            # 一个是进从进程1回收的链表<bookmark mark='A'/>,
            self.wait_until_bookmark('A')
            self.play(Indicate(allocations[0]))
            # 另外一个是原来的空闲链表<bookmark mark='B'/>.
            self.wait_until_bookmark('B')
            self.play(Indicate(allocations[3]))
            self.wait()

        with self.voiceover(text=s_free_second) as tracker:
            # 接下来,假设进程2<bookmark mark='A'/>执行完毕, 我们需要将其回收.
            self.wait_until_bookmark('A')
            self.play(Indicate(allocations[1]))
            # 这里,我们它与空闲内存不相邻的假设.而因为我们没有办法控制进程结束的顺序,所以我们不确定该进程的页链表是在什么位置.
            # 它有可能在空闲链表的前面<bookmark mark='B'/>,也有可能在空闲链表的中间.也有可能在后面.地址有可能相邻, 也有可能不相邻.
            self.wait_until_bookmark('B')
            for i in range(3):
                allocations[1].save_state()
                if i == 2:
                    self.play(allocations[1].animate.next_to(allocations[3], RIGHT, buff=0))
                elif i == 1:
                    self.play(allocations[1].animate.next_to(allocations[3], LEFT, buff=0))
                else:
                    self.play(allocations[1].animate.next_to(allocations[i], LEFT, buff=0))
                self.play(Restore(allocations[1]), run_time=1)
        with self.voiceover(text=s_free_second_judge) as tracker:
            # 而这是我们需要判断的地方,咱们按照进程的基础地址以及要释放的长度,得到其<bookmark mark='A'/>起始位置
            self.wait_until_bookmark('A')
            self.play(
                Indicate(allocations[1][0]),
            )
            # 以及<bookmark mark='B'/>结束位置
            self.wait_until_bookmark('B')
            self.play(
                Indicate(allocations[1][-3]),
            )
            # 拿着这两个值,遍历当前的<bookmark mark='C'/>空闲链表.
            self.wait_until_bookmark('C')
            self.play(
                Indicate(allocations[0]),
                Indicate(allocations[3]),
                Indicate(self.point_to_free)
            )
        with self.voiceover(text=s_free_second_merge) as tracker:
            # 经过遍历以后,我们会发现图中第二个页表的位置<bookmark mark='A'/>和我的起始位置相邻.这个时候,咱们就开始合并这两个链表. 
            self.wait_until_bookmark('A')
            self.play(
                ApplyWave(allocations[0][-3]),
                ApplyWave(allocations[1][0]),
            )

        with self.voiceover(text=s_free_second_act) as tracker:
            # 所谓合并,就是将两个链表当中后一个链表的property<bookmark mark='A'/>置为零, 
            self.wait_until_bookmark('A')
            self.play(
                allocations[1][0].get_rows()[1][1].animate.become(
                    Text(str("0")).scale(3).set_color(YELLOW).move_to(allocations[1][0].get_rows()[1][1].get_center())
            ))

            # 然后将前一个链表的property设为<bookmark mark='B'/>两者之和,也就是4.
            self.wait_until_bookmark('B')
            self.play(
                allocations[0][0].get_rows()[1][1].animate.become(
                    Text(str("4")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
            ))

            # 然后将两者链接<bookmark mark='C'/>在一起. 
            self.wait_until_bookmark('C')
            self.play(
                self.point_to_prev.animate.become(
                    DoubleArrow(
                        allocations[0][-3].get_center() + 4 * RIGHT,
                        allocations[1][0].get_center() + 4 * LEFT,
                    )
                )
            )
            # 并且和后面的链表重新<bookmark mark='D'/>链接
            self.wait_until_bookmark('D')
            self.play(
                self.point_to_free.animate.become(
                    DoubleArrow(
                        allocations[1][-3].get_center() + 4 * RIGHT,
                        allocations[3][0].get_center() + 4 * LEFT,
                    )
                )
            )

        with self.voiceover(text=s_free_second_done) as tracker:
            # 这一次, 我们还是有两个链表. 第一个是前面被释放的两个合并后链表<bookmark mark='A'/>. 另外一个是最初的<bookmark mark='B'/>空闲列表.
            self.wait_until_bookmark('A')
            self.play(
                Indicate(allocations[0:2])
            )
            self.wait_until_bookmark('B')
            self.play(
                Indicate(allocations[3])
            )

        with self.voiceover(text=s_free_third) as tracker:
            # process 3 的释放也是同样的流程.
            # 判定与进程2的进程相邻后, 与合并后的1,2进行再一次<bookmark mark='A'/>合并,
            self.wait_until_bookmark('A')
            self.play(
                allocations[2][0].get_rows()[1][1].animate.become(
                    Text(str("0")).scale(3).set_color(YELLOW).move_to(allocations[2][0].get_rows()[1][1].get_center())
            ))
            self.play(
                allocations[0][0].get_rows()[1][1].animate.become(
                    Text(str("6")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
            ))

            #然后判定与空闲内存仍然相邻,继续<bookmark mark='B'/>合并.
            self.wait_until_bookmark('B')
            self.play(
                allocations[3][0].get_rows()[1][1].animate.become(
                    Text(str("0")).scale(3).set_color(YELLOW).move_to(allocations[3][0].get_rows()[1][1].get_center())
            ))
            self.play(
                allocations[0][0].get_rows()[1][1].animate.become(
                    Text(str("8")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
            ))


            # 最后把它们链接<bookmark mark='C'/>起来
            self.wait_until_bookmark('C')
            arrow_between = DoubleArrow(
                allocations[1][-3].get_center() + 4 * RIGHT,
                allocations[2][0].get_center() + 4 * LEFT,
            )
            self.play(
                GrowArrow(arrow_between)
            )
            self.play(
                self.point_to_free.animate.become(
                    DoubleArrow(
                        allocations[2][-3].get_center() + 4 * RIGHT,
                        allocations[3][0].get_center() + 4 * LEFT,
                    )
                )
            )


        with self.voiceover(text=s_free_third_done) as tracker:
            # 这样,我们就释放了三个进程的内存空间,并<bookmark mark='A'/>恢复了所有的空闲内存空间.
            self.wait_until_bookmark('A')
            self.play(
                FadeOut(self.point_to_free),
                FadeOut(self.point_to_prev),
                FadeOut(arrow_between),
                allocations[2].animate.move_to(allocations[2].get_center() + 6 * DOWN + 4 * LEFT),
                allocations[1].animate.move_to(allocations[1].get_center() + 6 * DOWN + 2 * LEFT)
            )

        self.wait()
