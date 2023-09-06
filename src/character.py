from manim import *

class Characters(Scene):
    face = None

    def create_face(self):
        face = Text(":-|").set_color(YELLOW).scale(2).rotate(1.5*PI)
        #surrand= SurroundingRectangle(face, color=WHITE,corner_radius=0.5)
        #surranded_face = VGroup(face, surrand)
        #surranded_face.scale(2).rotate(1.5*PI)
        self.face = face #surranded_face

    def construct(self):
        self.create_face()
        self.add(self.face)
        self.play(
            self.face.animate.become(Text(":-o").scale(2).rotate(1.5*PI).set_color(YELLOW)),
        )
        self.wait()
        self.play(
            self.face.animate.become(Text(":-)").scale(2).rotate(1.5*PI).set_color(YELLOW)),
        )
        self.wait()

        title = Text("muMu").next_to(self.face, DOWN, buff=0.3).set_color(GRAY)
        self.play(FadeIn(title))

        self.wait()
