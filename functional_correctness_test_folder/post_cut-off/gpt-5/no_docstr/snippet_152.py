class Trie:
    def __init__(self):
        self._root = {}
        self._END = "_end"

    def insert(self, word: str):
        node = self._root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[self._END] = True

    def is_word(self, word: str) -> bool:
        node = self._root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return node.get(self._END, False)

    def is_prefix(self, prefix: str) -> bool:
        node = self._root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
