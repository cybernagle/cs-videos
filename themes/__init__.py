"""
Theme and styling system for cs-videos.

Provides consistent colors, fonts, and visual styles across all videos.
"""
from .colors import ThemePalette, get_theme, set_theme
from .typography import Typography

__all__ = [
    'ThemePalette',
    'get_theme',
    'set_theme',
    'Typography',
]
