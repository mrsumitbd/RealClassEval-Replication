
class PushBoxGame:
    """
    This class implements a functionality of a sokoban game, where the player needs to move boxes to designated targets in order to win.
    """

    def __init__(self, map):
        """
        Initialize the push box game with the map and various attributes.
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
        """
        self.targets = []
        self.boxes = []
        self.player_row = 0
        self.player_col = 0
        for r, row in enumerate(self.map):
            for c, ch in enumerate(row):
                if ch == 'O':
                    self.player_row = r
                    self.player_col = c
                elif ch == 'G':
                    self.targets.append((r, c))
                elif ch == 'X':
                    self.boxes.append((r, c))
        self.target_count = len(self.targets)
        self.is_game_over = False

    def check_win(self):
        """
        Check if the game is won. The game is won when all the boxes are placed on target positions.
        And update the value of self.is_game_over.
        """
        # All boxes must be on targets
        win = all(box in self.targets for box in self.boxes)
        self.is_game_over = win
        return self.is_game_over

    def move(self, direction):
        """
        Move the player based on the specified direction and check if the game is won.
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
        pr, pc = self.player_row, self.player_col
        nr, nc = pr + dr, pc + dc

        # Check map bounds
        if not (0 <= nr < len(self.map) and 0 <= nc < len(self.map[0])):
            return self.check_win()

        # Check wall
        if self.map[nr][nc] == '#':
            return self.check_win()

        # Check if next cell is a box
        if (nr, nc) in self.boxes:
            # Try to push the box
            br, bc = nr + dr, nc + dc
            # Check bounds for box
            if not (0 <= br < len(self.map) and 0 <= bc < len(self.map[0])):
                return self.check_win()
            # Check if box can be pushed (not wall, not another box)
            if self.map[br][bc] == '#' or (br, bc) in self.boxes:
                return self.check_win()
            # Move box
            self.boxes[self.boxes.index((nr, nc))] = (br, bc)
            # Move player
            self.player_row, self.player_col = nr, nc
        else:
            # Move player if not wall or box
            self.player_row, self.player_col = nr, nc

        return self.check_win()

    def print_map(self):
        """
        Print the current map with player, boxes, and targets.
        """
        # Build a 2D array of chars
        rows = [list(row) for row in self.map]
        # Place targets (G)
        for r, c in self.targets:
            if rows[r][c] == ' ':
                rows[r][c] = 'G'
        # Place boxes (X)
        for r, c in self.boxes:
            if (r, c) == (self.player_row, self.player_col):
                continue  # Player on box
            if (r, c) in self.targets:
                rows[r][c] = 'X'  # Could use another char for box on target
            else:
                rows[r][c] = 'X'
        # Place player (O)
        pr, pc = self.player_row, self.player_col
        if (pr, pc) in self.targets:
            rows[pr][pc] = 'O'
        elif (pr, pc) in self.boxes:
            rows[pr][pc] = 'O'
        else:
            rows[pr][pc] = 'O'
        # Print
        for row in rows:
            print(' '.join(row))
