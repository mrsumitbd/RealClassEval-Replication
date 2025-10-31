
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self.context = []
        self.conditional_stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        line = line.strip()
        if line.startswith('ifeq') or line.startswith('ifneq'):
            self.conditional_stack.append(
                line.split(' ', 1)[1].strip().strip('()'))
            self.context.append(False)
        elif line == 'else':
            if not self.conditional_stack:
                raise ValueError(f"Unmatched 'else' at line {line_index}")
            self.context[-1] = not self.context[-1]
        elif line.startswith('endif'):
            if not self.conditional_stack:
                raise ValueError(f"Unmatched 'endif' at line {line_index}")
            self.conditional_stack.pop()
            self.context.pop()
        return tuple(self.context)

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.context = []
        self.conditional_stack = []

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
