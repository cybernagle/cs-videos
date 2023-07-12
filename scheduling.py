from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class Scheduling(VoiceoverScene):
    def construct(self):

        self.set_speech_service(RecorderService())
        # 首先说进程被执行?
        # 这是多个进程, 他们都将被调度程序调度到 CPU 上执行.
        p1 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5)
        p1_text = Tex("$process_x: 1day$", font_size = 40).next_to(p1, DOWN)
        p1_group = Group(p1, p1_text)
        with self.voiceover(text="操作系统运行了多个进程, 这是进程1, 它需要执行1天") as tracker:
            self.add(p1, p1_text)
        self.play(p1_group.animate.scale(0.5).move_to(LEFT * 5.5 + UP * 1.5))

        p2 = Rectangle(color=GREEN, fill_opacity=0.5, width = 4, height = 0.5)
        p2_text = Tex("$process_y: 2day$", font_size = 40).next_to(p2, DOWN)
        p2_group = Group(p2, p2_text)
        with self.voiceover(text="进程2需要2天") as tracker:
            self.add(p2, p2_text)
        self.play(p2_group.animate.scale(0.5).next_to(p1,DOWN, buff = p1.height * 4))

        p3 = Rectangle(color=GREEN, fill_opacity=0.5, width = 6, height = 0.5)
        p3_text = Tex("$process_z: 3day$", font_size = 40).next_to(p3, DOWN)
        p3_group = Group(p3, p3_text)
        with self.voiceover(text="进程3需要3天") as tracker:
            self.add(p3, p3_text)
        self.play(p3_group.animate.scale(0.5).next_to(p2,DOWN, buff = p1.height * 4))  # 

        process_group = Group(p1_group, p2_group, p3_group)

        self.play(process_group.animate.arrange(RIGHT))

        timeline = Arrow(start=5*LEFT, end=5* RIGHT, color = BLUE,buff = 1).next_to(process_group, DOWN, buff=0.1)
        overall_time = Text("总执行时间: 6天", font_size = 20).next_to(timeline, DOWN, buff = 0.1)
        timeline_group = Group(timeline, overall_time)

        with self.voiceover(text="它们一共要执行6天") as tracker:
            self.play(Create(timeline), FadeIn(overall_time))

        # 他们可以有着不同的执行顺序
        with self.voiceover(text="进程可以有者不同的执行顺序.不同的执行顺序也有不同的效率") as tracker:
            self.play(process_group.animate.arrange(LEFT))
            self.wait(1)
            self.play(process_group.animate.arrange(RIGHT))

        cpu = RoundedRectangle(color=BLUE, fill_opacity=0.5, corner_radius=1.5, height=4.0, width=4.0)
        self.play(cpu.animate.scale(0.2).move_to(LEFT*2.3 + UP*1.4))
        cpu_text = Text("CPU", font_size = 20).next_to(cpu, DOWN, buff=0.1)

        self.play(FadeIn(cpu_text))
        cpu_group = Group(cpu, cpu_text)

        with self.voiceover(text="从CPU的角度来说,我们需要充分的利用其运算能力,那么,如何衡量或者说如何量化对CPU的利用情况呢?这里我们引入了两个指标") as tracker:
            pass

        # 而我们如何衡量一个不同调度方法或者算法的优劣?
        # 这就要求我们需要对我们的调度算法进行量化. 这也就引入了两个
        # 概念: turnaround time -- 周转时间. response time -- 响应时间
        # turnaround time 是: 进程结束的时间, 减去进程开始执行的时间.(brace)
        # response time 是: 进程启动的时间, 减去进程开始执行的时间.(brace)

        tt = Text("周转时间", font_size = 25).next_to(process_group, UP, buff = 1).shift(LEFT)
        tt_formula = Tex("$ = T_{completion} - T_{arrival} $", font_size = 20).next_to(tt, RIGHT, buff = 0.1)
        tt_group = Group(tt, tt_formula)
        rt = Text("响应时间", font_size = 25).next_to(tt, DOWN, buff=0.1)
        rt_formula = Tex("$ = T_{firstrun} - T_{arrival} $", font_size =  20).next_to(rt, RIGHT, buff = 0.1)

        rt_group = Group(rt, rt_formula)
        with self.voiceover(text="第一个指标是周转时间") as tracker:
            self.play(Create(tt))
        with self.voiceover(text="它等于进程执行结束的时间减去抵达CPU的时间") as tracker:
            self.play(FadeIn(tt_formula, run_time=tracker.get_remaining_duration()))

        # 下图 process x 的周转时间是:
        with self.voiceover(text="在我们的图示中,现在展示的是进程z的周转时间.它等于进程z的执行时间,也就是3") as tracker:
            self.play(Indicate(process_group[2], run_time=tracker.get_remaining_duration()))
        # 下图 process y 的周转时间是:
        with self.voiceover(text="y周转时间等于z加上y,等于5") as tracker:
            self.play(Indicate(process_group[1:3]), run_time=tracker.get_remaining_duration())
        # process z 的周转时间是:
        with self.voiceover(text="最后,是z的周转时间,它是三者总和也就是6") as tracker:
            self.play(Indicate(process_group, run_time=tracker.get_remaining_duration()))


        with self.voiceover(text="紧接着我们看第二个指标,叫做响应时间") as tracker:
            self.play(Create(rt))
        with self.voiceover(text="它等于进程被执行的时间减去抵达CPU的时间") as tracker:
            self.play(FadeIn(rt_formula))
        # process x 的响应时间是 0
        with self.voiceover(text="进程z的响应时间是0,因为它是第一个被执行的程序,不需要等待") as tracker:
            self.play(Indicate(process_group[2], run_time=tracker.get_remaining_duration()))
        # process y 的响应时间是
        with self.voiceover(text="这是进程y的响应时间3") as tracker:
            self.play(Indicate(process_group[1:3], run_time=tracker.get_remaining_duration()))
        # process z 的响应时间是
        with self.voiceover(text="进程x的响应时间是3+2=5") as tracker:
            self.play(Indicate(process_group, run_time=tracker.get_remaining_duration()))

        formula_group = Group(tt_group, rt_group)

        self.play(FadeOut(formula_group), FadeOut(cpu_group))

        ptimeline_group = Group(process_group, timeline_group)
        with self.voiceover(text="有了这两个量化指标后,我们来看看几个常用的调度算法") as tracker:
            self.play(ptimeline_group.animate.move_to(UP*2))
        # 有了量化的标准, 接下来我们看看调度的一些算法, 看看他们的表现如何;
        # 本视频介绍的算法包括: fifo , sjf, rr, MLFQ , Proportional Share
        fifo = Text("FIFO", font_size=25, color = RED)
        sjf = Text("SJF", font_size=25, color = WHITE).next_to(fifo, DOWN, buff=0.1)
        rr = Text("Round Robin", font_size=25, color = ORANGE).next_to(sjf, DOWN, buff=0.1)
        #mlfq = Text("MLFQ", font_size=25, color = PURPLE).next_to(rr, DOWN, buff=0.1)

        with self.voiceover(text="他们分别是fifo,先进先出算法") as tracker:
            self.play(FadeIn(fifo))
        with self.voiceover(text="sjf,最短优先算法") as tracker:
            self.play(FadeIn(sjf))
        with self.voiceover(text="round robin,轮训算法") as tracker:
            self.play(FadeIn(rr))

        algorithms = Group(fifo, sjf, rr)
        self.play(algorithms.animate.move_to(LEFT * 5))


        # 首先谈一下 First In First Out, FIFO 算法, 它的调度是按照进程来的顺序, 依次执行(3, 1, 2)
        with self.voiceover(text="我们先来看看fifo算法的表现") as tracker:
            self.play(Indicate(fifo, run_time=tracker.get_remaining_duration(),scale_factor=2))
        # (添加一个 point, 添加一条线, 再转换成数字. 然后数字相加)
        # 在我们的上图示例当中, fifo 的调度顺序就是 x, y ,z
        # 而它的平均周转时间是 ( 3 + 5 + 6 ) / 14 = 4.66
        # 它的平均响应时间是 (0+3+4) / 3 = 2.33

        ####
        # turnaround time
        ####
        with self.voiceover(text="我们来看看它的周转时间") as tracker:
            self.play(tt.animate.next_to(process_group, DOWN , buff = 1.6))
        ta1 = Tex("$3$", font_size = 40, color = WHITE).next_to(p3, DOWN, buff = 0)
        ta2 = Tex("$5$", font_size = 40, color = WHITE).next_to(process_group[1:3], DOWN, buff = 0)
        ta3 = Tex("$6$", font_size = 40, color = WHITE).next_to(process_group, DOWN, buff = 0)



        with self.voiceover(text="3加上") as tracker:
            self.play(Indicate(process_group[2]))
            self.play(ta1.animate.move_to(DOWN*0.4+LEFT*3))
        plus1 = Tex("$+$").next_to(ta1)
        self.add(plus1)

        # 下图 process y 的周转时间是:
        with self.voiceover(text="5加上") as tracker:
            self.play(Indicate(process_group[1:3]))
            self.play(ta2.animate.next_to(ta1, RIGHT, buff = 0.8))
        plus2 = Tex("$+$").next_to(ta2)
        self.add(plus2)

        # process z 的周转时间是:
        with self.voiceover(text="6") as tracker:
            self.play(Indicate(process_group))
            self.play(ta3.animate.next_to(ta2, RIGHT, buff = 0.8))

        ta_avg = Tex("$T_{average} = 14 / 3 = 4.66$", font_size = 35)

        with self.voiceover(text="等于14,取平均值也就是除以3,等于4.66") as tracker:
            self.play(ta_avg.animate.next_to(ta3, RIGHT, buff= 1))

        ################
        # response time
        ################
        with self.voiceover(text="我们再来看看响应时间") as tracker:
            self.play(rt.animate.next_to(process_group, DOWN , buff = 3))
        rt1 = Tex("$0$", font_size = 40, color = WHITE).next_to(p3, DOWN, buff = 0)
        rt2 = Tex("$3$", font_size = 40, color = WHITE).next_to(p2, DOWN, buff = 0)
        rt3 = Tex("$5$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)


        with self.voiceover(text="0,加上") as tracker:
            self.play(Indicate(process_group[2]))
            self.play(rt1.animate.move_to(DOWN*2+LEFT*3))
            plus3 = Tex("$+$").next_to(rt1)
            self.add(plus3)

        # 下图 process y 的周转时间是:
        with self.voiceover(text="3加上") as tracker:
            self.play(Indicate(process_group[1:3]))
            self.play(rt2.animate.next_to(rt1, RIGHT, buff = 0.8))
            plus4 = Tex("$+$").next_to(rt2)
            self.add(plus4)

        # process z 的周转时间是:
        with self.voiceover(text="2") as tracker:
            self.play(Indicate(process_group))
            self.play(rt3.animate.next_to(rt2, RIGHT, buff = 0.8))

        rt_avg = Tex("$T_{average} = 8 / 3 = 1.66$", font_size = 35)
        with self.voiceover(text="等于8,取平均值也就是除以3等于1.55") as tracker:
            self.play(rt_avg.animate.next_to(rt3, RIGHT, buff= 1))

        fifo_group = Group(ta1, ta2, ta3, ta_avg, rt1, rt2, rt3, rt_avg, plus1, plus2, plus3, plus4)
        self.play(FadeOut(fifo_group))

        # 接下来我们看一下 Short Job First, SJF, 是进程进来以后, 找出最短执行时间的, 进行执行.(1,2,3)
        with self.voiceover(text="那么sjf表现如何呢?") as tracker:
            self.play(Indicate(sjf,run_time=tracker.get_remaining_duration()))
        # 它的平均周转时间可以达到 ( 1 + 3 + 6 ) / 3 = 3.33
        # 它的平均响应时间可以达到 (0+1+3) / 3 = 1.33
        # 这个时候 FIFO 的执行时间可以得到很高的提升.
        # 我们可以看到 FIFO 根据任务抵达的时间不同, 收到的影响也很大.
        # 而 FIFO 这种按照最短任务来执行的的方法, 我们
        sjf_ta1 = Tex("$1$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)
        sjf_ta2 = Tex("$3$", font_size = 40, color = WHITE).next_to(process_group[0:2], DOWN, buff = 0)
        sjf_ta3 = Tex("$6$", font_size = 40, color = WHITE).next_to(process_group, DOWN, buff = 0)

        with self.voiceover(text="它的第一个进程是最短的也就是x,周转时间为1") as tracker:
            self.play(Indicate(process_group[0]))
            self.play(sjf_ta1.animate.move_to(DOWN*0.4+LEFT*3))
            plus1 = Tex("$+$").next_to(sjf_ta1)
            self.add(plus1)

        # 下图 process y 的周转时间是:
        with self.voiceover(text="第二短的是y,加上x的1就是3") as tracker:
            self.play(Indicate(process_group[0:2]))
            self.play(sjf_ta2.animate.next_to(sjf_ta1, RIGHT, buff = 0.8))
            plus2 = Tex("$+$").next_to(sjf_ta2)
            self.add(plus2)

        # process z 的周转时间是:
        with self.voiceover(text="加上最后的6") as tracker:
            self.play(Indicate(process_group))
            self.play(sjf_ta3.animate.next_to(sjf_ta2, RIGHT, buff = 0.8))

        sjf_ta_avg = Tex("$T_{average} = 10 / 3 = 3.33$", font_size = 35)
        with self.voiceover(text="所以sjf的周转时间的表现上是10除以3,等于3.33") as tracker:
            self.play(sjf_ta_avg.animate.next_to(sjf_ta3, RIGHT, buff= 1))
        fifo_ta_avg_result = Tex("$4.66$", font_size = 40, color=BLUE).next_to(sjf_ta_avg, RIGHT, buff=0.5)

        ####################
        # response time
        ####################
        sjf_rt1 = Tex("$0$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)
        sjf_rt2 = Tex("$1$", font_size = 40, color = WHITE).next_to(process_group[0:2], DOWN, buff = 0)
        sjf_rt3 = Tex("$3$", font_size = 40, color = WHITE).next_to(process_group, DOWN, buff = 0)

        with self.voiceover(text="在响应时间的表现上") as tracker:
            pass
        with self.voiceover(text="0") as tracker:
            self.play(Indicate(process_group[0]))
            self.play(sjf_rt1.animate.move_to(DOWN*2+LEFT*3))
            plus3 = Tex("$+$").next_to(sjf_rt1)
            self.add(plus3)

        # 下图 process y 的周转时间是:
        with self.voiceover(text="加上1") as tracker:
            self.play(Indicate(process_group[0:2]))
            self.play(sjf_rt2.animate.next_to(sjf_rt1, RIGHT, buff = 0.8))
            plus4 = Tex("$+$").next_to(sjf_rt2)
            self.add(plus4)

        # process z 的周转时间是:
        with self.voiceover(text="加上3") as tracker:
            self.play(Indicate(process_group))
            self.play(sjf_rt3.animate.next_to(sjf_rt2, RIGHT, buff = 0.8))

        sjf_rt_avg = Tex("$T_{average} = 4 / 3 = 1.33$", font_size = 35)
        with self.voiceover(text="最后得到的结果就是4除以3等于1.33") as tracker:
            self.play(sjf_rt_avg.animate.next_to(sjf_rt3, RIGHT, buff= 1))

        fifo_rt_avg_result = Tex("$1.66$", font_size = 40, color=BLUE).next_to(sjf_rt_avg, RIGHT, buff=0.5)

        with self.voiceover(text="对比之前的FIFO,我们可以看到,数据上有一定的提高.") as tracker:
            self.play(FadeIn(fifo_rt_avg_result),FadeIn(fifo_ta_avg_result))
        self.play(FadeOut(fifo_ta_avg_result), FadeOut(fifo_rt_avg_result))

        sjf_group = Group(sjf_ta1, sjf_ta2, sjf_ta3, sjf_ta_avg, sjf_rt1, sjf_rt2, sjf_rt3, sjf_rt_avg,plus1, plus2, plus3, plus4)
        self.play(FadeOut(sjf_group))


        r1 = Rectangle(color=RED, fill_opacity=0.5, width = 2, height = 0.5).scale(0.5).next_to(p1, RIGHT)
        r2 = Rectangle(color=RED, fill_opacity=0.5, width = 2, height = 0.5).scale(0.5).next_to(r1, RIGHT)
        r3 = Rectangle(color=RED, fill_opacity=0.5, width = 2, height = 0.5).scale(0.5).next_to(r2,RIGHT)
        r4 = Rectangle(color=RED, fill_opacity=0.5, width = 2, height = 0.5).scale(0.5).next_to(r3,RIGHT)
        r5 = Rectangle(color=RED, fill_opacity=0.5, width = 2, height = 0.5).scale(0.5).next_to(r4,RIGHT)
        rgroup = Group(r1, r2, r3, r4, r5)
        with self.voiceover(text="那么 SJF 存在什么问题吗? 它的问题是, 当有很多个短任务来到系统当中时") as tracker:
            self.wait(5)
            self.play(FadeIn(r1))
            self.play(FadeIn(r2))
            self.play(FadeIn(r3))
            self.play(FadeIn(r4))
            self.play(FadeIn(r5))

        with self.voiceover ("长任务也就是 3 天的这个任务, 将一直不会被执行. 我们会说它处于饥饿状态. 这个问题怎么解决呢?请将这个问题放在脑海中, 稍等我们将回来再看这个问题.") as tracker:
                self.play(Indicate(p3, run_time=tracker.get_remaining_duration()), FadeOut(rgroup))

        with self.voiceover(text="接下来,我们将来看:Round Robin算法,你会看到它在响应时间上能够做到很大的提升") as tracker:
            self.play(Indicate(rr,scale_factor=2, run_time=tracker.get_remaining_duration()))

        # 它的解决方案是, 将进程等分一个一个的小块, 它将有效的提高其响应时间.
        # 在我们的示例当中, 我们把进程按照 一天的时间进行等分. 这样我们就能够得到 RR 的情况下,
        # 三个进程的平均响应时间为 (0+1+2)/3 = 1

        rr_p1_1 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5).next_to(p1, DOWN, buff=0).scale(0.5)

        rr_p2_1 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5).next_to(p2, DOWN, buff=-0)
        rr_p2_2 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5).next_to(rr_p2_1, LEFT, buff=0)
        rr_p2_group = Group(rr_p2_1, rr_p2_2).scale(0.5)

        rr_p3_1 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5).next_to(p3, DOWN, buff=0)
        rr_p3_2 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5).next_to(rr_p3_1, LEFT, buff=0)
        rr_p3_3 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5).next_to(rr_p3_2, LEFT, buff=0)
        rr_p3_group = Group(rr_p3_1, rr_p3_2, rr_p3_3).scale(0.5)

        rr_process_group = Group(rr_p1_1, rr_p2_group, rr_p3_group)
        with self.voiceover(text="它的做法是,将进程拆成等分的时间小块来执行") as tracker:
            self.play(
                rr_process_group.animate.arrange().next_to(timeline_group, DOWN,buff = 0.1)
            )

        with self.voiceover(text="在我们的实例当中,我们将进程拆成1天的等分时间片,然后按照sjf或者fifo的算法依序执行每一个小的等分的时间片") as tracker:
            self.play(rr_p3_1.animate.set_color(RED))
            self.wait(0.1)
            self.play(rr_p2_1.animate.set_color(RED))
            self.wait(0.1)
            self.play(rr_p1_1.animate.set_color(RED))

        ##################
        # turnaround time
        ##################

        rr_ta1 = Tex("$ 3+5+6 = T_{average} = 14 / 3 = 4.66 $", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)
        with self.voiceover(text="它的响应时间能够达到多少呢?我们假设使用的是FIFO,那么周转时间一致") as tracker:
            self.play(rr_ta1.animate.next_to(tt,DOWN, buff=0.2))

        ##################
        # response time
        ##################
        rr_rt1 = Tex("$0$", font_size = 40, color = WHITE).next_to(rr_p3_1, DOWN, buff = 0)
        rr_rt2 = Tex("$1$", font_size = 40, color = WHITE).next_to(rr_p2_1, DOWN, buff = 0)
        rr_rt3 = Tex("$2$", font_size = 40, color = WHITE).next_to(rr_p1_1, DOWN, buff = 0)

        with self.voiceover(text="但是,它的响应时间能够得到很大的提升.") as tracker:
            pass
        with self.voiceover(text="进程z的响应时间为0加上") as tracker:
            self.play(Indicate(rr_p3_1[0]))
            self.play(rr_rt1.animate.move_to(DOWN*2+LEFT*3))
            plus3 = Tex("$+$").next_to(rr_rt1)
            self.add(plus3)

        with self.voiceover(text="进程y的响应时间1加上") as tracker:
            self.play(Indicate(rr_p2_1))
            self.play(rr_rt2.animate.next_to(rr_rt1, RIGHT, buff = 0.8))
            plus4 = Tex("$+$").next_to(rr_rt2)
            self.add(plus4)

        with self.voiceover(text="进程x的响应时间2") as tracker:
            self.play(Indicate(rr_p1_1),Indicate(rr_p2_1))
            self.play(rr_rt3.animate.next_to(rr_rt2, RIGHT, buff = 0.8))

        rr_rt_avg = Tex("$T_{average} = 3 / 3 = 1$", font_size = 35)
        rr_group = Group(rr_rt1, rr_rt2, rr_rt3, rr_rt_avg)

        with self.voiceover(text="最后它的平均响应时间是3除以3,就等于1.这样,有了Round Robin算法后,无论是FIFO,还是SJF,我们都可以保证响应时间上可以做到一致,先别着急离开视频,还记得我们前面提到的问题了吗?") as tracker:
            self.play(rr_rt_avg.animate.next_to(rr_rt3, RIGHT, buff= 1))


#        rr_group = Group(rr_ta1, rr_rt1, rr_rt2, rr_rt3, rr_rt_avg, plus3, plus4)
#        self.play(FadeOut(rr_group))



        with self.voiceover(text="问题是SJF,如何在短进程很多的情况下长进程仍然被执行呢?答案就是设置优先级.那么,这也就是MLFQ,优先级队列算法尝试做的事情.请期待一下下期的视频.谢谢.再见.") as tracker:
            self.play(
                FadeOut(process_group),
                FadeOut(timeline_group),
                FadeOut(tt_group),
                FadeOut(rt_group),
                FadeOut(rr_group),
                FadeOut(rr_ta1),
                FadeOut(rr_process_group),
                FadeOut(algorithms)
            )
            self.play(FadeIn(Text("MLFQ: Multi Level Feedback Queue"), run_time=3))
