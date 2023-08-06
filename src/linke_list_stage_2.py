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

    def init_pages(self) -> VGroup:
        tables = VGroup(*[
            Table(
                [["0"],
                 ["0"],
                 ["pre-next"]],
                row_labels=[Text("flag"), Text("property"), Text("page_link")],
                include_outer_lines=True,
                arrange_in_grid_config={"cell_alignment": RIGHT})
                for _ in range(12)
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

    def set_table_value(self, table: Table, row: int, col: int, value: Text) -> Table:
        self.play(
            table.get_rows()[row][col].animate.become(value.move_to(table.get_rows()[row][col].get_center()))
        )

    def construct(self):
        # 这是一个空闲页链表
        self.init_pages()
        self.add(self.pages.arrange(buff=2))
        self.camera.frame.move_to(self.pages[0].get_center())
        self.set_table_value(self.pages[0], 1, 1, Text("12").set_color(RED))
        self.set_link()
        self.add(self.page_link)
        # 这个页链表有12个页
        self.camera.frame.scale(8)
        self.camera.frame.move_to(self.page_link[5].get_center())
        index = 0
        allocations = VGroup()
        for i in range(0, 12, 3):
            allocations.add(self.pages[i:i + 3])
            allocations[index].add(self.page_link[i:i + 3])
            index += 1

        for i in range(3):
            desc = Text("Proces {}".format(i+1)).scale(4).next_to(allocations[i].get_center(), UP, buff=3)
            allocations[i].add(desc)
            allocations[i].save_state()
            allocations[i].move_to(allocations[i].get_center() + 6 * UP + i * 2* RIGHT)
            allocations[i+1][0].get_rows()[1][1].scale(3)
            self.set_table_value(allocations[i+1][0], 1, 1, Text(str(12-(i+1)*3)).scale(3).set_color(RED))

        # first order
        for i in range(3):
            self.play(Restore(allocations[i]), run_time=1)
            allocations[i][-3].save_state()
            # 这个时候, 我们与空闲内存不相邻. 所以我们不能进行合并. 
            self.play(
                Indicate(allocations[i][-3]),
            )
            # 这样, 我们只能用链表将其串接起来. 但是对 property 我们是不需要进行更新的.

        self.wait()
