from manim import *

class Seventy(Scene):
    def construct(self):
        ten = VGroup()
        for i in range(10):
            ten.add(Circle(color=RED).scale(0.1).shift(RIGHT * i))

        ten.arrange()
        self.play(FadeIn(ten))
        self.wait()
        seven = VGroup()
        for i in range(7):
            seven.add(ten.copy())
        seven.arrange(DOWN)
        self.play(
            FadeOut(ten),
            FadeIn(seven)
        )
        #seven.shift(LEFT*3)
        
        self.play(seven.animate.scale(0.6).align_on_border(UL))

        s1 = seven.copy().next_to(seven, RIGHT, buff=1)
        s2 = seven.copy().next_to(s1, RIGHT, buff=1)

        s3 = seven.copy().next_to(seven, DOWN, buff=1)
        s4 = seven.copy().next_to(s3, RIGHT, buff=1)
        s5 = seven.copy().next_to(s4, RIGHT, buff=1)
        s6 = seven.copy().next_to(s3, DOWN, buff=1)

        self.play(FadeIn(s1))
        self.wait()
        self.play(FadeIn(s2))
        self.wait()
        self.play(FadeIn(s3))
        self.wait()
        self.play(FadeIn(s4))
        self.wait()
        self.play(FadeIn(s5))
        self.wait()
        self.play(FadeIn(s6))

        self.wait()