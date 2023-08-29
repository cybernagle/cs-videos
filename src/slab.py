from manim import *

class Slab(Scene):
    memory = VGroup()
    slabs = VGroup()
    yuanshen = ImageMobject("./yuanshen.jpg")
    wukong = ImageMobject("./blackmyth.jpg")
    bilibili = ImageMobject("./bilibli.jpg")
    def create_memory(self) -> VGroup:
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0
        for i in range(30):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=0.4, height=1,
                             grid_xstep=0.5, grid_ystep=1)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, RIGHT, buff=0)
            mem.add(rect)

        self.memory = mem

    def create_slabs(self):
        # 创建三个方块
        square1 = Square(side_length=1.3, fill_opacity=0.6, color=BLUE)
        square2 = Square(side_length=2, fill_opacity=0.6, color=BLUE)
        square3 = Square(side_length=4, fill_opacity=0.6, color=BLUE)

        # 设置方块位置
        distance = 4
        square1.next_to(square2, LEFT*distance)
        square3.next_to(square2, RIGHT*distance)

        # 创建四个长方形
        rectangles1 = VGroup(*[Rectangle(height=0.2, width=1, fill_opacity=0.5, color=RED) for _ in range(4)])
        rectangles2 = VGroup(*[Rectangle(height=0.2, width=1.8, fill_opacity=0.5, color=PURPLE) for _ in range(6)])
        rectangles3 = VGroup(*[Rectangle(height=0.2, width=3.8, fill_opacity=0.5, color=ORANGE) for _ in range(13)])

        # 设置长方形位置
        rectangles1.arrange(direction=UP,buff=0.1)
        rectangles1.move_to(square1)
        rectangles2.arrange(direction=UP,buff=0.1)
        rectangles2.move_to(square2)
        rectangles3.arrange(direction=UP,buff=0.1)
        rectangles3.move_to(square3)

        # 将方块和长方形添加到场景中
        self.slabs = VGroup(
            square1, square2, square3,
            rectangles1, rectangles2, rectangles3
        )

    def construct(self):
        # issue defi
        self.create_memory()
        self.memory.shift(LEFT*6)
        self.add(self.memory)
        self.wait()
        self.memory.save_state()
        #self.yuanshen.save_state()
        #self.wukong.save_state()
        self.play(
            FadeIn(self.yuanshen.shift(UP*2 + LEFT*3)),
            FadeIn(self.wukong.shift(UP*2+RIGHT*3)),
            FadeIn(self.bilibili.shift(UP*2+LEFT*0.3).scale(0.5))
        )
        self.wait()
        self.play(
            self.memory[0:5].animate.set_color(RED),
            self.memory[5:10].animate.set_color(ORANGE),
            self.memory[10:15].animate.set_color(YELLOW),
            self.memory[15:20].animate.set_color(GREEN),
        )

        self.wait()
        self.play(
            self.memory[5:10].animate.set_color(BLUE),
            FadeOut(self.bilibili)
        )
        self.wait()
        self.play(self.memory[20:27].animate.set_color(PURPLE))

        # 碎片
        self.play(
            Indicate(self.memory[5:10]),
            Indicate(self.memory[27:]),
        )


        # 当访问的对象越小的时候, 我们的碎片也就越多.
        self.play(
            self.memory[0:2].animate.set_color(RED_A),
            self.memory[3:6].animate.set_color(YELLOW),
            self.memory[7:11].animate.set_color(RED_B),
            self.memory[11:13].animate.set_color(GREEN),
            self.memory[15:19].animate.set_color(RED_C),
            self.memory[20:25].animate.set_color(PURPLE),
            self.memory[26:].animate.set_color(ORANGE),
        )

        self.play(
            Indicate(self.memory[2]),
            Indicate(self.memory[6]),
            Indicate(self.memory[13:15]),
            Indicate(self.memory[19]),
            Indicate(self.memory[25]),
        )
        self.wait()

        self.play(
            FadeOut(self.yuanshen),
            FadeOut(self.wukong),
        )
        self.yuanshen.shift(DOWN*2+RIGHT*3)
        self.wukong.shift(DOWN*2+LEFT*3)

        # issue resolveing 
        # 如何解决这些碎片呢?
        # 引入 buddy system
        self.play(
            self.memory.animate.shift(DOWN*3),
        )
        Restore(self.wukong)
        Restore(self.yuanshen)
        self.remove(self.wukong)
        self.remove(self.yuanshen)
        #self.play(
        #)

        self.create_slabs()

        self.slabs.shift(LEFT)
        self.add(self.slabs)
        self.play(
            self.memory[0:].animate.set_color(BLUE),
        )

        self.play(FadeIn(self.yuanshen.shift(LEFT+UP*2)))
        self.play(self.yuanshen.animate.shift(LEFT*2.7))

        self.play(
            self.memory[2].animate.set_color(RED)
        )
        self.play(
            Indicate(self.memory[2]),
            Indicate(self.slabs[3][2])
        )

        self.play(FadeIn(self.wukong.shift(LEFT+UP*2)))

        self.play(
            Indicate(self.slabs[3][2])
        )

        self.play(
            Indicate(self.memory)
        )

        self.wait()
