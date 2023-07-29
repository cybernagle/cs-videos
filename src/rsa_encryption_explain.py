from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class RSAEncryption(Scene):
    def construct(self):

        # 当我们把个人的信息通过互联网发送的时候?信息是如何被加密的?

        # 假设我们发送的信息是一个!给到对方.
        # 从计算机的角度来看,它就是一个数字:33

        raw = Text("!", font_size=50)
        raw_ascii = Text("33",font_size = 50)

        self.play(Create(raw))
        self.play(raw.animate.become(raw_ascii))

        # 计算机在这个时候生成了两个很大的质数,为了方便大家运算,为了方便大家理解,我们取两个很小的值:5,7

        # 根据两个质数,我们首先得到它们的乘积:5*7=35, 记为N
        # 然后,我们将5-1,7-1相乘得到24,找到一个与24互质的数字,我们这里选择5,记为E
        # 再取最后一个数字,它的要求是和前面的E相乘之后,能和24的最大公约数是1.这里,我们取29

        # 酱紫,我们就得到了RSA加密过程当中需要的密钥:分为公钥E,N,私钥D,N
        # 回到我们要发送的信息感叹号,在经过ASCII转换成数字33.
        # 我们用私钥
