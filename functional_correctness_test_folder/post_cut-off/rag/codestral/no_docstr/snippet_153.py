
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self.stack = []
        self.contexts = {}

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        stripped_line = line.strip()
        if stripped_line.startswith('if'):
            self.stack.append(('if', line_index))
        elif stripped_line.startswith('else'):
            if self.stack and self.stack[-1][0] == 'if':
                self.stack[-1] = ('else', line_index)
        elif stripped_line.startswith('endif'):
            if self.stack:
                self.stack.pop()
        return tuple(self.stack)

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.stack = []
        self.contexts = {}

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
        return len(context1) != len(context2)
