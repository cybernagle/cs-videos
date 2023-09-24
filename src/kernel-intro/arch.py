from manim import *

class Arch(Scene):

    def title(self):
        simu = Text("内核的基本结构")
        self.play(AddTextLetterByLetter(simu))
        self.wait(0.5)
        self.play(FadeOut(simu))

    def construct(self):

        self.title()
        control = Text("控制").set_color(BLUE).shift(LEFT*5+DOWN*2.5)
        calc = Text("运算").set_color(BLUE).next_to(control, RIGHT, buff=1)
        store = Text("存储").set_color(BLUE).next_to(calc, RIGHT, buff=1)
        in_put = Text("输入").set_color(BLUE).next_to(store, RIGHT, buff=1)
        output = Text("输出").set_color(BLUE).next_to(in_put, RIGHT, buff=1)

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

        start_point = LEFT*20
        end_point = RIGHT*20

        button_line = Line(start_point, end_point, color=ORANGE).next_to(store, UP)
        self.add(button_line)

        driver_group = VGroup().next_to(control, UP)
        driver_text_group = VGroup()
        contents = ['主板驱动', '磁盘驱动', '键盘驱动', '显示器驱动', '网卡驱动']
        for i in range(len(contents)):
            r_color = RED
            height = 0.5
            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2.2, height=height,
                             grid_xstep=2.2, grid_ystep=height)
            rect.next_to(driver_group, RIGHT, buff=0.5)
            r_text = Text(contents[i]).scale(0.5).move_to(rect.get_center())
            driver_text_group.add(r_text)
            driver_group.add(rect)
        drivers = VGroup(driver_group, driver_text_group).next_to(store,UP*1.3).shift(RIGHT*0.3)
        self.add(drivers)

        for i in range(len(driver_group)):
            self.play(Indicate(driver_group[i]))

        # process 
        proc = Rectangle(color=RED_B, fill_opacity=0.5, width=1, height=1,
                         grid_xstep=1.0, grid_ystep=1).next_to(driver_group[0], UP*8, aligned_edge=LEFT)
        proc_t = Text("进").scale(0.5).move_to(proc)
        proc1 = proc.copy().next_to(proc, RIGHT)
        proc_t1 = Text("程").scale(0.5).move_to(proc1)
        proc2 = proc.copy().next_to(proc1, RIGHT, buff=5)
        proc_t2 = Text("管").scale(0.5).move_to(proc2)
        proc3 = proc.copy().next_to(proc2, RIGHT)
        proc_t3 = Text("理").scale(0.5).move_to(proc3)

        self.add(
            proc, proc1, proc2, proc3,
            proc_t, proc_t1, proc_t2, proc_t3
        )
        self.wait()

        # file management
        fm = Rectangle(color=RED_C, fill_opacity=0.5, width=2.2, height=1,
                         grid_xstep=2.0, grid_ystep=2).next_to(driver_group[1], UP*8)
        fm_text = Text("文件管理").scale(0.5).move_to(fm.get_center())
        self.play(FadeIn(fm), FadeIn(fm_text))
        self.wait()

        # network management
        network = Rectangle(color=RED_D, fill_opacity=0.5, width=2.2, height=1,
                         grid_xstep=2.0, grid_ystep=2).next_to(driver_group[4], UP*8)
        network_text = Text("网络协议栈").scale(0.5).move_to(network.get_center())
        self.play(FadeIn(network), FadeIn(network_text))

        self.wait()
        # memory management
        mm = Rectangle(color=RED_A, fill_opacity=0.5, width=4.9, height=1,
                         grid_xstep=4.9, grid_ystep=2).next_to(driver_group[0], UP, aligned_edge=LEFT)
        mm_text = Text("内存管理").scale(0.5).move_to(mm.get_center())

        self.play(FadeIn(mm), FadeIn(mm_text))

        self.wait()
        # interrupt management
        it = Rectangle(color=RED_A, fill_opacity=0.5, width=7.6, height=1,
                         grid_xstep=7.6, grid_ystep=2).next_to(driver_group[2], UP, aligned_edge=LEFT)
        it_text = Text("中断管理").scale(0.5).move_to(it.get_center())
        self.play(FadeIn(it), FadeIn(it_text))

        self.wait()
        upper_line = Line(start_point, end_point, color=ORANGE).next_to(proc2, UP)
        self.add(upper_line)
        posix = Text("POSIX", color=YELLOW).next_to(proc, UP*3, aligned_edge=LEFT)#.shift(LEFT*2.1)
        self.add(posix)

        posixs = Text(
            'WAIT, EXIT\nKILL\nOPEN, CLOSE, READ\nSOCKET, BIND, READ\nFORK, EXEC', color=BLUE
        ).scale(0.3).next_to(posix, RIGHT)
        self.add(posixs)

        self.wait()

        self.play(Indicate(store))
