from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class VulnerableCodeExplain(VoiceoverScene):
    def construct(self):
        clang = """
unsigned long long getbuf()
{
  char buf[36];
  volatile char* variable_length;
  int i;
  unsigned long long val = (unsigned long long)Gets(buf);
        ...
  return val % 40;
}
void test()
{
  unsigned long long val;
  char* variable_length;
  val = getbuf();
}
        """
        c_object = Code(code=clang,
                    tab_width=4, background="window",
                     language="C", font="Monospace").scale(0.5)
        asm = """
        test function:           [0xFF00]
          push   %rbp
          ...
          callq get_buf          [0xFF05]
          cmp    $0x28,%rax
          ...

        get_buf function:        [0xFF15]
          push   %rbp
          mov    %rsp,%rbp
          sub    $0x30,%rsp
          lea    -0x30(%rbp),%rdi
          callq  400cb0 <Gets>
          ...
        """
        self.set_speech_service(RecorderService())

        asm_object = Code(code=asm, language="C").scale(0.8).shift(RIGHT*3.5)

        #这段代码有什么问题吗?

        with self.voiceover(text="你知道这段代码有什么问题?") as tracker:
            self.play(Create(c_object))
        with self.voiceover(text="首先它的逻辑很简单, <bookmark mark='A'/>test 函数会调用<bookmark mark='B'/> getbuf 函数, 再执行 <bookmark mark='C'/>Gets, 从而获得用户输入") as tracker:
            self.wait_until_bookmark("A")
            self.play(Indicate(c_object.code[9]))

            self.wait_until_bookmark("B")
            self.play(Indicate(c_object.code[0]))


            self.wait_until_bookmark("C")
            self.play(Indicate(c_object.code[5], run_time=2))

        self.play(c_object.animate.shift(LEFT*3.5))

        with self.voiceover(text="那么让我们看看机器它在干什么 <bookmark mark='A'/>这是编译后的代码") as tracker:
            self.wait_until_bookmark("A")
            self.play(Create(asm_object))
            self.play(FadeOut(c_object))
        self.play(asm_object.animate.shift(LEFT*3.5))

        with self.voiceover(text="机器按顺序从上到下执行 <bookmark mark='A'/>test 代码, 在执行到 <bookmark mark='B'/>call get_buf 时, CPU 跳转到 <bookmark mark='C'/>get buf 的地址执行") as tracker:
            self.wait_until_bookmark("A")
            for i in asm_object.code[1:3]:
                self.play(Indicate(i))
            self.wait_until_bookmark("B")
            self.play(Indicate(asm_object.code[3]))
            self.wait_until_bookmark("C")
            self.play(ApplyWave(asm_object.code[7]))

        # build a memory
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0fc0
        for i in range(10):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=2, height=0.5,
                      grid_xstep=2.0, grid_ystep=0.5)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, DOWN, buff=0)
            addr.next_to(rect, LEFT, buff=0.2)
            mem.add(rect)
            addresses.add(addr)
            start_addr += 8

        #with self.voiceover(text="这时机器将调用 get_buf 这行代码的地址<bookmark mark='A'>压入栈中. 假设被压到的地址是: <bookmark mark='B'> 1-0-0-0") as tracker:
        #    # bookmark A
        #    self.wait_until_bookmark("A")
        #    self.play(Indicate(asm_object.code[3][-8:]))

        mem_group = VGroup(mem, addresses)
        mem_group.shift(RIGHT*3+UP*2.5)

        self.play(
            asm_object.animate.shift(LEFT*2),
        )
        # 这个时候, 我们内存当中的栈空间被修改成了这个样子.
        with self.voiceover(text="这是我们栈空间") as tracker:
            self.play(
                Create(mem_group)
            )


        ret_addr = asm_object.code[3][-8:].copy()
        with self.voiceover(text="这时机器将调用 get_buf 这行代码的地址<bookmark mark='A'/>压入栈中. 假设被压到的地址是: <bookmark mark='B'/> 1-0-0-0") as tracker:
            self.wait_until_bookmark("A")
            self.play(Indicate(asm_object.code[3][-8:]))

            ret_addr = asm_object.code[3][-8:].copy()

            self.wait_until_bookmark("B")
            self.play(mem[8].animate.set_fill(RED))
            self.play(ret_addr.animate.move_to(mem[8].get_center()))


        #ret_addr.animate.move_to(mem[8].get_center())

        # 机器继续执行到<bookmark mark="A"> sub 0x30, $rsp
        with self.voiceover(text="机器继续执行到<bookmark mark='A'/> sub 0x30, $rsp") as tracker:
            for i in asm_object.code[7:10]:
                self.play(Indicate(i))
            self.wait_until_bookmark("A")
            self.play(Indicate(asm_object.code[10]))

        # 开辟了 0x30 的空间.
        b = Brace(mem[2:8], direction=RIGHT, buff=0.02)
        size = b.get_text("0x30")
        with self.voiceover(text="这样栈上就开辟了 30 大小的空间") as tracker:
            self.play(ApplyWave(mem[2:8]))
            self.play(GrowFromCenter(b),Write(size))

        # 接着执行到 Get, 最后将内容放到这个 0x30 的空间当中.
        with self.voiceover(text="接着执行到 Get, 最后将内容放到这个 30 大小的空间当中.") as tracker:
            self.play(Indicate(asm_object.code[11]))
            self.play(Indicate(asm_object.code[12]))
            self.play(mem[2:8].animate.set_fill(YELLOW))

        with self.voiceover(text="问题在这个时候出现了.如果我们输入的内容, 超出了 <bookmark mark='A'/>0x30 的区域, 那么, <bookmark mark='B'/>返回地址将会被覆盖.") as tracker:

            self.wait_until_bookmark("A")
            self.play(Indicate(mem[8:]))

            self.wait_until_bookmark("B")
            self.play(mem[8:].animate.set_fill(YELLOW))

        mem_group.add(b)
        mem_group.add(ret_addr)

        malicious_code = """
        int malicious_code() {
            # 修改你的游戏血量
            change_your_health_point()
        }
        """
        malicious_code_object = Code(code=malicious_code,
                    tab_width=4, background="window",
                     language="C", font="Monospace")

        self.play(FadeOut(asm_object), mem_group.animate.shift(LEFT*6))
        with self.voiceover(text="这也就意味着, 我们可以<bookmark mark='A'/>写一段危险的代码放在内存, 然后把返回地址<bookmark mark='B'/>指向过来, 从而可以做到很多不干净的事情. 比如说, 修改你的血量.") as tracker:
            self.wait_until_bookmark("A")
            self.play(malicious_code_object.animate.next_to(mem_group,RIGHT, buff=1))
            pointer = Arrow(mem[8], malicious_code_object, buff=0.1, color=YELLOW)
            self.play(FadeOut(ret_addr))

            malicious_addr = Text(hex(0x1234),font_size=20).move_to(mem[8].get_center())
            self.wait_until_bookmark("B")
            self.play(Create(malicious_addr))
            self.play(GrowArrow(pointer))

