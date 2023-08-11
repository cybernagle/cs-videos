from manim import *

class Script:
    def __init__(self, text: str, scenes: list):
        self.text = text
        self.scenes = scenes

    def create_scene(self, scene: Scene):
        self.scenes.append(scene)

    def get_scenes(self):
        return self.scenes

    def get_text(self):
        return self.text

class InterruptScene(Scene):
    def construct(self):
        title = Text("Operating System Interrupts")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        description = Text("Interrupts are signals sent to the processor that an event needs immediate attention")
        self.play(Write(description))
        self.wait(2)
        self.play(FadeOut(description))

        keyboard_example = Text("When you press a key, the keyboard sends an interrupt signal to the processor")
        self.play(Write(keyboard_example))
        self.wait(2)
        self.play(FadeOut(keyboard_example))

        interrupt_handling = Text("The processor then interrupts what it's doing to handle the event")
        self.play(Write(interrupt_handling))
        self.wait(2)
        self.play(FadeOut(interrupt_handling))

        conclusion = Text("This is how operating system handles interrupts")
        self.play(Write(conclusion))
        self.wait(2)
        self.play(FadeOut(conclusion))

if __name__ == "__main__":
    script = Script("Operating System Interrupts", [])
    script.create_scene(InterruptScene())
