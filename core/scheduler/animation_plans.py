"""
Animation sequence planning and composition.

Provides abstractions for composing complex animation sequences
from simpler building blocks.
"""
from dataclasses import dataclass, field
from typing import List, Any, Optional, Union
from abc import ABC, abstractmethod
from enum import Enum


class AnimationType(Enum):
    """Types of animation compositions."""
    SERIAL = "serial"  # Execute one after another
    PARALLEL = "parallel"  # Execute simultaneously
    DELAY = "delay"  # Wait before executing


@dataclass
class AnimationSequence(ABC):
    """
    Base class for animation sequences.

    Animation sequences are composable building blocks for
    creating complex animations.
    """

    @abstractmethod
    def duration(self) -> float:
        """Get the total duration of this sequence."""
        pass

    @abstractmethod
    def to_list(self) -> List[Any]:
        """Convert to a flat list of animations."""
        pass

    def then(self, next_sequence: 'AnimationSequence') -> 'SerialAnimation':
        """
        Chain this sequence with another.

        Args:
            next_sequence: Sequence to execute after this one

        Returns:
            SerialAnimation combining both sequences
        """
        return SerialAnimation([self, next_sequence])

    def and_(self, other_sequence: 'AnimationSequence') -> 'ParallelAnimation':
        """
        Execute this sequence in parallel with another.

        Args:
            other_sequence: Sequence to execute in parallel

        Returns:
            ParallelAnimation combining both sequences
        """
        return ParallelAnimation([self, other_sequence])

    def with_delay(self, delay: float) -> 'SerialAnimation':
        """
        Add a delay before this sequence.

        Args:
            delay: Delay in seconds

        Returns:
            SerialAnimation with delay followed by this sequence
        """
        return SerialAnimation([DelayAnimation(delay), self])


@dataclass
class DelayAnimation(AnimationSequence):
    """
    A simple delay/pause animation.

    Attributes:
        delay: Duration of delay in seconds
    """

    delay: float

    def duration(self) -> float:
        return self.delay

    def to_list(self) -> List[Any]:
        return [{'type': 'delay', 'duration': self.delay}]


@dataclass
class SerialAnimation(AnimationSequence):
    """
    Execute animations serially (one after another).

    Attributes:
        sequences: List of sequences to execute in order
    """

    sequences: List[AnimationSequence] = field(default_factory=list)

    def duration(self) -> float:
        return sum(seq.duration() for seq in self.sequences)

    def to_list(self) -> List[Any]:
        result = []
        for seq in self.sequences:
            result.extend(seq.to_list())
        return result

    def add(self, sequence: AnimationSequence) -> None:
        """Add a sequence to the end."""
        self.sequences.append(sequence)


@dataclass
class ParallelAnimation(AnimationSequence):
    """
    Execute animations in parallel (simultaneously).

    Attributes:
        sequences: List of sequences to execute simultaneously
    """

    sequences: List[AnimationSequence] = field(default_factory=list)

    def duration(self) -> float:
        if not self.sequences:
            return 0.0
        return max(seq.duration() for seq in self.sequences)

    def to_list(self) -> List[Any]:
        # Flatten parallel animations into a single entry
        flat = [seq.to_list() for seq in self.sequences]
        return [{'type': 'parallel', 'animations': flat}]

    def add(self, sequence: AnimationSequence) -> None:
        """Add a sequence to execute in parallel."""
        self.sequences.append(sequence)


@dataclass
class ShowAnimation(AnimationSequence):
    """
    Show/create an object animation.

    Attributes:
        object_id: ID of object to show
        object_type: Type of object
        parameters: Object creation parameters
        duration: Duration to display
    """

    object_id: str
    object_type: str
    parameters: dict = field(default_factory=dict)
    duration: float = 1.0

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'show',
            'object_id': self.object_id,
            'object_type': self.object_type,
            'parameters': self.parameters,
            'duration': self.duration
        }]


@dataclass
class TransformAnimation(AnimationSequence):
    """
    Transform one object into another.

    Attributes:
        from_id: Source object ID
        to_id: Target object ID
        duration: Transform duration
    """

    from_id: str
    to_id: str
    duration: float = 1.0

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'transform',
            'from_id': self.from_id,
            'to_id': self.to_id,
            'duration': self.duration
        }]


@dataclass
class FadeAnimation(AnimationSequence):
    """
    Fade an object in or out.

    Attributes:
        object_id: Object to fade
        fade_in: True for fade in, False for fade out
        duration: Fade duration
    """

    object_id: str
    fade_in: bool = True
    duration: float = 0.5

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'fade_in' if self.fade_in else 'fade_out',
            'object_id': self.object_id,
            'duration': self.duration
        }]


@dataclass
class MoveAnimation(AnimationSequence):
    """
    Move an object to a new position.

    Attributes:
        object_id: Object to move
        to_x: Target X position
        to_y: Target Y position
        duration: Move duration
    """

    object_id: str
    to_x: float
    to_y: float
    duration: float = 1.0

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'move',
            'object_id': self.object_id,
            'to': {'x': self.to_x, 'y': self.to_y},
            'duration': self.duration
        }]


@dataclass
class ScaleAnimation(AnimationSequence):
    """
    Scale an object.

    Attributes:
        object_id: Object to scale
        scale_factor: Scale multiplier
        duration: Scale duration
    """

    object_id: str
    scale_factor: float = 1.0
    duration: float = 0.5

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'scale',
            'object_id': self.object_id,
            'scale_factor': self.scale_factor,
            'duration': self.duration
        }]


@dataclass
class HighlightAnimation(AnimationSequence):
    """
    Highlight an object.

    Attributes:
        object_id: Object to highlight
        color: Highlight color
        scale: Scale factor for highlight effect
        duration: Highlight duration
    """

    object_id: str
    color: str = "YELLOW"
    scale: float = 1.2
    duration: float = 0.5

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'highlight',
            'object_id': self.object_id,
            'color': self.color,
            'scale': self.scale,
            'duration': self.duration
        }]


@dataclass
class RemoveAnimation(AnimationSequence):
    """
    Remove an object from the scene.

    Attributes:
        object_id: Object to remove
        duration: Removal animation duration (0 for instant)
    """

    object_id: str
    duration: float = 0.0

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{
            'type': 'remove',
            'object_id': self.object_id,
            'duration': self.duration
        }]


@dataclass
class WaitAnimation(AnimationSequence):
    """
    Wait/pause for a specified duration.

    Attributes:
        duration: Wait duration in seconds
    """

    duration: float = 1.0

    def duration(self) -> float:
        return self.duration

    def to_list(self) -> List[Any]:
        return [{'type': 'wait', 'duration': self.duration}]


# Convenience functions for creating animations

def show(object_id: str, object_type: str, **params) -> ShowAnimation:
    """Create a show animation."""
    return ShowAnimation(object_id=object_id, object_type=object_type, parameters=params)


def transform(from_id: str, to_id: str, duration: float = 1.0) -> TransformAnimation:
    """Create a transform animation."""
    return TransformAnimation(from_id=from_id, to_id=to_id, duration=duration)


def fade_in(object_id: str, duration: float = 0.5) -> FadeAnimation:
    """Create a fade-in animation."""
    return FadeAnimation(object_id=object_id, fade_in=True, duration=duration)


def fade_out(object_id: str, duration: float = 0.5) -> FadeAnimation:
    """Create a fade-out animation."""
    return FadeAnimation(object_id=object_id, fade_in=False, duration=duration)


def move(object_id: str, to_x: float, to_y: float, duration: float = 1.0) -> MoveAnimation:
    """Create a move animation."""
    return MoveAnimation(object_id=object_id, to_x=to_x, to_y=to_y, duration=duration)


def scale(object_id: str, scale_factor: float, duration: float = 0.5) -> ScaleAnimation:
    """Create a scale animation."""
    return ScaleAnimation(object_id=object_id, scale_factor=scale_factor, duration=duration)


def highlight(object_id: str, color: str = "YELLOW", scale: float = 1.2) -> HighlightAnimation:
    """Create a highlight animation."""
    return HighlightAnimation(object_id=object_id, color=color, scale=scale)


def remove(object_id: str, duration: float = 0.0) -> RemoveAnimation:
    """Create a remove animation."""
    return RemoveAnimation(object_id=object_id, duration=duration)


def wait(duration: float = 1.0) -> WaitAnimation:
    """Create a wait animation."""
    return WaitAnimation(duration=duration)


def serial(*sequences: AnimationSequence) -> SerialAnimation:
    """Create a serial animation from multiple sequences."""
    return SerialAnimation(list(sequences))


def parallel(*sequences: AnimationSequence) -> ParallelAnimation:
    """Create a parallel animation from multiple sequences."""
    return ParallelAnimation(list(sequences))


def delay(seconds: float) -> DelayAnimation:
    """Create a delay animation."""
    return DelayAnimation(delay=seconds)
