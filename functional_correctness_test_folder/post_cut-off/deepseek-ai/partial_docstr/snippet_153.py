
class ConditionalTracker:

    def __init__(self) -> None:
        self.conditional_stack = []
        self.context_history = {}

    def process_line(self, line: str, line_index: int) -> tuple:
        stripped_line = line.strip()
        if stripped_line.startswith('if '):
            self.conditional_stack.append((len(self.conditional_stack), True))
        elif stripped_line.startswith('elif '):
            if self.conditional_stack:
                self.conditional_stack[-1] = (
                    self.conditional_stack[-1][0], True)
        elif stripped_line == 'else:':
            if self.conditional_stack:
                self.conditional_stack[-1] = (
                    self.conditional_stack[-1][0], False)
        elif stripped_line.startswith('for ') or stripped_line.startswith('while '):
            self.conditional_stack.append((len(self.conditional_stack), True))
        elif stripped_line.startswith('def ') or stripped_line.startswith('class '):
            self.conditional_stack = []

        current_context = tuple((level, is_if_or_elif)
                                for level, is_if_or_elif in self.conditional_stack)
        self.context_history[line_index] = current_context

        if stripped_line.endswith(':'):
            pass
        else:
            if stripped_line and not any(stripped_line.startswith(s) for s in ['if ', 'elif ', 'else:', 'for ', 'while ', 'def ', 'class ']):
                pass

        return current_context

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.conditional_stack = []
        self.context_history = {}

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
            level1, is_if_or_elif1 = context1[i]
            level2, is_if_or_elif2 = context2[i]
            if level1 != level2:
                continue
            if is_if_or_elif1 != is_if_or_elif2:
                return True
        return False
