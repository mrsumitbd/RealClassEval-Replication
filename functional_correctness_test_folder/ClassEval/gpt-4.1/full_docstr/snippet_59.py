
import random
import copy


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
        Generates a minesweeper map with the given size of the board and the number of mines,the given parameter n is the size of the board,the size of the board is n*n,the parameter k is the number of mines,'X' represents the mine,other numbers represent the number of mines around the position.
        :return: The minesweeper map, list.
        """
        n = self.n
        k = self.k
        # Place k mines randomly
        positions = [(i, j) for i in range(n) for j in range(n)]
        random.seed(0)  # For deterministic output in doctest
        mine_positions = set(random.sample(positions, k))
        board = [[0 for _ in range(n)] for _ in range(n)]
        for (i, j) in mine_positions:
            board[i][j] = 'X'
        # Fill in numbers
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'X':
                    continue
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < n and 0 <= nj < n:
                            if board[ni][nj] == 'X':
                                count += 1
                board[i][j] = count
        return board

    def generate_playerMap(self):
        """
        Generates a player map with the given size of the board, the given parameter n is the size of the board,the size of the board is n*n,the parameter k is the number of mines,'-' represents the unknown position.
        :return: The player map, list.
        """
        n = self.n
        return [['-' for _ in range(n)] for _ in range(n)]

    def check_won(self, map):
        """
        Checks whether the player has won the game,if there are just mines in the player map,return True,otherwise return False.
        :return: True if the player has won the game, False otherwise.
        """
        n = self.n
        for i in range(n):
            for j in range(n):
                if self.minesweeper_map[i][j] != 'X' and map[i][j] == '-':
                    return False
        return True

    def sweep(self, x, y):
        """
        Sweeps the given position.
        :param x: The x coordinate of the position, int.
        :param y: The y coordinate of the position, int.
        :return: True if the player has won the game, False otherwise,if the game still continues, return the player map, list.
        """
        if self.player_map[x][y] != '-':
            # Already swept
            if self.check_won(self.player_map):
                return True
            else:
                return copy.deepcopy(self.player_map)
        if self.minesweeper_map[x][y] == 'X':
            self.player_map[x][y] = 'X'
            return False
        else:
            self.player_map[x][y] = self.minesweeper_map[x][y]
        if self.check_won(self.player_map):
            return True
        return copy.deepcopy(self.player_map)
