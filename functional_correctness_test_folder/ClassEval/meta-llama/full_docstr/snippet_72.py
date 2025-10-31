
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
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.player_row = i
                    self.player_col = j
                elif cell == 'G':
                    self.targets.append((i, j))
                elif cell == 'X':
                    self.boxes.append((i, j))
        self.target_count = len(self.targets)

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"]) 
        >>> game.check_win()
        """
        count = sum(1 for box in self.boxes if box in self.targets)
        self.is_game_over = count == self.target_count
        return self.is_game_over

    def print_map(self):
        """
        Print the current state of the game map.
        """
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if (i, j) == (self.player_row, self.player_col):
                    print('O', end=' ')
                elif (i, j) in self.boxes:
                    print('X', end=' ')
                elif (i, j) in self.targets:
                    print('G', end=' ')
                else:
                    print(cell, end=' ')
            print()

    def move(self, direction):
        """
        Move the player based on the specified direction and check if the game is won.
        :param direction: str, the direction of the player's movement. 
            It can be 'w', 's', 'a', or 'd' representing up, down, left, or right respectively.

        :return: True if the game is won, False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"])       
        >>> game.print_map()
        # # # # # 
        # O     #
        #   X   #
        #     G #
        # # # # #
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
        directions = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        dr, dc = directions[direction]
        new_row, new_col = self.player_row + dr, self.player_col + dc

        if self.map[new_row][new_col] == '#':
            return self.is_game_over

        if (new_row, new_col) in self.boxes:
            box_new_row, box_new_col = new_row + dr, new_col + dc
            if self.map[box_new_row][box_new_col] == '#' or (box_new_row, box_new_col) in self.boxes:
                return self.is_game_over
            self.boxes.remove((new_row, new_col))
            self.boxes.append((box_new_row, box_new_col))

        self.player_row, self.player_col = new_row, new_col
        self.check_win()
        return self.is_game_over
