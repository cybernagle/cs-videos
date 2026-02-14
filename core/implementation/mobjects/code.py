"""
Code display mobject for showing source code with syntax highlighting.
"""
try:
    from manim import *
    from manim import VGroup, Rectangle, Text, Table
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    VGroup = object
    Rectangle = object
    Text = object
    Table = object

from typing import Optional, List, Dict


class CodeDisplay(VGroup if MANIM_AVAILABLE else object):
    """
    Display source code with syntax highlighting.

    Attributes:
        code: Source code string
        language: Programming language for syntax highlighting
        font_size: Font size for code
        line_numbers: Whether to show line numbers
    """

    def __init__(
        self,
        code: str = "",
        language: str = "C",
        font_size: float = 24,
        line_numbers: bool = True,
        background_color: str = "#1e1e1e",
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.code = code
        self.language = language
        self.font_size = font_size
        self.line_numbers = line_numbers
        self.background_color = background_color

        # Parse code into lines
        self.lines = code.strip().split('\n') if code else []

        # Build the mobject
        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the code display mobject."""
        from ..themes import get_theme

        theme = get_theme()

        # Create background
        bg_height = len(self.lines) * 0.4 + 0.5
        background = Rectangle(
            width=10,
            height=bg_height,
            fill_color=self.background_color,
            fill_opacity=1.0,
            stroke_width=0
        )

        self.add(background)

        # Add code lines
        for i, line in enumerate(self.lines):
            y_pos = bg_height / 2 - 0.3 - i * 0.4

            # Line number
            if self.line_numbers:
                line_num = Text(
                    str(i + 1),
                    font_size=self.font_size * 0.8,
                    color=theme.colors.GRAY
                ).move_to([-4.5, y_pos, 0])
                self.add(line_num)

            # Code text
            code_text = Text(
                line,
                font_size=self.font_size,
                color=theme.colors.WHITE,
                font="Fira Code"
            ).move_to([-3.5, y_pos, 0])

            self.add(code_text)

    def highlight_line(self, line_number: int, color: str = "YELLOW"):
        """Highlight a specific line."""
        # Find the line mobject and add highlight
        # Implementation depends on how mobjects are stored
        pass

    def set_code(self, new_code: str):
        """Update the code text."""
        self.code = new_code
        self.lines = new_code.strip().split('\n')
        # Rebuild the mobject
        self.clear()
        self._build()


class InlineCode(VGroup if MANIM_AVAILABLE else object):
    """
    Inline code element (single line or expression).

    Useful for showing code snippets within explanations.
    """

    def __init__(
        self,
        code: str,
        font_size: float = 28,
        background: bool = True,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.code = code
        self.font_size = font_size
        self.background = background

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the inline code mobject."""
        from ..themes import get_theme

        theme = get_theme()

        # Code text
        text = Text(
            self.code,
            font_size=self.font_size,
            color=theme.colors.CODE_FOREGROUND,
            font="Fira Code"
        )

        if self.background:
            # Add background rectangle
            bg = Rectangle(
                width=text.width + 0.4,
                height=text.height + 0.2,
                fill_color=theme.colors.CODE_BACKGROUND,
                fill_opacity=1.0,
                stroke_color=theme.colors.CODE_BORDER,
                stroke_width=1
            )
            bg.move_to(text.get_center())
            self.add(bg)

        self.add(text)


class FunctionSignature(VGroup if MANIM_AVAILABLE else object):
    """
    Display a function signature with parameter highlighting.

    Useful for explaining function interfaces.
    """

    def __init__(
        self,
        return_type: str,
        function_name: str,
        parameters: List[str],
        font_size: float = 28,
        **kwargs
    ):
        if not MANIM_AVAILABLE:
            return

        self.return_type = return_type
        self.function_name = function_name
        self.parameters = parameters
        self.font_size = font_size

        super().__init__(**kwargs)
        self._build()

    def _build(self):
        """Build the function signature mobject."""
        from ..themes import get_theme

        theme = get_theme()

        # Return type
        return_text = Text(
            self.return_type,
            font_size=self.font_size,
            color=theme.colors.TYPE_COLOR
        )
        self.add(return_text)

        # Function name
        name_text = Text(
            self.function_name,
            font_size=self.font_size,
            color=theme.colors.FUNCTION_NAME_COLOR
        ).next_to(return_text, RIGHT, buff=0.2)
        self.add(name_text)

        # Opening parenthesis
        paren1 = Text("(", font_size=self.font_size, color=theme.colors.WHITE).next_to(name_text, RIGHT, buff=0.05)
        self.add(paren1)

        # Parameters
        last = paren1
        for i, param in enumerate(self.parameters):
            param_text = Text(param, font_size=self.font_size, color=theme.colors.PARAMETER_COLOR).next_to(last, RIGHT, buff=0.05)
            self.add(param_text)
            last = param_text

            if i < len(self.parameters) - 1:
                comma = Text(", ", font_size=self.font_size, color=theme.colors.WHITE).next_to(last, RIGHT, buff=0.05)
                self.add(comma)
                last = comma

        # Closing parenthesis
        paren2 = Text(")", font_size=self.font_size, color=theme.colors.WHITE).next_to(last, RIGHT, buff=0.05)
        self.add(paren2)
