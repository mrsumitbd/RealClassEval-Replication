
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiffHunk:
    """
    Represents a single diff hunk with line mappings.
    """
    # The line number in the new file where this hunk starts
    new_start: int
    # The list of lines in the hunk, each line starts with one of:
    #   ' '  context line
    #   '+'  addition
    #   '-'  deletion
    diff_lines: List[str]

    def get_new_line_number(self, diff_line_offset: int) -> Optional[int]:
        """
        Return the new file line number corresponding to the given offset
        within the hunk. If the line at the offset is a deletion ('-'),
        return None because it does not exist in the new file.
        """
        if diff_line_offset < 0 or diff_line_offset >= len(self.diff_lines):
            return None

        # Count how many new lines have been seen up to this offset
        new_line_counter = 0
        for i in range(diff_line_offset):
            line = self.diff_lines[i]
            if line.startswith(('+', ' ')):
                new_line_counter += 1

        line = self.diff_lines[diff_line_offset]
        if line.startswith('-'):
            return None
        # For context or addition lines, the new line number is the start
        # plus the number of new lines seen before this line
        return self.new_start + new_line_counter

    def contains_line_change(self, content: str) -> List[int]:
        """
        Return a list of new file line numbers where the hunk contains a
        change (addition or deletion) that matches the given content.
        """
        matches: List[int] = []
        for offset, line in enumerate(self.diff_lines):
            # Skip context lines
            if not line.startswith(('+', '-')):
                continue
            # Compare the content after the diff marker
            if line[1:] == content:
                new_line_num = self.get_new_line_number(offset)
                if new_line_num is not None:
                    matches.append(new_line_num)
        return matches
