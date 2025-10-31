
from dataclasses import dataclass
from typing import Optional, List


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
        line = self.changes[diff_line_offset]
        if line.startswith('+'):
            return self.new_start + sum(1 for change in self.changes[:diff_line_offset] if change.startswith('+'))
        elif line.startswith(' '):
            return self.new_start + sum(1 for change in self.changes[:diff_line_offset] if change.startswith('+'))
        else:
            return None

    def contains_line_change(self, content: str) -> List[int]:
        '''Find line numbers where the given content appears in changes.'''
        result = []
        current_new_line = self.new_start
        for change in self.changes:
            if change.startswith('+'):
                if content in change[1:].strip():
                    result.append(current_new_line)
                current_new_line += 1
            elif change.startswith(' '):
                current_new_line += 1
        return result
