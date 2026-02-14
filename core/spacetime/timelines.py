"""
Timeline management for spacetime objects.

Timelines manage collections of spacetime objects and provide
query capabilities for temporal organization.
"""
from typing import List, Optional, Callable
from dataclasses import dataclass, field

from .objects import SpacetimeObject, TimeWindow


@dataclass
class Timeline:
    """
    A timeline manages a collection of spacetime objects.

    Timelines provide methods for adding, removing, and querying objects.

    Attributes:
        name: Optional name for the timeline
        objects: List of spacetime objects on this timeline
    """

    name: Optional[str] = None
    objects: List[SpacetimeObject] = field(default_factory=list)

    @property
    def duration(self) -> float:
        """Get the total duration of the timeline."""
        if not self.objects:
            return 0.0
        return max(obj.time.end for obj in self.objects)

    @property
    def start_time(self) -> float:
        """Get the earliest start time on the timeline."""
        if not self.objects:
            return 0.0
        return min(obj.time.start for obj in self.objects)

    def add(self, obj: SpacetimeObject) -> None:
        """
        Add a spacetime object to the timeline.

        Args:
            obj: SpacetimeObject to add
        """
        self.objects.append(obj)

    def remove(self, obj_id: str) -> bool:
        """
        Remove an object by ID.

        Args:
            obj_id: ID of object to remove

        Returns:
            True if object was removed, False if not found
        """
        for i, obj in enumerate(self.objects):
            if obj.id == obj_id:
                self.objects.pop(i)
                return True
        return False

    def get(self, obj_id: str) -> Optional[SpacetimeObject]:
        """
        Get an object by ID.

        Args:
            obj_id: ID of object to retrieve

        Returns:
            SpacetimeObject if found, None otherwise
        """
        for obj in self.objects:
            if obj.id == obj_id:
                return obj
        return None

    def get_objects_at_time(self, time: float) -> List[SpacetimeObject]:
        """
        Get all objects active at a specific time.

        Args:
            time: Time point to query

        Returns:
            List of SpacetimeObjects active at the given time
        """
        return [obj for obj in self.objects if obj.time.contains(time)]

    def get_objects_in_layer(self, layer: int) -> List[SpacetimeObject]:
        """
        Get all objects in a specific layer.

        Args:
            layer: Layer number

        Returns:
            List of SpacetimeObjects in the layer
        """
        return [obj for obj in self.objects if obj.layer == layer]

    def get_objects_by_type(self, obj_type: str) -> List[SpacetimeObject]:
        """
        Get all objects of a specific type.

        Args:
            obj_type: Type string from metadata

        Returns:
            List of SpacetimeObjects of the specified type
        """
        return [obj for obj in self.objects if obj.object_type == obj_type]

    def get_objects_in_time_range(
        self, start: float, end: float
    ) -> List[SpacetimeObject]:
        """
        Get objects active within a time range.

        Args:
            start: Range start time
            end: Range end time

        Returns:
            List of SpacetimeObjects active in the range
        """
        window = TimeWindow(start=start, end=end)
        return [obj for obj in self.objects if obj.time.overlaps(window)]

    def filter(self, predicate: Callable[[SpacetimeObject], bool]) -> 'Timeline':
        """
        Create a new timeline with objects matching a predicate.

        Args:
            predicate: Function that returns True for objects to include

        Returns:
            New Timeline with filtered objects
        """
        filtered = [obj for obj in self.objects if predicate(obj)]
        return Timeline(name=f"{self.name}_filtered", objects=filtered)

    def sort_by_start_time(self) -> 'Timeline':
        """
        Create a new timeline with objects sorted by start time.

        Returns:
            New Timeline with sorted objects
        """
        sorted_objects = sorted(self.objects, key=lambda obj: obj.time.start)
        return Timeline(name=f"{self.name}_sorted", objects=sorted_objects)

    def merge(self, other: 'Timeline') -> 'Timeline':
        """
        Merge another timeline into this one.

        Args:
            other: Another Timeline to merge

        Returns:
            New Timeline containing objects from both timelines
        """
        merged_objects = self.objects + other.objects
        return Timeline(
            name=f"{self.name}_merged",
            objects=merged_objects
        )

    def copy(self) -> 'Timeline':
        """
        Create a shallow copy of the timeline.

        Returns:
            New Timeline with same objects
        """
        return Timeline(name=f"{self.name}_copy", objects=self.objects.copy())

    def __len__(self) -> int:
        """Get the number of objects on the timeline."""
        return len(self.objects)

    def __iter__(self):
        """Iterate over objects on the timeline."""
        return iter(self.objects)

    def __repr__(self) -> str:
        return f"Timeline(name='{self.name}', objects={len(self.objects)}, duration={self.duration:.2f}s)"


@dataclass
class TimelineSegment:
    """
    A segment of a timeline with time bounds.

    Useful for representing chapters or sections of a video.

    Attributes:
        name: Segment name
        timeline: The timeline for this segment
        start_offset: Global start time offset
    """

    name: str
    timeline: Timeline
    start_offset: float = 0.0

    @property
    def end_offset(self) -> float:
        """Get the end time offset."""
        return self.start_offset + self.timeline.duration

    @property
    def time_window(self) -> TimeWindow:
        """Get the time window for this segment."""
        return TimeWindow(
            start=self.start_offset,
            end=self.end_offset
        )

    def contains_time(self, time: float) -> bool:
        """Check if a global time is within this segment."""
        return self.start_offset <= time <= self.end_offset

    def to_local_time(self, global_time: float) -> float:
        """Convert global time to local segment time."""
        return global_time - self.start_offset

    def to_global_time(self, local_time: float) -> float:
        """Convert local segment time to global time."""
        return local_time + self.start_offset


@dataclass
class TimelineSequence:
    """
    A sequence of timeline segments.

    Useful for representing full videos with multiple chapters.

    Attributes:
        name: Sequence name
        segments: List of TimelineSegments in order
    """

    name: str
    segments: List[TimelineSegment] = field(default_factory=list)

    @property
    def duration(self) -> float:
        """Get total duration of all segments."""
        if not self.segments:
            return 0.0
        return max(seg.end_offset for seg in self.segments)

    def add_segment(self, segment: TimelineSegment) -> None:
        """Add a segment to the sequence."""
        self.segments.append(segment)

    def get_segment_at_time(self, time: float) -> Optional[TimelineSegment]:
        """Get the segment active at a given global time."""
        for segment in self.segments:
            if segment.contains_time(time):
                return segment
        return None

    def get_all_timelines(self) -> List[Timeline]:
        """Get all timelines from all segments."""
        return [seg.timeline for seg in self.segments]

    def merge_all(self) -> Timeline:
        """
        Merge all segment timelines into one.

        Offsets are applied to object time windows.

        Returns:
            Single merged Timeline
        """
        merged = Timeline(name=f"{self.name}_merged")
        for segment in self.segments:
            for obj in segment.timeline.objects:
                # Create new object with adjusted time
                adjusted_obj = SpacetimeObject(
                    id=f"{segment.name}_{obj.id}",
                    space=obj.space,
                    time=TimeWindow(
                        start=obj.time.start + segment.start_offset,
                        end=obj.time.end + segment.start_offset,
                        padding=obj.time.padding
                    ),
                    layer=obj.layer,
                    metadata=obj.metadata.copy()
                )
                adjusted_obj.metadata['segment'] = segment.name
                merged.add(adjusted_obj)
        return merged

    def __len__(self) -> int:
        return len(self.segments)

    def __repr__(self) -> str:
        return f"TimelineSequence(name='{self.name}', segments={len(self.segments)}, duration={self.duration:.2f}s)"
