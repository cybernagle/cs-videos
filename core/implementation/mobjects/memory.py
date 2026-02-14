"""
Memory visualization mobjects.

Components for displaying memory, memory cells, and page tables.
"""
try:
    from manim import *
    from manim import VGroup, Rectangle, Square, Text, Table, AnnularSector
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    VGroup = object
    Rectangle = object
    Square = object
    Text = object
    Table = object
    AnnularSector = object

from typing import Optional, List, Dict, Any


class MemoryCell(VGroup if MANIM_AVAILABLE else object):
    """
    A single memory cell with address and value.

    Attributes:
        address: Memory address (displayed as hex)
        value: Cell value
        width: Cell width
        height: Cell height
        show_address: Whether to display address
        highlighted: Whether cell is highlighted
    """

    def __init__(
        self,
        address: int = 0,
        value: Any = 0,
        width: float = 0.8,
        height: float = 0.6,
        show_address: bool = True,
        highlighted: bool = False,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.address = address
        self.value = value
        self.width = width
        self.height = height
        self.show_address = show_address
        self.highlighted = highlighted

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the memory cell mobject."""
        from ..themes import get_theme

        theme = get_theme()

        # Cell rectangle
        cell = Rectangle(
            width=self.width,
            height=self.height,
            fill_color=theme.colors.HIGHLIGHT if self.highlighted else theme.colors.MEMORY_CELL,
            fill_opacity=0.6 if self.highlighted else 0.3,
            stroke_color=theme.colors.WHITE,
            stroke_width=1
        )
        self.add(cell)

        # Value text
        value_str = str(self.value)
        value_text = Text(
            value_str,
            font_size=20,
            color=theme.colors.WHITE
        ).move_to(cell.get_center())
        self.add(value_text)

        # Address label
        if self.show_address:
            addr_text = Text(
                hex(self.address),
                font_size=12,
                color=theme.colors.GRAY
            ).next_to(cell, DOWN, buff=0.1)
            self.add(addr_text)

    def set_value(self, new_value: Any):
        """Update the cell value."""
        self.value = new_value
        # Would update the text mobject

    def set_highlight(self, highlighted: bool):
        """Set highlight state."""
        self.highlighted = highlighted
        # Would update the fill color


class MemoryViz(VGroup if MANIM_AVAILABLE else object):
    """
    Memory visualization with multiple cells arranged in rows.

    This is the main memory display component, migrated from
    lib/manim-os.py create_memory().

    Attributes:
        cells: Number of memory cells
        rows: Number of rows to arrange cells in
        values: Optional initial values for cells
        highlight_cells: List of cell indices to highlight
        show_addresses: Whether to show addresses
        cell_width: Width of each cell
        cell_height: Height of each cell
    """

    def __init__(
        self,
        cells: int = 16,
        rows: int = 1,
        values: Optional[List[Any]] = None,
        highlight_cells: Optional[List[int]] = None,
        show_addresses: bool = True,
        cell_width: float = 0.8,
        cell_height: float = 0.6,
        start_address: int = 0x0,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.cells = cells
        self.rows = rows
        self.values = values or [0] * cells
        self.highlight_cells = highlight_cells or []
        self.show_addresses = show_addresses
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.start_address = start_address

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the memory visualization."""
        cells_per_row = self.cells // self.rows

        for i in range(self.cells):
            row = i // cells_per_row
            col = i % cells_per_row

            address = self.start_address + i * 4  # 4 bytes per cell
            value = self.values[i] if i < len(self.values) else 0
            is_highlighted = i in self.highlight_cells

            cell = MemoryCell(
                address=address,
                value=value,
                width=self.cell_width,
                height=self.cell_height,
                show_address=self.show_addresses and col == 0,
                highlighted=is_highlighted
            )

            # Position cell
            x = (col - cells_per_row / 2) * (self.cell_width + 0.1)
            y = -(row - self.rows / 2) * (self.cell_height + 0.1)
            cell.move_to([x, y, 0])

            self.add(cell)

    def update_cell(self, index: int, new_value: Any):
        """Update a specific cell's value."""
        if 0 <= index < len(self.submobjects):
            # Would update the specific cell mobject
            pass

    def highlight_cell(self, index: int, highlight: bool = True):
        """Highlight or unhighlight a specific cell."""
        if 0 <= index < len(self.submobjects):
            # Would update the cell's highlight state
            pass


class PageTableViz(VGroup if MANIM_AVAILABLE else object):
    """
    Page table visualization.

    Shows page table entries with flags and mappings.

    Attributes:
        num_entries: Number of page table entries
        entries: List of page table entry data
    """

    def __init__(
        self,
        num_entries: int = 8,
        entries: Optional[List[Dict]] = None,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.num_entries = num_entries
        self.entries = entries or [{}] * num_entries

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the page table visualization."""
        from ..themes import get_theme

        theme = get_theme()

        # Create table
        table_data = []
        for i in range(self.num_entries):
            entry = self.entries[i] if i < len(self.entries) else {}
            page_num = entry.get('page_number', i)
            frame_num = entry.get('frame_number', 0)
            present = entry.get('present', False)
            dirty = entry.get('dirty', False)

            flags = []
            if present:
                flags.append('P')
            if dirty:
                flags.append('D')

            table_data.append([
                str(page_num),
                str(frame_num),
                ','.join(flags)
            ])

        table = Table(
            table_data,
            row_labels=[Text(f"{i}") for i in range(self.num_entries)],
            col_labels=[Text("Page"), Text("Frame"), Text("Flags")],
            include_outer_lines=True,
            background_rectangle_color=theme.colors.TABLE_BACKGROUND,
            arrange_in_grid_config={"cell_alignment": RIGHT}
        )

        self.add(table)


class SlabAllocatorViz(VGroup if MANIM_AVAILABLE else object):
    """
    Slab allocator visualization.

    Shows different sized slabs with allocated objects.
    Migrated from lib/manim-os.py create_slabs().

    Attributes:
        slab_sizes: List of slab sizes
        allocations: List of allocation counts per slab
    """

    def __init__(
        self,
        slab_sizes: List[float] = [1.3, 2.0, 4.0],
        allocations: List[int] = [4, 6, 13],
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.slab_sizes = slab_sizes
        self.allocations = allocations

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the slab allocator visualization."""
        from ..themes import get_theme

        theme = get_theme()

        colors = [RED, PURPLE, ORANGE]
        distance = 4

        # Create slab containers
        containers = VGroup()
        for i, size in enumerate(self.slab_sizes):
            container = Square(
                side_length=size,
                fill_opacity=0.3,
                color=BLUE
            )

            # Position containers
            if i == 0:
                pass  # First one stays
            elif i == 1:
                pass  # Middle one
            else:
                container.next_to(containers[1], RIGHT * distance)

            containers.add(container)

        self.add(containers)

        # Create allocated objects
        for i, (size, count) in enumerate(zip(self.slab_sizes, self.allocations)):
            objects = VGroup(*[
                Rectangle(
                    height=0.2,
                    width=size - 0.2,
                    fill_opacity=0.5,
                    color=colors[i % len(colors)]
                )
                for _ in range(count)
            ])

            objects.arrange(direction=UP, buff=0.1)
            objects.move_to(containers[i])

            self.add(objects)


class ChunkViz(VGroup if MANIM_AVAILABLE else object):
    """
    Memory chunk visualization (malloc chunk).

    Shows a chunk with header and data sections.
    Migrated from lib/manim-os.py create_allocate_chunk().

    Attributes:
        chunk_size: Size of the data portion
        show_prev_size: Whether to show prev_size field
        show_size: Whether to show size field
    """

    def __init__(
        self,
        chunk_size: float = 2.5,
        show_prev_size: bool = True,
        show_size: bool = True,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.chunk_size = chunk_size
        self.show_prev_size = show_prev_size
        self.show_size = show_size

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the chunk visualization."""
        from ..themes import get_theme

        theme = get_theme()

        chunk_group = VGroup()
        text_group = VGroup()

        fields = []
        if self.show_prev_size:
            fields.append("presize")
        if self.show_size:
            fields.append("size")
        fields.extend(["F", "B", "data"])

        for i, field_name in enumerate(fields):
            if field_name in ["presize", "size"]:
                r_color = theme.colors.CHUNK_HEADER
                height = 0.5
            elif field_name == "data":
                r_color = theme.colors.CHUNK_DATA
                height = self.chunk_size
            else:
                r_color = theme.colors.CHUNK_FLAGS
                height = 0.5

            rect = Rectangle(
                color=r_color,
                fill_opacity=0.5,
                width=2,
                height=height
            )
            rect.next_to(chunk_group, DOWN, buff=0)

            text = Text(field_name).scale(0.5).move_to(rect.get_center())
            text_group.add(text)
            chunk_group.add(rect)

        self.add(chunk_group, text_group)
