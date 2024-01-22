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

    def construct(self):

        kernel = Rectangle(width=2, height=2, color=OBJ_A).shift(LEFT*2)
        tkernel = Text("内核态").scale(0.5).next_to(kernel, UP)
        user = Rectangle(width=2, height=2, color=OBJ_B).shift(RIGHT*2)
        tuser = Text("用户态").scale(0.5).next_to(user, UP)
        os = VGroup(kernel, user, tkernel, tuser)
        package = Circle(radius=0.5, color=OBJ_C).next_to(kernel, LEFT)
        tpackage = Text("数据包").scale(0.3).move_to(package)
        gpackage = VGroup(package, tpackage)

        kcode.next_to(kernel, DOWN*1.5)

        #内核一般分为用户态和内核态, 内核态将负责对硬件进行调度工作, 而用户态则根据内核态的各种系统调用.
        self.play(FadeIn(os))

        #ebpf 程序, 会分为两个部分, 用户态代码, 及内核态代码. 
        self.play(FadeIn(kcode))

        ucode.next_to(kcode, RIGHT)

        self.play(FadeIn(ucode))

        #前者可以是 c,rust, 经过编译后, 会转换为 ebpf 虚拟机的字节码, 在 bpf 虚拟机当中运行. 
        self.play(Indicate(kcode))
        kkcode = kcode.copy()
        self.play(kkcode.animate.scale(0.1).move_to(kernel))

        # 用户态的程序, 可以通过 bpf map 来获取 bpf 字节码获取到的内容.
        self.play(Indicate(ucode))
        self.play(ucode.copy().animate.scale(0.1).move_to(user))
        arrow = Arrow(user.get_left(), kernel.get_right())
        self.play(GrowArrow(arrow))

        #上面的程序可以被分为两个部分, 第一行 bpf 是 bpf 程序本身, 被编译后,会变成字节码在 bpf 虚拟机当中执行.
        #`b.get_syscall_fnname("execve")` 将这个字节码程序附加到了 execve 系统调用.
        #这样, 当操作系统每次执行 execve 的时候, bpf 虚拟机当中字节码就会被执行. 并且在标准输出打印 "Hello World!"
        #
        #如下所示:
        #
        #<video width="320" height="240" controls>
        #  <source src="ebpfhello.mov" type="video/mov">
        #</video>
