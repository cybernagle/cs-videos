"""
Bookmark management for video editing and navigation.

Bookmarks allow marking important moments in videos for
easy navigation and synchronization with voiceover.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from pathlib import Path


@dataclass
class Bookmark:
    """
    A bookmark marking a specific moment in a video.

    Attributes:
        name: Unique identifier for the bookmark
        time: Time in seconds
        label: Human-readable description
        chapter: Optional chapter name
        metadata: Additional data
    """

    name: str
    time: float
    label: str = ""
    chapter: str = ""
    metadata: dict = field(default_factory=dict)

    def __str__(self) -> str:
        if self.label:
            return f"{self.name} ({self.label}) - {self.time:.2f}s"
        return f"{self.name} - {self.time:.2f}s"


class BookmarkManager:
    """
    Manages bookmarks for video navigation and editing.

    Provides functionality to add, remove, query, and export bookmarks.
    """

    def __init__(self):
        """Initialize an empty bookmark manager."""
        self.bookmarks: Dict[str, Bookmark] = {}

    def add(self, bookmark: Bookmark) -> None:
        """
        Add a bookmark.

        Args:
            bookmark: Bookmark to add
        """
        self.bookmarks[bookmark.name] = bookmark

    def remove(self, name: str) -> bool:
        """
        Remove a bookmark by name.

        Args:
            name: Bookmark name

        Returns:
            True if bookmark was removed, False if not found
        """
        if name in self.bookmarks:
            del self.bookmarks[name]
            return True
        return False

    def get(self, name: str) -> Optional[Bookmark]:
        """
        Get a bookmark by name.

        Args:
            name: Bookmark name

        Returns:
            Bookmark or None if not found
        """
        return self.bookmarks.get(name)

    def get_at_time(self, time: float, tolerance: float = 0.5) -> Optional[Bookmark]:
        """
        Get a bookmark near a specific time.

        Args:
            time: Time to search around
            tolerance: Time tolerance in seconds

        Returns:
            Nearest bookmark or None
        """
        nearest = None
        nearest_dist = float('inf')

        for bookmark in self.bookmarks.values():
            dist = abs(bookmark.time - time)
            if dist <= tolerance and dist < nearest_dist:
                nearest = bookmark
                nearest_dist = dist

        return nearest

    def get_in_range(self, start: float, end: float) -> List[Bookmark]:
        """
        Get all bookmarks within a time range.

        Args:
            start: Range start
            end: Range end

        Returns:
            List of bookmarks in range, sorted by time
        """
        bookmarks = [
            b for b in self.bookmarks.values()
            if start <= b.time <= end
        ]
        return sorted(bookmarks, key=lambda b: b.time)

    def get_by_chapter(self, chapter: str) -> List[Bookmark]:
        """
        Get all bookmarks in a chapter.

        Args:
            chapter: Chapter name

        Returns:
            List of bookmarks in chapter
        """
        return [
            b for b in self.bookmarks.values()
            if b.chapter == chapter
        ]

    def list_all(self) -> List[Bookmark]:
        """
        Get all bookmarks sorted by time.

        Returns:
            List of all bookmarks
        """
        return sorted(self.bookmarks.values(), key=lambda b: b.time)

    def rename(self, old_name: str, new_name: str) -> bool:
        """
        Rename a bookmark.

        Args:
            old_name: Current name
            new_name: New name

        Returns:
            True if renamed, False if old_name not found
        """
        if old_name not in self.bookmarks:
            return False

        bookmark = self.bookmarks[old_name]
        bookmark.name = new_name
        self.bookmarks[new_name] = bookmark
        del self.bookmarks[old_name]
        return True

    def update_time(self, name: str, new_time: float) -> bool:
        """
        Update bookmark time.

        Args:
            name: Bookmark name
            new_time: New time value

        Returns:
            True if updated, False if not found
        """
        if name in self.bookmarks:
            self.bookmarks[name].time = new_time
            return True
        return False

    def export_to_dict(self) -> dict:
        """
        Export bookmarks to dictionary format.

        Returns:
            Dictionary with bookmark data
        """
        return {
            name: {
                'time': b.time,
                'label': b.label,
                'chapter': b.chapter,
                'metadata': b.metadata
            }
            for name, b in self.bookmarks.items()
        }

    def import_from_dict(self, data: dict) -> None:
        """
        Import bookmarks from dictionary format.

        Args:
            data: Dictionary with bookmark data
        """
        for name, info in data.items():
            bookmark = Bookmark(
                name=name,
                time=info.get('time', 0.0),
                label=info.get('label', ''),
                chapter=info.get('chapter', ''),
                metadata=info.get('metadata', {})
            )
            self.add(bookmark)

    def export_to_manim(self) -> str:
        """
        Export bookmarks to Manim-compatible code.

        Returns:
            Python code string with bookmark definitions
        """
        lines = []
        lines.append("# Bookmarks for Manim VoiceoverScene")
        lines.append("")

        for bookmark in self.list_all():
            label_escaped = bookmark.label.replace('"', '\\"')
            lines.append(
                f'self.add_bookmark("{bookmark.name}", {bookmark.time:.3f}, "{label_escaped}")'
            )

        return '\n'.join(lines)

    def export_to_csv(self, path: str) -> None:
        """
        Export bookmarks to CSV file.

        Args:
            path: Output file path
        """
        import csv

        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Time', 'Label', 'Chapter'])

            for bookmark in self.list_all():
                writer.writerow([
                    bookmark.name,
                    f'{bookmark.time:.3f}',
                    bookmark.label,
                    bookmark.chapter
                ])

    def import_from_csv(self, path: str) -> None:
        """
        Import bookmarks from CSV file.

        Args:
            path: Input file path
        """
        import csv

        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bookmark = Bookmark(
                    name=row['Name'],
                    time=float(row['Time']),
                    label=row.get('Label', ''),
                    chapter=row.get('Chapter', '')
                )
                self.add(bookmark)

    def create_chapter_bookmarks(
        self, chapter_durations: Dict[str, float]
    ) -> None:
        """
        Create bookmarks at the start of each chapter.

        Args:
            chapter_durations: Dictionary of chapter name to duration
        """
        current_time = 0.0
        for chapter_name, duration in chapter_durations.items():
            bookmark = Bookmark(
                name=f"chapter_{chapter_name}",
                time=current_time,
                label=f"Chapter: {chapter_name}",
                chapter=chapter_name
            )
            self.add(bookmark)
            current_time += duration

    def validate(self) -> List[str]:
        """
        Validate bookmarks for common issues.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check for duplicate times
        times = {}
        for name, bookmark in self.bookmarks.items():
            time_key = int(bookmark.time * 10)  # Group by 0.1s intervals
            if time_key in times:
                errors.append(
                    f"Bookmarks '{name}' and '{times[time_key]}' "
                    f"are at the same time ({bookmark.time:.2f}s)"
                )
            else:
                times[time_key] = name

        # Check for negative times
        for name, bookmark in self.bookmarks.items():
            if bookmark.time < 0:
                errors.append(f"Bookmark '{name}' has negative time: {bookmark.time:.2f}s")

        return errors

    def __len__(self) -> int:
        """Get the number of bookmarks."""
        return len(self.bookmarks)

    def __contains__(self, name: str) -> bool:
        """Check if a bookmark exists."""
        return name in self.bookmarks

    def __repr__(self) -> str:
        return f"BookmarkManager({len(self.bookmarks)} bookmarks)"
