from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

script = """
如何记忆这一串数字?
我们需要一个手机<bookmark mark='A'/>解锁屏幕
和普通的解锁屏幕不同,我们给他<bookmark mark='B'/>编上号码
接下来, 我们将需要记忆的数字代入<bookmark mark='C'/>931621.
于是我们得出来一个<bookmark mark='D'/>镰刀形状的图案.
你记住<bookmark mark='E'/>了视频开头的数字了吗?
"""

class UnlockAnimation(VoiceoverScene):
    
    memorize_panel = None
    memorize_num = None

    def init_panel(self):
        circles = [Circle(radius=0.3, color=BLUE).shift(np.array([ j - 1,i - 1, 0])) for i in reversed(range(3)) for j in range(3)]
        circle_zero = Circle(radius=0.3, color=BLUE).shift(np.array([0,-2,0]))
        
        labels = [Text(str(i+1)).scale(0.5).move_to(circle.get_center()) for i, circle in enumerate(circles)] + [Text("0").scale(0.5).move_to(circle_zero.get_center())]
        self.memorize_num = VGroup(*labels)
        self.memorize_panel = VGroup(*circles, circle_zero)

    def construct(self):
        self.set_speech_service(RecorderService())
        with self.voiceover(text=script) as tracker:
            # 如何记忆这一串数字?
            num = Text("931621", color=RED)
            self.play(Create(num))
            self.play(num.animate.shift(UP * 2))
            self.init_panel()
            self.wait_until_bookmark('A')
            # 我们需要一个手机解锁屏幕
            self.play(
                FadeIn(self.memorize_panel),
            )
            #和普通的解锁屏幕不同,我们给他编上号码
            self.wait_until_bookmark('B')
            self.play(
                FadeIn(self.memorize_num),
            )

            #接下来, 我们将需要记忆的数字代入.
            self.wait_until_bookmark('C')
            path = VMobject(color=YELLOW)
            num_list = [
                self.memorize_panel[8],
                self.memorize_panel[2],
                self.memorize_panel[0],
                self.memorize_panel[5],
                self.memorize_panel[1],
                self.memorize_panel[0],
            ]
            path.set_points_as_corners([p.get_center() for p in num_list])
            self.play(Create(path), run_time=2)

            # 于是我们得出来一个镰刀形状的图案.
            self.wait_until_bookmark('D')
            self.play(FadeOut(self.memorize_panel),
                      FadeOut(self.memorize_num))

            # 你记住了视频开头的数字了吗?
            self.wait_until_bookmark('E')
            self.play(FadeOut(num))

