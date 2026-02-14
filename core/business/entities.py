"""
Business entities for CS educational content.

Defines domain-specific entities like Process, Memory, CPU, etc.
These are higher-level abstractions that can be used in stories.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class ProcessState(Enum):
    """Process states in an operating system."""
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    TERMINATED = "terminated"


@dataclass
class Process:
    """
    Represents a process in OS context.

    Attributes:
        pid: Process ID
        name: Process name
        state: Current process state
        priority: Process priority
        memory_size: Memory allocated to process
        pc: Program counter value
        registers: CPU register values
    """

    pid: int
    name: str
    state: ProcessState = ProcessState.NEW
    priority: int = 0
    memory_size: int = 0
    pc: int = 0
    registers: Dict[str, int] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Process(pid={self.pid}, name='{self.name}', state={self.state.value})"


@dataclass
class MemoryBlock:
    """
    Represents a block of memory.

    Attributes:
        address: Starting address
        size: Size in bytes
        content: Content (as bytes or int)
        is_allocated: Whether this block is allocated
        process_id: ID of process owning this block (if allocated)
    """

    address: int
    size: int
    content: Any = 0
    is_allocated: bool = False
    process_id: Optional[int] = None

    @property
    def end_address(self) -> int:
        """Get the end address of this block."""
        return self.address + self.size - 1

    def contains(self, addr: int) -> bool:
        """Check if this block contains an address."""
        return self.address <= addr <= self.end_address

    def __str__(self) -> str:
        status = "allocated" if self.is_allocated else "free"
        return f"MemoryBlock(0x{self.address:X}, size={self.size}, {status})"


@dataclass
class PageTableEntry:
    """
    Represents an entry in a page table.

    Attributes:
        page_number: Virtual page number
        frame_number: Physical frame number
        present: Whether page is present in memory
        read_only: Whether page is read-only
        dirty: Whether page has been modified
        accessed: Whether page has been accessed
    """

    page_number: int
    frame_number: int = 0
    present: bool = False
    read_only: bool = False
    dirty: bool = False
    accessed: bool = False

    def __str__(self) -> str:
        flags = []
        if self.present:
            flags.append("P")
        if self.read_only:
            flags.append("RO")
        if self.dirty:
            flags.append("D")
        if self.accessed:
            flags.append("A")

        flags_str = ",".join(flags) if flags else "-"
        return f"PTE[{self.page_number}] -> F{self.frame_number} [{flags_str}]"


@dataclass
class PageTable:
    """
    Represents a page table for memory management.

    Attributes:
        entries: Dictionary mapping page number to entry
        page_size: Size of each page in bytes
    """

    entries: Dict[int, PageTableEntry] = field(default_factory=dict)
    page_size: int = 4096  # 4KB pages

    def add_entry(self, entry: PageTableEntry) -> None:
        """Add or update a page table entry."""
        self.entries[entry.page_number] = entry

    def get_entry(self, page_number: int) -> Optional[PageTableEntry]:
        """Get a page table entry."""
        return self.entries.get(page_number)

    def translate(self, virtual_address: int) -> Optional[int]:
        """
        Translate virtual address to physical address.

        Args:
            virtual_address: Virtual address to translate

        Returns:
            Physical address, or None if page not present
        """
        page_number = virtual_address // self.page_size
        offset = virtual_address % self.page_size

        entry = self.get_entry(page_number)
        if entry is None or not entry.present:
            return None

        physical_address = entry.frame_number * self.page_size + offset
        return physical_address


@dataclass
class CPU:
    """
    Represents a CPU with registers and execution state.

    Attributes:
        registers: CPU register values
        pc: Program counter
        flags: CPU flags (zero, carry, etc.)
        current_process: Currently running process
    """

    registers: Dict[str, int] = field(default_factory=dict)
    pc: int = 0
    flags: Dict[str, bool] = field(default_factory=dict)
    current_process: Optional[Process] = None

    def set_register(self, name: str, value: int) -> None:
        """Set a register value."""
        self.registers[name.upper()] = value

    def get_register(self, name: str) -> int:
        """Get a register value."""
        return self.registers.get(name.upper(), 0)

    def set_flag(self, name: str, value: bool) -> None:
        """Set a CPU flag."""
        self.flags[name.upper()] = value

    def get_flag(self, name: str) -> bool:
        """Get a CPU flag."""
        return self.flags.get(name.upper(), False)

    def step(self) -> None:
        """Execute one instruction (increment PC)."""
        self.pc += 1

    def __str__(self) -> str:
        proc_name = self.current_process.name if self.current_process else "idle"
        return f"CPU(PC={self.pc}, running={proc_name})"


@dataclass
class Instruction:
    """
    Represents a machine instruction.

    Attributes:
        opcode: Operation code
        operands: Instruction operands
        address: Instruction address in memory
        mnemonic: Human-readable mnemonic
    """

    opcode: str
    operands: List[str] = field(default_factory=list)
    address: int = 0
    mnemonic: str = ""

    def __str__(self) -> str:
        if self.operands:
            return f"{self.opcode} {', '.join(self.operands)}"
        return self.opcode


@dataclass
class CodeBlock:
    """
    Represents a block of code.

    Attributes:
        code: Source code string
        language: Programming language
        start_address: Starting address (for assembly)
        instructions: List of instructions (for assembly)
    """

    code: str
    language: str = "C"
    start_address: int = 0
    instructions: List[Instruction] = field(default_factory=list)

    def __str__(self) -> str:
        lines = self.code.strip().split('\n')
        preview = lines[0] if lines else ""
        return f"CodeBlock({self.language}, '{preview[:30]}...')"


@dataclass
class StackFrame:
    """
    Represents a stack frame.

    Attributes:
        base_pointer: Base pointer address
        return_address: Return address
        local_variables: Local variable values
        arguments: Function argument values
    """

    base_pointer: int
    return_address: int = 0
    local_variables: Dict[str, int] = field(default_factory=dict)
    arguments: Dict[str, int] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"StackFrame(bp=0x{self.base_pointer:X}, {len(self.local_variables)} locals)"


@dataclass
class FileDescriptor:
    """
    Represents a file descriptor.

    Attributes:
        fd: File descriptor number
        filename: Name of the file
        offset: Current file offset
        flags: File flags (read, write, etc.)
    """

    fd: int
    filename: str
    offset: int = 0
    flags: Dict[str, bool] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"FD({self.fd}, '{self.filename}')"


@dataclass
class IORequest:
    """
    Represents an I/O request.

    Attributes:
        request_id: Unique request ID
        process_id: Process making the request
        device: Device name (e.g., "disk", "keyboard")
        operation: Operation type ("read", "write")
        address: Memory address for data
        size: Number of bytes
    """

    request_id: int
    process_id: int
    device: str
    operation: str
    address: int
    size: int

    def __str__(self) -> str:
        return f"IORequest(id={self.request_id}, pid={self.process_id}, {self.device}.{self.operation})"


# Factory functions for creating common entities

def create_process(pid: int, name: str, **kwargs) -> Process:
    """Create a Process with common defaults."""
    return Process(pid=pid, name=name, **kwargs)


def create_memory_block(
    address: int,
    size: int,
    content: Any = 0,
    is_allocated: bool = False
) -> MemoryBlock:
    """Create a MemoryBlock."""
    return MemoryBlock(
        address=address,
        size=size,
        content=content,
        is_allocated=is_allocated
    )


def create_cpu() -> CPU:
    """Create a CPU with default registers."""
    return CPU(
        registers={
            'EAX': 0, 'EBX': 0, 'ECX': 0, 'EDX': 0,
            'ESI': 0, 'EDI': 0, 'ESP': 0, 'EBP': 0,
            'EIP': 0
        },
        flags={
            'ZF': False, 'CF': False, 'SF': False, 'OF': False
        }
    )


def create_page_table(num_pages: int, page_size: int = 4096) -> PageTable:
    """Create an empty page table."""
    entries = {}
    for i in range(num_pages):
        entries[i] = PageTableEntry(page_number=i, present=False)
    return PageTable(entries=entries, page_size=page_size)
