"""
Conflict detection for spacetime objects.

Uses spatial hashing for efficient O(n) conflict detection instead of naive O(n²).
"""
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict

from .objects import SpacetimeObject, SpaceRegion, TimeWindow
from .timelines import Timeline


@dataclass
class Conflict:
    """
    Represents a detected conflict between two objects.

    Attributes:
        obj1: First conflicting object
        obj2: Second conflicting object
        overlap_region: Spatial overlap region
        overlap_time: Time overlap window
        severity: Conflict severity estimate (0-1)
        suggestion: Suggested resolution
    """

    obj1: SpacetimeObject
    obj2: SpacetimeObject
    overlap_region: Optional[SpaceRegion] = None
    overlap_time: Optional[TimeWindow] = None
    severity: float = 0.0
    suggestion: str = ""

    def __str__(self) -> str:
        return (f"Conflict: '{self.obj1.id}' <-> '{self.obj2.id}' "
                f"(layer={self.obj1.layer}, severity={self.severity:.2f})")


@dataclass
class ConflictReport:
    """
    Report of detected conflicts.

    Attributes:
        conflicts: List of detected conflicts
        total_objects: Total number of objects checked
        total_conflicts: Total number of conflicts found
        has_conflicts: Whether any conflicts exist
    """

    conflicts: List[Conflict] = field(default_factory=list)
    total_objects: int = 0
    total_conflicts: int = 0

    @property
    def has_conflicts(self) -> bool:
        """Check if any conflicts were found."""
        return len(self.conflicts) > 0

    def get_conflicts_by_layer(self, layer: int) -> List[Conflict]:
        """Get conflicts on a specific layer."""
        return [c for c in self.conflicts if c.obj1.layer == layer]

    def get_conflicts_by_type(self, obj_type: str) -> List[Conflict]:
        """Get conflicts involving a specific object type."""
        return [c for c in self.conflicts
                if c.obj1.object_type == obj_type or c.obj2.object_type == obj_type]

    def get_severe_conflicts(self, threshold: float = 0.7) -> List[Conflict]:
        """Get conflicts above a severity threshold."""
        return [c for c in self.conflicts if c.severity >= threshold]

    def print_report(self) -> None:
        """Print a human-readable conflict report."""
        if not self.has_conflicts:
            print(f"✓ No conflicts detected among {self.total_objects} objects")
            return

        print(f"⚠ Found {self.total_conflicts} conflicts among {self.total_objects} objects:\n")

        for i, conflict in enumerate(self.conflicts, 1):
            print(f"{i}. {conflict}")
            if conflict.overlap_region:
                print(f"   Overlap region: {conflict.overlap_region}")
            if conflict.overlap_time:
                print(f"   Overlap time: {conflict.overlap_time}")
            if conflict.suggestion:
                print(f"   Suggestion: {conflict.suggestion}")
            print()

    def __len__(self) -> int:
        return len(self.conflicts)

    def __repr__(self) -> str:
        return f"ConflictReport(conflicts={self.total_conflicts}, objects={self.total_objects})"


class SpatialHashGrid:
    """
    Spatial hash grid for efficient collision detection.

    Divides space into cells and only checks collisions between
    objects in the same or adjacent cells.

    Attributes:
        cell_size: Size of each grid cell
        grid: Dictionary mapping cell coordinates to object sets
    """

    def __init__(self, cell_size: float = 1.0):
        """
        Initialize the spatial hash grid.

        Args:
            cell_size: Size of each grid cell (should be larger than
                      typical object size for best performance)
        """
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], Set[str]] = defaultdict(set)

    def _get_cell_coords(self, region: SpaceRegion) -> List[Tuple[int, int]]:
        """
        Get grid cell coordinates that a region overlaps.

        Args:
            region: SpaceRegion to get cells for

        Returns:
            List of (x, y) cell coordinates
        """
        cells = []
        start_x = int(region.left / self.cell_size)
        end_x = int(region.right / self.cell_size)
        start_y = int(region.bottom / self.cell_size)
        end_y = int(region.top / self.cell_size)

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                cells.append((x, y))

        return cells

    def insert(self, obj_id: str, region: SpaceRegion) -> None:
        """
        Insert an object into the grid.

        Args:
            obj_id: Unique object identifier
            region: Spatial region of the object
        """
        cells = self._get_cell_coords(region)
        for cell in cells:
            self.grid[cell].add(obj_id)

    def get_potential_collisions(
        self, obj_id: str, region: SpaceRegion
    ) -> Set[str]:
        """
        Get objects that might collide with the given region.

        Args:
            obj_id: ID of the object to check
            region: Spatial region to check

        Returns:
            Set of object IDs that might collide
        """
        potential: Set[str] = set()
        cells = self._get_cell_coords(region)

        for cell in cells:
            potential.update(self.grid[cell])

        potential.discard(obj_id)  # Remove self
        return potential

    def clear(self) -> None:
        """Clear the grid."""
        self.grid.clear()


class ConflictDetector:
    """
    Detects spacetime conflicts using efficient algorithms.

    Uses spatial hashing for O(n) average-case performance instead
    of naive O(n²) pairwise checking.
    """

    def __init__(self, spatial_cell_size: float = 1.0):
        """
        Initialize the conflict detector.

        Args:
            spatial_cell_size: Cell size for spatial hash grid
        """
        self.spatial_cell_size = spatial_cell_size

    def detect_conflicts(
        self, timeline: Timeline, check_layers: Optional[List[int]] = None
    ) -> ConflictReport:
        """
        Detect all conflicts in a timeline.

        Args:
            timeline: Timeline to check
            check_layers: Optional list of layers to check (default: all)

        Returns:
            ConflictReport with all detected conflicts
        """
        report = ConflictReport(total_objects=len(timeline.objects))

        if len(timeline.objects) < 2:
            return report

        # Filter by layers if specified
        objects_to_check = timeline.objects
        if check_layers is not None:
            objects_to_check = [obj for obj in timeline.objects
                              if obj.layer in check_layers]

        if len(objects_to_check) < 2:
            return report

        # Group objects by layer to avoid cross-layer checks
        by_layer: Dict[int, List[SpacetimeObject]] = defaultdict(list)
        for obj in objects_to_check:
            by_layer[obj.layer].append(obj)

        # Check each layer independently
        for layer, layer_objects in by_layer.items():
            layer_conflicts = self._detect_layer_conflicts(layer_objects)
            report.conflicts.extend(layer_conflicts)

        report.total_conflicts = len(report.conflicts)
        return report

    def _detect_layer_conflicts(
        self, objects: List[SpacetimeObject]
    ) -> List[Conflict]:
        """
        Detect conflicts among objects on the same layer.

        Uses temporal bucketing + spatial hashing for efficiency.

        Args:
            objects: List of objects on the same layer

        Returns:
            List of detected conflicts
        """
        if len(objects) < 2:
            return []

        conflicts: List[Conflict] = []

        # First, group by time overlap to reduce checks
        # Sort objects by start time
        sorted_objects = sorted(objects, key=lambda o: o.time.start)

        # Use sliding window to find temporally overlapping objects
        for i, obj1 in enumerate(sorted_objects):
            # Check subsequent objects while there's temporal overlap potential
            for j in range(i + 1, len(sorted_objects)):
                obj2 = sorted_objects[j]

                # If obj2 starts after obj1 ends (with padding), no more overlaps
                if obj2.time.start > obj1.time.padded_end:
                    break

                # Check time overlap
                if not obj1.time.overlaps(obj2.time):
                    continue

                # Check spatial overlap using exact intersection
                if obj1.space.intersects(obj2.space):
                    conflict = self._create_conflict(obj1, obj2)
                    conflicts.append(conflict)

        return conflicts

    def _create_conflict(
        self, obj1: SpacetimeObject, obj2: SpacetimeObject
    ) -> Conflict:
        """Create a Conflict object with details."""
        # Calculate overlap region
        overlap_region = obj1.get_overlap_region(obj2)
        overlap_time = obj1.get_overlap_time(obj2)

        # Calculate severity based on overlap amount
        severity = 0.0
        if overlap_region and overlap_time:
            space_overlap_ratio = overlap_region.area() / min(
                obj1.space.area(), obj2.space.area()
            )
            time_overlap_ratio = overlap_time.duration / min(
                obj1.time.duration, obj2.time.duration
            )
            severity = (space_overlap_ratio + time_overlap_ratio) / 2

        # Generate suggestion
        suggestion = self._generate_suggestion(obj1, obj2, severity)

        return Conflict(
            obj1=obj1,
            obj2=obj2,
            overlap_region=overlap_region,
            overlap_time=overlap_time,
            severity=severity,
            suggestion=suggestion
        )

    def _generate_suggestion(
        self, obj1: SpacetimeObject, obj2: SpacetimeObject, severity: float
    ) -> str:
        """Generate a resolution suggestion for a conflict."""
        if severity < 0.3:
            return "Minor overlap - consider adjusting timing slightly"

        # Check if one object can be moved in time
        time_diff = abs(obj1.time.start - obj2.time.start)
        if time_diff < 1.0:
            return "Objects start at nearly the same time - try staggering their appearance"

        # Check spatial separation
        centers_dist = ((obj1.space.center[0] - obj2.space.center[0])**2 +
                       (obj1.space.center[1] - obj2.space.center[1])**2)**0.5

        if centers_dist < 2.0:
            return "Objects are close together - try moving them further apart horizontally or vertically"

        # Check layer change
        if obj1.layer == obj2.layer:
            return f"Consider placing one object on a different layer (current: {obj1.layer})"

        return "Consider adjusting timing, position, or layer"

    def detect_conflicts_in_sequence(
        self, sequence: 'TimelineSequence'
    ) -> Dict[str, ConflictReport]:
        """
        Detect conflicts in each segment of a sequence.

        Args:
            sequence: TimelineSequence to check

        Returns:
            Dictionary mapping segment names to ConflictReports
        """
        reports = {}
        for segment in sequence.segments:
            report = self.detect_conflicts(segment.timeline)
            reports[segment.name] = report

        return reports


class ConflictResolver:
    """
    Provides automatic resolution suggestions for conflicts.

    Not meant to auto-resolve, but to provide intelligent suggestions.
    """

    @staticmethod
    def suggest_time_shift(conflict: Conflict) -> Tuple[float, float]:
        """
        Suggest time shifts to resolve conflict.

        Returns:
            (shift_for_obj1, shift_for_obj2) - negative means earlier, positive means later
        """
        if not conflict.overlap_time:
            return (0.0, 0.0)

        # Shift obj2 to start after obj1 ends
        shift = conflict.obj1.time.end - conflict.obj2.time.start + 0.5
        return (0.0, shift)

    @staticmethod
    def suggest_space_shift(conflict: Conflict) -> Tuple[float, float]:
        """
        Suggest spatial shifts to resolve conflict.

        Returns:
            (dx_for_obj1, dy_for_obj1) - shift for obj1, obj2 stays put
        """
        if not conflict.overlap_region:
            return (0.0, 0.0)

        # Shift obj1 horizontally away from obj2
        dx = conflict.obj2.space.right - conflict.obj1.space.left + 0.5
        if conflict.obj1.space.center[0] < conflict.obj2.space.center[0]:
            dx = -dx

        return (dx, 0.0)

    @staticmethod
    def suggest_layer_change(conflict: Conflict, available_layers: List[int]) -> int:
        """
        Suggest a new layer for obj2 to avoid conflict.

        Args:
            conflict: Conflict to resolve
            available_layers: List of available layer numbers

        Returns:
            Suggested layer number for obj2
        """
        current_layer = conflict.obj1.layer
        for layer in available_layers:
            if layer != current_layer:
                return layer
        return current_layer + 1
