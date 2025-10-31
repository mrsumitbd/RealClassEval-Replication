
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DiffHunk:
    """Represents a single diff hunk with line mappings."""

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """Get the absolute line number in the new file for a given offset within this hunk."""
        pass

    def contains_line_change(self, content: str) -> List[int]:
        """Find line numbers where the given content appears in changes."""
        pass
