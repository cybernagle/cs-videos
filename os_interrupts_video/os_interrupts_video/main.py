from manim import *
from script import Script
from animation import Animation
from video_controls import VideoControls
from keyboard_input_example import KeyboardInputExample
from animation import InterruptScene

class Main:
    def __init__(self):
        self.script = None
        self.animations = []
        self.video_controls = None
        self.keyboard_input_example = None

    def create_script(self, text: str, scenes: list):
        self.script = Script(text, scenes)

    def create_animation(self, scene: Scene, mobject: Mobject):
        animation = Animation(scene, mobject)
        self.animations.append(animation)

    def create_video_controls(self, play: bool, pause: bool, rewind: bool, fast_forward: bool):
        self.video_controls = VideoControls(play, pause, rewind, fast_forward)

    def create_keyboard_input_example(self, key: str, interrupt: bool):
        self.keyboard_input_example = KeyboardInputExample(key, interrupt)

    def compile_video(self):
        for animation in self.animations:
            animation.create_animation()
            animation.remove_animation()

        #self.video_controls.play_video("./media/videos/1080p60")

        self.keyboard_input_example.render()

if __name__ == "__main__":
    main = Main()
    main.create_script("Operating System Interrupts", [])
    main.create_animation(InterruptScene(), Text("Operating System Interrupts"))
    main.create_video_controls(True, False, False, False)
    main.create_keyboard_input_example("A", True)
    main.compile_video()
