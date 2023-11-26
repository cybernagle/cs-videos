from manim import *

# 2
class KernelCover(Scene):
    def construct(self):
        kernel = ImageMobject("./resources/linux.png").shift(LEFT*3.5)
        name = Text("Kernel\nIntroduction",color=ORANGE).scale(2).next_to(kernel, RIGHT, buff=0)
        #intro = Text("").scale(2).next_to(kernel, RIGHT, buff=0)
        self.add(kernel, name)#, intro)

    
