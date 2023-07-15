from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class VulnerableCodeExplain(Scene):
    def construct(self):
        """
        这段代码有什么问题吗?
        让我们拆开来看
        """
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

        """
        程序是一个获取输入的代码.这段代码有什么问题吗?
        """
        self.play(Create(c_object))
        self.play(c_object.animate.shift(LEFT*3))


        asm = """
        sub    $0x30,%rsp
        lea    -0x30(%rbp),%rdi
        callq  400cb0 <Gets>
        """

        asm_object = Code(code=asm, language="C").scale(0.8)
        """
        我们看一下这行代码
        """
        self.play(Indicate(c_object.code[5], run_time=2))

        # 把它转换成汇编码
        self.play(asm_object.animate.shift(RIGHT*4))


        # 看不懂没关系,看看它在内存里面干了啥.
        self.play(Indicate(asm_object.code[1]))
        memory = Rectangle(color=BLUE, fill_opacity=0.1, width=2, height=4, grid_xstep=2.0, grid_ystep=0.5).shift(DOWN*0.25)
        """
        被编译后, 分为了几个模块被放入到内存当中.
        其中几个模块比较重要

        代码放在 text 段
        main 函数在调用该函数时存放地址在 stack 中.
        代码执行过程当中, 在 stack 中开辟一段空白空间长度为10, 用来存放 buffer.
        然后将 buffer 的内容输出.
        然后结束该函数.

        思考一个问题: 如果用户输入的 buffer 不仅仅是 10 的长度会发生什么问题?
        这个时候用户输入的内容在 buffer 向下扩展.覆盖掉了下面的代码.
        而前文当中, 我们知道, main 的返回地址存储在这里.
        而我们可以将 main 的返回地址覆盖掉.
        指向到任何我们想指向的地址.
        这样, 我们就完成了 buffer overflow 的逻辑.
        """
