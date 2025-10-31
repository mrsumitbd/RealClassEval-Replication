
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        '''Get the absolute line number in the new file for a given offset within this hunk.'''
        if 0 <= diff_line_offset < len(self.lines):
            line = self.lines[diff_line_offset]
            if not line.startswith('-'):
                return self.new_start + diff_line_offset
        return None

    def contains_line_change(self, content: str) -> List[int]:
        '''Find line numbers where the given content appears in changes.'''
        line_numbers = []
        for i, line in enumerate(self.lines):
            if line.startswith('+') and content in line[1:]:
                line_numbers.append(self.new_start + i)
        return line_numbers
