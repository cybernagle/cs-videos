# Migration Guide: From Old to New Architecture

This guide helps migrate existing video content to the new 4-layer architecture.

## Overview of Changes

### Before (Old Approach)
```python
# Direct Manim code in scene files
from manim import *

class MyScene(Scene):
    def construct(self):
        # Everything mixed together
        code = Code("int main() { return 0; }")
        memory = MemoryVisualization(cells=16)
        self.play(FadeIn(code))
        self.play(code.animate.shift(LEFT))
        self.play(FadeIn(memory))
        # No conflict detection, lots of duplication
```

### After (New 4-Layer Architecture)
```python
# Separated concerns with conflict detection
from core.business import StoryBuilder
from core.business.narrative import show_code, display_memory
from core.implementation import LayeredScene

# 1. Business Layer: Define story
story = StoryBuilder("My Video") \
    .new_chapter("Introduction") \
    .with_scene("Show code", "Here is some C code", [
        show_code("int main() { return 0; }"),
        display_memory(cells=16)
    ]) \
    .end_chapter() \
    .build()

# 2-4. Other layers handled automatically
scene = LayeredScene(story=story)
scene.render_story()  # Conflict detection included!
```

## Migration Steps

### Step 1: Understand Your Current Scene

Identify the key elements in your existing scene:
1. What content is shown? (code, memory, registers, diagrams)
2. In what order do things appear?
3. Are there any voiceovers?
4. What are the timings?

### Step 2: Create a Story

Convert your scene to a Story using the Business Layer:

```python
from core.business import Story, Chapter, SceneNarrative
from core.business.narrative import show_code, display_memory, wait

# Old approach: Direct Manim code
# New approach: Define story first
story = Story(title="My Video")

chapter = Chapter(title="Introduction")
story.add_chapter(chapter)

# Old: self.play(FadeIn(Code(...)))
# New: Create scene with action
scene = SceneNarrative(
    description="Show C code",
    voiceover_text="Here is a simple C program"
)
scene.add_action(show_code("int main() { return 0; }"))
scene.add_action(wait(duration=2))
chapter.add_scene(scene)
```

### Step 3: Extract Components

Move reusable visual elements to `components/`:

```python
# Old: Code duplicated in every scene
# New: Create reusable component

# components/data_structures/tree.py
from core.implementation.mobjects import VGroup

class BinaryTree(VGroup):
    def __init__(self, nodes, edges, **kwargs):
        super().__init__(**kwargs)
        # Build tree visualization
        ...

# Now reusable across all scenes
```

### Step 4: Use Theme System

Replace hardcoded colors with theme references:

```python
# Old
rect = Rectangle(fill_color="#FFFF00", stroke_color="#FFFFFF")

# New
from themes import get_theme
theme = get_theme()
rect = Rectangle(fill_color=theme.MEMORY, stroke_color=theme.WHITE)
```

### Step 5: Check for Conflicts

Use the conflict detection system:

```python
from core.spacetime import ConflictDetector

# Convert story to timeline
timeline = story.to_spacetime().merge_all()

# Detect conflicts
detector = ConflictDetector()
report = detector.detect_conflicts(timeline)

if report.has_conflicts():
    report.print_report()
    # Adjust timing or positioning
```

## Common Migration Patterns

### Pattern 1: Simple Code Display

**Before:**
```python
class CodeScene(Scene):
    def construct(self):
        code = Code(
            "int main() { return 0; }",
            language="C"
        )
        self.play(FadeIn(code))
        self.wait(2)
```

**After:**
```python
from core.business import StoryBuilder
from core.business.narrative import show_code

story = StoryBuilder("Code Display") \
    .new_chapter("Main") \
    .with_scene(
        "Show code",
        "int main() { return 0; }",
        [show_code("int main() { return 0; }")]
    ) \
    .end_chapter() \
    .build()
```

### Pattern 2: Code + Explanation

**Before:**
```python
class ExplainedScene(Scene):
    def construct(self):
        code = Code("int x = 5;")
        explanation = Text("Variable declaration")
        code.to_edge(UP)
        explanation.next_to(code, DOWN)
        self.play(FadeIn(code))
        self.play(FadeIn(explanation))
```

**After:**
```python
from core.spacetime.layouts import LayoutTemplate
from core.business import StoryBuilder

# Use predefined layout
layout = LayoutTemplate.code_with_explanation()

story = StoryBuilder("Explained Code") \
    .new_chapter("Main") \
    .with_scene("Show code and explanation", "", [
        show_code("int x = 5;", position="top"),
        show_text("Variable declaration", position="bottom")
    ]) \
    .end_chapter() \
    .build()
```

### Pattern 3: Memory + Registers

**Before:**
```python
from lib.manim_os import OSLibrary

class MemoryScene(OSLibrary, Scene):
    def construct(self):
        self.create_memory(length=16)
        self.play(FadeIn(self.memory))
        # Position manually, risk of overlap
```

**After:**
```python
from core.business import StoryBuilder
from core.business.narrative import display_memory, display_register

story = StoryBuilder("Memory Scene") \
    .new_chapter("Main") \
    .with_scene("Show memory", "", [
        display_memory(cells=16, position="center"),
        display_register("EAX", 0, position="left")
    ]) \
    .end_chapter() \
    .build()

# Conflicts automatically detected!
```

## Component Migration Checklist

For each component in `lib/manim-os.py`:

- [ ] Extract to `components/` subdirectory
- [ ] Create class that extends VGroup
- [ ] Add theme support (colors from `themes/colors.py`)
- [ ] Add type hints for parameters
- [ ] Add docstring with usage example
- [ ] Update imports in old code to use new component
- [ ] Test component in isolation

## Scene Migration Checklist

For each existing scene:

- [ ] Read through scene and identify all visual elements
- [ ] Create Story with equivalent chapters/scenes
- [ ] Map old Manim code to narrative actions
- [ ] Extract custom components to `components/`
- [ ] Replace hardcoded values with theme references
- [ ] Check for spacetime conflicts
- [ ] Test render output matches original
- [ ] Keep old version as reference until verified

## Testing Your Migration

1. **Syntax check**: Import your new story module
   ```python
   python -c "from my_video import story; print(story)"
   ```

2. **Timeline check**: Verify timeline is created
   ```python
   timeline = story.to_spacetime().merge_all()
   print(f"Objects: {len(timeline.objects)}")
   ```

3. **Conflict check**: Run conflict detection
   ```python
   from core.spacetime import ConflictDetector
   report = ConflictDetector().detect_conflicts(timeline)
   report.print_report()
   ```

4. **Visual check**: Render and compare with original
   ```bash
   manim -pql my_new_scene.py MyNewScene
   ```

## Getting Help

If you encounter issues during migration:

1. Check `ARCHITECTURE.md` for layer descriptions
2. Check `examples/` for complete working examples
3. Run `test_architecture.py` to verify installation
4. Check conflict detection output for overlapping objects

## Timeline

Recommended migration order:

1. **Week 1-2**: Set up new architecture, understand patterns
2. **Week 3-4**: Migrate simple algorithm videos
3. **Week 5-6**: Migrate memory management videos
4. **Week 7-8**: Migrate process/OS videos
5. **Week 9-10**: Migrate bootloader videos
6. **Week 11-12**: Final testing and cleanup

## Rollback Plan

If migration doesn't work for a particular scene:

1. Keep original file as `*_old.py`
2. Create new version as `*_new.py`
3. Compare rendered outputs
4. If new version has issues, keep old version
5. Document issues for future resolution
