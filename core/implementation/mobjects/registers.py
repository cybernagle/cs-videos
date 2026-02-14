"""
CPU register visualization mobjects.

Components for displaying CPU registers and flags.
"""
try:
    from manim import *
    from manim import VGroup, Rectangle, Text, Table, Square
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    VGroup = object
    Rectangle = object
    Text = object
    Table = object
    Square = object

from typing import Optional, Dict, List


class RegisterDisplay(VGroup if MANIM_AVAILABLE else object):
    """
    Display a single CPU register with name and value.

    Attributes:
        name: Register name (e.g., "EAX", "RIP")
        value: Register value
        bits: Number of bits (32 or 64)
        width: Display width
        height: Display height
    """

    def __init__(
        self,
        name: str = "REG",
        value: int = 0,
        bits: int = 32,
        width: float = 2.5,
        height: float = 1.0,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.name = name
        self.value = value
        self.bits = bits
        self.width = width
        self.height = height

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the register display mobject."""
        from ..themes import get_theme

        theme = get_theme()

        # Background rectangle
        bg = Rectangle(
            width=self.width,
            height=self.height,
            fill_color=theme.colors.REGISTER_BG,
            fill_opacity=0.3,
            stroke_color=theme.colors.WHITE,
            stroke_width=2
        )
        self.add(bg)

        # Register name
        name_text = Text(
            self.name,
            font_size=24,
            color=theme.colors.REGISTER_NAME
        ).move_to([bg.get_left()[0] + 0.5, bg.get_center()[1], 0])

        # Check alignment - manim text centering
        name_text.align_to(bg, LEFT).shift(RIGHT * 0.3)
        self.add(name_text)

        # Register value (hexadecimal)
        hex_str = self._format_value()
        value_text = Text(
            hex_str,
            font_size=20,
            color=theme.colors.WHITE
        ).next_to(name_text, RIGHT, buff=0.3)
        self.add(value_text)

    def _format_value(self) -> str:
        """Format the value as hexadecimal."""
        # Calculate hex digits based on bits
        hex_digits = self.bits // 4
        format_str = f"0x{{:0{hex_digits}X}}"
        return format_str.format(self.value & ((1 << self.bits) - 1))

    def set_value(self, new_value: int):
        """Update the register value."""
        self.value = new_value
        # Would update the text mobject

    def increment(self, amount: int = 1):
        """Increment the register value."""
        self.value = (self.value + amount) & ((1 << self.bits) - 1)

    def decrement(self, amount: int = 1):
        """Decrement the register value."""
        self.value = (self.value - amount) & ((1 << self.bits) - 1)


class BitFieldDisplay(VGroup if MANIM_AVAILABLE else object):
    """
    Display a bit field with individual bits.

    Useful for showing flags, status registers, etc.

    Attributes:
        value: Integer value to display as bits
        num_bits: Number of bits to display
        label: Optional label for the field
        bit_labels: Optional labels for individual bits
    """

    def __init__(
        self,
        value: int = 0,
        num_bits: int = 8,
        label: str = "",
        bit_labels: Optional[List[str]] = None,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.value = value
        self.num_bits = num_bits
        self.label = label
        self.bit_labels = bit_labels

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the bit field display."""
        from ..themes import get_theme

        theme = get_theme()

        bits = VGroup()

        for i in range(self.num_bits):
            bit_value = (self.value >> i) & 1

            # Bit square
            square = Square(
                side_length=0.5,
                fill_color=theme.colors.BIT_ONE if bit_value else theme.colors.BIT_ZERO,
                fill_opacity=0.7,
                stroke_color=theme.colors.WHITE,
                stroke_width=1
            )

            # Position bit (right to left, LSB on right)
            x_pos = -(self.num_bits - 1 - i) * 0.55
            square.move_to([x_pos, 0, 0])

            bits.add(square)

            # Bit value text
            bit_text = Text(
                str(bit_value),
                font_size=20,
                color=theme.colors.WHITE
            ).move_to(square.get_center())
            bits.add(bit_text)

            # Bit label if provided
            if self.bit_labels and i < len(self.bit_labels):
                label = Text(
                    self.bit_labels[i],
                    font_size=12,
                    color=theme.colors.GRAY
                ).next_to(square, UP, buff=0.1)
                bits.add(label)

        self.add(bits)

        # Add main label if provided
        if self.label:
            label_text = Text(
                self.label,
                font_size=18,
                color=theme.colors.WHITE
            ).next_to(bits, DOWN, buff=0.3)
            self.add(label_text)

    def set_bit(self, bit_index: int, value: bool):
        """Set a specific bit."""
        if value:
            self.value |= (1 << bit_index)
        else:
            self.value &= ~(1 << bit_index)

    def toggle_bit(self, bit_index: int):
        """Toggle a specific bit."""
        self.value ^= (1 << bit_index)


class FlagRegister(VGroup if MANIM_AVAILABLE else object):
    """
    Display CPU flags register (CF, PF, AF, ZF, SF, TF, IF, DF, OF).

    Common x86 flags:
    - CF: Carry Flag
    - PF: Parity Flag
    - AF: Auxiliary Flag
    - ZF: Zero Flag
    - SF: Sign Flag
    - TF: Trap Flag
    - IF: Interrupt Flag
    - DF: Direction Flag
    - OF: Overflow Flag
    """

    FLAG_NAMES = ["CF", "PF", "AF", "ZF", "SF", "IF", "DF", "OF"]

    def __init__(
        self,
        value: int = 0,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.value = value
        self.flag_bits: Dict[str, int] = {}

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the flags register display."""
        from ..themes import get_theme

        theme = get_theme()

        flags = VGroup()

        for i, flag_name in enumerate(self.FLAG_NAMES):
            bit_value = (self.value >> i) & 1
            self.flag_bits[flag_name] = bit_value

            # Flag background
            bg = Rectangle(
                width=0.8,
                height=0.5,
                fill_color=theme.colors.FLAG_SET if bit_value else theme.colors.FLAG_CLEAR,
                fill_opacity=0.7,
                stroke_color=theme.colors.WHITE,
                stroke_width=1
            )

            # Position flag
            y_pos = (i - len(self.FLAG_NAMES) / 2) * 0.6
            bg.move_to([0, y_pos, 0])

            flags.add(bg)

            # Flag name
            name_text = Text(
                flag_name,
                font_size=16,
                color=theme.colors.WHITE
            ).move_to(bg.get_center())
            flags.add(name_text)

        self.add(flags)

    def set_flag(self, flag_name: str, value: bool):
        """Set a specific flag."""
        if flag_name in self.FLAG_NAMES:
            bit_index = self.FLAG_NAMES.index(flag_name)
            if value:
                self.value |= (1 << bit_index)
            else:
                self.value &= ~(1 << bit_index)
            self.flag_bits[flag_name] = 1 if value else 0

    def get_flag(self, flag_name: str) -> bool:
        """Get the value of a specific flag."""
        return self.flag_bits.get(flag_name, False)

    def set_zero_flag(self, value: int):
        """Set ZF based on whether value is zero."""
        self.set_flag("ZF", value == 0)

    def set_sign_flag(self, value: int, bits: int = 32):
        """Set SF based on the sign bit of value."""
        self.set_flag("SF", (value >> (bits - 1)) & 1)

    def set_carry_flag(self, did_carry: bool):
        """Set CF."""
        self.set_flag("CF", did_carry)


class RegisterFile(VGroup if MANIM_AVAILABLE else object):
    """
    Display a collection of CPU registers.

    Typical x86 registers:
    - General purpose: EAX, EBX, ECX, EDX, ESI, EDI, EBP, ESP
    - Special: EIP (instruction pointer)

    Attributes:
        registers: Dictionary of register name to value
        layout: Layout arrangement ('vertical' or 'horizontal')
    """

    def __init__(
        self,
        registers: Optional[Dict[str, int]] = None,
        layout: str = "vertical",
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.registers = registers or self._default_registers()
        self.layout = layout

        super().__init__(**kwargs)
        self._build()

    def _default_registers(self) -> Dict[str, int]:
        """Get default x86 register set."""
        return {
            'EAX': 0,
            'EBX': 0,
            'ECX': 0,
            'EDX': 0,
            'ESI': 0,
            'EDI': 0,
            'EBP': 0,
            'ESP': 0,
            'EIP': 0
        }

    def _build(self):
        """Build the register file display."""
        register_displays = []

        for name, value in self.registers.items():
            reg = RegisterDisplay(name=name, value=value, bits=32)
            register_displays.append(reg)

        if self.layout == "vertical":
            for i, reg in enumerate(register_displays):
                y_pos = 2 - i * 1.1
                reg.move_to([0, y_pos, 0])
                self.add(reg)
        else:  # horizontal
            for i, reg in enumerate(register_displays):
                x_pos = -6 + i * 2.7
                reg.move_to([x_pos, 0, 0])
                self.add(reg)

    def get_register(self, name: str) -> int:
        """Get a register value."""
        return self.registers.get(name.upper(), 0)

    def set_register(self, name: str, value: int):
        """Set a register value."""
        self.registers[name.upper()] = value
        # Would update the display
