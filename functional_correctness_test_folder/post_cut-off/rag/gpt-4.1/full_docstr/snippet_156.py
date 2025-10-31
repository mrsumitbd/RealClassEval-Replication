from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        new_line_num = self.new_start
        cur_offset = 0
        for line in self.lines:
            if line.startswith('+') or line.startswith(' '):
                if cur_offset == diff_line_offset:
                    return new_line_num
                new_line_num += 1
                cur_offset += 1 if not line.startswith('-') else 0
            elif line.startswith('-'):
                continue
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        result = []
        new_line_num = self.new_start
        for line in self.lines:
            if line.startswith('+') or line.startswith(' '):
                if content in line[1:]:
                    result.append(new_line_num)
                new_line_num += 1
        return result
