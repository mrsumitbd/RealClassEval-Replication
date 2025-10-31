
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    """
    Represents a single diff hunk with line mappings.

    Attributes
    ----------
    new_start_line : int
        The first line number in the new file that this hunk starts at.
    lines : List[str]
        The raw lines of the hunk, including the leading diff markers
        ('+', '-', or ' ').
    """

    new_start_line: int
    lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Get the absolute line number in the new file for a given offset within this hunk.

        Parameters
        ----------
        diff_line_offset : int
            Zero‑based index into ``self.lines``.

        Returns
        -------
        Optional[int]
            The line number in the new file if the line exists in the new file
            (i.e. it is an addition or context line).  ``None`` is returned
            for deletion lines which do not appear in the new file.
        """
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            raise IndexError("diff_line_offset out of range")

        new_line = self.new_start_line
        for idx, line in enumerate(self.lines):
            if idx == diff_line_offset:
                if line.startswith(("+", " ")):
                    return new_line
                else:
                    return None

            # Update the line counter after processing the current line
            if line.startswith(("+", " ")):
                new_line += 1
            # Deletion lines do not increment the new file line counter

        # Should never reach here
        return None

    def contains_line_change(self, content: str) -> List[int]:
        """
        Find line numbers where the given content appears in changes.

        Parameters
        ----------
        content : str
            The string to search for within the hunk.

        Returns
        -------
        List[int]
            A list of line numbers in the new file where the content appears
            in an added line.  Context lines are ignored because they are not
            considered changes.
        """
        new_line = self.new_start_line
        matches: List[int] = []

        for line in self.lines:
            if line.startswith("+"):
                # This is an added line; check for the content
                if content in line[1:]:
                    matches.append(new_line)
                new_line += 1
            elif line.startswith(" "):
                # Context line – skip for matching but still increment
                new_line += 1
            # Deletion lines do not affect the new file line counter

        return matches
