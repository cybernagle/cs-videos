from manim import *
import pickle
import random

class FileStructure(Scene):
    def construct(self):

        row = 31
        column = 47

        matrix = [[]]

        # 加载二维矩阵
        with open('matrix.pkl', 'rb') as file:
            matrix = pickle.load(file)

        rain = VGroup()
        for i in range(row):
            for j in range(column):
                num = matrix[i][j]

                binary = Text(str(num), color="#008000", weight=BOLD ,fill_opacity=0.6).scale(0.8).shift(
                    LEFT * (column / 2 - j) * 0.8 + UP * (row / 2 - i) * 0.7
                )
                rain.add(binary)
        rain.add(binary)
        self.add(rain)

        a = Text("一切皆", color=YELLOW).scale(2).shift(LEFT*2)

        self.add(a)
        b = Text("文件!", color=ORANGE).scale(3).next_to(a, RIGHT)
        self.add(b)
        #self.add(Text("是什么?", color=YELLOW).scale(2).next_to(b, RIGHT, buff=0.2))

