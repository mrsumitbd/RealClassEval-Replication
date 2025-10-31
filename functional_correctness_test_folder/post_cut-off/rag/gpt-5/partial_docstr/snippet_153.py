import re
from typing import List, Tuple


class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self._stack: List[int] = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        context = tuple(self._stack)
        s = line.lstrip()

        if not s or s.startswith("#"):
            return context

        def starts_with(token: str, text: str) -> bool:
            if not text.startswith(token):
                return False
            if len(text) == len(token):
                return True
            nxt = text[len(token)]
            return nxt.isspace() or nxt in "([#"

        while True:
            s = s.lstrip()
            if not s or s.startswith("#"):
                break

            matched = False

            # else
            if starts_with("else", s):
                if not self._stack:
                    raise ValueError(f"Unmatched 'else' at line {line_index}")
                self._stack[-1] = 1
                s = s[4:].lstrip()
                matched = True
                # continue to allow "else ifeq ..."
                continue

            # endif
            if starts_with("endif", s):
                if not self._stack:
                    raise ValueError(f"Unmatched 'endif' at line {line_index}")
                self._stack.pop()
                s = s[5:].lstrip()
                matched = True
                continue

            # if-variants
            for token in ("ifeq", "ifneq", "ifdef", "ifndef"):
                if starts_with(token, s):
                    self._stack.append(0)
                    s = s[len(token):].lstrip()
                    matched = True
                    break

            if not matched:
                break

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
