
class ConditionalTracker:
    """Utility for tracking conditional contexts in Makefiles."""

    def __init__(self) -> None:
        """Initialize the conditional tracker."""
        self._context_stack = []
        self._current_context = ()

    def process_line(self, line: str, line_index: int) -> tuple:
        """Process a line and return the conditional context the line is IN.
        Args:
            line: The line to process
            line_index: Index of the line (for debugging)
        Returns:
            Tuple representing the conditional context the line is IN
        """
        line = line.strip()
        if line.startswith('ifeq') or line.startswith('ifneq'):
            self._context_stack.append(len(self._current_context))
            self._current_context += (line_index,)
        elif line.startswith('else'):
            if not self._context_stack:
                raise ValueError(f"Unexpected 'else' at line {line_index}")
            depth = self._context_stack[-1]
            self._current_context = self._current_context[:depth] + (
                line_index,)
        elif line.startswith('endif'):
            if not self._context_stack:
                raise ValueError(f"Unexpected 'endif' at line {line_index}")
            depth = self._context_stack.pop()
            self._current_context = self._current_context[:depth]
        return self._current_context

    def reset(self) -> None:
        """Reset the tracker state."""
        self._context_stack = []
        self._current_context = ()

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """Check if two conditional contexts are mutually exclusive.
        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.
        Args:
            context1: First conditional context
            context2: Second conditional context
        Returns:
            True if contexts are mutually exclusive
        """
        min_length = min(len(context1), len(context2))
        for i in range(min_length):
            if context1[i] != context2[i]:
                return True
        return False
