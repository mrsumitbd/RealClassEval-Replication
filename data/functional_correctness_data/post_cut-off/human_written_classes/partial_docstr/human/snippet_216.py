from typing import Dict, List, Optional, Tuple
import random

class CubeState:

    def __init__(self, seed: int, scramble_moves: int):
        self.seed = seed
        self.cube = Cube()
        self.message_history: List[Dict] = []
        self.actions: List[str] = []
        self.step_rewards: List[float] = []
        self.total_reward: float = 0.0
        self.num_steps: int = 0
        self.max_steps = 20
        self.reward_per_correctly_placed_cubie = 0.05
        self.curriculum_level = 0
        self.scramble_sequence: List[str] = []
        self.scramble_sequence_length: int = 0
        self.progress_history: List[float] = []
        random.seed(seed)
        self.cube.reset()
        self._scramble_cube(scramble_moves)
        self.progress_history.append(self.cube.count_solved_cubies())

    def _scramble_cube(self, num_moves: int):
        """Scramble the cube with random moves"""
        moves = ['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'", 'U2', 'D2', 'L2', 'R2', 'F2', 'B2']
        self.scramble_sequence = []
        for _ in range(num_moves):
            move = random.choice(moves)
            self.scramble_sequence.append(move)
            self.cube.rotate(move)
        self.scramble_sequence_length = len(self.scramble_sequence)
        return ' '.join(self.scramble_sequence)

    def apply_move(self, move: str) -> bool:
        """Apply a move to the cube and return success"""
        try:
            self.cube.rotate(move)
            self.actions.append(move)
            self.num_steps += 1
            self.progress_history.append(self.cube.count_solved_cubies())
            return True
        except Exception as e:
            logger.error(f'Error applying move {move}: {e}')
            return False

    def is_solved(self) -> bool:
        """Check if the cube is solved"""
        return self.cube.is_solved()

    def get_cube_state_visualization(self) -> str:
        """Get a text representation of the cube state for visualization"""
        return str(self.cube)