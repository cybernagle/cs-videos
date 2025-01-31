from manim import *
from manim_voiceover import VoiceoverScene
from manim.scene.moving_camera_scene import MovingCameraScene
from manim_voiceover.services.azure import AzureService

# below code did not work
# import manimforge as mf
# mf.setup()

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

IMAGE="../../images"

SHADOW="#D3D3D3"


class QuantitativeEngineer(MovingCameraScene, VoiceoverScene):

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
        self.human_voice()

        people = ImageMobject(f"{IMAGE}/people-head-00.png").shift(UP)

        self.play(FadeIn(people))
        # self.interactive_embed()
        # 我们知道, 量化工程师无非是要选择买或者卖股票这种东西, 那么, 他们究竟量化的是什么东西?
        #  self.vo


