from manim import *

class Takeit(Scene):
    def construct(self):
        tex = Text("用一个事故", color=GREEN_E).shift(LEFT*2.8+UP*1).scale(2)#.rotate(angle=PI*0.1)
        img = ImageMobject("./resource/explosion.png").shift(RIGHT*2.8+UP*1)
        self.add(tex, img)
        self.add(Text("来讲讲文件系统", color=ORANGE).scale(2).shift(DOWN*1.5+LEFT*0.5))
