"""
Layout definitions and zones for spacetime objects.

Provides predefined layouts and spatial zones for common video compositions.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

from .objects import SpaceRegion, SpacetimeObject, TimeWindow


class Position(Enum):
    """Standard positions in a scene."""
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"


@dataclass
class Zone:
    """
    A named spatial zone within a layout.

    Zones provide convenient named regions for positioning objects.

    Attributes:
        name: Zone identifier
        region: Spatial region of the zone
        default_layer: Default layer for objects in this zone
    """

    name: str
    region: SpaceRegion
    default_layer: int = 0

    def create_object(
        self,
        id: str,
        start_time: float,
        duration: float,
        width: Optional[float] = None,
        height: Optional[float] = None,
        layer: Optional[int] = None,
        **metadata
    ) -> SpacetimeObject:
        """
        Create a spacetime object positioned in this zone.

        Args:
            id: Object identifier
            start_time: Start time
            duration: Duration
            width: Object width (defaults to zone width)
            height: Object height (defaults to zone height)
            layer: Layer number (defaults to zone default)
            **metadata: Additional metadata

        Returns:
            SpacetimeObject positioned in the zone
        """
        if width is None:
            width = self.region.width * 0.9  # 90% of zone width
        if height is None:
            height = self.region.height * 0.9  # 90% of zone height
        if layer is None:
            layer = self.default_layer

        # Center the object in the zone
        x = self.region.center[0] - width / 2
        y = self.region.center[1] - height / 2

        return SpacetimeObject(
            id=id,
            space=SpaceRegion(x=x, y=y, width=width, height=height),
            time=TimeWindow(start=start_time, end=start_time + duration),
            layer=layer,
            metadata={'zone': self.name, **metadata}
        )


@dataclass
class Layout:
    """
    A layout defines spatial zones for scene composition.

    Layouts provide reusable zone configurations for common video patterns.

    Attributes:
        name: Layout identifier
        zones: Dictionary of zone name to Zone
    """

    name: str
    zones: Dict[str, Zone] = field(default_factory=dict)

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the layout."""
        self.zones[zone.name] = zone

    def get_zone(self, name: str) -> Optional[Zone]:
        """Get a zone by name."""
        return self.zones.get(name)

    def create_object_in_zone(
        self,
        zone_name: str,
        id: str,
        start_time: float,
        duration: float,
        **kwargs
    ) -> Optional[SpacetimeObject]:
        """
        Create an object in a specific zone.

        Args:
            zone_name: Name of the zone
            id: Object identifier
            start_time: Start time
            duration: Duration
            **kwargs: Additional arguments passed to Zone.create_object

        Returns:
            SpacetimeObject or None if zone not found
        """
        zone = self.get_zone(zone_name)
        if zone is None:
            return None
        return zone.create_object(id, start_time, duration, **kwargs)

    @property
    def bounds(self) -> SpaceRegion:
        """Get the bounding region of all zones."""
        if not self.zones:
            return SpaceRegion(x=0, y=0, width=0, height=0)

        min_x = min(z.region.left for z in self.zones.values())
        max_x = max(z.region.right for z in self.zones.values())
        min_y = min(z.region.bottom for z in self.zones.values())
        max_y = max(z.region.top for z in self.zones.values())

        return SpaceRegion(
            x=min_x,
            y=min_y,
            width=max_x - min_x,
            height=max_y - min_y
        )


class LayoutTemplate:
    """
    Predefined layout templates for common video compositions.

    Provides static methods that return configured Layout objects.
    """

    @staticmethod
    def fullscreen() -> Layout:
        """
        Single fullscreen zone.

        Useful for titles, single content, etc.
        """
        layout = Layout(name="fullscreen")
        layout.add_zone(Zone(
            name="main",
            region=SpaceRegion(x=-7, y=-4, width=14, height=8),
            default_layer=0
        ))
        return layout

    @staticmethod
    def split_horizontal() -> Layout:
        """
        Split screen horizontally (left and right).

        Useful for comparisons, before/after, etc.
        """
        layout = Layout(name="split_horizontal")

        # Left zone
        layout.add_zone(Zone(
            name="left",
            region=SpaceRegion(x=-7, y=-4, width=6.5, height=8),
            default_layer=0
        ))

        # Right zone
        layout.add_zone(Zone(
            name="right",
            region=SpaceRegion(x=0.5, y=-4, width=6.5, height=8),
            default_layer=0
        ))

        return layout

    @staticmethod
    def split_vertical() -> Layout:
        """
        Split screen vertically (top and bottom).

        Useful for code + explanation, etc.
        """
        layout = Layout(name="split_vertical")

        # Top zone
        layout.add_zone(Zone(
            name="top",
            region=SpaceRegion(x=-7, y=0.5, width=14, height=3.5),
            default_layer=0
        ))

        # Bottom zone
        layout.add_zone(Zone(
            name="bottom",
            region=SpaceRegion(x=-7, y=-4, width=14, height=3.5),
            default_layer=0
        ))

        return layout

    @staticmethod
    def thirds() -> Layout:
        """
        Divide screen into three vertical sections.

        Useful for showing process flow, etc.
        """
        layout = Layout(name="thirds")

        width = 14 / 3 - 0.2  # With small gap

        # Left third
        layout.add_zone(Zone(
            name="left",
            region=SpaceRegion(x=-7, y=-4, width=width, height=8),
            default_layer=0
        ))

        # Middle third
        layout.add_zone(Zone(
            name="center",
            region=SpaceRegion(x=-7 + width + 0.3, y=-4, width=width, height=8),
            default_layer=0
        ))

        # Right third
        layout.add_zone(Zone(
            name="right",
            region=SpaceRegion(x=-7 + 2 * (width + 0.3), y=-4, width=width, height=8),
            default_layer=0
        ))

        return layout

    @staticmethod
    def focus_with_sidebar() -> Layout:
        """
        Main content area with sidebar on the right.

        Useful for code + explanation, diagram + notes, etc.
        """
        layout = Layout(name="focus_with_sidebar")

        # Main area (left 2/3)
        layout.add_zone(Zone(
            name="main",
            region=SpaceRegion(x=-7, y=-4, width=9, height=8),
            default_layer=0
        ))

        # Sidebar (right 1/3)
        layout.add_zone(Zone(
            name="sidebar",
            region=SpaceRegion(x=2.5, y=-4, width=4, height=8),
            default_layer=0
        ))

        return layout

    @staticmethod
    def title_with_content() -> Layout:
        """
        Title bar at top with main content below.

        Useful for titled sections, chapter headers, etc.
        """
        layout = Layout(name="title_with_content")

        # Title bar (top)
        layout.add_zone(Zone(
            name="title",
            region=SpaceRegion(x=-7, y=3, width=14, height=1),
            default_layer=0
        ))

        # Main content (below)
        layout.add_zone(Zone(
            name="content",
            region=SpaceRegion(x=-7, y=-4, width=14, height=6.5),
            default_layer=0
        ))

        return layout

    @staticmethod
    def four_quadrants() -> Layout:
        """
        Divide screen into four quadrants.

        Useful for comparisons, multiple related items, etc.
        """
        layout = Layout(name="four_quadrants")

        half_width = 6.8
        half_height = 3.8

        # Top-left
        layout.add_zone(Zone(
            name="top_left",
            region=SpaceRegion(x=-7, y=0.2, width=half_width, height=half_height),
            default_layer=0
        ))

        # Top-right
        layout.add_zone(Zone(
            name="top_right",
            region=SpaceRegion(x=-0.2, y=0.2, width=half_width, height=half_height),
            default_layer=0
        ))

        # Bottom-left
        layout.add_zone(Zone(
            name="bottom_left",
            region=SpaceRegion(x=-7, y=-4.2, width=half_width, height=half_height),
            default_layer=0
        ))

        # Bottom-right
        layout.add_zone(Zone(
            name="bottom_right",
            region=SpaceRegion(x=-0.2, y=-4.2, width=half_width, height=half_height),
            default_layer=0
        ))

        return layout

    @staticmethod
    def code_with_explanation() -> Layout:
        """
        Code display at top with explanation area below.

        Specifically designed for CS educational content.
        """
        layout = Layout(name="code_with_explanation")

        # Code area (top, larger)
        layout.add_zone(Zone(
            name="code",
            region=SpaceRegion(x=-7, y=0, width=14, height=3.5),
            default_layer=0
        ))

        # Explanation area (bottom)
        layout.add_zone(Zone(
            name="explanation",
            region=SpaceRegion(x=-7, y=-4, width=14, height=3.5),
            default_layer=0
        ))

        return layout

    @staticmethod
    def memory_layout() -> Layout:
        """
        Specialized layout for memory visualization.

        Main memory area with registers/pointers on the side.
        """
        layout = Layout(name="memory_layout")

        # Memory visualization (center)
        layout.add_zone(Zone(
            name="memory",
            region=SpaceRegion(x=-3, y=-4, width=6, height=8),
            default_layer=0
        ))

        # Registers (left)
        layout.add_zone(Zone(
            name="registers",
            region=SpaceRegion(x=-7, y=-2, width=3, height=4),
            default_layer=0
        ))

        # Annotations (right)
        layout.add_zone(Zone(
            name="annotations",
            region=SpaceRegion(x=3.5, y=-2, width=3, height=4),
            default_layer=0
        ))

        return layout

    @staticmethod
    def process_diagram() -> Layout:
        """
        Layout for process/state diagram visualization.

        Central diagram with label areas around it.
        """
        layout = Layout(name="process_diagram")

        # Central diagram
        layout.add_zone(Zone(
            name="diagram",
            region=SpaceRegion(x=-4, y=-3, width=8, height=6),
            default_layer=0
        ))

        # Labels (right side)
        layout.add_zone(Zone(
            name="labels",
            region=SpaceRegion(x=4.5, y=-3, width=2, height=6),
            default_layer=0
        ))

        # Title (top)
        layout.add_zone(Zone(
            name="title",
            region=SpaceRegion(x=-7, y=3.5, width=14, height=0.8),
            default_layer=0
        ))

        return layout

    @staticmethod
    def pipeline() -> Layout:
        """
        Pipeline/flow visualization layout.

        Horizontal flow with annotation areas.
        """
        layout = Layout(name="pipeline")

        # Pipeline stages (horizontal)
        layout.add_zone(Zone(
            name="pipeline",
            region=SpaceRegion(x=-6, y=-1.5, width=12, height=3),
            default_layer=0
        ))

        # Labels below
        layout.add_zone(Zone(
            name="stage_labels",
            region=SpaceRegion(x=-6, y=-3.5, width=12, height=1),
            default_layer=0
        ))

        # Explanation (bottom)
        layout.add_zone(Zone(
            name="explanation",
            region=SpaceRegion(x=-7, y=-4.5, width=14, height=0.5),
            default_layer=0
        ))

        return layout


def create_zone_at_position(
    name: str,
    position: Position,
    width: float = 3.0,
    height: float = 2.0,
    offset: float = 3.0,
    default_layer: int = 0
) -> Zone:
    """
    Create a zone at a standard position.

    Args:
        name: Zone name
        position: Position enum value
        width: Zone width
        height: Zone height
        offset: Offset from center for edge positions
        default_layer: Default layer

    Returns:
        Zone at the specified position
    """
    if position == Position.CENTER:
        region = SpaceRegion(
            x=-width / 2,
            y=-height / 2,
            width=width,
            height=height
        )
    elif position == Position.LEFT:
        region = SpaceRegion(
            x=-offset - width / 2,
            y=-height / 2,
            width=width,
            height=height
        )
    elif position == Position.RIGHT:
        region = SpaceRegion(
            x=offset - width / 2,
            y=-height / 2,
            width=width,
            height=height
        )
    elif position == Position.TOP:
        region = SpaceRegion(
            x=-width / 2,
            y=offset - height / 2,
            width=width,
            height=height
        )
    elif position == Position.BOTTOM:
        region = SpaceRegion(
            x=-width / 2,
            y=-offset - height / 2,
            width=width,
            height=height
        )
    elif position == Position.TOP_LEFT:
        region = SpaceRegion(
            x=-offset - width / 2,
            y=offset - height / 2,
            width=width,
            height=height
        )
    elif position == Position.TOP_RIGHT:
        region = SpaceRegion(
            x=offset - width / 2,
            y=offset - height / 2,
            width=width,
            height=height
        )
    elif position == Position.BOTTOM_LEFT:
        region = SpaceRegion(
            x=-offset - width / 2,
            y=-offset - height / 2,
            width=width,
            height=height
        )
    elif position == Position.BOTTOM_RIGHT:
        region = SpaceRegion(
            x=offset - width / 2,
            y=-offset - height / 2,
            width=width,
            height=height
        )
    else:
        raise ValueError(f"Unknown position: {position}")

    return Zone(name=name, region=region, default_layer=default_layer)
