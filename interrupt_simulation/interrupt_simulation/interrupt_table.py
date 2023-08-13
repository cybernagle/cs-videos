from manim import *

class InterruptTable(Scene):
    def __init__(self):
        super().__init__()
        self.table = {}

    def add_interrupt(self, interrupt: str):
        if interrupt not in self.table:
            self.table[interrupt] = Text(interrupt).scale(0.5)
            self.play(FadeIn(self.table[interrupt]))
        else:
            raise ValueError("Interrupt already exists in the table.")

    def remove_interrupt(self, interrupt: str):
        if interrupt in self.table:
            self.play(FadeOut(self.table[interrupt]))
            del self.table[interrupt]
        else:
            raise ValueError("Interrupt does not exist in the table.")

    def construct(self):
        title = Text("Interrupt Table").scale(1.5)
        self.play(Write(title))
        self.wait(1)
