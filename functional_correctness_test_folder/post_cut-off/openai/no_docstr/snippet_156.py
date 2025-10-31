
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DiffHunk:
    """
    Represents a single hunk of a unified diff.

    Attributes
    ----------
    old_start : int
        The starting line number in the original file.
    old_lines : int
        The number of lines the hunk applies to in the original file.
    new_start : int
        The starting line number in the new file.
    new_lines : int
        The number of lines the hunk applies to in the new file.
    lines : List[str]
        The raw lines of the hunk, each beginning with one of
        '+', '-', or ' '.
    """
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    lines: List[str] = field(default_factory=list)

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Return the new file line number that corresponds to the line at
        ``diff_line_offset`` in the hunk, if that line is an addition.
        For context or deletion lines, return ``None``.

        Parameters
        ----------
        diff_line_offset : int
            Zero‑based index into ``self.lines``.

        Returns
        -------
        Optional[int]
            The new file line number or ``None`` if the line is not an
            addition.
        """
        if diff_line_offset < 0 or diff_line_offset >= len(self.lines):
            return None

        new_line_num = self.new_start
        for i, line in enumerate(self.lines):
            if i == diff_line_offset:
                if line.startswith('+'):
                    return new_line_num
                else:
                    return None

            if line.startswith(' '):
                new_line_num += 1
            elif line.startswith('+'):
                new_line_num += 1
            # deletions ('-') do not consume a new line number

        return None

    def contains_line_change(self, content: str) -> List[int]:
        """
        Return a list of indices of lines in the hunk that contain the
        given ``content`` string and represent a change (addition or
        deletion).

        Parameters
        ----------
        content : str
            The substring to search for.

        Returns
        -------
        List[int]
            Indices of matching lines within ``self.lines``.
        """
        matches: List[int] = []
        for idx, line in enumerate(self.lines):
            if content in line and line[0] in ('+', '-'):
                matches.append(idx)
        return matches
