"""
Concrete Manim mobject implementations.

These are reusable visual components migrated from lib/manim-os.py
and enhanced to work with the 4-layer architecture.
"""
from .code import CodeDisplay
from .memory import MemoryViz, MemoryCell, PageTableViz
from .registers import RegisterDisplay

__all__ = [
    'CodeDisplay',
    'MemoryViz',
    'MemoryCell',
    'PageTableViz',
    'RegisterDisplay',
]
