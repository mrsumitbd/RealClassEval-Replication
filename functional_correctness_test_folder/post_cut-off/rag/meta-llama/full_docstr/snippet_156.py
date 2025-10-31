
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        if self.lines[diff_line_offset].startswith('-'):
            return None
        return self.new_start + sum(1 for line in self.lines[:diff_line_offset+1] if not line.startswith('-'))

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        return [self.new_start + i for i, line in enumerate(self.lines) if (line.startswith('+') or line.startswith('-')) and content in line]
