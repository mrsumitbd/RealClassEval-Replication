
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    new_start: int
    old_lines: int
    new_lines: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        current_new_line = self.new_start
        current_old_line = self.old_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if line.startswith('+'):
                    return current_new_line
                elif line.startswith('-'):
                    return None
                else:
                    return current_new_line
            if not line.startswith('-'):
                current_new_line += 1
            if not line.startswith('+'):
                current_old_line += 1
        return None

    def contains_line_change(self, content: str) -> List[int]:
        changed_lines = []
        current_new_line = self.new_start
        for i, line in enumerate(self.lines):
            if line.startswith('+') and content in line[1:].strip():
                changed_lines.append(current_new_line)
                current_new_line += 1
            elif not line.startswith('-'):
                current_new_line += 1
        return changed_lines
