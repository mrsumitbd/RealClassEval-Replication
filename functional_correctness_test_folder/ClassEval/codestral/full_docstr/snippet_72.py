
class PushBoxGame:
    """
    This class implements a functionality of a sokoban game, where the player needs to move boxes to designated targets in order to win.
    """

    def __init__(self, map):
        """
        Initialize the push box game with the map and various attributes.
        :param map: list[str], the map of the push box game, represented as a list of strings.
            Each character on the map represents a different element, including the following:
            - '#' represents a wall that neither the player nor the box can pass through;
            - 'O' represents the initial position of the player;
            - 'G' represents the target position;
            - 'X' represents the initial position of the box.
        >>> map = ["#####", "#O  #", "# X #", "#  G#", "#####"]
        >>> game = PushBoxGame(map)
        """
        self.map = map
        self.player_row = 0
        self.player_col = 0
        self.targets = []
        self.boxes = []
        self.target_count = 0
        self.is_game_over = False
        self.init_game()

    def init_game(self):
        """
        Initialize the game by setting the positions of the player, targets, and boxes based on the map.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])
        >>> game.targets
        [(3, 3)]
        >>> game.boxes
        [(2, 2)]
        >>> game.player_row
        1
        >>> game.player_col
        1
        """
        for i, row in enumerate(self.map):
            for j, char in enumerate(row):
                if char == 'O':
                    self.player_row, self.player_col = i, j
                elif char == 'G':
                    self.targets.append((i, j))
                    self.target_count += 1
                elif char == 'X':
                    self.boxes.append((i, j))

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])
        >>> game.check_win()
        """
        self.is_game_over = all(box in self.targets for box in self.boxes)

    def move(self, direction):
        """
        Move the player based on the specified direction and check if the game is won.
        :param direction: str, the direction of the player's movement.
            It can be 'w', 's', 'a', or 'd' representing up, down, left, or right respectively.

        :return: True if the game is won, False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])
        >>> game.print_map()
        # # # # # #
        # O     # #
        #   X   # #
        #     G # #
        # # # # # #
        >>> game.move('d')
        False
        >>> game.move('s')
        False
        >>> game.move('a')
        False
        >>> game.move('s')
        False
        >>> game.move('d')
        True
        """
        row, col = self.player_row, self.player_col
        if direction == 'w':
            row -= 1
        elif direction == 's':
            row += 1
        elif direction == 'a':
            col -= 1
        elif direction == 'd':
            col += 1

        if self.map[row][col] == '#':
            return False

        if (row, col) in self.boxes:
            box_row, box_col = row, col
            if direction == 'w':
                box_row -= 1
            elif direction == 's':
                box_row += 1
            elif direction == 'a':
                box_col -= 1
            elif direction == 'd':
                box_col += 1

            if self.map[box_row][box_col] == '#' or (box_row, box_col) in self.boxes:
                return False

            self.boxes.remove((row, col))
            self.boxes.append((box_row, box_col))

        self.player_row, self.player_col = row, col
        self.check_win()
        return self.is_game_over

    def print_map(self):
        """
        Print the current state of the game map.
        """
        for i, row in enumerate(self.map):
            for j, char in enumerate(row):
                if (i, j) == (self.player_row, self.player_col):
                    print('O', end=' ')
                elif (i, j) in self.boxes:
                    print('X', end=' ')
                elif (i, j) in self.targets:
                    print('G', end=' ')
                else:
                    print(char, end=' ')
            print()
