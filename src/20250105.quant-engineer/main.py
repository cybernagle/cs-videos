from manim import *
from manim.opengl import *
from manim_voiceover import VoiceoverScene
from manim.scene.moving_camera_scene import MovingCameraScene
from manim_voiceover.services.azure import AzureService

# below code did not work
# import manimforge as mf
# mf.setup()

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"


IMAGE="../../images"

SHADOW="#D3D3D3"


class QuantitativeEngineer(MovingCameraScene, VoiceoverScene):

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

    def curve(self):
        # 创建坐标轴
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 4, 0.5],
            axis_config={
                "include_numbers": False,
                "color": DARK_GRAY
            },
            color = WORD_A
        )

        # 定义模拟指数基金回报的函数
        def fund_return_function(x):
            return 0.1 * (x - 2) * (x - 6) * (x - 8) / 5 + 2

        # 绘制函数曲线
        fund_return_curve = axes.plot(fund_return_function, color=BLUE)

        # 添加坐标轴和曲线到场景
        self.add(axes, fund_return_curve)

        # 添加标题
        title = Text("指数基金回报曲线", font_size=36, color=OBJ_A).to_edge(UP)
        self.add(title)

        # 显示动画
        self.play(Create(axes), Create(fund_return_curve), Write(title))
        self.wait(2)

    def portfolio(self):

        def fund_return_function(x):
            return 0.05 * (x - 2) * (x - 6) * (x - 8) * np.sin(5 * x)

    def portfolio_instance(self):

        tiktok = ImageMobject(f"{IMAGE}/logo-tiktok.png").scale(0.3)
        amazon = ImageMobject(f"{IMAGE}/logo-aws.png").scale(0.3)
        facebook = ImageMobject(f"{IMAGE}/logo-facebook.png").scale(0.3)
        google = ImageMobject(f"{IMAGE}/logo-google.png").scale(0.3)
        microsoft = ImageMobject(f"{IMAGE}/logo-microsoft.png").scale(0.3)
        netflix = ImageMobject(f"{IMAGE}/logo-netflix.png").scale(0.3)

        # 图像列表
        images = [tiktok, amazon, facebook, google, microsoft, netflix]

        # 创建图像组
        image_group = Group(*images
        ).arrange(RIGHT, buff=0.5).move_to(UP * 1.5)

        # 添加图像到场景
        self.play(FadeIn(image_group))

        x_labels = [MathTex(f"x_{{{i+1}}}", color=BLACK) for i in range(len(images))]

        # 将每个标签放置在对应的图像下方
        for image, label in zip(image_group, x_labels):
            label.next_to(image, DOWN, buff=0.5)

        # 将标签组合成一个 VGroup
        x_labels_group = VGroup(*x_labels)

        self.play(FadeIn(x_labels_group))

        # 创建 b1, b2, b3, b4, b5, b6 标签
        b_labels = [MathTex(f"b_{i+1}", color=RED) for i in range(len(images))]

        for b, x in zip(b_labels, x_labels):
            b.next_to(x, LEFT, buff=0.1)

        b_labels_group = VGroup(*b_labels)

        alpha_label = MathTex(f"alpha  +", color=RED).next_to(b_labels_group, LEFT, buff=0.1)

        # 创建加号
        plus_signs = [MathTex("+", color=RED) for _ in range(len(images) - 1)]
        for p, x in zip(plus_signs, x_labels):
            p.next_to(x, RIGHT, buff=0.2)
        plus_signs_group = VGroup(*plus_signs)

        self.play(
            FadeIn(b_labels_group),
            FadeIn(alpha_label),
            FadeIn(plus_signs_group)
        )


        equal_sign = MathTex("=").next_to(x_labels_group, RIGHT, buff=0.2)
        y_label = Text(r"= Y", color=RED).scale(0.8).next_to(x_labels_group, RIGHT, buff=0.2)
        index_label = Text(r"= 指数基金(sp500)", color=RED).scale(0.45).next_to(x_labels_group, RIGHT, buff=0.2)
        self.play(FadeIn(y_label))
        self.play(FadeOut(y_label))
        self.play(FadeIn(index_label))

        self.wait(2)

    def construct(self):
        self.human_voice()

        """
        people = OpenGLImageMobject(f"{IMAGE}/people-head-00.png").shift(UP)
        # people = ImageMobject(f"{IMAGE}/people-head-00.png").shift(UP)
        scene1 = "我们知道, 量化工程师无非是要选择买或者卖股票, 那么, 这个过程中,他们需要量化的是什么呢?"

        # with self.voiceover(text=scene1) as tracker:
        self.play(FadeIn(people))
        people.shift(RIGHT*5)
        # self.wait(10)
        #  self.vo

        index = Text("指数基金", color=WORD_A)
        self.play(FadeIn(index))
        self.interactive_embed()
        """
        # self.curve()
        # self.portfolio_instance()
