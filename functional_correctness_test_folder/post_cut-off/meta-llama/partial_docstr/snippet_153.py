
class ConditionalTracker:

    def __init__(self) -> None:
        self.context_stack = []
        self.conditional_context = ()

    def process_line(self, line: str, line_index: int) -> tuple:
        stripped_line = line.strip()
        if stripped_line.startswith('if') or stripped_line.startswith('elif'):
            self.context_stack.append((stripped_line, line_index))
            self.conditional_context = tuple(self.context_stack)
        elif stripped_line.startswith('else'):
            if self.context_stack:
                last_if, last_if_index = self.context_stack[-1]
                self.context_stack[-1] = (f'not ({last_if})', last_if_index)
                self.conditional_context = tuple(self.context_stack)
        elif stripped_line == '':
            pass
        else:
            if stripped_line.startswith('return') or stripped_line.startswith('break') or stripped_line.startswith('continue'):
                self.context_stack = []
            while self.context_stack and stripped_line.startswith('dedent'):
                self.context_stack.pop()
                self.conditional_context = tuple(self.context_stack)
        return self.conditional_context

    def reset(self) -> None:
        self.context_stack = []
        self.conditional_context = ()

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        min_len = min(len(context1), len(context2))
        for i in range(min_len):
            cond1 = context1[i][0]
            cond2 = context2[i][0]
            if cond1 != cond2 and (cond1.startswith('not') or cond2.startswith('not')):
                not_cond = cond1 if cond1.startswith('not') else cond2
                cond = cond2 if cond1.startswith('not') else cond1
                not_cond = not_cond.replace('not (', '').replace(')', '')
                if not_cond == cond:
                    return True
            elif cond1 != cond2:
                return True
        return False
