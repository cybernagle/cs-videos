from manim import *

class Channel(Scene):

    def construct(self):

        control = Text("控制").set_color(ORANGE).scale(0.5).shift(LEFT*5)
        calc = Text("运算").set_color(BLUE).scale(0.5).next_to(control, RIGHT, buff=1.5)
        store = Text("存储").set_color(RED).scale(0.5).next_to(calc, RIGHT, buff=1.5)
        in_put = Text("输入").set_color(BLUE).scale(0.5).next_to(store, RIGHT, buff=1.5)
        output = Text("输出").set_color(ORANGE).scale(0.5).next_to(in_put, RIGHT, buff=1.5)

        cpu_arm = ImageMobject("./resources/cpu.png").scale(0.1).next_to(calc, DOWN).shift(LEFT*1.5)
        cpu_intel = ImageMobject("./resources/quadcore.png").scale(0.1).next_to(cpu_arm, RIGHT)

        disk_ram = ImageMobject("./resources/ram.png").scale(0.1).next_to(store, DOWN).shift(LEFT*0.5)
        disk_disk = ImageMobject("./resources/floppy-disk.png").scale(0.1).next_to(disk_ram)
        disk_uflash = ImageMobject("./resources/pendrive.png").scale(0.1).next_to(disk_disk)


        input_keyboard = ImageMobject("./resources/keyboard.png").scale(0.1).next_to(in_put,DOWN).shift(LEFT*0.5)
        input_mouse = ImageMobject("./resources/mouse.png").scale(0.1).next_to(input_keyboard)
        input_microphone = ImageMobject("./resources/microphone.png").scale(0.1).next_to(input_mouse)

        output_monitor = ImageMobject("./resources/monitor.png").scale(0.1).next_to(output, DOWN).shift(LEFT*0.5)
        output_printer = ImageMobject("./resources/printer.png").scale(0.1).next_to(output_monitor)
        output_headset = ImageMobject("./resources/headset.png").scale(0.1).next_to(output_printer)

        hardware = VGroup(
            control, calc, store, in_put, output,
        )

        self.add(
            hardware,
            cpu_arm,cpu_intel,
            disk_ram, disk_disk, disk_uflash,
            input_keyboard, input_mouse, input_microphone,
            output_monitor, output_printer, output_headset
        )
