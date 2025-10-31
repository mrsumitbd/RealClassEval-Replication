
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffHunk:
    old_start: int = field(default=0)
    old_count: int = field(default=0)
    new_start: int = field(default=0)
    new_count: int = field(default=0)
    lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Given an offset (0-based) into the hunk's lines, return the corresponding
        new file line number, or None if the line is a deletion (i.e., starts with '-').
        """
        new_line_num = self.new_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if line.startswith('-'):
                    return None
                elif line.startswith('+') or line.startswith(' '):
                    return new_line_num
            if not line.startswith('-'):
                new_line_num += 1
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """
        Returns a list of line indices in the hunk where the line content matches `content`
        and the line is either an addition or a deletion (not context).
        """
        indices = []
        for idx, line in enumerate(self.lines):
            if (line.startswith('+') or line.startswith('-')) and line[1:] == content:
                indices.append(idx)
        return indices
