from manim import *

class Mmap(Scene):

    memory = None
    linked = None
    square_mem = None
    page_table = None

    def set_table_value(self, table: Table, row: int, col: int, value: Text) -> Table:
        self.play(
            table.get_rows()[row][col].animate.become(value.move_to(table.get_rows()[row][col].get_center()))
        )

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

        # 这是我们的物理内存
        self.add(self.square_mem)
        self.wait()
        # 物理内存会被分为很多个页面,一般每个页面占去 4kb 的存储.
        self.play(
            self.square_mem.animate.arrange(RIGHT, buff = 0.5).to_edge(LEFT),
        )
        self.linked()
        # 页之间, 将通过链表串联起来
        self.add(self.linked)

        physical = VGroup(self.square_mem, self.linked)

        self.wait(0.5)
        self.play(physical.animate.shift(DOWN*3))

        # disk
        disk = self.create_square_mem(color=PURPLE)
        disk.arrange(RIGHT, buff = 0).to_edge(LEFT)
        # 这是我们的磁盘
        self.add(disk)
        self.wait(0.5)
        self.play(disk.animate.shift(UP*3))

        # on disk we put out applications
        # 假设在磁盘 1-5 的位置存放了我们的应用程序
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
        # 程序中会包含 elfheader 头信息,.text信息用来存放代码, 
        self.add(elfhdr_body,text_body)
        self.add(text,elfhdr)
        # 当然还有包含其他的段信息, 比如说 stack.
        self.wait(0.5)
        self.add(stack, stack_body)

        text_vma = Tex(r"$\texttt{0x4567} - \texttt{0xFFFF} $").scale(0.5).next_to(text_body, UP)
        stack_vma = Tex(r"$\texttt{0xFFFF} - \texttt{0x1000F} $").scale(0.5).next_to(stack_body, UP)

        # 除了 elfheader 的头部信息, 其他段都会有自己的虚拟地址.
        # 这里我们假设代码段的地址是从 4567 到 ffff
        self.wait(0.5)
        self.add(text_vma)
        self.wait(0.5)
        # stack 段的地址从 ffff 到 1000F
        self.add(stack_vma)

        # 这个时候, 我们的磁盘代码文件,  
        self.play(Indicate(disk[1:5]))
        # 与 text 空间
        self.play(Indicate(text_body))
        # 并于虚拟地址建立了映射
        self.play(Indicate(text_vma))

        # 有的时候, 文件不一定是必要的, 比如说我们的 stack 空间, 它仅仅映射到了 ffff 到 1000f 这个虚拟地址.
        self.play(Indicate(stack_body))
        self.play(Indicate(stack_vma))

        # 这些空间会共享同一个页表.
        self.page_table = Table(
            [["0", ""],
             ["1", ""],
             ["2", ""],
             ["3", ""],
             ["4", ""]],
            col_labels=[Text("VPN"), Text("PFN")],
            include_outer_lines=True
        ).set_column_colors(YELLOW).scale(0.3)
        self.page_table.next_to(stack_body, RIGHT).shift(RIGHT*0.2)

        self.play(FadeIn(self.page_table))

        # 从代码文件,到 text 空间,到 vma 的过程, 我们将其称之为 mmap.

        # 回到我们的程序结构当中.
        # elfheader 当中会存在两个信息: entry ,以及 type
        # type 用于标识我们文件的类型,因为我们是程序文件,所以就是可执行文件.
        # 另外一个就是 entry, 也就是我们文件的入口,在这里我们假设入口就是 4567
        # 要注意, elfhdr 当中不仅仅包含这些内容. 我们仅仅是为了演示方便.
        entry = Text("entry").scale(0.5).move_to(elfhdr_body[0])
        elftype = Text("type").scale(0.5).move_to(elfhdr_body[1])

        self.play(
            FadeIn(entry),
            FadeIn(elftype),
        )
        reg = Text("cs:ip").scale(0.5).move_to(text_body[0])

        # 接下来, 我们的cpu的 cs ip 寄存器就指向了该地址.
        self.play(FadeIn(reg))
        #并开始向后执行
        self.play(reg.animate.move_to(text_body[1]))

        # 假设 4567 的 4 是 VPN.
        # 这个时候它会发现,页表当中的第四个位置是空的.
        self.play(Indicate(
            self.page_table.get_cell((6,1))
        ))

        # 空的意味着什么呢?
        # 该代码没有被加载到内存当中.
        # 所以, 这个时候,我们就需要调用页中断来将代码加载到内存当中.
        self.play(disk[1].copy().animate.move_to(self.square_mem[2]))

        pfn = Text("2").scale(0.5).set_color(RED)

        pfn.move_to(self.page_table.get_cell((6,2)).get_center())
            
        # 然后, 我们再更新页表的内容.
        self.play(
            FadeIn(pfn)
        )

        # 这样, 当我们下一次尝试访问同样的代码地址时候.
        self.play(reg.animate.move_to(text_body[0]))

        #  我们会直接从页表当中获取物理物理页
        self.play(
            Indicate(pfn)
        )
        self.play(
            Indicate(self.square_mem[2])
        )

        # 而不需要从磁盘当中重新加载
        self.play(
            Indicate(disk[1])
        )

        self.wait()
