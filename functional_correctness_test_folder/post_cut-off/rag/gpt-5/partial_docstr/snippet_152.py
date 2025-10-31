class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    __slots__ = ('_children', '_end')

    def __init__(self):
        '''Initializes the Trie with an empty root node.'''
        self._children: list[list[int]] = [[-1] * 26]
        self._end: list[bool] = [False]

    def _new_node(self) -> int:
        self._children.append([-1] * 26)
        self._end.append(False)
        return len(self._children) - 1

    @staticmethod
    def _idx(c: str) -> int:
        return ord(c) - 65  # 'A' -> 0 ... 'Z' -> 25

    def insert(self, word: str):
        '''
        Inserts a word into the Trie. Assumes word is already uppercase.
        '''
        if not word:
            return
        node = 0
        for ch in word:
            i = self._idx(ch)
            if i < 0 or i >= 26:
                return
            nxt = self._children[node][i]
            if nxt == -1:
                nxt = self._new_node()
                self._children[node][i] = nxt
            node = nxt
        self._end[node] = True

    def is_word(self, word: str) -> bool:
        '''
        Searches for a complete word in the Trie. Assumes word is already uppercase.
        '''
        if not word:
            return False
        node = 0
        for ch in word:
            i = self._idx(ch)
            if i < 0 or i >= 26:
                return False
            node = self._children[node][i]
            if node == -1:
                return False
        return self._end[node]

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        if prefix == "":
            return True
        node = 0
        for ch in prefix:
            i = self._idx(ch)
            if i < 0 or i >= 26:
                return False
            node = self._children[node][i]
            if node == -1:
                return False
        return True
