"""
Story and script abstractions for video narratives.

This module provides the user-facing API for creating video stories
without worrying about visualization details.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


@dataclass
class SceneNarrative:
    """
    A single narrative beat or scene in a story.

    Contains the description, voiceover text, and a list of actions
    that make up this narrative moment.

    Attributes:
        description: Human-readable description of the scene
        voiceover_text: Text to be spoken during this scene
        actions: List of narrative actions
        bookmarks: Dict of bookmark name to time offset
        metadata: Optional additional metadata
    """

    description: str
    voiceover_text: str = ""
    actions: List['NarrativeAction'] = field(default_factory=list)
    bookmarks: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        """Estimated duration based on voiceover text length."""
        # Rough estimate: ~150 words per minute, or ~2.5 words per second
        word_count = len(self.voiceover_text.split())
        return max(1.0, word_count / 2.5)

    def add_action(self, action: 'NarrativeAction') -> None:
        """Add an action to this scene."""
        self.actions.append(action)

    def add_bookmark(self, name: str, time: float) -> None:
        """Add a bookmark at a specific time."""
        self.bookmarks[name] = time

    def get_bookmark(self, name: str) -> Optional[float]:
        """Get a bookmark time by name."""
        return self.bookmarks.get(name)

    def __str__(self) -> str:
        return f"SceneNarrative('{self.description[:30]}...', {len(self.actions)} actions)"


@dataclass
class Chapter:
    """
    A chapter or section of a story.

    Chapters group related scenes together and provide structure
    to longer narratives.

    Attributes:
        title: Chapter title
        description: Optional chapter description
        scenes: List of scenes in this chapter
        metadata: Optional additional metadata
    """

    title: str
    description: str = ""
    scenes: List[SceneNarrative] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        """Total duration of all scenes in this chapter."""
        return sum(scene.duration for scene in self.scenes)

    def add_scene(self, scene: SceneNarrative) -> None:
        """Add a scene to this chapter."""
        self.scenes.append(scene)

    def get_scene(self, index: int) -> Optional[SceneNarrative]:
        """Get a scene by index."""
        if 0 <= index < len(self.scenes):
            return self.scenes[index]
        return None

    def __len__(self) -> int:
        return len(self.scenes)

    def __str__(self) -> str:
        return f"Chapter('{self.title}', {len(self.scenes)} scenes, {self.duration:.1f}s)"


@dataclass
class Story:
    """
    A complete video narrative.

    Stories are the top-level abstraction for video content.
    They contain chapters, which contain scenes, which contain actions.

    This is the main entry point for users creating video content.

    Attributes:
        title: Story title
        description: Optional description
        chapters: List of chapters in this story
        metadata: Optional additional metadata
    """

    title: str
    description: str = ""
    chapters: List[Chapter] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        """Total duration of all chapters."""
        return sum(chapter.duration for chapter in self.chapters)

    @property
    def scene_count(self) -> int:
        """Total number of scenes across all chapters."""
        return sum(len(chapter.scenes) for chapter in self.chapters)

    def add_chapter(self, chapter: Chapter) -> None:
        """Add a chapter to this story."""
        self.chapters.append(chapter)

    def get_chapter(self, index: int) -> Optional[Chapter]:
        """Get a chapter by index."""
        if 0 <= index < len(self.chapters):
            return self.chapters[index]
        return None

    def get_chapter_by_title(self, title: str) -> Optional[Chapter]:
        """Find a chapter by its title."""
        for chapter in self.chapters:
            if chapter.title == title:
                return chapter
        return None

    def to_spacetime(self):
        """
        Convert this story to a spacetime timeline.

        This is the bridge between the business layer and spacetime layer.
        Each narrative action is converted to appropriate spacetime objects.

        Returns:
            Timeline representing this story
        """
        from ..spacetime.objects import SpacetimeObject, SpaceRegion, TimeWindow
        from ..spacetime.timelines import Timeline, TimelineSegment, TimelineSequence

        sequence = TimelineSequence(name=self.title)
        current_time = 0.0

        for chapter in self.chapters:
            timeline = Timeline(name=chapter.title)
            chapter_start = current_time

            for scene in chapter.scenes:
                scene_start = current_time - chapter_start

                # Convert each action to a spacetime object
                for action in scene.actions:
                    obj = action.to_spacetime_object(scene_start)
                    if obj:
                        timeline.add(obj)

                current_time += scene.duration

            segment = TimelineSegment(
                name=chapter.title,
                timeline=timeline,
                start_offset=chapter_start
            )
            sequence.add_segment(segment)

        return sequence

    def __str__(self) -> str:
        return (f"Story('{self.title}', {len(self.chapters)} chapters, "
                f"{self.scene_count} scenes, {self.duration:.1f}s)")

    def __repr__(self) -> str:
        return self.__str__()


# Convenience functions for creating stories

def create_scene(
    description: str,
    voiceover: str = "",
    actions: Optional[List['NarrativeAction']] = None,
    **metadata
) -> SceneNarrative:
    """
    Create a scene with the given parameters.

    Args:
        description: Scene description
        voiceover: Voiceover text
        actions: List of narrative actions
        **metadata: Additional metadata

    Returns:
        SceneNarrative instance
    """
    return SceneNarrative(
        description=description,
        voiceover_text=voiceover,
        actions=actions or [],
        metadata=metadata
    )


def create_chapter(
    title: str,
    scenes: Optional[List[SceneNarrative]] = None,
    description: str = "",
    **metadata
) -> Chapter:
    """
    Create a chapter with the given parameters.

    Args:
        title: Chapter title
        scenes: List of scenes
        description: Optional description
        **metadata: Additional metadata

    Returns:
        Chapter instance
    """
    return Chapter(
        title=title,
        description=description,
        scenes=scenes or [],
        metadata=metadata
    )


class StoryBuilder:
    """
    Builder pattern for constructing stories.

    Provides a fluent interface for building complex stories.
    """

    def __init__(self, title: str):
        self.story = Story(title=title)

    def with_description(self, description: str) -> 'StoryBuilder':
        """Set the story description."""
        self.story.description = description
        return self

    def with_metadata(self, **metadata) -> 'StoryBuilder':
        """Add metadata to the story."""
        self.story.metadata.update(metadata)
        return self

    def add_chapter(self, chapter: Chapter) -> 'StoryBuilder':
        """Add a chapter to the story."""
        self.story.add_chapter(chapter)
        return self

    def new_chapter(self, title: str, description: str = "") -> 'ChapterBuilder':
        """
        Start a new chapter.

        Returns a ChapterBuilder for adding scenes to this chapter.
        """
        return ChapterBuilder(self, title, description)

    def build(self) -> Story:
        """Build and return the story."""
        return self.story


class ChapterBuilder:
    """Builder for constructing chapters."""

    def __init__(self, story_builder: StoryBuilder, title: str, description: str):
        self.story_builder = story_builder
        self.chapter = Chapter(title=title, description=description)

    def with_scene(
        self,
        description: str,
        voiceover: str = "",
        actions: Optional[List['NarrativeAction']] = None
    ) -> 'ChapterBuilder':
        """Add a scene to this chapter."""
        scene = SceneNarrative(
            description=description,
            voiceover_text=voiceover,
            actions=actions or []
        )
        self.chapter.add_scene(scene)
        return self

    def end_chapter(self) -> StoryBuilder:
        """Finish this chapter and return to story builder."""
        self.story_builder.story.add_chapter(self.chapter)
        return self.story_builder
