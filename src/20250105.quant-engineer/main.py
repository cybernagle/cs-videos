from manim import *
from manim.opengl import *
from manim_voiceover import VoiceoverScene
from manim.scene.moving_camera_scene import MovingCameraScene
from manim_voiceover.services.azure import AzureService


# import numpy as np

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
    labels = VGroup()

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
        # 创建二维坐标系，坐标从0开始
        axes = NumberPlane(
            x_range=[0, 30, 5],  # x轴范围从0到30
            y_range=[0, 10000, 1000],  # y轴范围从0到10000
            x_length=10,        # x轴长度
            y_length=6,         # y轴长度
            background_line_style={
                "stroke_color": LIGHT_GRAY ,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }
        )
        self.add(axes)

        def fund_return_function(x):
            np.random.seed(int(x * 10))  # 根据 x 值设置随机种子，使函数具有随机性
            base_value = 9000 / (np.exp(0.1 * 30) * (1 + 0.1 * np.sin(10) + 0.05 * np.sin(50) + 0.05 * np.sin(100)))
            return base_value * np.exp(0.1 * x) * (1 + 0.1 * np.sin(x) + 0.05 * np.sin(5 * x) + 0.05 * np.sin(10 * x))

        def customize_portfolio(x):
            # 根据 x 值设置随机种子，使函数具有随机性
            np.random.seed(int(x * 10))
            # 增加正弦项的幅度以增加波动性
            amplitude_factor = 3  # 这个因子可以调整波动的幅度
            # 定义原始函数
            original_value = np.exp(0.1 * x) * (1 + amplitude_factor * 0.1 * np.sin(x) + amplitude_factor * 0.05 * np.sin(5 * x) + amplitude_factor * 0.05 * np.sin(10 * x))
            # 计算在 x = 30 时的修正因子
            correction_factor = 6000 / (np.exp(0.1 * 30) * (1 + amplitude_factor * 0.1 * np.sin(30) + amplitude_factor * 0.05 * np.sin(150) + amplitude_factor * 0.05 * np.sin(300)))
            # 返回修正后的函数值
            return correction_factor * original_value

        def your_portfolio(x):
            np.random.seed(int(x * 10))  # 根据 x 值设置随机种子，使函数具有随机性
            base_value = 6000 / (np.exp(0.1 * 30) * (1 + 0.1 * np.sin(10) + 0.05 * np.sin(50) + 0.05 * np.sin(100)))
            return base_value * np.exp(0.1 * x) * (1 + 0.1 * np.sin(x) + 0.05 * np.sin(5 * x) + 0.05 * np.sin(10 * x))

        # 绘制函数曲线

        fund_return_curve = axes.plot(fund_return_function, color=BLUE)
        customize_curve = axes.plot(customize_portfolio, color=PURPLE)
        index_curve_pos = axes.c2p(30, fund_return_function(30))
        customize_curve_pos = axes.c2p(30, customize_portfolio(30))

        # 添加坐标轴和曲线到场景
        self.add(axes, fund_return_curve)

        index_title = Text(
            "指数基金回报", font_size=20, color=BLUE
        ).move_to(index_curve_pos).shift(DOWN*0.4)
        customize_title = Text(
            "个人组合回报", font_size=20, color=PURPLE
        ).move_to(customize_curve_pos).shift(DOWN*0.4)

        sp500 = "大部分人应该都听过指数基金这个东西. 如标普500指数基金，包含了500家大型的不同行业公司的股票，能够反映整体市场的表现, 甚至说经济的表现."

        with self.voiceover(text=sp500) as tracker:
            self.play(Create(axes), Create(fund_return_curve))
            self.play(Write(index_title))

        portfolio_text = "量化工程师将使用指数基金作为基准, 表现优于指数, 我们说它打败了市场.否则, 它就是被市场击败."
        with self.voiceover(text=portfolio_text) as tracker:
            self.play(Create(customize_curve))
            self.play(Write(customize_title))

    def portfolio_instance(self):

        tiktok = ImageMobject(f"{IMAGE}/logo-tiktok.png").scale(0.3)
        amazon = ImageMobject(f"{IMAGE}/logo-aws.png").scale(0.3)
        facebook = ImageMobject(f"{IMAGE}/logo-facebook.png").scale(0.3)
        google = ImageMobject(f"{IMAGE}/logo-google.png").scale(0.3)
        microsoft = ImageMobject(f"{IMAGE}/logo-microsoft.png").scale(0.3)
        netflix = ImageMobject(f"{IMAGE}/logo-netflix.png").scale(0.3)

        images = [tiktok, amazon, facebook, google, microsoft, netflix]

        image_group = Group(
            *images
        ).arrange(RIGHT, buff=0.5).move_to(UP * 1.5)

        pick = "作为量化工程师, 将首先选择自己的价值组合."
        with self.voiceover(text=pick) as tracker:
            self.play(FadeIn(image_group))

        x_labels = [MathTex(f"x_{{{i+1}}}", color=BLACK) for i in range(len(images))]

        for image, label in zip(image_group, x_labels):
            label.next_to(image, DOWN, buff=2)

        x_labels_group = VGroup(*x_labels)

        quantlize = "随后将其量化为 x1 到 xn."
        with self.voiceover(text=quantlize) as tracker:
            self.play(FadeIn(x_labels_group))

        b_labels = [MathTex(f"b_{i+1}", color=RED) for i in range(len(images))]

        for b, x in zip(b_labels, x_labels):
            b.next_to(x, LEFT, buff=0.1)

        b_labels_group = VGroup(*b_labels)

        alpha_label = MathTex(f"alpha  +", color=RED).next_to(b_labels_group, LEFT, buff=0.1)

        plus_signs = [MathTex("+", color=RED) for _ in range(len(images) - 1)]
        for p, x in zip(plus_signs, x_labels):
            p.next_to(x, RIGHT, buff=0.2)
        plus_signs_group = VGroup(*plus_signs)

        equal_sign = MathTex("=").next_to(x_labels_group, RIGHT, buff=0.2)
        y_label = Text(r"= Y", color=RED).scale(0.8).next_to(x_labels_group, RIGHT, buff=0.2)
        index_label = Text(r"= 指数基金(sp500)", color=RED).scale(0.45).next_to(x_labels_group, RIGHT, buff=0.2)

        quant_index = "而基准指数的回报, 我们将其设为 y, 随后为自己的组合添加上权重 beta, 和 alpha"
        with self.voiceover(text=quant_index) as tracker:
            self.play(
                FadeIn(b_labels_group),
                FadeIn(alpha_label),
                FadeIn(plus_signs_group),
                FadeIn(y_label)
            )


        final = "这里的指数 Y 可以是指代我们前面提到的标普500"
        with self.voiceover(text=final) as tracker:
            self.play(FadeOut(y_label))
            self.play(FadeIn(index_label))

        defeat = "这里面的 alpha 为负时,  我们可以说组合被市场击败, 否则, 我们就击败了市场."
        with self.voiceover(text=defeat) as tracker:
            self.play(Indicate(alpha_label))

        self.labels.add(x_labels_group, b_labels_group, index_label, plus_signs_group, alpha_label)

        self.wait(2)

    def compute_alpha(self):
        # Create the computer image
        computer = ImageMobject(f"{IMAGE}/laptop.png").scale(0.8)
        linear_regression = "紧接着, 我们将公式进行线性回归运算."
        with self.voiceover(text=linear_regression) as tracker:
            self.play(FadeIn(computer))

            self.labels.next_to(computer, DOWN, buff=0.5)
            self.play(FadeIn(self.labels))

        # Create historical data text on the left
        historical_data = Text("历史数据", font_size=30, color=BLACK).shift( LEFT * 5 )
        arrow_to_computer = Arrow(
            start=historical_data.get_right(),
            end=computer.get_left(),
            buff=0.5, color=BLACK
        )

        history = "代入历史数据以后"

        with self.voiceover(text=history) as tracker:
            self.play(
                FadeIn(historical_data),
                FadeIn(arrow_to_computer)
            )

        # Create an arrow from the computer to the right
        arrow_to_right = Arrow(start=computer.get_right(), end=RIGHT * 5, buff=0.5, color=BLACK)
        alpha_label = MathTex(r"alpha", color=RED).scale(0.8).next_to(
            arrow_to_right,RIGHT , buff=0.5
        ).shift(UP*0.2)
        beta_label = MathTex(r"beta", color=RED).scale(0.8).next_to(
            arrow_to_right, RIGHT, buff=0.5
        ).shift(DOWN*0.2)

        ab = "我们就拥有了 alpha 和 beta"
        with self.voiceover(text=ab) as tracker:
            self.play(Write(arrow_to_right))
            self.play(FadeIn(alpha_label),FadeIn(beta_label))

    def alpha_perf(self):
        alpha = MathTex(r"\alpha", font_size=144, color=BLACK)

        equation = MathTex(
            r"\alpha = \begin{cases} "
            r" Volatility \\"
            r" Momentum \\"
            r" Macro Factors \\"
            r" \dots "
            r"\end{cases}", color=BLACK
        )
        perf = "得到了 alpha 以后, 需要从我们之前的方程式提取出更加细节的东西, 也被称之为 alpha 的性能. 比方说,上下波动是否很大?这个东西被称之为波动率; 之前买的人多吗?被称之为动量; 最近加息降息了吗?被称之为宏观因子; 等等等等, 最后, 我们就可以使用机器来将各个因子代入, 并且进行统计学习并根据其进行预测."
        with self.voiceover(text=perf) as tracker:
            self.play(Write(equation))

    def effect(self):
        # 创建二维坐标系，坐标从0开始
        ax = NumberPlane(
            x_range=[0, 30, 5],  # x轴范围从0到30
            y_range=[0, 10000, 1000],  # y轴范围从0到10000
            x_length=10,        # x轴长度
            y_length=6,         # y轴长度
            background_line_style={
                "stroke_color": LIGHT_GRAY ,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }
        )
        self.add(ax)

        # 定义随机波动函数
        def random_wave_func(x):
            np.random.seed(int(x * 10))  # 根据 x 值设置随机种子，使函数具有随机性
            base_value = 2000 / (np.exp(0.1 * 10) * (1 + 0.1 * np.sin(10) + 0.05 * np.sin(50) + 0.05 * np.sin(100)))
            return base_value * np.exp(0.1 * x) * (1 + 0.1 * np.sin(x) + 0.05 * np.sin(5 * x) + 0.05 * np.sin(10 * x))

        def exp2(x):
            # 定义原始函数
            original_value = np.exp(0.2 * x) * (1 + 0.1 * np.sin(x) + 0.05 * np.sin(5 * x) + 0.05 * np.sin(10 * x))
            # 计算修正因子
            correction_factor_10 = 2000 / (np.exp(0.2 * 10) * (1 + 0.1 * np.sin(10) + 0.05 * np.sin(50) + 0.05 * np.sin(100)))
            correction_factor_20 = 6000 / (np.exp(0.2 * 20) * (1 + 0.1 * np.sin(20) + 0.05 * np.sin(100) + 0.05 * np.sin(200)))
            if x <= 10:
                return correction_factor_10 * original_value
            else:
                return correction_factor_20 * original_value

        def exp3(x):
            if x <= 20:
                return 6000
            elif x <= 25:
                # 指数下降
                return 6000 * np.exp(-0.2 * (x - 20))
            else:
                # 随机运动
                np.random.seed(int(x * 10))  # 为了使随机结果可重复
                return 4000 + 1000 * np.random.uniform(-1, 1)

            # 定义原始函数
            pass


        step1 = "所以我们也可以看到, 当一些宏观的数据出现的时候, 市场就会有比较大的波动."
        wave_graph = ax.plot(random_wave_func, x_range=[0, 10], color=BLUE)

        with self.voiceover(text=step1) as tracker:
            self.play(Create(wave_graph), run_time=tracker.duration)

        end_point1 = ax.c2p(10, random_wave_func(10))
        macro = Text("联储降息", color=WORD_A).scale(0.5).move_to(end_point1).shift(UP*0.2)
        step2 = "比如说, 联储的降息, 就会引起很大的数据变动."

        with self.voiceover(text=step2) as tracker:
            self.play(FadeIn(macro))
            exp_graph = ax.plot(exp2, x_range=[10, 20], color=GREEN)
            self.play(Create(exp_graph))

        end_point2 = ax.c2p(20, exp2(20))
        report = Text("Deepseek 火了", color=RED).scale(0.5).move_to(end_point2).shift(UP*0.2)

        step3 = "最近的 deepseek 的模型发布, 也导致了价格发生了很大的变动.这些, 有很大的部分都是因为将因子代入到公式以后, 触发了买卖操作而导致."
        with self.voiceover(text=step3) as tracker:
            self.play(FadeIn(report))
            exp_graph = ax.plot(exp3, x_range=[20, 30], color=BLUE)
            self.play(Create(exp_graph))


    def construct(self):
        self.human_voice()

        people = ImageMobject(f"{IMAGE}/people-head-00.png").scale(0.7)
        stockmarket = ImageMobject(f"{IMAGE}/stock-market.png").scale(0.7)
        scene1 = "我们知道, 量化工程师无非是要选择买或者卖股票, 那么, 这个过程中,他们需要量化的是什么呢?"

        with self.voiceover(text=scene1) as tracker:
            self.play(FadeIn(people))
            self.play(people.animate.shift(LEFT*3))

            self.play(FadeIn(stockmarket))
            self.play(stockmarket.animate.shift(RIGHT*3))
            arrow_to_stock = Arrow(
                start=people.get_right(),
                end=stockmarket.get_left(),
                buff=0.5, color=BLACK
            )
            self.play(Write(arrow_to_stock))

        self.clear()
        self.curve()
        self.clear()
        self.portfolio_instance()
        self.clear()
        self.compute_alpha()
        self.clear()
        self.alpha_perf()
        self.clear()
        self.effect()
