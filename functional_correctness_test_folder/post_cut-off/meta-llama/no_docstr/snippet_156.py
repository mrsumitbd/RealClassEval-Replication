
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DiffHunk:
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        if self.lines[diff_line_offset].startswith('+'):
            return self.new_start + self._count_preceding_new_lines(diff_line_offset)
        elif self.lines[diff_line_offset].startswith('-'):
            return None
        else:
            return self.new_start + self._count_preceding_new_lines(diff_line_offset) - self._count_preceding_removed_lines(diff_line_offset)

    def contains_line_change(self, content: str) -> List[int]:
        result = []
        for i, line in enumerate(self.lines):
            if line.lstrip().startswith('+') and content in line:
                result.append(self.get_new_line_number(i))
        return [line for line in result if line is not None]

    def _count_preceding_new_lines(self, diff_line_offset: int) -> int:
        return sum(1 for i in range(diff_line_offset + 1) if self.lines[i].startswith('+') or not self.lines[i].startswith('-'))

    def _count_preceding_removed_lines(self, diff_line_offset: int) -> int:
        return sum(1 for i in range(diff_line_offset + 1) if self.lines[i].startswith('-'))
