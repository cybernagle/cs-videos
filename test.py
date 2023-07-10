from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        #square.rotate(PI/3) # pi/n 代表倾斜度
        square.set_fill(BLUE, opacity=0.5)
        square.next_to(circle, LEFT, buff = 4) # buff 代表中间的间隔


        self.play(Create(square), Create(circle))
        #self.play(Transform(square,circle))
        #self.play(FadeOut(square))


class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        self.play(Create(square))
        self.play(square.animate.shift(2*LEFT))

        self.play(ReplacementTransform(square, circle))
        self.play(circle.animate.set_fill(PINK, opacity=0.5))

class DifferentRotation(Scene):
    def construct(self):
        left_square = Rectangle(color=BLUE, fill_opacity=0.7).shift(4*LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(4*RIGHT)

        self.play(left_square.animate.rotate(PI/2), Rotate(right_square, angle=PI), run_time=2)

        self.wait()

class RectangleExample(Scene):
    def construct(self):
        vmem = Rectangle(color=BLUE, fill_opacity=0.1, width=2.0, height=4.0, grid_xstep=2.0, grid_ystep=0.5).shift(4*LEFT)
        pmem = Rectangle(color=YELLOW, fill_opacity=0.1, width=2.0, height=4.0, grid_xstep=2.0, grid_ystep=0.5).shift(4*RIGHT)
        page_table = Rectangle(color=GREEN, fill_opacity=0.1, width=2.0, height=2.0, grid_xstep=1.0, grid_ystep=0.5)

        self.play(Create(vmem))
        self.play(Create(pmem))
        self.play(Create(page_table))
        self.wait()

class LagRatios(Scene):
    def construct(self):
        ratios = [0, 0.3, 0.6, 0.9, 1.2]

        group = VGroup(*[Dot() for _ in range(4)]).arrange_submobjects()
        groups = VGroup(*[group.copy() for _ in ratios]).arrange_submobjects(buff=0.5)
        self.add(groups)

        self.add(Text("lag_ratio = ", font_size = 36).next_to(groups, UP, buff = 1.5))
        for group, ratio in zip(groups, ratios):
            self.add(Text(str(ratio), font_size= 36).next_to(group, UP))

        self.play(AnimationGroup(*[
            group.animate(lag_ratio=ratio, run_time=1.5).shift(DOWN*2)
            for group, ratio in zip(groups, ratios)

        ]))

        self.play(groups.animate(run_time=1, lag_ratio=0.1).shift(UP*2))


class BooleanOperations(Scene):
    def construct(self):
        ellipse1 = Ellipse(
            width=4.0, height=5.0, fill_opacity = 0.5,color=BLUE, stroke_width=10
        ).move_to(LEFT)
        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        bool_ops_text = MarkupText("Boolean Operation").next_to(ellipse1, UP*3)
        ellipse_group = Group( bool_ops_text,ellipse1, ellipse2).move_to(LEFT*2)
        self.play(FadeIn(ellipse_group))

        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity = 0.5)
        self.play(i.animate.scale(0.25).move_to(RIGHT * 5 + UP * 2.5))
        intersection_text = Text("Intersection", font_size = 23).next_to(i, UP)
        self.play(FadeIn(intersection_text))

        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        union_text = Text("Union", font_size = 23)
        self.play(u.animate.scale(0.3).next_to(i, DOWN, buff=union_text.height * 3))
        union_text.next_to(u, UP)
        self.play(FadeIn(union_text))

        e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        exclusion_text = Text("Exclusion", font_size = 23)
        self.play(e.animate.scale(0.3).next_to(u, DOWN, buff=exclusion_text.height * 3.5))
        exclusion_text.next_to(e, UP)
        self.play(FadeIn(exclusion_text))

        d = Difference(ellipse1, ellipse2, color=PINK, fill_opacity=0.5)
        difference_text = Text("Difference", font_size = 23)
        self.play(d.animate.scale(0.3).next_to(u, LEFT, buff=difference_text.height * 3.5))
        difference_text.next_to(d, UP)
        self.play(FadeIn(difference_text))


class BraceAnnotations(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        b1text = Text("hhh", font_size = 23)
        #b1text = b1.get_text("hhh")
        b1text.next_to(b1, DOWN)
        b2 = Brace(line, direction=line.copy().rotate(PI/2).get_unit_vector())
        #b2text = Text("x-x_1", font_size = 23)
        #b2text.next_to(b2, UP*0.1, RIGHT*4)
        b2text = b2.get_tex("x-x_1")
        self.add(line, dot, dot2, b1, b2, b1text, b2text)

class VectorArror(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(ORIGIN, [2,2,0], buff = 0)
        numberplane = NumberPlane()

        origin_text = Text('(0, 0)').next_to(dot, DOWN)
        tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)
        self.add(numberplane, dot, arrow, origin_text, tip_text)

class GradientImageFromArray(Scene):
    def construct(self):
        n = 512
        imageArray = np.uint8(
            [[i * 256 / n for i in range(0,n)] for _ in range(0, 256)]
        )

        image = ImageMobject(imageArray).scale(2)
        image.background_rectangle = SurroundingRectangle(image, GREEN)
        self.add(image, image.background_rectangle)


class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius = 1, color = BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([2,0,0], [5,0,0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point = [2, 0 , 0]), run_time = 1.5)
        self.wait()

class MovingAround(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=0.5)

        self.play(square.animate.shift(LEFT))
        self.play(square.animate.set_fill(ORANGE))
        self.play(square.animate.scale(0.3))
        self.play(square.animate.scale(2))
        self.play(square.animate.rotate(2))

class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT,RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving,radius = 0.5 + 3*SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )

        self.add(line1, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point = rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(
                Angle(
                    line1, line_moving, radius = 0.5, other_angle=False
                )
            )
        )

        tex.add_updater(
            lambda x:x.move_to(
                Angle(
                    line1, line_moving, radius = 0.5 + 3*SMALL_BUFF, other_angle = False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))

class MovingDots(Scene):
    def construct(self):
        d1, d2 = Dot(color=BLUE), Dot(color=GREEN)
        dg = VGroup(d1,d2).arrange(RIGHT,buff=1)
        #l1 = Line(d1.get_center(), d2.get_center()).set_color(RED)
        x = ValueTracker(0)
        y = ValueTracker(0)
        d1.add_updater(lambda z: z.set_x(x.get_value()))
        #d2.add_updater(lambda z: z.set_y(y.get_value()))
        #l1.add_updater(lambda z: z.become(Line(d1.get_center(), d2.get_center())))

        self.add(d1)#, d2, l1)
        self.play(x.animate.set_value(5))
        #self.play(y.animate.set_value(4))
        self.wait()

class MovingGroupToDestination(Scene):
    def construct(self):
        group = VGroup(Dot(LEFT), Dot(ORIGIN), Dot(RIGHT,), Dot(2 * RIGHT)).scale(1.4)

        dest = Dot([4,3,0], color = YELLOW)
        self.add(group, dest)

        self.play(group.animate.shift(dest.get_center() - group[2].get_center()))
        self.wait(0.5)


class MovingFrameBox(Scene):
    def construct(self):
        text = MathTex(
            "\\frac{d}{dx}f(x)g(x)=", "f(x)\\frac{d}{dx}g(x)","+",
            "g(x)\\frac{d}{dx}f(x)"
        )
        self.play(Write(text))
        framebox1 = SurroundingRectangle(text[1], buff = .1)
        framebox2 = SurroundingRectangle(text[3], buff= .1)
        self.play(Create(framebox1))
        self.wait()
        self.play(
            ReplacementTransform(framebox1, framebox2),
        )
        self.wait()

class RotationUpdater(Scene):
    def construct(self):
        def update_forth(mobj,dt):
            mobj.rotate_about_origin(dt)
        def update_back(mobj, dt):
            mobj.rotate_about_origin(-dt)

        line_reference = Line(ORIGIN, LEFT).set_color(WHITE)
        line_moving = line_reference.copy().set_color(YELLOW)#Line(ORIGIN,LEFT).set_color(YELLOW)

        self.add(line_reference, line_moving)

        line_moving.add_updater(update_forth)
        self.wait(4)
        line_moving.remove_updater(update_forth)
        line_moving.add_updater(update_back)
        self.wait(4)
        line_moving.remove_updater(update_back)
        self.wait(2)



class MovingZoomedSceneAround(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor = 0.3,
            zoomed_display_height = 1,
            zoomed_display_width = 6,
            image_frame_stroke_width = 20,
            zoomed_camera_config = {
                "default_frame_stroke_width": 3
            },
            **kwargs
        )
    def construct(self):
        dot = Dot().shift(UL*2)
        image = ImageMobject(np.uint8([[0, 100, 30, 200],
                                       [255, 0, 5, 33]
                                       ]))
        image.height = 7
        frame_text = Text("Frame", color = PURPLE, font_size = 67)
        zoomed_camera_text = Text("Zoomed camera", color = RED, font_size = 67)

        self.add(image, dot)

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff = MED_SMALL_BUFF)
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        frame_text.next_to(frame, DOWN)
        self.play(Create(frame), FadeIn(frame_text, shift=UP))
        self.wait()

class MemoryVisualization(VoiceoverScene):
    def construct(self):
        # You can choose from a multitude of TTS services,
        # or in this example, record your own voice:
        self.set_speech_service(RecorderService())

        clang = Code("main.c", color=WHITE).shift(2*UP)
        asm  = Text("mov 0x1,-0x4(%rpb)")

        with self.voiceover(text="这是一小段C代码") as tracker:
            self.play(Create(clang))
            self.play(clang.animate.shift(DOWN*2))
            self.wait(2)

        with self.voiceover(text=" 其中第四行代码 a =1 在经过编译以后,我们可以得到这条指令") as tracker:
            self.play(
                ReplacementTransform(clang, asm), run_time=2
            )

        reg = asm[-5:-1].copy()
        heightlight = SurroundingRectangle(asm[-5:-1], RED, buff = .1)

        with self.voiceover(text=" 请注意看 rbp 这个寄存器, 它存储了 a 的虚拟地址") as tracker:
            self.play(Create(heightlight))

        address = Rectangle(color=RED, fill_opacity=0.5, width=2, height=0.5)

        with self.voiceover(text=" 这个虚拟地址指向了黄色的这块区域") as tracker:
            self.play(ReplacementTransform(asm, address), FadeOut(heightlight))

        main_mem = Rectangle(color=BLUE, fill_opacity=0.1, width=2, height=4, grid_xstep=2.0, grid_ystep=0.5).shift(DOWN*0.25)
        with self.voiceover(text=" 这是该区域在虚拟内存当中的位置.") as tracker:
            self.play(Create(main_mem))

        mem_group = VGroup(address, main_mem)
        self.play(mem_group.animate.shift(LEFT*4))

        rbp_addr = Tex(r"$rbp = \texttt{0x4567} \rightarrow$", font_size = 36).next_to(address, RIGHT, buff = 0.1)

        with self.voiceover(text=" 我们假设这块区域的地址是 0x4567.") as tracker:
            self.play(Create(rbp_addr))

        self.wait(1)
        binary = MathTable(
            [["0","1","0","0","0","1","0","1","0","1","1","0","0","1","1","1"]],
            include_outer_lines=True,
            v_buff=0.1,
            h_buff=0.1
        ).next_to(rbp_addr, RIGHT, buff = 0.1)


        binary.add_highlighted_cell((0,1), color=YELLOW)
        binary.add_highlighted_cell((0,2), color=YELLOW)
        binary.add_highlighted_cell((0,3), color=YELLOW)
        binary.add_highlighted_cell((0,4), color=YELLOW)

        # 为 binary 打上标签.
        vpn = Text("虚拟页号VPN", color=YELLOW , font_size=20)
        vpn.next_to(binary.get_cell((0,2)), DOWN, buff = 0.1)

        offset = Text("偏移量OffSet", color=WHITE, font_size=20)
        offset.next_to(binary.get_cell((0,11)), DOWN, buff=0.1)

        with self.voiceover(text=" 地址 4567 被转换成二进制后如图所示") as tracker:
            self.play(Create(binary))
        with self.voiceover(text=" 其中前四位也就是黄色区域是虚拟页号, 后面 12 位白色的是偏移量, 代表在一个页里面的位置.") as tracker:
            self.play(Create(vpn), Create(offset))
        # 把 binary 和 rbp 和内存都group 一下移动到屏幕上方.
        binary_group = VGroup(binary, vpn, offset)

        vm_group = VGroup(mem_group, rbp_addr, binary_group)
        self.play(vm_group.animate.shift(UP * 2))

        # 创建一个页表
        page_table = Table(
            [["0110", "1001"],
             ["0100", "0110"],
             ["0101", "0010"],
             ["0000", "1000"]],
            col_labels=[Text("VPN"), Text("PFN")],
            include_outer_lines=True
        ).set_column_colors(YELLOW).scale(0.3)


        with self.voiceover(text=" 这是我们的页表") as tracker:
            self.play(Create(page_table), Create(Text("页表", font_size=20).next_to(page_table,DOWN, buff=0.1)))
        with self.voiceover(text=" 根据虚拟地址里面的虚拟页号") as tracker:
            self.play(Indicate(vpn))
        with self.voiceover(text=" 我们找到在对应页表中的位置") as tracker:
            self.play(Indicate(page_table.get_cell((3,1))))
        with self.voiceover(text=" 然后, 我们就可以找到对应的物理页真") as tracker:
            self.play(Indicate(page_table.get_cell((3,2))))

        pfn = MathTable(
            [["0","1","1","0"]],
            include_outer_lines=True,
            v_buff=0.1,
            h_buff=0.1
        ).shift(DOWN*2).shift(RIGHT*0.5).set_row_colors(YELLOW)

        # moving from page table
        pfn_from_pt = page_table.get_cell((3,2)).copy()

        with self.voiceover(text=" 紧接着, 我们取出物理页真") as tracker:
            self.play(pfn_from_pt.animate.scale(2).move_to(DOWN*2))
            self.play(Transform(pfn_from_pt, pfn))


        # moving from binary
        offset_from_binary = binary.get_rows()[0][-12:]
        self.play(offset_from_binary.animate.move_to(DOWN*2+RIGHT*2.8))

        pfn_offset = MathTable(
            [["0","1","0","1","0","1","1","0","0","1","1","1"]],
            include_outer_lines=True,
            v_buff=0.1,
            h_buff=0.1
        )
        pfn_offset.next_to(pfn, RIGHT, buff=0)

        with self.voiceover(text=" 把物理页者和虚拟地址当中的偏移量组合起来, 我们就得到了相应的物理地址,这就是虚拟地址通过页表转换成物理地址的过程.") as tracker:
            self.play(offset_from_binary.animate.move_to(pfn_offset))
            self.play(Create(pfn_offset))
            self.remove(offset_from_binary)

            self.play(Create(Text("物理地址", font_size = 20).next_to(pfn_offset[8], DOWN, buff=0.1)))

        self.wait()


class LangChain(Scene):
    def construct(self):
        pass


class DiffBetweenForkAndExec(Scene):
    def construct(self):
        pass

class ProportionalShare(Scene):
    def construct(self):
        pass


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
        fifo_ta_avg_result = Tex("$4.66$", font_size = 40, color=BLUE).next_to(sjf_ta_avg, RIGHT, buff=0.5)

        ####
        # response time
        ####
        sjf_rt1 = Tex("$0$", font_size = 40, color = WHITE).next_to(p1, DOWN, buff = 0)
        sjf_rt2 = Tex("$1$", font_size = 40, color = WHITE).next_to(process_group[0:2], DOWN, buff = 0)
        sjf_rt3 = Tex("$3$", font_size = 40, color = WHITE).next_to(process_group, DOWN, buff = 0)

        self.play(Indicate(process_group[0]))
        self.play(sjf_rt1.animate.move_to(DOWN*2+LEFT*3))
        plus3 = Tex("$+$").next_to(sjf_rt1)
        self.add(plus3)

        # 下图 process y 的周转时间是:
        self.play(Indicate(process_group[0:2]))
        self.play(sjf_rt2.animate.next_to(sjf_rt1, RIGHT, buff = 0.8))
        plus4 = Tex("$+$").next_to(sjf_rt2)
        self.add(plus4)

        # process z 的周转时间是:
        self.play(Indicate(process_group))
        self.play(sjf_rt3.animate.next_to(sjf_rt2, RIGHT, buff = 0.8))

        sjf_rt_avg = Tex("$T_{average} = 4 / 3 = 1.33$", font_size = 35)
        self.play(sjf_rt_avg.animate.next_to(sjf_rt3, RIGHT, buff= 1))
        fifo_rt_avg_result = Tex("$1.66$", font_size = 40, color=BLUE).next_to(sjf_rt_avg, RIGHT, buff=0.5)
        self.play(FadeIn(fifo_rt_avg_result),FadeIn(fifo_ta_avg_result))
        self.wait(1)
        self.play(FadeOut(fifo_ta_avg_result), FadeOut(fifo_rt_avg_result))

        sjf_group = Group(sjf_ta1, sjf_ta2, sjf_ta3, sjf_ta_avg, sjf_rt1, sjf_rt2, sjf_rt3, sjf_rt_avg,plus1, plus2, plus3, plus4)
        self.play(FadeOut(sjf_group))

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

