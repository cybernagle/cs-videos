from manim import *

class OSLibrary(VGroup):

    def shift_code_indicator(self, index, source,target , size=1, run_time=1):
        if size <= 1:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index])),
                Indicate(target.code[index])
            )
        else:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index:index+size])),
                Indicate(target.code[index:index+size]),
                run_time=run_time
            )

    def shift_code_indicator(self, index, source,target , size=1):
        if size <= 1:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index])),
                Indicate(target.code[index])
            )
        else:
            self.play(
                source.animate.become(SurroundingRectangle(target.code[index:index+size])),
                Indicate(target.code[index:index+size])
            )

    def create_gdt(self):
        table = Table(
            [["0", "kernel code 0x0"], 
             ["1", "kernel data"], 
             ["2", "user code 0x123"], 
             ["3", "user data"]],
            include_outer_lines=True,
            h_buff=1.5,
            v_buff=0.7,
            line_config={"stroke_color": WHITE, "stroke_width": 1},
            background_stroke_color=WHITE
        )
        return table

    def create_cs(self):
        keys = VGroup(*[Rectangle(height=0.5, width=0.5).set_fill(WHITE, opacity=0.2) for i in range(4)]).arrange(RIGHT, buff=0)
        labels = VGroup(*[Text(char).scale(0.5).move_to(keys[i]) for i, char in enumerate("1011")])
        self.cs = VGroup(keys, labels)

    def generate_cycle(self, inner_radius=1, outer_radius=1.5,color=GREEN):
        cycle = VGroup()
        for i in range(8):
            a = AnnularSector(inner_radius=inner_radius, outer_radius=outer_radius, angle=44.5 * DEGREES,start_angle=i*45*DEGREES ,color=color)
            cycle.add(a)
        return cycle

    def generate_tree(self):
        vertices = [ 1,2,3,4,5,6,7]
        edges = [
            (1,2), (1,3),(2,4), (2,5), (3, 6),(3,7)
        ]
        layout = {
            1: [0, 0, 0],
            2: [1, -1, 0],
            3: [-1, -1, 0],
            4: [2, -2, 0],
            5: [0.5, -2, 0],
            6: [-2, -2, 0],
            7: [-0.5, -2, 0],
        }

        tree = Graph(vertices, edges,labels=True, label_fill_color=GREEN,layout_scale=2,
                     layout=layout)#.set_color(YELLOW)
        return tree

    def generate_disk(self):
        disks = VGroup()
        prev_disk = AnnularSector(inner_radius=0.1, outer_radius=1.14, angle= 2*PI , color=GREEN)

        disks.add(prev_disk)

        disk = VGroup()
        init = 0.1
        for i in range(5):
            inner = init
            outer = init+0.2
            s = self.generate_cycle(inner_radius=inner, outer_radius=outer,color=GREEN)
            disk.add(s)
            s.move_to(disk)
            init+=0.21
        disks.add(disk)

        return disks

    def create_memory(self) -> VGroup:
        mem = VGroup()
        addresses = VGroup()
        start_addr = 0x0
        for i in range(30):
            rect = Rectangle(color=BLUE, fill_opacity=0.5, width=0.4, height=1,
                             grid_xstep=0.5, grid_ystep=1)
            addr = Text(hex(start_addr), font_size = 15)
            rect.next_to(mem, RIGHT, buff=0)
            mem.add(rect)

        self.memory = mem

    def create_slabs(self):
        # 创建三个方块
        square1 = Square(side_length=1.3, fill_opacity=0.6, color=BLUE)
        square2 = Square(side_length=2, fill_opacity=0.6, color=BLUE)
        square3 = Square(side_length=4, fill_opacity=0.6, color=BLUE)

        # 设置方块位置
        distance = 4
        square1.next_to(square2, LEFT*distance)
        square3.next_to(square2, RIGHT*distance)

        # 创建四个长方形
        rectangles1 = VGroup(*[Rectangle(height=0.2, width=1, fill_opacity=0.5, color=RED) for _ in range(4)])
        rectangles2 = VGroup(*[Rectangle(height=0.2, width=1.8, fill_opacity=0.5, color=PURPLE) for _ in range(6)])
        rectangles3 = VGroup(*[Rectangle(height=0.2, width=3.8, fill_opacity=0.5, color=ORANGE) for _ in range(13)])

        # 设置长方形位置
        rectangles1.arrange(direction=UP,buff=0.1)
        rectangles1.move_to(square1)
        rectangles2.arrange(direction=UP,buff=0.1)
        rectangles2.move_to(square2)
        rectangles3.arrange(direction=UP,buff=0.1)
        rectangles3.move_to(square3)

        # 将方块和长方形添加到场景中
        self.slabs = VGroup(
            square1, square2, square3,
            rectangles1, rectangles2, rectangles3
        )


    # memory related operation
    def create_memory(
            self,
            length=30, color=YELLOW, width=1.5, height=0.5, x_grid = 1.5, y_grid = 0.5,
            addr=False, addr_start=0x0, addr_step=0x10
    ) -> VGroup:
        mem = VGroup()

        addresses = VGroup()
        start_addr = addr

        width = width
        height = height

        for i in range(length):
            buff = 0
            rect = Rectangle(color=color, fill_opacity=0.5, width=width, height=height,
                             grid_xstep=x_grid, grid_ystep=y_grid)

            if addr:
                address = Text(hex(start_addr), font_size = 10.5).next_to(rect, DOWN, buff=0.1)
                start_addr += addr_step
                addresses.add(address)
            rect.next_to(mem, RIGHT, buff=buff)
            mem.add(rect)
        mem.add(addresses)
        mem.move_to(ORIGIN)
        return mem

    def create_mem_unit(
            self, height=9, width=4,unit_length=0.5, fill_opacity=0.2,
            color=BLUE
    ) -> VGroup():
        squares = VGroup(*[
            Square(color=color,side_length=unit_length, fill_opacity=fill_opacity).shift(i*0.5*DOWN + j*0.5*RIGHT).shift(UP*1.5+LEFT*0.8)
            for i in range(height)
            for j in range(width)
        ])
        squares.move_to(ORIGIN)
        return squares

    # page related & data structures
    def linked(self, func):
        def wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            arrows = VGroup(*[
                DoubleArrow(
                    square.get_center() + 0.05*RIGHT,
                    square.get_center() + 0.95*RIGHT,
                    stroke_width=0.5,
                )
                for square in results
            ])
            results.add(arrows)
        return wrapper

    def init_pages(self) -> VGroup:
        tables = VGroup(*[
            Table(
                [["0"],
                 ["0"],
                 ["pre-next"]],
                row_labels=[Text("flag"), Text("property"), Text("page_link")],
                include_outer_lines=True,
                background_rectangle_color=BLUE,
                arrange_in_grid_config={"cell_alignment": RIGHT})
                for _ in range(12)
        ])
        self.pages = tables

    def set_table_value(self, table: Table, row: int, col: int, value: Text) -> Table:
        self.play(
            table.get_rows()[row][col].animate.become(value.move_to(table.get_rows()[row][col].get_center()))
        )

    # malloc related
    def create_prev_free_bit(self):
        bit = Square(
            side_length=0.5,
            fill_opacity=0.5,
            color=RED_E,
            stroke_color=RED_E,
            background_stroke_color=RED_E
        )
        text = Text("P", color=WHITE).scale(0.5).move_to(bit)
        prev_free_bit = VGroup(text,bit)
        self.previous_free_bit = prev_free_bit 

    def create_allocate_chunk(self) -> VGroup:
        chunk_group = VGroup()
        text_group = VGroup()
        text = ['size',"presize", "F", "B", "data"]
        for i in range(5):
            r_color = BLUE
            height = 0.5

            # yellow area is chunk header
            if i <= 1:
                r_color = YELLOW

            # data block should much bigger
            if i == 4:
                height = 2.5

            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)

        chunk = VGroup(chunk_group, text_group)
        self.allocated_chunk = chunk

    def create_fake_chunk(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ['size', 'presize', 'F', 'B', 'data']
        for i in range(5):
            r_color = BLUE
            height = 0.5

            # yellow area is chunk header
            if i <= 1:
                r_color = RED
            if i == 4:
                height = 1.5

            rect = Rectangle(color=r_color, fill_opacity=1, width=2, height=height,stroke_color=RED_E,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.fake_chunk = VGroup(chunk_group, text_group)

    def create_fake_chunk_obj(self) -> VGroup:
        chunk_group = VGroup()
        text_group = VGroup()
        text = ['size', 'presize', 'F', 'B', 'data']
        for i in range(5):
            r_color = BLUE
            height = 0.5

            # yellow area is chunk header
            if i <= 1:
                r_color = RED

            rect = Rectangle(color=r_color, fill_opacity=1, width=2, height=height,stroke_color=RED_E,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        return VGroup(chunk_group, text_group)

    # stack related tasks
    def create_stack(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ["", "" ,"" ,'chunk0_addr', 'chunk1_addr', '', '']
        for i in range(len(text)):
            r_color = GREEN
            height = 0.5
            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.stack = VGroup(chunk_group, text_group)

    def create_stack(self):
        chunk_group = VGroup()
        text_group = VGroup()
        text = ["", "" ,"" ,'', '', '', '', "",""]
        for i in range(len(text)):
            r_color = RED
            height = 0.5
            rect = Rectangle(color=r_color, fill_opacity=0.5, width=2, height=height,
                             grid_xstep=2.0, grid_ystep=height)
            rect.next_to(chunk_group, DOWN, buff=0)
            r_text = Text(text[i]).scale(0.5).move_to(rect.get_center())
            text_group.add(r_text)
            chunk_group.add(rect)
        self.stack = VGroup(chunk_group, text_group)
