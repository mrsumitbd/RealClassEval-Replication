
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    # lines in the hunk, including diff markers (' ', '+', '-')
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Given a line offset (0-based) within the hunk, return the corresponding new file line number,
        or None if the line is a deletion (i.e., starts with '-').
        """
        new_line_num = self.new_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if line.startswith('-'):
                    return None
                elif line.startswith('+') or line.startswith(' '):
                    return new_line_num
            if line.startswith('+') or line.startswith(' '):
                new_line_num += 1
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """
        Returns a list of new file line numbers (1-based) where the given content appears as an addition.
        """
        result = []
        new_line_num = self.new_start
        for line in self.lines:
            if line.startswith('+') and line[1:] == content:
                result.append(new_line_num)
            if line.startswith('+') or line.startswith(' '):
                new_line_num += 1
        return result
