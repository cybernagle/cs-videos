from manim import *

# 1
class KernelIntro(Scene):

    def construct(self):

        computer = ImageMobject("./resources/laptop.png")

        self.add(computer)
        self.play(computer.animate.shift(LEFT*5))
        receiver = ImageMobject("./resources/laptop.png").next_to(computer, RIGHT, buff=6)
        self.play(FadeIn(receiver))

        temp_group = VGroup()

        hello = Text("你好")
        hello.save_state()
        hello.next_to(computer)
        self.add(hello)
        self.wait(1)
        self.play(hello.animate.next_to(receiver, LEFT))
        self.wait(0.5)
        self.play(Restore(hello))
        fbi = ImageMobject("./resources/fbi.png")
        video = ImageMobject("./resources/camera.png")
        self.wait(0.5)
        self.play(FadeOut(hello),FadeIn(fbi))
        self.wait(1)
        self.play(FadeOut(fbi), FadeIn(video))

        self.play(
            FadeOut(video),
            FadeOut(receiver)
        )
        self.play(computer.animate.shift(RIGHT*5))
        
        kernel = ImageMobject("./resources/linux.png")
        self.add(kernel.scale(0.5))
        self.play(kernel.animate.shift(RIGHT*3))
        self.wait()
