class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    def __init__(self):
        '''Initializes the Trie with an empty root node.'''
        self._root = {}
        self._END = "_end"

    def insert(self, word: str):
        '''
        Inserts a word into the Trie. Assumes word is already uppercase.
        '''
        node = self._root
        for ch in word:
            node = node.setdefault(ch, {})
        node[self._END] = True

    def is_word(self, word: str) -> bool:
        '''
        Searches for a complete word in the Trie. Assumes word is already uppercase.
        '''
        node = self._root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return node.get(self._END, False)

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        node = self._root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
