from manim import *

class ComputerScene(Scene):
    # keyboard
    keyboard = VGroup()
    keys = VGroup()
    key_value = VGroup()

    def keyboard(self):
        self.keys = VGroup(*[Rectangle(height=0.6, width=1).set_fill(WHITE, opacity=0.2) for i in range(10)]).arrange(RIGHT, buff=0.1)
        self.labels = VGroup(*[Text(char).scale(0.5).move_to(self.keys[i]) for i, char in enumerate("QWERTYUIOP")])
        self.keyboard = VGroup(self.keys, self.labels)

    def press(self, index):
        key = self.keys[index]
        label = self.labels[index]
        self.play(key.animate.set_fill(BLUE, opacity=0.5), label.animate.set_color(BLUE), run_time=0.1)
        self.play(key.animate.set_fill(WHITE, opacity=0.2), label.animate.set_color(BLACK), run_time=0.1)

    def construct(self):

        # 这是一个键盘,就在我们按下E键的时候,他就把 E 打包好,让它的小朋友送到系统酱哪里去.
        # 他的小朋友我们把它叫做信号酱.
        # 信号酱不是一个单纯的工具人, 它也有着自己的个性. 这些个性, 都被标注在这样一个结构里面.
        # 首先要负责的就是, 把身份给到系统酱, 系统酱会根据这个身份信息了解到,哦, 这是键盘的娃娃
        # 它们比较敏感, 优先处理!
        # 于是,系统酱就把信号酱给到了它的中断处理部门. 中断处理部门看到信号,然后拿出来一张表格
        # 说, 啊,键盘的小朋友哇.
        # 知道了, 你先把你的准备的东西拿出来吧
        # 键盘拿出来几个容器,用来保存它打断其他人执行任务的一些必要信息.
        # 比如说, 被打断的人执行到哪一步啦.
        # 被打断的人需要用的一些表单哪.等等诸如此类.
        # 最后, 中断处理部门的人就开始安排信号酱要求的任务: 把 E 输出到屏幕上.
        self.keyboard()
        self.play(Create(self.keyboard))
        self.press(2)

        self.wait()
        #computer = Square(side_length=5, fill_opacity=0.5, color=BLUE)

        #io_interface = Square(side_length=1, fill_opacity=0.5, color=YELLOW)
        #io_interface.align_to(computer.get_corner(UP+LEFT), UP+LEFT) 

        #interrupt_vector = Table(
        #    [
        #        ["0", "Time Interrput"],
        #        ["1", "Keyboard"],
        #        ["12", "Mouse"],
        #        ["...", "..."]
        #    ],
        #    include_outer_lines=True)

        #interrupt_vector.scale(0.5)
        #interrupt_vector.move_to(computer.get_center())

        #arrow_io_to_int = Arrow(io_interface.get_corner(DOWN+RIGHT), 
        #                        interrupt_vector.get_cell((1, 0)).get_corner(UP+LEFT))

        #arrow_int_to_handler = Arrow(interrupt_vector.get_cell((1, 0)).get_corner(RIGHT),
        #                             interrupt_vector.get_cell((1, 1)).get_corner(LEFT))

        #self.add(computer, io_interface, interrupt_vector,
        #         arrow_io_to_int, arrow_int_to_handler)
