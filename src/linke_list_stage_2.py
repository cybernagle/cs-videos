import math
from manim import *
#from manim_voiceover import VoiceoverScene
#from manim_voiceover.services.recorder import RecorderService


class PageLinkedListManagement(MovingCameraScene):#, VoiceoverScene):
    page_link = VGroup()
    pages = VGroup()
    braces = VGroup()
    point_to_free = DoubleArrow()
    point_to_prev = DoubleArrow()
    saved = None

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

    #def set_table_value(self, table: Table, row: int, col: int, value: Text) -> Table:
    #    table.get_rows()[row][col].animate.become(value.move_to(table.get_rows()[row][col].get_center()))
    #    return table

    def construct(self):
        # 这是一个空闲页链表
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
        # 这个页链表有12个页
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
                Text(str(12 - (i+1)*3)).scale(3).set_color(YELLOW).move_to(allocations[i+1][0].get_rows()[1][1].get_center())
            )

        # first order
        self.play(Restore(allocations[0]), run_time=1)

        # 我们现在有四个链表. 三个链表分别属于进程 1, 2, 3
        # 还有一个空闲链表
        # 这个时候, 我们进程一的内存使用完了. 我们需要释放内存
        # 这里为了演示,我们假设其与空闲内存不相邻.
        self.play(
            Indicate(allocations[0][-3]),
            Indicate(allocations[3][0]),
        )

        # 这样, 我们只能用链表将其串接起来. 
        # 我们释放的这个内存快, 包含两个页, 所以我们将 property 设置为 2
        # 因为它们不相邻,所以我们不需要更新两个链表头节点的值,后面我们会讲到需要修改的情况.
        self.play(
            allocations[0][0].get_rows()[1][1].animate.become(
                Text(str("2")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
        ))
        # 我们直接用链表将其链接起来.
        self.point_to_free = DoubleArrow(allocations[0][-3].get_center() + 4 * RIGHT,
                                    allocations[3][0].get_center() + 4 * LEFT)
        self.play(GrowArrow(self.point_to_free))

        # 所以这个时候这个空闲链表中就包含了两个链表.
        # 一个是进从进程回收的链表,
        self.play(Indicate(allocations[0]))
        # 另外一个是原来的空闲链表.
        self.play(Indicate(allocations[3]))

        self.saved = allocations.copy()
        """
        second order
        """
        # 接下来,假设进程2执行完毕, 我们需要将其回收.
        self.play(Indicate(allocations[1]))
        # 这里,我们没有假设它与空闲内存不相邻.这个时候,因为我们没有办法控制进程结束的顺序,所以我们不确定该进程的页链表是在什么位置.

        # 它有可能在空闲链表的前面,也有可能在空闲链表的后面.也有可能在中间.有可能相邻, 也有可能不相邻.
        for i in range(3):
            allocations[1].save_state()
            if i == 2:
                self.play(allocations[1].animate.next_to(allocations[3], RIGHT, buff=0))
            elif i == 1:
                self.play(allocations[1].animate.next_to(allocations[3], LEFT, buff=0))
            else:
                self.play(allocations[1].animate.next_to(allocations[i], LEFT, buff=0))
            self.play(Restore(allocations[1]), run_time=1)
        # 这是我们需要判断的地方,咱们按照进程的基础地址以及要释放的长度,得到其起始位置以及结束位置
        # 拿着这两个值,遍历当前的空闲链表.
        self.play(
            Indicate(allocations[0]),
            Indicate(allocations[3]),
            Indicate(self.point_to_free)
        )
        # 经过遍历以后,我们会发现图中第三个页表的位置和我的起始位置相邻.这个时候,咱们就合并这两个链表. 
        # 所谓合并,就是将两个链表当中后一个链表的 property <bookmark mark='A'/>置为零, 然后将前一个链表的property设为<bookmark mark='B'/>两者之和,也就是4.
        self.play(
            allocations[1][0].get_rows()[1][1].animate.become(
                Text(str("0")).scale(3).set_color(YELLOW).move_to(allocations[1][0].get_rows()[1][1].get_center())
        ))
        self.play(
            allocations[0][0].get_rows()[1][1].animate.become(
                Text(str("4")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
        ))

        # 然后将两者链接在一起. 
        self.play(
            self.point_to_prev.animate.become(
                DoubleArrow(
                    allocations[0][-3].get_center() + 4 * RIGHT,
                    allocations[1][0].get_center() + 4 * LEFT,
                )
            )
        )
        self.play(
            self.point_to_free.animate.become(
                DoubleArrow(
                    allocations[1][-3].get_center() + 4 * RIGHT,
                    allocations[3][0].get_center() + 4 * LEFT,
                )
            )
        )

        # 这一次, 我们还是有两个链表. 第一个是前面被释放的<bookmark mark='A'/>两个链表. 另外一个是最初的<bookmark mark='B'/>空闲列表.
        self.play(
            Indicate(allocations[0:2])
        )
        self.play(
            Indicate(allocations[3])
        )

        # process 3 也是同样的流程.
        # 判定与进程2的进程相邻后, 与合并后的1,2进行再一次<bookmark mark='A'/>合并,然后判定与空闲内存仍然相邻,继续<bookmark mark='B'>合并. 
        # bookmark A
        self.play(
            allocations[2][0].get_rows()[1][1].animate.become(
                Text(str("0")).scale(3).set_color(YELLOW).move_to(allocations[2][0].get_rows()[1][1].get_center())
        ))
        self.play(
            allocations[0][0].get_rows()[1][1].animate.become(
                Text(str("6")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
        ))

        # bookmark B
        self.play(
            allocations[3][0].get_rows()[1][1].animate.become(
                Text(str("0")).scale(3).set_color(YELLOW).move_to(allocations[3][0].get_rows()[1][1].get_center())
        ))
        self.play(
            allocations[0][0].get_rows()[1][1].animate.become(
                Text(str("8")).scale(3).set_color(YELLOW).move_to(allocations[0][0].get_rows()[1][1].get_center())
        ))


        # 让后把所有的链接.
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

        # 这样,我们就释放了三个进程的内存空间,并<bookmark mark='A'>恢复了所有的空闲内存空间.
        self.play(
            #Restore(allocations[1]),
            Restore(allocations[2]),
            FadeOut(self.point_to_free),
            FadeOut(self.point_to_prev),
            FadeOut(arrow_between),
            # just simple copy and become seems not work.
            # we should comes up with a better idea
            #allocations[1].animate.become(self.saved)
        )

        self.wait()