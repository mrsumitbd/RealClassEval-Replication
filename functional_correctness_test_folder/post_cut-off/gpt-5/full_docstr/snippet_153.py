class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self._stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        # Context for this line is the current state before any directive on this line is applied
        context_for_line = tuple(self._stack)

        s = line.lstrip()
        if not s or s.startswith('#'):
            return context_for_line

        # Normalize spacing for directive checks
        lower = s.lower()

        def starts_with_kw(text, kw):
            if not text.startswith(kw):
                return False
            if len(text) == len(kw):
                return True
            ch = text[len(kw)]
            return ch.isspace() or ch in '()'  # allow forms like ifeq (a,b)

        # Handle else-if form: "else ifeq ..." which is effectively "else" then "ifeq ..."
        if starts_with_kw(lower, 'else'):
            # Toggle current branch if inside a conditional
            if self._stack:
                self._stack[-1] = 1 if self._stack[-1] == 0 else 0
            # Check for immediate nested if after else
            rest = lower[4:].lstrip()
            if starts_with_kw(rest, 'ifeq') or starts_with_kw(rest, 'ifneq') or starts_with_kw(rest, 'ifdef') or starts_with_kw(rest, 'ifndef'):
                self._stack.append(0)
            return context_for_line

        # Handle starting conditionals
        if starts_with_kw(lower, 'ifeq') or starts_with_kw(lower, 'ifneq') or starts_with_kw(lower, 'ifdef') or starts_with_kw(lower, 'ifndef'):
            self._stack.append(0)
            return context_for_line

        # Handle endif
        if starts_with_kw(lower, 'endif'):
            if self._stack:
                self._stack.pop()
            return context_for_line

        return context_for_line

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
