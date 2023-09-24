from manim import *

# 3
class SimpleKernel(Scene):

    def title(self):
        simu = Text("没有内核的计算机")
        self.play(AddTextLetterByLetter(simu))
        self.wait(0.5)
        self.play(FadeOut(simu))

    def information(self):
        text = Text("01010101101")
        self.add(text)
        self.wait(1)
        cpu = ImageMobject("./resources/cpu.png").scale(0.3)
        self.play(text.animate.next_to(cpu, LEFT))
        self.add(cpu)

        after_text = Text("11111101100")

        after_text.next_to(cpu, RIGHT)
        self.play(AddTextLetterByLetter(after_text))

        cpu.save_state()
        start_point = text[0].get_top()
        end_point = text[-1].get_top()
        arrow = CurvedArrow(end_point, start_point)
        self.play(cpu.animate.move_to(end_point))
        self.play(MoveAlongPath(cpu, arrow), Create(arrow))
        self.play(Restore(cpu))

        control = VGroup(text, arrow)

        self.play(
            arrow.animate.set_color(RED),
        )
        self.play(
            cpu.animate.shift(UP),
            FadeOut(after_text),
            control.animate.shift(UP)
        )

        self.play(
            control.animate.next_to(cpu, UP),
        )

        disk = ImageMobject("./resources/floppy-disk.png").scale(0.3).next_to(cpu, DOWN)
        keyboard = ImageMobject("./resources/keyboard.png").scale(0.3).next_to(disk, DOWN)
        monitor = ImageMobject("./resources/monitor.png").scale(0.3).next_to(keyboard, DOWN)

        control_text = Text("控制").set_color(BLUE).next_to(control, LEFT).shift(DOWN*0.3)
        calc_text = Text("运算").set_color(BLUE).next_to(control_text, DOWN, buff=0.7)
        store_text = Text("存储").set_color(BLUE).next_to(calc_text, DOWN, buff=0.7)
        input_text = Text("输入").set_color(BLUE).next_to(store_text, DOWN, buff=0.7)
        output_text = Text("输出").set_color(BLUE).next_to(input_text, DOWN, buff=0.7)

        self.add(disk)
        self.add(keyboard)
        self.add(monitor)

        self.play(
            FadeIn(control_text),
            FadeIn(calc_text),
            FadeIn(store_text),
            FadeIn(input_text),
            FadeIn(output_text),
        )

        self.wait()

    def construct(self):
        #self.title()
        self.wait(1)
        self.information()

