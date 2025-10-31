class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    def __init__(self):
        self._root = {}
        self._END = "_end_"

    def insert(self, word: str):
        if not word:
            return
        node = self._root
        for ch in word.upper():
            node = node.setdefault(ch, {})
        node[self._END] = True

    def is_word(self, word: str) -> bool:
        if not word:
            return False
        node = self._root
        for ch in word.upper():
            if ch not in node:
                return False
            node = node[ch]
        return node.get(self._END, False)

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        if prefix is None:
            return False
        node = self._root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
