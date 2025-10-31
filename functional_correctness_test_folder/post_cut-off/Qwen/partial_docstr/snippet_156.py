
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
    line_map: Dict[int, int] = field(default_factory=dict)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        if diff_line_offset in self.line_map:
            return self.line_map[diff_line_offset]
        return None

    def contains_line_change(self, content: str) -> List[int]:
        changed_lines = []
        for i, line in enumerate(self.lines):
            if line.startswith('+') and not line.startswith('++'):
                changed_lines.append(self.new_start + i)
            elif line.startswith('-') and not line.startswith('--'):
                changed_lines.append(self.old_start + i)
        return changed_lines
