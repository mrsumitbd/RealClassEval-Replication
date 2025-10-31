
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        line = self.lines[diff_line_offset]
        if line.startswith('-'):
            return None
        elif line.startswith('+'):
            return self.new_start + diff_line_offset
        else:
            return self.new_start + diff_line_offset

    def contains_line_change(self, content: str) -> List[int]:
        line_numbers = []
        for i, line in enumerate(self.lines):
            if line.startswith('+') and line[1:] in content:
                line_numbers.append(self.new_start + i)
        return line_numbers
