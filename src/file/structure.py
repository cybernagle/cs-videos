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

                binary = Text(str(num), color=GREEN).scale(0.3).shift(
                    LEFT * (column / 2 - j) * 0.3 + UP * (row / 2 - i) * 0.25
                )
                rain.add(binary)
        rain.add(binary)

        self.wait()
