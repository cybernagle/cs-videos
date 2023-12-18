import os
from manim import *

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.pyttsx3 import PyTTSX3Service


BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

code = """
for i in range(len(data)-1):
    if data[i] > data[i + 1]:
        data[i], data[i + 1] = data[i + 1], data[i]
"""
code3 = """
for j in range(len(data)):
    for i in range(len(data)-1-i):
        if data[i] > data[i + 1]:
            data[i], data[i + 1] = data[i + 1], data[i]
"""

class BubbleSort(VoiceoverScene):
    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND
    def computer_voice(self):
        self.set_speech_service(
            AzureService(
                voice="zh-CN-YunhaoNeural",
                style="newscast-casual",
            )
        )
    def human_voice(self):
        self.set_speech_service(
            AzureService(
                voice="zh-CN-XiaomengNeural",
                style="newscast-casual",
            )
        )

    def construct(self):
        data = [ 7, 4, 8, 3, 2, 6]
        squares = VGroup()
        numbers = VGroup()
        for i in range(6):
            squares.add(Square(side_length=0.5, color=OBJ_A, fill_opacity=1))

        squares.arrange(RIGHT)
        squares.move_to(ORIGIN).shift(DOWN)
        for i in range(len(data)):
            numbers.add(
                Text(str(data[i]), color=WORD_B).scale(0.5).move_to(squares[i].get_center())
            )

        # 创建用于交换正方形的函数
        def swap_squares(square1, square2):
            """交换两个正方形的位置"""
            posi1 = square1.get_center()
            posi2 = square2.get_center()
            with self.voiceover("交换") as tracker:
                self.play(
                    square1.animate.move_to(posi2),
                    square2.animate.move_to(posi1),
                    run_time=0.5
                )

        # 我是一台计算机
        # 这是我现在看到的内存的样子,他一片漆黑, 我不知道里面放了什么东西.
        self.computer_voice()
        with self.voiceover(text="我是一台计算机, <bookmark mark='A'/>这是我现在看到的内存的样子,他<bookmark mark='B'/>一片空白, 我不知道里面放了什么东西.") as tracker:
            self.wait_until_bookmark('A')
            self.play(FadeIn(squares))
            self.wait_until_bookmark('A')
            self.play(Wiggle(squares))

        # 而我需要让这个这块内存中中的数据按照从小到大的顺序进行排列
        # 怎么做呢?
        with self.voiceover(text="而我需要让这块内存中中的数据按照从小到大的顺序进行排列, 怎么做呢?最简单的,把所有的数据过一遍, 大的就放到前面.") as tracker:
            for i in range(len(squares)):
                self.play(Indicate(squares[i]))
        # 
        # 开始吧
        with self.voiceover(text="开始吧") as tracker:
            for i in range(5):
                self.play(FadeIn(numbers[i]), FadeIn(numbers[i + 1]))
                if data[i] > data[i + 1]:
                    self.play(Indicate(numbers[i]), Indicate(numbers[i + 1]))
                    swap_squares(numbers[i], numbers[i + 1])
                    temp = numbers[i]
                    numbers[i] = numbers[i + 1]
                    numbers[i + 1] = temp
                    data[i], data[i + 1] = data[i + 1], data[i]
                else:
                    self.wait(0.5)
                self.play(FadeOut(numbers[i]), FadeOut(numbers[i + 1]))
            target = VGroup(squares, numbers)

        simple_swap = Code(code=code, language="python").next_to(squares,UP, buff=0.5)

        # 我是一名程序员
        # 这是我写的一个排序程序
        self.human_voice()
        with self.voiceover(text="我是一名程序员,这是我写的一个<bookmark mark='A'/>排序程序") as tracker:
            self.wait_until_bookmark('A')
            self.play(FadeIn(simple_swap))
        
        code2 = """
        swapped=True
        for j in range(len(data)-1):
            if not swapped:
                return data
            swaped = False
            for i in range(len(data)-1):
                if data[i] > data[i + 1]:
                    data[i], data[i + 1] = data[i + 1], data[i]
                    swapped = True
        """
        # 但是显然, 任务没有完成, 于是我修改了程序
        more_swap = Code(code=code2, language="python").next_to(squares,UP, buff=0.5)
        with self.voiceover(text="但是显然, 任务没有完成, 于是我<bookmark mark='A'/>修改了程序") as tracker:
            self.wait_until_bookmark('A')
            self.play(Transform(simple_swap, more_swap))

        swapped = True
        swapped_f = Text("swapped = False", color=WORD_B).scale(0.5).next_to(squares, DOWN, buff=1)
        swapped_t = Text("swapped = True", color=WORD_B).scale(0.5).next_to(squares, DOWN, buff=1)
        self.computer_voice()
        # 我似乎多了一些新的逻辑, 一次排序不够,我将多次排序
        # 而且,多了一个交换swap检查,每次排序前 swap 都是False,如果发生了哪怕一次交换,swap 都修改为 True
        # 开始吧.
        with self.voiceover(text="我似乎多了一些新的逻辑, 一次排序不够,我将多次排序,而且,多了一个交换swap<bookmark mark='A'/>检查,每次排序前 swap 都是False,如果发生了哪怕一次交换,swap 都修改为 True, 开始吧<bookmark mark='B'/>") as tracker:
            self.wait_until_bookmark("A")
            self.play(FadeIn(swapped_t))
            self.wait_until_bookmark('B')
            for j in range(5):
                self.play(Circumscribe(more_swap.code[2]))
                self.play(Circumscribe(squares))
                self.wait()
                if not swapped:
                    self.play(Circumscribe(more_swap.code[4]))
                    break
                swapped = False
                self.play(
                    FadeOut(swapped_t), 
                    FadeIn(swapped_f)
                )
                for i in range(5):
                    self.play(Circumscribe(more_swap.code[7]))
                    self.play(FadeIn(numbers[i]), FadeIn(numbers[i + 1]),Circumscribe(numbers[i:i+2]))
                    if data[i] > data[i + 1]:
                        self.play(Circumscribe(more_swap.code[8:]))
                        self.play(Circumscribe(numbers[i]), Circumscribe(numbers[i + 1]))
                        swap_squares(numbers[i], numbers[i + 1])
                        temp = numbers[i]
                        numbers[i] = numbers[i + 1]
                        numbers[i + 1] = temp
                        data[i], data[i + 1] = data[i + 1], data[i]
                        self.play(Circumscribe(swapped_f))
                        if not swapped:
                            self.play(FadeOut(swapped_f), FadeIn(swapped_t))
                        swapped = True
                    else:
                        self.wait(0.5)
                    self.play(FadeOut(numbers[i]), FadeOut(numbers[i + 1]), run_time=0.5)

        with self.voiceover(text="没有一次交换, 我认为任务完成了.") as tracker:
            pass