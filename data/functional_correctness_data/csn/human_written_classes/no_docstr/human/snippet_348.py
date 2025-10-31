class ZobristHash:

    def __init__(self, board):
        self.board = board
        self.hash_set = set()
        self.hash = 0
        for square in self.board.squares:
            self.hash ^= square.zobrist_strings[EMPTY]
        self.hash_set.clear()
        self.hash_set.add(self.hash)

    def update(self, square, color):
        self.hash ^= square.zobrist_strings[square.color]
        self.hash ^= square.zobrist_strings[color]

    def add(self):
        self.hash_set.add(self.hash)

    def dupe(self):
        return self.hash in self.hash_set