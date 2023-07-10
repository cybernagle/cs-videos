class Scheduling(Scene):
    def construct(self):
        # 首先说进程被执行?
        # 这是多个进程, 他们都将被调度程序调度到 CPU 上执行.
        p1 = Rectangle(color=GREEN, fill_opacity=0.5, width = 2, height = 0.5)
        self.play(p1.animate.scale(0.5).move_to(LEFT * 5.5 + UP * 1.5))
        p1_text = Text("进程x: 1day", font_size = 20).next_to(p1, DOWN)
        self.play(FadeIn(p1_text))
        p1_group = Group(p1, p1_text)

        p2 = Rectangle(color=GREEN, fill_opacity=0.5, width = 4, height = 0.5)
        self.play(p2.animate.scale(0.5).next_to(p1,DOWN, buff = p1.height * 4))
        p2_text = Text("进程y: 2day", font_size = 20).next_to(p2, DOWN)
        self.play(FadeIn(p2_text))
        p2_group = Group(p2, p2_text)

        p3 = Rectangle(color=GREEN, fill_opacity=0.5, width = 6, height = 0.5)
        self.play(p3.animate.scale(0.5).next_to(p2,DOWN, buff = p1.height * 4))
        p3_text = Text("进程z: 3day", font_size = 20).next_to(p3, DOWN)
        self.play(FadeIn(p3_text))
        p3_group = Group(p3, p3_text)

        process_group = Group(p1_group, p2_group, p3_group)
        #pg2 = process_group.copy()

        self.play(process_group.animate.arrange(LEFT))#.next_to(cpu, DOWN, buff=1))

        timeline = Arrow(start=5*LEFT, end=5* RIGHT, color = BLUE,buff = 1).next_to(process_group, DOWN, buff=0.1)
        overall_time = Text("总执行时间: 6天", font_size = 20).next_to(timeline, DOWN, buff = 0.1)
        timeline_group = Group(timeline, overall_time)
        self.play(Create(timeline), FadeIn(overall_time))
        self.play(ApplyWave(process_group))

        # 而不同的调度有着不同的效率
        self.play(process_group.animate.arrange(RIGHT))
        self.wait(1)
        self.play(process_group.animate.arrange(LEFT))
        self.wait(1)
        self.play(process_group.animate.arrange(RIGHT))
        self.wait(1)

        cpu = RoundedRectangle(color=BLUE, fill_opacity=0.5, corner_radius=1.5, height=4.0, width=4.0)
        self.play(cpu.animate.scale(0.2).move_to(LEFT*2.3 + UP*1.4))
        cpu_text = Text("CPU", font_size = 20).next_to(cpu, DOWN, buff=0.1)
        self.play(FadeIn(cpu_text))
        cpu_group = Group(cpu, cpu_text)

        # 而我们如何衡量一个不同调度方法或者算法的优劣?
        # 这就要求我们需要对我们的调度算法进行量化. 这也就引入了两个
        # 概念: turnaround time -- 周转时间. response time -- 响应时间
        # turnaround time 是: 进程结束的时间, 减去进程开始执行的时间.(brace)
        # response time 是: 进程启动的时间, 减去进程开始执行的时间.(brace)

        tt = Text("周转时间", font_size = 25).next_to(process_group, UP, buff = 1).shift(LEFT)
        tt_formula = Tex("$ = T_completion - T_arrival $", font_size = 20).next_to(tt, RIGHT, buff = 0.1)
        tt_group = Group(tt, tt_formula)
        rt = Text("响应时间", font_size = 25).next_to(tt, DOWN, buff=0.1)
        rt_formula = Tex("$ = T_firstrun - T_arrival $", font_size =  20).next_to(rt, RIGHT, buff = 0.1)

        rt_group = Group(rt, rt_formula)
        #with self.voiceover(text="") as tracker:
        self.play(Create(tt))
        self.play(FadeIn(tt_formula))
        # 下图 process x 的周转时间是:
        self.play(Indicate(process_group[0]))
        # 下图 process y 的周转时间是:
        self.play(Indicate(process_group[0:2]))
        # process z 的周转时间是:
        self.play(Indicate(process_group))

        self.play(Create(rt))
        self.play(FadeIn(rt_formula))
        # process x 的响应时间是 0
        # 0
        # process y 的响应时间是
        self.play(Indicate(process_group[0]))
        # process z 的响应时间是
        self.play(Indicate(process_group[0:2]))

        formula_group = Group(tt_group, rt_group)

        self.play(FadeOut(formula_group), FadeOut(cpu_group))

        ptimeline_group = Group(process_group, timeline_group)
        self.play(ptimeline_group.animate.move_to(UP*2))
        # 有了量化的标准, 接下来我们看看调度的一些算法, 看看他们的表现如何;
        # 本视频介绍的算法包括: fifo , sjf, rr, MLFQ , Proportional Share
        fifo = Text("FIFO", font_size=25, color = RED)
        sjf = Text("SJF", font_size=25, color = WHITE).next_to(fifo, DOWN, buff=0.1)
        rr = Text("Round Robin", font_size=25, color = ORANGE).next_to(sjf, DOWN, buff=0.1)
        mlfq = Text("MLFQ", font_size=25, color = PURPLE).next_to(rr, DOWN, buff=0.1)

        self.play(FadeIn(fifo))
        self.wait(0.5)
        self.play(FadeIn(sjf))
        self.wait(0.5)
        self.play(FadeIn(rr))
        self.wait(0.5)
        self.play(FadeIn(mlfq))

        algorithms = Group(fifo, sjf, rr, mlfq)
        self.play(algorithms.animate.move_to(LEFT * 5))

        # 首先谈一下 First In First Out, FIFO 算法, 它的调度是按照进程来的顺序, 依次执行(3, 1, 2)
        self.play(Indicate(fifo))
        # (添加一个 point, 添加一条线, 再转换成数字. 然后数字相加)
        # 在我们的上图示例当中, fifo 的调度顺序就是 x, y ,z
        # 而它的平均周转时间是 ( 3 + 5 + 6 ) / 14 = 4.66
        # 它的平均响应时间是 (0+3+4) / 3 = 2.33

        ####
        # turnaround time
        ####
        self.play(tt.animate.next_to(process_group, DOWN , buff = 1.6))
        ta1 = Tex("$3$", font_size = 40, color = WHITE).next_to(p3, DOWN, buff = 0)
        ta2 = Tex("$5$", font_size = 40, color = WHITE).next_to(p2, DOWN, buff = 0)
        ta3 = Tex("$6$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)


        self.play(Indicate(process_group[2]))
        self.play(ta1.animate.move_to(DOWN*0.4+LEFT*3))
        plus1 = Tex("$+$").next_to(ta1)
        self.add(plus1)

        # 下图 process y 的周转时间是:
        self.play(Indicate(process_group[1:3]))
        self.play(ta2.animate.next_to(ta1, RIGHT, buff = 0.8))
        plus2 = Tex("$+$").next_to(ta2)
        self.add(plus2)

        # process z 的周转时间是:
        self.play(Indicate(process_group))
        self.play(ta3.animate.next_to(ta2, RIGHT, buff = 0.8))

        ta_avg = Tex("$T_{average} = 14 / 3 = 4.66$", font_size = 35)
        self.play(ta_avg.animate.next_to(ta3, RIGHT, buff= 1))

        ###
        # response time
        ###
        self.play(rt.animate.next_to(process_group, DOWN , buff = 3))
        rt1 = Tex("$0$", font_size = 40, color = WHITE).next_to(p3, DOWN, buff = 0)
        rt2 = Tex("$3$", font_size = 40, color = WHITE).next_to(p2, DOWN, buff = 0)
        rt3 = Tex("$5$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)


        self.play(Indicate(process_group[2]))
        self.play(rt1.animate.move_to(DOWN*2+LEFT*3))
        plus3 = Tex("$+$").next_to(rt1)
        self.add(plus3)

        # 下图 process y 的周转时间是:
        self.play(Indicate(process_group[1:3]))
        self.play(rt2.animate.next_to(rt1, RIGHT, buff = 0.8))
        plus4 = Tex("$+$").next_to(rt2)
        self.add(plus4)

        # process z 的周转时间是:
        self.play(Indicate(process_group))
        self.play(rt3.animate.next_to(rt2, RIGHT, buff = 0.8))
        rt_avg = Tex("$T_{average} = 8 / 3 = 1.66$", font_size = 35)
        self.play(rt_avg.animate.next_to(rt3, RIGHT, buff= 1))

        fifo_group = Group(ta1, ta2, ta3, ta_avg, rt1, rt2, rt3, rt_avg, plus1, plus2, plus3, plus4)
        self.play(FadeOut(fifo_group))

        # 接下来我们看一下 Short Job First, SJF, 是进程进来以后, 找出最短执行时间的, 进行执行.(1,2,3)
        self.play(Indicate(sjf))
        # 它的平均周转时间可以达到 ( 1 + 3 + 6 ) / 3 = 3.33
        # 它的平均响应时间可以达到 (0+1+3) / 3 = 1.33
        # 这个时候 FIFO 的执行时间可以得到很高的提升.
        # 我们可以看到 FIFO 根据任务抵达的时间不同, 收到的影响也很大.
        # 而 FIFO 这种按照最短任务来执行的的方法, 我们
        sjf_ta1 = Tex("$1$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)
        sjf_ta2 = Tex("$3$", font_size = 40, color = WHITE).next_to(process_group[0:2], DOWN, buff = 0)
        sjf_ta3 = Tex("$6$", font_size = 40, color = WHITE).next_to(process_group, DOWN, buff = 0)

        self.play(Indicate(process_group[0]))
        self.play(sjf_ta1.animate.move_to(DOWN*0.4+LEFT*3))
        plus1 = Tex("$+$").next_to(sjf_ta1)
        self.add(plus1)

        # 下图 process y 的周转时间是:
        self.play(Indicate(process_group[0:2]))
        self.play(sjf_ta2.animate.next_to(sjf_ta1, RIGHT, buff = 0.8))
        plus2 = Tex("$+$").next_to(sjf_ta2)
        self.add(plus2)

        # process z 的周转时间是:
        self.play(Indicate(process_group))
        self.play(sjf_ta3.animate.next_to(sjf_ta2, RIGHT, buff = 0.8))

        sjf_ta_avg = Tex("$T_{average} = 10 / 3 = 3.33$", font_size = 35)
        self.play(sjf_ta_avg.animate.next_to(sjf_ta3, RIGHT, buff= 1))
        fifo_ta_avg_result = Tex("$4.66$").next_to(sjf_ta_avg, RIGHT, buff=0.5)

        ####
        # response time
        ####
        sjf_rt1 = Tex("$0$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)
        sjf_rt2 = Tex("$1$", font_size = 40, color = WHITE).next_to(process_group[0:2], DOWN, buff = 0)
        sjf_rt3 = Tex("$3$", font_size = 40, color = WHITE).next_to(process_group, DOWN, buff = 0)

        self.play(Indicate(process_group[0]))
        self.play(sjf_rt1.animate.move_to(DOWN*2+LEFT*3))
        plus1 = Tex("$+$").next_to(sjf_rt1)
        self.add(plus1)

        # 下图 process y 的周转时间是:
        self.play(Indicate(process_group[0:2]))
        self.play(sjf_rt2.animate.next_to(sjf_rt1, RIGHT, buff = 0.8))
        plus2 = Tex("$+$").next_to(sjf_rt2)
        self.add(plus2)

        # process z 的周转时间是:
        self.play(Indicate(process_group))
        self.play(sjf_rt3.animate.next_to(sjf_rt2, RIGHT, buff = 0.8))

        sjf_rt_avg = Tex("$T_{average} = 4 / 3 = 1.33$", font_size = 35)
        self.play(sjf_rt_avg.animate.next_to(sjf_rt3, RIGHT, buff= 1))
        fifo_rt_avg_result = Tex("$1.66$", font_size = 40).next_to(sjf_rt_avg, RIGHT, buff=0.5)
        self.play(FadeIn(fifo_rt_avg_result),FadeIn(fifo_ta_avg_result))
        self.wait(1)
        self.play(FadeOut(fifo_ta_avg_result), FadeOut(fifo_rt_avg_result))

        # 同学就发现了, FIFO 是不是也可以达到这样的效果? 答案是肯定的. 如果进程的进入顺序是按照从小到大抵达我们的系统. 那么 FIFO 的效果是和 SJF 一致的. 所以结论是, FIFO 算法会根据进程的进入顺序不同, 再效率的表现上面不同.
        # 那么 SJF 存在什么问题吗? 它的问题是, 当有很多个短任务来到系统当中时, 长任务也就是 3 天的这个任务, 将一直不会被执行. 我们会说它处于饥饿状态. 请将这个问题放在脑海中, 稍等我们将回来再看这个问题.


        # 接下来,我们来思考一个问题, 关于响应时间, 我们能否通过某种算法提高?答案是确定的: Round Robin
        self.play(Indicate(rr))
        # 它的解决方案是, 将进程等分, 它将有效的提高其响应时间.
        # 在我们的示例当中, 我们把进程按照 一天的时间进行等分. 这样我们就能够得到 RR 的情况下,
        # 三个进程的平均响应时间为 (0+1+2)/3 = 1

        # 回到我们之前的问题, SJF 的问题在于, 长进程一直不能被执行从而产生饥饿.
        # 为了解决这个问题, 谈一下 Multi Level Feedback Queue
        self.play(Indicate(mlfq))

