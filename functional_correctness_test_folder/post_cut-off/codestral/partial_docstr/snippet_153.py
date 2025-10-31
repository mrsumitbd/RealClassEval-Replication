
class ConditionalTracker:

    def __init__(self) -> None:
        self.context_stack = []
        self.current_context = ()

    def process_line(self, line: str, line_index: int) -> tuple:
        if 'if ' in line or 'elif ' in line:
            self.context_stack.append(self.current_context)
            self.current_context += (line_index,)
        elif 'else:' in line:
            self.context_stack.append(self.current_context)
            self.current_context += (line_index,)
        elif 'endif' in line:
            self.current_context = self.context_stack.pop()
        return self.current_context

    def reset(self) -> None:
        self.context_stack = []
        self.current_context = ()

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        for i in range(min(len(context1), len(context2))):
            if context1[i] != context2[i]:
                return True
        return len(context1) != len(context2)
