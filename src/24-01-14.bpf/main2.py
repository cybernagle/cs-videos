from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService


BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

SHADOW="#D3D3D3"

"""
# 一个实例

我们知道内核一般分为用户态和内核态, 内核态将负责对硬件进行调度工作, 而用户态则根据内核态的各种系统调用, 来实现各种各样的应用程序和服务.

ebpf 程序, 会分为两个部分, 用户态代码, 另外一个部分内核态代码. 

用户态代码, 可以是 python ,可以是 rust, 内核态代码, 会被编译成 ebpf 虚拟机的字节码, 在 bpf 虚拟机当中运行. 

而用户态的程序, 可以通过 bpf map 来获取 bpf 字节码获取到的内容.

让我们来看一个例子:

```
bpf = r'''
int hello(void *ctx) {
    bpf_trace_printk("Hello World!");
    return 0;
}
'''

from bcc import BPF
b = BPF(text=bpf)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name="hello")

b.trace_print()
```

上面的程序可以被分为两个部分, 第一行 bpf 是 bpf 程序本身, 被编译后,会变成字节码在 bpf 虚拟机当中执行.
`b.get_syscall_fnname("execve")` 将这个字节码程序附加到了 execve 系统调用.
这样, 当操作系统每次执行 execve 的时候, bpf 虚拟机当中字节码就会被执行. 并且在标准输出打印 "Hello World!"

如下所示:

<video width="320" height="240" controls>
  <source src="ebpfhello.mov" type="video/mov">
</video>
"""

kcode = Code(
    "b1.py",
    tab_width=4,
    background_stroke_width=1,
    background_stroke_color=WHITE,
    insert_line_no=True,
    style=Code.styles_list[15],
    background="window",
    language="python",
).scale(0.5)

ucode = Code(
    "b2.py",
    tab_width=4,
    background_stroke_width=1,
    background_stroke_color=WHITE,
    insert_line_no=True,
    style=Code.styles_list[15],
    background="window",
    language="python",
).scale(0.5)

class BpfExample(VoiceoverScene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND

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
        kernel = Rectangle(width=2, height=2, color=OBJ_A).shift(LEFT*2)
        tkernel = Text("内核态").scale(0.5).next_to(kernel, UP)
        user = Rectangle(width=2, height=2, color=OBJ_B).shift(RIGHT*2)
        tuser = Text("用户态").scale(0.5).next_to(user, UP)
        os = VGroup(kernel, user, tkernel, tuser)
        package = Circle(radius=0.5, color=OBJ_C).next_to(kernel, LEFT)
        tpackage = Text("数据包").scale(0.3).move_to(package)
        gpackage = VGroup(package, tpackage)

        kcode.next_to(kernel, DOWN*1.5)

        # 接下来我们看看一个小的 ebpf 程序是什么样的. 我们知道内核一般分为用户态和内核态, 内核态将负责对硬件进行调度工作, 而用户态则根据内核态的各种系统调用.
        littleebpf = "接下来我们看看一个小的 eBPF 程序是什么样的. 我们知道内核一般分为用户态和内核态, 内核态<bookmark mark='A'/>将负责对硬件进行调度工作, 而用户态<bookmark mark='B'/>则根据内核态的各种系统调用实现各种服务或应用."
        with self.voiceover(text=littleebpf) as tracker:
            self.play(FadeIn(os))
            self.wait_until_bookmark("A")
            self.play(Indicate(kernel))
            self.wait_until_bookmark("B")
            self.play(Indicate(user))

        ucode.next_to(kcode, RIGHT)
        #ebpf 程序, 会分为两个部分, 用户态代码, 及内核态代码. 
        twopart = "eBPF 程序, 会分为两个部分, 用户态代码<bookmark mark='A'/>, 以及内核态<bookmark mark='B'/>代码. "
        with self.voiceover(text=twopart) as tracker:
            self.wait_until_bookmark("A")
            self.play(FadeIn(kcode))
            self.wait_until_bookmark("B")
            self.play(FadeIn(ucode))

        #前者可以是 c,rust, 经过编译后, 会转换为 ebpf 虚拟机的字节码, 在 bpf 虚拟机当中运行. 

        prev = "前者<bookmark mark='A'/>可以是 C,RUST, 经过编译后, 会转换为 eBPF 虚拟机的<bookmark mark='B'/>字节码, 在 bpf 虚拟机当中运行. "
        kkcode = kcode.copy()
        with self.voiceover(text=prev) as tracker:
            self.wait_until_bookmark("A")
            self.play(Indicate(kcode))
            self.wait_until_bookmark("B")
            self.play(kkcode.animate.scale(0.2).move_to(kernel))

        # 用户态的程序, 可以通过 bpf map 来获取 bpf 字节码获取到的内容.
        next = "用户态的<bookmark mark='A'/>程序, 可以通过 BPF map 来获取<bookmark mark='B'/>前者字节码所产生的内容."
        with self.voiceover(text=next) as tracker:
            self.wait_until_bookmark("A")
            self.play(Indicate(ucode))
            self.play(ucode.copy().animate.scale(0.1).move_to(user))
            arrow = Arrow(user.get_left(), kernel.get_right())
            self.wait_until_bookmark("B")
            self.play(GrowArrow(arrow))
        final = "最后让我们来看一下代码的运行结果, 可以看到, 当操作系统执行 EXECVE 的时候, BPF 虚拟机当中字节码就会被执行. 并且在标准输出打印 I'm BPF Program!!"
        with self.voiceover(text=final):
            pass
