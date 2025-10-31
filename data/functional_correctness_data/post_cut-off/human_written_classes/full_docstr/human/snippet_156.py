from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        target_line = self.lines[diff_line_offset]
        if target_line.startswith('-'):
            return None
        lines_before = 0
        for i in range(diff_line_offset):
            if not self.lines[i].startswith('-'):
                lines_before += 1
        return self.new_start + lines_before

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        matches = []
        current_new_line = self.new_start
        for line in self.lines:
            if line.startswith('+') and content.lower() in line.lower():
                matches.append(current_new_line)
            if not line.startswith('-'):
                current_new_line += 1
        return matches