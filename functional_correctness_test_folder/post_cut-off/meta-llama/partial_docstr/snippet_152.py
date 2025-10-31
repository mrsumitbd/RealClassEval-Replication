
class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    def __init__(self):
        self.root = {}

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True  # '$' denotes the end of a word

    def is_word(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return '$' in node

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
