
from collections import deque
import copy


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
        raise ValueError("No blank tile found")

    def move(self, state, direction):
        """
        Find the blank block, then makes the board moves forward the given direction.
        :param state: a 3*3 size list of Integer, stores the state before moving.
        :param direction: str, only has 4 direction 'up', 'down', 'left', 'right'
        :return new_state: a 3*3 size list of Integer, stores the state after moving.
        >>> eightPuzzle.move([[2, 3, 4], [5, 8, 1], [6, 0, 7]], 'left')
        [[2, 3, 4], [5, 8, 1], [0, 6, 7]]
        """
        i, j = self.find_blank(state)
        new_state = copy.deepcopy(state)
        if direction == 'up':
            if i == 0:
                raise ValueError("Move up not possible")
            new_state[i][j], new_state[i -
                                       1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == 'down':
            if i == 2:
                raise ValueError("Move down not possible")
            new_state[i][j], new_state[i +
                                       1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == 'left':
            if j == 0:
                raise ValueError("Move left not possible")
            new_state[i][j], new_state[i][j -
                                          1] = new_state[i][j-1], new_state[i][j]
        elif direction == 'right':
            if j == 2:
                raise ValueError("Move right not possible")
            new_state[i][j], new_state[i][j +
                                          1] = new_state[i][j+1], new_state[i][j]
        else:
            raise ValueError("Invalid direction")
        return new_state

    def get_possible_moves(self, state):
        """
        According the current state, find all the possible moving directions. Only has 4 direction 'up', 'down', 'left', 'right'.
        :param state: a 3*3 size list of Integer, stores the current state.
        :return moves: a list of str, store all the possible moving directions according to the current state.
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
        start = tuple(tuple(row) for row in self.initial_state)
        goal = tuple(tuple(row) for row in self.goal_state)

        queue = deque()
        queue.append((start, []))
        visited = {start}

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            # Convert back to list of lists for move operations
            current_state = [list(row) for row in current]
            for move_dir in self.get_possible_moves(current_state):
                new_state_list = self.move(current_state, move_dir)
                new_state = tuple(tuple(row) for row in new_state_list)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [move_dir]))

        # If no solution found
        return []
