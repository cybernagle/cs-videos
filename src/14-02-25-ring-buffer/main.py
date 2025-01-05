from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService


BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

class RingBuffer():
    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND

        # https://github.com/torvalds/linux/blob/master/lib/kfifo.c
    def construct(self):

        """

        在内核当中, 当我们需要对数据进行传输的时候, 我们需要一个 buffer.

        传统来说, 我们需要放一个缓冲区在中间,作为过度, 这样能够避免数据丢失.
        对与这个缓冲区, 会面临两个操作,一个负责写, 一个负责读.
        那么我们就会面临多个问题:
        1. 如何保证写的速度和读的速度一致?
        2. 如何保证写的速度和读的速度不会超过缓冲区的大小?
        3. 脏数据的处理?

        为了解决这些问题, 我们引入了环形缓冲区.
        所谓环形缓冲区, 本质上就是一个缓冲区, 与一块普通的内存区域的区别在于, 如果写入数据超过了缓冲区的大小,
        缓冲区的指针会返回到最开始的缓冲区未知, 这让缓冲区在概念上形成了一个环形.

        而为了管理缓冲区, 我们需要引入两个指针, 一个负责跟踪读取, 一个负责跟踪写入



        """

        pass
