"""
Spacetime Layer - LAYER 2

Manages objects in time and space, detects conflicts, defines layouts.

This layer is responsible for:
- Spatial regions and collision detection
- Time windows and overlap detection
- Spacetime objects with conflict checking
- Timeline management
- Layout definitions
"""

from .objects import SpaceRegion, TimeWindow, SpacetimeObject
from .timelines import Timeline
from .layouts import Layout, Zone, LayoutTemplate
from .conflict_detection import ConflictDetector, ConflictReport

__all__ = [
    'SpaceRegion',
    'TimeWindow',
    'SpacetimeObject',
    'Timeline',
    'Layout',
    'Zone',
    'LayoutTemplate',
    'ConflictDetector',
    'ConflictReport',
]
