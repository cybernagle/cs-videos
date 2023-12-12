from manim import *

class ChordDiagram(Scene):
    def construct(self):
        # 创建一个圆
        circle = Circle(radius=2)
        self.play(Create(circle))

        # 创建和弦
        chords = [
            Line(circle.point_at_angle(i*2*PI/8), circle.point_at_angle(j*2*PI/8))
            for i in range(8)
            for j in range(i)
        ]

        # 添加和弦到场景
        self.play(*[Create(chord) for chord in chords])

        self.wait()
