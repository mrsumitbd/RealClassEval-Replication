
class MahjongConnect:
    """
    MahjongConnect is a class representing a game board for Mahjong Connect with features like creating the board, checking valid moves, finding paths, removing icons, and checking if the game is over.
    """

    def __init__(self, BOARD_SIZE, ICONS):
        """
        initialize the board size and the icon list, create the game board
        :param BOARD_SIZE: list of two integer numbers, representing the number of rows and columns of the game board
        :param ICONS: list of string, representing the icons
        """
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        """
        create the game board with the given board size and icons
        :return: 2-dimensional list, the game board
        """
        rows, cols = self.BOARD_SIZE
        icons = self.ICONS
        board = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(icons[j % len(icons)])
            board.append(row)
        return board

    def is_valid_move(self, pos1, pos2):
        """
        check if the move of two icons is valid (i.e. positions are within the game board range, the two positions are not the same, the two positions have the same icon, and there is a valid path between the two positions)
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return:True or False ,representing whether the move of two icons is valid
        """
        if pos1 == pos2:
            return False
        if not self._in_board(pos1) or not self._in_board(pos2):
            return False
        x1, y1 = pos1
        x2, y2 = pos2
        if self.board[x1][y1] == ' ' or self.board[x2][y2] == ' ':
            return False
        if self.board[x1][y1] != self.board[x2][y2]:
            return False
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        """
        check if there is a path between two icons
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return: True or False ,representing whether there is a path between two icons
        """
        from collections import deque

        rows, cols = self.BOARD_SIZE
        x1, y1 = pos1
        x2, y2 = pos2

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # visited[x][y][turns][dir] = True
        visited = [
            [[[False]*4 for _ in range(4)] for _ in range(cols)] for _ in range(rows)]

        # Try all 4 directions from the start
        queue = deque()
        for d, (dx, dy) in enumerate(directions):
            nx, ny = x1 + dx, y1 + dy
            if self._is_empty_or_target(nx, ny, pos2):
                queue.append((nx, ny, d, 0))  # (x, y, direction, turns)

        while queue:
            cx, cy, dirc, turns = queue.popleft()
            if not self._in_board((cx, cy)):
                continue
            if turns > 2:
                continue
            if (cx, cy) == pos2:
                return True
            if visited[cx][cy][turns][dirc]:
                continue
            visited[cx][cy][turns][dirc] = True
            for nd, (dx, dy) in enumerate(directions):
                nx, ny = cx + dx, cy + dy
                nturns = turns + (0 if nd == dirc else 1)
                if nturns > 2:
                    continue
                if not self._in_board((nx, ny)) and (nx, ny) != pos2:
                    continue
                if self._is_empty_or_target(nx, ny, pos2):
                    queue.append((nx, ny, nd, nturns))
        return False

    def remove_icons(self, pos1, pos2):
        """
        remove the connected icons on the game board
        :param pos1: position tuple(x, y) of the first icon to be removed
        :param pos2: position tuple(x, y) of the second icon to be removed
        :return: None
        """
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1] = ' '
        self.board[x2][y2] = ' '

    def is_game_over(self):
        """
        Check if the game is over (i.e., if there are no more icons on the game board)
        :return: True or False ,representing whether the game is over
        """
        for row in self.board:
            for cell in row:
                if cell != ' ':
                    return False
        return True

    def _in_board(self, pos):
        x, y = pos
        return 0 <= x < self.BOARD_SIZE[0] and 0 <= y < self.BOARD_SIZE[1]

    def _is_empty_or_target(self, x, y, target):
        if (x, y) == target:
            return True
        if not self._in_board((x, y)):
            return False
        return self.board[x][y] == ' '
