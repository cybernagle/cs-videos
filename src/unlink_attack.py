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


    def construct(self):
        self.create_allocate_chunk()
        self.allocated_chunk.shift(UP*2)
        self.chunks = VGroup(
            self.allocated_chunk.copy().shift(LEFT*4),
            self.allocated_chunk,
            self.allocated_chunk.copy().shift(RIGHT*4),
        )
        self.add(self.allocated_chunk)
        self.add(self.chunks)

        for i,v in enumerate(self.chunks):
            text = "chunk{}".format(i)
            self.add(Text(text).scale(0.5).next_to(v, UP))

        for i in range(2):
            curve_arrow = CurvedArrow(
                    start_point=self.chunks[i][0][3].get_right(),
                    end_point=self.chunks[i+1][0][3].get_left(),
                    radius=2,
                    tip_length=0.15
                )
            tip = curve_arrow.get_tip()
            curve_arrow.position_tip(tip, at_start=True)
            self.play(FadeIn(
                curve_arrow
            ))

        for i in reversed(range(2)):
            curve_arrow = CurvedArrow(
                    start_point=self.chunks[i+1][0][2].get_left(),
                    end_point=self.chunks[i][0][2].get_right(),
                    tip_length=0.15
                )
            tip = curve_arrow.get_tip()
            curve_arrow.position_tip(tip, at_start=True)

            self.play(FadeIn(
                curve_arrow
            ))

        self.create_fake_chunk()
        self.fake_chunk.next_to(self.allocated_chunk[0][3], DOWN, buff=0)
        self.play(Create(self.fake_chunk))
        self.wait()
