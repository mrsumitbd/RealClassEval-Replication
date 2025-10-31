
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    # Recognized conditional keywords in Makefiles
    _COND_START = ('ifeq', 'ifneq', 'ifdef', 'ifndef')
    _COND_ELSE = 'else'
    _COND_END = 'endif'

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self.stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.'''
        stripped = line.strip()
        tokens = stripped.split()
        context = tuple(self.stack)

        if not tokens:
            return context

        keyword = tokens[0]

        if keyword in self._COND_START:
            # Start a new conditional block, default branch 0
            self.stack.append(0)
        elif keyword == self._COND_ELSE:
            # Switch to the else branch at current level
            if self.stack:
                self.stack[-1] = 1
        elif keyword == self._COND_END:
            # End the current conditional block
            if self.stack:
                self.stack.pop()

        return context

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.stack = []

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        '''Check if two conditional contexts are mutually exclusive.'''
        minlen = min(len(context1), len(context2))
        for i in range(minlen):
            if context1[i] != context2[i]:
                return True
        return False
