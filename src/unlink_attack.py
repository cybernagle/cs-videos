from manim import *
from manim_data_structures import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

code = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHUNK_SIZE 0x80

int main(){
  unsigned long long *chunk1, *chunk2;
  char data[20] = "";

  chunk1 = (unsigned long long*) malloc(CHUNK_SIZE);
  if(chunk1 == NULL) {
    printf("Failed to allocate memory for chunk1\n");
    return 1;
  }

  chunk2 = (unsigned long long*) malloc(CHUNK_SIZE);
  if(chunk2 == NULL) {
    free(chunk1);
    printf("Failed to allocate memory for chunk2\n");
    return 1;
  }

  free(chunk2);

  chunk1[3] = (unsigned long long)data;
  strcpy(data, "Victim's data");
  chunk1[0] = 0x002164656b636168LL;
  printf("%s\n", data);

  free(chunk1);
  return 0;
}
"""

class UnlinkAttack(VoiceoverScene):

    chunks = VGroup()
    allocated_chunk = None
    fake_chunk = None
    stack = None
    previous_free_bit = None
    malloc = None
    arrows = None

    def create_malloc(self):
        self.malloc = Code(file_name="./malloc.c",
                        tab_width=4, language="C", style="solarized-dark")
    def create_prev_free_bit(self):
        bit = Square(
            side_length=0.5,
            fill_opacity=0.5,
            color=RED_E,
            stroke_color=RED_E,
            background_stroke_color=RED_E
        )
        text = Text("P", color=WHITE).scale(0.5).move_to(bit)
        prev_free_bit = VGroup(text,bit)
        self.previous_free_bit = prev_free_bit 

    def create_allocate_chunk(self) -> VGroup:
        chunk_group = VGroup()
        text_group = VGroup()
        text = ['size',"presize", "F", "B", "data"]
        for i in range(5):
            r_color = BLUE
            height = 0.5

            # yellow area is chunk header
            if i <= 1:
                r_color = YELLOW

            # data block should much bigger
            if i == 4:
                height = 2.5

            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)

        chunk = VGroup(chunk_group, text_group)
        self.allocated_chunk = chunk
    def create_fake_chunk(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ['size', 'presize', 'F', 'B', 'data']
        for i in range(5):
            r_color = BLUE
            height = 0.5

            # yellow area is chunk header
            if i <= 1:
                r_color = RED

            rect = Rectangle(color=r_color, fill_opacity=1, width=2, height=height,stroke_color=RED_E,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.fake_chunk = VGroup(chunk_group, text_group)

    def create_stack(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ['chunk1_addr', 'chunk2_addr', '', 'B', 'data']
        for i in range(5):
            r_color = BLUE
            height = 0.5

            # yellow area is chunk header
            if i <= 1:
                r_color = RED

            rect = Rectangle(color=r_color, fill_opacity=1, width=2, height=height,stroke_color=RED_E,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.fake_chunk = VGroup(chunk_group, text_group)

    def shift_code_indicator(self, index, source,target , size=1):
        if size <= 1:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index])),
                Indicate(target.code[index])
            )
        else:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index:index+size])),
                Indicate(target.code[index:index+size])
            )

    def construct(self):
        all = VGroup()
        self.create_malloc()
        self.malloc.scale(0.5).align_on_border(UP)
        self.add(self.malloc)

        # chunks
        self.create_allocate_chunk()
        self.malloc.save_state()


        indicator = SurroundingRectangle(self.malloc.code[0:8])
        # chunk definition
        self.play(
            FadeIn(indicator),
            Indicate(self.malloc.code[0:8])
        )

        # free 代码的关键代码讲解
        self.shift_code_indicator(12,indicator, self.malloc)
        self.shift_code_indicator(14,indicator, self.malloc)
        self.shift_code_indicator(16,indicator, self.malloc)
        self.shift_code_indicator(24,indicator, self.malloc)
        self.shift_code_indicator(35,indicator, self.malloc, 2)
        self.remove(indicator)

        # restore state
        self.play(Restore(self.malloc))
        self.malloc.shift(LEFT*3)
        self.allocated_chunk.shift(UP*2+RIGHT*2)
        self.play(Transform(self.malloc.code[0:8].copy(),self.allocated_chunk))

        self.chunks = VGroup(
            self.allocated_chunk,
            self.allocated_chunk.copy().shift(RIGHT*3),
        )

        self.add(self.chunks[1])

        # chunk desc 
        text_group = VGroup()
        for i,v in enumerate(self.chunks):
            text = "chunk{}".format(i)
            tmp = Text(text).scale(0.5).next_to(v, UP)
            text_group.add(tmp)
            self.add(tmp)

        # chunk double link arrows
        arrows = VGroup()
        right_arrow = CurvedArrow(
                start_point=self.chunks[0][0][3].get_right(),
                end_point=self.chunks[1][0][3].get_left(),
                radius=2,
                tip_length=0.15
            )
        tip = right_arrow.get_tip()
        right_arrow.position_tip(tip, at_start=True)
        self.play(FadeIn(
            right_arrow
        ))
        arrows.add(right_arrow)

        left_arrow = CurvedArrow(
            start_point=self.chunks[1][0][2].get_left(),
            end_point=self.chunks[0][0][2].get_right(),
            tip_length=0.15
        )
        tip = left_arrow.get_tip()
        left_arrow.position_tip(tip, at_start=True)

        self.play(FadeIn(
            left_arrow
        ))
        arrows.add(left_arrow)

        # 假设我们要释放 chunk2
        self.play(Indicate(self.chunks[1]))
        # normal unlink
        arrows.save_state()

        p = Point(location=self.chunks[1][0][2].get_center()).shift(RIGHT*5)
        self.add(p)
        unlinked_right_arrow = CurvedArrow(
            start_point=self.chunks[0][0][3].get_right(),
            end_point=p.get_center(),
            tip_length=0.15
        )
        tip = unlinked_right_arrow.get_tip()
        unlinked_right_arrow.position_tip(tip, at_start=True)

        self.play(Transform(arrows[0],unlinked_right_arrow))

        unlinked_left_arrow = CurvedArrow(
            start_point=p.get_center(),
            end_point=self.chunks[0][0][2].get_right(),
            tip_length=0.15
        )
        tip = unlinked_left_arrow.get_tip()
        unlinked_left_arrow.position_tip(tip, at_start=True)
        self.play(Transform(arrows[1],unlinked_left_arrow))

        # 并且, 我们在释放前会检查两个指针是不是指向了正确的位置.
        self.play(Indicate(self.chunks[1]))
          
        self.play(Restore(arrows))

        # what we need to do is, unlink ...
        self.create_fake_chunk()
        self.fake_chunk.next_to(self.allocated_chunk[0][3], DOWN, buff=0)
        desc = Text("FAKE",color=RED_E).scale(0.3).next_to(self.fake_chunk, RIGHT)
        self.add(desc)
        self.play(Create(self.fake_chunk))

        self.create_prev_free_bit()
        self.previous_free_bit.move_to(self.chunks[1][0][1], aligned_edge=RIGHT)
        self.add(self.previous_free_bit)

        self.play(
            self.previous_free_bit.animate.become(
                Text("0").scale(0.5).move_to(self.previous_free_bit.get_center())
        ))
        self.wait()

        self.play(FadeOut(self.malloc))
        # but ,how to pass security check?

        # unlink
        self.wait()
