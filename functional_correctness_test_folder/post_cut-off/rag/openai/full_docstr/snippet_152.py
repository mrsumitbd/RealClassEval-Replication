class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    class _Node:
        __slots__ = ('children', 'end')

        def __init__(self):
            self.children = {}
            self.end = False

    def __init__(self):
        '''Initializes the Trie with an empty root node.'''
        self.root = self._Node()

    def insert(self, word: str):
        '''
        Inserts a word into the Trie. Assumes word is already uppercase.
        '''
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, self._Node())
        node.end = True

    def is_word(self, word: str) -> bool:
        '''
        Searches for a complete word in the Trie. Assumes word is already uppercase.
        '''
        node = self.root
        for ch in word:
            node = node.children.get(ch)
            if node is None:
                return False
        return node.end

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return False
        return True
