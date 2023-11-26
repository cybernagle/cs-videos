from manim import *

class UnivasalHash(Scene):
    def construct(self):

        trapezoid = Polygon(
            [-1, -2, 0],  # 左下角点
            [-1, 2, 0],   # 左上角点
            [1, 1, 0],    # 右上角点
            [1, -1, 0],   # 右下角点
            color=WHITE
        )

        left_side = Line([-1, -2, 0], [-1, 2, 0], color=GREEN)
        right_side = Line([1, 1, 0], [1, -1, 0], color=GREY)

        self.play(Create(trapezoid))
        self.play(Create(left_side), Create(right_side))
        self.wait()
