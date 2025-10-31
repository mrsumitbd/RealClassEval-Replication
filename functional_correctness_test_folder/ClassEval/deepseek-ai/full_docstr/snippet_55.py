
import random
from collections import deque


class MahjongConnect:
    def __init__(self, BOARD_SIZE, ICONS):
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        rows, cols = self.BOARD_SIZE
        board = []
        icon_count = len(self.ICONS)
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(random.choice(self.ICONS))
            board.append(row)
        return board

    def is_valid_move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        rows, cols = self.BOARD_SIZE

        if not (0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols):
            return False

        if pos1 == pos2:
            return False

        if self.board[x1][y1] != self.board[x2][y2] or self.board[x1][y1] == ' ' or self.board[x2][y2] == ' ':
            return False

        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if self.board[x1][y1] != self.board[x2][y2]:
            return False

        rows, cols = self.BOARD_SIZE
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        queue = deque()
        queue.append((x1, y1))
        visited[x1][y1] = True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            if (x, y) == (x2, y2):
                return True
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if not visited[nx][ny] and (self.board[nx][ny] == ' ' or (nx, ny) == (x2, y2)):
                        visited[nx][ny] = True
                        queue.append((nx, ny))
        return False

    def remove_icons(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        if self.is_valid_move(pos1, pos2):
            self.board[x1][y1] = ' '
            self.board[x2][y2] = ' '

    def is_game_over(self):
        for row in self.board:
            for cell in row:
                if cell != ' ':
                    return False
        return True
