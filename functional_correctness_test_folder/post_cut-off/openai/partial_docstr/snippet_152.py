class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word: str):
        node = self
        for ch in word.upper():
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def is_word(self, word: str) -> bool:
        node = self
        for ch in word.upper():
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        node = self
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
