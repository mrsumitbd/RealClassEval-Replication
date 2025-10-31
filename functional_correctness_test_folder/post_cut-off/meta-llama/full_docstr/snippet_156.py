
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
        '''Get the absolute line number in the new file for a given offset within this hunk.'''
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        line = self.lines[diff_line_offset]
        if line.startswith('-'):
            return None
        if line.startswith(' '):
            return self.new_start + diff_line_offset - sum(1 for l in self.lines[:diff_line_offset] if l.startswith('-'))
        return self.new_start + diff_line_offset - sum(1 for l in self.lines[:diff_line_offset] if l.startswith('-'))

    def contains_line_change(self, content: str) -> List[int]:
        '''Find line numbers where the given content appears in changes.'''
        result = []
        for i, line in enumerate(self.lines):
            if (line.startswith('+') or line.startswith('-')) and content in line[1:].strip():
                new_line_number = self.get_new_line_number(i)
                if new_line_number is not None:
                    result.append(new_line_number)
        return result
