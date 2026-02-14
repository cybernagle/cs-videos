"""
Scene base classes that integrate the 4-layer architecture with Manim.

Provides LayeredScene which uses spacetime timelines and the director
to render animations with automatic conflict detection.
"""
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    from manim import *
    from manim_voiceover import VoiceoverScene
    MANIM_AVAILABLE = True
except ImportError:
    MANIM_AVAILABLE = False
    # Create dummy classes for type checking
    class Scene:
        pass
    class VoiceoverScene:
        pass

from ..spacetime.timelines import Timeline
from ..spacetime.conflict_detection import ConflictDetector, ConflictReport
from ..scheduler.director import Director, ManimDirector
from ..business.story import Story


class LayeredScene(VoiceoverScene if MANIM_AVAILABLE else Scene):
    """
    Base scene class with 4-layer integration.

    Features:
    - Automatic conflict detection before rendering
    - Director-based animation execution
    - Voiceover synchronization support
    - Spacetime timeline integration

    Usage:
        class MyScene(LayeredScene):
            def construct(self):
                story = self.create_story()
                self.render_story(story)

        def create_story(self) -> Story:
            # Define story at business layer
            ...
    """

    def __init__(self, story: Optional[Story] = None, **kwargs):
        """
        Initialize the layered scene.

        Args:
            story: Optional story to render
            **kwargs: Additional arguments passed to Manim Scene
        """
        if MANIM_AVAILABLE:
            super().__init__(**kwargs)
        else:
            # For development without Manim
            pass

        self.story = story
        self.timeline: Optional[Timeline] = None
        self.director: Optional[ManimDirector] = None
        self.conflict_detector: Optional[ConflictDetector] = None
        self.mobjects_map: Dict[str, Any] = {}  # Map object IDs to Manim mobjects

    def check_conflicts(
        self, timeline: Optional[Timeline] = None
    ) -> ConflictReport:
        """
        Check for spacetime conflicts in the timeline.

        Args:
            timeline: Timeline to check (defaults to self.timeline)

        Returns:
            ConflictReport with detected conflicts
        """
        if timeline is None:
            timeline = self.timeline

        if timeline is None:
            raise ValueError("No timeline to check")

        if self.conflict_detector is None:
            self.conflict_detector = ConflictDetector()

        report = self.conflict_detector.detect_conflicts(timeline)
        return report

    def render_story(self, story: Optional[Story] = None) -> None:
        """
        Render a story using the 4-layer architecture.

        This is the main entry point for rendering.

        Args:
            story: Story to render (defaults to self.story)

        Raises:
            ValueError: If conflicts are detected
        """
        if story is None:
            story = self.story

        if story is None:
            raise ValueError("No story to render")

        # Convert story to spacetime timeline
        sequence = story.to_spacetime()
        merged_timeline = sequence.merge_all()
        self.timeline = merged_timeline

        # Check for conflicts
        report = self.check_conflicts()
        if report.has_conflicts:
            print("⚠ Spacetime conflicts detected:")
            report.print_report()
            raise ValueError("Cannot render with conflicts detected")

        # Create director and execute
        self.director = ManimDirector(timeline=self.timeline)
        self.director.execute(self)

    def render_timeline(self, timeline: Timeline) -> None:
        """
        Render a spacetime timeline directly.

        Args:
            timeline: Timeline to render

        Raises:
            ValueError: If conflicts are detected
        """
        self.timeline = timeline

        # Check for conflicts
        report = self.check_conflicts()
        if report.has_conflicts:
            print("⚠ Spacetime conflicts detected:")
            report.print_report()
            raise ValueError("Cannot render with conflicts detected")

        # Create director and execute
        self.director = ManimDirector(timeline=self.timeline)
        self.director.execute(self)

    # Animation handlers - these will be called by the director

    def _handle_show(self, instruction) -> None:
        """Handle a 'show' animation instruction."""
        obj_id = instruction.object_id
        params = instruction.parameters
        obj_type = params.get('type', 'unknown')
        space = params.get('space')
        layer = params.get('layer', 0)

        # Create appropriate mobject based on type
        mobject = self._create_mobject(obj_type, params)

        if mobject is None:
            return

        # Position the mobject
        if space:
            mobject.move_to([space.center[0], space.center[1], 0])

        # Add to scene
        self.play(FadeIn(mobject), run_time=instruction.duration)

        # Register mobject
        self.mobjects_map[obj_id] = mobject
        if self.director:
            self.director.register_mobject(obj_id, mobject)

    def _handle_show_code(self, instruction) -> None:
        """Handle a 'show_code' animation instruction."""
        from .mobjects.code import CodeDisplay

        code = instruction.parameters.get('code', '')
        language = instruction.parameters.get('language', 'C')
        space = instruction.parameters.get('space')

        mobject = CodeDisplay(code=code, language=language)

        if space:
            mobject.move_to([space.center[0], space.center[1], 0])

        self.play(FadeIn(mobject), run_time=instruction.duration)

        self.mobjects_map[instruction.object_id] = mobject
        if self.director:
            self.director.register_mobject(instruction.object_id, mobject)

    def _handle_show_memory(self, instruction) -> None:
        """Handle a 'show_memory' animation instruction."""
        from .mobjects.memory import MemoryViz

        cells = instruction.parameters.get('cells', 16)
        rows = instruction.parameters.get('rows', 1)
        values = instruction.parameters.get('values')
        highlight_cells = instruction.parameters.get('highlight_cells', [])
        space = instruction.parameters.get('space')

        mobject = MemoryViz(cells=cells, rows=rows, values=values,
                          highlight_cells=highlight_cells)

        if space:
            mobject.move_to([space.center[0], space.center[1], 0])

        self.play(FadeIn(mobject), run_time=instruction.duration)

        self.mobjects_map[instruction.object_id] = mobject
        if self.director:
            self.director.register_mobject(instruction.object_id, mobject)

    def _handle_show_register(self, instruction) -> None:
        """Handle a 'show_register' animation instruction."""
        from .mobjects.registers import RegisterDisplay

        name = instruction.parameters.get('name', 'REG')
        value = instruction.parameters.get('value', 0)
        bits = instruction.parameters.get('bits', 32)
        space = instruction.parameters.get('space')

        mobject = RegisterDisplay(name=name, value=value, bits=bits)

        if space:
            mobject.move_to([space.center[0], space.center[1], 0])

        self.play(FadeIn(mobject), run_time=instruction.duration)

        self.mobjects_map[instruction.object_id] = mobject
        if self.director:
            self.director.register_mobject(instruction.object_id, mobject)

    def _handle_default(self, instruction) -> None:
        """Default handler for unknown animation types."""
        print(f"Warning: No handler for animation type '{instruction.action_type}'")

    def _create_mobject(self, obj_type: str, params: Dict[str, Any]) -> Optional[Any]:
        """
        Create a Manim mobject based on type.

        Args:
            obj_type: Type of object to create
            params: Creation parameters

        Returns:
            Manim mobject or None
        """
        # This is a placeholder - actual implementation would
        # delegate to component factory based on obj_type
        return None


class SceneBuilder:
    """
    Helper class for building Manim scenes using the 4-layer architecture.

    Provides a fluent interface for scene construction.
    """

    def __init__(self, scene_class: type = LayeredScene):
        """
        Initialize the scene builder.

        Args:
            scene_class: Scene class to use (default: LayeredScene)
        """
        self.scene_class = scene_class
        self.story: Optional[Story] = None
        self.timeline: Optional[Timeline] = None

    def with_story(self, story: Story) -> 'SceneBuilder':
        """Set the story to render."""
        self.story = story
        return self

    def with_timeline(self, timeline: Timeline) -> 'SceneBuilder':
        """Set the timeline to render."""
        self.timeline = timeline
        return self

    def check_conflicts(self) -> ConflictReport:
        """Check the timeline for conflicts."""
        if self.timeline is None:
            raise ValueError("No timeline set")

        detector = ConflictDetector()
        return detector.detect_conflicts(self.timeline)

    def build(self) -> LayeredScene:
        """Build and return the scene instance."""
        return self.scene_class(story=self.story)

    def to_config(self) -> Dict[str, Any]:
        """
        Export scene configuration as dictionary.

        Useful for serialization and debugging.
        """
        return {
            'scene_class': self.scene_class.__name__,
            'has_story': self.story is not None,
            'has_timeline': self.timeline is not None,
            'story_title': self.story.title if self.story else None,
            'story_duration': self.story.duration if self.story else None,
            'timeline_objects': len(self.timeline.objects) if self.timeline else 0,
            'timeline_duration': self.timeline.duration if self.timeline else None,
        }


def create_scene(story: Story) -> LayeredScene:
    """
    Convenience function to create a scene from a story.

    Args:
        story: Story to render

    Returns:
        LayeredScene instance
    """
    return LayeredScene(story=story)


def render_to_file(
    story: Story,
    output_path: str,
    scene_class: type = LayeredScene,
    **manim_kwargs
) -> None:
    """
    Render a story to a video file.

    This is a convenience wrapper around Manim's rendering.

    Args:
        story: Story to render
        output_path: Output file path
        scene_class: Scene class to use
        **manim_kwargs: Additional arguments for Manim
    """
    if not MANIM_AVAILABLE:
        print("Manim is not available. Cannot render.")
        return

    # Create temporary scene class
    class RenderScene(scene_class):
        def construct(self):
            self.render_story(story)

    # Manim would handle the actual rendering
    # This is a placeholder for the rendering logic
    print(f"Would render to: {output_path}")
    print(f"Story: {story.title}")
    print(f"Duration: {story.duration:.2f}s")
    print(f"Chapters: {len(story.chapters)}")
    print(f"Scenes: {story.scene_count}")
