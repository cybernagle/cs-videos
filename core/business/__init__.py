"""
Business Layer - LAYER 1

Pure narrative and domain logic, completely independent of visualization.

This layer is responsible for:
- Story/script abstractions
- Narrative constructs
- Business entities (Process, Memory, etc.)
"""

from .story import Story, Chapter, SceneNarrative, NarrativeAction
from .narrative import ShowCodeAction, TransformAction, HighlightAction, VoiceoverAction

__all__ = [
    'Story',
    'Chapter',
    'SceneNarrative',
    'NarrativeAction',
    'ShowCodeAction',
    'TransformAction',
    'HighlightAction',
    'VoiceoverAction',
]
