class MahjongConnect:
    """
    MahjongConnect is a class representing a game board for Mahjong Connect with features like creating the board, checking valid moves, finding paths, removing icons, and checking if the game is over.
    """

    def __init__(self, BOARD_SIZE, ICONS):
        """
        initialize the board size and the icon list, create the game board
        :param BOARD_SIZE: list of two integer numbers, representing the number of rows and columns of the game board
        :param ICONS: list of string, representing the icons
        >>>mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.BOARD_SIZE = [4, 4]
        mc.ICONS = ['a', 'b', 'c']
        mc.board = mc.create_board()
        """
        self.BOARD_SIZE = BOARD_SIZE
        self.ICONS = ICONS
        self.board = self.create_board()

    def create_board(self):
        """
        create the game board with the given board size and icons
        :return: 2-dimensional list, the game board
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        >>> mc.create_board()
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        """
        rows, cols = self.BOARD_SIZE
        if not self.ICONS:
            return [[' ' for _ in range(cols)] for _ in range(rows)]
        board = []
        for _ in range(rows):
            row = [self.ICONS[j % len(self.ICONS)] for j in range(cols)]
            board.append(row)
        return board

    def _in_bounds(self, pos):
        x, y = pos
        rows, cols = self.BOARD_SIZE
        return 0 <= x < rows and 0 <= y < cols

    def is_valid_move(self, pos1, pos2):
        """
        check if the move of two icons is valid (i.e. positions are within the game board range, the two positions are not the same, the two positions have the same icon, and there is a valid path between the two positions)
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return:True or False ,representing whether the move of two icons is valid
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        >>> mc.is_valid_move((0, 0), (1, 0))
        True
        """
        if pos1 == pos2:
            return False
        if not (self._in_bounds(pos1) and self._in_bounds(pos2)):
            return False
        x1, y1 = pos1
        x2, y2 = pos2
        icon1 = self.board[x1][y1]
        icon2 = self.board[x2][y2]
        if icon1 == ' ' or icon2 == ' ':
            return False
        if icon1 != icon2:
            return False
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        """
        check if there is a path between two icons
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return: True or False ,representing whether there is a path between two icons
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        >>> mc.is_valid_move((0, 0), (1, 0))
        True
        """
        if not (self._in_bounds(pos1) and self._in_bounds(pos2)):
            return False

        # Allow movement through empty cells (' ') with up to 2 turns (3 segments).
        from collections import deque

        rows, cols = self.BOARD_SIZE
        target = pos2

        # Directions: up, down, left, right
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # visited[(x,y)][dir_index] = minimal turns used to reach (x,y) coming from dir_index
        # dir_index: 0..3 for dirs, 4 for None (start)
        visited = [[[float('inf')] * 5 for _ in range(cols)]
                   for __ in range(rows)]

        sx, sy = pos1
        tx, ty = pos2

        dq = deque()
        # Start with no direction and 0 turns
        dq.append((sx, sy, 4, 0))  # 4 represents None direction
        visited[sx][sy][4] = 0

        def can_step(nx, ny):
            if not (0 <= nx < rows and 0 <= ny < cols):
                return False
            if (nx, ny) == target:
                return True
            return self.board[nx][ny] == ' '

        while dq:
            x, y, d_idx, turns = dq.popleft()
            if (x, y) == target:
                return True
            for nd_idx, (dx, dy) in enumerate(dirs):
                nx, ny = x + dx, y + dy
                if not can_step(nx, ny):
                    continue
                nturns = turns + (0 if d_idx in (nd_idx, 4) else 1)
                if nturns > 2:
                    continue
                if visited[nx][ny][nd_idx] <= nturns:
                    continue
                visited[nx][ny][nd_idx] = nturns
                dq.append((nx, ny, nd_idx, nturns))

        return False

    def remove_icons(self, pos1, pos2):
        """
        remove the connected icons on the game board
        :param pos1: position tuple(x, y) of the first icon to be removed
        :param pos2: position tuple(x, y) of the second icon to be removed
        :return: None
        >>> mc = MahjongConnect([4, 4], ['a', 'b', 'c'])
        mc.board = [['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        >>> mc.remove_icons((0, 0), (1, 0))
        mc.board = [[' ', 'b', 'c', 'a'],
                    [' ', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a'],
                    ['a', 'b', 'c', 'a']]
        """
        if self.is_valid_move(pos1, pos2):
            x1, y1 = pos1
            x2, y2 = pos2
            self.board[x1][y1] = ' '
            self.board[x2][y2] = ' '

    def is_game_over(self):
        """
        Check if the game is over (i.e., if there are no more icons on the game board)
        :return: True or False ,representing whether the game is over
        >>> mc = MahjongConnect([4, 4] ['a', 'b', 'c'])
        >>> mc.board = [[' ', ' ', ' ', ' '],
        >>>         [' ', ' ', ' ', ' '],
        >>>         [' ', ' ', ' ', ' '],
        >>>         [' ', ' ', ' ', ' ']]
        >>> mc.is_game_over()
        True
        """
        for row in self.board:
            for cell in row:
                if cell != ' ':
                    return False
        return True
