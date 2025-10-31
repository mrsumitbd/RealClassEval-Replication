class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word: str):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['_end_'] = True

    def is_word(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return node.get('_end_', False)

    def is_prefix(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
