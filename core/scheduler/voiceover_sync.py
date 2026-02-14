"""
Voiceover synchronization for animations.

Handles loading transcripts, parsing bookmarks, and syncing
animations to voiceover timing.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import re


@dataclass
class Bookmark:
    """
    A bookmark in the voiceover timeline.

    Attributes:
        name: Bookmark identifier
        time: Time in seconds
        label: Optional human-readable label
    """

    name: str
    time: float
    label: str = ""

    def __str__(self) -> str:
        return f"Bookmark('{self.name}', {self.time:.2f}s)"


@dataclass
class Transcript:
    """
    A voiceover transcript with timing information.

    Can be parsed from SRT or other subtitle formats.

    Attributes:
        segments: List of transcript segments with timing
        bookmarks: List of bookmarks
        total_duration: Total duration
    """

    @dataclass
    class Segment:
        """A segment of transcript with start and end times."""
        start: float
        end: float
        text: str

        @property
        def duration(self) -> float:
            return self.end - self.start

    segments: List[Segment] = field(default_factory=list)
    bookmarks: List[Bookmark] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        if not self.segments:
            return 0.0
        return max(seg.end for seg in self.segments)

    @classmethod
    def from_srt(cls, srt_content: str) -> 'Transcript':
        """
        Parse an SRT subtitle file.

        Args:
            srt_content: Content of SRT file

        Returns:
            Transcript object
        """
        transcript = cls()

        # Split into blocks
        blocks = re.split(r'\n\s*\n', srt_content.strip())

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue

            # Parse timing line (format: 00:00:00,000 --> 00:00:02,500)
            timing_line = lines[1]
            match = re.match(
                r'(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)',
                timing_line
            )

            if match:
                start_h, start_m, start_s, start_ms = map(int, match.group(1, 2, 3, 4))
                end_h, end_m, end_s, end_ms = map(int, match.group(5, 6, 7, 8))

                start = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000
                end = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000

                text = '\n'.join(lines[2:])

                transcript.segments.append(cls.Segment(start=start, end=end, text=text))

        return transcript

    @classmethod
    def from_vtt(cls, vtt_content: str) -> 'Transcript':
        """
        Parse a WebVTT subtitle file.

        Args:
            vtt_content: Content of VTT file

        Returns:
            Transcript object
        """
        transcript = cls()

        lines = vtt_content.strip().split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Look for timing line (format: 00:00:00.000 --> 00:00:02.500)
            if '-->' in line:
                match = re.match(
                    r'(\d+):(\d+):(\d+)\.(\d+)\s*-->\s*(\d+):(\d+):(\d+)\.(\d+)',
                    line
                )

                if match:
                    start_h, start_m, start_s, start_ms = map(int, match.group(1, 2, 3, 4))
                    end_h, end_m, end_s, end_ms = map(int, match.group(5, 6, 7, 8))

                    start = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000
                    end = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000

                    # Collect text lines
                    i += 1
                    text_lines = []
                    while i < len(lines) and lines[i].strip() != '':
                        text_lines.append(lines[i])
                        i += 1

                    text = '\n'.join(text_lines)
                    transcript.segments.append(cls.Segment(start=start, end=end, text=text))

            i += 1

        return transcript

    def get_segment_at_time(self, time: float) -> Optional[Segment]:
        """Get the transcript segment active at a given time."""
        for segment in self.segments:
            if segment.start <= time <= segment.end:
                return segment
        return None

    def get_text_at_time(self, time: float) -> str:
        """Get the transcript text at a given time."""
        segment = self.get_segment_at_time(time)
        return segment.text if segment else ""

    def add_bookmark(self, name: str, time: float, label: str = "") -> None:
        """Add a bookmark at a specific time."""
        # Remove existing bookmark with same name
        self.bookmarks = [b for b in self.bookmarks if b.name != name]
        self.bookmarks.append(Bookmark(name=name, time=time, label=label))
        self.bookmarks.sort(key=lambda b: b.time)

    def get_bookmark(self, name: str) -> Optional[Bookmark]:
        """Get a bookmark by name."""
        for bookmark in self.bookmarks:
            if bookmark.name == name:
                return bookmark
        return None

    def get_bookmarks_in_range(self, start: float, end: float) -> List[Bookmark]:
        """Get all bookmarks within a time range."""
        return [b for b in self.bookmarks if start <= b.time <= end]


class VoiceoverSyncer:
    """
    Synchronizes animation plans with voiceover transcripts.

    Adjusts animation timing to match voiceover pacing and
    ensures bookmarks align with key moments.
    """

    def __init__(self, transcript: Optional[Transcript] = None):
        """
        Initialize the voiceover syncer.

        Args:
            transcript: Optional transcript to sync with
        """
        self.transcript = transcript

    def load_transcript(self, content: str, format: str = 'srt') -> Transcript:
        """
        Load a transcript from content.

        Args:
            content: Transcript content
            format: Format of transcript ('srt' or 'vtt')

        Returns:
            Loaded Transcript object
        """
        if format == 'srt':
            self.transcript = Transcript.from_srt(content)
        elif format == 'vtt':
            self.transcript = Transcript.from_vtt(content)
        else:
            raise ValueError(f"Unsupported transcript format: {format}")

        return self.transcript

    def sync_plan(self, plan: 'AnimationPlan') -> 'AnimationPlan':
        """
        Sync an animation plan with the loaded transcript.

        Adjusts animation timing based on voiceover segments.

        Args:
            plan: Animation plan to sync

        Returns:
            Synced animation plan
        """
        if self.transcript is None:
            return plan

        # For each animation, find corresponding transcript segment
        for anim in plan.animations:
            segment = self.transcript.get_segment_at_time(anim.start_time)
            if segment:
                # Adjust duration to match segment
                if segment.duration > anim.duration:
                    anim.duration = segment.duration

                # Add transcript text to parameters
                anim.parameters['voiceover_text'] = segment.text

        return plan

    def extract_bookmarks_from_transcript(self) -> List[Bookmark]:
        """
        Extract bookmarks from transcript segment text.

        Looks for patterns like [Bookmark: name] in text.

        Returns:
            List of extracted bookmarks
        """
        if self.transcript is None:
            return []

        bookmarks = []
        pattern = re.compile(r'\[Bookmark:\s*([^\]]+)\]', re.IGNORECASE)

        for segment in self.transcript.segments:
            matches = pattern.findall(segment.text)
            for match in matches:
                bookmarks.append(Bookmark(
                    name=match.strip(),
                    time=segment.start,
                    label=match.strip()
                ))

        return bookmarks

    def align_animations_to_words(
        self,
        plan: 'AnimationPlan',
        words_per_second: float = 2.5
    ) -> 'AnimationPlan':
        """
        Align animation timing based on word count.

        Args:
            plan: Animation plan to adjust
            words_per_second: Speaking rate (default 2.5 wps)

        Returns:
            Adjusted animation plan
        """
        if self.transcript is None:
            return plan

        current_time = 0.0

        for anim in plan.animations:
            # Get transcript text at this time
            text = self.transcript.get_text_at_time(current_time)
            word_count = len(text.split())

            # Calculate expected duration
            expected_duration = word_count / words_per_second

            # Adjust animation timing
            anim.start_time = current_time
            anim.duration = max(anim.duration, expected_duration)

            current_time += anim.duration

        return plan

    def estimate_duration_from_text(self, text: str, wps: float = 2.5) -> float:
        """
        Estimate voiceover duration from text.

        Args:
            text: Text to estimate duration for
            wps: Words per second speaking rate

        Returns:
            Estimated duration in seconds
        """
        word_count = len(text.split())
        return max(1.0, word_count / wps)
