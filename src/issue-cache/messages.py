from manim import *

class RotatingCircles(Scene):
    def construct(self):

        first = ImageMobject("./resource/1.png").scale(1.5)
        sec = ImageMobject("./resource/2.png").scale(1.5)
        thr = ImageMobject("./resource/3.png").scale(1.5)

        self.add(first)
        self.wait()
        self.add(sec)
        self.wait(2)
        self.add(thr)
        self.wait()
