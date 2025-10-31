
import re
from typing import Tuple, List


class ConditionalTracker:
    """
    Tracks conditional blocks in a simple line‑by‑line language.
    Supports `if`, `elif`, `else`, and `end` statements.
    """

    def __init__(self) -> None:
        # Stack of active conditions (outermost first)
        self._conditions: List[str] = []
        # Stack of indentation levels corresponding to the conditions
        self._indent_levels: List[int] = []

    def process_line(self, line: str, line_index: int) -> Tuple[int, Tuple[str, ...]]:
        """
        Process a single line of code and update the internal state.
        Returns a tuple (line_index, current_context) where current_context
        is a tuple of active conditions for this line.
        """
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Pop conditions that are no longer in scope
        while self._indent_levels and indent < self._indent_levels[-1]:
            self._indent_levels.pop()
            self._conditions.pop()

        # Handle conditional statements
        if stripped.startswith("if "):
            cond = stripped[3:].rstrip(":").strip()
            self._indent_levels.append(indent)
            self._conditions.append(cond)
        elif stripped.startswith("elif "):
            cond = stripped[5:].rstrip(":").strip()
            if self._conditions:
                self._conditions[-1] = cond
