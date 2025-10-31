
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def is_word(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def is_prefix(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Example usage:


def main():
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("banana")

    print(trie.is_word("apple"))   # True
    print(trie.is_word("app"))     # True
    print(trie.is_word("ap"))      # False
    print(trie.is_prefix("app"))   # True
    print(trie.is_prefix("ap"))    # True
    print(trie.is_prefix("ban"))   # True
    print(trie.is_prefix("ora"))   # False


if __name__ == "__main__":
    main()
