"""
Animation orchestration and direction.

The Director is responsible for converting spacetime timelines
into actual Manim animations and executing them in the correct order.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from abc import ABC, abstractmethod

from ..spacetime.objects import SpacetimeObject, TimeWindow
from ..spacetime.timelines import Timeline
from ..business.story import Story


@dataclass
class AnimationPlan:
    """
    A plan for executing animations on a Manim scene.

    Contains sorted animation instructions with proper timing.

    Attributes:
        animations: List of animation instructions in execution order
        total_duration: Total duration of all animations
    """

    animations: List['AnimationInstruction'] = field(default_factory=list)
    total_duration: float = 0.0

    def add_animation(self, animation: 'AnimationInstruction') -> None:
        """Add an animation to the plan."""
        self.animations.append(animation)
        self.total_duration = max(
            self.total_duration,
            animation.start_time + animation.duration
        )

    def sort_by_time(self) -> None:
        """Sort animations by start time."""
        self.animations.sort(key=lambda a: a.start_time)


@dataclass
class AnimationInstruction:
    """
    A single animation instruction.

    Attributes:
        object_id: ID of the spacetime object
        action_type: Type of animation (show, transform, fade, etc.)
        start_time: When to start this animation
        duration: Animation duration
        parameters: Animation-specific parameters
    """

    object_id: str
    action_type: str
    start_time: float
    duration: float
    parameters: Dict[str, Any] = field(default_factory=dict)

    @property
    def end_time(self) -> float:
        """Get the end time of this animation."""
        return self.start_time + self.duration


class Director:
    """
    Orchestrates animation execution from spacetime timelines.

    The Director converts spacetime objects and timelines into
    executable animation plans for Manim scenes.

    Attributes:
        timeline: Spacetime timeline to execute
        voiceover_syncer: Optional voiceover synchronization
        bookmark_manager: Optional bookmark manager
    """

    def __init__(
        self,
        timeline: Optional[Timeline] = None,
        voiceover_syncer: Optional['VoiceoverSyncer'] = None,
        bookmark_manager: Optional['BookmarkManager'] = None
    ):
        self.timeline = timeline
        self.voiceover_syncer = voiceover_syncer
        self.bookmark_manager = bookmark_manager

    def create_animation_plan(self, timeline: Optional[Timeline] = None) -> AnimationPlan:
        """
        Create an animation plan from a timeline.

        Args:
            timeline: Timeline to create plan from (uses self.timeline if None)

        Returns:
            AnimationPlan with sorted animation instructions
        """
        if timeline is None:
            timeline = self.timeline

        if timeline is None:
            raise ValueError("No timeline provided")

        plan = AnimationPlan()

        # Convert each spacetime object to animation instructions
        for obj in timeline.objects:
            instructions = self._object_to_instructions(obj)
            for instr in instructions:
                plan.add_animation(instr)

        # Sort by start time
        plan.sort_by_time()

        # Sync with voiceover if available
        if self.voiceover_syncer:
            plan = self.voiceover_syncer.sync_plan(plan)

        return plan

    def _object_to_instructions(
        self, obj: SpacetimeObject
    ) -> List[AnimationInstruction]:
        """
        Convert a spacetime object to animation instructions.

        Args:
            obj: SpacetimeObject to convert

        Returns:
            List of AnimationInstruction objects
        """
        instructions = []

        obj_type = obj.object_type

        # Create instruction based on object type
        if obj_type == 'code_display':
            instructions.append(AnimationInstruction(
                object_id=obj.id,
                action_type='show_code',
                start_time=obj.time.start,
                duration=obj.time.duration,
                parameters={
                    'code': obj.metadata.get('code', ''),
                    'language': obj.metadata.get('language', 'C'),
                    'space': obj.space,
                    'layer': obj.layer
                }
            ))

        elif obj_type == 'memory_display':
            instructions.append(AnimationInstruction(
                object_id=obj.id,
                action_type='show_memory',
                start_time=obj.time.start,
                duration=obj.time.duration,
                parameters={
                    'cells': obj.metadata.get('cells', 16),
                    'rows': obj.metadata.get('rows', 1),
                    'values': obj.metadata.get('values'),
                    'highlight_cells': obj.metadata.get('highlight_cells', []),
                    'space': obj.space,
                    'layer': obj.layer
                }
            ))

        elif obj_type == 'register_display':
            instructions.append(AnimationInstruction(
                object_id=obj.id,
                action_type='show_register',
                start_time=obj.time.start,
                duration=obj.time.duration,
                parameters={
                    'name': obj.metadata.get('name', 'REG'),
                    'value': obj.metadata.get('value', 0),
                    'bits': obj.metadata.get('bits', 32),
                    'space': obj.space,
                    'layer': obj.layer
                }
            ))

        else:
            # Generic show instruction
            instructions.append(AnimationInstruction(
                object_id=obj.id,
                action_type='show',
                start_time=obj.time.start,
                duration=obj.time.duration,
                parameters={
                    'space': obj.space,
                    'layer': obj.layer,
                    'metadata': obj.metadata
                }
            ))

        return instructions

    def execute(self, scene, timeline: Optional[Timeline] = None) -> None:
        """
        Execute the timeline on a Manim scene.

        This is the main entry point for rendering.

        Args:
            scene: Manim scene object
            timeline: Timeline to execute (uses self.timeline if None)
        """
        plan = self.create_animation_plan(timeline)

        # Group animations by time for efficient execution
        time_groups = self._group_by_time(plan)

        # Execute each time group
        for time, animations in time_groups:
            self._execute_at_time(scene, time, animations)

    def _group_by_time(
        self, plan: AnimationPlan
    ) -> List[Tuple[float, List[AnimationInstruction]]]:
        """
        Group animations that start at the same time.

        Args:
            plan: Animation plan

        Returns:
            List of (time, animations) tuples sorted by time
        """
        groups = []
        current_time = None
        current_group = []

        for anim in plan.animations:
            if current_time is None or anim.start_time != current_time:
                if current_group:
                    groups.append((current_time, current_group))
                current_time = anim.start_time
                current_group = []
            current_group.append(anim)

        if current_group:
            groups.append((current_time, current_group))

        return groups

    def _execute_at_time(
        self,
        scene,
        time: float,
        animations: List[AnimationInstruction]
    ) -> None:
        """
        Execute a group of animations at a specific time.

        Args:
            scene: Manim scene
            time: Current time
            animations: Animations to execute
        """
        # Group by layer for proper z-ordering
        by_layer: Dict[int, List[AnimationInstruction]] = {}
        for anim in animations:
            layer = anim.parameters.get('layer', 0)
            if layer not in by_layer:
                by_layer[layer] = []
            by_layer[layer].append(anim)

        # Execute layer by layer (bottom to top)
        for layer in sorted(by_layer.keys()):
            layer_animations = by_layer[layer]
            for anim in layer_animations:
                self._execute_instruction(scene, anim)

            # Wait for all animations in this layer to complete
            if layer_animations:
                max_duration = max(a.duration for a in layer_animations)
                scene.wait(max_duration)

    def _execute_instruction(self, scene, instruction: AnimationInstruction) -> None:
        """
        Execute a single animation instruction.

        This is a bridge method that will be implemented by the
        concrete scene class in the implementation layer.

        Args:
            scene: Manim scene
            instruction: Animation instruction to execute
        """
        # The actual implementation will be in LayeredScene
        # This method serves as documentation of the interface
        handler_name = f"_handle_{instruction.action_type}"
        handler = getattr(scene, handler_name, None)

        if handler is None:
            # Default handler
            handler = getattr(scene, '_handle_default', None)

        if handler:
            handler(instruction)
        else:
            # No handler found, skip
            pass

    def get_timing_breakdown(
        self, timeline: Optional[Timeline] = None
    ) -> Dict[str, Any]:
        """
        Get timing breakdown for a timeline.

        Useful for debugging and optimization.

        Args:
            timeline: Timeline to analyze (uses self.timeline if None)

        Returns:
            Dictionary with timing information
        """
        if timeline is None:
            timeline = self.timeline

        if timeline is None:
            raise ValueError("No timeline provided")

        plan = self.create_animation_plan(timeline)

        # Calculate statistics
        by_type: Dict[str, List[float]] = {}
        for anim in plan.animations:
            if anim.action_type not in by_type:
                by_type[anim.action_type] = []
            by_type[anim.action_type].append(anim.duration)

        type_stats = {}
        for action_type, durations in by_type.items():
            type_stats[action_type] = {
                'count': len(durations),
                'total': sum(durations),
                'average': sum(durations) / len(durations) if durations else 0,
                'min': min(durations) if durations else 0,
                'max': max(durations) if durations else 0
            }

        return {
            'total_duration': plan.total_duration,
            'total_animations': len(plan.animations),
            'by_type': type_stats,
            'layers': len(set(a.parameters.get('layer', 0) for a in plan.animations))
        }


class ManimDirector(Director):
    """
    Director implementation specifically for Manim.

    Provides Manim-specific animation execution.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mobjects: Dict[str, Any] = {}  # Map object IDs to Manim mobjects

    def register_mobject(self, obj_id: str, mobject: Any) -> None:
        """Register a Manim mobject for an object ID."""
        self.mobjects[obj_id] = mobject

    def get_mobject(self, obj_id: str) -> Optional[Any]:
        """Get a Manim mobject by object ID."""
        return self.mobjects.get(obj_id)

    def has_mobject(self, obj_id: str) -> bool:
        """Check if a mobject is registered."""
        return obj_id in self.mobjects
