
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
        for i in range(len(self.map)):
            row = self.map[i]
            for j in range(len(row)):
                char = row[j]
                if char == 'O':
                    self.player_row = i
                    self.player_col = j
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
        boxes_on_target = 0
        for box in self.boxes:
            if box in self.targets:
                boxes_on_target += 1
        self.is_game_over = (boxes_on_target == self.target_count)
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
        dr, dc = 0, 0
        if direction == 'w':
            dr = -1
        elif direction == 's':
            dr = 1
        elif direction == 'a':
            dc = -1
        elif direction == 'd':
            dc = 1

        new_row = self.player_row + dr
        new_col = self.player_col + dc

        if new_row < 0 or new_row >= len(self.map) or new_col < 0 or new_col >= len(self.map[0]):
            return False

        if self.map[new_row][new_col] == '#':
            return False

        box_index = -1
        for i, box in enumerate(self.boxes):
            if box == (new_row, new_col):
                box_index = i
                break

        if box_index != -1:
            new_box_row = new_row + dr
            new_box_col = new_col + dc

            if (new_box_row < 0 or new_box_row >= len(self.map) or
                    new_box_col < 0 or new_box_col >= len(self.map[0])):
                return False

            if (self.map[new_box_row][new_box_col] == '#' or
                    (new_box_row, new_box_col) in self.boxes):
                return False

            self.boxes[box_index] = (new_box_row, new_box_col)

        self.player_row = new_row
        self.player_col = new_col

        return self.check_win()

    def print_map(self):
        """
        Print the current state of the game map.
        """
        map_copy = [list(row) for row in self.map]
        for r, c in self.targets:
            if map_copy[r][c] != 'X':
                map_copy[r][c] = 'G'
        for r, c in self.boxes:
            map_copy[r][c] = 'X'
        if map_copy[self.player_row][self.player_col] == ' ':
            map_copy[self.player_row][self.player_col] = 'O'
        for row in map_copy:
            print(' '.join(row))
