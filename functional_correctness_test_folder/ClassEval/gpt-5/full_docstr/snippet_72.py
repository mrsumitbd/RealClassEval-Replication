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
        self.map = map[:]  # keep original static map for walls/targets
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
        self.targets = []
        self.boxes = []
        self.player_row = 0
        self.player_col = 0
        for r, row in enumerate(self.map):
            for c, ch in enumerate(row):
                if ch == 'O':
                    self.player_row, self.player_col = r, c
                elif ch == 'G':
                    self.targets.append((r, c))
                elif ch == 'X':
                    self.boxes.append((r, c))
        self.target_count = len(self.targets)
        self.is_game_over = False

    def _is_wall(self, r, c):
        if r < 0 or r >= len(self.map):
            return True
        if c < 0 or c >= len(self.map[r]):
            return True
        return self.map[r][c] == '#'

    def _is_box(self, r, c):
        return (r, c) in self.boxes

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        :return self.is_game_over: True if all the boxes are placed on target positions, or False otherwise.
        >>> game = PushBoxGame(["#####", "#O  #", "# X #", "#  G#", "#####"]) 
        >>> game.check_win()
        """
        targets_set = set(self.targets)
        self.is_game_over = len(self.boxes) > 0 and all(
            b in targets_set for b in self.boxes)
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
        if self.is_game_over:
            return True

        dir_map = {
            'w': (-1, 0),
            's': (1, 0),
            'a': (0, -1),
            'd': (0, 1)
        }
        if direction not in dir_map:
            return self.check_win()

        dr, dc = dir_map[direction]
        nr, nc = self.player_row + dr, self.player_col + dc

        if self._is_wall(nr, nc):
            return self.check_win()

        if self._is_box(nr, nc):
            br, bc = nr + dr, nc + dc
            if self._is_wall(br, bc) or self._is_box(br, bc):
                return self.check_win()
            # push box
            # update box position
            idx = self.boxes.index((nr, nc))
            self.boxes[idx] = (br, bc)
            # move player
            self.player_row, self.player_col = nr, nc
        else:
            # move into empty/target cell
            self.player_row, self.player_col = nr, nc

        return self.check_win()

    def print_map(self):
        rows = len(self.map)
        for r in range(rows):
            line_chars = []
            cols = len(self.map[r])
            for c in range(cols):
                ch = ' '
                if self.map[r][c] == '#':
                    ch = '#'
                else:
                    if (r, c) == (self.player_row, self.player_col):
                        ch = 'O'
                    elif (r, c) in self.boxes:
                        ch = 'X'
                    elif self.map[r][c] == 'G':
                        ch = 'G'
                    else:
                        ch = ' '
                line_chars.append(ch)
            print(' '.join(line_chars) + ' ')
