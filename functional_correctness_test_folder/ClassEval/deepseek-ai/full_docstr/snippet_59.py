
import random


class MinesweeperGame:
    def __init__(self, n, k) -> None:
        self.n = n
        self.k = k
        self.minesweeper_map = self.generate_mine_sweeper_map()
        self.player_map = self.generate_playerMap()
        self.score = 0

    def generate_mine_sweeper_map(self):
        mines = random.sample(range(self.n * self.n), self.k)
        mine_map = [[0 for _ in range(self.n)] for _ in range(self.n)]

        for mine in mines:
            x = mine // self.n
            y = mine % self.n
            mine_map[x][y] = 'X'

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]

        for i in range(self.n):
            for j in range(self.n):
                if mine_map[i][j] == 'X':
                    continue
                count = 0
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < self.n and 0 <= nj < self.n and mine_map[ni][nj] == 'X':
                        count += 1
                mine_map[i][j] = count
        return mine_map

    def generate_playerMap(self):
        return [['-' for _ in range(self.n)] for _ in range(self.n)]

    def check_won(self, map):
        for i in range(self.n):
            for j in range(self.n):
                if map[i][j] == '-' and self.minesweeper_map[i][j] != 'X':
                    return False
        return True

    def sweep(self, x, y):
        if self.minesweeper_map[x][y] == 'X':
            self.player_map[x][y] = 'X'
            return False

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if self.player_map[cx][cy] != '-':
                continue
            self.player_map[cx][cy] = self.minesweeper_map[cx][cy]
            if self.minesweeper_map[cx][cy] == 0:
                directions = [(-1, -1), (-1, 0), (-1, 1),
                              (0, -1),          (0, 1),
                              (1, -1),  (1, 0), (1, 1)]
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.n and 0 <= ny < self.n and self.player_map[nx][ny] == '-':
                        stack.append((nx, ny))

        if self.check_won(self.player_map):
            return True
        return self.player_map
