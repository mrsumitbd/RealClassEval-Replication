
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    """
    Represents a single diff hunk with line mappings.

    Attributes
    ----------
    old_start : int
        The first line number in the original file that this hunk starts at.
    new_start : int
        The first line number in the new file that this hunk starts at.
    old_lines : List[str]
        Lines from the original file that belong to this hunk.
    new_lines : List[str]
        Lines from the new file that belong to this hunk.
    """

    old_start: int
    new_start: int
    old_lines: List[str]
    new_lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Get the absolute line number in the new file for a given offset within this hunk.

        Parameters
        ----------
        diff_line_offset : int
            Zero‑based offset into the list of new lines for this hunk.

        Returns
        -------
        Optional[int]
            The absolute line number in the new file if the offset is valid,
            otherwise ``None``.
        """
        if 0 <= diff_line_offset < len(self.new_lines):
            return self.new_start + diff_line_offset
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """
        Find line numbers where the given content appears in changes.

        Parameters
        ----------
        content : str
            The string to search for in the new lines of this hunk.

        Returns
        -------
        List[int]
            A list of absolute line numbers in the new file where the content
            appears. The list is sorted in ascending order.
        """
        return [
            self.new_start + idx
            for idx, line in enumerate(self.new_lines)
            if content in line
        ]
