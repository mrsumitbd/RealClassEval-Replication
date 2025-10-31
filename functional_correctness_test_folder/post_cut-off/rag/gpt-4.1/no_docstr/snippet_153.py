
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

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
        # Save current context before processing this line
        context = tuple(self.stack)
        # Recognize conditional directives
        if stripped.startswith('ifdef') or stripped.startswith('ifndef') or stripped.startswith('ifeq') or stripped.startswith('ifneq'):
            # Use the line index and the directive to uniquely identify the branch
            directive = stripped.split()[0]
            self.stack.append((directive, line_index))
        elif stripped == 'else':
            if self.stack:
                directive, idx = self.stack.pop()
                # Mark else branch by negating the directive
                self.stack.append((f'else-{directive}', idx))
        elif stripped == 'endif':
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
