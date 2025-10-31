class TicTacToe:
    """
    The class represents a game of Tic-Tac-Toe and its functions include making a move on the board, checking for a winner, and determining if the board is full.
    """

    def __init__(self, N=3):
        """
        Initialize a 3x3 game board with all empty spaces and current symble player, default is 'X'.
        """
        self.N = N
        self.board = [[' ' for _ in range(N)] for _ in range(N)]
        self.current_player = 'X'

    def make_move(self, row, col):
        """
        Place the current player's mark at the specified position on the board and switch the mark.
        :param row: int, the row index of the position
        :param col: int, the column index of the position
        :return: bool, indicating whether the move was successful or not
        >>> ttt.current_player
        'X'
        >>> ttt.make_move(1, 1)
        >>> ttt.current_player
        'O'
        """
        if not (0 <= row < self.N and 0 <= col < self.N):
            return False
        if self.board[row][col] != ' ':
            return False
        self.board[row][col] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def check_winner(self):
        """
        Check if there is a winner on the board in rows, columns and diagonals three directions
        :return: str or None, the mark of the winner ('X' or 'O'), or None if there is no winner yet
        >>> moves = [(1, 0), (2, 0), (1, 1), (2, 1), (1, 2)]
        >>> for move in moves:
        ...     ttt.make_move(move[0], move[1])
        >>> ttt.check_winner()
        'X'
        """
        n = self.N
        b = self.board

        # Check rows
        for r in range(n):
            if b[r][0] != ' ' and all(b[r][c] == b[r][0] for c in range(n)):
                return b[r][0]

        # Check columns
        for c in range(n):
            if b[0][c] != ' ' and all(b[r][c] == b[0][c] for r in range(n)):
                return b[0][c]

        # Check main diagonal
        if b[0][0] != ' ' and all(b[i][i] == b[0][0] for i in range(n)):
            return b[0][0]

        # Check anti-diagonal
        if b[0][n - 1] != ' ' and all(b[i][n - 1 - i] == b[0][n - 1] for i in range(n)):
            return b[0][n - 1]

        return None

    def is_board_full(self):
        """
        Check if the game board is completely filled.
        :return: bool, indicating whether the game board is full or not
        >>> ttt.is_board_full()
        False
        """
        return all(cell != ' ' for row in self.board for cell in row)
