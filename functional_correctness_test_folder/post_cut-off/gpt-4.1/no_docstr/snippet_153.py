
class ConditionalTracker:

    def __init__(self) -> None:
        self.stack = []

    def process_line(self, line: str, line_index: int) -> tuple:
        stripped = line.strip()
        if stripped.startswith("if "):
            cond = stripped[3:].strip().rstrip(":")
            self.stack.append(('if', cond, line_index))
            return ('if', cond, line_index)
        elif stripped.startswith("elif "):
            cond = stripped[5:].strip().rstrip(":")
            # pop previous 'if' or 'elif'
            if self.stack and self.stack[-1][0] in ('if', 'elif'):
                self.stack.pop()
            self.stack.append(('elif', cond, line_index))
            return ('elif', cond, line_index)
        elif stripped.startswith("else"):
            # pop previous 'if' or 'elif'
            if self.stack and self.stack[-1][0] in ('if', 'elif'):
                self.stack.pop()
            self.stack.append(('else', None, line_index))
            return ('else', None, line_index)
        elif stripped == "" or stripped.startswith("#"):
            return None
        else:
            return None

    def reset(self) -> None:
        self.stack = []

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        if context1 is None or context2 is None:
            return False
        type1, cond1, _ = context1
        type2, cond2, _ = context2
        if type1 == 'else' or type2 == 'else':
            return True
        if type1 in ('if', 'elif') and type2 in ('if', 'elif'):
            return cond1 != cond2
        return False
