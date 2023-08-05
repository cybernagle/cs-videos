import math
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService


class PageLinkedListManagement(MovingCameraScene, VoiceoverScene):
    page_linked_list = VGroup()
    pages = VGroup()

    def init_pages(self) -> VGroup:
        table = Table(
            [["REF", "FLAGS", "PROPERTY"],
             ["P_LINK", "PRE_P_LINK", "PRE_VADDR"]],
            include_outer_lines=True,
            include_background_rectangle=True,
            background_rectangle_color=BLUE,
        ).move_to(self.square_mem[0].get_center()).scale_to_fit_width(self.square_mem[0].get_width()*1.2).set_stroke(width=0.2)

    def set_linked(self) -> VGroup:
        arrows = VGroup(*[
            DoubleArrow(
                obj.get_center()+0.05*RIGHT,
                obj.get_center() + 0.95*RIGHT,
                stroke_width=0.5,
            )
            for obj in self.pages
        ])
