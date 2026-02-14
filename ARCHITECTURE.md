# 4-Layer Architecture for cs-videos

## Overview

The cs-videos repository has been refactored with a 4-layer architecture that separates concerns, enables component reuse, and provides spacetime conflict detection.

```
┌─────────────────────────────────────────────────────────┐
│ Business Layer (core/business/)                      │
│ Story/scripts, pure narrative logic                    │
├─────────────────────────────────────────────────────────┤
│ Spacetime Layer (core/spacetime/)                   │
│ Objects, timelines, layouts, conflict detection         │
├─────────────────────────────────────────────────────────┤
│ Scheduler Layer (core/scheduler/)                     │
│ Animation orchestration, voiceover sync                │
├─────────────────────────────────────────────────────────┤
│ Implementation Layer (core/implementation/)              │
│ Manim code, concrete mobject implementations          │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

```
/root/cs-videos/
├── core/                           # NEW: Core framework
│   ├── business/                   # LAYER 1
│   │   ├── __init__.py
│   │   ├── story.py                # Story/script abstractions
│   │   ├── narrative.py            # Narrative constructs and actions
│   │   └── entities.py             # Business entities (Process, Memory, etc.)
│   ├── spacetime/                  # LAYER 2
│   │   ├── __init__.py
│   │   ├── objects.py              # SpaceRegion, TimeWindow, SpacetimeObject
│   │   ├── timelines.py            # Timeline management
│   │   ├── layouts.py              # Layout regions and zones
│   │   ├── conflict_detection.py   # Overlap detection algorithm
│   │   └── visualization.py        # Debug viz (gantt charts, heatmaps)
│   ├── scheduler/                  # LAYER 3
│   │   ├── __init__.py
│   │   ├── director.py             # Animation orchestration
│   │   ├── voiceover_sync.py       # Voiceover synchronization
│   │   ├── bookmarks.py            # Bookmark management
│   │   └── animation_plans.py      # Animation sequence planning
│   └── implementation/             # LAYER 4
│       ├── __init__.py
│       ├── scenes.py               # Scene base classes
│       └── mobjects/               # Concrete Manim objects
│           ├── __init__.py
│           ├── code.py             # Code display components
│           ├── memory.py           # Memory visualizations
│           └── registers.py        # CPU register displays
│
├── themes/                         # NEW: Theme and styling
│   ├── __init__.py
│   ├── colors.py                   # Color palettes
│   └── typography.py               # Font configurations
│
├── components/                     # NEW: Reusable visual components
│   └── __init__.py                 # (To be populated from lib/manim-os.py)
│
├── examples/                       # NEW: Migration examples
│   └── c_program_execution/
│       └── __init__.py             # Example using new architecture
│
└── lib/                            # EXISTING: To be migrated
    └── manim-os.py                 # Legacy code (preserve for compatibility)
```

## Quick Start

### Creating a Story

```python
from core.business import StoryBuilder
from core.business.narrative import show_code, voiceover

story = StoryBuilder("My Video") \
    .new_chapter("Introduction") \
    .with_scene(
        "Show code",
        "Here is some C code",
        [show_code("int main() { return 0; }")]
    ) \
    .end_chapter() \
    .build()
```

### Checking for Conflicts

```python
from core.spacetime import ConflictDetector

# Convert story to timeline
timeline = story.to_spacetime().merge_all()

# Detect conflicts
detector = ConflictDetector()
report = detector.detect_conflicts(timeline)

if report.has_conflicts():
    report.print_report()
```

### Rendering with Manim

```python
from core.implementation import LayeredScene

scene = LayeredScene(story=story)
scene.render_story()  # Automatically checks conflicts
```

## Layer Descriptions

### LAYER 1: Business Layer (`core/business/`)

**Purpose**: Pure narrative and domain logic, independent of visualization.

**Key Classes**:
- `Story`: Complete video narrative
- `Chapter`: Section of a story
- `SceneNarrative`: Single narrative beat
- `NarrativeAction`: Actions like show_code, transform, highlight

**File**: `core/business/story.py`, `narrative.py`, `entities.py`

### LAYER 2: Spacetime Layer (`core/spacetime/`)

**Purpose**: Manage objects in time and space, detect conflicts.

**Key Classes**:
- `SpaceRegion`: 2D spatial region with collision detection
- `TimeWindow`: Time interval with overlap detection
- `SpacetimeObject`: Object existing in spacetime
- `Timeline`: Collection of spacetime objects
- `ConflictDetector`: Detects overlaps using O(n) spatial hashing

**File**: `core/spacetime/objects.py`, `timelines.py`, `conflict_detection.py`

### LAYER 3: Scheduler Layer (`core/scheduler/`)

**Purpose**: Orchestrate animations, sync with voiceover.

**Key Classes**:
- `Director`: Converts timelines to animation plans
- `VoiceoverSyncer`: Syncs animations to voiceover transcripts
- `BookmarkManager`: Manages video bookmarks

**File**: `core/scheduler/director.py`, `voiceover_sync.py`, `bookmarks.py`

### LAYER 4: Implementation Layer (`core/implementation/`)

**Purpose**: Concrete Manim implementations.

**Key Classes**:
- `LayeredScene`: Base scene with 4-layer integration
- `CodeDisplay`: Code visualization component
- `MemoryViz`: Memory visualization
- `RegisterDisplay`: CPU register display

**File**: `core/implementation/scenes.py`, `mobjects/code.py`, `mobjects/memory.py`, `mobjects/registers.py`

## Benefits

| Problem | Solution |
|----------|----------|
| Code duplication | Reusable component library (`components/`) |
| Mixed concerns | Clear layer separation |
| No conflict detection | Spacetime overlap detection (`ConflictDetector`) |
| Hard to maintain | Well-defined interfaces between layers |
| Scattered colors | Theme system (`themes/colors.py`) |
| Inconsistent layouts | Layout templates (`LayoutTemplate`) |

## Migration Strategy

1. **Phase 1** (Current): Core framework implemented
2. **Phase 2**: Migrate `lib/manim-os.py` to `components/`
3. **Phase 3**: Migrate existing scenes one by one
4. **Phase 4**: Update documentation and examples

## Requirements

- Python 3.7+ (for `dataclasses`)
- Manim (for rendering)
- manim-voiceover (optional, for voiceover sync)

## Example Output

```
$ python examples/c_program_execution/__init__.py

============================================================
CONFLICT DETECTION DEMO
============================================================
⚠ Found 1 conflicts among 3 objects:

1. 'source_code' <-> 'memory' (layer=0, severity=0.50)
   Overlap region: SpaceRegion(x=-3.00, y=-1.50, w=5.00, h=3.00)
   Overlap time: TimeWindow(2.00s - 3.00s, padding=0.50s)
   Suggestion: Objects start at nearly the same time - try staggering their appearance

============================================================
4-LAYER ARCHITECTURE DEMONSTRATION
============================================================

1. BUSINESS LAYER - Creating story...
   Created: Story('C Program Execution', 3 chapters, 5 scenes, 18.3s)
   Duration: 18.3s
   Chapters: 3
   Scenes: 5

2. SPACETIME LAYER - Converting to timeline...
   Timeline: Timeline(name='C Program Execution_merged', objects=5, duration=18.32s)
   Objects: 5

3. CONFLICT DETECTION - Checking for overlaps...
   No conflicts detected!

4. SCHEDULER LAYER - Creating animation plan...
   Total duration: 18.3s
   Total animations: 5
   Layers used: 1

5. IMPLEMENTATION LAYER - Ready to render
   (Rendering requires Manim to be installed)
```
