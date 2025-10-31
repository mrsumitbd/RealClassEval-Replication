from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    # Each item: (prefix, text) where prefix in {' ', '+', '-'}
    lines: List[Tuple[str, str]]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None

        new_line_num = self.new_start
        for idx, (prefix, _) in enumerate(self.lines):
            if idx == diff_line_offset:
                if prefix in (' ', '+'):
                    return new_line_num
                return None
            if prefix in (' ', '+'):
                new_line_num += 1
        return None

    def contains_line_change(self, content: str) -> List[int]:
        matches: List[int] = []
        for idx, (prefix, text) in enumerate(self.lines):
            if prefix in ('+', '-') and content in text:
                matches.append(idx)
        return matches
