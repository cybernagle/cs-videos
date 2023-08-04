from manim import *

class Characters(Scene):
    face = None

    def create_face(self):
        face = Text(":-)")
        surrand= SurroundingRectangle(face, color=WHITE)
        surranded_face = VGroup(face, surrand)
        surranded_face.scale(2)#.rotate(1.5*PI)
        self.face = surranded_face

    def construct(self):
        self.create_face()
        self.play(Create(self.face))
        #self.play(
        self.face[0].become(Text(":-(").scale(2))#.rotate(1.5*PI))

        #)
        self.wait()
