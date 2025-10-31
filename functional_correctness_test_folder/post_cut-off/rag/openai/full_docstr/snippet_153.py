class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    def __init__(self) -> None:
        '''Initialize the conditional tracker.'''
        self.stack: list[tuple[str, str, bool]] = []

    def process_line(self, line: str, line_index: int) -> tuple:
        '''Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        '''
        stripped = line.lstrip()
        # Handle .if directives
        if stripped.startswith('.if '):
            condition = stripped[3:].strip()
            self.stack.append(('.if', condition, True))
        elif stripped.startswith('.ifdef '):
            condition = stripped[6:].strip()
            self.stack.append(('.ifdef', condition, True))
        elif stripped.startswith('.ifndef '):
            condition = stripped[7:].strip()
            self.stack.append(('.ifndef', condition, True))
        elif stripped.startswith('.ifeq '):
            condition = stripped[5:].strip()
            self.stack.append(('.ifeq', condition, True))
        elif stripped.startswith('.ifneq '):
            condition = stripped[6:].strip()
            self.stack.append(('.ifneq', condition, True))
        # Handle .else
        elif stripped.startswith('.else'):
            if self.stack:
                # toggle branch flag to False
                directive, condition, _ = self.stack[-1]
                self.stack[-1] = (directive
