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

class ArrangeTable(Scene):
    def construct(self):
        t = Table(
            [["true", "true", "true", "do_a"],
             ["false", "true", "true", "do_c"],
             ["true", "false", "true", "do_a"],
             ["true", "true", "false", "do_b"],
             ["false", "false", "true", "do_d"],
             ["false", "true", "false", "do_c"],
             ["true", "false", "false", "do_a"],
             ["false", "false", "false", "do_d"],],
            col_labels=[Text("X"), Text("Y"), Text("Z"), Text("Result")],
            include_outer_lines=True,
            color=GREEN
        ).scale(0.4).move_to(LEFT*0.3).set_row_colors(YELLOW)
        self.play(t.animate.arrange())

class SineCurveUnitCircle(Scene):
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4,0,0])
        self.curve_start = np.array([-3,0,0])

        #x_start = np.array([-6,0,0])
        #x_end = np.array([6,0.0])

        #y_start = np.array([-4, -2,0])
        #y_end = np.array([-4,2,0])

        #y_axis = Line(x_start, x_end)
        #y_axis = Line(y_start, y_end)

        #self.add(x_axis, y_axis)
        #self.add_x_labels()

        #self.origin_point =  np.array([-4,0,0])
        #self.curve_start = np.array([-3,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

        #x_labels = [
        #    MathTex("\pi"), MathTex("2 \pi"),
        #    MathTex("3 \pi"), MathTex("4 \pi"),
        #]

        #for i in range(len(x_labels)):
        #    x_labels[i].next_to(np.array([-1+2*i, 0,0]), DOWN)
        #    self.add(x_labels([i]))

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius = 0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt*rate)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset *4
            y = dot.get_center()[1]

            return Line(dot.get_center(), np.array([x,y,0]), color = YELLOW_A, stroke_width = 2)

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0]  + self.t_offset * 4
            y = dot.get_center()[1]

            new_line = Line(last_line.get_end(), np.array([x,y,0]),color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line,
                 dot_to_curve_line, sine_curve_line)
        self.wait(8.5)


