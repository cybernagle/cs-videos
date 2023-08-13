## main.py
from manim import *

class Simulation(Scene):
    def construct(self):
        # Create interrupt table
        interrupt_table = InterruptTable()
        self.play(ShowCreation(interrupt_table))

        # Create computer with interrupt table
        computer = Computer(interrupt_table)
        self.play(ShowCreation(computer))

        # Run computer
        computer.run()

        # Add interrupts
        interrupts = ["Interrupt 1", "Interrupt 2", "Interrupt 3"]
        for interrupt in interrupts:
            computer.interrupt_handler(interrupt)

        # End simulation
        self.play(FadeOut(computer), FadeOut(interrupt_table))

if __name__ == "__main__":
    scene = Simulation()
    scene.render()
