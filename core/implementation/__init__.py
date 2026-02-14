"""
Implementation Layer - LAYER 4

Concrete Manim implementations, completely decoupled from business logic.

This layer is responsible for:
- Concrete Manim mobject implementations
- Animation wrappers
- Scene base classes
- Rendering configuration
"""

from .scenes import LayeredScene, SceneBuilder

__all__ = [
    'LayeredScene',
    'SceneBuilder',
]
