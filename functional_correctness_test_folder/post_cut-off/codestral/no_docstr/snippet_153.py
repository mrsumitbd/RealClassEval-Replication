
class ConditionalTracker:

    def __init__(self) -> None:
        self.contexts = []

    def process_line(self, line: str, line_index: int) -> tuple:
        if line.startswith('if'):
            context = ('if', line_index)
            self.contexts.append(context)
            return context
        elif line.startswith('elif'):
            context = ('elif', line_index)
            self.contexts.append(context)
            return context
        elif line.startswith('else'):
            context = ('else', line_index)
            self.contexts.append(context)
            return context
        else:
            return None

    def reset(self) -> None:
        self.contexts = []

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        if context1[0] == 'if' and context2[0] == 'elif':
            return True
        elif context1[0] == 'if' and context2[0] == 'else':
            return True
        elif context1[0] == 'elif' and context2[0] == 'else':
            return True
        else:
            return False
