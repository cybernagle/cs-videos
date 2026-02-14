"""
C Program Execution example using the 4-layer architecture.

This example demonstrates how to create an educational video about
C program compilation and execution using the new architecture.
"""
from core.business import Story, Chapter, SceneNarrative, StoryBuilder
from core.business.narrative import (
    show_code, display_memory, display_register,
    voiceover, wait, transform, highlight
)
from core.spacetime import ConflictDetector
from core.spacetime.visualization import SpaceTimeVisualizer


def create_c_program_story() -> Story:
    """
    Create a story about C program execution.

    This demonstrates the business layer - creating content
    without worrying about visualization details.
    """
    # Use the builder pattern for fluent story construction
    builder = StoryBuilder("C Program Execution")

    # Chapter 1: Source Code
    builder.new_chapter("Source Code", "Introduction to C source code") \
        .with_scene(
            "Show simple C program",
            voiceover_text="这是一个简单的 C 程序",
            actions=[
                show_code(
                    code="#include <stdio.h>\n\nint main() {\n    return 0;\n}",
                    language="C",
                    position="center"
                )
            ]
        ) \
        .with_scene(
            "Explain main function",
            voiceover_text="程序从 main 函数开始执行",
            actions=[
                highlight("code_main"),
                wait(2)
            ]
        ) \
        .end_chapter()

    # Chapter 2: Compilation
    builder.new_chapter("Compilation", "The C compilation process") \
        .with_scene(
            "Preprocessing",
            voiceover_text="预处理器处理头文件",
            actions=[
                display_memory(
                    cells=8,
                    rows=1,
                    position="left"
                )
            ]
        ) \
        .with_scene(
            "Compilation to assembly",
            voiceover_text="编译器生成汇编代码",
            actions=[
                show_code(
                    code="main:\n    push rbp\n    mov rbp, rsp\n    mov eax, 0\n    pop rbp\n    ret",
                    language="asm",
                    position="center"
                )
            ]
        ) \
        .end_chapter()

    # Chapter 3: Execution
    builder.new_chapter("Execution", "Program execution in memory") \
        .with_scene(
            "Load into memory",
            voiceover_text="程序被加载到内存",
            actions=[
                display_memory(
                    cells=16,
                    rows=2,
                    position="center"
                )
            ]
        ) \
        .with_scene(
            "CPU execution",
            voiceover_text="CPU 执行指令",
            actions=[
                display_register(
                    name="RIP",
                    value=0x1000,
                    position="left"
                ),
                display_register(
                    name="RBP",
                    value=0x7FF0,
                    position="left"
                )
            ]
        ) \
        .end_chapter()

    return builder.build()


def demonstrate_conflict_detection():
    """
    Demonstrate the conflict detection system.

    This shows how the spacetime layer can detect visual conflicts
    before rendering.
    """
    from core.spacetime import SpacetimeObject, SpaceRegion, TimeWindow, Timeline

    # Create a timeline with potential conflicts
    timeline = Timeline(name="demo")

    # Object 1: Code display at center, 0-3 seconds
    obj1 = SpacetimeObject(
        id="source_code",
        space=SpaceRegion(x=-4, y=-2, width=8, height=4),
        time=TimeWindow(start=0, end=3),
        layer=0,
        metadata={'type': 'code_display'}
    )
    timeline.add(obj1)

    # Object 2: Memory at center, 2-5 seconds (CONFLICTS!)
    obj2 = SpacetimeObject(
        id="memory",
        space=SpaceRegion(x=-3, y=-1.5, width=6, height=3),
        time=TimeWindow(start=2, end=5),
        layer=0,
        metadata={'type': 'memory_display'}
    )
    timeline.add(obj2)

    # Object 3: Register on left, no conflict
    obj3 = SpacetimeObject(
        id="register",
        space=SpaceRegion(x=-6.5, y=-0.5, width=2, height=1),
        time=TimeWindow(start=1, end=4),
        layer=0,
        metadata={'type': 'register_display'}
    )
    timeline.add(obj3)

    # Detect conflicts
    detector = ConflictDetector()
    report = detector.detect_conflicts(timeline)

    print("=" * 60)
    print("CONFLICT DETECTION DEMO")
    print("=" * 60)
    report.print_report()

    # Generate visualizations
    print("\nGenerating Gantt chart...")
    gantt = SpaceTimeVisualizer.gantt_chart(timeline, "/tmp/gantt.txt")
    print(gantt)

    print("\nGenerating heatmap at t=2.5s...")
    heatmap = SpaceTimeVisualizer.space_heatmap(timeline, 2.5, "/tmp/heatmap.txt")
    print(heatmap)

    return report


def demonstrate_layer_separation():
    """
    Demonstrate how the 4 layers work together.

    This shows the complete flow from business logic to rendering.
    """
    print("=" * 60)
    print("4-LAYER ARCHITECTURE DEMONSTRATION")
    print("=" * 60)

    # LAYER 1: Business Layer - Define the story
    print("\n1. BUSINESS LAYER - Creating story...")
    story = create_c_program_story()
    print(f"   Created: {story}")
    print(f"   Duration: {story.duration:.1f}s")
    print(f"   Chapters: {len(story.chapters)}")
    print(f"   Scenes: {story.scene_count}")

    # LAYER 2: Spacetime Layer - Convert to timeline
    print("\n2. SPACETIME LAYER - Converting to timeline...")
    sequence = story.to_spacetime()
    merged_timeline = sequence.merge_all()
    print(f"   Timeline: {merged_timeline}")
    print(f"   Objects: {len(merged_timeline.objects)}")

    # Conflict detection
    print("\n3. CONFLICT DETECTION - Checking for overlaps...")
    detector = ConflictDetector()
    report = detector.detect_conflicts(merged_timeline)
    if report.has_conflicts:
        print(f"   Found {report.total_conflicts} conflicts!")
    else:
        print("   No conflicts detected!")

    # LAYER 3: Scheduler Layer - Create animation plan
    print("\n4. SCHEDULER LAYER - Creating animation plan...")
    from core.scheduler import Director
    director = Director(timeline=merged_timeline)
    timing = director.get_timing_breakdown()
    print(f"   Total duration: {timing['total_duration']:.1f}s")
    print(f"   Total animations: {timing['total_animations']}")
    print(f"   Layers used: {timing['layers']}")

    # LAYER 4: Implementation Layer - Would render with Manim
    print("\n5. IMPLEMENTATION LAYER - Ready to render")
    print("   (Rendering requires Manim to be installed)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_conflict_detection()
    print("\n\n")
    demonstrate_layer_separation()
