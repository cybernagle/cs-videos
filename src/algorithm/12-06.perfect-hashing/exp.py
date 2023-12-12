# 导入 manim 库
from manim import *

# 定义一个继承自 Scene 的类
class ExponentialFunction(Scene):
    # 定义构造方法
    def construct(self):
        # 创建一个 Axes 对象，设置 x 和 y 的范围和标签
        axes = Axes(
            x_range=[0, 20, 1],
            y_range=[-0.1, 2, 1],
            x_axis_config={"include_numbers": True},
            y_axis_config={"include_numbers": True},
            tips=True,
        )
        # 设置 Axes 的位置和颜色
        axes.move_to(ORIGIN)
        axes.set_fill(color=BLUE, opacity=1)

        graph = axes.plot(lambda x: 1/2 ** x, x_range=[0, 19], use_smoothing=False, color=RED)

        # 用 get_graph_label 方法添加函数标签
        #label = axes.get_graph_label(graph, label="y=\\frac{1}{2}^x")
        # 用 play 方法显示 Axes 和图像
        self.play(FadeIn(axes))
        self.play(Create(graph))#, Write(label), run_time=2)
        # 等待一会儿
        self.wait()
