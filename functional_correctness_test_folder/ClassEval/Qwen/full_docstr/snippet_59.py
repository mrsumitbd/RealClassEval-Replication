
import random


class MinesweeperGame:
    """
    This is a class that implements mine sweeping games including minesweeping and winning judgment.
    """

    def __init__(self, n, k) -> None:
        """
        Initializes the MinesweeperGame class with the size of the board and the number of mines.
        :param n: The size of the board, int.
        :param k: The number of mines, int.
        """
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def generate_mine_sweeper_map(self):
        """
        Generates a minesweeper map with the given size of the board and the number of mines.
        """
        map = [[0 for _ in range(self.n)] for _ in range(self.n)]
        mines = random.sample(range(self.n * self.n), self.k)
        for mine in mines:
            row, col = divmod(mine, self.n)
            map[row][col] = 'X'
            for i in range(max(0, row-1), min(self.n, row+2)):
                for j in range(max(0, col-1), min(self.n, col+2)):
                    if map[i][j] != 'X':
                        map[i][j] += 1
        return map

    def generate_playerMap(self):
        """
        Generates a player map with the given size of the board.
        """
        return [['-' for _ in range(self.n)] for _ in range(self.n)]

    def check_won(self, map):
        """
        Checks whether the player has won the game.
        """
        for i in range(self.n):
            for j in range(self.n):
                if map[i][j] == '-' and self.minesweeper_map[i][j] != 'X':
                    return False
        return True

    def sweep(self, x, y):
        """
        Sweeps the given position.
        """
        if self.minesweeper_map[x][y] == 'X':
            self.player_map[x][y] = 'X'
            return False
        else:
            self.player_map[x][y] = self.minesweeper_map[x][y]
            if self.check_won(self.player_map):
                return True
            return self.player_map
