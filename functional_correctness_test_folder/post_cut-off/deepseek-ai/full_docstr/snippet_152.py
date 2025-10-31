
class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    def __init__(self):
        '''Initializes the Trie with an empty root node.'''
        self.root = {}
        self.end_symbol = '*'

    def insert(self, word: str):
        '''
        Inserts a word into the Trie. Assumes word is already uppercase.
        '''
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node[self.end_symbol] = True

    def is_word(self, word: str) -> bool:
        '''
        Searches for a complete word in the Trie. Assumes word is already uppercase.
        '''
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return self.end_symbol in node

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        node = self.root
        for char in prefix:
            if char not in node:
                return False
            node = node[char]
        return True
