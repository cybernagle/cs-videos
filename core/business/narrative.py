"""
Narrative actions and constructs.

Defines the building blocks for creating narrative actions
that can be converted to spacetime objects and animations.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum


class ActionType(Enum):
    """Types of narrative actions."""
    SHOW_CODE = "show_code"
    TRANSFORM = "transform"
    HIGHLIGHT = "highlight"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    MOVE = "move"
    SCALE = "scale"
    ROTATE = "rotate"
    VOICEOVER = "voiceover"
    BOOKMARK = "bookmark"
    WAIT = "wait"


@dataclass
class NarrativeAction(ABC):
    """
    Base class for all narrative actions.

    Narrative actions describe what should happen in a scene
    without specifying implementation details.

    Attributes:
        action_type: Type of action
        duration: Duration in seconds (optional, can be estimated)
        metadata: Optional additional data
    """

    action_type: ActionType
    duration: Optional[float] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @abstractmethod
    def to_spacetime_object(self, start_time: float):
        """
        Convert this action to a spacetime object.

        Args:
            start_time: Start time for this action

        Returns:
            SpacetimeObject or None (some actions don't create objects)
        """
        pass

    def get_duration(self) -> float:
        """Get the duration of this action."""
        if self.duration is not None:
            return self.duration
        return 1.0  # Default duration


@dataclass
class ShowCodeAction(NarrativeAction):
    """
    Display code on screen.

    Attributes:
        code: Code string to display
        language: Programming language (for syntax highlighting)
        position: Position enum ('center', 'left', 'right', etc.)
        width: Display width
        height: Display height
    """

    code: str = ""
    language: str = "C"
    position: str = "center"
    width: float = 8.0
    height: float = 3.0
    layer: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.SHOW_CODE

    def to_spacetime_object(self, start_time: float):
        from ..spacetime.objects import SpacetimeObject, SpaceRegion, TimeWindow

        # Calculate position
        if self.position == "center":
            x = -self.width / 2
            y = -self.height / 2
        elif self.position == "left":
            x = -6.0
            y = -self.height / 2
        elif self.position == "right":
            x = 6.0 - self.width
            y = -self.height / 2
        elif self.position == "top":
            x = -self.width / 2
            y = 2.0
        elif self.position == "bottom":
            x = -self.width / 2
            y = -3.0
        else:
            x = -self.width / 2
            y = -self.height / 2

        return SpacetimeObject(
            id=f"code_{id(self)}",
            space=SpaceRegion(x=x, y=y, width=self.width, height=self.height),
            time=TimeWindow(start=start_time, end=start_time + self.get_duration()),
            layer=self.layer,
            metadata={
                'type': 'code_display',
                'code': self.code,
                'language': self.language
            }
        )


@dataclass
class TransformAction(NarrativeAction):
    """
    Transform one object into another.

    Attributes:
        from_id: ID of source object
        to_id: ID of target object
        duration: Transform duration
    """

    from_id: str = ""
    to_id: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.TRANSFORM

    def to_spacetime_object(self, start_time: float):
        # Transforms don't create new objects, they modify existing ones
        # Return None as this is handled by the scheduler
        return None


@dataclass
class HighlightAction(NarrativeAction):
    """
    Highlight or indicate an object.

    Attributes:
        target_id: ID of object to highlight
        color: Highlight color
        scale: Scale factor for highlight effect
    """

    target_id: str = ""
    color: str = "YELLOW"
    scale: float = 1.2

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.HIGHLIGHT
        self.duration = 0.5

    def to_spacetime_object(self, start_time: float):
        # Highlights don't create new objects
        return None


@dataclass
class FadeInAction(NarrativeAction):
    """
    Fade in an object.

    Attributes:
        target_id: ID of object to fade in
        duration: Fade duration
    """

    target_id: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.FADE_IN
        if self.duration is None:
            self.duration = 0.5

    def to_spacetime_object(self, start_time: float):
        return None


@dataclass
class FadeOutAction(NarrativeAction):
    """
    Fade out an object.

    Attributes:
        target_id: ID of object to fade out
        duration: Fade duration
    """

    target_id: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.FADE_OUT
        if self.duration is None:
            self.duration = 0.5

    def to_spacetime_object(self, start_time: float):
        return None


@dataclass
class MoveAction(NarrativeAction):
    """
    Move an object to a new position.

    Attributes:
        target_id: ID of object to move
        to_x: Target X position
        to_y: Target Y position
    """

    target_id: str = ""
    to_x: float = 0.0
    to_y: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.MOVE
        if self.duration is None:
            self.duration = 1.0

    def to_spacetime_object(self, start_time: float):
        return None


@dataclass
class MemoryDisplayAction(NarrativeAction):
    """
    Display a memory visualization.

    Attributes:
        cells: Number of memory cells
        rows: Number of rows
        values: Optional initial values
        position: Position ('left', 'center', 'right')
        highlight_cells: List of cell indices to highlight
    """

    cells: int = 16
    rows: int = 1
    values: Optional[List[int]] = None
    position: str = "center"
    highlight_cells: Optional[List[int]] = None
    layer: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.SHOW_CODE  # Reuse show code for visualization

    def to_spacetime_object(self, start_time: float):
        from ..spacetime.objects import SpacetimeObject, SpaceRegion, TimeWindow

        # Calculate size based on cells and rows
        cell_width = 0.5
        cell_height = 0.5
        width = self.cells / self.rows * cell_width + 0.5
        height = self.rows * cell_height + 0.5

        # Calculate position
        if self.position == "center":
            x = -width / 2
            y = -height / 2
        elif self.position == "left":
            x = -4.0
            y = -height / 2
        elif self.position == "right":
            x = 4.0 - width
            y = -height / 2
        else:
            x = -width / 2
            y = -height / 2

        return SpacetimeObject(
            id=f"memory_{id(self)}",
            space=SpaceRegion(x=x, y=y, width=width, height=height),
            time=TimeWindow(start=start_time, end=start_time + self.get_duration()),
            layer=self.layer,
            metadata={
                'type': 'memory_display',
                'cells': self.cells,
                'rows': self.rows,
                'values': self.values,
                'highlight_cells': self.highlight_cells or []
            }
        )


@dataclass
class RegisterDisplayAction(NarrativeAction):
    """
    Display a CPU register.

    Attributes:
        name: Register name (e.g., 'EAX', 'RIP')
        value: Register value
        bits: Number of bits (32 or 64)
        position: Position
    """

    name: str = "EAX"
    value: int = 0
    bits: int = 32
    position: str = "left"
    layer: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.SHOW_CODE

    def to_spacetime_object(self, start_time: float):
        from ..spacetime.objects import SpacetimeObject, SpaceRegion, TimeWindow

        width = 2.5
        height = 1.0

        if self.position == "left":
            x = -6.0
        elif self.position == "right":
            x = 3.5
        else:
            x = -width / 2

        y = 2.0  # Top of screen

        return SpacetimeObject(
            id=f"register_{self.name}_{id(self)}",
            space=SpaceRegion(x=x, y=y, width=width, height=height),
            time=TimeWindow(start=start_time, end=start_time + self.get_duration()),
            layer=self.layer,
            metadata={
                'type': 'register_display',
                'name': self.name,
                'value': self.value,
                'bits': self.bits
            }
        )


@dataclass
class VoiceoverAction(NarrativeAction):
    """
    Add voiceover text (doesn't create visual objects).

    Attributes:
        text: Voiceover text
        bookmarks: Optional bookmarks for specific moments
    """

    text: str = ""
    bookmarks: Optional[Dict[str, float]] = None

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.VOICEOVER
        # Estimate duration from text
        word_count = len(self.text.split())
        self.duration = max(1.0, word_count / 2.5)

    def to_spacetime_object(self, start_time: float):
        # Voiceover doesn't create visual objects
        return None


@dataclass
class BookmarkAction(NarrativeAction):
    """
    Add a bookmark at a specific time.

    Attributes:
        name: Bookmark name
        time_offset: Time offset from action start
    """

    name: str = ""
    time_offset: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.BOOKMARK
        self.duration = 0.0

    def to_spacetime_object(self, start_time: float):
        return None


@dataclass
class WaitAction(NarrativeAction):
    """
    Pause/wait for a specified duration.

    Attributes:
        duration: Wait duration in seconds
    """

    duration: float = 1.0

    def __post_init__(self):
        super().__post_init__()
        self.action_type = ActionType.WAIT
        self.metadata = {}

    def to_spacetime_object(self, start_time: float):
        return None


# Convenience functions

def show_code(
    code: str,
    language: str = "C",
    position: str = "center",
    duration: Optional[float] = None,
    **kwargs
) -> ShowCodeAction:
    """Create a ShowCodeAction with common defaults."""
    return ShowCodeAction(
        code=code,
        language=language,
        position=position,
        duration=duration,
        **kwargs
    )


def transform(from_id: str, to_id: str, duration: float = 1.0) -> TransformAction:
    """Create a TransformAction."""
    return TransformAction(from_id=from_id, to_id=to_id, duration=duration)


def highlight(target_id: str, color: str = "YELLOW", scale: float = 1.2) -> HighlightAction:
    """Create a HighlightAction."""
    return HighlightAction(target_id=target_id, color=color, scale=scale)


def fade_in(target_id: str, duration: float = 0.5) -> FadeInAction:
    """Create a FadeInAction."""
    return FadeInAction(target_id=target_id, duration=duration)


def fade_out(target_id: str, duration: float = 0.5) -> FadeOutAction:
    """Create a FadeOutAction."""
    return FadeOutAction(target_id=target_id, duration=duration)


def move(target_id: str, to_x: float, to_y: float, duration: float = 1.0) -> MoveAction:
    """Create a MoveAction."""
    return MoveAction(target_id=target_id, to_x=to_x, to_y=to_y, duration=duration)


def display_memory(
    cells: int = 16,
    rows: int = 1,
    values: Optional[List[int]] = None,
    position: str = "center",
    duration: Optional[float] = None
) -> MemoryDisplayAction:
    """Create a MemoryDisplayAction."""
    return MemoryDisplayAction(
        cells=cells,
        rows=rows,
        values=values,
        position=position,
        duration=duration
    )


def display_register(
    name: str,
    value: int,
    bits: int = 32,
    position: str = "left",
    duration: Optional[float] = None
) -> RegisterDisplayAction:
    """Create a RegisterDisplayAction."""
    return RegisterDisplayAction(
        name=name,
        value=value,
        bits=bits,
        position=position,
        duration=duration
    )


def voiceover(text: str) -> VoiceoverAction:
    """Create a VoiceoverAction."""
    return VoiceoverAction(text=text)


def wait(duration: float = 1.0) -> WaitAction:
    """Create a WaitAction."""
    return WaitAction(duration=duration)


def bookmark(name: str, time_offset: float = 0.0) -> BookmarkAction:
    """Create a BookmarkAction."""
    return BookmarkAction(name=name, time_offset=time_offset)
