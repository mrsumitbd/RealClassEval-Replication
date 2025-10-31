class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

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
        # The context for the current line is the state before any directive on this line takes effect
        context = tuple(self._stack)

        stripped = line.lstrip()
        # Ignore pure comment lines
        if not stripped or stripped.startswith('#'):
            return context

        def _starts_with_directive(s: str, name: str) -> bool:
            if not s.startswith(name):
                return False
            if len(s) == len(name):
                return True
            ch = s[len(name)]
            return ch.isspace() or ch in '()'

        # Open new conditional level after the line if this is an if*
        if (_starts_with_directive(stripped, 'ifeq')
                or _starts_with_directive(stripped, 'ifneq')
                or _starts_with_directive(stripped, 'ifdef')
                or _starts_with_directive(stripped, 'ifndef')):
            # Enter the "then" branch (0) for the following lines
            self._stack.append(0)
            return context

        # Switch branch on else
        if _starts_with_directive(stripped, 'else'):
            if self._stack:
                self._stack[-1] = 1
            return context

        # Close conditional level on endif
        if _starts_with_directive(stripped, 'endif'):
            if self._stack:
                self._stack.pop()
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
