import os
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.pyttsx3 import PyTTSX3Service

class BubbleSort(VoiceoverScene):

    def construct(self):

        voiceses =  [
            {"voice": "zh-CN-XiaoxiaoNeural", "genda" : "Female"},
            {"voice": "zh-CN-YunxiNeural", "genda": "Male"},
            {"voice": "zh-CN-YunjianNeural", "genda": "Male"},
            {"voice": "zh-CN-XiaoyiNeural", "genda": "Female"},
            {"voice": "zh-CN-YunyangNeural", "genda": "Male" },
            {"voice": "zh-CN-XiaochenNeural", "genda":  "Female" },
            {"voice": "zh-CN-XiaohanNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaomengNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaomoNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaoqiuNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaoruiNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaoshuangNeural" ,"genda": "Female, Child" },
            {"voice": "zh-CN-XiaoxuanNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaoyanNeural" ,"genda": "Female" },
            {"voice": "zh-CN-XiaoyouNeural" ,"genda": "Female, Child" },
            {"voice": "zh-CN-XiaozhenNeural" ,"genda": "Female" },
            {"voice": "zh-CN-YunfengNeural" ,"genda": "Male" },
            {"voice": "zh-CN-YunhaoNeural" ,"genda": "Male" },
            {"voice": "zh-CN-YunxiaNeural" ,"genda": "Male" },
            {"voice": "zh-CN-YunyeNeural" ,"genda": "Male" },
            {"voice": "zh-CN-YunzeNeural" ,"genda": "Male" },
            #{"voice": "zh-CN-YunjieNeural1" ,"genda": "Male" },
        ]

        #{"voice": "zh-CN-XiaorouNeural1" ,"genda": "Female" },
        goodlook = "你今天真好看!"
        a = Text(goodlook)
        self.play(Create(a))

        x = 1
        for i in voiceses:
            self.set_speech_service(
                AzureService(
                    voice=i["voice"],
                    style="newscast-casual",
                )
            )
            voice = Text(str(x) + ": " + i["voice"], color=BLUE).scale(0.5).next_to(a, UP)
            self.add(voice)
            with self.voiceover(text="你今天真好看!" ) as tracker:
                pass
            self.wait()
            self.remove(voice)
            x += 1
