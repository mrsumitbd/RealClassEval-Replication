import copy
import random
from typing import Any, Mapping, Optional, TypedDict

class SlidingPuzzleGameLogic:

    @staticmethod
    def generate(config: Mapping[str, Any]) -> dict[str, Any]:
        """Generate a new Sliding Puzzle."""
        size = config.get('size', 4)
        shuffle_moves = config.get('shuffle_moves', 100)
        grid = [[r * size + c + 1 for c in range(size)] for r in range(size)]
        grid[size - 1][size - 1] = 0
        solution = [row[:] for row in grid]
        empty_pos = (size - 1, size - 1)
        for _ in range(shuffle_moves):
            moves = []
            r, c = empty_pos
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = (r + dr, c + dc)
                if 0 <= nr < size and 0 <= nc < size:
                    moves.append((nr, nc))
            if moves:
                new_r, new_c = random.choice(moves)
                grid[r][c], grid[new_r][new_c] = (grid[new_r][new_c], grid[r][c])
                empty_pos = (new_r, new_c)
        return {'size': size, 'grid': grid, 'solution': solution, 'empty_pos': empty_pos, 'commands': {'up': 'Slide tile below empty space up', 'down': 'Slide tile above empty space down', 'left': 'Slide tile to the right of empty space left', 'right': 'Slide tile to the left of empty space right', 'view': 'View the current state of the board'}}

    @staticmethod
    def init(game_state: dict[str, Any]) -> str:
        """Initialize Sliding Puzzle game and return welcome message."""
        size = game_state['size']
        return f"\n===== SLIDING PUZZLE =====\nArrange the {size}x{size} grid by sliding tiles into the empty space.\n- The goal is to arrange numbers from 1 to {size * size - 1} in order\n- Use 'up', 'down', 'left', 'right' to slide in that direction\n- Use 'view' to see the current state of the board"

    @staticmethod
    def step(action: str, game_state: dict[str, Any]) -> tuple[str, float, bool, dict[str, Any]]:
        """Process an action in the Sliding Puzzle game."""
        size = game_state['size']
        grid = game_state['grid']
        empty_r, empty_c = game_state['empty_pos']
        response = "Unknown command. Type 'help' to see available commands."
        reward = 0.0
        is_terminated = False
        new_state = copy.deepcopy(game_state)
        move_made = False
        if action.startswith('slide '):
            try:
                _, r, c = action.split()
                r, c = (int(r) - 1, int(c) - 1)
                if not (0 <= r < size and 0 <= c < size):
                    return (f'Invalid position. Row/column must be between 1 and {size}.', reward, is_terminated, new_state)
                if abs(r - empty_r) + abs(c - empty_c) != 1:
                    return ('Tile must be adjacent to the empty space.', reward, is_terminated, new_state)
                new_state['grid'][empty_r][empty_c] = grid[r][c]
                new_state['grid'][r][c] = 0
                new_state['empty_pos'] = (r, c)
                move_made = True
                response = f'Slid tile {grid[r][c]} into the empty space.'
            except ValueError:
                return ('Invalid input format. Use: slide row col', reward, is_terminated, new_state)
        elif action in ['up', 'down', 'left', 'right']:
            if action == 'up':
                r, c = (empty_r + 1, empty_c)
                dir_text = 'up'
            elif action == 'down':
                r, c = (empty_r - 1, empty_c)
                dir_text = 'down'
            elif action == 'left':
                r, c = (empty_r, empty_c + 1)
                dir_text = 'left'
            elif action == 'right':
                r, c = (empty_r, empty_c - 1)
                dir_text = 'right'
            if 0 <= r < size and 0 <= c < size:
                new_state['grid'][empty_r][empty_c] = grid[r][c]
                new_state['grid'][r][c] = 0
                new_state['empty_pos'] = (r, c)
                move_made = True
                response = f'Slid tile {grid[r][c]} {dir_text}.'
            else:
                return (f'Cannot slide {dir_text}.', reward, is_terminated, new_state)
        if move_made:
            reward = 0
            if new_state['grid'] == new_state['solution']:
                response = "Congratulations! You've solved the puzzle!"
                reward = 1.0
                is_terminated = True
        return (response, reward, is_terminated, new_state)

    @staticmethod
    def render(game_state: dict[str, Any]) -> str:
        """Render the current Sliding Puzzle game state."""
        grid = game_state['grid']
        size = game_state['size']
        output = ['\n']
        max_digits = len(str(size * size - 1))
        output.append('  ' + '+' + '-' * (max_digits + 2) * size + '+')
        for i, row in enumerate(grid):
            row_str = f'{i + 1} |'
            for val in row:
                if val == 0:
                    row_str += ' ' * (max_digits + 2)
                else:
                    row_str += f' {val:>{max_digits}} '
            row_str += '|'
            output.append(row_str)
        output.append('  ' + '+' + '-' * (max_digits + 2) * size + '+')
        col_labels = '    '
        for i in range(size):
            col_labels += f'{i + 1:^{max_digits + 2}}'
        output.append(col_labels)
        return '\n'.join(output)