
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self.context_stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        stripped_line = line.strip()
        if stripped_line.startswith('ifeq') or stripped_line.startswith('ifneq') or stripped_line.startswith('ifdef') or stripped_line.startswith('ifndef'):
            self.context_stack.append(stripped_line)
        elif stripped_line.startswith('else'):
            if self.context_stack:
                self.context_stack[-1] = 'else'
        elif stripped_line.startswith('endif'):
            if self.context_stack:
                self.context_stack.pop()
        return tuple(self.context_stack)

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.context_stack = []

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
        for c1, c2 in zip(context1, context2):
            if c1 != c2:
                return True
        return len(context1) != len(context2)
