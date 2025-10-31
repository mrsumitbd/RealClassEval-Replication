class ConditionalTracker:

    def __init__(self) -> None:
        self._stack: list[int] = []

    def process_line(self, line: str, line_index: int) -> tuple:
        token = self._extract_token(line)
        if token == 'if':
            self._stack.append(0)
        elif token == 'elif':
            if self._stack:
                if self._stack[-1] != -1:
                    self._stack[-1] += 1
        elif token == 'else':
            if self._stack:
                self._stack[-1] = -1
        elif token == 'endif':
            if self._stack:
                self._stack.pop()
        return tuple(self._stack)

    def reset(self) -> None:
        '''Reset the tracker state.'''
        self._stack.clear()

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        '''Check if two conditional contexts are mutually exclusive.
        Two contexts are mutually exclusive if they differ at any conditional level,
        which means they're in different branches of some conditional block.
        Args:
            context1: First conditional context
            context2: Second conditional context
        Returns:
            True if contexts are mutually exclusive
        '''
        for a, b in zip(context1, context2):
            if a != b:
                return True
        return False

    @staticmethod
    def _extract_token(line: str) -> str | None:
        s = line.strip()
        # Strip common wrappers/prefixes
        changed = True
        while changed and s:
            changed = False
            if s.startswith('#'):
                s = s[1:].lstrip()
                changed = True
            elif s.startswith('//'):
                s = s[2:].lstrip()
                changed = True
            elif s.startswith('{%'):
                s = s[2:].lstrip()
                changed = True
        # Also trim closing %} if present
        if s.endswith('%}'):
            s = s[:-2].rstrip()
        # Remove trailing ':' or '{' or '}'
        if s.endswith(':') or s.endswith('{') or s.endswith('}'):
            s = s[:-1].rstrip()

        # Get first word
        word = ''
        for ch in s:
            if ch.isalpha():
                word += ch
            else:
                break
        word = word.lower()
        if word in {'if', 'elif', 'else', 'endif'}:
            return word
        return None
