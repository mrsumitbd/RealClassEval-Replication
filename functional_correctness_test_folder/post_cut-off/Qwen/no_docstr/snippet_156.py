
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffHunk:
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if 0 <= diff_line_offset < len(self.lines):
            line = self.lines[diff_line_offset]
            if line.startswith('+'):
                return self.new_start + diff_line_offset
        return None

    def contains_line_change(self, content: str) -> List[int]:
        line_numbers = []
        for i, line in enumerate(self.lines):
            if line.startswith('+') or line.startswith('-'):
                if content in line[1:]:
                    line_numbers.append(
                        self.new_start + i if line.startswith('+') else self.old_start + i)
        return line_numbers
