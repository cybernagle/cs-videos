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
# BPF 是什么?

它可以安全高效地扩展内核的能力而无需修改内核源代码或加载内核模块。
它可以监控内核中的网络流量，并根据流量类型进行流量控制。
它可以在程序运行时, 动态的植入监控点,获取运行时的状态.
它叫做 ebpf.

# BPF 历史 

在 1993 年, 一篇论文 ("The BSD Packet Filter: A New Architecture for User-level Packet Capture" 在屏幕上显示这个, 并翻译成中文) 
描述了如何解决数据包的抓取过程当中, 在内核态和用户态之间的数据复制导致了大量的性能损耗问题.(一个图, 从内核态流动到用户态, 判断, drop , 或者流给用户)

文中提到了的解决方案是, 在内核态当中,使用自定义的指令来对数据包进行过滤的功能. 并将这种解决方案被称之为: BPF
(一个图, 从在内核态进行判断, drop , 或者直接给到用户)

1997 年, linux kernel 2.1.75 在内核当中实现了一个小的 bpf 的虚拟机,用于执行 bpf 的指令, 而后, tcpdump 采用了该技术用于 socket 过滤功能.

时间进一步来到了 2014 年, linux 的内核版本来到了 3.18, bpf 也进化成为了 ebpf

我们说进化, 主要是 bpf 的功能发生了以下主要的改变: 
1. 它的指令扩展支持了 64 位的指令集
2. 在原有的执行环境当中, 添加了 map 功能, 让大数据的操作成为可能.
3. 操作系统专门新增了一个系统调用, 被称之为 bpf()
4. 为了安全性, 新增了代码检查器.

从这个时间点开始, ebpf 的应用范围逐渐的迈出网络过滤. ebpf 可以使用在系统调用, socket, 文件系统,KPROBE, CGROUP 等等. 

(在内核态的方框上面, 添加上系统调用,文件系统,SOCKET等等.)
换句话说, 基本上内核中的各种功能, 都可以动态的附加上 ebpf 的程序.

2016 年, 各个大厂, Netflix 开始大批量应用 ebpf 在系统监控领域, Cilium 项目启动, 2017 年, Facebook 的所有流量都使用 ebpf 的 xdp 来进行处理.

如今, 国外的 GCP , AWS, RedHat, 微软

国内的阿里云,蚂蚁金服, 字节跳动, kindling 等等, 都在使用该项技术来提升安全性以及可观测性.
微软最近也开始研发了 eBPF for windows. 足见该项功能未来的应用场景.

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

class WhatIsBpf(VoiceoverScene):

    def __init__(self):
        super().__init__()
        self.camera.background_color = BACKGROUND

    def construct(self):
        # 它可以安全高效地扩展内核的能力且无需修改内核源代码或加载内核模块。
        # 它可以监控内核中的网络流量，并根据流量类型进行流量控制。
        # 它可以在程序运行时, 动态的植入监控点,获取运行时的状态.
        positions = [[-4,0,0],[-2,0,0],[0,0,0],[2,0,0],[4,0,0]]
        safety = Text("安全")#, color=WORD_A)
        effe = Text("高效")#, color=WORD_A)
        scale = Text("扩展")#, color=WORD_A)
        ctrl = Text("控制")#, color=WORD_A)
        dynamic = Text("动态")#, color=WORD_A)
        #self.add(safety,effe,scale,ctrl,dynamic)
        #self.play(Create(safety))
        self.add(safety)
        self.play(safety.animate.move_to(positions[0]))
        #self.play(Create(effe))
        self.add(effe)
        self.play(effe.animate.move_to(positions[1]))
        #self.play(Create(scale))
        self.add(scale)
        self.play(scale.animate.move_to(positions[2]))
        #self.play(Create(ctrl))
        self.add(ctrl)
        self.play(ctrl.animate.move_to(positions[3]))
        #self.play(Create(dynamic))
        self.add(dynamic)
        self.play(dynamic.animate.move_to(positions[4]))
        tbpf = Text("BPF", color=WORD_B).scale(3).next_to(scale,UP).set_z_index(1)
        self.play(SpiralIn(tbpf))

        self.wait()
        self.clear()
        #在 1993 年, 一篇关于伯克利过滤器的论文,描述了一个新的用户级数据包捕获架构.
        paper = ImageMobject("./images/bpf-paper.png").shift(UP)
        tpaper = Text("The BSD Packet Filter: A New Architecture for User-level Packet Capture").scale(0.5).next_to(paper,DOWN)
        tcpaper = Text("伯克利过滤器: 一个新的用户级数据包捕获架构").scale(0.5).next_to(tpaper,DOWN)

        self.play(FadeIn(paper), FadeIn(tpaper), FadeIn(tcpaper))
        self.wait()
        self.play(FadeOut(paper), FadeOut(tpaper), FadeOut(tcpaper))
        paper_abstruct = ImageMobject("./images/bpf-paper-abstruct.png").scale(2)

        # 在概论当中,其声明可以做到比原有过滤器提高20倍的性能.
        self.play(FadeIn(paper_abstruct))

        draw_line1 = Line([-2,-0.9,0],[2.4,-0.9,0], color=RED).set_z_index(1)
        draw_line2 = Line([-2.5,-1.15,0],[2.4,-1.15,0], color=RED).set_z_index(1)
        draw_line3 = Line([-2.5,-1.4,0],[-1.3,-1.4,0], color=RED).set_z_index(1)
        self.play(Create(draw_line1))
        self.play(Create(draw_line2))
        self.play(Create(draw_line3))
        self.wait()

        #能够做到这一点, 是其解决了数据包的抓取过程当中, 在内核态和用户态之间的数据复制导致了大量的性能损耗问题.(一个图, 从内核态流动到用户态, 判断, drop , 或者流给用户)
        self.clear()
        kernel = Rectangle(width=2, height=2, color=OBJ_A).shift(LEFT*2)
        tkernel = Text("内核态").scale(0.5).next_to(kernel, UP)
        user = Rectangle(width=2, height=2, color=OBJ_B).shift(RIGHT*2)
        tuser = Text("用户态").scale(0.5).next_to(user, UP)
        os = VGroup(kernel, user, tkernel, tuser)
        package = Circle(radius=0.5, color=OBJ_C).next_to(kernel, LEFT)
        tpackage = Text("数据包").scale(0.3).move_to(package)
        gpackage = VGroup(package, tpackage)

        self.play(FadeIn(os))
        self.play(gpackage.animate.move_to(kernel))
        gpackage_copy = gpackage.copy()
        self.play(gpackage_copy.animate.move_to(user))
        
        drop = Text("Drop?").scale(0.5).next_to(gpackage_copy, DOWN)
        self.play(FadeIn(drop))
        self.play(FadeOut(drop))
        self.play(FadeOut(gpackage_copy))

        self.wait()
        #而它所提到的解决方案是, 在内核态当中,使用自定义的指令来对数据包进行过滤的功能. 并将这种解决方案被称之为: BPF
        self.play(gpackage.animate.next_to(kernel, LEFT))
        self.play(gpackage.animate.move_to(kernel))
        drop.next_to(gpackage, DOWN)
        self.play(FadeIn(drop))
        self.play(FadeOut(drop))
        self.play(FadeOut(gpackage))

        gpackage_copy.move_to(kernel)
        self.play(gpackage_copy.animate.move_to(user))
        self.play(FadeOut(gpackage_copy))
        #(一个图, 从在内核态进行判断, drop , 或者直接给到用户)

        # 一条时间线, 从左到右遍历 ebpf 的发展.
        # 1992 年, 论文发表后,
        # 到 1997 年, linux kernel 2.1.75 在内核当中实现了一个小的 bpf 的虚拟机,用于执行 bpf 的指令, 而后, tcpdump 采用了该技术用于 socket 过滤功能.
        self.clear()
        bpf_timeline = NumberLine(
            x_range=[0, 21, 3],
            length=10,
            color=BLUE,
            include_numbers=False,
            label_direction=UP,
            include_tip=True,

        )
        self.play(FadeIn(bpf_timeline))
        first = Text("1992").scale(0.5).next_to(bpf_timeline.ticks[0], DOWN)
        second = Text("1997").scale(0.5).next_to(bpf_timeline.ticks[1], DOWN)
        third = Text("2014").scale(0.5).next_to(bpf_timeline.ticks[3], DOWN)
        forth = Text("2016").scale(0.5).next_to(bpf_timeline.ticks[4], DOWN)
        fifth = Text("Now").scale(0.5).next_to(bpf_timeline.ticks[6], DOWN)

        #self.add(first, second, third, forth, fifth)
        self.play(FadeIn(first))
        ppaper = ImageMobject("./images/bpf-paper.png").scale(0.1).next_to(bpf_timeline.ticks[0], UP)
        self.play(FadeIn(ppaper))

        linux = ImageMobject("./images/linux.png").scale(0.1).next_to(bpf_timeline.ticks[1], UP)
        self.play(FadeIn(linux), FadeIn(second))

        #时间进一步来到了 2014 年, linux 的内核版本来到了 3.18, bpf 也进化成为了 ebpf
        ebpf = ImageMobject("./images/ebpf.png").scale(0.1).next_to(bpf_timeline.ticks[3], UP+RIGHT*0.2)
        self.play(FadeIn(ebpf), FadeIn(third))

        bpfline = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_tip=False,
            color=ORANGE,
            include_numbers=False,
            rotation=90 * DEGREES,
        )
        bpfline.next_to(bpf_timeline.ticks[3], UP, buff=0)
        self.play(Write(bpfline))

        #
        #我们说进化, 主要是 bpf 的功能发生了以下主要的改变: 
        # 1. 它的指令扩展支持了 64 位的指令集
        f1 = Text("64位指令集",color=ORANGE).scale(0.3).next_to(bpfline.ticks[1], LEFT)
        # 2. 在原有的执行环境当中, 添加了 map 功能, 让大数据的操作成为可能.
        f2 = Text("bpf map(like heap)",color=ORANGE).scale(0.3).next_to(bpfline.ticks[2], LEFT)
        # 3. 操作系统专门新增了一个系统调用, 被称之为 bpf()
        f3 = Text("bpf()",color=ORANGE).scale(0.3).next_to(bpfline.ticks[3], LEFT)
        # 4. 为了安全性, 新增了代码检查器.
        f4 = Text("代码检查器", color=ORANGE).scale(0.3).next_to(bpfline.ticks[4], LEFT)
        #
        self.play(FadeIn(f1))
        self.play(FadeIn(f2))
        self.play(FadeIn(f3))
        self.play(FadeIn(f4))

        #从这个时间点开始, ebpf 的应用范围逐渐的迈出网络过滤. ebpf 可以使用在系统调用, socket, 文件系统,KPROBE, CGROUP 等等. 
        kernel2 = Rectangle(width=2, height=2, color=OBJ_A).shift(LEFT*2)
        tkernel2 = Text("内核").scale(0.5).move_to(kernel)
        gk = VGroup(kernel2, tkernel2)
        gk.scale(0.5).next_to(bpfline.ticks[2], RIGHT)
        self.play(FadeIn(gk))
        
        socket = Text("socket", color=OBJ_B).scale(0.3).next_to(gk, UP)
        cgroup = Text("cgroup", color=OBJ_B).scale(0.3).next_to(gk, DOWN)
        filesys = Text("文件系统", color=OBJ_B).scale(0.3).next_to(gk, RIGHT)
        self.play(FadeIn(socket))
        self.play(FadeIn(cgroup))
        self.play(FadeIn(filesys))

        #
        #(在内核态的方框上面, 添加上系统调用,文件系统,SOCKET等等.)
        #换句话说, 基本上内核中的各种功能, 都可以动态的附加上 ebpf 的程序.
        #
        #2016 年, 各个大厂, Netflix 开始大批量应用 ebpf 在系统监控领域, Cilium 项目启动, 2017 年, Facebook 的所有流量都使用 ebpf 的 xdp 来进行处理.
        bpfline2 = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_tip=False,
            color=ORANGE,
            include_numbers=False,
            rotation=270 * DEGREES,
        )
        bpfline2.next_to(bpf_timeline.ticks[4], DOWN, buff=0)
        forth.next_to(bpfline2.ticks[0], RIGHT+DOWN*0.3)
        self.play(FadeIn(forth), FadeIn(bpfline2))
        netflux = ImageMobject("./images/netflix.png").scale(0.1).next_to(bpfline2.ticks[1], LEFT)
        cilium = ImageMobject("./images/cilium.png").scale(0.2).next_to(bpfline2.ticks[2], LEFT)
        facebook = ImageMobject("./images/facebook.png").scale(0.1).next_to(bpfline2.ticks[3], LEFT)
        self.play(FadeIn(netflux))
        self.play(FadeIn(cilium))
        self.play(FadeIn(facebook))

        #如今, 国外的 GCP , AWS, RedHat, 微软
        bpfline3 = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_tip=False,
            color=ORANGE,
            include_numbers=False,
            rotation=90 * DEGREES,
        )
        bpfline3.next_to(bpf_timeline.ticks[6], UP, buff=0)
        self.play(FadeIn(bpfline3))

        #国内的阿里云,蚂蚁金服, 字节跳动, kindling 等等, 都在使用该项技术来提升安全性以及可观测性.
        #微软最近也开始研发了 eBPF for windows. 足见该项功能未来的应用场景.
        ali = ImageMobject("./images/alicloud.jpeg").scale(0.3).next_to(bpfline3.ticks[1], LEFT)
        tencent = ImageMobject("./images/tencent.png").scale(0.1).next_to(bpfline3.ticks[2], LEFT)
        tik = ImageMobject("./images/tik-tok.png").scale(0.1).next_to(bpfline3.ticks[3], LEFT)
        micro = ImageMobject("./images/microsoft.png").scale(0.1).next_to(bpfline3.ticks[1], RIGHT)
        kind = ImageMobject("./images/kindling.png").scale(0.3).next_to(bpfline3.ticks[2], RIGHT)
        aws = ImageMobject("./images/aws.png").scale(0.1).next_to(bpfline3.ticks[3], RIGHT)
        self.play(FadeIn(fifth))
        self.play(FadeIn(ali))
        self.play(FadeIn(tencent))
        self.play(FadeIn(tik))
        self.play(FadeIn(micro))
        self.play(FadeIn(kind))
        self.play(FadeIn(aws))

        self.wait()
        self.clear()
        ebpf_for_win = ImageMobject("./images/ebpf-for-windows.png").scale(1.5)
        self.play(FadeIn(ebpf_for_win))
        self.clear()
        self.wait()