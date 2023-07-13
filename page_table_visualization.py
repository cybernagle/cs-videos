from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class MemoryVisualization(VoiceoverScene):
    def construct(self):
        # You can choose from a multitude of TTS services,
        # or in this example, record your own voice:
        self.set_speech_service(RecorderService())

        clang = Code("page_table_visualization.c", color=WHITE).shift(2*UP)
        asm  = Text("mov 0x1,-0x4(%rpb)")

        with self.voiceover(text="这是一小段C代码") as tracker:
            self.play(Create(clang))
            self.play(clang.animate.shift(DOWN*2))
            self.wait(2)

        with self.voiceover(text=" 其中第四行代码 a =1 在经过编译以后,我们可以得到这条指令") as tracker:
            self.play(
                ReplacementTransform(clang, asm), run_time=2
            )

        reg = asm[-5:-1].copy()
        heightlight = SurroundingRectangle(asm[-5:-1], RED, buff = .1)

        with self.voiceover(text=" 请注意看 rbp 这个寄存器, 它存储了 a 的虚拟地址") as tracker:
            self.play(Create(heightlight))

        address = Rectangle(color=RED, fill_opacity=0.5, width=2, height=0.5)

        with self.voiceover(text=" 这个虚拟地址指向了黄色的这块区域") as tracker:
            self.play(ReplacementTransform(asm, address), FadeOut(heightlight))

        main_mem = Rectangle(color=BLUE, fill_opacity=0.1, width=2, height=4, grid_xstep=2.0, grid_ystep=0.5).shift(DOWN*0.25)
        with self.voiceover(text=" 这是该区域在虚拟内存当中的位置.") as tracker:
            self.play(Create(main_mem))

        mem_group = VGroup(address, main_mem)
        self.play(mem_group.animate.shift(LEFT*4))

        rbp_addr = Tex(r"$rbp = \texttt{0x4567} \rightarrow$", font_size = 36).next_to(address, RIGHT, buff = 0.1)

        with self.voiceover(text=" 我们假设这块区域的地址是 0x4567.") as tracker:
            self.play(Create(rbp_addr))

        self.wait(1)
        binary = MathTable(
            [["0","1","0","0","0","1","0","1","0","1","1","0","0","1","1","1"]],
            include_outer_lines=True,
            v_buff=0.1,
            h_buff=0.1
        ).next_to(rbp_addr, RIGHT, buff = 0.1)


        binary.add_highlighted_cell((0,1), color=YELLOW)
        binary.add_highlighted_cell((0,2), color=YELLOW)
        binary.add_highlighted_cell((0,3), color=YELLOW)
        binary.add_highlighted_cell((0,4), color=YELLOW)

        # 为 binary 打上标签.
        vpn = Text("虚拟页号VPN", color=YELLOW , font_size=20)
        vpn.next_to(binary.get_cell((0,2)), DOWN, buff = 0.1)

        offset = Text("偏移量OffSet", color=WHITE, font_size=20)
        offset.next_to(binary.get_cell((0,11)), DOWN, buff=0.1)

        with self.voiceover(text=" 地址 4567 被转换成二进制后如图所示") as tracker:
            self.play(Create(binary))
        with self.voiceover(text=" 其中前四位也就是黄色区域是虚拟页号, 后面 12 位白色的是偏移量, 代表在一个页里面的位置.") as tracker:
            self.play(Create(vpn), Create(offset))
        # 把 binary 和 rbp 和内存都group 一下移动到屏幕上方.
        binary_group = VGroup(binary, vpn, offset)

        vm_group = VGroup(mem_group, rbp_addr, binary_group)
        self.play(vm_group.animate.shift(UP * 2))

        # 创建一个页表
        page_table = Table(
            [["0110", "1001"],
             ["0100", "0110"],
             ["0101", "0010"],
             ["0000", "1000"]],
            col_labels=[Text("VPN"), Text("PFN")],
            include_outer_lines=True
        ).set_column_colors(YELLOW).scale(0.3)


        with self.voiceover(text=" 这是我们的页表") as tracker:
            self.play(Create(page_table), Create(Text("页表", font_size=20).next_to(page_table,DOWN, buff=0.1)))
        with self.voiceover(text=" 根据虚拟地址里面的虚拟页号") as tracker:
            self.play(Indicate(vpn))
        with self.voiceover(text=" 我们找到在对应页表中的位置") as tracker:
            self.play(Indicate(page_table.get_cell((3,1))))
        with self.voiceover(text=" 然后, 我们就可以找到对应的物理页真") as tracker:
            self.play(Indicate(page_table.get_cell((3,2))))

        pfn = MathTable(
            [["0","1","1","0"]],
            include_outer_lines=True,
            v_buff=0.1,
            h_buff=0.1
        ).shift(DOWN*2).shift(RIGHT*0.5).set_row_colors(YELLOW)

        # moving from page table
        pfn_from_pt = page_table.get_cell((3,2)).copy()

        with self.voiceover(text=" 紧接着, 我们取出物理页真") as tracker:
            self.play(pfn_from_pt.animate.scale(2).move_to(DOWN*2))
            self.play(Transform(pfn_from_pt, pfn))


        # moving from binary
        offset_from_binary = binary.get_rows()[0][-12:]
        self.play(offset_from_binary.animate.move_to(DOWN*2+RIGHT*2.8))

        pfn_offset = MathTable(
            [["0","1","0","1","0","1","1","0","0","1","1","1"]],
            include_outer_lines=True,
            v_buff=0.1,
            h_buff=0.1
        )
        pfn_offset.next_to(pfn, RIGHT, buff=0)

        with self.voiceover(text=" 把物理页者和虚拟地址当中的偏移量组合起来, 我们就得到了相应的物理地址,这就是虚拟地址通过页表转换成物理地址的过程.") as tracker:
            self.play(offset_from_binary.animate.move_to(pfn_offset))
            self.play(Create(pfn_offset))
            self.remove(offset_from_binary)

            self.play(Create(Text("物理地址", font_size = 20).next_to(pfn_offset[8], DOWN, buff=0.1)))

        self.wait()
