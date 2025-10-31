
class ConditionalTracker:
    '''Utility for tracking conditional contexts in Makefiles.'''

    CONDITIONALS = {
        "ifdef", "ifndef", "ifeq", "ifneq",
        "else", "endif"
    }

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
        context = tuple(self.stack)
        if not tokens:
            return context

        keyword = tokens[0]
        if keyword not in self.CONDITIONALS:
            return context

        if keyword in {"ifdef", "ifndef", "ifeq", "ifneq"}:
            # Use a tuple to represent the conditional block
            # (type, argument, line_index)
            if len(tokens) > 1:
                arg = " ".join(tokens[1:])
            else:
                arg = ""
            self.stack.append((keyword, arg, line_index))
        elif keyword == "else":
            if self.stack:
                prev = self.stack.pop()
                # Mark as else branch by toggling a bool
                # (type, argument, line_index, is_else)
                if len(prev) == 3:
                    self.stack.append((prev[0], prev[1], prev[2], True))
                else:
                    # Already in else, just keep as is
                    self.stack.append(prev)
        elif keyword == "endif":
            if self.stack:
                self.stack.pop()
        return tuple(self.stack)

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
        min_len = min(len(context1), len(context2))
        for i in range(min_len):
            c1 = context1[i]
            c2 = context2[i]
            # Compare all fields except the "else" marker
            if c1[:3] != c2[:3]:
                return True
            # If one is in else and the other is not, they're mutually exclusive
            is_else1 = c1[3] if len(c1) > 3 else False
            is_else2 = c2[3] if len(c2) > 3 else False
            if is_else1 != is_else2:
                return True
        # If one context is deeper than the other, they're not mutually exclusive
        return False
