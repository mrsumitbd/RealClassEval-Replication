import random
from typing import Any, Dict, List

class CurriculumLevel:
    """Represents a curriculum learning level for Rubik's cube solving"""

    def __init__(self, level: int, min_scramble_moves: int, max_scramble_moves: int, max_steps: int, reward_per_correctly_placed_cubie: float, example_patterns: List[List[str]]=None, description: str=None):
        """
        Initialize a curriculum level

        Args:
            level: Level number (higher is more difficult)
            min_scramble_moves: Minimum number of scramble moves
            max_scramble_moves: Maximum number of scramble moves
            max_steps: Maximum allowed steps to solve at this level
            reward_per_correctly_placed_cubie: Reward multiplier for correctly placed cubies
            example_patterns: Optional list of move sequences to learn at this level
            description: Human-readable description of this level
        """
        self.level = level
        self.min_scramble_moves = min_scramble_moves
        self.max_scramble_moves = max_scramble_moves
        self.max_steps = max_steps
        self.reward_per_correctly_placed_cubie = reward_per_correctly_placed_cubie
        self.example_patterns = example_patterns or []
        self.description = description or f'Level {level}: {min_scramble_moves}-{max_scramble_moves} scramble moves'

    def get_scramble_moves(self) -> int:
        """Get a random number of scramble moves within the level's range"""
        return random.randint(self.min_scramble_moves, self.max_scramble_moves)

    def __repr__(self) -> str:
        return f'CurriculumLevel(level={self.level}, scramble_moves={self.min_scramble_moves}-{self.max_scramble_moves})'