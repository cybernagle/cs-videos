from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

text_keyboard = """
 这是一个键盘,就在我们按下<bookmark mark='A'/>E键的时候,他就把 E 打包好,让它的<bookmark mark='B'/>小朋友送到系统处理部门哪里去.
 他的小朋友<bookmark mark='C'/>我们把它叫做中断酱.
"""

text_interrupt = """
 就像打酱油需要酱油瓶,中断酱去系统管理部门也不能空手去. 它也要带上几个容器,
 它们分别是 <bookmark mark='A'/>叫做 pushreg 和 trapframe 的两个结构体.<bookmark mark='B'/>
 紧接着中断酱来到系统管理部门<bookmark mark='C'/>
 哎呀, 它忘记了<bookmark mark='D'/>自己的容器.
"""

text_toos = """
 他找到了系统部门的 <bookmark mark='A'/>trap 酱.
 然后把身份<bookmark mark='B'/>给到它, trap酱一看, 哦<bookmark mark='C'/>, 这是键盘的娃娃
 它们比较敏感, 优先处理!
 于是拿出来一个<bookmark mark='D'/> switch_case说,这是键盘的小朋友, case KBD<bookmark mark='E'/> 吧, 让其他人先停下手头工作,先处理键盘宝宝的.
"""

text_ossave = """
 为了表示歉意,中断酱拿出来了前面准备的<bookmark mark='A'/>容器,用来保存它打断其他人手头工作的一些<bookmark mark='B'/>必要信息.
 比如说, 被打断的人执行到哪一步啦.那么信号酱也贴心的把这个保存在了叫做
 cs和eip的容器里面.他处理了多少文件啦,就保存在ss里面等等.
"""

text_osoutput = """
当然了, 在执行这些任务过程当中,中断酱也会有自己的任务进度.也就存在了
trapframe<bookmark mark='A'/>的其他cs&eip等类似的容器里面.
最后, 系统处理部门的人就开始安排中断酱<bookmark mark='B'/>给的内容:接收E, 写到标准输出
"""

trapframe_text = """
struct pushregs {
    ...
    uint32_t reg_ebx;
    uint32_t reg_edx;
    ...
};
struct trapframe {
    struct pushregs tf_regs;
    ...
    uint32_t tf_trapno;
    ...
    uintptr_t tf_eip;
    uint16_t tf_cs;
    ...
    uint16_t tf_ss;
}
"""

trap_dispatch = """
static void
trap_dispatch(
      struct trapframe *tf
    ) {
    ...
    switch (tf->tf_trapno) {
    case T_PGFLT:  //page fault
        ...
    case IRQ_OFFSET + IRQ_TIMER:
        ticks ++;
        ...
    case IRQ_OFFSET + IRQ_KBD:
        ...
    case T_SWITCH_TOU:
        ...
    default:
        ...
    }
}

"""

class ComputerScene(MovingCameraScene,
                    VoiceoverScene):
    # keyboard
    keyboard = VGroup()
    keys = VGroup()
    key_value = VGroup()
    operating_system = VGroup()
    signal = None
    trapframe = None
    dispatcher = None
    monitor = None
    trapper = None
    trapper_reverse = None

    def create_trapper(self):
        self.trapper = Text("|-:").set_color("#00FFFF")

    def create_monitor(self):
        screen = RoundedRectangle(height=3, width=4)
        screen.set_fill(BLUE_E, opacity=0.5)
        self.monitor = screen

    def keyboard(self):
        self.keys = VGroup(*[Rectangle(height=0.6, width=1).set_fill(WHITE, opacity=0.2) for i in range(10)]).arrange(RIGHT, buff=0.1)
        self.labels = VGroup(*[Text(char).scale(0.5).move_to(self.keys[i]) for i, char in enumerate("QWERTYUIOP")])
        self.keyboard = VGroup(self.keys, self.labels)

    def press(self, index, run_time=0.1):
        key = self.keys[index]
        label = self.labels[index]
        self.play(key.animate.set_fill(BLUE, opacity=0.5), label.animate.set_color(BLUE), run_time=run_time)
        self.play(key.animate.set_fill(WHITE, opacity=0.2), label.animate.set_color(BLACK), run_time=run_time)

    def create_os(self):
        kernel = Circle(radius=0.5, fill_opacity=0.5).set_color(GREEN)
        user = Circle(radius=1.5, fill_opacity=0.5).set_color(BLUE)

        kernel_space = Text("Kernel Space").scale(0.4).next_to(kernel, UP)
        user_space = Text("User Space").scale(0.4).next_to(user, UP)

        self.operating_system.add(VGroup(kernel, user), VGroup(kernel_space, user_space))

    def create_signal(self):
        self.signal = Text(":-)").set_color("#00FFFF")

    def create_information(self):
        trapframe = Code(code=trapframe_text, language="C").scale(0.5)
        self.trapframe = trapframe

    def create_trap_dispatch(self):
        self.dispatcher = Code(code=trap_dispatch, language="C").scale(0.5)

    def construct(self):

        self.set_speech_service(RecorderService())
        # 这是一个键盘,就在我们按下E键的时候,他就把 E 打包好,让它的小朋友送到系统酱哪里去.
        self.keyboard()
        self.play(Create(self.keyboard))

        self.create_os()
        self.add(self.operating_system.next_to(
            self.keyboard, RIGHT*30
        ))

        self.create_monitor()
        self.add(self.monitor.next_to(self.operating_system, RIGHT*20))

        with self.voiceover(text=text_keyboard) as tracker:

            self.wait_until_bookmark("A")
            self.press(2, 0.5)

            self.create_signal()
            self.wait_until_bookmark("B")
            self.play(Create(self.signal.next_to(self.keyboard[0][2], UP)))

            # 他的小朋友我们把它叫做中断酱.
            self.wait_until_bookmark("C")
            self.play(Wiggle(self.signal))

        self.create_information()

        # 就像打酱油需要酱油瓶,中断酱去系统酱哪里也不能空手去. 它也要带上几个容
        # 器, 这些都放在两个 struct 里面.

        with self.voiceover(text=text_interrupt) as tracker:
            self.play(self.camera.frame.animate.move_to(self.signal.get_center()))
            self.wait_until_bookmark("A")
            self.play(Create(self.trapframe.next_to(self.signal, UP)))
            # 中断酱来到 OS
            self.camera.frame.add_updater(lambda _signal, dt: _signal.move_to(self.signal))

            self.wait_until_bookmark("B")
            self.play(self.signal.animate.next_to(self.operating_system, LEFT, buff=0.2),run_time=3)
            # 哦, 差点忘记了它的容器.
            self.wait_until_bookmark("C")
            self.wait_until_bookmark("D")
            self.play(self.trapframe.animate.next_to(self.signal, LEFT))

        signal = VGroup(self.signal, self.trapframe)
        self.camera.frame.remove_updater(lambda _signal, dt: _signal.move_to(self.signal))


        # 他找到了系统部门的 trap 酱.
        self.play(self.camera.frame.animate.add_updater(lambda _signal, dt: _signal.move_to(self.operating_system)))
        self.wait()

        with self.voiceover(text=text_toos) as tracker:
            self.create_trapper()
            self.trapper.move_to(self.operating_system[0][0].get_center())

            # 然后把身份给到系统酱, trap酱一看, 哦, 这是键盘的娃娃,它们比较敏感,优先处理!
            self.wait_until_bookmark("A")
            self.play(Create(self.trapper))
            trapnum = self.trapframe.code[9][-7:-1].copy()
            self.play(trapnum.animate.next_to(self.signal, UP))
            self.wait_until_bookmark("B")
            self.play(trapnum.animate.next_to(self.trapper, UP))
            self.wait_until_bookmark("C")
            self.play(self.trapper.animate.become(Text(":-o").set_color("#00FFFF").move_to(self.operating_system[0][0].get_center())))
            # trap 酱拿出来一个 switch_case 说,这是键盘的小朋友, case KBD 吧, 让其他人先停下手头工作,先处理键盘宝宝的.
            self.create_trap_dispatch()
            self.wait_until_bookmark("D")
            self.play(Create(self.dispatcher.next_to(self.operating_system, RIGHT)))

            self.wait_until_bookmark("E")
            self.play(
                Wiggle(self.dispatcher.code[11:13]),
                Wiggle(self.dispatcher.code[5])
            )
            self.play(self.camera.frame.animate.remove_updater(lambda _signal, dt: _signal.move_to(self.operating_system)))

        with self.voiceover(text=text_ossave) as tracker:

            self.wait_until_bookmark("A")
            # 信号酱拿出来了前面准备的几个容器,用来保存它打断其他人手头工作的一些必要信息.
            self.play(Indicate(self.trapframe))
            self.wait_until_bookmark("B")
            self.play(Wiggle(self.trapframe.code[0:6]))
            # 比如说, 被打断的人执行到哪一步啦.那么信号酱也贴心的把这个保存在了
            # cs+eip里面.他处理了多少文件啦,就保存在ss里面等等.


        with self.voiceover(text=text_osoutput) as tracker:

            # 当然了, 在执行这些任务过程当中,它也会有自己的任务进度.也就存在了
            # trapframe的其他cs&eip等类似的容器里面.
            self.wait_until_bookmark("A")
            self.play(Wiggle(self.trapframe.code[7:-1]))
            # 然后, 中断处理部门的人就开始安排信号酱给的内容:接收E, 写到标准输出
            self.wait_until_bookmark("B")
            self.play(self.camera.frame.animate.add_updater(lambda _signal, dt: _signal.move_to(self.monitor)))
            e = Text("E", color=WHITE).move_to(self.monitor.get_center()+LEFT*1.5+UP)
            self.play(FadeIn(e))
