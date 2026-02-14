"""
Typography and font configurations.

Provides font settings for different text types.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Typography:
    """
    Typography configuration for the video project.

    Defines font sizes, families, and weights for different text types.
    """

    # Font families
    CODE_FONT: str = "Fira Code"
    TEXT_FONT: str = "Noto Sans"
    MATH_FONT: str = "Latin Modern Math"
    MONOSPACE_FONT: str = "Fira Code"

    # Font sizes
    TITLE_SIZE: float = 48
    SUBTITLE_SIZE: float = 36
    HEADING_SIZE: float = 28
    BODY_SIZE: float = 24
    CAPTION_SIZE: float = 20
    CODE_SIZE: float = 22
    SMALL_SIZE: float = 16
    TINY_SIZE: float = 12

    # Font weights (if supported)
    WEIGHT_LIGHT: str = "Light"
    WEIGHT_NORMAL: str = "Regular"
    WEIGHT_MEDIUM: str = "Medium"
    WEIGHT_BOLD: str = "Bold"

    @staticmethod
    def title() -> Dict[str, Any]:
        """Get font configuration for titles."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.TITLE_SIZE,
            'weight': Typography.WEIGHT_BOLD,
            'slant': 'NORMAL'
        }

    @staticmethod
    def subtitle() -> Dict[str, Any]:
        """Get font configuration for subtitles."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.SUBTITLE_SIZE,
            'weight': Typography.WEIGHT_MEDIUM,
            'slant': 'NORMAL'
        }

    @staticmethod
    def heading() -> Dict[str, Any]:
        """Get font configuration for headings."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.HEADING_SIZE,
            'weight': Typography.WEIGHT_MEDIUM,
            'slant': 'NORMAL'
        }

    @staticmethod
    def body() -> Dict[str, Any]:
        """Get font configuration for body text."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.BODY_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'NORMAL'
        }

    @staticmethod
    def code() -> Dict[str, Any]:
        """Get font configuration for code."""
        return {
            'font': Typography.CODE_FONT,
            'size': Typography.CODE_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'ROMAN'  # Monospace should not be italic
        }

    @staticmethod
    def code_inline() -> Dict[str, Any]:
        """Get font configuration for inline code."""
        return {
            'font': Typography.CODE_FONT,
            'size': Typography.BODY_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'ROMAN'
        }

    @staticmethod
    def caption() -> Dict[str, Any]:
        """Get font configuration for captions."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.CAPTION_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'NORMAL'
        }

    @staticmethod
    def small() -> Dict[str, Any]:
        """Get font configuration for small text."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.SMALL_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'NORMAL'
        }

    @staticmethod
    def math() -> Dict[str, Any]:
        """Get font configuration for math."""
        return {
            'font': Typography.MATH_FONT,
            'size': Typography.BODY_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'ITALIC'  # Math is typically italic
        }

    @staticmethod
    def register() -> Dict[str, Any]:
        """Get font configuration for CPU registers."""
        return {
            'font': Typography.MONOSPACE_FONT,
            'size': Typography.CODE_SIZE,
            'weight': Typography.WEIGHT_BOLD,
            'slant': 'NORMAL'
        }

    @staticmethod
    def memory_address() -> Dict[str, Any]:
        """Get font configuration for memory addresses."""
        return {
            'font': Typography.MONOSPACE_FONT,
            'size': Typography.SMALL_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'NORMAL'
        }

    @staticmethod
    def label() -> Dict[str, Any]:
        """Get font configuration for labels."""
        return {
            'font': Typography.TEXT_FONT,
            'size': Typography.SMALL_SIZE,
            'weight': Typography.WEIGHT_NORMAL,
            'slant': 'ITALIC'
        }


class FontScale:
    """
    Font scaling factors for different contexts.

    Useful for adjusting all font sizes proportionally.
    """

    DEFAULT = 1.0
    LARGE = 1.2
    SMALL = 0.85
    TINY = 0.7

    @staticmethod
    def scale_font_config(config: Dict[str, Any], scale: float) -> Dict[str, Any]:
        """
        Scale font configuration by a factor.

        Args:
            config: Font configuration dictionary
            scale: Scaling factor

        Returns:
            Scaled font configuration
        """
        result = config.copy()
        if 'size' in result:
            result['size'] = result['size'] * scale
        return result


# Preset typography configurations

class CompactTypography(Typography):
    """More compact typography for dense content."""

    TITLE_SIZE: float = 40
    SUBTITLE_SIZE: float = 32
    HEADING_SIZE: float = 24
    BODY_SIZE: float = 20
    CAPTION_SIZE: float = 18
    CODE_SIZE: float = 18
    SMALL_SIZE: float = 14


class LargeTypography(Typography):
    """Larger typography for better visibility."""

    TITLE_SIZE: float = 56
    SUBTITLE_SIZE: float = 42
    HEADING_SIZE: float = 32
    BODY_SIZE: float = 28
    CAPTION_SIZE: float = 24
    CODE_SIZE: float = 26
    SMALL_SIZE: float = 20
