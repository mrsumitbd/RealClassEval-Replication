
class TicTacToe:
    """
    The class represents a game of Tic-Tac-Toe and its functions include making a move on the board, checking for a winner, and determining if the board is full.
    """

    def __init__(self, N=3):
        """
        Initialize a 3x3 game board with all empty spaces and current symble player, default is 'X'.
        """
        self.board = [[' ' for _ in range(N)] for _ in range(
            N)]  # Changed to N for a square board
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
        True
        >>> ttt.current_player
        'O'
        """
        if row < 0 or row >= len(self.board) or col < 0 or col >= len(self.board):
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
        >>> moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]
        >>> ttt = TicTacToe()
        >>> for move in moves:
        ...     ttt.make_move(move[0], move[1])
        >>> ttt.check_winner()
        'X'
        """
        N = len(self.board)
        # Check rows
        for row in self.board:
            if row.count(row[0]) == N and row[0] != ' ':
                return row[0]

        # Check columns
        for col in range(N):
            check = []
            for row in range(N):
                check.append(self.board[row][col])
            if check.count(check[0]) == N and check[0] != ' ':
                return check[0]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        return None

    def is_board_full(self):
        """
        Check if the game board is completely filled.
        :return: bool, indicating whether the game board is full or not
        >>> ttt = TicTacToe()
        >>> ttt.is_board_full()
        False
        """
        for row in self.board:
            if ' ' in row:
                return False
        return True


# Example usage
if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'ttt': TicTacToe()})
