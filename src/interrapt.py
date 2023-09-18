from manim import *

class Keyboard(Scene):

    # keyboard
    keyboard = VGroup()
    keys = VGroup()
    key_value = VGroup()

    def keyboard(self):
        self.keys = VGroup(*[Rectangle(height=0.6, width=1).set_fill(WHITE, opacity=0.2) for i in range(10)]).arrange(RIGHT, buff=0.1)
        self.labels = VGroup(*[Text(char).scale(0.5).move_to(self.keys[i]) for i, char in enumerate("QWERTYUIOP")])
        self.keyboard = VGroup(self.keys, self.labels)

    def press(self, index):
        key_E = self.keys[index]
        label_E = self.labels[index]
        self.play(key_E.animate.set_fill(BLUE, opacity=0.5), label_E.animate.set_color(BLUE), run_time=0.1)
        self.play(key_E.animate.set_fill(WHITE, opacity=0.2), label_E.animate.set_color(BLACK), run_time=0.1)

    def construct(self):
        self.keyboard()
        self.add(self.keyboard)
        self.press(2)
        self.wait()
