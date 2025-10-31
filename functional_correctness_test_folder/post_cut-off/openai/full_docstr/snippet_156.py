
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    """
    Represents a single diff hunk with line mappings.

    Attributes
    ----------
    old_start : int
        The starting line number in the original file for this hunk.
    old_lines : int
        The number of lines in the original file that this hunk covers.
    new_start : int
        The starting line number in the new file for this hunk.
    new_lines : int
        The number of lines in the new file that this hunk covers.
    lines : List[str]
        The list of lines in the hunk, each prefixed with ' ', '+', or '-'.
    """

    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Get the absolute line number in the new file for a given offset within this hunk.

        Parameters
        ----------
        diff_line_offset : int
            The zero‑based index of the line within the hunk.

        Returns
        -------
        Optional[int]
            The absolute line number in the new file if the line is part of the new file
            (i.e., not a deletion).  Returns ``None`` if the line is a deletion.
        """
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            raise IndexError("diff_line_offset out of range")

        new_line_num = self.new_start - 1  # will be incremented before first line
        for i, line in enumerate(self.lines):
            if line[0] != '-':
                new_line_num += 1
            if i == diff_line_offset:
                return new_line_num if line[0] != '-' else None
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """
        Find line numbers where the given content appears in changes.

        Parameters
        ----------
        content : str
            The string to search for within added lines.

        Returns
        -------
        List[int]
            A list of absolute line numbers in the new file where the content appears
            in added lines.  Lines that are deletions are ignored.
        """
        result: List[int] = []
        for offset, line in enumerate(self.lines):
            if line.startswith('+') and content in line[1:]:
                new_line = self.get_new_line_number(offset)
                if new_line is not None:
                    result.append(new_line)
        return result
