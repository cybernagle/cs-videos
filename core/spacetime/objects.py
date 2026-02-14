"""
Core spacetime objects - SpaceRegion, TimeWindow, SpacetimeObject

These are the fundamental data structures for the spacetime layer.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class SpaceRegion:
    """
    A region in 2D space with collision detection.

    Uses AABB (Axis-Aligned Bounding Box) collision detection.

    Attributes:
        x: Left coordinate (can be negative, center is 0)
        y: Bottom coordinate (can be negative, center is 0)
        width: Width of the region
        height: Height of the region
    """

    x: float
    y: float
    width: float
    height: float

    def __post_init__(self):
        """Validate dimensions are positive."""
        if self.width <= 0:
            raise ValueError(f"Width must be positive, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"Height must be positive, got {self.height}")

    @property
    def left(self) -> float:
        """Left boundary."""
        return self.x

    @property
    def right(self) -> float:
        """Right boundary."""
        return self.x + self.width

    @property
    def bottom(self) -> float:
        """Bottom boundary."""
        return self.y

    @property
    def top(self) -> float:
        """Top boundary."""
        return self.y + self.height

    @property
    def center(self) -> tuple[float, float]:
        """Center point (x, y)."""
        return (self.x + self.width / 2, self.y + self.height / 2)

    def intersects(self, other: 'SpaceRegion') -> bool:
        """
        AABB collision detection.

        Two rectangles intersect if and only if they overlap on both axes.

        Args:
            other: Another SpaceRegion to check intersection with

        Returns:
            True if regions intersect, False otherwise
        """
        return not (
            self.right < other.left or
            other.right < self.left or
            self.top < other.bottom or
            other.top < self.bottom
        )

    def contains(self, other: 'SpaceRegion') -> bool:
        """
        Check if this region fully contains another region.

        Args:
            other: Another SpaceRegion to check

        Returns:
            True if this region fully contains other
        """
        return (self.left <= other.left and
                self.right >= other.right and
                self.bottom <= other.bottom and
                self.top >= other.top)

    def area(self) -> float:
        """Calculate area of the region."""
        return self.width * self.height

    def expanded(self, padding: float) -> 'SpaceRegion':
        """
        Create a new region expanded by padding on all sides.

        Args:
            padding: Amount to expand (can be negative to shrink)

        Returns:
            New SpaceRegion with expanded boundaries
        """
        return SpaceRegion(
            x=self.x - padding,
            y=self.y - padding,
            width=self.width + 2 * padding,
            height=self.height + 2 * padding
        )

    def shifted(self, dx: float, dy: float) -> 'SpaceRegion':
        """
        Create a new region shifted by dx, dy.

        Args:
            dx: Horizontal shift
            dy: Vertical shift

        Returns:
            New SpaceRegion shifted by specified amounts
        """
        return SpaceRegion(
            x=self.x + dx,
            y=self.y + dy,
            width=self.width,
            height=self.height
        )

    def __str__(self) -> str:
        return f"SpaceRegion(x={self.x:.2f}, y={self.y:.2f}, w={self.width:.2f}, h={self.height:.2f})"


@dataclass
class TimeWindow:
    """
    A time interval with overlap detection.

    Attributes:
        start: Start time in seconds
        end: End time in seconds
        padding: Optional padding for overlap checking (default 0.5s)
    """

    start: float
    end: float
    padding: float = 0.5

    def __post_init__(self):
        """Validate time window."""
        if self.end < self.start:
            raise ValueError(f"End ({self.end}) must be >= start ({self.start})")
        if self.padding < 0:
            raise ValueError(f"Padding must be non-negative, got {self.padding}")

    @property
    def duration(self) -> float:
        """Duration of the time window."""
        return self.end - self.start

    @property
    def padded_start(self) -> float:
        """Start time with padding applied."""
        return self.start - self.padding

    @property
    def padded_end(self) -> float:
        """End time with padding applied."""
        return self.end + self.padding

    def overlaps(self, other: 'TimeWindow') -> bool:
        """
        Check if two time windows overlap (considering padding).

        Args:
            other: Another TimeWindow to check

        Returns:
            True if windows overlap, False otherwise
        """
        return not (self.padded_end < other.start or
                   other.padded_end < self.start)

    def contains(self, time: float) -> bool:
        """
        Check if a time point is within this window.

        Args:
            time: Time point to check

        Returns:
            True if time is within window
        """
        return self.start <= time <= self.end

    def intersection(self, other: 'TimeWindow') -> Optional['TimeWindow']:
        """
        Get the intersection of two time windows.

        Args:
            other: Another TimeWindow

        Returns:
            New TimeWindow representing intersection, or None if no overlap
        """
        if not self.overlaps(other):
            return None

        return TimeWindow(
            start=max(self.start, other.start),
            end=min(self.end, other.end)
        )

    def extended(self, extra_start: float = 0, extra_end: float = 0) -> 'TimeWindow':
        """
        Create a new time window with extended boundaries.

        Args:
            extra_start: Time to add to start (can be negative)
            extra_end: Time to add to end (can be negative)

        Returns:
            New TimeWindow with extended boundaries
        """
        return TimeWindow(
            start=self.start + extra_start,
            end=self.end + extra_end,
            padding=self.padding
        )

    def __str__(self) -> str:
        return f"TimeWindow({self.start:.2f}s - {self.end:.2f}s, padding={self.padding:.2f}s)"


@dataclass
class SpacetimeObject:
    """
    An object existing in both space and time.

    This is the core abstraction for objects in a video scene.
    Each object has a spatial region, temporal window, and optional layer.

    Attributes:
        id: Unique identifier for the object
        space: Spatial region the object occupies
        time: Time window the object exists in
        layer: Z-index layer (objects on same layer can conflict)
        metadata: Optional metadata (type, content, etc.)
    """

    id: str
    space: SpaceRegion
    time: TimeWindow
    layer: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def object_type(self) -> str:
        """Get the object type from metadata."""
        return self.metadata.get('type', 'unknown')

    def conflicts_with(self, other: 'SpacetimeObject') -> bool:
        """
        Check if this object conflicts with another.

        Conflict occurs when:
        1. Time windows overlap
        2. Space regions intersect
        3. Objects are on the same layer

        Args:
            other: Another SpacetimeObject

        Returns:
            True if objects conflict, False otherwise
        """
        return (self.time.overlaps(other.time) and
                self.space.intersects(other.space) and
                self.layer == other.layer)

    def get_overlap_region(self, other: 'SpacetimeObject') -> Optional[SpaceRegion]:
        """
        Get the spatial overlap region with another object.

        Args:
            other: Another SpacetimeObject

        Returns:
            SpaceRegion representing overlap, or None if no overlap
        """
        if not self.space.intersects(other.space):
            return None

        overlap_left = max(self.space.left, other.space.left)
        overlap_right = min(self.space.right, other.space.right)
        overlap_bottom = max(self.space.bottom, other.space.bottom)
        overlap_top = min(self.space.top, other.space.top)

        return SpaceRegion(
            x=overlap_left,
            y=overlap_bottom,
            width=overlap_right - overlap_left,
            height=overlap_top - overlap_bottom
        )

    def get_overlap_time(self, other: 'SpacetimeObject') -> Optional[TimeWindow]:
        """
        Get the time overlap with another object.

        Args:
            other: Another SpacetimeObject

        Returns:
            TimeWindow representing overlap, or None if no overlap
        """
        return self.time.intersection(other.time)

    def __str__(self) -> str:
        return f"SpacetimeObject(id='{self.id}', type='{self.object_type}', layer={self.layer})"

    def __repr__(self) -> str:
        return (f"SpacetimeObject(id='{self.id}', space={self.space}, "
                f"time={self.time}, layer={self.layer})")


# Convenience functions for creating common objects

def create_centered_object(
    id: str,
    width: float,
    height: float,
    start_time: float,
    duration: float,
    layer: int = 0,
    **metadata
) -> SpacetimeObject:
    """
    Create a spacetime object centered at origin.

    Args:
        id: Object identifier
        width: Object width
        height: Object height
        start_time: Start time
        duration: Duration
        layer: Z-index layer
        **metadata: Additional metadata

    Returns:
        SpacetimeObject centered at origin
    """
    return SpacetimeObject(
        id=id,
        space=SpaceRegion(
            x=-width / 2,
            y=-height / 2,
            width=width,
            height=height
        ),
        time=TimeWindow(start=start_time, end=start_time + duration),
        layer=layer,
        metadata=metadata
    )


def create_left_object(
    id: str,
    width: float,
    height: float,
    start_time: float,
    duration: float,
    offset: float = -3.0,
    layer: int = 0,
    **metadata
) -> SpacetimeObject:
    """Create a spacetime object positioned on the left side."""
    return SpacetimeObject(
        id=id,
        space=SpaceRegion(
            x=offset - width / 2,
            y=-height / 2,
            width=width,
            height=height
        ),
        time=TimeWindow(start=start_time, end=start_time + duration),
        layer=layer,
        metadata=metadata
    )


def create_right_object(
    id: str,
    width: float,
    height: float,
    start_time: float,
    duration: float,
    offset: float = 3.0,
    layer: int = 0,
    **metadata
) -> SpacetimeObject:
    """Create a spacetime object positioned on the right side."""
    return SpacetimeObject(
        id=id,
        space=SpaceRegion(
            x=offset - width / 2,
            y=-height / 2,
            width=width,
            height=height
        ),
        time=TimeWindow(start=start_time, end=start_time + duration),
        layer=layer,
        metadata=metadata
    )
