from manim import *

class PageFault(Scene):

    memory = None
    linked = None
    square_mem = None

    def create_memory(self, length=30, color=YELLOW) -> VGroup:
        mem = VGroup()
        width = 1.5
        height = 0.5
        for i in range(length):
            buff = 0

            rect = Rectangle(color=color, fill_opacity=0.5, width=width, height=height,
                             grid_xstep=width, grid_ystep=height)
            rect.next_to(mem, RIGHT, buff=buff)
            mem.add(rect)
        return mem
        #self.memory = mem

    def create_square_mem(self, color=BLUE) -> VGroup():
        squares = VGroup(*[
            Square(color=color,side_length=0.5, fill_opacity=0.2).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(9)
            for j in range(4)
        ])
        return squares

    def linked(self) -> VGroup:
        arrows = VGroup(*[
            DoubleArrow(
                square.get_center() + 0.05*RIGHT,
                square.get_center() + 0.95*RIGHT,
                stroke_width=0.5,
            )
            for square in self.square_mem
        ])

        self.linked = arrows

    def construct(self):
        self.square_mem = self.create_square_mem()
        self.square_mem.arrange(RIGHT, buff = 0.5).to_edge(LEFT),
        self.linked()
        self.add(self.square_mem)
        self.add(self.linked)
        physical = VGroup(self.square_mem, self.linked)

        self.wait(0.5)
        self.play(physical.animate.shift(DOWN*3))

        # disk
        disk = self.create_square_mem(color=PURPLE)
        disk.arrange(RIGHT, buff = 0).to_edge(LEFT)
        self.add(disk)
        self.wait(0.5)
        self.play(disk.animate.shift(UP*3))

        # on disk we put out applications
        self.play(
            disk[1:5].animate.set_fill(opacity=0.8)
        )

        self.wait()
        elfhdr_body = self.create_memory(length=2, color=GREEN)
        text_body = self.create_memory(length=3, color=YELLOW)
        stack_body  = self.create_memory(length=1, color=RED)
        elfhdr_body.shift(LEFT*5.5)
        text_body.next_to(elfhdr_body,RIGHT, buff=0.1)
        stack_body.next_to(text_body,RIGHT, buff=0.1)

        elfhdr = Text("elfheader").scale(0.5).next_to(elfhdr_body[0], DOWN)
        text = Text(".text").scale(0.5).next_to(text_body[0], DOWN)
        stack = Text("stack").scale(0.5).next_to(stack_body[0], DOWN)
        self.add(elfhdr_body,text_body, stack_body)
        
        self.add(text,elfhdr, stack)

        # 需要注意, elfhdr 当中不仅仅包含这些内容. 我们仅仅是为了演示方便.
        entry = Text("entry").scale(0.5).move_to(elfhdr_body[0])
        elftype = Text("type").scale(0.5).move_to(elfhdr_body[1])

        self.add(entry, elftype)

        text_vma = Tex(r"$\texttt{0x4567} - \texttt{0xFFFF} $").scale(0.5).next_to(text_body, UP)
        stack_vma = Tex(r"$\texttt{0xFFFF} - \texttt{0x1000F} $").scale(0.5).next_to(stack_body, UP)

        self.add(text_vma, stack_vma)

        # 将磁盘文件, 与进程的 text 空间, 并虚拟地址建立映射关系的, 被称之为位 mmap.(这个时候切一个单独的画面, 只展示 mmap 这个 page)
        # 这个时候, 我们的磁盘代码文件, 与 text 空间, 并于虚拟地址建立了映射.
        self.play(Indicate(disk[2:5]))
        self.play(Indicate(text_body))
        self.play(Indicate(text_vma))

        # 而文件不一定是必要的, 比如说我们的 stack, 并没有用到任何的磁盘文件, 但是它也映射到了 ffff - 1000f 这个虚拟空间.
        # 有的时候, 文件不一定是必要的, 比如说我们的 stack 空间, 它仅仅映射到了 ffff 到 1000f 这个虚拟地址.
        self.play(Indicate(stack_body))
        self.play(Indicate(stack_vma))


        self.wait()
