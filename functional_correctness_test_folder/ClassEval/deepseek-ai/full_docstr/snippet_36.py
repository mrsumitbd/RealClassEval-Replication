
from collections import deque


class EightPuzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def move(self, state, direction):
        new_state = [row[:] for row in state]
        i, j = self.find_blank(new_state)
        if direction == 'up' and i > 0:
            new_state[i][j], new_state[i -
                                       1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == 'down' and i < 2:
            new_state[i][j], new_state[i +
                                       1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == 'left' and j > 0:
            new_state[i][j], new_state[i][j -
                                          1] = new_state[i][j-1], new_state[i][j]
        elif direction == 'right' and j < 2:
            new_state[i][j], new_state[i][j +
                                          1] = new_state[i][j+1], new_state[i][j]
        return new_state

    def get_possible_moves(self, state):
        moves = []
        i, j = self.find_blank(state)
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
        queue = deque()
        queue.append((self.initial_state, []))
        visited = set()
        visited.add(tuple(tuple(row) for row in self.initial_state))

        while queue:
            current_state, path = queue.popleft()
            if current_state == self.goal_state:
                return path
            for move in self.get_possible_moves(current_state):
                new_state = self.move(current_state, move)
                state_tuple = tuple(tuple(row) for row in new_state)
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_state, path + [move]))
        return []
