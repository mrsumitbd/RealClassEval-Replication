class ConditionalTracker:

    def __init__(self) -> None:
        self._stack = []  # list of (chain_id, branch_id)
        self._next_chain_id = 1

    def process_line(self, line: str, line_index: int) -> tuple:
        s = line.strip()
        if not s:
            return tuple(self._stack)

        # Normalize directive token at start
        token = s.lstrip('#').split(None, 1)[0].rstrip(':').lower()

        if token == 'if':
            self._stack.append((self._next_chain_id, 0))
            self._next_chain_id += 1
        elif token == 'elif':
            if self._stack:
                cid, bid = self._stack[-1]
                self._stack[-1] = (cid, bid + 1)
        elif token == 'else':
            if self._stack:
                cid, bid = self._stack[-1]
                self._stack[-1] = (cid, bid + 1)
        elif token in ('endif', 'fi', 'end'):
            if self._stack:
                self._stack.pop()

        return tuple(self._stack)

    def reset(self) -> None:
        self._stack.clear()
        self._next_chain_id = 1

    @staticmethod
    def are_mutually_exclusive(context1: tuple, context2: tuple) -> bool:
        # contexts are tuples of (chain_id, branch_id)
        map1 = {cid: bid for cid, bid in context1}
        map2 = {cid: bid for cid, bid in context2}
        for cid in set(map1.keys()) & set(map2.keys()):
            if map1[cid] != map2[cid]:
                return True
        return False
