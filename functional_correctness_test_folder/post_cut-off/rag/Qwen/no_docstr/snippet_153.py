
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
        if line.strip().startswith('ifeq'):
            self.context_stack.append(('ifeq', line_index))
        elif line.strip().startswith('ifneq'):
            self.context_stack.append(('ifneq', line_index))
        elif line.strip().startswith('ifdef'):
            self.context_stack.append(('ifdef', line_index))
        elif line.strip().startswith('ifndef'):
            self.context_stack.append(('ifndef', line_index))
        elif line.strip() == 'else':
            if self.context_stack:
                self.context_stack[-1] = (self.context_stack[-1]
                                          [0], line_index)
        elif line.strip() == 'endif':
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
        min_length = min(len(context1), len(context2))
        for i in range(min_length):
            if context1[i] != context2[i]:
                return True
        return len(context1) != len(context2)
