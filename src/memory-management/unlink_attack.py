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


        # 首先我们来阅读一下 glibc 当中, 关于管理内存单元的结构以及释放的关键性代码.
        # 可以看到我们的每个单元由数据结构 malloc_chunk 来进行管理,
        # 其包含一个上一个 chunk 的大小, 当前大小以及指向前驱节点以及后驱节点的指针.
        # 这里, 我们就可以知道,malloc 得到的数据结构是一个双向链表.
        indicator = SurroundingRectangle(self.malloc.code[0:7])
        # chunk definition
        self.play(
            FadeIn(indicator),
            Indicate(self.malloc.code[0:7])
        )

        # 继续向下, 我们可以看到 free 的代码, 在free 的过程当中,会判断上一个节点是否是inuse的状态.
        self.shift_code_indicator(12,indicator, self.malloc)
        # 如果没有,那么当前节点和前一个节点将会进行合并.
        self.shift_code_indicator(14,indicator, self.malloc)
        # 然后, 使用unlink宏,将合并后的节点进行释放.
        self.shift_code_indicator(16,indicator, self.malloc)

        # 而释放的过程页很简单, 在判定前后两个节点是否指向释放节点本身后.
        self.shift_code_indicator(24,indicator, self.malloc)

        # 将双向链表重新进行链接,从而释放该区域.
        self.shift_code_indicator(35,indicator, self.malloc, 2)
        self.remove(indicator)

        # 接下来, 我们将这些数据结构可视化,看看对应代码具体执行了什么事情.
        # restore state
        self.play(Restore(self.malloc))
        self.malloc.shift(LEFT*3)
        self.allocated_chunk.shift(UP*2+RIGHT*2)
        # 首先, 是我们的内存块管理单元.
        # 这个内存块管理单元当中, 黄色区域是chunk 的头,而蓝色部位是chunk的数据节点本身.
        # 当我们访问 chunk 的地址的时候,一般指向的,都是chunk的数据节点本身.
        self.play(Transform(self.malloc.code[0:8].copy(),self.allocated_chunk))

        # 假设我们现在申请了两个内存单元, chunk0, chunk1
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
        # 申请了之后,它们将会链接起来.chunk1 的F就是chunk0,
        # chunk0的B就是chunk1
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

        # 如果我们要释放 chunk1
        self.play(Indicate(self.chunks[1]))
        # normal unlink
        arrows.save_state()

        p = Point(location=self.chunks[1][0][2].get_center()).shift(RIGHT*5)
        self.add(p)
        # 那么 chunk0 的B将会指向chunk1 的后继节点.而chunk1的后继节点将会指向chunk0
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

        # 并且, 我们在释放前会再次确认被释放的前驱节点的后继节点是我自己.
        # 以及后继节点的前驱节点是我自己.
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

        # 上面我们讲了正常释放的逻辑, 接下来我们看看该漏洞会以怎样的形式被利用.
        self.play(FadeOut(self.malloc))

        # 我们还是用代码的形式来进行演示.
        self.create_hack_code()
        self.hackcode.scale(0.5).align_on_border(LEFT).shift(UP*2)
        self.add(self.hackcode)

        # about how to hack
        # what we need to do is, unlink ...
        # 首先, 这个代码块的前三行在 chunk0 的位置创建了一个fakechunk.
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

        # 并且申请了两个地址放在了 fakechunk 的前后指针当中.
        # 这两个指针作为变量都位于栈上.
        # 这里注意看, fakechunk的F也就是前驱是相较于 chunk0 向上的两个位置.
        # fakechunk的 B 也就是后继, 是相较于 chunk0 向上的三个位置.
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

        # 而这两行代码,fake_chunk -> F -> B == B->F = chunk0_addr
        # 就可以保证fakechunk它的前驱的后继,以及后继的前驱是指向自己fakechunk本身.从而通过安全检查.
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

        # 接下来咱们对要释放的 chunk1 的头部进行修改.即将presize修改为fakechunk的大小0x80,然后将最低位置为0
        # 让堆管理器认为 chunk0 下的 fake chunk 是空闲的. 从而可以让fakechunk和chunk1一起被释放掉.
        self.shift_code_indicator(5, indicator, self.hackcode, 3)
        self.add(self.previous_free_bit)
        self.play(Indicate(
            self.chunks[1][0:2]
        ))

        self.fake_chunk.save_state()
        self.play(self.fake_chunk.animate.shift(RIGHT))
        self.play(Restore(self.fake_chunk))

        # 最后, 咱们来到 unlink 的过程.即将fake_chunk 的前驱节点的后继节点.
        # 在我们的视频当中, fake_chunk 的前驱节点是chunk0 - 3
        # 而在malloc_chunk的数据结构告诉我们,后继节点是存储在其起始地址+3的位置,
        # 也就是存储我们的chunk0地址的位置.
        # 这样,chunk0 的前驱节点也就是 chunk0-3 的位置, 指向了chunk0 本身.
        # 也就是意味着,我们访问chunk0 的时候,就是在访问chunk0-3的栈上面的位置.
        # 这样,我们就可以通过chunk0来访问本不该能够访问的栈地址而完成了hack.
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
