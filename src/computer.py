from manim import *

class ComputerScene(Scene):
    def construct(self):
        # 大的正方形代表电脑
        computer = Square(side_length=5, fill_opacity=0.5, color=BLUE)

        # 左上角的小方块代表 I/O 接口
        io_interface = Square(side_length=1, fill_opacity=0.5, color=YELLOW)
        io_interface.align_to(computer.get_corner(UP+LEFT), UP+LEFT) 

        # 中间的表代表中断向量
        interrupt_vector = Table([["Interrupt", "Handler"],
                                  ["Int 0", "Handler 0"],
                                  ["Int 1", "Handler 1"],
                                  ["...", "..."]],
                                 include_outer_lines=True)
        interrupt_vector.scale(0.5)
        interrupt_vector.move_to(computer.get_center())

        # 创建从 I/O 接口到中断向量的箭头
        arrow_io_to_int = Arrow(io_interface.get_corner(DOWN+RIGHT), 
                                interrupt_vector.get_cell((1, 0)).get_corner(UP+LEFT))

        # 创建从中断向量到处理程序的箭头
        arrow_int_to_handler = Arrow(interrupt_vector.get_cell((1, 0)).get_corner(RIGHT),
                                     interrupt_vector.get_cell((1, 1)).get_corner(LEFT))

        self.add(computer, io_interface, interrupt_vector,
                 arrow_io_to_int, arrow_int_to_handler)
