from manim import *
m = Rectangle(height=0.6, width=0.4, color=OBJ_B, fill_opacity=0.5).next_to(hash_func, RIGHT, buff=0.05)
tm = Text("M", color=WORD_B).scale(0.5).move_to(m)
gm = VGroup(m, tm)

hash_func1 = Polygon(
    [-0.5, -1.3, 0],  # 左下角点
    [-0.5, 1.3, 0],   # 左上角点
    [0.5, 0.3, 0],    # 右上角点
    [0.5, -0.3, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5,
    stroke_opacity=0
)
# 我们定义一个大于U集合的prime p
prime = Rectangle(height=2.6, width=0.4, color=OBJ_C, fill_opacity=0.5).next_to(univasal, UP, buff=0.05)
tprime = Text("P", color=OBJ_C).scale(0.5).move_to(prime)
gprime = VGroup(prime, tprime)

hash_func2 = Polygon(
    [-2.5, -1, 0],  # 左下角点
    [-2.5, 1, 0],   # 左上角点
    [-1, 1.3, 0],    # 右上角点
    [-1, -1.3, 0],   # 右下角点
    color=SHADOW,
    fill_opacity=0.5,
    stroke_opacity=0
