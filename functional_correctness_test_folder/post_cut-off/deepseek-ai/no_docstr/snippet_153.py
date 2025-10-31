
class ConditionalTracker:

    def __init__(self) -> None:
        self.conditions = []

    def process_line(self, line: str, line_index: int) -> tuple:
        stripped = line.strip()
        if stripped.startswith("if "):
            condition = stripped[3:].split(':')[0].strip()
            context = (line_index, condition, "if")
            self.conditions.append(context)
            return context
        elif stripped.startswith("elif "):
            condition = stripped[5:].split(':')[0].strip()
            context = (line_index, condition, "elif")
            self.conditions.append(context)
            return context
        elif stripped.startswith("else:"):
            context = (line_index, None, "else")
            self.conditions.append(context)
            return context
        return None

    def reset(self) -> None:
        self.conditions = []

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        if context1[2] == "if" and context2[2] == "if":
            return True
        if (context1[2] == "if" and context2[2] == "elif") or (context1[2] == "elif" and context2[2] == "if"):
            return False
        if context1[2] == "elif" and context2[2] == "elif":
            return True
        if context1[2] == "else" or context2[2] == "else":
            return True
        return False
