
class ConditionalTracker:

    def __init__(self) -> None:
        self.context_stack = []
        self.current_context = ()

    def process_line(self, line: str, line_index: int) -> tuple:
        if line.strip().startswith("if "):
            self.context_stack.append(self.current_context)
            self.current_context += (line_index,)
        elif line.strip().startswith("elif "):
            self.current_context = self.context_stack[-1] + (line_index,)
        elif line.strip().startswith("else:"):
            self.current_context = self.context_stack[-1] + (line_index,)
        elif line.strip().startswith("endif"):
            self.current_context = self.context_stack.pop()
        return self.current_context

    def reset(self) -> None:
        self.context_stack = []
        self.current_context = ()

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        for c1, c2 in zip(context1, context2):
            if c1 != c2:
                return True
        return len(context1) != len(context2)
