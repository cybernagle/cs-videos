from manim import *

# 4
class KernelProto(Scene):
    def construct(self):
        control = Text("控制").set_color(BLUE).shift(LEFT*5)
        calc = Text("运算").set_color(BLUE).next_to(control, RIGHT, buff=1)
        store = Text("存储").set_color(BLUE).next_to(calc, RIGHT, buff=1)
        in_put = Text("输入").set_color(BLUE).next_to(store, RIGHT, buff=1)
        output = Text("输出").set_color(BLUE).next_to(in_put, RIGHT, buff=1)

        self.play(
            FadeIn(control),
            FadeIn(calc),
            FadeIn(store),
            FadeIn(in_put),
            FadeIn(output)
        )

        cpu_arm = ImageMobject("./resources/cpu.png").scale(0.1).next_to(calc, DOWN).shift(LEFT*1.5)
        cpu_intel = ImageMobject("./resources/quadcore.png").scale(0.1).next_to(cpu_arm, RIGHT)
        self.play(
            FadeIn(cpu_arm),
            FadeIn(cpu_intel),
        )

        disk_ram = ImageMobject("./resources/ram.png").scale(0.1).next_to(store, DOWN).shift(LEFT*0.5)
        disk_disk = ImageMobject("./resources/floppy-disk.png").scale(0.1).next_to(disk_ram)
        disk_uflash = ImageMobject("./resources/pendrive.png").scale(0.1).next_to(disk_disk)

        self.play(
            FadeIn(disk_ram),
            FadeIn(disk_disk),
            FadeIn(disk_uflash),
        )

        input_keyboard = ImageMobject("./resources/keyboard.png").scale(0.1).next_to(in_put,DOWN).shift(LEFT*0.5)
        input_mouse = ImageMobject("./resources/mouse.png").scale(0.1).next_to(input_keyboard)
        input_microphone = ImageMobject("./resources/microphone.png").scale(0.1).next_to(input_mouse)
        self.play(
            FadeIn(input_keyboard),
            FadeIn(input_mouse),
            FadeIn(input_microphone),
        )

        output_monitor = ImageMobject("./resources/monitor.png").scale(0.1).next_to(output, DOWN).shift(LEFT*0.5)
        output_printer = ImageMobject("./resources/printer.png").scale(0.1).next_to(output_monitor)
        output_headset = ImageMobject("./resources/headset.png").scale(0.1).next_to(output_printer)

        self.play(
            FadeIn(output_monitor),
            FadeIn(output_printer),
            FadeIn(output_headset),
        )

        hardware = VGroup(
            control, calc, store, in_put, output,
        )

        self.play(
            hardware.animate.shift(DOWN*2),
            cpu_arm.animate.shift(DOWN*2),
            cpu_intel.animate.shift(DOWN*2),
            disk_ram.animate.shift(DOWN*2),
            disk_disk.animate.shift(DOWN*2),
            disk_uflash.animate.shift(DOWN*2),
            output_monitor.animate.shift(DOWN*2),
            output_printer.animate.shift(DOWN*2),
            output_headset.animate.shift(DOWN*2),

            input_keyboard.animate.shift(DOWN*2),
            input_mouse.animate.shift(DOWN*2),
            input_microphone.animate.shift(DOWN*2),
        )

        self.wait()

        text = [
            "- 可以运行我们的计算任务",
            "- 可以处理出错的情况",
            "- 可以多个任务一起运行",
            "- 可以和任务进行交流，看看运算进度",
            "- 我不希望了解所有的硬件，只想专注于解题"
        ]

        list_obj = VGroup(*[Text(item).scale(0.5) for item in text])

        list_obj.arrange(DOWN, aligned_edge=LEFT).shift(LEFT*2.4)

        self.play(Write(list_obj))

        start_point = LEFT*20
        end_point = RIGHT*20

        button_line = Line(start_point, end_point, color=ORANGE).next_to(store, UP)
        self.add(button_line)
        upper_line = Line(start_point, end_point, color=ORANGE).next_to(list_obj, UP)
        self.add(upper_line)

        posix = Text("POSIX", color=YELLOW).next_to(list_obj, UP*3).shift(LEFT*2.1)
        self.play(AddTextLetterByLetter(posix))

        posixs = Text(
            'WAIT, EXIT\nKILL\nOPEN, CLOSE, READ\nSOCKET, BIND, READ\nFORK, EXEC', color=BLUE
        ).scale(0.3).next_to(posix, RIGHT)
        self.play(AddTextLetterByLetter(posixs))

        kernel = ImageMobject("./resources/linux.png").scale(0.6).next_to(list_obj, RIGHT, buff=3)
        self.play(FadeIn(kernel))
        self.wait(1)
        self.play(Indicate(list_obj))


        self.wait()

