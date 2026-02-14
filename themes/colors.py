"""
Color palette and theme definitions.

Provides semantic color names for consistent styling across videos.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
 class ThemePalette:
    """
    Theme color palette with semantic color names.

    Colors are organized by purpose (syntax, UI, memory, etc.)
    for easy reference and consistency.
    """

    # Background colors
    BACKGROUND: str = "#2B3A42"
    BACKGROUND_DARK: str = "#1a1a1a"
    BACKGROUND_LIGHT: str = "#3a4a52"

    # Text colors
    WHITE: str = "#FFFFFF"
    GRAY: str = "#888888"
    BLACK: str = "#000000"

    # Accent colors (from original design)
    WORD_A: str = "#00CED1"  # Dark Turquoise
    OBJ_A: str = "#3EB489"  # Medium Sea Green
    MEMORY: str = "#FFFF00"  # Yellow

    # Syntax highlighting colors
    KEYWORD: str = "#569CD6"  # Blue
    STRING: str = "#CE9178"  # Orange/Brown
    COMMENT: str = "#6A9955"  # Green
    FUNCTION: str = "#DCDCAA"  # Light Yellow
    NUMBER: str = "#B5CEA8"  # Light Green
    TYPE_COLOR: str = "#4EC9B0"  # Teal
    FUNCTION_NAME_COLOR: str = "#DCDCAA"  # Light Yellow
    PARAMETER_COLOR: str = "#9CDCFE"  # Light Blue
    VARIABLE: str = "#9CDCFE"  # Light Blue

    # Code display colors
    CODE_BACKGROUND: str = "#1E1E1E"
    CODE_FOREGROUND: str = "#D4D4D4"
    CODE_BORDER: str = "#404040"

    # Memory visualization colors
    MEMORY_CELL: str = "#4FC3F7"  # Light Blue
    MEMORY_ALLOCATED: str = "#FF7043"  # Orange
    MEMORY_FREE: str = "#81C784"  # Green
    MEMORY_HIGHLIGHT: str = "#FFEB3B"  # Yellow

    # Register colors
    REGISTER_BG: str = "#37474F"
    REGISTER_NAME: str = "#FFA726"
    REGISTER_VALUE: str = "#E0E0E0"

    # Bit field colors
    BIT_ONE: str = "#66BB6A"  # Green
    BIT_ZERO: str = "#78909C"  # Blue Gray

    # Flag colors
    FLAG_SET: str = "#4CAF50"  # Green
    FLAG_CLEAR: str = "#757575"  # Gray

    # UI element colors
    HIGHLIGHT: str = "#FFD54F"  # Amber
    WARNING: str = "#FF5722"  # Deep Orange
    ERROR: str = "#F44336"  # Red
    SUCCESS: str = "#4CAF50"  # Green
    INFO: str = "#2196F3"  # Blue

    # Table colors
    TABLE_BACKGROUND: str = "#263238"
    TABLE_BORDER: str = "#546E7A"
    TABLE_HEADER: str = "#37474F"

    # Data structure colors
    NODE_BG: str = "#5C6BC0"  # Indigo
    NODE_BORDER: str = "#7986CB"
    EDGE_COLOR: str = "#9FA8DA"
    ARROW_COLOR: str = "#FFFFFF"

    # Chunk colors (malloc)
    CHUNK_HEADER: str = "#FFF176"  # Yellow
    CHUNK_DATA: str = "#81D4FA"  # Light Blue
    CHUNK_FLAGS: str = "#A1887F"  # Brown

    # Process colors
    PROCESS_RUNNING: str = "#66BB6A"  # Green
    PROCESS_READY: str = "#42A5F5"  # Blue
    PROCESS_WAITING: str = "#FFA726"  # Orange
    PROCESS_BLOCKED: str = "#EF5350"  # Red

    # Animation colors
    TRANSFORM_FROM: str = "#AB47BC"  # Purple
    TRANSFORM_TO: str = "#26C6DA"  # Cyan

    def to_dict(self) -> Dict[str, str]:
        """Convert palette to dictionary."""
        return {
            name: getattr(self, name)
            for name in dir(self)
            if name.isupper() and not name.startswith('_')
        }


# Default theme instance
_default_theme: Optional[ThemePalette] = None


def get_theme() -> ThemePalette:
    """Get the current theme palette."""
    global _default_theme
    if _default_theme is None:
        _default_theme = ThemePalette()
    return _default_theme


def set_theme(theme: ThemePalette) -> None:
    """Set the global theme palette."""
    global _default_theme
    _default_theme = theme


# Predefined theme presets

class DarkTheme(ThemePalette):
    """Dark theme for better visibility in videos."""

    BACKGROUND = "#1E1E1E"
    BACKGROUND_DARK = "#121212"
    BACKGROUND_LIGHT = "#2D2D2D"


class LightTheme(ThemePalette):
    """Light theme (not recommended for video)."""

    BACKGROUND = "#F5F5F5"
    BACKGROUND_DARK = "#E0E0E0"
    BACKGROUND_LIGHT = "#FFFFFF"
    BLACK = "#FFFFFF"
    WHITE = "#000000"


class HighContrastTheme(ThemePalette):
    """High contrast theme for accessibility."""

    BACKGROUND = "#000000"
    WHITE = "#FFFFFF"
    MEMORY = "#FFFF00"
    HIGHLIGHT = "#00FF00"


def create_custom_theme(**overrides) -> ThemePalette:
    """
    Create a custom theme with overridden colors.

    Args:
        **overrides: Color name to hex value mappings

    Returns:
        New ThemePalette with overridden colors
    """
    theme = ThemePalette()
    for name, value in overrides.items():
        if hasattr(theme, name.upper()):
            setattr(theme, name.upper(), value)
    return theme
