from manim import *

class MmapIntro(Scene):
    def construct(self):
        # 建立这种映射关系, 我们将其称之为 mmap.
        relation = Tex(r"$ file \rightarrow .text \rightarrow virtual mem area $").shift(RIGHT*0.2)
        mmap = Text("mmap:").next_to(relation, LEFT).set_color(RED)
        self.play(Create(relation))
        self.play(FadeIn(mmap))
        self.wait()
