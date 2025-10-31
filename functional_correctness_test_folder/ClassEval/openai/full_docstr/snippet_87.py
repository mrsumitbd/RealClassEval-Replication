
class TicTacToe:
    """
    The class represents a game of Tic-Tac-Toe and its functions include making a move on the board,
    checking for a winner, and determining if the board is full.
    """

    def __init__(self, N=3):
        """
        Initialize an N×N game board with all empty spaces and current symbol player, default is 'X'.
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
        >>> ttt = TicTacToe()
        >>> ttt.current_player
        'X'
        >>> ttt.make_move(1, 1)
        True
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
        Check if there is a winner on the board in rows, columns and diagonals.
        :return: str or None, the mark of the winner ('X' or 'O'), or None if there is no winner yet
        >>> ttt = TicTacToe()
        >>> moves = [(1, 0), (2, 0), (1, 1), (2, 1), (1, 2)]
        >>> for move in moves:
        ...     ttt.make_move(move[0], move[1])
        >>> ttt.check_winner()
        'X'
        """
        lines = []

        # Rows and columns
        for i in range(self.N):
            lines.append(self.board[i])  # row
            lines.append([self.board[j][i] for j in range(self.N)])  # column

        # Diagonals
        lines.append([self.board[i][i]
                     for i in range(self.N)])  # main diagonal
        lines.append([self.board[i][self.N - 1 - i]
                     for i in range(self.N)])  # anti-diagonal

        for line in lines:
            if all(cell == 'X' for cell in line):
                return 'X'
            if all(cell == 'O' for cell in line):
                return 'O'
        return None

    def is_board_full(self):
        """
        Check if the game board is completely filled.
        :return: bool, indicating whether the game board is full or not
        >>> ttt = TicTacToe()
        >>> ttt.is_board_full()
        False
        """
        return all(cell != ' ' for row in self.board for cell in row)
