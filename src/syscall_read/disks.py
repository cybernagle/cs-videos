
        superblock_tt = Rectangle(width=0.5, height=1.5, grid_ystep=0.75, grid_xstep=0.5, color=OBJ_C, fill_opacity=0.3).next_to(disk, LEFT*8)
        sb_text = Text("superblock", color=OBJ_C).scale(0.3).next_to(superblock_t, DOWN)
        dgroup.add(superblock_tt, sb_text)

        block_tt = Rectangle(height=1.5, width=3, grid_ystep=0.5, grid_xstep=0.5, color=OBJ_C).shift(LEFT*1.5)
        block_text = Text("blocks", color=OBJ_C).scale(0.3).next_to(block_tt, DOWN)
        dgroup.add(block_tt, block_text)

        ablock = Rectangle(height=0.5, width=0.5, color=OBJ_C, fill_opacity=0.8).move_to(block_tt).align_to(block_tt, UL)
        ablock_text = Text("block", color=OBJ_C).scale(0.2).next_to(ablock, DOWN, buff=0.1)
        dgroup.add(ablock, ablock_text)

        ainode = Rectangle(height=1, width=0.5, color=OBJ_B, fill_opacity=0.8).next_to(ablock, RIGHT, buff=0).align_to(ablock,UP)
        ainode_text = Text("inode", color=OBJ_B).scale(0.2).next_to(ainode, DOWN, buff=0.1)
        dgroup.add(ainode, ainode_text)

        block_count = Text("block\ncount", color=OBJ_C).scale(0.2).move_to(superblock_tt).shift(UP*0.3)
        inode_count = Text("inode\ncount", color=OBJ_B).scale(0.2).move_to(superblock_tt).shift(DOWN*0.3)
        dgroup.add(block_count, inode_count)
        dgroup.add(inode_count)

        
        self.wait()
