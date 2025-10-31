class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    class _Node:
        __slots__ = ('children', 'end')

        def __init__(self):
            self.children = [None] * 26  # A-Z
            self.end = False

    def __init__(self):
        '''Initializes the Trie with an empty root node.'''
        self._root = Trie._Node()

    def insert(self, word: str):
        '''
        Inserts a word into the Trie. Assumes word is already uppercase.
        '''
        if not word:
            return
        node = self._root
        for ch in word:
            idx = ord(ch) - 65  # 'A' -> 0
            if idx < 0 or idx >= 26:
                continue
            nxt = node.children[idx]
            if nxt is None:
                nxt = Trie._Node()
                node.children[idx] = nxt
            node = nxt
        node.end = True

    def is_word(self, word: str) -> bool:
        '''
        Searches for a complete word in the Trie. Assumes word is already uppercase.
        '''
        if not word:
            return False
        node = self._root
        for ch in word:
            idx = ord(ch) - 65
            if idx < 0 or idx >= 26:
                return False
            node = node.children[idx]
            if node is None:
                return False
        return node.end

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        if prefix == '':
            r = self._root
            if r.end:
                return True
            for c in r.children:
                if c is not None:
                    return True
            return False
        node = self._root
        for ch in prefix:
            idx = ord(ch) - 65
            if idx < 0 or idx >= 26:
                return False
            node = node.children[idx]
            if node is None:
                return False
        return True
