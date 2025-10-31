from typing import Any, Callable, Optional, Union

class ConditionalTracker:
    """Utility for tracking conditional contexts in Makefiles."""

    def __init__(self) -> None:
        """Initialize the conditional tracker."""
        self.conditional_stack: list[dict[str, Any]] = []
        self.conditional_branch_id: int = 0

    def process_line(self, line: str, line_index: int) -> tuple:
        """Process a line and return the conditional context the line is IN.

        Args:
            line: The line to process
            line_index: Index of the line (for debugging)

        Returns:
            Tuple representing the conditional context the line is IN
        """
        stripped = line.strip()
        current_context = tuple((block['branch_id'] for block in self.conditional_stack))
        if stripped.startswith(('ifeq', 'ifneq', 'ifdef', 'ifndef')):
            self.conditional_stack.append({'type': 'if', 'line': line_index, 'branch_id': self.conditional_branch_id})
            self.conditional_branch_id += 1
        elif stripped.startswith('else'):
            if self.conditional_stack and self.conditional_stack[-1]['type'] == 'if':
                self.conditional_stack[-1]['type'] = 'else'
                self.conditional_stack[-1]['branch_id'] = self.conditional_branch_id
                self.conditional_branch_id += 1
        elif stripped.startswith('endif'):
            if self.conditional_stack:
                self.conditional_stack.pop()
        return current_context

    def reset(self) -> None:
        """Reset the tracker state."""
        self.conditional_stack = []
        self.conditional_branch_id = 0

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
        if context1 == context2:
            return False
        if not context1 or not context2:
            return False
        min_len = min(len(context1), len(context2))
        return any((context1[i] != context2[i] for i in range(min_len)))