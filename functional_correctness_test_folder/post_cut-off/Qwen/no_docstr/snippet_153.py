
class ConditionalTracker:

    def __init__(self) -> None:
        self.context_stack = []
        self.current_context = None

    def process_line(self, line: str, line_index: int) -> tuple:
        if "if" in line:
            self.context_stack.append(self.current_context)
            self.current_context = ("if", line_index)
        elif "elif" in line:
            self.current_context = ("elif", line_index)
        elif "else" in line:
            self.current_context = ("else", line_index)
        elif "endif" in line:
            self.current_context = self.context_stack.pop() if self.context_stack else None
        return self.current_context

    def reset(self) -> None:
        self.context_stack = []
        self.current_context = None

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        if not context1 or not context2:
            return False
        return context1[0] != context2[0]
