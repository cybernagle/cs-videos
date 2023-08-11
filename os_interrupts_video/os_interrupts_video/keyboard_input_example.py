from manim import *

class KeyboardInputExample(Scene):
    def __init__(self, key: str, interrupt: bool):
        self.key = key
        self.interrupt = interrupt
        super().__init__()

    def construct(self):
        keyboard = Text("Keyboard")
        self.play(Write(keyboard))
        self.wait(2)

        key_text = Text(f"Key Pressed: {self.key}")
        self.play(Transform(keyboard, key_text))
        self.wait(2)

        if self.interrupt:
            interrupt_text = Text("Interrupt Signal Sent to Processor")
            self.play(Transform(keyboard, interrupt_text))
            self.wait(2)

        processor = Text("Processor")
        self.play(Transform(keyboard, processor))
        self.wait(2)

        handling_text = Text("Handling Interrupt")
        self.play(Transform(keyboard, handling_text))
        self.wait(2)

        done_text = Text("Done Handling Interrupt")
        self.play(Transform(keyboard, done_text))
        self.wait(2)

if __name__ == "__main__":
    scene = KeyboardInputExample("A", True)
    scene.render()
