from manim import *

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
        ratios = [0, 0.1, 0.5, 1, 2]

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
        l1 = Line(d1.get_center(), d2.get_center()).set_color(RED)
        x = ValueTracker(0)
        y = ValueTracker(0)
        d1.add_updater(lambda z: z.set_x(x.get_value()))
        d2.add_updater(lambda z: z.set_y(y.get_value()))
        l1.add_updater(lambda z: z.become(Line(d1.get_center(), d2.get_center())))

        self.add(d1, d2, l1)
        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(4))
        self.wait()
