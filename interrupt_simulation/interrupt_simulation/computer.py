## computer.py
from manim import *

class Computer(Scene):
    def __init__(self, interrupt_table: 'InterruptTable'):
        super().__init__()
        self.interrupt_table = interrupt_table
        self.is_running = False
        self.computer = Square(side_length=3).set_fill(WHITE, opacity=0.5)
        self.play(ShowCreation(self.computer))

    def run(self):
        self.is_running = True
        self.play(self.computer.animate.set_fill(GREEN, opacity=0.5))

    def interrupt_handler(self, interrupt: str):
        if self.is_running:
            self.play(self.computer.animate.set_fill(RED, opacity=0.5))
            self.interrupt_table.add_interrupt(interrupt)
            self.play(self.computer.animate.set_fill(GREEN, opacity=0.5))
            self.interrupt_table.remove_interrupt(interrupt)

    def construct(self):
        title = Text("Computer").scale(1.5)
        self.play(Write(title))
        self.wait(1)
