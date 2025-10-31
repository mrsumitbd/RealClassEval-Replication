
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
        line_prefix = self.lines[diff_line_offset][0]
        if line_prefix == '-':
            return None
        return self.new_start + (diff_line_offset - self.lines[:diff_line_offset+1].count('-'))

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        changed_lines = []
        for i, line in enumerate(self.lines):
            if (line.startswith('+') or line.startswith('-')) and content in line[1:]:
                if line.startswith('+'):
                    changed_lines.append(
                        self.new_start + i - self.lines[:i].count('-'))
                else:
                    # For removed lines, we don't have a corresponding new line number
                    # But we can still return the old line number for context
                    changed_lines.append(
                        self.old_start + i - self.lines[:i].count('+'))
        return changed_lines
