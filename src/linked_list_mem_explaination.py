import math
from manim import *
#from manim_voiceover import VoiceoverScene
#from manim_voiceover.services.recorder import RecorderService


class PageLinkedListManagement(MovingCameraScene):#, VoiceoverScene):
    page_link = VGroup()
    pages = VGroup()
    braces = VGroup()

    def init_pages(self) -> VGroup:
        tables = VGroup(*[
            Table(
                [["0"],
                 ["0"],
                 ["pre-next"]],
                row_labels=[Text("flag"), Text("property"), Text("page_link")],
                include_outer_lines=True,
                background_rectangle_color=BLUE,
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
        self.play(Create(self.page_link))
        # 这个页链表有12个页
        self.play(self.camera.frame.animate.scale(8))
        self.play(self.camera.frame.animate.move_to(self.page_link[5].get_center()))
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
            self.play(allocations[i].animate.move_to(allocations[i].get_center() + 6 * UP + i * 2* RIGHT))
            self.play(allocations[i+1][0].get_rows()[1][1].animate.scale(3))
            self.set_table_value(allocations[i+1][0], 1, 1, Text(str(12-(i+1)*3)).scale(3).set_color(RED))

        three_orders = [
            [0,1,2],
            [2,1,0],
            [1,2,0],
        ]
        for order in three_orders:
            for i in order:
                self.play(Restore(allocations[i]), run_time=0.3)

            for i in order:
                allocations[i].save_state()
                self.play(allocations[i].animate.move_to(allocations[i].get_center() + 6 * UP + i * 2* RIGHT),run_time=0.3)


        self.wait()
