from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    '''Represents a single diff hunk with line mappings.'''
    new_start: int
    lines: List[str]

    def _is_add(self, line: str) -> bool:
        return line.startswith("+")

    def _is_del(self, line: str) -> bool:
        return line.startswith("-")

    def _is_context(self, line: str) -> bool:
        return line.startswith(" ") or (not self._is_add(line) and not self._is_del(line))

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        '''Get the absolute line number in the new file for a given offset within this hunk.'''
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None

        new_line_num = self.new_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if self._is_del(line):
                    return None
                return new_line_num
            if self._is_add(line) or self._is_context(line):
                new_line_num += 1

        return None

    def contains_line_change(self, content: str) -> List[int]:
        '''Find line numbers where the given content appears in changes.'''
        results: List[int] = []
        new_line_num = self.new_start

        for line in self.lines:
            if self._is_add(line):
                if content in line[1:]:
                    results.append(new_line_num)
                new_line_num += 1
            elif self._is_context(line):
                new_line_num += 1
            else:
                # Deletion line: does not advance new line numbering
                pass

        return results
