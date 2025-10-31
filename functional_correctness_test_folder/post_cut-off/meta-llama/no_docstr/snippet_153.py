
class ConditionalTracker:

    def __init__(self) -> None:
        """
        Initializes the ConditionalTracker object.
        """
        self.context_stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        """
        Processes a line of code and returns the current context.

        Args:
        line (str): The line of code to process.
        line_index (int): The index of the line.

        Returns:
        tuple: The current context.
        """
        line = line.strip()
        if line.startswith('if') or line.startswith('elif'):
            self.context_stack.append((line_index, line))
        elif line.startswith('else'):
            if self.context_stack:
                self.context_stack[-1] = (self.context_stack[-1]
                                          [0], self.context_stack[-1][1] + ' else')
        elif line == '':
            pass
        else:
            if self.context_stack and line.startswith(('break', 'continue', 'pass')):
                pass
            elif self.context_stack and line.startswith('return'):
                self.context_stack = []
            elif line.startswith(('for', 'while')):
                self.context_stack.append((line_index, line))
            elif line == 'pass':
                pass
            elif line.startswith('def') or line.startswith('class'):
                self.context_stack = []
            else:
                if self.context_stack and ':' in line:
                    self.context_stack.append((line_index, line))
                while self.context_stack and line_index > self.context_stack[-1][0]:
                    self.context_stack.pop()
        return tuple(self.context_stack)

    def reset(self) -> None:
        """
        Resets the ConditionalTracker object.
        """
        self.context_stack = []

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        """
        Checks if two contexts are mutually exclusive.

        Args:
        context1 (tuple): The first context.
        context2 (tuple): The second context.

        Returns:
        bool: True if the contexts are mutually exclusive, False otherwise.
        """
        if not context1 or not context2:
            return False
        context1 = list(context1)
        context2 = list(context2)
        while len(context1) > 0 and len(context2) > 0 and context1[-1][1].strip().startswith('if') and context2[-1][1].strip().startswith('if'):
            if context1[-1] != context2[-1]:
                return True
            context1.pop()
            context2.pop()
        return False
