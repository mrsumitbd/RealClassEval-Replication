from dataclasses import dataclass
from typing import List, Optional, Tuple, Union


@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""
    old_start: int
    old_len: int
    new_start: int
    new_len: int
    lines: List[Tuple[str, str]]

    def __init__(
        self,
        old_start: int,
        old_len: int,
        new_start: int,
        new_len: int,
        lines: List[Union[str, Tuple[str, str]]],
    ):
        self.old_start = old_start
        self.old_len = old_len
        self.new_start = new_start
        self.new_len = new_len
        self.lines = []
        for entry in lines:
            if isinstance(entry, tuple) and len(entry) == 2:
                tag, text = entry
            elif isinstance(entry, str):
                if entry:
                    tag = entry[0]
                    text = entry[1:]
                else:
                    tag, text = ' ', ''
            else:
                raise TypeError(
                    "Each line must be a str or a (tag, text) tuple")
            if tag not in {' ', '+', '-'}:
                # Fallback: treat unknown tag as context
                text = f"{tag}{text}"
                tag = ' '
            self.lines.append((tag, text))

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None

        current_new_line = self.new_start
        for idx, (tag, _text) in enumerate(self.lines):
            if idx == diff_line_offset:
                if tag in (' ', '+'):
                    return current_new_line
                return None
            if tag in (' ', '+'):
                current_new_line += 1
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        result: List[int] = []
        current_new_line = self.new_start
        for tag, text in self.lines:
            if tag in (' ', '+'):
                if tag == '+' and content in text:
                    result.append(current_new_line)
                current_new_line += 1
            # Deletions do not exist in the new file; skip line number increment
        return result
