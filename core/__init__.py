"""
cs-videos 4-Layer Architecture Framework

A framework for creating educational computer science videos using Manim
with proper separation of concerns and spacetime conflict detection.

Layers:
1. Business Layer (core/business/) - Story/scripts, pure narrative logic
2. Spacetime Layer (core/spacetime/) - Objects, timelines, layouts, conflict detection
3. Scheduler Layer (core/scheduler/) - Animation orchestration, voiceover sync
4. Implementation Layer (core/implementation/) - Manim code, concrete mobjects

Example usage:
    from core.business import StoryBuilder
    from core.business.narrative import show_code, voiceover

    story = StoryBuilder("My Video") \\
        .new_chapter("Introduction") \\
        .with_scene("Show code", "Here is some code", [
            show_code("int main() { return 0; }")
        ]) \\
        .end_chapter() \\
        .build()

    # Convert to spacetime timeline
    timeline = story.to_spacetime().merge_all()

    # Check for conflicts
    from core.spacetime import ConflictDetector
    detector = ConflictDetector()
    report = detector.detect_conflicts(timeline)

    if report.has_conflicts:
        report.print_report()
    else:
        # Render with Manim
        from core.implementation import LayeredScene
        scene = LayeredScene(story=story)
        scene.render_story()
"""

from .business import Story, Chapter, SceneNarrative
from .spacetime import SpaceRegion, TimeWindow, SpacetimeObject, Timeline
from .spacetime import ConflictDetector, ConflictReport, LayoutTemplate
from .scheduler import Director, VoiceoverSyncer, BookmarkManager
from .implementation import LayeredScene

__version__ = "1.0.0"

__all__ = [
    # Business Layer
    'Story',
    'Chapter',
    'SceneNarrative',

    # Spacetime Layer
    'SpaceRegion',
    'TimeWindow',
    'SpacetimeObject',
    'Timeline',
    'ConflictDetector',
    'ConflictReport',
    'LayoutTemplate',

    # Scheduler Layer
    'Director',
    'VoiceoverSyncer',
    'BookmarkManager',

    # Implementation Layer
    'LayeredScene',
]
