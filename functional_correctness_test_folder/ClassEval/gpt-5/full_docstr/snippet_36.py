class EightPuzzle:
    """
    This class is an implementation of the classic 8-puzzle game, including methods for finding the blank tile, making moves, getting possible moves, and solving the puzzle using a breadth-first search algorithm.
    """

    def __init__(self, initial_state):
        """
        Initializing the initial state of Eight Puzzle Game, stores in attribute self.initial_state.
        And set the goal state of this game, stores in self.goal_state. In this case, set the size as 3*3
        :param initial_state: a 3*3 size list of Integer, stores the initial state
        """
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        """
        Find the blank position of current state, which is the 0 element.
        :param state: a 3*3 size list of Integer, stores the current state.
        :return i, j: two Integers, represent the coordinate of the blank block.
        >>> eightPuzzle = EightPuzzle([[2, 3, 4], [5, 8, 1], [6, 0, 7]])
        >>> eightPuzzle.find_blank([[2, 3, 4], [5, 8, 1], [6, 0, 7]])
        (2, 1)
        """
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        raise ValueError("Blank tile (0) not found in state")

    def move(self, state, direction):
        """
        Find the blank block, then makes the board moves forward the given direction.
        :param state: a 3*3 size list of Integer, stores the state before moving.
        :param direction: str, only has 4 direction 'up', 'down', 'left', 'right'
        :return new_state: a 3*3 size list of Integer, stores the state after moving.
        >>> eightPuzzle = EightPuzzle([[2, 3, 4], [5, 8, 1], [6, 0, 7]])
        >>> eightPuzzle.move([[2, 3, 4], [5, 8, 1], [6, 0, 7]], 'left')
        [[2, 3, 4], [5, 8, 1], [0, 6, 7]]
        """
        i, j = self.find_blank(state)
        new_state = [row[:] for row in state]

        if direction == 'up':
            if i == 0:
                return state
            new_i, new_j = i - 1, j
        elif direction == 'down':
            if i == 2:
                return state
            new_i, new_j = i + 1, j
        elif direction == 'left':
            if j == 0:
                return state
            new_i, new_j = i, j - 1
        elif direction == 'right':
            if j == 2:
                return state
            new_i, new_j = i, j + 1
        else:
            raise ValueError(
                "Invalid direction. Use 'up', 'down', 'left', or 'right'.")

        new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
        return new_state

    def get_possible_moves(self, state):
        """
        According the current state, find all the possible moving directions. Only has 4 direction 'up', 'down', 'left', 'right'.
        :param state: a 3*3 size list of Integer, stores the current state.
        :return moves: a list of str, store all the possible moving directions according to the current state.
        >>> eightPuzzle = EightPuzzle([[2, 3, 4], [5, 8, 1], [6, 0, 7]])
        >>> eightPuzzle.get_possible_moves([[2, 3, 4], [5, 8, 1], [6, 0, 7]])
        ['up', 'left', 'right']
        """
        i, j = self.find_blank(state)
        moves = []
        if i > 0:
            moves.append('up')
        if i < 2:
            moves.append('down')
        if j > 0:
            moves.append('left')
        if j < 2:
            moves.append('right')
        return moves

    def solve(self):
        """
        Use BFS algorithm to find the path solution which makes the initial state to the goal method.
        Maintain a list as a queue, named as open_list, append the initial state.
        Always visit and pop the 0 index element, invoke get_possible_moves method find all the possible directions.
        Traversal the possible_moves list and invoke move method to get several new states.Then append them.
        redo the above steps until the open_list is empty or the state has changed to the goal state.
        :return path: list of str, the solution to the goal state.
        >>> eightPuzzle = EightPuzzle([[1, 2, 3], [4, 5, 6], [7, 0, 8]])
        >>> eightPuzzle.solve()
        ['right']
        """
        from collections import deque

        def to_tuple(state):
            return tuple(tuple(row) for row in state)

        start = to_tuple(self.initial_state)
        goal = to_tuple(self.goal_state)

        if start == goal:
            return []

        queue = deque([start])
        parents = {start: (None, None)}
        visited = {start}

        while queue:
            current = queue.popleft()
            current_list = [list(row) for row in current]

            if current == goal:
                break

            for mv in self.get_possible_moves(current_list):
                next_state = self.move(current_list, mv)
                next_t = to_tuple(next_state)
                if next_t not in visited:
                    visited.add(next_t)
                    parents[next_t] = (current, mv)
                    queue.append(next_t)
                    if next_t == goal:
                        queue.clear()
                        break

        if goal not in parents:
            return []

        path = []
        node = goal
        while parents[node][0] is not None:
            node, move_taken = parents[node]
            path.append(parents[to_tuple([list(r) for r in node])]
                        [1] if move_taken is None else move_taken)
        path.reverse()
        return path
