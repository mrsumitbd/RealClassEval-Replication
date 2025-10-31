from typing import Dict, List, Optional

class SolvingStrategy:
    """Base class for Rubik's cube solving strategies"""

    def __init__(self, name: str, description: str, difficulty: int, steps: List[str], example_algorithms: List[Dict[str, str]]=None, tips: List[str]=None):
        """
        Initialize a solving strategy

        Args:
            name: Strategy name
            description: Detailed description of the strategy
            difficulty: Difficulty level (1-5)
            steps: Ordered list of steps to follow
            example_algorithms: Common algorithms used in this strategy
            tips: Tips for using this strategy effectively
        """
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.steps = steps
        self.example_algorithms = example_algorithms or []
        self.tips = tips or []

    def get_prompt_section(self) -> str:
        """Get formatted prompt section for this strategy"""
        prompt = f'\nSTRATEGY: {self.name} (Difficulty: {self.difficulty}/5)\n\nDESCRIPTION:\n{self.description}\n\nSTEPS:\n'
        for i, step in enumerate(self.steps, 1):
            prompt += f'{i}. {step}\n'
        if self.example_algorithms:
            prompt += '\nCOMMON ALGORITHMS:\n'
            for algo in self.example_algorithms:
                prompt += f"- {algo['name']}: {algo['moves']} - {algo['purpose']}\n"
        if self.tips:
            prompt += '\nTIPS:\n'
            for tip in self.tips:
                prompt += f'- {tip}\n'
        return prompt

    def __str__(self) -> str:
        return f'{self.name} (Difficulty: {self.difficulty}/5)'