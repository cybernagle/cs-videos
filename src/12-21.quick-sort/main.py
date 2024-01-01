from manim  import *
from manim.typing import Vector3

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

# quick sort 
import random

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"
 
class Element(VGroup):

    number = 0
    square = None
    text = None
    oposition  = None
    sposition = None

    def __init__(self, number=0,color=BLUE,fill_opacity=1,side_length: float = 2,**kwargs) -> None:
        super().__init__(**kwargs)
        self.number = number
        self.square = Square(side_length=side_length, fill_opacity=fill_opacity, color=color, **kwargs)
        self.text = Text(str(self.number)).scale(0.5).move_to(self.get_center())
        self.add(self.square,self.text)

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        if not isinstance(other, Element):
            return NotImplementedError
        return self.number == other.number

    def __gt__(self, other):
        if not isinstance(other, Element):
            return NotImplementedError
        return self.number > other.number

    def __lt__(self, other):
        if not isinstance(other, Element):
            return NotImplementedError
        return self.number < other.number

    def set_number(self, number):
        self.number = number
        self.text = Text(str(self.number)).scale(0.5).move_to(self.get_center())

    def get_number(self):
        return self.number

class QuickSort(VoiceoverScene):

    stack = VGroup()

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

    def quicksort(self,arr,position=UP*3):
        if len(arr) <= 1:
            return arr
        pivot = arr[0]

        pivot.square.set_color(OBJ_C).set_z_index(2)
        pivot.text.set_z_index(3)
        tpivot = Text("pivot").scale(0.3).next_to(pivot, UP)
        self.add(tpivot)
        with self.voiceover(text="中间数") as tracker:
            self.play(FadeOut(tpivot))
            self.play(pivot.animate.next_to(position, UP*0.5))

        pleft = position.copy() + LEFT + DOWN
        pright = position.copy() + RIGHT + DOWN

        smaller = VGroup()
        larger = VGroup()

        for i in arr:
            if i < pivot:
                smaller.add(i)
        for i in arr:
            if i > pivot:
                larger.add(i)

        leftarrow = Arrow(start=position+UP*0.2, end=pleft+UP*0.5, buff=0.1, color=GOLD, max_tip_length_to_length_ratio=0.1)
        rightarrow = Arrow(start=position+UP*0.2, end=pright+UP*0.5, buff=0.1, color=GOLD, max_tip_length_to_length_ratio=0.1)

        self.add(
            leftarrow,
            rightarrow
        )
        self.wait()
        tsmaller = Text("quick(smaller)").scale(0.3).next_to(pivot, LEFT)
        tlarger = Text("quick(larger)").scale(0.3).next_to(pivot, RIGHT)
        self.stack.add(tsmaller, tlarger)


        with self.voiceover(text="小的数.") as tracker:
            self.add(tsmaller)
            self.play(smaller.animate.arrange(buff=0.1).move_to(pleft))

        with self.voiceover(text="大的数.") as tracker:
            self.add(tlarger)
            if len(smaller) > 1:
                self.play(larger.animate.arrange(buff=0.1).next_to(smaller, RIGHT , buff=1))
            else:
                self.play(larger.animate.arrange(buff=0.1).move_to(pright))

        self.wait(0.5)
        ssmaller = self.quicksort(smaller, position=pleft)
        slarger = self.quicksort(larger, position=pright)
        new = VGroup()
        for i in ssmaller:
            new.add(i)
        new.add(pivot)
        for i in slarger:
            new.add(i)
        return new

    def construct(self):
        self.computer_voice()
        # generate 10 random numbers between 1-100 , and put them in Square
        data = [86,66,31,43,68,69,83,79,22,8] #[random.randint(1, 100) for i in range(10)]
        squares = VGroup()
        for i in data:
            s = Element(number=i,side_length=0.5, color=OBJ_A, fill_opacity=1)
            squares.add(s)
        squares.arrange(RIGHT, buff=0.1).move_to(ORIGIN)

        with self.voiceover(text="我是一台计算机,需要将以下n个数字进行从小到大排序.") as tracker:
            self.play(FadeIn(squares))
        with self.voiceover(text="首先,我将选择第一个数, 根据它来将所有的数分成两个部分.一部分数较之大,一部分较之小.重复这一步知道所有的数分开, 让我们开始吧.") as tracker:
            self.wait()

        sorted = self.quicksort(squares, UP*2)
        position: Vector3 = np.array((-4.0, 3.3, 0.0))
        

        i = 0
        with self.voiceover(text="所有的数都分开后, 每一个函数都按照之前的顺序返回, 这样我们就得到了拍好了顺序的数字.") as tracker:
            for v in sorted:
                self.play(v.animate.move_to(position+RIGHT*i))
                i+=1
        
        complexlgn = Line(start=UP*3+LEFT*5, end=DOWN*3+LEFT*5,color=RED).set_z_index(3)
        tcomplexlgn = MathTex("\log n").scale(0.8).next_to(complexlgn, LEFT).set_z_index(3)
        complexn = Line(start=DOWN * 3 + LEFT*5, end=DOWN * 3 + RIGHT*5, color=RED).set_z_index(3)
        tcomplexn = MathTex("n").scale(0.8).next_to(complexn, DOWN).set_z_index(3)

        #self.play(GrowFromCenter(complexlgn), GrowFromCenter(tcomplexlgn), GrowFromCenter(complexn), GrowFromCenter(tcomplexn))
        
        with self.voiceover(text="这样, 我每一次都查看了所有的n个数字,因为我每一次都将数据分为2 ,所以我的高度是 log n,那么, 我一共要执行 n 乘以 log n 次.") as tracker:
            self.add(complexlgn, tcomplexlgn, complexn, tcomplexn)

        self.clear()

        with self.voiceover(text="那么这样做有问题吗? 让我们来看另外一个情况.") as tracker:
            self.wait()
        # another situation
        data = [99, 98, 97, 96, 95, 94]
        badsituation = VGroup()
        for i in data:
            s = Element(number=i,side_length=0.5, color=OBJ_B, fill_opacity=1)
            badsituation.add(s)

        with self.voiceover(text="这是另外一堆数字, 让我们仍然每次选择第一个数字将其分为两堆.开始吧!") as tracker:
            badsituation.arrange(RIGHT, buff=0.1).move_to(ORIGIN)
            self.play(FadeIn(badsituation))
        badsorted = self.quicksort(badsituation, UP*2)
        i = 0

        with self.voiceover(text="像上次一样,我的每一个函数都按照之前的顺序返回并得到拍好顺序的数字.") as tracker:
            for v in badsorted:
                self.play(v.animate.move_to(position+RIGHT*i))
                i+=1
        
        lgbn = Line(start=UP*3+LEFT*6, end=DOWN*3+LEFT*6, color=RED).set_z_index(3)
        tlgbn = MathTex("n").scale(0.8).next_to(lgbn, LEFT).set_z_index(3)
        bn = Line(start=DOWN * 3 + LEFT*6, end=DOWN * 3 + RIGHT*3, color=RED).set_z_index(3)
        tbn = MathTable("n").scale(0.8).next_to(bn, DOWN).set_z_index(3)

        with self.voiceover(text="而这一次,我们可以看到数字每次都是更小,所以每一次的分堆的情况,都是一堆,所以,我们每次遍历的数字仍然是n,但是我们由于没有将数组进行过1次二分, 所以高度也是n.这样, 我们的算法复杂度就变成了 n 平方") as tracker:
            self.add(lgbn, tlgbn, bn, tbn)

        self.wait() 