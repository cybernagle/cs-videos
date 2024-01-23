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


class WhatIsBpf(VoiceoverScene):

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

        paper = ImageMobject("./images/bpf-paper.png").shift(UP)
        tpaper = Text("The BSD Packet Filter: A New Architecture for User-level Packet Capture").scale(0.5).next_to(paper,DOWN)
        tcpaper = Text("伯克利过滤器: 一个新的用户级数据包捕获架构").scale(0.5).next_to(tpaper,DOWN)

        in1993 = "在 1993 年, 一篇关于伯克利过滤器的论文,描述了一个新的用户级数据包捕获架构."
        with self.voiceover(text=in1993) as tracker:
            self.play(FadeIn(paper), FadeIn(tpaper), FadeIn(tcpaper))
        self.play(FadeOut(paper), FadeOut(tpaper), FadeOut(tcpaper))
        paper_abstruct = ImageMobject("./images/bpf-paper-abstruct.png").scale(2)

        inabstruct = "在概论当中,其声明<bookmark mark='A'/>可以做到比原有过滤器提高20倍的性能."
        draw_line1 = Line([-2,-0.9,0],[2.4,-0.9,0], color=RED).set_z_index(1)
        draw_line2 = Line([-2.5,-1.15,0],[2.4,-1.15,0], color=RED).set_z_index(1)
        draw_line3 = Line([-2.5,-1.4,0],[-1.3,-1.4,0], color=RED).set_z_index(1)
        with self.voiceover(text=inabstruct) as tracker:
            self.play(FadeIn(paper_abstruct))
            self.wait_until_bookmark("A")
            self.play(Create(draw_line1))
            self.play(Create(draw_line2))
            self.play(Create(draw_line3))

        self.clear()
        kernel = Rectangle(width=2, height=2, color=OBJ_A).shift(LEFT*2)
        tkernel = Text("内核态").scale(0.5).next_to(kernel, UP)
        user = Rectangle(width=2, height=2, color=OBJ_B).shift(RIGHT*2)
        tuser = Text("用户态").scale(0.5).next_to(user, UP)
        os = VGroup(kernel, user, tkernel, tuser)
        package = Circle(radius=0.5, color=OBJ_C).next_to(kernel, LEFT)
        tpackage = Text("数据包").scale(0.3).move_to(package)
        gpackage = VGroup(package, tpackage)

        #能够做到这一点, 是其解决了数据包的抓取过程当中, 在内核态和用户态之间的数据复制导致了大量的性能损耗问题.(一个图, 从内核态流动到用户态, 判断, drop , 或者流给用户)
        why_happen = "能够做到这一点, 是其解决了数据包的抓取过程当中, 在内核态和用户态之间的<bookmark mark='A'/>数据复制导致了大量的性能损耗问题."
        with self.voiceover(text=why_happen) as tracker:
            self.play(FadeIn(os))
            self.play(gpackage.animate.move_to(kernel))
            gpackage_copy = gpackage.copy()
            self.wait_until_bookmark("A")
            self.play(gpackage_copy.animate.move_to(user))
        
            drop = Text("Drop?").scale(0.5).next_to(gpackage_copy, DOWN)
            self.play(FadeIn(drop))
            self.play(FadeOut(drop))
            self.play(FadeOut(gpackage_copy))

        #而它所提到的解决方案是, 在内核态当中,使用自定义的指令来对数据包进行过滤的功能. 并将这种解决方案被称之为: BPF
        how_to_solve = "而它所提到的解决方案是<bookmark mark='A'/>, 在内核态当中,使用自定义的指令来对数据包进行过滤<bookmark mark='B'/>的功能. 并将其命名为: BPF"
        with self.voiceover(text=how_to_solve) as tracker:
            self.play(gpackage.animate.next_to(kernel, LEFT))
            self.play(gpackage.animate.move_to(kernel))
            self.wait_until_bookmark("A")
            drop.next_to(gpackage, DOWN)
            self.play(FadeIn(drop))
            self.wait_until_bookmark("B")
            self.play(FadeOut(drop))
            self.play(FadeOut(gpackage))

        self.clear()
        bpf_timeline = NumberLine(
            x_range=[0, 21, 3],
            length=10,
            color=BLUE,
            include_numbers=False,
            label_direction=UP,
            include_tip=True,

        )

        #1992 年, 论文发表后, 到 1997 年, linux kernel 2.1.75 在内核当中实现了一个小的 bpf 的虚拟机,用于执行 bpf 的指令, 而后, tcpdump 采用了该技术用于 socket 过滤功能.
        first = Text("1992").scale(0.5).next_to(bpf_timeline.ticks[0], DOWN)
        second = Text("1997").scale(0.5).next_to(bpf_timeline.ticks[1], DOWN)
        third = Text("2014").scale(0.5).next_to(bpf_timeline.ticks[3], DOWN)
        forth = Text("2016").scale(0.5).next_to(bpf_timeline.ticks[4], DOWN)
        fifth = Text("Now").scale(0.5).next_to(bpf_timeline.ticks[6], DOWN)
        ppaper = ImageMobject("./images/bpf-paper.png").scale(0.1).next_to(bpf_timeline.ticks[0], UP)
        linux = ImageMobject("./images/linux.png").scale(0.2).next_to(bpf_timeline.ticks[1], UP)
        tcpdump = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_tip=False,
            color=ORANGE,
            include_numbers=False,
            rotation=270 * DEGREES,
        )
        tcpdump.next_to(bpf_timeline.ticks[1], DOWN, buff=0)
        second.next_to(tcpdump.ticks[0], RIGHT+DOWN*0.3)
        tcpdumimg = ImageMobject("./images//tcpdump-logo.jpg").scale(0.3).next_to(tcpdump.ticks[2], LEFT)

        in1997 = "1992 年, <bookmark mark='A'/>论文发表后, 到 1997 <bookmark mark='B'/>年, linux kernel <bookmark mark='C'/>2点1点75的版本实现了一个小的 BPF 的虚拟机,用于执行 BPF 的指令, 而后, TCP dump<bookmark mark='D'/> 采用了该技术用于 socket 过滤功能."
        with self.voiceover(text=in1997) as tracker:
            self.play(FadeIn(bpf_timeline))
            self.wait_until_bookmark("A")
            self.play(FadeIn(first))
            self.play(FadeIn(ppaper))

            self.wait_until_bookmark("B")
            self.play(FadeIn(second))
            self.play(Create(tcpdump))
            self.wait_until_bookmark("C")
            self.play(FadeIn(linux))
            self.wait_until_bookmark("D")
            self.play(FadeIn(tcpdumimg))

        ebpf = ImageMobject("./images/ebpf.png").scale(0.3).next_to(bpf_timeline.ticks[3], UP+RIGHT*0.2)
        #时间进一步来到了 2014 年, linux 的内核版本来到了 3.18, bpf 也进化成为了 ebpf
        in2014 = "时间进一步来到了 2014<bookmark mark='A'/> 年, linux 的内核版本来到了 3.18, bpf 也进化成为了<bookmark mark='B'/> eBPF"
        with self.voiceover(text=in2014) as tracker:
            self.wait_until_bookmark("A")
            self.play(FadeIn(third))
            self.wait_until_bookmark("B")
            self.play(FadeIn(ebpf))

        bpfline = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_tip=False,
            color=ORANGE,
            include_numbers=False,
            rotation=90 * DEGREES,
        )
        bpfline.next_to(bpf_timeline.ticks[3], UP, buff=0)

        f1 = Text("64位指令集",color=ORANGE).scale(0.3).next_to(bpfline.ticks[1], LEFT)
        f2 = Text("bpf map(like heap)",color=ORANGE).scale(0.3).next_to(bpfline.ticks[2], LEFT)
        f3 = Text("bpf()",color=ORANGE).scale(0.3).next_to(bpfline.ticks[3], LEFT)
        f4 = Text("代码检查器", color=ORANGE).scale(0.3).next_to(bpfline.ticks[4], LEFT)
        evoloe = """我们说进化<bookmark mark='A'/>, 主要是 bpf 的功能发生了以下主要的改变:  
         第一. <bookmark mark='B'/>它的指令扩展支持了 64 位的指令集
         第二. <bookmark mark='C'/>在原有的执行环境当中, 添加了 map 功能, 让大数据的操作成为可能.
         第三. <bookmark mark='D'/>操作系统专门新增了一个系统调用, 被称之为 bpf()
         第四. <bookmark mark='E'/>为了安全性, 新增了代码检查器."""

        with self.voiceover(text=evoloe) as tracker:
            self.wait_until_bookmark("A")
            self.play(Write(bpfline))
            self.wait_until_bookmark("B")
            self.play(FadeIn(f1))
            self.wait_until_bookmark("C")
            self.play(FadeIn(f2))
            self.wait_until_bookmark("D")
            self.play(FadeIn(f3))
            self.wait_until_bookmark("E")
            self.play(FadeIn(f4))

        kernel2 = Rectangle(width=2, height=2, color=OBJ_A).shift(LEFT*2)
        tkernel2 = Text("内核").scale(0.5).move_to(kernel)
        gk = VGroup(kernel2, tkernel2)
        gk.scale(0.5).next_to(bpfline.ticks[2], RIGHT)
        
        socket = Text("socket", color=OBJ_B).scale(0.3).next_to(gk, UP)
        cgroup = Text("cgroup", color=OBJ_B).scale(0.3).next_to(gk, DOWN)
        filesys = Text("文件系统", color=OBJ_B).scale(0.3).next_to(gk, RIGHT)
        beginwith = "从这个时间点开始, eBPF 的应用范围逐渐迈出网络过滤.开始使用在<bookmark mark='A'/>系统调用, socket, 文件系统,KPROBE, CGROUP 等等. 换句话说, 基本上内核中的各种功能, 都可以动态的附加上 eBPF 的程序."
        with self.voiceover(text=beginwith) as tracker:
            self.wait_until_bookmark("A")
            self.play(FadeIn(gk))
            self.play(FadeIn(socket))
            self.play(FadeIn(cgroup))
            self.play(FadeIn(filesys))

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
        netflux = ImageMobject("./images/netflix.png").scale(0.1).next_to(bpfline2.ticks[1], LEFT)
        cilium = ImageMobject("./images/cilium.png").scale(0.2).next_to(bpfline2.ticks[2], LEFT)
        facebook = ImageMobject("./images/facebook.png").scale(0.1).next_to(bpfline2.ticks[3], LEFT)
        in2016 = "2016 年, 各个大厂, Netflix<bookmark mark='A'/> 开始大批量应用 eBPF 在系统监控领域, Cilium<bookmark mark='B'/> 项目启动, 2017 年, Facebook<bookmark mark='C'/> 的所有流量都使用 eBPF 的 xdp 来进行处理."
        with self.voiceover(text=in2016) as tracker:
            self.play(FadeIn(forth), FadeIn(bpfline2))
            self.wait_until_bookmark("A")
            self.play(FadeIn(netflux))
            self.wait_until_bookmark("B")
            self.play(FadeIn(cilium))
            self.wait_until_bookmark("C")
            self.play(FadeIn(facebook))

        bpfline3 = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_tip=False,
            color=ORANGE,
            include_numbers=False,
            rotation=90 * DEGREES,
        )
        bpfline3.next_to(bpf_timeline.ticks[6], UP, buff=0)

        #如今, 国外的 GCP , AWS, RedHat, 微软
        #国内的阿里云,蚂蚁金服, 字节跳动, kindling 等等, 都在使用该项技术来提升安全性以及可观测性.
        #微软最近也开始研发了 eBPF for windows. 足见该项功能未来的应用场景.
        ali = ImageMobject("./images/alicloud.jpeg").scale(0.3).next_to(bpfline3.ticks[1], LEFT)
        tencent = ImageMobject("./images/tencent.png").scale(0.1).next_to(bpfline3.ticks[2], LEFT)
        tik = ImageMobject("./images/tik-tok.png").scale(0.1).next_to(bpfline3.ticks[3], LEFT)
        micro = ImageMobject("./images/microsoft.png").scale(0.1).next_to(bpfline3.ticks[1], RIGHT)
        kind = ImageMobject("./images/kindling.png").scale(0.3).next_to(bpfline3.ticks[2], RIGHT)
        aws = ImageMobject("./images/aws.png").scale(0.1).next_to(bpfline3.ticks[3], RIGHT)
        now = "如今,阿里云,腾讯,字节跳动,微软, kindling, 亚马逊等等,都在使用该项技术来提升安全性以及可观测性. "
        with self.voiceover(text=now) as tracker:
            self.play(FadeIn(bpfline3))
            self.play(FadeIn(fifth))
            self.play(FadeIn(ali))
            self.play(FadeIn(tencent))
            self.play(FadeIn(tik))
            self.play(FadeIn(micro))
            self.play(FadeIn(kind))
            self.play(FadeIn(aws))

        self.clear()
        ebpf_for_win = ImageMobject("./images/ebpf-for-windows.png").scale(1.5)
        nowms = "微软最近也开始研发了 eBPF for windows. 足见该项功能未来的应用场景."
        with self.voiceover(text=nowms) as tracker:
            self.play(FadeIn(ebpf_for_win))