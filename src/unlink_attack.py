from manim import *
#from manim_voiceover import VoiceoverScene
#from manim_voiceover.services.recorder import RecorderService

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

class UnlinkAttack(Scene):#VoiceoverScene):

    chunks = VGroup()
    allocated_chunk = None
    fake_chunk = None
    stack = None
    previous_free_bit = None
    malloc = None
    arrows = None
    hackcode =  None

    def create_malloc(self):
        self.malloc = Code(file_name="./malloc.c",
                        tab_width=4, language="C", style="solarized-dark")
    def create_hack_code(self):
        self.hackcode = Code(file_name="./hackcode.c",
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
            if i == 4:
                height = 1.5

            rect = Rectangle(color=r_color, fill_opacity=1, width=2, height=height,stroke_color=RED_E,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.fake_chunk = VGroup(chunk_group, text_group)

    def create_fake_chunk_obj(self) -> VGroup:
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
        return VGroup(chunk_group, text_group)

    def create_stack(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ["", "" ,"" ,'chunk0_addr', 'chunk1_addr', '', '']
        for i in range(len(text)):
            r_color = GREEN
            height = 0.5
            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.stack = VGroup(chunk_group, text_group)

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


        indicator = SurroundingRectangle(self.malloc.code[0:7])
        # chunk definition
        self.play(
            FadeIn(indicator),
            Indicate(self.malloc.code[0:7])
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

        # 而如果 chunk1 的 presize 的低1位为0
        # 那么 chunk1, chunk2 将进行合并之后, 再进行释放.
        self.create_prev_free_bit()
        self.previous_free_bit.move_to(self.chunks[1][0][1], aligned_edge=RIGHT)
        self.add(self.previous_free_bit)

        self.play(
            self.previous_free_bit[0].animate.become(
                Text("0").scale(0.5).move_to(self.previous_free_bit.get_center())
        ))

        self.allocated_chunk.save_state()
        self.play(self.allocated_chunk.animate.shift(RIGHT*1))
        self.play(Restore(self.allocated_chunk))

        self.remove(self.previous_free_bit)

        self.play(FadeOut(self.malloc))

        self.create_hack_code()
        self.hackcode.scale(0.5).align_on_border(LEFT).shift(UP*2)
        self.add(self.hackcode)

        # about how to hack
        # what we need to do is, unlink ...
        indicator = SurroundingRectangle(self.hackcode.code[0:3])
        self.play(
            Create(indicator),
            Indicate(self.hackcode.code[0:3])
        )

        self.create_fake_chunk()
        self.fake_chunk.next_to(self.allocated_chunk[0][1], DOWN, buff=0)
        desc = Text("fake chunk",color=RED_E).scale(0.5).next_to(self.fake_chunk, LEFT, buff=0.1)
        self.add(desc)
        self.play(Create(self.fake_chunk))

        self.create_stack()
        self.stack.shift(LEFT*3.5)
        self.add(self.stack)

        fd_point_to_stack = Arrow(
            start=self.fake_chunk[0][2].get_left(),
            end=self.stack[0][0].get_right(),
            tip_length=0.15
        )
        bg_point_to_stack = Arrow(
            start=self.fake_chunk[0][3].get_left(),
            end=self.stack[0][1].get_right(),
            tip_length=0.15
        )

        self.play(
            Create(fd_point_to_stack),
            Create(bg_point_to_stack)
        )

        # 上面的两行代码,fake_chunk -> F -> B == B->F = chunk0_addr, 从而通过安全检查
        self.shift_code_indicator(3, indicator, self.hackcode)
        fake_obj = self.create_fake_chunk_obj()
        fake_obj.next_to(self.stack, LEFT, buff=0).align_to(self.stack,UP)
        self.add(fake_obj)
        self.play(
            Indicate(self.stack[0][3]),
            Indicate(fake_obj[0][3]),
        )

        self.play(fake_obj.animate.shift(DOWN*0.5))
        self.play(
            Indicate(self.stack[0][3]),
            Indicate(fake_obj[0][2]),
        )

        self.remove(fake_obj)

        # 接下来对要释放的 chunk1 的头部进行修改.及将presize修改为fakechunk的大小0x80,然后将最低位置为0
        # 让堆管理器认为 chunk0 下的 fake chunk 是空闲的. 从而可以让fakechunk和chunk1一起被释放掉.
        self.shift_code_indicator(5, indicator, self.hackcode, 3)
        self.add(self.previous_free_bit)
        self.play(Indicate(
            self.chunks[1][0:2]
        ))

        self.fake_chunk.save_state()
        self.play(self.fake_chunk.animate.shift(RIGHT))
        self.play(Restore(self.fake_chunk))

        # 最后咱们来到 unlink 的过程.
        self.shift_code_indicator(9,indicator, self.hackcode)
        chunk0_b_arrow = Arrow(
            start=self.fake_chunk[0][0].get_left(),
            end=self.stack[0][0],
            tip_length=0.15
        )
        chunk0_arrow = Arrow(
            start=self.chunks[0][0][2].get_left(),
            end=self.stack[0][3].get_right(),
            tip_length=0.15
        )
        self.play(
            fd_point_to_stack.animate.become(chunk0_b_arrow),
            Create(chunk0_arrow)
        )
        self.remove(bg_point_to_stack)
        self.remove(self.fake_chunk)

        self.wait()
