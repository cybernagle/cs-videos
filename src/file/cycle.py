from manim import *
import random
import pickle

class RotatingCircles(Scene):
    rain = None
    def generate_rain(self, row = 5, column = 10, data=[[]]):
        rain = VGroup()
        row = 5
        column = 10
        for i in range(row):
            for j in range(column):
                num = data[i][j]
                binary = Text(str(num), color=GREEN).scale(0.3).shift(
                    LEFT * (column / 2 - j) * 0.3 + UP * (row / 2 - i) * 0.25
                )
                rain.add(binary)
        return rain

    def generate_cycle(self, inner_radius=1, outer_radius=1.5,color=GREEN):
        cycle = VGroup()
        for i in range(8):
            a = AnnularSector(inner_radius=inner_radius, outer_radius=outer_radius, angle=44.5 * DEGREES,start_angle=i*45*DEGREES ,color=color)
            cycle.add(a)
        return cycle

    # <a href="https://www.flaticon.com/free-icons/drive" title="drive icons">Drive icons created by srip - Flaticon</a>

    def construct(self):

        #data = [[]]
        #init = 0.1
        #for i in range(5):
        #    init = 0.1
        #    outer = init + 0.2
        #    data.append([init, outer])
        #    init+=0.21


        disks = ImageMobject("./resources/disks.png").scale(0.8).shift(LEFT*3)

        self.add(disks)

        prev_disk = AnnularSector(inner_radius=0.1, outer_radius=1.14, angle= 2*PI , color=GREEN).move_to(3 * LEFT)
        self.play(
            FadeIn(prev_disk),
            prev_disk.animate.move_to(3*RIGHT)
        )

        disk = VGroup()
        init = 0.1
        for i in range(5):
            inner = init
            outer = init+0.2
            s = self.generate_cycle(inner_radius=inner, outer_radius=outer,color=GREEN).move_to(3*RIGHT)
            #s = AnnularSector(inner_radius=inner, outer_radius=outer, angle= 2*PI , color=GREEN).move_to(3 * RIGHT)
            disk.add(s)
            s.move_to(disk)
            init+=0.21

        self.add(disk)
        self.play(FadeOut(prev_disk))
        self.wait()

        self.play(Indicate(disk[0][0]))

        self.play(FadeOut(disks))
        self.wait()

        matrix = [[]]
        with open('matrix.pkl', 'rb') as file:
            matrix = pickle.load(file)
        rain = self.generate_rain(row=5, column = 10, data = matrix).shift(3*LEFT)

        for i in range(5):
            digit = Text(str(matrix[0][i]), color=GREEN).next_to(disk, LEFT)
            self.play(Rotate(disk,angle=-45*DEGREES))
            self.play(FadeIn(digit))
            self.play(digit.animate.move_to(rain[i]).scale(0.3))

        self.add(rain)
        self.wait()
            
