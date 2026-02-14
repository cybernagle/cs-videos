"""
Visualization tools for spacetime debugging.

Provides gantt charts, heatmaps, and other visualizations for
understanding spacetime object placement and conflicts.
"""
from typing import List, Optional, Tuple
from dataclasses import dataclass
import os

from .objects import SpacetimeObject, SpaceRegion, TimeWindow
from .timelines import Timeline
from .conflict_detection import ConflictReport


class SpaceTimeVisualizer:
    """
    Visualizes spacetime data for debugging and understanding.

    Creates text-based and file-based visualizations.
    """

    @staticmethod
    def gantt_chart(
        timeline: Timeline,
        output_path: Optional[str] = None,
        title: str = "Timeline Gantt Chart"
    ) -> str:
        """
        Create a text-based Gantt chart visualization.

        Args:
            timeline: Timeline to visualize
            output_path: Optional file path to save the chart
            title: Chart title

        Returns:
            String representation of the Gantt chart
        """
        if not timeline.objects:
            chart = "# No objects on timeline"
        else:
            # Sort objects by start time
            sorted_objs = sorted(timeline.objects, key=lambda o: o.time.start)

            # Calculate dimensions
            total_duration = timeline.duration or max(o.time.end for o in sorted_objs)
            chart_width = 80  # characters
            chart_height = len(sorted_objs) * 2 + 4

            lines = []
            lines.append(f"# {title}")
            lines.append(f"# Total duration: {total_duration:.2f}s")
            lines.append(f"# Objects: {len(sorted_objs)}")
            lines.append("#")

            # Time scale
            lines.append("# " + SpaceTimeVisualizer._create_time_scale(total_duration, chart_width))

            for obj in sorted_objs:
                # Object name
                name = obj.id[:20]
                lines.append(f"  {name:<20}")

                # Timeline bar
                bar = SpaceTimeVisualizer._create_timeline_bar(obj, total_duration, chart_width)
                lines.append(f"  {bar}")

            chart = "\n".join(lines)

        # Save to file if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(chart)

        return chart

    @staticmethod
    def _create_time_scale(duration: float, width: int) -> str:
        """Create time scale line."""
        if duration == 0:
            return "-" * width

        scale = []
        for i in range(width):
            time = (i / width) * duration
            if i % 10 == 0:
                scale.append(f"{time:.0f}s")
            else:
                scale.append(" ")
        return "".join(scale)

    @staticmethod
    def _create_timeline_bar(obj: SpacetimeObject, total_duration: float, width: int) -> str:
        """Create timeline bar for an object."""
        if total_duration == 0:
            return " " * width

        # Convert time to position
        start_pos = int((obj.time.start / total_duration) * width)
        end_pos = int((obj.time.end / total_duration) * width)

        # Create bar
        bar = [" "] * width
        for i in range(start_pos, min(end_pos, width)):
            bar[i] = "█"

        # Add layer info
        layer_char = str(obj.layer)
        if start_pos < width:
            bar[start_pos] = layer_char

        return "".join(bar)

    @staticmethod
    def space_heatmap(
        timeline: Timeline,
        time: float,
        output_path: Optional[str] = None,
        resolution: int = 40
    ) -> str:
        """
        Create a text-based spatial heatmap at a specific time.

        Args:
            timeline: Timeline to visualize
            time: Time point to visualize
            output_path: Optional file path to save the heatmap
            resolution: Grid resolution (characters per dimension)

        Returns:
            String representation of the heatmap
        """
        # Get objects active at time
        active_objs = [obj for obj in timeline.objects if obj.time.contains(time)]

        if not active_objs:
            heatmap = f"# No objects active at time {time:.2f}s"
        else:
            # Define space bounds
            x_min = min(obj.space.left for obj in active_objs)
            x_max = max(obj.space.right for obj in active_objs)
            y_min = min(obj.space.bottom for obj in active_objs)
            y_max = max(obj.space.top for obj in active_objs)

            # Create grid
            lines = []
            lines.append(f"# Spatial heatmap at t={time:.2f}s")
            lines.append(f"# Active objects: {len(active_objs)}")
            lines.append(f"# X range: [{x_min:.1f}, {x_max:.1f}]")
            lines.append(f"# Y range: [{y_min:.1f}, {y_max:.1f}]")
            lines.append("#")

            # Draw grid (top to bottom)
            for y in range(resolution - 1, -1, -1):
                row = []
                y_pos = y_min + (y / resolution) * (y_max - y_min)

                for x in range(resolution):
                    x_pos = x_min + (x / resolution) * (x_max - x_min)

                    # Check if any object covers this cell
                    covered = False
                    layer = -1
                    for obj in active_objs:
                        if (obj.space.left <= x_pos <= obj.space.right and
                            obj.space.bottom <= y_pos <= obj.space.top):
                            covered = True
                            layer = max(layer, obj.layer)
                            break

                    if covered:
                        row.append(str(layer % 10))
                    else:
                        row.append(".")

                lines.append("  " + "".join(row))

            # Legend
            lines.append("#")
            lines.append("# Legend: digits = layer numbers, . = empty space")

            heatmap = "\n".join(lines)

        # Save to file if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(heatmap)

        return heatmap

    @staticmethod
    def conflict_report_viz(
        report: ConflictReport,
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a formatted conflict report visualization.

        Args:
            report: ConflictReport to visualize
            output_path: Optional file path to save

        Returns:
            Formatted string representation
        """
        lines = []
        lines.append("=" * 60)
        lines.append("SPACETIME CONFLICT REPORT")
        lines.append("=" * 60)
        lines.append(f"Total objects checked: {report.total_objects}")
        lines.append(f"Total conflicts found: {report.total_conflicts}")
        lines.append("")

        if not report.has_conflicts:
            lines.append("✓ No conflicts detected!")
        else:
            lines.append("CONFLICTS:")
            lines.append("-" * 60)

            for i, conflict in enumerate(report.conflicts, 1):
                lines.append(f"\n{i}. {conflict.obj1.id} <-> {conflict.obj2.id}")
                lines.append(f"   Layer: {conflict.obj1.layer}")
                lines.append(f"   Severity: {conflict.severity:.2f}")

                if conflict.overlap_region:
                    lines.append(f"   Spatial overlap: {conflict.overlap_region}")

                if conflict.overlap_time:
                    lines.append(f"   Time overlap: {conflict.overlap_time}")

                if conflict.suggestion:
                    lines.append(f"   → {conflict.suggestion}")

        lines.append("")
        lines.append("=" * 60)

        viz = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(viz)

        return viz

    @staticmethod
    def object_summary(timeline: Timeline, output_path: Optional[str] = None) -> str:
        """
        Create a summary table of all objects.

        Args:
            timeline: Timeline to summarize
            output_path: Optional file path to save

        Returns:
            Formatted string summary
        """
        lines = []
        lines.append("=" * 100)
        lines.append(f"{'ID':<20} {'Type':<12} {'Layer':<6} {'Start':<8} {'End':<8} {'Space':<30}")
        lines.append("-" * 100)

        for obj in sorted(timeline.objects, key=lambda o: o.time.start):
            space_str = f"({obj.space.x:.1f},{obj.space.y:.1f}) {obj.space.width:.1f}x{obj.space.height:.1f}"
            lines.append(f"{obj.id:<20} {obj.object_type:<12} {obj.layer:<6} "
                        f"{obj.time.start:<8.2f} {obj.time.end:<8.2f} {space_str:<30}")

        lines.append("=" * 100)

        summary = "\n".join(lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(summary)

        return summary

    @staticmethod
    def layer_breakdown(timeline: Timeline) -> str:
        """
        Show breakdown of objects by layer.

        Args:
            timeline: Timeline to analyze

        Returns:
            Formatted string breakdown
        """
        from collections import defaultdict

        by_layer = defaultdict(list)
        for obj in timeline.objects:
            by_layer[obj.layer].append(obj)

        lines = []
        lines.append("LAYER BREAKDOWN:")
        lines.append("")

        for layer in sorted(by_layer.keys()):
            objs = by_layer[layer]
            lines.append(f"Layer {layer}: {len(objs)} objects")
            for obj in objs:
                lines.append(f"  - {obj.id} ({obj.object_type}) "
                           f"t={obj.time.start:.2f}-{obj.time.end:.2f}s")
            lines.append("")

        return "\n".join(lines)


def visualize_timeline(
    timeline: Timeline,
    output_dir: Optional[str] = None,
    prefix: str = "timeline"
) -> dict:
    """
    Create all visualizations for a timeline.

    Args:
        timeline: Timeline to visualize
        output_dir: Directory to save visualizations (default: current dir)
        prefix: Prefix for output files

    Returns:
        Dictionary with visualization paths and content
    """
    if output_dir is None:
        output_dir = "."

    os.makedirs(output_dir, exist_ok=True)

    results = {}

    # Gantt chart
    gantt_path = os.path.join(output_dir, f"{prefix}_gantt.txt")
    results['gantt'] = SpaceTimeVisualizer.gantt_chart(timeline, gantt_path)

    # Object summary
    summary_path = os.path.join(output_dir, f"{prefix}_summary.txt")
    results['summary'] = SpaceTimeVisualizer.object_summary(timeline, summary_path)

    # Layer breakdown
    results['layers'] = SpaceTimeVisualizer.layer_breakdown(timeline)

    # Heatmap at middle time
    if timeline.duration > 0:
        mid_time = timeline.duration / 2
        heatmap_path = os.path.join(output_dir, f"{prefix}_heatmap.txt")
        results['heatmap'] = SpaceTimeVisualizer.space_heatmap(
            timeline, mid_time, heatmap_path
        )

    return results
