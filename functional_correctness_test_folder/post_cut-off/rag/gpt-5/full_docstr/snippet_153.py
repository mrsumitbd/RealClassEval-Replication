import re
from typing import Tuple


class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    _RE_IF = re.compile(r'^\s*(ifeq|ifneq|ifdef|ifndef)\b')
    _RE_ELSEIF = re.compile(r'^\s*else\s+(ifeq|ifneq|ifdef|ifndef)\b')
    _RE_ELSE = re.compile(r'^\s*else\b')
    _RE_ENDIF = re.compile(r'^\s*endif\b')
    _RE_COMMENT = re.compile(r'^\s*#')

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self._stack: list[int] = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        # Current context before applying this line's directive
        context: Tuple[int, ...] = tuple(self._stack)

        # Ignore recipe lines and full-line comments
        if line.startswith('\t') or self._RE_COMMENT.match(line):
            return context

        stripped = line.strip()

        # Apply directive effects after capturing current context
        if self._RE_ENDIF.match(stripped):
            if self._stack:
                self._stack.pop()
            return context

        if self._RE_ELSEIF.match(stripped) or self._RE_ELSE.match(stripped):
            if self._stack:
                self._stack[-1] += 1
            return context

        if self._RE_IF.match(stripped):
            self._stack.append(0)
            return context

        return context

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self._stack.clear()

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        '''Check if two conditional contexts are mutually exclusive.
        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.
        Args:
            context1: First conditional context
            context2: Second conditional context
        Returns:
            True if contexts are mutually exclusive
        '''
        min_len = min(len(context1), len(context2))
        for i in range(min_len):
            if context1[i] != context2[i]:
                return True
        return False
