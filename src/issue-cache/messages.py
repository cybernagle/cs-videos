from manim import *

class RotatingCircles(Scene):
    def construct(self):

        resource = [
            "./resource/1.png",
            "./resource/2.png",
            "./resource/3.png",
            "./resource/4.png",
            "./resource/5.png",
            "./resource/6.png",
        ]

        for i in range(len(resource)):
            self.add(ImageMobject(resource[i]).scale(1.5))
            self.wait()

        #self.add(first)
        #self.wait()
        #self.add(sec)
        #self.wait(2)
        #self.add(thr)
        #self.wait()
