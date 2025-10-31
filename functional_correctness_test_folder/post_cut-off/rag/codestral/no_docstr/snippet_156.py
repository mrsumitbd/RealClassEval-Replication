
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    changes: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        '''Get the absolute line number in the new file for a given offset within this hunk.'''
        if diff_line_offset < 0 or diff_line_offset >= len(self.changes):
            return None
        return self.new_start + diff_line_offset

    def contains_line_change(self, content: str) -> List[int]:
        '''Find line numbers where the given content appears in changes.'''
        line_numbers = []
        for i, line in enumerate(self.changes):
            if content in line:
                line_numbers.append(self.new_start + i)
        return line_numbers
