from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None
        new_line_num = self.new_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if line.startswith("-"):
                    return None
                return new_line_num
            if not line.startswith("-"):
                new_line_num += 1
        return None

    def contains_line_change(self, content: str) -> List[int]:
        result: List[int] = []
        for idx, line in enumerate(self.lines):
            if line.startswith(("+", "-")) and content in line[1:]:
                result.append(idx)
        return result
