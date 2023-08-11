import unittest
from script import Script
from animation import Animation
from video_controls import VideoControls
from keyboard_input_example import KeyboardInputExample
from manim import Scene, Text

class TestScript(unittest.TestCase):
    def test_create_scene(self):
        script = Script("Test Script", [])
        scene = Scene()
        script.create_scene(scene)
        self.assertIn(scene, script.get_scenes())

class TestAnimation(unittest.TestCase):
    def test_create_animation(self):
        scene = Scene()
        mobject = Text("Test Animation")
        animation = Animation(scene, mobject)
        animation.create_animation()
        self.assertEqual(animation.scene, scene)
        self.assertEqual(animation.mobject, mobject)

class TestVideoControls(unittest.TestCase):
    def test_play_video(self):
        controls = VideoControls(play=True)
        self.assertTrue(controls.play)

class TestKeyboardInputExample(unittest.TestCase):
    def test_construct(self):
        scene = KeyboardInputExample("A", True)
        self.assertEqual(scene.key, "A")
        self.assertTrue(scene.interrupt)

if __name__ == "__main__":
    unittest.main()
