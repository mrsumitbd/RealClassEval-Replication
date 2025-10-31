from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""
    old_start: int
    new_start: int
    diff_lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        if diff_line_offset < 0 or diff_line_offset >= len(self.diff_lines):
            return None

        new_line = self.new_start
        for idx, raw in enumerate(self.diff_lines):
            # Ignore special marker lines like "\ No newline at end of file"
            if raw.startswith("\\"):
                if idx == diff_line_offset:
                    return None
                continue

            tag = raw[0] if raw else " "
            if idx == diff_line_offset:
                if tag == "-":
                    return None
                return new_line

            if tag in (" ", "+"):
                new_line += 1

        return None

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        result: List[int] = []
        new_line = self.new_start

        for raw in self.diff_lines:
            if raw.startswith("\\"):
                continue

            tag = raw[0] if raw else " "
            text = raw[1:] if raw else ""

            if tag == "+":
                if content in text:
                    result.append(new_line)
                new_line += 1
            elif tag == " ":
                new_line += 1
            # '-' lines do not exist in the new file and do not increment new_line

        return result
