class Trie:
    '''
    Trie data structure for efficient word and prefix lookups, optimized for the Word Hunt game.
    '''

    class Node:
        def __init__(self):
            self.children = {}
            self.is_end = False

    def __init__(self):
        '''Initializes the Trie with an empty root node.'''
        self.root = self.Node()

    def insert(self, word: str):
        '''
        Inserts a word into the Trie. Assumes word is already uppercase.
        '''
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = self.Node()
            node = node.children[c]
        node.is_end = True

    def is_word(self, word: str) -> bool:
        '''
        Searches for a complete word in the Trie. Assumes word is already uppercase.
        '''
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end

    def is_prefix(self, prefix: str) -> bool:
        '''
        Checks if a string is a prefix of any word in the Trie. Assumes prefix is already uppercase.
        '''
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
