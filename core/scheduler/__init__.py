"""
Scheduler Layer - LAYER 3

Orchestrates animations, syncs with voiceover, manages execution order.

This layer is responsible for:
- Animation orchestration (Director)
- Voiceover synchronization
- Bookmark management
- Animation sequence planning
"""

from .director import Director, AnimationPlan
from .voiceover_sync import VoiceoverSyncer, Transcript, Bookmark
from .bookmarks import BookmarkManager
from .animation_plans import AnimationSequence, ParallelAnimation, SerialAnimation

__all__ = [
    'Director',
    'AnimationPlan',
    'VoiceoverSyncer',
    'Transcript',
    'Bookmark',
    'BookmarkManager',
    'AnimationSequence',
    'ParallelAnimation',
    'SerialAnimation',
]
