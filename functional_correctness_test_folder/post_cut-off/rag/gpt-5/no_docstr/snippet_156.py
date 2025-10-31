from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""
    old_start: int
    new_start: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            raise IndexError("diff_line_offset out of range")

        new_line_num = self.new_start
        for i in range(diff_line_offset):
            line = self.lines[i]
            if line and line[0] in (' ', '+'):
                new_line_num += 1

        current_line = self.lines[diff_line_offset]
        if current_line and current_line[0] == '-':
            return None
        return new_line_num

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        result: List[int] = []
        new_line_num = self.new_start

        for line in self.lines:
            prefix = line[0] if line else ' '
            body = line[1:] if line else ''

            if prefix == '+':
                if content in body:
                    result.append(new_line_num)
                new_line_num += 1
            elif prefix == ' ':
                new_line_num += 1
            # '-' does not affect new_line_num

        return result
