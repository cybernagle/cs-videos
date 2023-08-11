from manim import *

class Animation:
    def __init__(self, scene: Scene, mobject: Mobject):
        self.scene = scene
        self.mobject = mobject

    def create_animation(self):
        self.scene.play(Write(self.mobject))

    def remove_animation(self):
        self.scene.play(FadeOut(self.mobject))

class InterruptScene(Scene):
    def construct(self):
        title = Text("Operating System Interrupts")
        animation = Animation(self, title)
        animation.create_animation()
        self.wait(2)
        animation.remove_animation()

        description = Text("Interrupts are signals sent to the processor that an event needs immediate attention")
        animation = Animation(self, description)
        animation.create_animation()
        self.wait(2)
        animation.remove_animation()

        keyboard_example = Text("When you press a key, the keyboard sends an interrupt signal to the processor")
        animation = Animation(self, keyboard_example)
        animation.create_animation()
        self.wait(2)
        animation.remove_animation()

        interrupt_handling = Text("The processor then interrupts what it's doing to handle the event")
        animation = Animation(self, interrupt_handling)
        animation.create_animation()
        self.wait(2)
        animation.remove_animation()

        conclusion = Text("This is how operating system handles interrupts")
        animation = Animation(self, conclusion)
        animation.create_animation()
        self.wait(2)
        animation.remove_animation()

if __name__ == "__main__":
    scene = InterruptScene()
    scene.render()
