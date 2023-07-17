        #mem_table = Table(
        #    [
        #        ["0x0FC8", "0"],
        #        ["0x0FD0", "0"],
        #        ["0x0FD8", "0"],
        #        ["0x0FE0", "0"],
        #        ["0x0FE8", "0"],
        #        ["0x0FF0", "0"],
        #        ["0x0FF8", "0"],
        #        ["0x1000", "0"]],
        #    include_outer_lines=True,
        #).scale(0.4).shift(RIGHT)

        #self.play(Create(mem_table))
        #ret_addr = asm_object.code[3][-10:].copy()
        #self.play(ret_addr.animate.move_to(mem_table.get_cell((8,2))))
