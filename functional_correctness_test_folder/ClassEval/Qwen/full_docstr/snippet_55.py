
import random


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
        total_icons = rows * cols
        icons = (self.ICONS * (total_icons //
                 len(self.ICONS) + 1))[:total_icons]
        random.shuffle(icons)
        return [icons[i * cols:(i + 1) * cols] for i in range(rows)]

    def is_valid_move(self, pos1, pos2):
        """
        check if the move of two icons is valid (i.e. positions are within the game board range, the two positions are not the same, the two positions have the same icon, and there is a valid path between the two positions)
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return:True or False ,representing whether the move of two icons is valid
        """
        x1, y1 = pos1
        x2, y2 = pos2
        rows, cols = self.BOARD_SIZE

        if not (0 <= x1 < rows and 0 <= y1 < cols and 0 <= x2 < rows and 0 <= y2 < cols):
            return False
        if pos1 == pos2:
            return False
        if self.board[x1][y1] != self.board[x2][y2]:
            return False
        if self.board[x1][y1] == ' ':
            return False
        return self.has_path(pos1, pos2)

    def has_path(self, pos1, pos2):
        """
        check if there is a path between two icons
        :param pos1: position tuple(x, y) of the first icon
        :param pos2: position tuple(x, y) of the second icon
        :return: True or False ,representing whether there is a path between two icons
        """
        def is_clear_path(x1, y1, x2, y2):
            if x1 == x2:
                step = 1 if y1 < y2 else -1
                for y in range(y1 + step, y2, step):
                    if self.board[x1][y] != ' ':
                        return False
                return True
            elif y1 == y2:
                step = 1 if x1 < x2 else -1
                for x in range(x1 + step, x2, step):
                    if self.board[x][y1] != ' ':
                        return False
                return True
            return False

        x1, y1 = pos1
        x2, y2 = pos2

        # Check direct horizontal or vertical paths
        if is_clear_path(x1, y1, x2, y2):
            return True

        # Check for one-bend paths
        for x in range(self.BOARD_SIZE[0]):
            if is_clear_path(x1, y1, x, y1) and is_clear_path(x, y1, x2, y2):
                return True
        for y in range(self.BOARD_SIZE[1]):
            if is_clear_path(x1, y1, x1, y) and is_clear_path(x1, y, x2, y2):
                return True

        return False

    def remove_icons(self, pos1, pos2):
        """
        remove the connected icons on the game board
        :param pos1: position tuple(x, y) of the first icon to be removed
        :param pos2: position tuple(x, y) of the second icon to be removed
        :return: None
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
        """
        for row in self.board:
            if any(icon != ' ' for icon in row):
                return False
        return True
