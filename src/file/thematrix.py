from manim import *
import random
import pickle

class TheMatrix(Scene):

    def generate_rain(self, row = 5, column = 10, data=[[]]):
        rain = VGroup()
        row = 5
        column = 10
        for i in range(row):
            for j in range(column):
                num = data[i][j]
                binary = Text(str(num), color="#008000", weight=BOLD).scale(0.3).shift(
                    LEFT * (column / 2 - j) * 0.3 + UP * (row / 2 - i) * 0.25
                )
                rain.add(binary)
        return rain

    def construct(self):
        matrix = [[]]
        with open('matrix.pkl', 'rb') as file:
            matrix = pickle.load(file)
        rain = self.generate_rain(row=5, column = 10, data = matrix).shift(3*LEFT)

        copies = VGroup()
        for i in range(400):
            copies.add(rain.copy())
                
        copies.arrange_in_grid(20, 20, buff=0.3)

        self.add(copies.scale(0.5))

        self.wait()
