from manim import *

# 2
class KernelInfo(Scene):

    def title(self):
        simu = Text("信息模拟与冯诺伊曼结构")
        self.play(AddTextLetterByLetter(simu))
        self.wait(0.5)
        self.play(FadeOut(simu))

    def text(self):
        a = Text("A")
        self.add(a)
        self.wait(1)
        binary = Text("01000001")
        self.play(Transform(a, binary))
        self.wait(1)
        self.remove(a)
        self.remove(binary)

    def color(self):
        red = Square(fill_opacity=1).set_color("#FF0000")
        self.add(red)
        self.wait(1)
        rgb = Text("#FF0000")
        self.play(Transform(red, rgb))
        binary = Text("111111110000000000000000")
        self.wait(1)
        self.play(Transform(red, binary))
        self.wait(1)
        self.remove(red, rgb, binary)
        self.wait()

    def construct(self):
        self.title()
        self.text()
        self.color()

        folder = ImageMobject("./resources/folder.png").scale(0.5).shift(LEFT*4)
        game = ImageMobject("./resources/gaming.png").scale(0.5).next_to(folder)
        video = ImageMobject("./resources/music.png").scale(0.5).next_to(game)
        music = ImageMobject("./resources/smartphone.png").scale(0.5).next_to(video)
        money = ImageMobject("./resources/income.png").scale(0.5).next_to(music)

        self.play(FadeIn(folder))
        self.play(FadeIn(game))
        self.play(FadeIn(video))
        self.play(FadeIn(music))
        self.play(FadeIn(money))

        
        



