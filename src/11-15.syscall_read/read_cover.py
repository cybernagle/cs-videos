from manim import *

BACKGROUND="#2B3A42"

WORD_A="#00CED1"
WORD_B="#FFD700"
OBJ_A="#3EB489"
OBJ_B="#FFC0CB"
OBJ_C="#FFA500"

class ReadCover(Scene):

    def generate_cycle(self, inner_radius=1, outer_radius=1.5,color=OBJ_A):
        cycle = VGroup()
        for i in range(8):
            a = AnnularSector(inner_radius=inner_radius, outer_radius=outer_radius, angle=44.5 * DEGREES,start_angle=i*45*DEGREES ,color=color)
            cycle.add(a)
        return cycle

    def generate_disk(self):
        disks = VGroup()
        prev_disk = AnnularSector(inner_radius=0.1, outer_radius=1.14, angle= 2*PI , color=OBJ_A)

        disks.add(prev_disk)

        disk = VGroup()
        init = 0.1
        for i in range(5):
            inner = init
            outer = init+0.2
            s = self.generate_cycle(inner_radius=inner, outer_radius=outer,color=OBJ_A)
            disk.add(s)
            s.move_to(disk)
            init+=0.21
        disks.add(disk)

        return disks

    def construct(self):
        self.camera.background_color = BACKGROUND
        disk = self.generate_disk()
        self.add(disk[1].shift(RIGHT*3+DOWN))
        dgroup = VGroup()

        superblock_tt = Rectangle(width=0.5, height=1.5, grid_ystep=0.75, grid_xstep=0.5, color=OBJ_C, fill_opacity=0.3).next_to(disk[1], LEFT*22)
        sb_text = Text("superblock", color=OBJ_C).scale(0.3).next_to(superblock_tt, DOWN)

        dgroup.add(superblock_tt, sb_text)

        block_tt = Rectangle(height=1.5, width=3, grid_ystep=0.5, grid_xstep=0.5, color=OBJ_C).shift(LEFT*2+DOWN)
        block_text = Text("blocks", color=OBJ_C).scale(0.3).next_to(block_tt, DOWN)
        dgroup.add(block_tt, block_text)


        self.add(dgroup)
        word = Tex("SYSTEM\_CALL: ", color=WORD_A).scale(1.8).shift(UP*1+LEFT*1.3)
        read = Tex("READ", color=WORD_B).scale(1.8).next_to(word, RIGHT, buff=0.3)
        self.add(word, read)
        #self.add(Text("READ", color=WORD_A).scale(2).shift(DOWN*2))
