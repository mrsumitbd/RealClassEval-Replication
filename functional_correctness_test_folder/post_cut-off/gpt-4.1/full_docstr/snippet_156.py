
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    # lines as in diff, with '+', '-', ' ' prefixes
    lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        '''Get the absolute line number in the new file for a given offset within this hunk.'''
        new_line_num = self.new_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if line.startswith('-'):
                    return None
                return new_line_num
            if line.startswith('+'):
                new_line_num += 1
            elif line.startswith(' '):
                new_line_num += 1
            # if line.startswith('-'): do not increment new_line_num
        return None

    def contains_line_change(self, content: str) -> List[int]:
        '''Find line numbers where the given content appears in changes.'''
        result = []
        new_line_num = self.new_start
        for line in self.lines:
            if line.startswith('+') or line.startswith('-'):
                if line[1:] == content:
                    if line.startswith('+'):
                        result.append(new_line_num)
                    elif line.startswith('-'):
                        # -1 to indicate deletion (no new line number)
                        result.append(-1)
            if line.startswith('+'):
                new_line_num += 1
            elif line.startswith(' '):
                new_line_num += 1
        return result
