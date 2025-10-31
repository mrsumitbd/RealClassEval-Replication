
class ConditionalTracker:

    def __init__(self) -> None:
        self.context_stack = []
        self.current_context = []

    def process_line(self, line: str, line_index: int) -> tuple:
        stripped = line.strip()
        # Detect entering a conditional block
        if stripped.startswith('if '):
            self.current_context.append(('if', line_index))
        elif stripped.startswith('elif '):
            if self.current_context and self.current_context[-1][0] in ('if', 'elif'):
                self.current_context[-1] = ('elif', line_index)
            else:
                self.current_context.append(('elif', line_index))
        elif stripped.startswith('else'):
            if self.current_context and self.current_context[-1][0] in ('if', 'elif'):
                self.current_context[-1] = ('else', line_index)
            else:
                self.current_context.append(('else', line_index))
        # Detect leaving a block (assume dedent by empty line or pass)
        elif stripped == '' or stripped == 'pass':
            # This is a simplification; in real code, indentation would be tracked
            if self.current_context:
                self.current_context.pop()
        # Return a tuple representing the current context
        return tuple(self.current_context)

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self.context_stack = []
        self.current_context = []

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        '''Check if two conditional contexts are mutually exclusive.
        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.
        '''
        min_len = min(len(context1), len(context2))
        for i in range(min_len):
            if context1[i] != context2[i]:
                return True
        return False
