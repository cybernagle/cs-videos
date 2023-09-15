from manim import *

class Characters(Scene):
    face = None

    def create_face(self):
        face = Text(":-|").set_color(YELLOW).scale(2).rotate(1.5*PI)
        face[2].shift(LEFT*0.13+DOWN*0.1)
        #surrand= SurroundingRectangle(face, color=WHITE,corner_radius=0.5)
        #surranded_face = VGroup(face, surrand)
        #surranded_face.scale(2).rotate(1.5*PI)
        self.face = face #surranded_face

    def construct(self):
        self.create_face()
        self.add(self.face)
        o = Text(":-0").scale(2).rotate(1.5*PI).set_color(YELLOW).shift(DOWN*0.05)
        o[0].move_to(self.face[0])
        o[1].move_to(self.face[1])
        o[2].shift(LEFT*0.13+DOWN*0.3)
        self.wait()
        self.play(
            self.face.animate.become(o),
        )
        self.wait()
        smile = Text(";-)").scale(2).rotate(1.5*PI).set_color(YELLOW)
        smile[0].shift(LEFT*0.13)
        smile[1].move_to(self.face[1])
        smile[2].shift(LEFT*0.14+DOWN*0.1)

        self.play(
            self.face.animate.become(smile),
        )
        self.wait()

        title = Text("muMu").next_to(self.face, DOWN, buff=0.3).set_color(GRAY)
        self.play(FadeIn(title))

        self.wait()
