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
        # Convert map to mutable list of lists for base map
        self.base_map = []
        for r, row in enumerate(self.map):
            base_row = []
            for c, ch in enumerate(row):
                if ch == 'O':
                    self.player_row, self.player_col = r, c
                    base_row.append(' ')
                elif ch == 'X':
                    self.boxes.append((r, c))
                    base_row.append(' ')
                elif ch == 'G':
                    self.targets.append((r, c))
                    base_row.append('G')
                else:
                    base_row.append(ch)
            self.base_map.append(base_row)
        self.target_count = len(self.targets)

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"]) 
        >>> game.check_win()
        """
        self.is_game_over = all(pos in self.targets for pos in self.boxes)
        return self.is_game_over

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
        dir_map = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if direction not in dir_map:
            return False
        dr, dc = dir_map[direction]
        new_r, new_c = self.player_row + dr, self.player_col + dc

        # Check bounds
        if not (0 <= new_r < len(self.base_map) and 0 <= new_c < len(self.base_map[0])):
            return False

        target_cell = self.base_map[new_r][new_c]
        # If wall, cannot move
        if target_cell == '#':
            return False

        # If there's a box at the new position
        if (new_r, new_c) in self.boxes:
            # Compute position beyond the box
            beyond_r, beyond_c = new_r + dr, new_c + dc
            if not (0 <= beyond_r < len(self.base_map) and 0 <= beyond_c < len(self.base_map[0])):
                return False
            beyond_cell = self.base_map[beyond_r][beyond_c]
            if beyond_cell == '#':
                return False
            if (beyond_r, beyond_c) in self.boxes:
                return False
            # Move the box
            self.boxes.remove((new_r, new_c))
            self.boxes.append((beyond_r, beyond_c))

        # Move the player
        self.player_row, self.player_col = new_r, new_c

        # Check win condition
        return self.check_win()

    def print_map(self):
        """
        Print the current state of the map with player, boxes, walls, targets, and empty spaces.
        """
        # Create a copy of base
