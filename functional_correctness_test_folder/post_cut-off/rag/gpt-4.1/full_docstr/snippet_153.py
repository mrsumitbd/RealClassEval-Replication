
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    CONDITIONAL_STARTS = ('ifeq', 'ifneq', 'ifdef', 'ifndef')
    CONDITIONAL_ELSE = ('else',)
    CONDITIONAL_END = ('endif',)

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self.stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        stripped = line.strip()
        tokens = stripped.split()
        # Save context before processing this line
        context = tuple(self.stack)
        if not tokens:
            return context
        keyword = tokens[0]
        if keyword in self.CONDITIONAL_STARTS:
            # Use line_index to uniquely identify this conditional block
            self.stack.append((keyword, line_index))
        elif keyword in self.CONDITIONAL_ELSE:
            if self.stack:
                prev = self.stack.pop()
                # Mark as 'else' branch for this conditional
                self.stack.append((f"{prev[0]}:else", prev[1]))
        elif keyword in self.CONDITIONAL_END:
            if self.stack:
                self.stack.pop()
        return context

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.stack = []

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
        minlen = min(len(context1), len(context2))
        for i in range(minlen):
            if context1[i] != context2[i]:
                return True
        return False
